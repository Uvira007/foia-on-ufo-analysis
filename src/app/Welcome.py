import sys
from pathlib import Path

# Adds 'src' to the system path
src_path = str(Path(__file__).resolve().parents[1])
if src_path not in sys.path:
    sys.path.append(src_path)
    
import streamlit as st
from PIL import Image
from utils.assets import assets_images, assets_content, pages_html

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
