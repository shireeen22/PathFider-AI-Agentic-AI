from dotenv import load_dotenv
import os
import json
import fitz  # PyMuPDF
from typing import List, Dict, Optional
from google import genai
from google.genai import types

load_dotenv()
# Initialize the Gemini client using the environment key
def get_genai_client():
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    # Default fallback to standard env loading
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Please check your .env file."
        )
    return genai.Client(api_key=api_key if api_key else None)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts plain text from a PDF file. Helper utility for the Resume Review Tool.
    
    Args:
        pdf_path: The absolute or relative path to the PDF file.
        
    Returns:
        The extracted text from the PDF file.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

def generate_learning_roadmap(career_goal: str, experience_level: str) -> str:
    """
    Generates a personalized, comprehensive learning roadmap for careers in AI, ML, GenAI, Data Science, or Software Engineering.
    
    Args:
        career_goal: The targeted career path (e.g., 'Machine Learning Engineer', 'Generative AI Specialist', 'Data Scientist', 'Software Engineer').
        experience_level: The user's current experience level ('Beginner', 'Intermediate', 'Advanced').
        
    Returns:
        A detailed roadmap with phases, milestones, technologies, and skills in Markdown format.
    """
    client = get_genai_client()
    prompt = f"""
    You are a professional AI and Technical Career Advisor.
    Generate a detailed, step-by-step learning roadmap for a user who wants to become a "{career_goal}".
    The user's current level is "{experience_level}".
    
    Your roadmap must include:
    1. A detailed list of skills and concepts to master (divided into Beginner, Intermediate, and Advanced stages relative to their starting level).
    2. Specific technologies, frameworks, and programming languages (e.g., PyTorch, Python, Docker, Scikit-learn, LangChain).
    3. Suggested timeframes for each stage.
    4. Practical tips on how to practice or build projects for each stage.
    
    Format the response as a clean, beautiful Markdown document with headings, bullet points, and code blocks for technologies.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Failed to generate roadmap: {str(e)}"

def recommend_projects(career_goal: str, experience_level: str) -> str:
    """
    Recommends hands-on coding and machine learning projects based on the user's target career goal and experience level.
    
    Args:
        career_goal: The target role or domain (e.g., 'Generative AI Specialist', 'Data Scientist', 'Machine Learning Engineer').
        experience_level: The user's skill level ('Beginner', 'Intermediate', 'Advanced').
        
    Returns:
        A Markdown-formatted list of recommended projects, including project titles, descriptions, suggested tech stacks, and dataset recommendations.
    """
    client = get_genai_client()
    prompt = f"""
    You are an AI Career Mentor. Recommends 3 distinct, industry-relevant projects for an aspiring "{career_goal}" at the "{experience_level}" level.
    
    For each project, provide:
    1. Project Title
    2. Problem Statement & Description
    3. Tech Stack (languages, libraries, tools)
    4. Dataset Suggestions: Recommend specific public datasets (e.g., from Kaggle, UCI, Hugging Face, or open APIs) that the user can use, along with how to obtain them.
    5. Portfolio Value: Why this project looks great on a resume/GitHub profile.
    
    Format the output in clean Markdown with clear headers for each project.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Failed to recommend projects: {str(e)}"

def recommend_courses(topic: str, budget_preference: str = "any") -> str:
    """
    Suggests high-quality online courses, textbooks, and learning resources for a specific topic in AI, machine learning, or software engineering.
    
    Args:
        topic: The subject to learn (e.g., 'Deep Learning', 'Transformers', 'System Design', 'Python').
        budget_preference: Filter by cost ('free', 'paid', or 'any').
        
    Returns:
        A Markdown-formatted list of course recommendations with platform names, descriptions, and estimated duration.
    """
    client = get_genai_client()
    prompt = f"""
    You are a Technical Education Consultant. Recommend 4 top-tier courses or learning resources for the topic "{topic}".
    Filter/prioritize based on the user's budget preference: "{budget_preference}".
    
    Include a mix of:
    - High-quality free courses (e.g., Fast.ai, YouTube Playlists, MIT OpenCourseWare, Stanford Online).
    - Premium/paid platforms (e.g., Coursera, edX, DeepLearning.AI, Udacity) if "paid" or "any" is selected.
    
    For each recommendation, provide:
    1. Course Title & Platform/Provider
    2. Price/Cost (Free vs Paid)
    3. Target Audience (Beginner/Intermediate/Advanced)
    4. Key Topics Covered & Why it is recommended.
    
    Format the response as clean Markdown.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Failed to recommend courses: {str(e)}"

def generate_interview_prep(topic: str, difficulty: str = "Intermediate") -> str:
    """
    Generates technical interview preparation questions, conceptual challenges, and detailed answers for technical interviews.
    
    Args:
        topic: The interview subject (e.g., 'Python OOP', 'Machine Learning Algorithms', 'Deep Learning & Neural Networks', 'Generative AI & LLMs').
        difficulty: The difficulty level of the interview ('Beginner', 'Intermediate', 'Advanced').
        
    Returns:
        A Markdown-formatted list of technical interview questions and comprehensive sample answers.
    """
    client = get_genai_client()
    prompt = f"""
    You are a Technical Interviewer.
    Generate a mock interview preparation guide for the topic "{topic}" at the "{difficulty}" level.
    
    Provide:
    1. 5 representative interview questions (mix of conceptual, coding, and system design questions appropriate for the difficulty).
    2. Comprehensive, correct answers/explanations for each question.
    3. Interview tips or common pitfalls for candidates when answering these questions.
    
    Format the output in clean Markdown.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Failed to generate interview prep: {str(e)}"

def review_resume(resume_text: str, target_role: str) -> str:
    """
    Reviews a candidate's resume or CV text against a target professional role (e.g., Machine Learning Engineer, Data Scientist).
    
    Args:
        resume_text: The plain text content of the resume.
        target_role: The role the candidate is targeting (e.g., 'Data Scientist', 'Generative AI Specialist').
        
    Returns:
        A Markdown analysis detailing matching score, strengths, critical skill gaps, and bullet-point suggestions for improvement.
    """
    client = get_genai_client()
    prompt = f"""
    You are an Expert Resume Reviewer and Technical Recruiter.
    Analyze the following resume text against the target role: "{target_role}".
    
    Resume Content:
    \"\"\"
    {resume_text}
    \"\"\"
    
    Provide a detailed evaluation in Markdown with:
    1. **Estimated Match Score (0-100%)**: Explain the score based on skills, experience, and projects.
    2. **Key Strengths**: What stands out in the resume for this role?
    3. **Critical Skill Gaps**: What key technologies, skills, or certifications are missing?
    4. **Actionable Suggestions for Improvement**:
       - Specific formatting/phrasing tweaks (e.g., using the STAR method for bullet points).
       - Recommended projects or certifications to add to bridge the gaps.
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Failed to review resume: {str(e)}"

def review_resume_pdf(pdf_path: str, target_role: str) -> str:
    """
    Parses a resume PDF file from the local path and reviews it against a target role.
    
    Args:
        pdf_path: The local absolute or relative file path to the PDF resume.
        target_role: The role the candidate is targeting.
        
    Returns:
        A detailed resume review report in Markdown format.
    """
    resume_text = extract_text_from_pdf(pdf_path)
    if resume_text.startswith("Error reading PDF file"):
        return resume_text
    return review_resume(resume_text, target_role)

def general_ai_chat(query: str) -> str:
    """
    Handles general AI, ML, software engineering, and career questions.
    """
    client = get_genai_client()

    prompt = f"""
You are Pathfinder AI Mentor.

Answer the following question professionally and clearly.

Question:
{query}

Always provide a complete answer in markdown.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Failed to answer question: {str(e)}"