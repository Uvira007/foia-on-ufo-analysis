from pathlib import Path
from typing import Tuple, Optional

# base_dir -> points to src/
_base_dir = Path(__file__).resolve().parents[1]
_assets_root = _base_dir / "assets"

assets_images = _assets_root / "images"
assets_content = _assets_root / "content"
pages_html = _base_dir / "pages" / "html"