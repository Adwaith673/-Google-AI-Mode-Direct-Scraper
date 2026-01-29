#!/usr/bin/env python3
"""
Wrapper script to run the scraper directly from the source code
without needing to install the package via pip.
"""
import sys
import os

# Add the 'src' directory to Python path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.insert(0, src_path)

try:
    from google_ai_scraper.main import main
except ImportError as e:
    print("❌ Error: Could not import the project modules.")
    print(f"Debug info: Looking in {src_path}")
    print(f"Python Error: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("🚀 Starting Google AI Scraper via wrapper...")
    main()