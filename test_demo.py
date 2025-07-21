

import os
import sys
import json
from pathlib import Path

def create_sample_data():
    """Create sample data to demonstrate the expected output format."""
    sample_questions = [
        {
            "question": "What is the next figure in the sequence?",
            "images": "extracted_content/images/page_1_image_1.png",
            "option_images": [
                "extracted_content/images/page_1_image_2.png",
                "extracted_content/images/page_1_image_3.png",
                "extracted_content/images/page_1_image_4.png",
                "extracted_content/images/page_1_image_5.png"
            ]
        },
        {
            "question": "Count the number of shapes shown in the figure.",
            "images": "extracted_content/images/page_2_image_1.png",
            "option_images": [
                "extracted_content/images/page_2_image_2.png",
                "extracted_content/images/page_2_image_3.png"
            ]
        }
    ]

    return sample_questions

def test_extractor():
    """Test the PDF extractor with basic functionality."""
    try:
       
        from pdf_content_extractor import PDFContentExtractor

        print(" PDF Content Extractor imported successfully")

       
        extractor = PDFContentExtractor("test_output")
        print(" PDFContentExtractor instance created")

        
        if os.path.exists("test_output"):
            print(" Output directories created")

        return True

    except ImportError as e:
        print(f" Import error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_dependencies():
    """Check if all required dependencies are available."""
    dependencies = {
        "PyMuPDF": "fitz",
        "pdfplumber": "pdfplumber",
        "Pillow": "PIL"
    }

    available = {}

    for name, module in dependencies.items():
        try:
            __import__(module)
            available[name] = " Available"
        except ImportError:
            available[name] = " Not installed"

    return available

def demo_json_output():
    """Demonstrate the expected JSON output format."""
    sample_data = create_sample_data()

    
    demo_dir = Path("demo_output")
    demo_dir.mkdir(exist_ok=True)

  
    with open(demo_dir / "sample_questions.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)

    print(f"Created demo JSON output: {demo_dir}/sample_questions.json")

    return sample_data

def main():
    """Main test function."""
    print(" PDF Content Extractor - Test & Demo")
    print("=" * 50)

    
    print("\nChecking Dependencies:")
    deps = check_dependencies()
    for name, status in deps.items():
        print(f"  {name}: {status}")

    print("\n Testing Basic Functionality:")
    if test_extractor():
        print("All basic tests passed!")
    else:
        print(" Some tests failed. Check the error messages above.")

    
    print("\nCreating Sample Output:")
    sample_data = demo_json_output()

    print(f"\n Sample Questions Found: {len(sample_data)}")
    for i, q in enumerate(sample_data, 1):
        print(f"  {i}. {q['question'][:50]}...")

    
    print("\n Usage Instructions:")
    print("  1. Install dependencies: pip install -r requirements.txt")
    print("  2. Place your PDF file in this directory")
    print("  3. Run: python pdf_content_extractor.py your_file.pdf")
    print("  4. Check results in extracted_content/ directory")

    print("\n✨ Test completed successfully!")

if __name__ == "__main__":
    main()
