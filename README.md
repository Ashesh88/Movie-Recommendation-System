# 🎬 Movie Recommendation System  

An **interactive web application** that recommends movies using **content-based filtering**, powered by **TF-IDF vectorization** and **Pinecone vector search**.  
Deployed live on **Render**: [🎥 Try it here!](https://movie-recommendation-system-2w4k.onrender.com/)  

---

## 🚀 Overview  

This system suggests movies similar to a selected title by analyzing **movie metadata** such as genres, tags, and descriptions.  
Users can refine recommendations using **genre filters** and view **movie posters** directly within the interface.  

---

## ✨ Key Features  

✅ **Personalized Recommendations** – Get movies similar to your favorite title.  
✅ **Genre-Based Filtering** – Narrow results by selecting one or more genres.  
✅ **Interactive UI** – Built with Streamlit for a clean and responsive design.  
✅ **Poster Previews** – Movie posters fetched dynamically using the OMDB API.  
✅ **Fast Search** – Powered by Pinecone for efficient vector similarity matching.  

---

## 🧠 How It Works  

1. **Data Loading** – Import movie metadata (title, genres, tags).  
2. **Feature Extraction** – Apply TF-IDF vectorization to encode text-based features.  
3. **Vector Storage** – Store and query embeddings using Pinecone for fast similarity search.  
4. **Recommendation Generation** – Compute cosine similarity to find top related movies.  
5. **Visualization** – Display results with movie posters and metadata in the Streamlit interface.  

---

## 🛠 Tech Stack  

| Category | Technologies |
|-----------|--------------|
| **Programming Language** | Python |
| **Web Framework** | Streamlit |
| **Libraries** | Pandas, NumPy, Scikit-learn |
| **Database** | Pinecone (Vector Database) |
| **API** | OMDB API |
| **Deployment** | Render |

---


---

## 💡 Example Usage  

1. Select a movie from the dropdown (e.g., *Toy Story (1995)*)  
2. Click **Recommend**  
3. Instantly get a list of similar movies with their posters and genres  

---

## 🔮 Future Improvements  

- 🔗 Integrate **collaborative filtering** for user-based recommendations  
- 🎞 Expand dataset via **IMDb/TMDb API**  
- 🧍 Add **user profiles** and feedback-based learning  
- 📅 Introduce filters for **release year**, **popularity**, or **ratings**  
- 📈 Visualize similarity metrics for better interpretability  

---

## 👨‍💻 Author  

**Ashesh Singh**  
📎 GitHub: [Ashesh88](https://github.com/Ashesh88)  
🌐 Live App: [Movie Recommendation System](https://movie-recommendation-system-2w4k.onrender.com/)  

---


