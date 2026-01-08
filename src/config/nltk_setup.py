import nltk

def ensure_nltk_resources():
    # Download required NLTK resources quietly
    for res in ('punkt_tab', 'stopwords', 'wordnet'):
        try:
            nltk.data.find(f'tokenizers/{res}')
        except LookupError:
            nltk.download(res, quiet=True)

if __name__ == '__main__':
    ensure_nltk_resources()