import os
import sys
import uuid
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), "career_mentor", ".env"))
load_dotenv()  # Fallback to root .env

# Verify and setup path
sys.path.append(os.path.join(os.path.dirname(__file__), "career_mentor"))

# Now import the agent and tools
try:
    from career_mentor.agent import root_agent
    from career_mentor.tools import (
        generate_learning_roadmap as tool_roadmap,
        recommend_projects as tool_projects,
        recommend_courses as tool_courses,
        generate_interview_prep as tool_interview,
        review_resume as tool_resume,
        extract_text_from_pdf
    )
except ImportError:
    # If path resolution differs under runner
    from agent import root_agent
    from tools import (
        generate_learning_roadmap as tool_roadmap,
        recommend_projects as tool_projects,
        recommend_courses as tool_courses,
        generate_interview_prep as tool_interview,
        review_resume as tool_resume,
        extract_text_from_pdf
    )

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Validate API Key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key or api_key == "YOUR_API_KEY":
    print("WARNING: GOOGLE_API_KEY is not set or is set to placeholder. Please configure it in career_mentor/.env")

# Initialize ADK Runner
session_service = InMemorySessionService()
runner = Runner(
    app_name="career_mentor",
    agent=root_agent,
    session_service=session_service,
    auto_create_session=True,
)

app = FastAPI(
    title="AI Learning and Career Mentor Agent API",
    description="Backend API powering the career mentorship dashboard, using ADK 2.0 and Gemini 3.5 Flash",
    version="1.0.0"
)

# API schemas
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = "user_default"

class RoadmapRequest(BaseModel):
    career_goal: str
    experience_level: str

class ProjectsRequest(BaseModel):
    career_goal: str
    experience_level: str

class CoursesRequest(BaseModel):
    topic: str
    budget_preference: str = "any"

class InterviewRequest(BaseModel):
    topic: str
    difficulty: str = "Intermediate"

class ResumeTextRequest(BaseModel):
    resume_text: str
    target_role: str

@app.post("/api/chat")
async def chat(chat_msg: ChatMessage):
    """
    General conversational endpoint that routes requests through the ADK 2.0 agent workflow.
    """
    if not chat_msg.session_id:
        chat_msg.session_id = str(uuid.uuid4())
    
    # Create structure for new message using google-genai schema
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=chat_msg.message)]
    )
    
    try:
        # Run agent loop
        events = runner.run(
            user_id=chat_msg.user_id,
            session_id=chat_msg.session_id,
            new_message=user_content
        )
        
        # Accumulate agent response text
        response_text = ""
        for event in events:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
                        
        if not response_text:
            response_text = "I processed your request, but did not generate a text response. Please let me know how else I can help!"
            
        return {
            "session_id": chat_msg.session_id,
            "response": response_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent runtime error: {str(e)}")

@app.post("/api/roadmap")
async def get_roadmap(req: RoadmapRequest):
    """Direct Roadmap generation tool endpoint."""
    try:
        roadmap = tool_roadmap(req.career_goal, req.experience_level)
        return {"roadmap": roadmap}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects")
async def get_projects(req: ProjectsRequest):
    """Direct Project Recommendation tool endpoint."""
    try:
        projects = tool_projects(req.career_goal, req.experience_level)
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/courses")
async def get_courses(req: CoursesRequest):
    """Direct Course Recommendation tool endpoint."""
    try:
        courses = tool_courses(req.topic, req.budget_preference)
        return {"courses": courses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview")
async def get_interview_prep(req: InterviewRequest):
    """Direct Interview Prep tool endpoint."""
    try:
        prep = tool_interview(req.topic, req.difficulty)
        return {"prep": prep}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resume-text")
async def get_resume_review_text(req: ResumeTextRequest):
    """Direct Resume Review tool endpoint via copy-pasted text."""
    try:
        review = tool_resume(req.resume_text, req.target_role)
        return {"review": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resume-pdf")
async def get_resume_review_pdf(
    file: UploadFile = File(...),
    target_role: str = Form(...)
):
    """Direct Resume Review tool endpoint via PDF upload."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Save the file temporarily
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, f"{uuid.uuid4()}_{file.filename}")
    
    try:
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
            
        resume_text = extract_text_from_pdf(temp_path)
        
        # Cleanup file after extraction
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        if resume_text.startswith("Error reading PDF file"):
            raise HTTPException(status_code=500, detail=resume_text)
            
        review = tool_resume(resume_text, target_role)
        return {"review": review}
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
