# PDF Content Analysis and Question Generation 

This project implements **Part 1** of the AI/Python Intern Assignment for PDF content extraction. The solution extracts text and images from PDF documents, specifically designed for educational content like IMO (International Mathematical Olympiad) papers.

##  Assignment Overview

The goal is to build a system that can process PDF documents and extract their contents (text and images), then use this information for AI-powered question generation. This repository covers **Part 1: PDF Content Extraction**.

## Features

- **Dual PDF Processing**: Supports both PyMuPDF (fast) and pdfplumber (precise) libraries
- **Text Extraction**: Extracts all textual content from PDF pages
- **Image Extraction**: Identifies and saves all images as separate files
- **Structured Output**: Creates organized JSON files with extracted content
- **Question Parsing**: Basic parsing of mathematical questions and their associated images
- **Command-Line Interface**: Easy-to-use CLI with multiple options
- **Robust Error Handling**: Comprehensive exception handling and logging
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Project Structure

```
pdf-content-extractor/
├── pdf_content_extractor.py    # Main extraction script
├── requirements.txt            # Python dependencies
├── README.md                  # This file
└── extracted_content/         # Output directory (created automatically)
    ├── images/               # Extracted images
    ├── questions.json        # Parsed questions
    ├── raw_pages.json        # Raw page data
    └── extraction.log        # Processing logs
```

##  Installation

### 1. Clone or Download the Project
```bash

```

### 2. Install Python Dependencies
```bash

pip install -r requirements.txt


pip install PyMuPDF pdfplumber Pillow
```

### 3. Verify Installation
```bash
python pdf_content_extractor.py --help
```

##  Usage

### Command Line Interface

#### Basic Usage
```bash

python pdf_content_extractor.py sample.pdf
```

#### Advanced Options
```bash

python pdf_content_extractor.py sample.pdf --method pymupdf --output results

python pdf_content_extractor.py sample.pdf --method pdfplumber


python pdf_content_extractor.py sample.pdf --verbose
```



### Programmatic Usage

```python
from pdf_content_extractor import PDFContentExtractor


extractor = PDFContentExtractor(output_dir="my_output")

questions = extractor.process_pdf("sample.pdf", method="pymupdf")


print(f"Found {len(questions)} questions")
```

##  Output Format

### JSON Structure (questions.json)
```json
[
  {
    "question": "What is the next figure?",
    "images": "path/to/question_image_1.png",
    "option_images": [
      "path/to/option_image_1.png",
      "path/to/option_image_2.png"
    ]
  }
]
```

### Raw Page Data (raw_pages.json)
```json
[
  {
    "page_number": 1,
    "text": "Extracted text content...",
    "images": ["path/to/image1.png", "path/to/image2.png"],
    "image_count": 2
  }
]
```


```

##  Example Workflow

1. **Place your PDF file** in the project directory
2. **Run the extraction**:
   ```bash
   python pdf_content_extractor.py "IMO class 1 sample.pdf"
   ```
3. **Check the results** in the `extracted_content/` directory:
   - `questions.json` - Parsed questions
   - `raw_pages.json` - Complete page data
   - `images/` - All extracted images
   - `extraction.log` - Processing log



## Contributing

Feel free to improve this solution by:
- Adding support for more PDF types
- Improving question parsing algorithms
- Enhancing image recognition capabilities
- Adding OCR support for scanned documents

##  License

This project is created for educational purposes as part of an internship assignment.

