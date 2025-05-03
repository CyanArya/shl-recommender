import streamlit as st
import requests
import pandas as pd
from typing import List, Dict, Any
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the recommender
from backend.recommender import AssessmentRecommender

# Streamlit page config
st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="📊",
    layout="centered"
)

# Simple Navbar
st.markdown("""
    <style>
    .navbar-simple {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 48px;
        background: #222;
        color: #fff;
        display: flex;
        align-items: center;
        padding-left: 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        z-index: 100;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    }
    .main-content { margin-top: 60px; }
    </style>
    <div class="navbar-simple">SHL Assessment Recommender</div>
    <div class="main-content"></div>
""", unsafe_allow_html=True)

st.markdown("<div class='main-content'>", unsafe_allow_html=True)

st.title("")
st.write("""
Enter a job description or query below to get relevant SHL assessment recommendations.
""")

# Input form
with st.form("recommendation_form", clear_on_submit=False):
    query = st.text_area(
        "Job Description or Query",
        placeholder="e.g., hiring java developer with 3 years experience",
        height=100
    )
    max_results = st.slider(
        "Number of recommendations",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )
    submitted = st.form_submit_button("Get Recommendations")

API_URL = "https://shl-recommender-1-rvfj.onrender.com/recommend"

def get_recommendations(query: str, max_results: int) -> List[Dict[str, Any]]:
    try:
        response = requests.post(
            API_URL,
            json={"query": query, "max_results": max_results}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error getting recommendations: {str(e)}")
        return []

def display_recommendations(recommendations: List[Dict[str, Any]]):
    if not recommendations:
        st.info("No recommendations found. Try a different query.")
        return
    df = pd.DataFrame(recommendations)
    df["Assessment"] = df.apply(
        lambda x: f'<a href="{x["assessment_url"]}" target="_blank">{x["assessment_name"]}</a>', axis=1
    )
    display_cols = [
        "Assessment",
        "description",
        "skills",
        "duration",
        "test_type",
        "remote_testing_support",
        "adaptive_irt_support",
        "similarity_score"
    ]
    df = df[display_cols]
    df = df.rename(columns={
        "description": "Description",
        "skills": "Skills",
        "duration": "Duration",
        "test_type": "Test Type",
        "remote_testing_support": "Remote",
        "adaptive_irt_support": "Adaptive/IRT",
        "similarity_score": "Relevance"
    })
    df["Relevance"] = (df["Relevance"] * 100).round(1).astype(str) + "%"
    st.markdown(
        df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

if submitted and query:
    with st.spinner("Getting recommendations..."):
        recommendations = get_recommendations(query, max_results)
        display_recommendations(recommendations)

st.markdown("---")
st.caption("SHL Assessment Recommendation System | Powered by AI")
st.markdown("</div>", unsafe_allow_html=True)
