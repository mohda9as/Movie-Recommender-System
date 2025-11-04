import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    """Fetch movie poster using TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0507e1097d16ac9046424633bd0df36a&language=en-US"
    try:
        data = requests.get(url)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Error+Loading"

def recommend(movie):
    """Recommend top 5 similar movies."""
    index = movieF[movieF['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movieF.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movieF.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

movie_dict = pickle.load(open('moviee.pkl', 'rb'))
movieF = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.header('🎬 Movie Recommender System')

movie_list = movieF['title'].values
selected_movie = st.selectbox("Select a movie ", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
