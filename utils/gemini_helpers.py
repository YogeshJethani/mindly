import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def initialize_gemini_model():
    """Initialize the Gemini model."""
    return genai.GenerativeModel('gemini-2.0-flash')

def extract_skills_from_profile(profile_text):
    """Extract skills from user profile using Gemini."""
    model = initialize_gemini_model()
    
    prompt = f"""
    Please analyze this professional profile and extract the following:
    1. Technical skills
    2. Soft skills
    3. Industry knowledge
    4. Years of experience in each skill (if mentioned)
    5. Proficiency level (if indicated)
    
    Format the output as a JSON object with these categories as keys.
    
    Profile:
    {profile_text}
    """
    
    response = model.generate_content(prompt)
    return response.text

def generate_career_paths(current_role, skills, target_industry=None):
    """Generate possible career paths based on skills and current role."""
    model = initialize_gemini_model()
    
    prompt = f"""
    Based on this professional's current role as {current_role} and their skills:
    {skills}
    
    Generate 3-5 possible career paths they could pursue {"in the " + target_industry if target_industry else ""}.
    
    For each path include:
    1. Job title progression (3-4 roles)
    2. Key skills needed to advance
    3. Estimated timeline
    4. Potential salary progression
    
    Format as a JSON object with an array of career paths.
    """
    
    response = model.generate_content(prompt)
    return response.text


def recommend_learning_path(current_skills, target_role):
    """Generate personalized learning recommendations."""
    model = initialize_gemini_model()
    
    prompt = f"""
    Create a personalized learning path for someone with these skills:
    {current_skills}
    
    Who wants to become a {target_role}.
    
    Include:
    1. 5-7 courses in recommended sequence
    2. Estimated time commitment for each
    3. Key skills each course will develop
    4. Specific projects they should complete to demonstrate skills
    
    Format as a JSON object with an array of learning items.
    """
    
    response = model.generate_content(prompt)
    return response.text