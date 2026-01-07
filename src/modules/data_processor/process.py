# src/modules/data_processor/process.py
import pandas as pd
from pdfminer.high_level import extract_text
from nltk.corpus import wordnet
import streamlit as st

def process_pdfs(uploaded_files, progress_callback = None):
    """
    Processes uploaded PDFs and returns a dictionary of results.
    """
    pdf_lst = []
    titles = []
    counts = []
    qualities = []
    unique_words = set()
    total_files = len(uploaded_files)
    for i, uploaded_file in enumerate(uploaded_files):
        #Notify the UI on progress
        if progress_callback:
            progress_callback(i/total_files, f"Processing {uploaded_file.name}...")
        doc_string = ""
        raw_text = extract_text(uploaded_file)
        words = raw_text.split()
        
        word_count = 0
        for w in words:
            # Matches your logic: length > 2 and exists in wordnet
            if len(w) > 2 and len(wordnet.synsets(w)) > 0:
                doc_string += w.lower() + " "
                word_count += 1
                unique_words.add(w.lower())

        if word_count > 2:
            if word_count < 100:
                quality = 'L'
            elif word_count < 1000:
                quality = 'M'
            else:
                quality = 'H'
            
            pdf_lst.append(doc_string)
            titles.append(uploaded_file.name)
            counts.append(word_count)
            qualities.append(quality)
    
    if progress_callback:
        progress_callback(1.0, "Processing complete.")

    return {
        "texts": pdf_lst,
        "titles": titles,
        "counts": counts,
        "qualities": qualities,
        "dict_size": len(unique_words)
    }
