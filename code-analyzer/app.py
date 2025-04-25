# import streamlit as st
# import ast
# import time
# import tracemalloc
# import io
# import contextlib
# from db_config import problems_collection, submissions_collection
# from bson import ObjectId

# st.set_page_config(
#     page_title="Code Analyzer",
#     page_icon="🔍",
#     layout="wide"
# )

# st.title("🔍 Code Analyzer")

# # Your complexity estimation function
# def estimate_complexity(code):
#     try:
#         tree = ast.parse(code)
#     except SyntaxError:
#         return "Unknown", "Unknown"

#     class ComplexityVisitor(ast.NodeVisitor):
#         def __init__(self):
#             self.loops = 0
#             self.recursions = 0
#             self.data_structures = 0

#         def visit_For(self, node):
#             self.loops += 1
#             self.generic_visit(node)

#         def visit_While(self, node):
#             self.loops += 1
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             # if any(isinstance(n, ast.Call) and n.func.id == node.name for n in ast.walk(node)):
#             #     self.recursions += 1
#             for call in ast.walk(node):
#                 if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
#                     if call.func.id == node.name:  # Self-reference
#                         self.recursions += 1
#             self.generic_visit(node)

#         def visit_List(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Dict(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Set(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Tuple(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#     visitor = ComplexityVisitor()
#     visitor.visit(tree)

#     time_complexity = f"O(n^{visitor.recursions})" if visitor.recursions > 0 else \
#                      f"O(n^{visitor.loops})" if visitor.loops > 0 else "O(1)"
#     space_complexity = "O(n)" if visitor.data_structures > 0 else "O(1)"

#     return time_complexity, space_complexity

# # UI Components
# problem_title = st.selectbox(
#     "Select Problem",
#     [p["title"] for p in problems_collection.find({})],
#     index=0
# )

# if problem_title:
#     problem = problems_collection.find_one({"title": problem_title})
#     st.markdown(f"### {problem['title']}")
#     st.markdown(f"**Difficulty:** {problem['difficulty']}")
#     st.markdown(f"**Description:** {problem['description']}")
    
#     st.markdown("---")
#     st.markdown("### Your Solution")
    
#     code = st.text_area(
#         "Write your Python code here",
#         height=300,
#         value=f"# Solution for {problem['title']}\n\ndef solution():\n    # Your code here\n    pass"
#     )
    
#     user_id = st.text_input("Your Name (for leaderboard)", "anonymous")
    
#     if st.button("Analyze Code"):
#         if not code.strip():
#             st.error("Please enter some code!")
#         else:
#             with st.spinner("Analyzing your code..."):
#                 # Time and memory analysis
#                 tracemalloc.start()
#                 start_time = time.time()
                
#                 output = io.StringIO()
#                 test_results = []
#                 execution_success = True
#                 try:
#                     with contextlib.redirect_stdout(output):
#                         local_namespace = {}
#                         exec(code, {}, local_namespace)
#                         if 'solution' in local_namespace:
#                             for i, test_case in enumerate(problem.get("test_cases", []), 1):
#                                 try:
#                                     # Evaluate the input (assuming it's a string for Reverse String)
#                                     test_input = test_case['input']
#                                     expected_output = test_case['output']
#                                     result = local_namespace['solution'](test_input)
#                                     # Convert result to string for comparison and display
#                                     actual_output = str(result)
#                                     passed = actual_output == expected_output
#                                     test_results.append({
#                                         "test_case": i,
#                                         "input": test_input,
#                                         "actual_output": actual_output,
#                                         "expected_output": expected_output,
#                                         "passed": passed
#                                     })
#                                     # Print result for capture in output
#                                     print(f"Test Case {i} Output: {actual_output}")
#                                 except Exception as e:
#                                     test_results.append({
#                                         "test_case": i,
#                                         "input": test_input,
#                                         "actual_output": f"Error: {str(e)}",
#                                         "expected_output": expected_output,
#                                         "passed": False
#                                     })
#                                     print(f"Test Case {i} Error: {str(e)}")
#                         else:
#                             output.write("Error: 'solution' function not defined")
#                             execution_success = False
#                 except Exception as e:
#                     output.write(f"Error: {str(e)}")
#                     execution_success = False
                            
                    
#                 except Exception as e:
#                     output.write(f"Error: {str(e)}")
#                     execution_success = False
                
#                 time_taken = time.time() - start_time
#                 current, peak = tracemalloc.get_traced_memory()
#                 tracemalloc.stop()
                
#                 # Complexity analysis
#                 time_complexity, space_complexity = estimate_complexity(code)
                
#                 # Save submission
#                 submission = {
#                     "problem": problem_title,
#                     "user": user_id,
#                     "code": code,
#                     "time_taken": time_taken,
#                     "memory_used": peak,
#                     "time_complexity": time_complexity,
#                     "space_complexity": space_complexity,
#                     "timestamp": time.time(),
#                     "output": output.getvalue(),
#                     "test_results": test_results
#                 }
#                 submissions_collection.insert_one(submission)
                
#                 # Display results
#                 st.success("Analysis complete!")
                
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.metric("Execution Time", f"{time_taken:.4f} seconds")
#                     st.metric("Memory Usage", f"{peak / 1024:.2f} KB")
                
#                 with col2:
#                     st.metric("Time Complexity", time_complexity)
#                     st.metric("Space Complexity", space_complexity)
                
#                 # st.markdown("### Program Output")
#                 # st.code(output.getvalue())
                
#                 # Display test case results
#                 st.markdown("### Test Case Results")
#                 for result in test_results:
#                     status = "✅ Passed" if result["passed"] else "❌ Failed"
#                     st.markdown(f"**Test Case {result['test_case']}: {status}**")
#                     st.code(f"Input: {result['input']}\nActual Output: {result['actual_output']}\nExpected Output: {result['expected_output']}")
                
#                 # Display raw output (for debugging)
#                 st.markdown("### Raw Program Output")
#                 output_text = output.getvalue()
#                 if output_text.strip():
#                     st.code(output_text)
#                 else:
#                     st.warning("No output produced. Check if the solution function is defined correctly.")
                
#                 if not execution_success:
#                     st.error("Your code contains errors that prevented execution")
                
#                 st.markdown("---")
#                 st.markdown("### How to improve?")
#                 if time_complexity in ["O(n^2)", "O(n^3)", "O(2^n)"]:
#                     st.warning("Consider optimizing your algorithm to reduce time complexity")
#                 if space_complexity == "O(n)":
#                     st.info("Your solution uses linear space - can you reduce it to constant space?")



# import streamlit as st
# import ast
# import time
# import tracemalloc
# import io
# import contextlib
# from db_config import problems_collection, submissions_collection
# from bson import ObjectId

# st.set_page_config(
#     page_title="Code Analyzer",
#     page_icon="🔍",
#     layout="wide"
# )

# st.title("🔍 Code Analyzer")

# # Complexity estimation function (updated to detect string concatenation)
# def estimate_complexity(code):
#     try:
#         tree = ast.parse(code)
#     except SyntaxError:
#         return "Unknown", "Unknown"

#     class ComplexityVisitor(ast.NodeVisitor):
#         def __init__(self):
#             self.loops = 0
#             self.recursions = 0
#             self.data_structures = 0

#         def visit_For(self, node):
#             self.loops += 1
#             self.generic_visit(node)

#         def visit_While(self, node):
#             self.loops += 1
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             for call in ast.walk(node):
#                 if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
#                     if call.func.id == node.name:
#                         self.recursions += 1
#             self.generic_visit(node)

#         def visit_List(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Dict(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Set(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Tuple(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_BinOp(self, node):
#             if isinstance(node.op, ast.Add) and (isinstance(node.left, ast.Str) or isinstance(node.right, ast.Str)):
#                 self.data_structures += 1  # String concatenation uses extra space
#             self.generic_visit(node)

#     visitor = ComplexityVisitor()
#     visitor.visit(tree)

#     time_complexity = f"O(n^{visitor.recursions})" if visitor.recursions > 0 else \
#                      f"O(n^{visitor.loops})" if visitor.loops > 0 else "O(1)"
#     space_complexity = "O(n)" if visitor.data_structures > 0 else "O(1)"

#     return time_complexity, space_complexity

# # UI Components
# problem_title = st.selectbox(
#     "Select Problem",
#     [p["title"] for p in problems_collection.find({})],
#     index=0
# )

# if problem_title:
#     problem = problems_collection.find_one({"title": problem_title})
#     st.markdown(f"### {problem['title']}")
#     st.markdown(f"**Difficulty:** {problem['difficulty']}")
#     st.markdown(f"**Description:** {problem['description']}")
#     st.markdown(f"**Function Signature:** solution({problem.get('parameters', 'N/A')})")
    
#     # Display test cases
#     st.markdown("**Test Cases:**")
#     for i, test_case in enumerate(problem.get("test_cases", []), 1):
#         st.code(f"Input {i}:\n{test_case['input']}\n\nExpected Output {i}:\n{test_case['output']}")
    
#     st.markdown("---")
#     st.markdown("### Your Solution")
    
#     # Generate default code with dynamic signature
#     parameters = problem.get("parameters", "")
#     param_list = [p.strip() for p in parameters.split(",") if p.strip()]
#     if param_list:
#         param_str = ", ".join(param_list)
#     else:
#         param_str = ""
#     default_code = f"# Solution for {problem['title']}\n\ndef solution({param_str}):\n    # Your code here\n    pass"
    
#     code = st.text_area(
#         "Write your Python code here",
#         height=300,
#         value=default_code
#     )
    
#     user_id = st.text_input("Your Name (for leaderboard)", "anonymous")
    
#     if st.button("Analyze Code"):
#         if not code.strip():
#             st.error("Please enter some code!")
#         else:
#             with st.spinner("Analyzing your code..."):
#                 # Time and memory analysis
#                 tracemalloc.start()
#                 start_time = time.time()
                
#                 output = io.StringIO()
#                 test_results = []
#                 execution_success = True
                
#                 try:
#                     with contextlib.redirect_stdout(output):
#                         # Define the code in a local namespace
#                         local_namespace = {}
#                         exec(code, {}, local_namespace)
                        
#                         # Check if solution function exists
#                         if 'solution' in local_namespace:
#                             # Run test cases
#                             for i, test_case in enumerate(problem.get("test_cases", []), 1):
#                                 try:
#                                     # Evaluate input as Python expression
#                                     test_input = ast.literal_eval(test_case['input'])
#                                     expected_output = test_case['output']
#                                     # Determine number of parameters
#                                     num_params = len(param_list)
#                                     if num_params == 1:
#                                         result = local_namespace['solution'](test_input)
#                                     elif num_params > 1:
#                                         if isinstance(test_input, (list, tuple)) and len(test_input) == num_params:
#                                             result = local_namespace['solution'](*test_input)
#                                         else:
#                                             raise ValueError(f"Invalid input format: expected {num_params} arguments")
#                                     else:
#                                         result = local_namespace['solution']()
#                                     actual_output = str(result)
#                                     passed = actual_output == expected_output
#                                     test_results.append({
#                                         "test_case": i,
#                                         "input": test_case['input'],
#                                         "actual_output": actual_output,
#                                         "expected_output": expected_output,
#                                         "passed": passed
#                                     })
#                                     print(f"Test Case {i} Output: {actual_output}")
#                                 except Exception as e:
#                                     test_results.append({
#                                         "test_case": i,
#                                         "input": test_case['input'],
#                                         "actual_output": f"Error: {str(e)}",
#                                         "expected_output": expected_output,
#                                         "passed": False
#                                     })
#                                     print(f"Test Case {i} Error: {str(e)}")
#                         else:
#                             output.write("Error: 'solution' function not defined")
#                             execution_success = False
#                 except Exception as e:
#                     output.write(f"Error: {str(e)}")
#                     execution_success = False
                
#                 time_taken = time.time() - start_time
#                 current, peak = tracemalloc.get_traced_memory()
#                 tracemalloc.stop()
                
#                 # Complexity analysis
#                 time_complexity, space_complexity = estimate_complexity(code)
                
#                 # Save submission
#                 submission = {
#                     "problem": problem_title,
#                     "user": user_id,
#                     "code": code,
#                     "time_taken": time_taken,
#                     "memory_used": peak,
#                     "time_complexity": time_complexity,
#                     "space_complexity": space_complexity,
#                     "timestamp": time.time(),
#                     "output": output.getvalue(),
#                     "test_results": test_results
#                 }
#                 submissions_collection.insert_one(submission)
                
#                 # Display results
#                 st.success("Analysis complete!")
                
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.metric("Execution Time", f"{time_taken:.4f} seconds")
#                     st.metric("Memory Usage", f"{peak / 1024:.2f} KB")
                
#                 with col2:
#                     st.metric("Time Complexity", time_complexity)
#                     st.metric("Space Complexity", space_complexity)
                
#                 # Display test case results
#                 st.markdown("### Test Case Results")
#                 if test_results:
#                     for result in test_results:
#                         status = "✅ Passed" if result["passed"] else "❌ Failed"
#                         st.markdown(f"**Test Case {result['test_case']}: {status}**")
#                         st.code(f"Input: {result['input']}\nActual Output: {result['actual_output']}\nExpected Output: {result['expected_output']}")
#                 else:
#                     st.warning("No test cases executed. Ensure test cases are defined for this problem.")
                
#                 # Display raw output (for debugging)
#                 st.markdown("### Raw Program Output")
#                 output_text = output.getvalue()
#                 if output_text.strip():
#                     st.code(output_text)
#                 else:
#                     st.warning("No output produced. Check if the solution function is defined correctly.")
                
#                 if not execution_success:
#                     st.error("Your code contains errors that prevented execution")
                
#                 st.markdown("---")
#                 st.markdown("### How to improve?")
#                 if time_complexity in ["O(n^2)", "O(n^3)", "O(2^n)"]:
#                     st.warning("Consider optimizing your algorithm to reduce time complexity")
#                 if space_complexity == "O(n)":
#                     st.info("Your solution uses linear space - can you reduce it to constant space?")


# import streamlit as st
# import ast
# import time
# import tracemalloc
# import io
# import contextlib
# from db_config import problems_collection, submissions_collection
# from bson import ObjectId

# st.set_page_config(
#     page_title="Code Analyzer",
#     page_icon="🔍",
#     layout="wide"
# )

# st.title("🔍 Code Analyzer")

# # Complexity estimation function (updated for Binary Search)
# def estimate_complexity(code):
#     try:
#         tree = ast.parse(code)
#     except SyntaxError:
#         return "Unknown", "Unknown"

#     class ComplexityVisitor(ast.NodeVisitor):
#         def __init__(self):
#             self.loops = 0
#             self.recursions = 0
#             self.data_structures = 0
#             self.is_binary_search = False

#         def visit_For(self, node):
#             self.loops += 1
#             self.generic_visit(node)

#         def visit_While(self, node):
#             # Check for Binary Search pattern (e.g., updating left/right with mid)
#             for child in ast.walk(node):
#                 if isinstance(child, ast.Assign):
#                     for target in child.targets:
#                         if isinstance(target, ast.Name) and target.id in ('left', 'right'):
#                             if isinstance(child.value, ast.BinOp) or 'mid' in ast.dump(child.value):
#                                 self.is_binary_search = True
#             if not self.is_binary_search:
#                 self.loops += 1
#             self.generic_visit(node)

#         def visit_FunctionDef(self, node):
#             for call in ast.walk(node):
#                 if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
#                     if call.func.id == node.name:
#                         self.recursions += 1
#             self.generic_visit(node)

#         def visit_List(self, node):
#             # Only count lists created in the code, not input parameters
#             if not isinstance(node.ctx, ast.Load):  # Ignore lists used as inputs
#                 self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Dict(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Set(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_Tuple(self, node):
#             self.data_structures += 1
#             self.generic_visit(node)

#         def visit_BinOp(self, node):
#             if isinstance(node.op, ast.Add) and (isinstance(node.left, ast.Str) or isinstance(node.right, ast.Str)):
#                 self.data_structures += 1  # String concatenation uses extra space
#             self.generic_visit(node)

#     visitor = ComplexityVisitor()
#     visitor.visit(tree)

#     # Adjust time complexity for Binary Search
#     time_complexity = f"O(n^{visitor.recursions})" if visitor.recursions > 0 else \
#                      "O(log n)" if visitor.is_binary_search else \
#                      f"O(n^{visitor.loops})" if visitor.loops > 0 else "O(1)"
#     space_complexity = "O(n)" if visitor.data_structures > 0 else "O(1)"

#     return time_complexity, space_complexity

# # UI Components
# problem_title = st.selectbox(
#     "Select Problem",
#     [p["title"] for p in problems_collection.find({})],
#     index=0
# )

# if problem_title:
#     problem = problems_collection.find_one({"title": problem_title})
#     st.markdown(f"### {problem['title']}")
#     st.markdown(f"**Difficulty:** {problem['difficulty']}")
#     st.markdown(f"**Description:** {problem['description']}")
#     st.markdown(f"**Function Signature:** solution({problem.get('parameters', 'N/A')})")
    
#     # Display test cases
#     st.markdown("**Test Cases:**")
#     for i, test_case in enumerate(problem.get("test_cases", []), 1):
#         st.code(f"Input {i}:\n{test_case['input']}\n\nExpected Output {i}:\n{test_case['output']}")
    
#     st.markdown("---")
#     st.markdown("### Your Solution")
    
#     # Generate default code with dynamic signature
#     parameters = problem.get("parameters", "")
#     param_list = [p.strip() for p in parameters.split(",") if p.strip()]
#     if param_list:
#         param_str = ", ".join(param_list)
#     else:
#         param_str = ""
#     default_code = f"# Solution for {problem['title']}\n\ndef solution({param_str}):\n    # Your code here\n    pass"
    
#     code = st.text_area(
#         "Write your Python code here",
#         height=300,
#         value=default_code
#     )
    
#     user_id = st.text_input("Your Name (for leaderboard)", "anonymous")
    
#     if st.button("Analyze Code"):
#         if not code.strip():
#             st.error("Please enter some code!")
#         else:
#             with st.spinner("Analyzing your code..."):
#                 # Time and memory analysis
#                 tracemalloc.start()
#                 start_time = time.time()
                
#                 output = io.StringIO()
#                 test_results = []
#                 execution_success = True
                
#                 try:
#                     with contextlib.redirect_stdout(output):
#                         # Define the code in a local namespace
#                         local_namespace = {}
#                         exec(code, {}, local_namespace)
                        
#                         # Check if solution function exists
#                         if 'solution' in local_namespace:
#                             # Run test cases
#                             for i, test_case in enumerate(problem.get("test_cases", []), 1):
#                                 try:
#                                     # Evaluate input as Python expression
#                                     test_input = ast.literal_eval(test_case['input'])
#                                     expected_output = test_case['output']
#                                     # Determine number of parameters
#                                     num_params = len(param_list)
#                                     if num_params == 1:
#                                         result = local_namespace['solution'](test_input)
#                                     elif num_params > 1:
#                                         if isinstance(test_input, (list, tuple)) and len(test_input) == num_params:
#                                             result = local_namespace['solution'](*test_input)
#                                         else:
#                                             raise ValueError(f"Invalid input format: expected {num_params} arguments")
#                                     else:
#                                         result = local_namespace['solution']()
#                                     actual_output = str(result)
#                                     passed = actual_output == expected_output
#                                     test_results.append({
#                                         "test_case": i,
#                                         "input": test_case['input'],
#                                         "actual_output": actual_output,
#                                         "expected_output": expected_output,
#                                         "passed": passed
#                                     })
#                                     print(f"Test Case {i} Output: {actual_output}")
#                                 except Exception as e:
#                                     test_results.append({
#                                         "test_case": i,
#                                         "input": test_case['input'],
#                                         "actual_output": f"Error: {str(e)}",
#                                         "expected_output": expected_output,
#                                         "passed": False
#                                     })
#                                     print(f"Test Case {i} Error: {str(e)}")
#                         else:
#                             output.write("Error: 'solution' function not defined")
#                             execution_success = False
#                 except Exception as e:
#                     output.write(f"Error: {str(e)}")
#                     execution_success = False
                
#                 time_taken = time.time() - start_time
#                 current, peak = tracemalloc.get_traced_memory()
#                 tracemalloc.stop()
                
#                 # Complexity analysis
#                 time_complexity, space_complexity = estimate_complexity(code)
                
#                 # Save submission
#                 submission = {
#                     "problem": problem_title,
#                     "user": user_id,
#                     "code": code,
#                     "time_taken": time_taken,
#                     "memory_used": peak,
#                     "time_complexity": time_complexity,
#                     "space_complexity": space_complexity,
#                     "timestamp": time.time(),
#                     "output": output.getvalue(),
#                     "test_results": test_results
#                 }
#                 submissions_collection.insert_one(submission)
                
#                 # Display results
#                 st.success("Analysis complete!")
                
#                 col1, col2 = st.columns(2)
                
#                 with col1:
#                     st.metric("Execution Time", f"{time_taken:.4f} seconds")
#                     st.metric("Memory Usage", f"{peak / 1024:.2f} KB")
                
#                 with col2:
#                     st.metric("Time Complexity", time_complexity)
#                     st.metric("Space Complexity", space_complexity)
                
#                 # Display test case results
#                 st.markdown("### Test Case Results")
#                 if test_results:
#                     for result in test_results:
#                         status = "✅ Passed" if result["passed"] else "❌ Failed"
#                         st.markdown(f"**Test Case {result['test_case']}: {status}**")
#                         st.code(f"Input: {result['input']}\nActual Output: {result['actual_output']}\nExpected Output: {result['expected_output']}")
#                 else:
#                     st.warning("No test cases executed. Ensure test cases are defined for this problem.")
                
#                 # Display raw output (for debugging)
#                 st.markdown("### Raw Program Output")
#                 output_text = output.getvalue()
#                 if output_text.strip():
#                     st.code(output_text)
#                 else:
#                     st.warning("No output produced. Check if the solution function is defined correctly.")
                
#                 if not execution_success:
#                     st.error("Your code contains errors that prevented execution")
                
#                 st.markdown("---")
#                 st.markdown("### How to improve?")
#                 if time_complexity in ["O(n^2)", "O(n^3)", "O(2^n)"]:
#                     st.warning("Consider optimizing your algorithm to reduce time complexity")
#                 if space_complexity == "O(n)":
#                     st.info("Your solution uses linear space - can you reduce it to constant space?")

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

# Complexity estimation function
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
            self.is_binary_search = False
            self.string_concat = False

        def visit_For(self, node):
            self.loops += 1
            self.generic_visit(node)

        def visit_While(self, node):
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id in ('left', 'right'):
                            if isinstance(child.value, ast.BinOp) or 'mid' in ast.dump(child.value):
                                self.is_binary_search = True
            if not self.is_binary_search:
                self.loops += 1
            self.generic_visit(node)

        def visit_FunctionDef(self, node):
            for call in ast.walk(node):
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Name):
                    if call.func.id == node.name:
                        self.recursions += 1
            self.generic_visit(node)

        def visit_List(self, node):
            if not isinstance(node.ctx, ast.Load):
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

        def visit_BinOp(self, node):
            if isinstance(node.op, ast.Add):
                # Detect string concatenation
                if isinstance(node.left, ast.Str) or isinstance(node.right, ast.Str) or \
                   (isinstance(node.left, ast.Name) and isinstance(node.right, ast.Name)):
                    self.string_concat = True
            self.generic_visit(node)

    visitor = ComplexityVisitor()
    visitor.visit(tree)

    time_complexity = f"O(n^{visitor.recursions})" if visitor.recursions > 0 else \
                     "O(log n)" if visitor.is_binary_search else \
                     f"O(n^{visitor.loops})" if visitor.loops > 0 else "O(1)"
    space_complexity = "O(n)" if visitor.data_structures > 0 or visitor.string_concat else "O(1)"

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
    st.markdown(f"**Function Signature:** solution({problem.get('parameters', 'N/A')})")
    
    st.markdown("**Test Cases:**")
    for i, test_case in enumerate(problem.get("test_cases", []), 1):
        st.code(f"Input {i}:\n{test_case['input']}\n\nExpected Output {i}:\n{test_case['output']}")
    
    st.markdown("---")
    st.markdown("### Your Solution")
    
    parameters = problem.get("parameters", "")
    param_list = [p.strip() for p in parameters.split(",") if p.strip()]
    param_str = ", ".join(param_list) if param_list else ""
    default_code = f"# Solution for {problem['title']}\n\ndef solution({param_str}):\n    # Your code here\n    pass"
    
    code = st.text_area(
        "Write your Python code here",
        height=300,
        value=default_code
    )
    
    user_id = st.text_input("Your Name (for leaderboard)", "anonymous")
    
    if st.button("Analyze Code"):
        if not code.strip():
            st.error("Please enter some code!")
        else:
            with st.spinner("Analyzing your code..."):
                tracemalloc.start()
                start_time = time.time()
                
                output = io.StringIO()
                test_results = []
                execution_success = True
                
                try:
                    with contextlib.redirect_stdout(output):
                        local_namespace = {}
                        exec(code, {}, local_namespace)
                        
                        if 'solution' in local_namespace:
                            for i, test_case in enumerate(problem.get("test_cases", []), 1):
                                try:
                                    test_input = ast.literal_eval(test_case['input'])
                                    expected_output = test_case['output']
                                    # Normalize expected output by removing quotes if present
                                    if expected_output.startswith('"') and expected_output.endswith('"'):
                                        expected_output = expected_output[1:-1]
                                    num_params = len(param_list)
                                    if num_params == 1:
                                        result = local_namespace['solution'](test_input)
                                    elif num_params > 1:
                                        if isinstance(test_input, (list, tuple)) and len(test_input) == num_params:
                                            result = local_namespace['solution'](*test_input)
                                        else:
                                            raise ValueError(f"Invalid input format: expected {num_params} arguments")
                                    else:
                                        result = local_namespace['solution']()
                                    actual_output = str(result)
                                    passed = actual_output == expected_output
                                    test_results.append({
                                        "test_case": i,
                                        "input": test_case['input'],
                                        "actual_output": actual_output,
                                        "expected_output": expected_output,
                                        "passed": passed
                                    })
                                    print(f"Test Case {i} Output: {actual_output}")
                                except Exception as e:
                                    test_results.append({
                                        "test_case": i,
                                        "input": test_case['input'],
                                        "actual_output": f"Error: {str(e)}",
                                        "expected_output": expected_output,
                                        "passed": False
                                    })
                                    print(f"Test Case {i} Error: {str(e)}")
                        else:
                            output.write("Error: 'solution' function not defined")
                            execution_success = False
                except Exception as e:
                    output.write(f"Error: {str(e)}")
                    execution_success = False
                
                time_taken = time.time() - start_time
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                time_complexity, space_complexity = estimate_complexity(code)
                
                submission = {
                    "problem": problem_title,
                    "user": user_id,
                    "code": code,
                    "time_taken": time_taken,
                    "memory_used": peak,
                    "time_complexity": time_complexity,
                    "space_complexity": space_complexity,
                    "timestamp": time.time(),
                    "output": output.getvalue(),
                    "test_results": test_results
                }
                submissions_collection.insert_one(submission)
                
                st.success("Analysis complete!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Execution Time", f"{time_taken:.4f} seconds")
                    st.metric("Memory Usage", f"{peak / 1024:.2f} KB")
                
                with col2:
                    st.metric("Time Complexity", time_complexity)
                    st.metric("Space Complexity", space_complexity)
                
                st.markdown("### Test Case Results")
                if test_results:
                    for result in test_results:
                        status = "✅ Passed" if result["passed"] else "❌ Failed"
                        st.markdown(f"**Test Case {result['test_case']}: {status}**")
                        st.code(f"Input: {result['input']}\nActual Output: {result['actual_output']}\nExpected Output: {result['expected_output']}")
                else:
                    st.warning("No test cases executed. Ensure test cases are defined for this problem.")
                
                st.markdown("### Raw Program Output")
                output_text = output.getvalue()
                if output_text.strip():
                    st.code(output_text)
                else:
                    st.warning("No output produced. Check if the solution function is defined correctly.")
                
                if not execution_success:
                    st.error("Your code contains errors that prevented execution")
                
                st.markdown("---")
                st.markdown("### How to improve?")
                if time_complexity in ["O(n^2)", "O(n^3)", "O(2^n)"]:
                    st.warning("Consider optimizing your algorithm to reduce time complexity")
                if space_complexity == "O(n)":
                    st.info("Your solution uses linear space - can you reduce it to constant space?")