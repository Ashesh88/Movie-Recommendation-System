import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
from pinecone.grpc import PineconeGRPC as Pinecone
import logging
from preprocessings import load_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# Initialize Pinecone using your API key
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("movie-recommendation-system")

def get_movie_id_by_title(movie_title, data):
    movie_info = data[data['title'] == movie_title].iloc[0]
    return movie_info['movieId']

def recommend_movies(movie_title, data, top_k, selected_genres):
    movie_id = get_movie_id_by_title(movie_title, data)
    query_response = index.query(
        id=str(movie_id),
        top_k=top_k + 1,
        include_metadata=True
    )

    if not query_response or 'matches' not in query_response:
        return []

    recommended_movies = []
    for match in query_response['matches'][1:top_k + 1]:
        metadata = match.get('metadata', {})
        movie_id = int(match['id'])
        movie_name = metadata.get('movie_name', 'Unknown Title')
        movie_genre = metadata.get('movie_genre', 'Unknown Genre').split()
        if selected_genres and not set(selected_genres).intersection(movie_genre):
            continue
        imdb_id = data[data['movieId'] == movie_id]['imdbId'].values[0]
        recommended_movies.append({
            'movie_id': movie_id,
            'movie_name': movie_name,
            'movie_genre': " ".join(movie_genre),
            'imdb_id': imdb_id
        })
    return recommended_movies

def get_movie_poster(imdb_id):
    if not imdb_id:
        return ""
    url = f"http://www.omdbapi.com/?i=tt{str(imdb_id).zfill(7)}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get('Poster', '')

def main():
    st.set_page_config(page_title="Movie Recommender", layout="wide", initial_sidebar_state="expanded")

    # Custom CSS
    st.markdown("""<style>
    body { background-color: #f3f4f6; font-family: 'Arial', sans-serif; }
    .title { font-size: 40px; font-weight: 700; color: #1F2937; text-align: center; margin-bottom: 40px; }
    .movie-card { border-radius: 15px; overflow: hidden; box-shadow: 0 10px 20px rgba(0,0,0,0.2); transition: transform 0.3s ease, box-shadow 0.3s ease; margin: 10px; background: linear-gradient(to bottom, #ffffff, #f0f0f0); text-align: center; padding: 10px; height: 100%; }
    .movie-card:hover { transform: translateY(-5px) scale(1.03); box-shadow: 0 15px 25px rgba(0,0,0,0.3); }
    .movie-image { width: 100%; height: 300px; object-fit: cover; border-radius: 10px; }
    .movie-title { font-size: 18px; font-weight: 600; color: #111827; margin-top: 10px; min-height: 50px; }
    .movie-genres { font-size: 14px; color: #6B7280; margin-top: 5px; }
    .scroll-container { display: flex; overflow-x: auto; padding-bottom: 10px; }
    .scroll-container::-webkit-scrollbar { display: none; }
    .sidebar .stCheckbox label { font-size: 14px; }
    </style>""", unsafe_allow_html=True)

    st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)

    data = load_data()
    if data is None or data.empty:
        st.write("Error: Data not loaded correctly.")
        return

    # Sidebar - genre filter
    st.sidebar.header("Filter by Genre")
    genres_list = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                   'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                   'IMAX', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    selected_genres = [genre for genre in genres_list if st.sidebar.checkbox(genre)]

    movie_title = st.selectbox("Select a Movie", data['title'].values)

    if st.button('Recommend'):
        recommended_movies = recommend_movies(movie_title, data, 20, selected_genres)
        if not recommended_movies:
            st.write("No recommendations found.")
        else:
            # Horizontally scrollable carousel
            st.markdown('<h3 style="color:#1F2937; margin-top:30px;">Recommended Movies</h3>', unsafe_allow_html=True)
            st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
            for movie in recommended_movies:
                poster_url = get_movie_poster(movie['imdb_id'])
                st.markdown(f"""
                <div class="movie-card" style="min-width:200px;">
                    <img src="{poster_url}" class="movie-image" />
                    <div class="movie-title">{movie['movie_name']}</div>
                    <div class="movie-genres">{movie['movie_genre']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()

