import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

def render_skills_radar(skills_data):
    """Render a radar chart of user skills."""
    if isinstance(skills_data, str):
        try:
            skills_data = json.loads(skills_data)
        except:
            st.error("Could not parse skills data")
            return
    
    # Extract technical skills with proficiency levels
    tech_skills = {}
    if "technical_skills" in skills_data:
        for skill in skills_data["technical_skills"]:
            # Assuming skills might have a proficiency level (1-5)
            # Default to 3 if not specified
            if isinstance(skill, dict):
                tech_skills[skill.get("name", "Unknown")] = skill.get("proficiency", 3)
            else:
                tech_skills[skill] = 3
    
    if not tech_skills:
        st.warning("No technical skills found to visualize")
        return
    
    # Create radar chart
    categories = list(tech_skills.keys())
    values = list(tech_skills.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Skills Proficiency'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        title="Technical Skills Assessment",
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_career_path_timeline(career_paths_data):
    """Render a timeline visualization of possible career paths."""
    if isinstance(career_paths_data, str):
        try:
            career_paths_data = json.loads(career_paths_data)
        except:
            st.error("Could not parse career paths data")
            return
            
    # Check if data is in expected format
    if not isinstance(career_paths_data, dict) or "paths" not in career_paths_data:
        if isinstance(career_paths_data, list):
            paths = career_paths_data
        else:
            st.error("Career paths data is not in expected format")
            st.write(career_paths_data)
            return
    else:
        paths = career_paths_data["paths"]
    
    # Create tabs for each career path
    if not paths:
        st.warning("No career paths found to visualize")
        return
        
    tabs = st.tabs([f"Path {i+1}: {path.get('title', 'Career Option')}" 
                   for i, path in enumerate(paths)])
    
    for i, (tab, path) in enumerate(zip(tabs, paths)):
        with tab:
            if "progression" in path:
                # Timeline view of job progression
                progression = path["progression"]
                
                df = pd.DataFrame(progression)
                
                # Create a Gantt chart
                fig = px.timeline(
                    df, 
                    x_start="start_year", 
                    x_end="end_year", 
                    y="role",
                    color="salary_range",
                    hover_data=["key_skills"]
                )
                
                fig.update_layout(
                    title=f"Career Timeline: {path.get('title', f'Option {i+1}')}",
                    xaxis_title="Years",
                    yaxis_title="Position"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Display additional information
            st.subheader("Required Skills")
            if "required_skills" in path:
                for skill in path["required_skills"]:
                    st.write(f"- {skill}")
            
            st.subheader("Potential Earnings")
            if "salary_progression" in path:
                salary_data = path["salary_progression"]
                years = list(salary_data.keys())
                salaries = list(salary_data.values())
                
                fig = px.line(
                    x=years, 
                    y=salaries, 
                    markers=True,
                    labels={"x": "Year", "y": "Annual Salary ($)"}
                )
                
                fig.update_layout(title="Projected Salary Growth")
                st.plotly_chart(fig, use_container_width=True)

def render_learning_path(learning_data):
    """Render a visual representation of recommended learning path."""
    if isinstance(learning_data, str):
        try:
            learning_data = json.loads(learning_data)
        except:
            st.error("Could not parse learning data")
            return
    
    # Check if data is in expected format
    if not isinstance(learning_data, dict) or "recommendations" not in learning_data:
        if isinstance(learning_data, list):
            courses = learning_data
        else:
            st.error("Learning data is not in expected format")
            st.write(learning_data)
            return
    else:
        courses = learning_data["recommendations"]
    
    if not courses:
        st.warning("No learning recommendations found")
        return
    
    # Create a sequential visualization of courses
    st.subheader("Recommended Learning Path")
    
    for i, course in enumerate(courses):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"### Step {i+1}")
            if "time_commitment" in course:
                st.markdown(f"⏱️ {course['time_commitment']}")
            if "impact_score" in course:
                st.markdown(f"🎯 Impact: {course['impact_score']}/10")
                
        with col2:
            st.markdown(f"### {course.get('title', 'Course')}")
            st.markdown(course.get('description', ''))
            
            if "skills_developed" in course:
                skills = course["skills_developed"]
                if isinstance(skills, list):
                    st.markdown("**Skills developed:**")
                    for skill in skills:
                        st.markdown(f"- {skill}")
            
            if "project" in course:
                with st.expander("Suggested Project"):
                    st.markdown(course["project"])
        
        st.divider()