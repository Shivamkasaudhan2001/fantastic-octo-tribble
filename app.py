import pickle
import time
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{movie_id}?api_key=36a2144a52c92f83dcbaef27b0f9d3c3&language=en-US".format(movie_id=movie_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

           # Retry up to 3 times
    for attempt in range(3):
            try:
                data = requests.get(url, headers=headers, timeout=10)
                data.raise_for_status()  # Check for HTTP errors
                json_data = data.json()
                
                if 'poster_path' in json_data and json_data['poster_path']:
                    full_path = "https://image.tmdb.org/t/p/w500/" + json_data['poster_path']
                    return full_path
                else:
                    return "https://via.placeholder.com/500x750?text=No+Poster"
                    
            except requests.exceptions.ConnectionError:
                if attempt < 2:  # Don't sleep on last attempt
                    time.sleep(2)  # Wait 2 seconds before retry
                continue
                
            except Exception as e:
                st.warning(f"Could not fetch poster: {e}")
                return "https://via.placeholder.com/500x750?text=No+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
     recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
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




