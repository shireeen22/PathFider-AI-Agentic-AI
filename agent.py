import os
import sys

# Ensure the career_mentor directory is in the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.agents.llm_agent import Agent
from tools import (
    generate_learning_roadmap,
    recommend_projects,
    recommend_courses,
    generate_interview_prep,
    review_resume,
    review_resume_pdf,
    general_ai_chat
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='career_mentor_agent',
    description=(
        'A comprehensive AI Learning and Career Mentor Agent that guides students '
        'and professionals in AI, ML, Data Science, Software Engineering, and GenAI.'
    ),
    instruction=(
    "You are an expert AI and Technical Career Mentor. Your goal is to guide "
    "students and aspiring professionals into successful careers in AI, Machine Learning, "
    "Generative AI, Data Science, and Software Engineering.\n\n"

    "You have access to specialized tools for different tasks:\n"
    "1. generate_learning_roadmap: Use this to generate structured milestones and learning paths.\n"
    "2. recommend_projects: Use this to recommend hands-on projects, datasets, and technologies.\n"
    "3. recommend_courses: Use this to suggest courses (free or paid) on any topic.\n"
    "4. generate_interview_prep: Use this to generate mock technical interview questions and answers.\n"
    "5. review_resume: Use this if the user pastes resume/CV text.\n"
    "6. review_resume_pdf: Use this if the user provides a local path to a PDF resume.\n"
    "7. general_ai_chat: Use this for general AI, ML, Data Science, Software Engineering, "
    "career guidance, skills, technologies, and job preparation questions.\n\n"

    "Always delegate to the most appropriate tool when users request these services. "
    "For general questions, use the general_ai_chat tool.\n\n"

    "After using any tool, summarize the output in a clear, professional, and encouraging manner.\n"
    "Always provide a complete final answer to the user.\n"
    "Never end without generating a user-facing response.\n"
),
    tools=[
    generate_learning_roadmap,
    recommend_projects,
    recommend_courses,
    generate_interview_prep,
    review_resume,
    review_resume_pdf,
    general_ai_chat
    ]
)

