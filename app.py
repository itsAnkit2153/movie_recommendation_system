import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# Function to fetch movie poster
# ----------------------------
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=4d6ca2caecfbb0bf8418511c20ba28da&language=en-US'
        )
        data = response.json()
        return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"

# ----------------------------
# Function to recommend movies
# ----------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = cosine_similarity([vectors[movie_index]], vectors)

    movies_list = sorted(
        list(enumerate(distances[0])),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# ----------------------------
# Load Data
# ----------------------------
movies = pickle.load(open('movies.pkl', 'rb'))
vectors = pickle.load(open('vectors.pkl', 'rb'))
movies_list = movies['title'].values

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# ----------------------------
# Custom CSS (No background image)
# ----------------------------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
        }

        .main {
            background-color: rgba(0,0,0,0);
        }

        .title {
            text-align: center;
            color: #ffcc00;
            font-size: 45px;
            font-weight: 800;
            text-shadow: 2px 2px 4px #000000;
            margin-bottom: 20px;
        }

        .stSelectbox label {
            font-size: 20px;
            font-weight: bold;
            color: #ffcc00;
        }

        .stButton>button {
            background-color: #ffcc00;
            color: black;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            padding: 10px 25px;
            transition: 0.3s;
            font-size: 18px;
        }

        .stButton>button:hover {
            background-color: #ffd633;
            transform: scale(1.05);
        }

        .movie-card {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: 0.3s;
        }

        .movie-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }

        .movie-title {
            color: #ffcc00;
            font-weight: bold;
            margin-top: 10px;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Streamlit UI
# ----------------------------
st.markdown("<h1 class='title'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "🎥 Select a movie you like:",
    movies_list
)

if st.button('✨ Recommend'):
    with st.spinner('🔍 Finding similar movies...'):
        names, posters = recommend(selected_movie_name)

    st.markdown("## 🎯 Recommended Movies")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(
                f"""
                <div class='movie-card'>
                    <img src="{posters[i]}" width="200" style="border-radius:10px;">
                    <p class='movie-title'>{names[i]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
