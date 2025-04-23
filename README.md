# **DSA Lab Interactive Platform**  
**A Complete Learning Environment for Data Structures & Algorithms**  

---

## **📌 Table of Contents**  
1. [**Project Overview**](#-project-overview)  
2. [**Key Features**](#-key-features)  
3. [**System Architecture**](#-system-architecture)  
4. [**Installation & Setup**](#-installation--setup)  
5. [**Running the Platform**](#-running-the-platform)  
6. [**Accessing Services**](#-accessing-services)  
7. [**Using the Platform**](#-using-the-platform)  
8. [**Development & Tech Stack**](#-development--tech-stack)  
9. [**Troubleshooting**](#-troubleshooting)  
10. [**Contributing**](#-contributing)  
 

---

## **🚀 Project Overview**  
The **DSA Lab Interactive Platform** is a **microservices-based learning environment** designed to help users master **Data Structures & Algorithms (DSA)** through:  
✔ **Interactive problem-solving** (Python)
✔ **Real-time code analysis & complexity estimation**  
✔ **Test case validation & leaderboard rankings**  

Built with **Docker, Streamlit, and MongoDB**, this platform provides a **seamless learning experience** for students, educators, and competitive programmers.  

---

## **✨ Key Features**  

### **1. Problem Repository**  
📌 **Add, edit, and manage** DSA problems with test cases  
📌 **Multi-language support** (Python, C, C++, Java, JavaScript)  
📌 **Test case validation** for accurate solution checking  

### **2. Code Execution & Analysis**  
⚡ **Real-time code execution** with **time & memory profiling**  
⚡ **Complexity estimation** (Big-O notation)  
⚡ **Error detection & debugging**  


### **3. Leaderboard & Plagiarism Checker**  
🏆 **Track user performance** with rankings  
🔎 **Detect code similarity** to prevent plagiarism  

---

## **📐 System Architecture**  

### **Microservices Breakdown**  
| **Service** | **Port** | **Description** |
|------------|---------|----------------|
| Landing Page | `8507` | Main portal with navigation |
| Problem Repository | `8501` | Manage DSA problems |
| Code Analyzer | `8502` | Execute & analyze code |
| Plagiarism checker | `8503` | hecks the plagiarism |
| Leaderboard | `8504` | Display of top coders |
| MongoDB | `27017` | Database for problems & submissions |

### **Tech Stack**  
- **Frontend**: Streamlit (Interactive UI)  
- **Backend**: Python (FastAPI for APIs)  
- **Database**: MongoDB (NoSQL storage)  
- **Containerization**: Docker & Docker Compose  

---

## **⚙️ Installation & Setup**  

### **Prerequisites**  
- **Docker** ([Install Guide](https://docs.docker.com/get-docker/))  
- **Docker Compose** ([Install Guide](https://docs.docker.com/compose/install/))  

### **Steps to Run**  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/asthaap/DSA-Virtual-Lab--2.git
   cd DSA-Virtual-Lab--2
   ```

2. **Set up `.env` file**  
   ```bash
   echo "MONGODB_URI=mongodb://admin:admin123@mongodb:27017/dsa_lab?authSource=admin" > .env
   ```

3. **Build and launch containers**  
   ```bash
   docker-compose up --build
   ```

4. **Access the platform**  
   Open **[http://localhost:8507](http://localhost:8507)** in your browser.  

---

## **🏃 Running the Platform**  

### **Starting Services**  
```bash
docker-compose up --build
```

### **Stopping Services**  
```bash
docker-compose down
```

### **Resetting the Database**  
```bash
docker-compose down -v
docker volume prune
docker-compose up --build
```

---

## **🌐 Accessing Services**  

| **Service** | **URL** |
|-------------|---------|
| **Landing Page** | [http://localhost:8507](http://localhost:8507) |
| **Problem Repository** | [http://localhost:8501](http://localhost:8501) |
| **Code Analyzer** | [http://localhost:8502](http://localhost:8502) |
| **Plagiarism Checker** | [http://localhost:8503](http://localhost:8503) |
| **Leaderboard** | [http://localhost:8504](http://localhost:8504) |

---

## **🎯 Using the Platform**  

### **1. Adding a Problem**  
- Go to **Problem Repository (`8501`)**  
- Click **"Add New Problem"**  
- Fill in:  
  ```yaml
  Title: Binary Search
  Description: Find an element in a sorted array in O(log n) time
  Test Cases:
    - Input: "[1,2,3,4,5]\n4" → Output: "3"
    - Input: "[10,20,30]\n15" → Output: "-1"
  ```

### **2. Solving a Problem**  
- Go to **Code Analyzer (`8502`)**  
- Select a problem & write code:  
  ```python
  def binary_search(arr, target):
      left, right = 0, len(arr)-1
      while left <= right:
          mid = (left + right) // 2
          if arr[mid] == target:
              return mid
          elif arr[mid] < target:
              left = mid + 1
          else:
              right = mid - 1
      return -1
  ```
- Click **"Analyze Code"** to test.  

## **💻 Development & Tech Stack**  

### **Folder Structure**  
```
DSA-virtual-lab--2/
├── docker-compose.yml          # Container orchestration
├── .env                        # Environment variables
├── landing/                    # Main portal
│   ├── app.py                  # Streamlit landing page
│   ├── Dockerfile              # Container config
│   └── requirements.txt        # Python dependencies
├── problem-repo/               # Problem management
│   ├── app.py                  # CRUD operations
│   ├── Dockerfile
│   ├── requirements.txt
│   └── db_config.py            # MongoDB connection
├── code-analyzer/              # Code execution & analysis
│   ├── app.py                  # Complexity estimation
│   ├── Dockerfile
│   └── requirements.txt
├── plagiarism-checker/         # Code similarity detection
│   ├── app.py                  # AST-based comparison
│   ├── Dockerfile
│   └── requirements.txt
└── leaderboard/                # User rankings
|    ├── app.py                  # Score aggregation
|    ├── Dockerfile
|    └── requirements.txt
|──.env
└──.Readme.md
```

### **Extending the Project**  
- **Add new visualizations** (e.g., Dynamic Programming)  
- **Support more languages** (Go, Rust, etc.)  
- **Enhance plagiarism detection** (AST-based analysis)  

---

## **🔧 Troubleshooting**  

| **Issue** | **Solution** |
|-----------|-------------|
| **MongoDB not connecting** | Run `docker-compose down -v` & restart |
| **Streamlit not loading** | Check `docker-compose logs <service>` |


---

## **🤝 Contributing**  
1. **Fork** the repository  
2. **Create a branch** (`git checkout -b feature/new-algo`)  
3. **Commit changes** (`git commit -am "Add new sorting viz"`)  
4. **Push** (`git push origin feature/new-algo`)  
5. **Open a Pull Request**  

---

### **🎉 Ready to Explore?**  
Visit **[http://localhost:8507](http://localhost:8507)** and start learning DSA interactively! 🚀  

---


This `README.md` provides **complete documentation** from setup to usage, making it easy for users & contributors to get started. 
