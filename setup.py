

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f" Python 3.6+ is required. Current version: {version.major}.{version.minor}")
        return False
    else:
        print(f" Python version {version.major}.{version.minor} is compatible")
        return True

def install_dependencies():
    """Install required dependencies."""
    print("\n Installing dependencies...")

    requirements = [
        "PyMuPDF>=1.23.0",
        "pdfplumber>=0.9.0", 
        "Pillow>=9.0.0"
    ]

    for requirement in requirements:
        try:
            print(f"Installing {requirement}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f" {requirement} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f" Failed to install {requirement}: {e}")
            return False

    return True

def verify_installation():
    """Verify that all libraries are properly installed."""
    print("\n🔍 Verifying installation...")

    libraries = {
        "PyMuPDF": "fitz",
        "pdfplumber": "pdfplumber", 
        "Pillow": "PIL"
    }

    all_good = True
    for name, module in libraries.items():
        try:
            __import__(module)
            print(f" {name} is working correctly")
        except ImportError as e:
            print(f"{name} failed to import: {e}")
            all_good = False

    return all_good

def create_sample_directory():
    """Create a sample directory structure."""
    print("\n Creating sample directory structure...")

    directories = [
        "sample_pdfs",
        "output_results", 
        "temp_workspace"
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")

def display_next_steps():
    """Display next steps for the user."""
    print("\n Setup completed successfully!")
    print("\nNext Steps:")
    print("1. Place your PDF file in the sample_pdfs/ directory")
    print("2. Run the extraction:")
    print("   python pdf_content_extractor.py sample_pdfs/your_file.pdf")
    print("3. Check results in the extracted_content/ directory")
    print("\n For more help:")
    print("   python pdf_content_extractor.py --help")
    print("   python test_demo.py")

def main():
    """Main setup function."""
    print("🔧 PDF Content Extractor - Setup Script")
    print("=" * 50)

    
    if not check_python_version():
        sys.exit(1)

    
    if not install_dependencies():
        print(" Failed to install some dependencies. Please install manually:")
        print("   pip install PyMuPDF pdfplumber Pillow")
        sys.exit(1)

    
    if not verify_installation():
        print(" Some libraries failed verification. Please check the installation.")
        sys.exit(1)

    
    create_sample_directory()

    
    display_next_steps()

if __name__ == "__main__":
    main()
