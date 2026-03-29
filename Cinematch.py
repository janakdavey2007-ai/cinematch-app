"""
🎬 CINEMATCH PRO MAX
🔥 ChatGPT-style recommender + Animations + Full UX
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import time

st.set_page_config(page_title="CineMatch 🎬", layout="wide")

# =========================
# CSS (UNCHANGED STYLE)
# =========================
st.markdown("""
<style>
.main-header {
    font-size: 3.5rem;
    text-align: center;
    font-weight: bold;
    color: #6366f1;
}
.movie-card {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 1rem;
    border-radius: 15px;
    color: white;
    margin: 10px 0;
}
.chat-box {
    background: #1e293b;
    padding: 1rem;
    border-radius: 15px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================
@st.cache_data
def get_movies():
    return [
        "🎭 The Dark Knight", "🧠 Inception", "🌌 Interstellar",
        "🔫 Pulp Fiction", "🏃 Forrest Gump", "👨‍👦 The Godfather",
        "👊 Fight Club", "💾 The Matrix", "🎪 Goodfellas",
        "🕵️ Se7en", "💃 La La Land", "🚢 Titanic",
        "🦸 Avengers", "🕷️ Spider-Man", "🦹 Deadpool"
    ]

# =========================
# ENGINE
# =========================
class Engine:
    def __init__(self):
        self.movies = get_movies()
        self.ratings = {}
        self.recommendations = []

    def rate(self, movie, rating):
        self.ratings[movie] = rating
        self.generate()

    def generate(self):
        avg = np.mean(list(self.ratings.values())) if self.ratings else 3.5
        recs = []
        for m in self.movies:
            if m not in self.ratings:
                score = avg + random.uniform(-0.5, 0.8)
                recs.append((m, round(max(1, min(5, score)), 1)))
        self.recommendations = sorted(recs, key=lambda x: x[1], reverse=True)

    def chat_recommend(self, text):
        text = text.lower()
        if "action" in text or "hero" in text:
            return ["🎭 The Dark Knight", "🦸 Avengers", "🕷️ Spider-Man"]
        elif "love" in text or "romance" in text:
            return ["🚢 Titanic", "💃 La La Land"]
        elif "space" in text or "sci" in text:
            return ["🌌 Interstellar", "🧠 Inception"]
        else:
            return random.sample(self.movies, 3)

# =========================
# INIT
# =========================
if "engine" not in st.session_state:
    st.session_state.engine = Engine()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================
# HEADER
# =========================
st.markdown('<div class="main-header">🎬 CineMatch PRO MAX</div>', unsafe_allow_html=True)

# =========================
# TRENDING
# =========================
st.subheader("🔥 Trending Movies")
cols = st.columns(5)
for i, m in enumerate(st.session_state.engine.movies[:5]):
    with cols[i]:
        st.markdown(f'<div class="movie-card">{m}</div>', unsafe_allow_html=True)

# =========================
# MAIN
# =========================
col1, col2 = st.columns([1,2])

# LEFT PANEL
with col1:
    st.subheader("⭐ Rate Movies")

    movie = st.selectbox("Select Movie", st.session_state.engine.movies)
    rating = st.slider("Rating", 1.0, 5.0, 4.0, 0.5)

    if st.button("➕ Add Rating"):
        st.session_state.engine.rate(movie, rating)
        st.success("Added!")
        st.rerun()

    if st.button("🎲 Surprise Me"):
        m = random.choice(st.session_state.engine.movies)
        r = random.choice([3,4,5])
        st.session_state.engine.rate(m, r)
        st.success(f"{m} auto-rated {r}⭐")
        st.rerun()

    if st.button("🧹 Reset"):
        st.session_state.engine.ratings = {}
        st.session_state.engine.recommendations = []
        st.session_state.chat_history = []
        st.rerun()

# RIGHT PANEL
with col2:
    st.subheader("🎯 Recommendations")

    if st.session_state.engine.recommendations:
        for m, s in st.session_state.engine.recommendations[:5]:
            st.markdown(f'<div class="movie-card">{m} ⭐ {s}</div>', unsafe_allow_html=True)
    else:
        st.info("Rate movies to see recommendations")

# =========================
# CHATGPT STYLE CHAT
# =========================
st.markdown("---")
st.subheader("💬 AI Movie Chat")

user_input = st.text_input("Ask something like: 'Suggest action movies'")

if st.button("Send"):
    if user_input.strip() != "":
        st.session_state.chat_history.append(("You", user_input))

        with st.spinner("Thinking... 🤖"):
            time.sleep(1)
            response = st.session_state.engine.chat_recommend(user_input)

        reply = "I recommend: " + ", ".join(response)
        st.session_state.chat_history.append(("AI", reply))

# DISPLAY CHAT
for role, msg in st.session_state.chat_history:
    st.markdown(f'<div class="chat-box"><b>{role}:</b> {msg}</div>', unsafe_allow_html=True)

# =========================
# ANALYTICS
# =========================
if st.session_state.engine.ratings:
    st.markdown("---")
    st.subheader("📊 Your Ratings")

    vals = list(st.session_state.engine.ratings.values())
    fig = px.histogram(x=vals, nbins=5)
    st.plotly_chart(fig, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🎬 CineMatch PRO MAX | AI Recommender + Chat System")
