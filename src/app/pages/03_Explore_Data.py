import streamlit as st
import numpy as np
import pandas as pd
from utils.assets import assets_images, pages_html

import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from wordcloud import WordCloud

st.sidebar.image( str(assets_images / "explore.png"), width=True)
st.sidebar.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .header{padding: 10px 16px; background: #555; color: #f1f1f1; position:fixed;top:0;} .sticky { position: fixed; top: 0; width: 100%;} </style><div class="header" id="myHeader">FOIA Document Analysis</div>', unsafe_allow_html=True)

style = open( str(pages_html / "style.html"))
st.markdown( style.read(), unsafe_allow_html=True )

chevron = open( str(pages_html / "explore.html"))
st.markdown(chevron.read(), unsafe_allow_html=True)


ready = False
maxK = 0

try:
    x = st.session_state.pdf_lst
    maxK = len(x)-1
    if maxK > 1:
      ready = True
    else:
      st.warning( "Please process more than one PDF file and then try again." )
except AttributeError:
    ready = False
    st.warning( "Please start by processing PDF files and then try again." )

if ready:

  vectorizer = TfidfVectorizer(stop_words='english',lowercase=True)
  
  X = vectorizer.fit_transform(st.session_state.pdf_lst)

  from sklearn.cluster import KMeans
  from sklearn.metrics import silhouette_score

  #
  Sum_of_squared_distances = []
  Silhouette_scores = []
  if( maxK > 20 ):
    maxK = 20
  K = range(2, maxK+1)
  for k in K:
      km = KMeans(n_clusters=k, max_iter=100, n_init=40)
      km = km.fit(X)
      label=km.predict(X)
      Silhouette_scores.append( silhouette_score(X, label) )
      #print('Silhouette Score(n=(' + str(k) + '): {' + str(s) + '}')
      Sum_of_squared_distances.append(km.inertia_)
  
  plt.figure( 1 )
  plt.plot(K, Sum_of_squared_distances, 'bx-')
  plt.xlabel('k')
  plt.ylabel('Sum of Squared Distances')
  plt.title('Elbow Method For Optimal k')
  st.pyplot(plt)
  
  plt.figure(2)
  plt.plot(K, Silhouette_scores, 'bx-')
  plt.xlabel('k')
  plt.ylabel('Silhouette Score')
  plt.title('Silhouette Score For Optimal k')
  st.pyplot(plt)

  true_k = st.slider( "Number of Clusters", min_value=0, max_value=maxK, value=0 )

  if st.button("Calculate") and true_k > 0:
      model = KMeans(n_clusters=true_k, init='k-means++')
      model.fit(X)
      labels=model.labels_
      wiki_cl=pd.DataFrame(list(zip(st.session_state.titles,st.session_state.counts,st.session_state.quality,labels)),columns=['title','count','quality','cluster'])
      print(wiki_cl.sort_values(by=['cluster']))
      
      result={'cluster':labels,'wiki':st.session_state.pdf_lst}
      result=pd.DataFrame(result)
  
      for k in range(0,true_k):
          s=result[result.cluster==k]
          text=s['wiki'].str.cat(sep=' ')
          text=text.lower()
          text=' '.join([word for word in text.split()])
          wordcloud = WordCloud(width=800, height=400, max_words=80, background_color="white").generate(text)
          print('Cluster: {}'.format(k))
          titles=wiki_cl[wiki_cl.cluster==k]['title']
          numDocs = len(titles)
          
          counts=wiki_cl[wiki_cl.cluster==k]['count']
          avgLength = sum(counts) / numDocs
          
          qualities=wiki_cl[wiki_cl.cluster==k]['quality']

          plt.figure(figsize=(14,6))
          plt.imshow(wordcloud, interpolation="bilinear")
          plt.axis("off")
          st.subheader( "Cluster #" + str(k+1) + ", Number of Docs = " + str( numDocs )+ ", Avg. Doc Length = {:.2f}".format( avgLength )  )
          st.pyplot(plt)
          
          import pandas
          from collections import Counter

          key_order= ['L', 'M', 'H']

          plt.figure()
          letter_counts = Counter(qualities)
          ordered_letter_counts = {k: letter_counts[k] for k in key_order }
          print( ordered_letter_counts )
          df = pandas.DataFrame.from_dict(ordered_letter_counts, orient='index')
          ax = df.plot.bar( legend=None )
          ax.set_xlabel( "Document Quality")
          ax.set_ylabel( "Number of Documents in Cluster #" + str(k+1))
          st.pyplot( plt )
          
          

