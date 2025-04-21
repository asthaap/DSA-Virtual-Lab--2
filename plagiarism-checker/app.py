import streamlit as st
from difflib import SequenceMatcher
from db_config import submissions_collection, problems_collection
from bson import ObjectId

st.set_page_config(
    page_title="Plagiarism Checker",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Plagiarism Checker")

def normalize_code(code):
    """Basic code normalization for comparison"""
    return code.strip().lower().replace(" ", "").replace("\t", "")

def check_similarity(code1, code2):
    norm1 = normalize_code(code1)
    norm2 = normalize_code(code2)
    return SequenceMatcher(None, norm1, norm2).ratio() * 100

# UI Components
problem_title = st.selectbox(
    "Select Problem",
    [p["title"] for p in problems_collection.find({})],
    index=0
)

if problem_title:
    st.markdown(f"### Checking submissions for: {problem_title}")
    
    threshold = st.slider(
        "Similarity Threshold (%)",
        min_value=50,
        max_value=100,
        value=80,
        help="Minimum similarity percentage to flag as potential plagiarism"
    )
    
    if st.button("Run Plagiarism Check"):
        submissions = list(submissions_collection.find({"problem": problem_title}))
        
        if len(submissions) < 2:
            st.warning("Need at least 2 submissions to compare")
        else:
            results = []
            for i in range(len(submissions)):
                for j in range(i+1, len(submissions)):
                    similarity = check_similarity(
                        submissions[i]["code"],
                        submissions[j]["code"]
                    )
                    if similarity >= threshold:
                        results.append({
                            "user1": submissions[i]["user"],
                            "user2": submissions[j]["user"],
                            "similarity": similarity,
                            "id1": submissions[i]["_id"],
                            "id2": submissions[j]["_id"]
                        })
            
            if not results:
                st.success("No plagiarism detected above the threshold!")
            else:
                st.warning(f"Found {len(results)} potential plagiarism cases:")
                
                for result in sorted(results, key=lambda x: x["similarity"], reverse=True):
                    with st.expander(
                        f"{result['user1']} ↔ {result['user2']} - {result['similarity']:.1f}% similar"
                    ):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**{result['user1']}'s solution**")
                            submission = submissions_collection.find_one({"_id": result["id1"]})
                            st.code(submission["code"])
                        
                        with col2:
                            st.markdown(f"**{result['user2']}'s solution**")
                            submission = submissions_collection.find_one({"_id": result["id2"]})
                            st.code(submission["code"])