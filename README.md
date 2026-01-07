# UFO - FOIA Analysis

## Short description
- Streamlit app for exploring and analyzing FOIA documents.

## Quick setup
1. Create a virtual environment and install requirements:
   - python -m venv .venv
   - .venv\Scripts\activate
   - pip install -r requirements.txt

## How to run
- Recommended (keeps package context): from the repository root
  - python -m src.app.Welcome
- Streamlit (PowerShell):
  - $env:PYTHONPATH="src"; streamlit run src/app/Welcome.py
- Streamlit (cmd):
  - set PYTHONPATH=src&& streamlit run src/app/Welcome.py

## Import and package notes
- The project uses a small helper in src/app/utils/assets.py that resolves asset directories reliably (works both when running as a package and when using a direct run/fallback).
- Preferred imports (relative, from repo root):
  - from utils.assets import assets_images, assets_content, pages_html

## VS Code configuration (for IntelliSense & analysis)
- Add a .env with:
  - PYTHONPATH=./src
- Add to .vscode/settings.json:
  - {
      "python.analysis.extraPaths": ["./src"]
    }

## Package markers
- If you add or refactor packages, ensure package markers exist:
  - src/__init__.py
  - src/app/__init__.py
  - src/app/utils/__init__.py

## Assets helper (example)
- src/app/utils/assets.py exposes:
  - APP_DIR, assets_images, assets_content, pages_html
  - get_assets_paths()
- Usage example:
  - from src.app.utils.assets import assets_images, assets_content, pages_html

## Troubleshooting
- If you run Welcome.py directly and see relative import errors, run as a module or switch to absolute imports and set PYTHONPATH to include ./src.
- For Streamlit, easiest is to set PYTHONPATH as shown above before running.

## Testing
- No tests configured in the repo (add tests under tests/ and run with your preferred test runner).
