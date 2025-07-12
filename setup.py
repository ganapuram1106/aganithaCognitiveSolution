#!/usr/bin/env python3
"""
Setup script for PubMed Research Paper Fetcher

This script helps users set up the environment and test the installation.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed:")
        print(f"  Error: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"✗ Python 3.7 or higher is required. Current version: {version.major}.{version.minor}")
        return False
    else:
        print(f"✓ Python version {version.major}.{version.minor}.{version.micro} is compatible")
        return True


def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("✗ requirements.txt not found")
        return False
    
    # Install dependencies
    success = run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )
    
    return success


def test_imports():
    """Test if all required modules can be imported."""
    print("\nTesting imports...")
    
    required_modules = [
        'requests',
        'pandas', 
        'Bio',
        'argparse'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} imported successfully")
        except ImportError as e:
            print(f"✗ Failed to import {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n✗ Failed to import: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✓ All required modules imported successfully")
        return True


def create_sample_files():
    """Create sample files for testing."""
    print("\nCreating sample files...")
    
    # Create sample queries file if it doesn't exist
    if not os.path.exists('sample_queries.txt'):
        sample_queries = """# Sample queries for PubMed Research Paper Fetcher
# Lines starting with # are comments and will be ignored
# One query per line

cancer immunotherapy
diabetes treatment
COVID-19 vaccine
Alzheimer's disease
breast cancer"""
        
        with open('sample_queries.txt', 'w') as f:
            f.write(sample_queries)
        print("✓ Created sample_queries.txt")
    
    # Create .gitignore if it doesn't exist
    if not os.path.exists('.gitignore'):
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
myenv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.csv
test_results.csv
batch_results_*.csv
pubmed_results.csv
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("✓ Created .gitignore")
    
    return True


def print_usage_examples():
    """Print usage examples."""
    print("\n" + "="*60)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\nUSAGE EXAMPLES:")
    print("-" * 30)
    
    print("\n1. Basic usage:")
    print("   python pubmed_fetcher.py -q \"cancer immunotherapy\" -e \"your.email@example.com\"")
    
    print("\n2. With custom output file:")
    print("   python pubmed_fetcher.py -q \"diabetes treatment\" -e \"researcher@university.edu\" -o results.csv")
    
    print("\n3. Limited results:")
    print("   python pubmed_fetcher.py -q \"COVID-19 vaccine\" -e \"scientist@company.com\" -m 25")
    
    print("\n4. Batch processing from file:")
    print("   python batch_processor.py -f sample_queries.txt -e \"your.email@example.com\"")
    
    print("\n5. Batch processing with specific queries:")
    print("   python batch_processor.py -q \"cancer immunotherapy\" \"diabetes treatment\" -e \"researcher@university.edu\"")
    
    print("\n6. Test the installation:")
    print("   python test_pubmed_fetcher.py")
    
    print("\nIMPORTANT NOTES:")
    print("-" * 30)
    print("• You must provide a valid email address for NCBI E-utilities")
    print("• The tool respects NCBI's rate limits (0.1 second delay between requests)")
    print("• Results are saved as CSV files")
    print("• You can customize keywords and settings in config.py")
    
    print("\nFor more information, see README.md")


def main():
    """Main setup function."""
    print("="*60)
    print("PubMed Research Paper Fetcher - Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        print("\n✗ Setup failed: Incompatible Python version")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n✗ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n✗ Setup failed: Could not import required modules")
        sys.exit(1)
    
    # Create sample files
    if not create_sample_files():
        print("\n✗ Setup failed: Could not create sample files")
        sys.exit(1)
    
    # Print usage examples
    print_usage_examples()
    
    print("\n" + "="*60)
    print("Setup completed successfully!")
    print("You can now use the PubMed Research Paper Fetcher.")
    print("="*60)


if __name__ == "__main__":
    main() 