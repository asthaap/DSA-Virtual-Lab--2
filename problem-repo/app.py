import streamlit as st
from db_config import problems_collection
from bson import ObjectId
import urllib.parse

st.set_page_config(
    page_title="Problem Repository",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Problem Repository")

# CRUD Operations
def get_all_problems():
    return list(problems_collection.find({}))

def save_problem(problem_data):
    if "_id" in problem_data:
        problems_collection.update_one(
            {"_id": problem_data["_id"]},
            {"$set": problem_data}
        )
    else:
        problems_collection.insert_one(problem_data)

def delete_problem(problem_id):
    problems_collection.delete_one({"_id": ObjectId(problem_id)})

# UI Components
tab1, tab2 = st.tabs(["Browse Problems", "Manage Problems"])

with tab1:
    st.header("Available Problems")
    problems = get_all_problems()
    
    if not problems:
        st.info("No problems found in the database.")
    else:
        for problem in problems:
            with st.expander(problem["title"]):
                st.markdown(f"**Description:** {problem['description']}")
                st.markdown(f"**Difficulty:** {problem.get('difficulty', 'Not specified')}")
                
                solve_url = f"http://localhost:8502/?problem={urllib.parse.quote(problem['title'])}"
                st.markdown(f"[👉 Solve this problem]({solve_url})", unsafe_allow_html=True)
                
                st.markdown("**Test Cases:**")
                for i, test_case in enumerate(problem["test_cases"], 1):
                    st.code(f"Input {i}:\n{test_case['input']}\n\nOutput {i}:\n{test_case['output']}")

with tab2:
    st.header("Problem Management")
    
    edit_id = st.session_state.get("edit_id", None)
    problem_to_edit = None
    
    if edit_id:
        problem_to_edit = problems_collection.find_one({"_id": ObjectId(edit_id)})
    
    with st.form("problem_form"):
        title = st.text_input("Title", value=problem_to_edit["title"] if problem_to_edit else "")
        description = st.text_area("Description", value=problem_to_edit["description"] if problem_to_edit else "")
        difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard"],
            index=["Easy", "Medium", "Hard"].index(problem_to_edit["difficulty"]) if problem_to_edit else 0
        )
        
        st.markdown("**Test Cases**")
        test_cases = []
        if problem_to_edit:
            for tc in problem_to_edit["test_cases"]:
                cols = st.columns([4, 4, 1])
                input_case = cols[0].text_area("Input", value=tc["input"], key=f"input_{tc['_id']}")
                output_case = cols[1].text_area("Output", value=tc["output"], key=f"output_{tc['_id']}")
                if cols[2].button("❌", key=f"delete_{tc['_id']}"):
                    problems_collection.update_one(
                        {"_id": problem_to_edit["_id"]},
                        {"$pull": {"test_cases": {"_id": tc["_id"]}}}
                    )
                    st.rerun()
                test_cases.append({"input": input_case, "output": output_case})
        else:
            for i in range(2):
                cols = st.columns([4, 4])
                input_case = cols[0].text_area("Input", key=f"input_{i}")
                output_case = cols[1].text_area("Output", key=f"output_{i}")
                test_cases.append({"input": input_case, "output": output_case})
        
        submitted = st.form_submit_button("💾 Save Problem")
        if submitted:
            if not title or not description:
                st.error("Title and description are required!")
            else:
                problem_data = {
                    "title": title,
                    "description": description,
                    "difficulty": difficulty,
                    "test_cases": test_cases
                }
                
                if problem_to_edit:
                    problem_data["_id"] = problem_to_edit["_id"]
                
                save_problem(problem_data)
                st.success("Problem saved successfully!")
                st.session_state.pop("edit_id", None)
                st.rerun()

    if not edit_id:
        st.header("Existing Problems")
        problems = get_all_problems()
        for problem in problems:
            cols = st.columns([4, 1, 1])
            cols[0].write(f"**{problem['title']}** ({problem['difficulty']})")
            if cols[1].button("✏️ Edit", key=f"edit_{problem['_id']}"):
                st.session_state["edit_id"] = str(problem["_id"])
                st.rerun()
            if cols[2].button("🗑️ Delete", key=f"delete_{problem['_id']}"):
                delete_problem(problem["_id"])
                st.success("Problem deleted!")
                st.rerun()