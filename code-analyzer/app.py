import streamlit as st
import ast
import time
import tracemalloc
import io
import contextlib
from db_config import problems_collection, submissions_collection
from bson import ObjectId

st.set_page_config(
    page_title="Code Analyzer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Code Analyzer")

# Your complexity estimation function
def estimate_complexity(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return "Unknown", "Unknown"

    class ComplexityVisitor(ast.NodeVisitor):
        def __init__(self):
            self.loops = 0
            self.recursions = 0
            self.data_structures = 0

        def visit_For(self, node):
            self.loops += 1
            self.generic_visit(node)

        def visit_While(self, node):
            self.loops += 1
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            # if any(isinstance(n, ast.Call) and n.func.id == node.name for n in ast.walk(node)):
            #     self.recursions += 1
            for call in ast.walk(node):
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
                    if call.func.id == node.name:  # Self-reference
                        self.recursions += 1
            self.generic_visit(node)

        def visit_List(self, node):
            self.data_structures += 1
            self.generic_visit(node)

        def visit_Dict(self, node):
            self.data_structures += 1
            self.generic_visit(node)

        def visit_Set(self, node):
            self.data_structures += 1
            self.generic_visit(node)

        def visit_Tuple(self, node):
            self.data_structures += 1
            self.generic_visit(node)

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    time_complexity = f"O(n^{visitor.recursions})" if visitor.recursions > 0 else \
                     f"O(n^{visitor.loops})" if visitor.loops > 0 else "O(1)"
    space_complexity = "O(n)" if visitor.data_structures > 0 else "O(1)"

    return time_complexity, space_complexity

# UI Components
problem_title = st.selectbox(
    "Select Problem",
    [p["title"] for p in problems_collection.find({})],
    index=0
)

if problem_title:
    problem = problems_collection.find_one({"title": problem_title})
    st.markdown(f"### {problem['title']}")
    st.markdown(f"**Difficulty:** {problem['difficulty']}")
    st.markdown(f"**Description:** {problem['description']}")
    
    st.markdown("---")
    st.markdown("### Your Solution")
    
    code = st.text_area(
        "Write your Python code here",
        height=300,
        value=f"# Solution for {problem['title']}\n\ndef solution():\n    # Your code here\n    pass"
    )
    
    user_id = st.text_input("Your Name (for leaderboard)", "anonymous")
    
    if st.button("Analyze Code"):
        if not code.strip():
            st.error("Please enter some code!")
        else:
            with st.spinner("Analyzing your code..."):
                # Time and memory analysis
                tracemalloc.start()
                start_time = time.time()
                
                output = io.StringIO()
                try:
                    with contextlib.redirect_stdout(output):
                        exec(code, {})
                    execution_success = True
                except Exception as e:
                    output.write(f"Error: {str(e)}")
                    execution_success = False
                
                time_taken = time.time() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                # Complexity analysis
                time_complexity, space_complexity = estimate_complexity(code)
                
                # Save submission
                submission = {
                    "problem": problem_title,
                    "user": user_id,
                    "code": code,
                    "time_taken": time_taken,
                    "memory_used": peak,
                    "time_complexity": time_complexity,
                    "space_complexity": space_complexity,
                    "timestamp": time.time(),
                    "output": output.getvalue()
                }
                submissions_collection.insert_one(submission)
                
                # Display results
                st.success("Analysis complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Execution Time", f"{time_taken:.4f} seconds")
                    st.metric("Memory Usage", f"{peak / 1024:.2f} KB")
                
                with col2:
                    st.metric("Time Complexity", time_complexity)
                    st.metric("Space Complexity", space_complexity)
                
                st.markdown("### Program Output")
                st.code(output.getvalue())
                
                if not execution_success:
                    st.error("Your code contains errors that prevented execution")
                
                st.markdown("---")
                st.markdown("### How to improve?")
                if time_complexity in ["O(n^2)", "O(n^3)", "O(2^n)"]:
                    st.warning("Consider optimizing your algorithm to reduce time complexity")
                if space_complexity == "O(n)":
                    st.info("Your solution uses linear space - can you reduce it to constant space?")