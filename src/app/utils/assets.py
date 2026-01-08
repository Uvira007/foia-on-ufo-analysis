from pathlib import Path

# Since assets.py is in src/app/utils/, go up 3 levels to reach foia-analysis
REPO_ROOT = Path(__file__).resolve().parents[3]

# Build paths precisely from the root
_app_root = REPO_ROOT / "src" / "app"
assets_images = _app_root / "assets" / "images"
assets_content = _app_root / "assets" / "content"
pages_html = _app_root / "pages" / "html"