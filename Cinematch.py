"""
🎬 CINEMATCH PRO - ULTIMATE Movie Recommendation Experience
🔥 Hollywood-level animations + Real-time reactions + Superb UX
NO TensorFlow/NLTK! Pure Magic ✨
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import random
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(page_title="CineMatch 🎬", page_icon="🎬", layout="wide")

# =========================
# SUPERB CUSTOM CSS
# =========================
st.markdown("""
<style>
/* SAME CSS — NO CHANGE */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

.main-header {
    font-family: 'Inter', sans-serif;
    font-size: 4rem !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-weight: 800;
    margin-bottom: 1rem;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 20px #667eea; }
    to { text-shadow: 0 0 30px #764ba2; }
}

.hero-card {
    background: linear-gradient(145deg, #1e3a8a, #3b82f6);
    border-radius: 25px;
    padding: 2rem;
    color: white;
    box-shadow: 0 25px 50px rgba(0,0,0,0.25);
    animation: slideUp 1s ease-out;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(50px); }
    to { opacity: 1; transform: translateY(0); }
}

.movie-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 20px;
    padding: 1.5rem;
    color: white;
    margin: 1rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.movie-card:hover {
    transform: translateY(-10px) scale(1.02);
}

.recommendation-list {
    background: linear-gradient(135deg, #1e293b, #334155);
    border-radius: 20px;
    padding: 2rem;
    color: white;
}

.metric-glow {
    background: linear-gradient(45deg, #10b981, #059669);
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# MOVIE DATA
# =========================
@st.cache_data
def get_movies():
    return {
        "🎭 The Dark Knight": 5.0, "🧠 Inception": 4.8, "🌌 Interstellar": 4.7, "🔫 Pulp Fiction": 4.6,
        "🏃 Forrest Gump": 4.5, "👨‍👦 The Godfather": 4.9, "👊 Fight Club": 4.7, "💾 The Matrix": 4.6,
        "🎪 Goodfellas": 4.5, "🕵️ Se7en": 4.4, "💃 La La Land": 4.3, "🚢 Titanic": 4.2,
        "💕 The Notebook": 4.1, "😍 When Harry Met Sally": 4.0, "👗 Pretty Woman": 3.9,
        "🦸 Avengers": 4.4, "🔨 Iron Man": 4.3, "🕷️ Spider-Man": 4.2, "🦹 Deadpool": 4.1,
        "🐺 Logan": 4.3, "🍻 The Hangover": 3.8, "😎 Superbad": 3.9, "🚔 21 Jump Street": 3.7,
        "👨‍👧 Step Brothers": 3.8, "📺 Anchorman": 3.9
    }

# =========================
# RECOMMENDATION ENGINE (FIXED)
# =========================
class CineMatchPro:
    def __init__(self):
        self.movies = get_movies()
        self.ratings = {}
        self.recommendations = []
        
    def rate_movie(self, movie, rating):
        self.ratings[movie] = rating
        self._generate_recommendations()
    
    def _generate_recommendations(self):
        self.recommendations = []
        
        avg_rating = np.mean(list(self.ratings.values())) if self.ratings else 3.5
        unseen_movies = [m for m in self.movies if m not in self.ratings]
        
        temp_recs = []
        
        for movie in unseen_movies:
            base_score = self.movies[movie]
            user_bias = avg_rating - 3.5
            similarity_boost = random.uniform(0.8, 1.2)
            
            pred_score = base_score + user_bias * 0.5 * similarity_boost
            
            temp_recs.append({
                'movie': movie,
                'score': round(max(1.0, min(5.0, pred_score)), 1),
                'reason': self._get_reason(avg_rating)
            })
        
        # SORTING FIX
        self.recommendations = sorted(temp_recs, key=lambda x: x['score'], reverse=True)[:10]
    
    def _get_reason(self, avg_rating):
        reasons = {
            'high': ['Perfect match for your taste!', 'You\'ll love this!', 'Top recommendation!'],
            'medium': ['Great choice!', 'Highly recommended', 'Worth watching'],
            'low': ['Good option', 'Try this one', 'Not bad']
        }
        
        if avg_rating >= 4.2:
            return random.choice(reasons['high'])
        elif avg_rating >= 3.5:
            return random.choice(reasons['medium'])
        else:
            return random.choice(reasons['low'])

# Initialize
if 'engine' not in st.session_state:
    st.session_state.engine = CineMatchPro()

# =========================
# UI (UNCHANGED)
# =========================
st.markdown('<h1 class="main-header">🎬 CineMatch PRO</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center;font-size:1.5rem;color:#64748b;">Rate movies → Watch AI magic happen ✨</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    
    selected_movie = st.selectbox(
        "Choose movie:",
        options=list(st.session_state.engine.movies.keys())
    )
    
    rating = st.slider("⭐ Your rating:", 1.0, 5.0, 4.0, 0.5)
    
    if st.button("🎬 RATE MOVIE", use_container_width=True):
        st.session_state.engine.rate_movie(selected_movie, rating)
        st.success(f"{selected_movie} rated {rating}⭐")
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if st.session_state.engine.recommendations:
        for rec in st.session_state.engine.recommendations:
            st.markdown(f"**{rec['movie']}** → ⭐ {rec['score']}")

st.markdown("---")
st.metric("Movies Rated", len(st.session_state.engine.ratings))
