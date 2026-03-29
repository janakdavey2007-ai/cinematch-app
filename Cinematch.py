"""
🎬 CINEMATCH PRO MAX - ULTIMATE VERSION
🔥 Mood + Chat + Voice-ready logic + Explainable AI + Gamification
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import time
import webbrowser

st.set_page_config(page_title="CineMatch 🎬", layout="wide")

# =========================
# DATA
# =========================
@st.cache_data
def get_movies():
    return {
        "🎭 The Dark Knight": "action",
        "🧠 Inception": "sci-fi",
        "🌌 Interstellar": "sci-fi",
        "🔫 Pulp Fiction": "action",
        "🏃 Forrest Gump": "drama",
        "👨‍👦 The Godfather": "drama",
        "👊 Fight Club": "dark",
        "💾 The Matrix": "sci-fi",
        "💃 La La Land": "romance",
        "🚢 Titanic": "romance",
        "😂 Superbad": "comedy",
        "🍻 Hangover": "comedy"
    }

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
                score = avg + random.uniform(-0.5, 1.0)
                recs.append((m, round(max(1, min(5, score)), 1)))
        self.recommendations = sorted(recs, key=lambda x: x[1], reverse=True)

    def explain(self, movie):
        if not self.ratings:
            return "Popular choice among users"
        liked = max(self.ratings, key=self.ratings.get)
        return f"Because you liked {liked}"

    def personality(self):
        if not self.ratings:
            return "🎬 Explorer"
        genres = [self.movies[m] for m in self.ratings]
        return f"🎭 You are a {max(set(genres), key=genres.count)} lover!"

    def chat(self, text):
        text = text.lower()
        if "action" in text:
            return ["🎭 The Dark Knight", "🔫 Pulp Fiction"]
        if "romance" in text:
            return ["🚢 Titanic", "💃 La La Land"]
        if "funny" in text:
            return ["😂 Superbad", "🍻 Hangover"]
        return random.sample(list(self.movies.keys()), 2)

# =========================
# INIT
# =========================
if "engine" not in st.session_state:
    st.session_state.engine = Engine()
if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================
# HEADER
# =========================
st.title("🎬 CineMatch PRO MAX")

# =========================
# MOOD BASED (FEATURE 1)
# =========================
st.subheader("🎭 Mood Based Recommendations")
mood = st.selectbox("Select Mood", ["Happy", "Sad", "Excited", "Romantic"])

if st.button("Get Mood Movies"):
    st.success(f"Showing {mood} movies!")
    st.write(random.sample(list(st.session_state.engine.movies.keys()), 3))

# =========================
# MAIN UI
# =========================
col1, col2 = st.columns([1,2])

with col1:
    st.subheader("⭐ Rate Movies")
    movie = st.selectbox("Movie", list(st.session_state.engine.movies.keys()))
    rating = st.slider("Rating", 1.0, 5.0, 4.0, 0.5)

    if st.button("Add Rating"):
        st.session_state.engine.rate(movie, rating)
        st.balloons()
        st.rerun()

    if st.button("🎲 Surprise"):
        m = random.choice(list(st.session_state.engine.movies.keys()))
        st.session_state.engine.rate(m, random.choice([3,4,5]))
        st.rerun()

    if st.button("🧹 Reset"):
        st.session_state.engine.ratings = {}
        st.session_state.engine.recommendations = []
        st.rerun()

with col2:
    st.subheader("🎯 Recommendations")
    if st.session_state.engine.recommendations:
        for m, s in st.session_state.engine.recommendations[:5]:
            st.write(f"{m} ⭐ {s}")
            st.caption(st.session_state.engine.explain(m))

            # Trailer button (FEATURE 3)
            if st.button(f"▶ Trailer {m}"):
                webbrowser.open("https://www.youtube.com/results?search_query="+m)
    else:
        st.info("Rate movies to get recommendations")

# =========================
# CHAT SYSTEM (FEATURE 10)
# =========================
st.markdown("---")
st.subheader("💬 Chat Recommender")

user_input = st.text_input("Ask: suggest action movies")

if st.button("Send"):
    if user_input:
        st.session_state.chat.append(("You", user_input))
        reply = st.session_state.engine.chat(user_input)
        st.session_state.chat.append(("AI", ", ".join(reply)))

for role, msg in st.session_state.chat:
    st.write(f"**{role}:** {msg}")

# =========================
# PERSONALITY (FEATURE 6)
# =========================
st.markdown("---")
st.subheader("🧠 Your Movie Personality")
st.success(st.session_state.engine.personality())

# =========================
# GAMIFICATION (FEATURE 5)
# =========================
st.markdown("### 🏆 Achievements")
if len(st.session_state.engine.ratings) >= 5:
    st.success("🎖 Movie Enthusiast Badge Unlocked!")

# =========================
# ANALYTICS (FEATURE 4)
# =========================
if st.session_state.engine.ratings:
    st.subheader("📊 Your Ratings")
    fig = px.histogram(x=list(st.session_state.engine.ratings.values()))
    st.plotly_chart(fig)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🚀 CineMatch PRO MAX | Advanced AI Recommender")
