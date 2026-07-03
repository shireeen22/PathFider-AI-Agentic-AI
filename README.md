# Pathfinder AI | Next-Gen AI Learning and Career Mentor Agent

Pathfinder AI is a production-ready, interactive Career and Learning Mentor Agent designed to guide students and aspiring professionals entering domains such as Machine Learning, Data Science, Software Engineering, Deep Learning, and Generative AI. 

Built on top of Google's **Agent Development Kit (ADK) 2.0** and powered by **Gemini 3.5 Flash**, the system leverages specialized tool modularization to deliver structured, high-accuracy guidance alongside a conversational chat interface.

---

## Key Features

1. **Learning Roadmap Tool (`generate_learning_roadmap`)**
   - Generates beginner, intermediate, and advanced milestone roadmaps customized to the user's targeted career path and starting skill level.
   - Suggests specific technologies, study timelines, and practice milestones.

2. **Project Recommendation Tool (`recommend_projects`)**
   - Suggests high-quality portfolio projects with descriptions, target stacks, and portfolio value arguments.
   - Incorporates specific dataset recommendations from open platforms like Kaggle, Hugging Face, or public APIs.

3. **Course Recommendation Tool (`recommend_courses`)**
   - Discovers top-tier courses, learning resources, and textbooks based on a targeted subject area.
   - Supports budget preferences (`free` vs. `paid` vs. `any`).

4. **Interview Preparation Tool (`generate_interview_prep`)**
   - Generates realistic mock technical interviews containing conceptual, coding, and system design questions.
   - Provides comprehensive model answers and flags common candidate pitfalls.

5. **Resume Analyzer Tool (`review_resume` / `review_resume_pdf`)**
   - Conducts full resume audits matching the user's profile against a targeted job title.
   - Outputs an estimated match score, key strengths, skill gaps, and actionable formatting/positioning recommendations.
   - Includes automatic PDF text extraction using PyMuPDF (`fitz`).

---

## Project Structure

```text
agentic-ai-capstone/
│
├── career_mentor/              # ADK Agent Configuration
│   ├── .env                    # Local environment config (API Keys)
│   ├── __init__.py
│   ├── agent.py                # Core Agent declaration and prompts
│   └── tools.py                # Custom Python tool functions
│
├── static/                     # Frontend Web Assets
│   └── index.html              # Sleek glassmorphic web dashboard
│
├── server.py                   # FastAPI backend server linking ADK to UI
├── requirements.txt            # Python dependencies
└── README.md                   # This documentation file
```

---

## Setup & Installation

### 1. Prerequisites
- Python 3.11+
- Pip or UV package manager
- Google AI Studio API Key (Gemini API)

### 2. Clone and Install Dependencies
Navigate to the project root and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Configure your Gemini API Key in the `career_mentor/.env` file:
```env
GOOGLE_GENAI_USE_ENTERPRISE=0
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

---

## Running the Application

### 1. Start the Backend Server
Launch the FastAPI production server using Uvicorn:
```bash
python server.py
```
By default, the server runs on `http://127.0.0.1:8000`.

### 2. Launch the Web Interface
Open your browser and navigate to:
```text
http://127.0.0.1:8000
```
This loads the glassmorphic, interactive dashboard supporting:
- Full conversational AI chat with Pathfinder AI.
- Dedicated tab forms for Roadmaps, Projects, Courses, and Interview Mock Q&A.
- A Resume audit portal where you can upload your PDF resume or paste raw text.

---

## Interactive Local Debugging via ADK CLI

You can interact with and debug the ADK agent using ADK's built-in command line interface:

### 1. Terminal Chat
To converse directly with the agent inside your terminal:
```bash
adk run career_mentor
```

### 2. Developer Web UI
To visualize execution traces, agent tool invocation steps, and inspect memory states, start the ADK dev server:
```bash
adk web career_mentor
```
Then navigate to the URL provided by the CLI (default: `http://localhost:8000/dev-ui/`).

---

## Production Deployment to Google Cloud

The project is built to support seamless deployment using the ADK CLI to target Google Cloud execution runtimes:

### 1. Deploying to Agent Engine (Agent Runtime)
Deploys the agent configuration directly onto Google's serverless Agent Runtime environment:
```bash
adk deploy agent_engine --project <GCP_PROJECT_ID> --region <REGION>
```

### 2. Deploying to Google Cloud Run
Wraps the agent into a containerized FastAPI application and hosts it on Cloud Run:
```bash
adk deploy cloud_run --project <GCP_PROJECT_ID> --region <REGION>
```

### 3. Deploying to Google Kubernetes Engine (GKE)
For enterprise-scale, high-concurrency environments requiring custom cluster hosting:
```bash
adk deploy gke --project <GCP_PROJECT_ID> --region <REGION> --cluster <CLUSTER_NAME>
```
