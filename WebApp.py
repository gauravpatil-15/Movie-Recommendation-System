import streamlit as st
import pickle
import pandas as pd
import requests  # To hit the API


# Loading movies as dictionary & also similarity matrix
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# To fetch the movie's poster using API
def fetch_poster(movie_id) :
    respose = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = respose.json()
    
    # data['poster_path'] was not the full image path..
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])
    
    recommended_movies = []
    recommended_movie_poster = []

    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))

        recommended_movies.append(movies.iloc[i[0]].title)

    # Returning both movie names and their posters
    return recommended_movies, recommended_movie_poster

st.title("Movie Recommender System")

st.text('Enter the movie name for which you want similar suggestions..')
selected_movie_name = st.selectbox(" "
    , movies['title'].values,
    label_visibility='collapsed')

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 =  st.columns(5)

    with col1:
        st.image(posters[0])
        st.text(names[0])

    with col2:
        st.image(posters[1])
        st.text(names[1])

    with col3:
        st.image(posters[2])
        st.text(names[2])

    with col4:
        st.image(posters[3])
        st.text(names[3])

    with col5:
        st.image(posters[4])
        st.text(names[4])