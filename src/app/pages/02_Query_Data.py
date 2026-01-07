import streamlit as st
from modules.vector_space.vectorSpace import VectorSpace  # generate Vector space model
from utils.assets import assets_images, pages_html

st.sidebar.image(str(assets_images / "query.png"), width=True)
st.sidebar.write(
    '<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .header{padding: 10px 16px; background: #555; color: #f1f1f1; position:fixed;top:0;} .sticky { position: fixed; top: 0; width: 100%;} </style><div class="header" id="myHeader">FOIA Document Analysis</div>',
    unsafe_allow_html=True)

style = open(str(pages_html / "style.html"))
st.markdown(style.read(), unsafe_allow_html=True)

chevron = open(str(pages_html / "query.html"))
st.markdown(chevron.read(), unsafe_allow_html=True)

ready = False

try:
    x = st.session_state.pdf_lst
    if( len(x) > 0 ):
      ready = True
    else:
      st.warning("Please start by processing PDF files and then try again.")
except AttributeError:
    ready = False
    st.warning("Please start by processing PDF files and then try again.")
    
prev_qry = ""

# if processing is completed perform the retrieval else ask the user to perform processing.
if ready:
    v = VectorSpace()
    query = st.text_input("Terms of Query", value="")  # Query term to be searched for in the document collections.
    rank = st.number_input("Number of Documents to Return", 1, 600, 10)  # no.of. documents to be retrieved.
    if st.button("Search") or ( prev_qry != query ): # Check if button clicked
        prev_qry = query
        if (query != '') & (rank > 0): #Check if there is a search term entered and no.of. documents to retrieve is > 0
            st.dataframe(v.query_vectorizer(query, rank)) #fit a vector space model and retrieve the document names and content.
        else:
            st.warning("No search term or results found.") # warning to user
