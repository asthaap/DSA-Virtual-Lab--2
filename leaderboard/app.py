import streamlit as st
from db_config import submissions_collection, problems_collection
import time
from datetime import datetime

st.set_page_config(
    page_title="Leaderboard",
    page_icon="🏆",
    layout="wide"
)

st.title("🏆 Leaderboard")

# Time period filter
time_period = st.selectbox(
    "Time Period",
    ["All Time", "Last 7 Days", "Last 30 Days"],
    index=0
)

# Problem filter
all_problems = ["All Problems"] + [p["title"] for p in problems_collection.find({})]
selected_problem = st.selectbox(
    "Filter by Problem",
    all_problems,
    index=0
)

# Calculate time filter
time_filter = {}
if time_period == "Last 7 Days":
    time_filter["timestamp"] = {"$gte": time.time() - 7*24*60*60}
elif time_period == "Last 30 Days":
    time_filter["timestamp"] = {"$gte": time.time() - 30*24*60*60}

# Calculate problem filter
problem_filter = {}
if selected_problem != "All Problems":
    problem_filter["problem"] = selected_problem

# Combine filters
query = {**time_filter, **problem_filter}

# Get leaderboard data
pipeline = [
    {"$match": query},
    {"$group": {
        "_id": "$user",
        "total_submissions": {"$sum": 1},
        "avg_time": {"$avg": "$time_taken"},
        "avg_memory": {"$avg": "$memory_used"},
        "total_score": {
            "$sum": {
                "$switch": {
                    "branches": [
                        {"case": {"$eq": ["$time_complexity", "O(1)"]}, "then": 100},
                        {"case": {"$eq": ["$time_complexity", "O(n)"]}, "then": 80},
                        {"case": {"$eq": ["$time_complexity", "O(n^2)"]}, "then": 50},
                        {"case": {"$eq": ["$time_complexity", "O(n^3)"]}, "then": 30},
                        {"case": {"$eq": ["$time_complexity", "O(2^n)"]}, "then": 10}
                    ],
                    "default": 50
                }
            }
        }
    }},
    {"$sort": {"total_score": -1}},
    {"$limit": 20}
]

leaderboard_data = list(submissions_collection.aggregate(pipeline))

# Display leaderboard
st.header("Top Coders")

if not leaderboard_data:
    st.info("No submissions found for the selected filters")
else:
    for i, entry in enumerate(leaderboard_data, 1):
        cols = st.columns([1, 3, 2, 2, 2])
        
        # Rank
        if i == 1:
            cols[0].markdown("🥇")
        elif i == 2:
            cols[0].markdown("🥈")
        elif i == 3:
            cols[0].markdown("🥉")
        else:
            cols[0].markdown(f"**#{i}**")
        
        # User info
        cols[1].markdown(f"**{entry['_id']}**")
        
        # Stats
        cols[2].markdown(f"📊 **{entry['total_score']} pts**")
        cols[3].markdown(f"⏱️ {entry['avg_time']:.4f}s avg")
        cols[4].markdown(f"💾 {entry['avg_memory']/1024:.2f} KB avg")
        
        st.progress(min(entry["total_score"] / 500, 1.0))  # Assuming max 500 points
        st.markdown("---")

# Recent activity
st.header("Recent Activity")
recent_submissions = submissions_collection.find(query).sort("timestamp", -1).limit(5)

for sub in recent_submissions:
    cols = st.columns([2, 2, 1, 1, 1])
    cols[0].markdown(f"**{sub['user']}** solved **{sub['problem']}**")
    cols[1].markdown(f"{datetime.fromtimestamp(sub['timestamp']).strftime('%Y-%m-%d %H:%M')}")
    cols[2].markdown(f"⏱️ {sub['time_taken']:.4f}s")
    cols[3].markdown(f"💾 {sub['memory_used']/1024:.2f} KB")
    cols[4].markdown(f"📊 {sub['time_complexity']}")
    
    with st.expander("View Details"):
        st.code(sub["code"])