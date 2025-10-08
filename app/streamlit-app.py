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
    movie_id = movie_info['movieId']
    return movie_id

def recommend_movies(movie_title, data, top_k, selected_genres):
    movie_id = get_movie_id_by_title(movie_title, data)
    if not movie_id:
        return []

    query_response = index.query(
        id=str(movie_id),
        top_k=top_k + 1,
        include_metadata=True
    )

    if not query_response or 'matches' not in query_response:
        st.write("No matches found for the movie.")
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
    st.set_page_config(
        page_title="Movie Recommender",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for title, search box, and background
    st.markdown("""<style>
        body { background-color: #f0f2f6; }
        .title { 
            font-size: 40px; 
            font-weight: 800; 
            color: #1F2937; 
            text-align: center; 
            margin-bottom: 30px; 
            font-family: 'Arial', sans-serif;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        .stSelectbox>div>div>div { 
            background-color: #ffffff; 
            color: #1F2937; 
            border-radius: 8px; 
        }
        .stSelectbox>div>div>div>div { color: #1F2937; }
    </style>""", unsafe_allow_html=True)

    st.markdown('<div class="title">🎬 Movie Recommendation System</div>', unsafe_allow_html=True)

    data = load_data()
    if data is None or data.empty:
        st.write("Error: Data not loaded correctly.")
        return

    movie_title = st.selectbox("Select a Movie", data['title'].values)
    genres_list = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime',
                   'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                   'IMAX', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    selected_genres = [genre for genre in genres_list if st.sidebar.checkbox(genre)]

    if st.button('Recommend'):
        recommended_movies = recommend_movies(movie_title, data, 12, selected_genres)

        if not recommended_movies:
            st.write("No recommendations found.")
        else:
            num_columns = 3
            rows = [recommended_movies[i:i + num_columns] for i in range(0, len(recommended_movies), num_columns)]

            for row in rows:
                cols = st.columns(num_columns)
                for col, movie in zip(cols, row):
                    poster_url = get_movie_poster(movie['imdb_id'])
                    with col:
                        st.markdown(f"""
                            <div class="movie-card">
                                <img src="{poster_url}" class="movie-image" />
                                <div class="movie-title">{movie['movie_name']}</div>
                                <div class="movie-genres">Genres: {movie['movie_genre']}</div>
                            </div>
                        """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
