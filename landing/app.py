import streamlit as st

st.set_page_config(
    page_title="AlgoPlatform",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 DSA mini virtual lab")
st.markdown("""
### Your Complete Algorithm Analysis Platform
Select a service to get started:
""")

services = {
    "🧠 Problem Repository": "http://localhost:8501",
    "🔍 Code Analyzer": "http://localhost:8502",
    "🔎 Plagiarism Checker": "http://localhost:8503",
    "🏆 Leaderboard": "http://localhost:8504"
}

for service, url in services.items():
    st.markdown(f"""
    <a href="{url}" target="_self">
        <button style="
            width: 100%;
            padding: 0.5rem;
            margin: 0.25rem 0;
            font-size: 1rem;
            border-radius: 0.5rem;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        ">
            {service}
        </button>
    </a>
    """, unsafe_allow_html=True)

st.markdown("---")
st.write("© 2023 AlgoPlatform - All rights reserved")