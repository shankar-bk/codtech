from flask import Flask, request, render_template_string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

# Load and preprocess dataset
movies = pd.read_csv("movies.csv")
movies['genres'] = movies['genres'].fillna('')
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

# Recommendation function
def get_recommendations(title, top_n=5):
    idx = indices.get(title)
    if idx is None:
        return []
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices].tolist()
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    movie_title = ""
    if request.method == 'POST':
        movie_title = request.form['movie']
        recommendations = get_recommendations(movie_title)

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>🎬 Telugu Movie Recommender</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', sans-serif;
                background: #0f2027;  /* fallback */
                background: linear-gradient(to right, #2c5364, #203a43, #0f2027);
                overflow: hidden;
                color: #fff;
                text-align: center;
            }
            .bubbles {
                position: absolute;
                width: 100%;
                height: 100%;
                z-index: -1;
                overflow: hidden;
            }
            .bubble {
                position: absolute;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.1);
                animation: floatUp 20s linear infinite;
            }
            @keyframes floatUp {
                0% {
                    bottom: -100px;
                    transform: translateX(0) scale(0.5);
                }
                100% {
                    bottom: 110%;
                    transform: translateX(50px) scale(1);
                }
            }
            .container {
                margin-top: 100px;
                padding: 20px;
            }
            h1 {
                font-size: 48px;
                margin-bottom: 20px;
                color: #00ffd5;
            }
            form input[type="text"] {
                padding: 12px;
                width: 300px;
                border: none;
                border-radius: 5px;
                font-size: 18px;
                outline: none;
            }
            form input[type="submit"] {
                padding: 12px 20px;
                background-color: #00ffd5;
                border: none;
                color: #000;
                font-size: 18px;
                border-radius: 5px;
                margin-left: 10px;
                cursor: pointer;
            }
            .cards {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 30px;
            }
            .card {
                background: rgba(255, 255, 255, 0.05);
                padding: 15px 20px;
                margin: 10px;
                border-radius: 15px;
                width: 220px;
                transition: 0.3s;
                box-shadow: 0 0 15px rgba(0,0,0,0.3);
            }
            .card:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: scale(1.05);
            }
            .card i {
                font-size: 30px;
                margin-bottom: 10px;
                color: #00ffd5;
            }
            .footer {
                margin-top: 50px;
                font-size: 14px;
                color: #ccc;
            }
        </style>
    </head>
    <body>
        <div class="bubbles">
            {% for i in range(20) %}
            <div class="bubble" style="left: {{ loop.index * 5 }}%; width: {{ 10 + (loop.index % 5) * 5 }}px; height: {{ 10 + (loop.index % 5) * 5 }}px; animation-duration: {{ 10 + loop.index }}s;"></div>
            {% endfor %}
        </div>

        <div class="container">
            <h1><i class="fas fa-film"></i> Telugu Movie Recommender</h1>
            <form method="post">
                <input type="text" name="movie" placeholder="e.g., Pushpa: The Rise (2021)" value="{{ movie_title }}" required />
                <input type="submit" value="🎬 Recommend" />
            </form>

            {% if recommendations %}
                <div class="cards">
                    {% for movie in recommendations %}
                        <div class="card">
                            <i class="fas fa-clapperboard"></i>
                            <h3>{{ movie }}</h3>
                        </div>
                    {% endfor %}
                </div>
            {% elif movie_title %}
                <p style="margin-top: 30px; color: red;">No recommendations found for "<strong>{{ movie_title }}</strong>".</p>
            {% endif %}

            <div class="footer">
                Made with ❤️ by Shankar | Flask + Scikit-learn
            </div>
        </div>
    </body>
    </html>
    ''', recommendations=recommendations, movie_title=movie_title)

if __name__ == '__main__':
    app.run(debug=True)
