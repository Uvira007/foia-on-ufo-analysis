import nltk
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords

class VectorSpace:
    def __init__(self, df: pd.DataFrame = None):
        # df can be passed in or read from session_state at runtime
        if df is None:
            if 'dfAllData' in st.session_state:
                df = st.session_state['dfAllData']
            else:
                raise RuntimeError("Provide a dataframe or set st.session_state['dfAllData']")
        self.df = df
        self.texts = self.df['text'].tolist()
        # ensure stopwords exist
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            self.stop_words = set(stopwords.words('english'))
        self.cleaned_text = []
        self.doc_vector = None

    def preprocess_doc(self):
        if self.cleaned_text:
            return
        for doc in self.texts:
            tokens = self.tokenize_text(doc)
            doc_text = self.remove_stopwords(tokens)
            final_text = self.word_stemmer(doc_text)
            final_text = ' '.join(final_text)
            self.cleaned_text.append(final_text)

    def tokenize_text(self, doc_text):
        try:
            return nltk.word_tokenize(doc_text)
        except LookupError:
            # newer NLTK uses punkt_tab; download if missing
            nltk.download('punkt_tab', quiet=True)
            return nltk.word_tokenize(doc_text)

    def word_stemmer(self, token_list):
        ps = nltk.stem.PorterStemmer()
        return [ps.stem(word) for word in token_list]

    def remove_stopwords(self, token_list):
        return [w for w in token_list if w.lower() not in self.stop_words]

    def query_vectorizer(self, query: str, rank: int = 10) -> pd.DataFrame:
        self.preprocess_doc()
        vectorizer = TfidfVectorizer()
        vectorizer.fit(self.cleaned_text)
        self.doc_vector = vectorizer.transform(self.cleaned_text)

        tokens = self.tokenize_text(query)
        tokens = self.remove_stopwords(tokens)
        q = ' '.join(self.word_stemmer(tokens))
        query_vector = vectorizer.transform([q])

        cosine_similarities = cosine_similarity(self.doc_vector, query_vector).flatten()
        related_docs_indices = cosine_similarities.argsort()[:-(rank+1):-1]

        doc_rows = self.df[['fileName', 'text']].iloc[related_docs_indices]
        filteredDoc = pd.DataFrame(doc_rows)
        filteredDoc.columns = ['File Name', 'Content']
        filteredDoc = filteredDoc.assign(SNo=range(1, len(filteredDoc)+1)).set_index('SNo')
        return filteredDoc