import sys
import os
from pathlib import Path

# Anchor to project root (foia-analysis)
# Since Welcome.py is in src/app/, we go up 2 levels
REPO_ROOT = Path(__file__).resolve().parents[2]

# Add the project root to sys.path so 'from src.app...' works
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

# Now use absolute imports from the root
from src.app.utils.assets import assets_images, assets_content, pages_html
from src.config.nltk_setup import ensure_nltk_resources

import streamlit as st
from PIL import Image
from utils.assets import assets_images, assets_content, pages_html

# Run the setup script before any other logic
ensure_nltk_resources()

style_path = str(pages_html / "style.html")
style = open(style_path).read()
st.markdown( style, unsafe_allow_html=True )

st.sidebar.image(str(assets_images / "home.png"), width=True)
st.sidebar.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .header{padding: 10px 16px; background: #555; color: #f1f1f1; position:fixed;top:0;} .sticky { position: fixed; top: 0; width: 100%;} </style><div class="header" id="myHeader">FOIA Document Analysis</div>', unsafe_allow_html=True)

title_alignment="""
<style>
#team-ufo {
  text-align: center
}
</style>
"""
st.markdown(title_alignment, unsafe_allow_html=True)

colT1,colT2,colT3 = st.columns(3)
with colT2:
  st.title("Team UFO")
  st.markdown( "<p style=\"text-align: center;\">FOIA Document Analysis</p>", unsafe_allow_html=True)
with colT1:
  ufoImg = Image.open(str(assets_images / 'favpng_roswell-unidentified-flying-object-sprite.png'))
  st.image(ufoImg, width=200)
with colT3:
  tsImg = Image.open(str(assets_images / 'favpng_united-states-youtube-clip-art.png'))
  st.image( tsImg, width=275 )

intro = open( str(assets_content / "intro.md"))

sections = open( str(assets_content / "sections.md"))

st.markdown( intro.read() )

st.markdown( sections.read() )
