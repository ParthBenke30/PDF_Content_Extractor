

import os
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional


try:
    import fitz  
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


class PDFContentExtractor:
    """
    A comprehensive PDF content extraction tool that handles text and image extraction
    from PDF files, specifically designed for educational content like math olympiad papers.
    """

    def __init__(self, output_dir: str = "extracted_content"):
        """
        Initialize the PDF content extractor.

        Args:
            output_dir (str): Directory to save extracted images and JSON output
        """
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.extracted_data = []

        
        self._create_directories()

        
        self._setup_logging()

    def _create_directories(self):
        """Create necessary output directories if they don't exist."""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            self.images_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created output directories: {self.output_dir}")
        except OSError as e:
            raise OSError(f"Failed to create directories: {e}")

    def _setup_logging(self):
        """Setup logging configuration."""
        log_file = self.output_dir / "extraction.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def extract_with_pymupdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract content using PyMuPDF (fitz) - fastest and most comprehensive.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            List[Dict]: Extracted content organized by pages
        """
        if not PYMUPDF_AVAILABLE:
            raise ImportError("PyMuPDF is not available. Install with: pip install PyMuPDF")

        self.logger.info(f"Extracting content from {pdf_path} using PyMuPDF")

        try:
            doc = fitz.open(pdf_path)
            page_data = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)

                text = page.get_text()

                
                image_list = page.get_images(full=True)
                page_images = []

                for img_index, img in enumerate(image_list):
                    try:
                        
                        xref = img[0]
                        pix = fitz.Pixmap(doc, xref)

                        if pix.n - pix.alpha > 3:
                            pix = fitz.Pixmap(fitz.csRGB, pix)

                        
                        image_name = f"page_{page_num + 1}_image_{img_index + 1}.png"
                        image_path = self.images_dir / image_name
                        pix.save(str(image_path))

                        page_images.append(str(image_path))
                        self.logger.info(f"Saved image: {image_name}")

                        pix = None  

                    except Exception as e:
                        self.logger.warning(f"Failed to extract image {img_index} from page {page_num + 1}: {e}")

                
                page_info = {
                    "page_number": page_num + 1,
                    "text": text.strip(),
                    "images": page_images,
                    "image_count": len(page_images)
                }
                page_data.append(page_info)

            doc.close()
            self.logger.info(f"Successfully extracted content from {len(page_data)} pages")
            return page_data

        except Exception as e:
            self.logger.error(f"Error extracting with PyMuPDF: {e}")
            raise

    def extract_with_pdfplumber(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract content using pdfplumber - excellent for text and table extraction.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            List[Dict]: Extracted content organized by pages
        """
        if not PDFPLUMBER_AVAILABLE:
            raise ImportError("pdfplumber is not available. Install with: pip install pdfplumber")

        self.logger.info(f"Extracting content from {pdf_path} using pdfplumber")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                page_data = []

                for page_num, page in enumerate(pdf.pages):
                    
                    text = page.extract_text() or ""

                    images = page.images
                    page_images = []

                    for img_index, img in enumerate(images):
                        
                        image_info = {
                            "x0": img.get("x0", 0),
                            "y0": img.get("y0", 0),
                            "x1": img.get("x1", 0),
                            "y1": img.get("y1", 0),
                            "width": img.get("width", 0),
                            "height": img.get("height", 0)
                        }
                        page_images.append(image_info)

                    page_info = {
                        "page_number": page_num + 1,
                        "text": text.strip(),
                        "images": [],  
                        "image_metadata": page_images,
                        "image_count": len(page_images)
                    }
                    page_data.append(page_info)

                self.logger.info(f"Successfully extracted content from {len(page_data)} pages")
                return page_data

        except Exception as e:
            self.logger.error(f"Error extracting with pdfplumber: {e}")
            raise

    def parse_math_questions(self, page_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Parse the extracted content to identify math questions and their associated images.
        This is specifically designed for IMO-style math papers.

        Args:
            page_data (List[Dict]): Raw extracted page data

        Returns:
            List[Dict]: Structured question data matching the assignment's JSON format
        """
        questions = []

        for page in page_data:
            text = page["text"]
            page_images = page["images"]

            
            lines = text.split('\n')
            current_question = ""
            question_images = []
            option_images = []

            for line in lines:
                line = line.strip()

                
                if not line:
                    continue

                
                if any(keyword in line.lower() for keyword in ["question", "what", "which", "find", "solve", "calculate"]):
                    
                    if current_question:
                        questions.append({
                            "question": current_question.strip(),
                            "images": question_images[0] if question_images else "",
                            "option_images": option_images
                        })

                    
                    current_question = line
                    question_images = page_images[:1] if page_images else []  
                    option_images = page_images[1:] if len(page_images) > 1 else []  

                else:
                    
                    if current_question:
                        current_question += " " + line

            if current_question:
                questions.append({
                    "question": current_question.strip(),
                    "images": question_images[0] if question_images else "",
                    "option_images": option_images
                })

        self.logger.info(f"Parsed {len(questions)} questions from the PDF")
        return questions

    def save_json_output(self, data: List[Dict[str, Any]], filename: str = "extracted_content.json"):
        """
        Save the extracted and parsed data to a JSON file.

        Args:
            data (List[Dict]): Data to save
            filename (str): Output JSON filename
        """
        output_path = self.output_dir / filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Saved JSON output to: {output_path}")
            print(f"JSON output saved to: {output_path}")

        except Exception as e:
            self.logger.error(f"Error saving JSON output: {e}")
            raise

    def process_pdf(self, pdf_path: str, method: str = "pymupdf") -> List[Dict[str, Any]]:
        """
        Main method to process a PDF file and extract all content.

        Args:
            pdf_path (str): Path to the PDF file
            method (str): Extraction method ("pymupdf" or "pdfplumber")

        Returns:
            List[Dict]: Processed question data
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        self.logger.info(f"Starting PDF processing: {pdf_path}")

        
        if method.lower() == "pymupdf":
            page_data = self.extract_with_pymupdf(pdf_path)
        elif method.lower() == "pdfplumber":
            page_data = self.extract_with_pdfplumber(pdf_path)
        else:
            raise ValueError(f"Unknown extraction method: {method}")

        
        questions = self.parse_math_questions(page_data)

        
        self.save_json_output(questions, "questions.json")
        self.save_json_output(page_data, "raw_pages.json")

        return questions


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="PDF Content Extraction Tool for Math Olympiad Papers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_extractor.py sample.pdf
  python pdf_extractor.py sample.pdf --method pdfplumber --output results
  python pdf_extractor.py sample.pdf --method pymupdf --output /path/to/output
        """
    )

    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file to process"
    )

    parser.add_argument(
        "--method",
        choices=["pymupdf", "pdfplumber"],
        default="pymupdf",
        help="PDF extraction method (default: pymupdf)"
    )

    parser.add_argument(
        "--output",
        default="extracted_content",
        help="Output directory for results (default: extracted_content)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Check library availability
    if args.method == "pymupdf" and not PYMUPDF_AVAILABLE:
        print("Error: PyMuPDF is not installed. Install with: pip install PyMuPDF")
        return 1

    if args.method == "pdfplumber" and not PDFPLUMBER_AVAILABLE:
        print("Error: pdfplumber is not installed. Install with: pip install pdfplumber")
        return 1

    if not PILLOW_AVAILABLE:
        print("Warning: Pillow is not installed. Image processing may be limited.")

    try:
    
        extractor = PDFContentExtractor(output_dir=args.output)
        questions = extractor.process_pdf(args.pdf_path, method=args.method)

        
        print(f"\nExtraction completed successfully!")
        print(f"- Total questions found: {len(questions)}")
        print(f"- Output directory: {args.output}")
        print(f"- Method used: {args.method}")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
