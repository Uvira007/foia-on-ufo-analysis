# src/app/pages/process_data.py
import sys
from pathlib import Path

# --- PATH FIX FOR PORTABILITY ---
# Resolve the path to the 'src' directory
# __file__ is src/app/pages/process_data.py -> .parents[2] is src/
src_root = str(Path(__file__).resolve().parents[2])
if src_root not in sys.path:
    sys.path.insert(0, src_root)
# --------------------------------

from modules.data_processor.process import process_pdfs
import streamlit as st
import pandas as pd
import advertools as adv
import matplotlib.pyplot as plt2
import numpy as np
from collections import Counter
from utils.assets import assets_images, pages_html
# ... (keep other imports: pandas, advertools, etc.)

st.sidebar.image( str(assets_images / "process.png"), width=True)
st.sidebar.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .header{padding: 10px 16px; background: #555; color: #f1f1f1; position:fixed;top:0;} .sticky { position: fixed; top: 0; width: 100%;} </style><div class="header" id="myHeader">FOIA Document Analysis</div>', unsafe_allow_html=True)


style = open( str(pages_html / "style.html"))
st.markdown(style.read(), unsafe_allow_html=True)

chevron = open( str(pages_html / "process.html"))
st.markdown(chevron.read(), unsafe_allow_html=True)

dict = {''}

st.session_state.pdf_lst = []
st.session_state.titles = []
st.session_state.counts = []
st.session_state.quality = []

st.session_state.dfAllData = pd.DataFrame()

uploaded_files = st.file_uploader("Choose a file", type=['pdf'], accept_multiple_files=True)

if uploaded_files:
    if st.button("Process Documents"):
        with st.spinner('Processing files...'):
            progress_bar = st.progress(0, text="Starting...")
            def update_progress(percent, text):
                progress_bar.progress(percent, text=text)
            # Call the extracted function
            results = process_pdfs(uploaded_files, progress_callback=update_progress)
            
            progress_bar.empty()
            # Update session state
            st.session_state.pdf_lst = results["texts"]
            st.session_state.titles = results["titles"]
            st.session_state.counts = results["counts"]
            st.session_state.quality = results["qualities"]
            
            st.session_state.dfAllData = pd.DataFrame({
                'text': results["texts"],
                'fileName': results["titles"],
                'wordCount': results["counts"]
            })

        st.success(f"Imported {len(results['titles'])} PDFs. Dictionary size: {results['dict_size']}")
        
        st.session_state.dfAllData['text'] = st.session_state.pdf_lst
        st.session_state.dfAllData['fileName'] = st.session_state.titles
        st.session_state.dfAllData['wordCount'] = st.session_state.counts
#  st.session_state.dfAllData['lineCount'] = lineCount
  
        df = pd.DataFrame(st.session_state.pdf_lst, columns=['value'])
        word_freq = adv.word_frequency(text_list=df['value'])
        
        frequency = word_freq.sort_values(by='abs_freq', ascending=False).head(25)
        
        # rearrange your data
        labels = frequency['word']
        values = frequency['abs_freq']
        
        indexes = np.arange(len(labels))
        
        plt2.barh(indexes, values)
        
        # add labels
        
        plt2.yticks(indexes, labels, rotation=0)
        plt2.title("Top 25 Frequent Words & Terms")
        
        ax = plt2.gca()
        ax.set_xlabel("Frequency of Word/Term")
        ax.set_ylabel("Word/Term")
        
        plt2.tight_layout()  # pad=1.08, h_pad=None, w_pad=None, rect=None)
        
        st.pyplot( plt2 )
        
        key_order= ['L', 'M', 'H']
        
        plt2.figure()
        letter_counts = Counter(st.session_state.quality)
        ordered_letter_counts = {k: letter_counts[k] for k in key_order }
        print( ordered_letter_counts )
        df = pd.DataFrame.from_dict(ordered_letter_counts, orient='index')
        ax = df.plot.bar( legend=None )
        ax.set_xlabel( "Document Quality")
        ax.set_ylabel( "Number of Documents in Collection")
        st.pyplot( plt2 )



