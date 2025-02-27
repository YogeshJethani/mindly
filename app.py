import streamlit as st
import json
import uuid
from pages.login import login_page  # Import login page
from utils.gemini_helpers import (
    extract_skills_from_profile,
    generate_career_paths, 
    recommend_learning_path
)
from utils.db_helpers import (
    save_user_profile,
    get_user_profile,
    save_career_paths,
    save_learning_path
)
from components.visualizations import (
    render_skills_radar,
    render_career_path_timeline,
    render_learning_path
)

# Initialize session for authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show login page if not logged in
if not st.session_state.logged_in:
    login_page()
else:
    # App configuration
    st.set_page_config(
        page_title="AI Career Navigator",
        page_icon="🤯",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if "user_id" not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    if "profile_submitted" not in st.session_state:
        st.session_state.profile_submitted = False
    if "career_goals_submitted" not in st.session_state:
        st.session_state.career_goals_submitted = False
    if "skills_data" not in st.session_state:
        st.session_state.skills_data = None
    if "career_paths" not in st.session_state:
        st.session_state.career_paths = None
    if "learning_path" not in st.session_state:
        st.session_state.learning_path = None

    # App header
    st.title("🧭 AI Career Navigator")
    st.markdown("Use the power of AI to map your career journey and get personalized learning recommendations")

    # Sidebar for user input
    with st.sidebar:
        st.header("Your Career Profile")
        
        # Profile input
        if not st.session_state.profile_submitted:
            with st.form("profile_form"):
                st.subheader("Professional Background")
                current_role = st.text_input("Current Role")
                years_experience = st.slider("Years of Experience", 0, 30, 5)
                
                profile_text = st.text_area(
                    "Paste your professional profile (LinkedIn, resume, etc.)",
                    height=300,
                    help="The more details you provide, the better recommendations you'll get"
                )
                
                submit_profile = st.form_submit_button("Analyze My Profile")
                
                if submit_profile and profile_text:
                    with st.spinner("Analyzing your professional profile..."):
                        # Extract skills using Gemini
                        skills_json = extract_skills_from_profile(profile_text)
                        try:
                            skills_data = json.loads(skills_json)
                            st.session_state.skills_data = skills_data
                            
                            # Save to database
                            user_data = {
                                "user_id": st.session_state.user_id,
                                "current_role": current_role,
                                "years_experience": years_experience,
                                "profile_text": profile_text,
                                "extracted_skills": skills_data
                            }
                            save_user_profile(st.session_state.user_id, user_data)
                            
                            st.session_state.profile_submitted = True
                            st.success("Profile analyzed successfully!")
                            st.rerun()
                        except json.JSONDecodeError:
                            st.error("Error processing skills. Please try again.")
                            st.code(skills_json)
    
    # Main content area
    if not st.session_state.profile_submitted:
        st.header("Welcome to AI Career Navigator!")
        st.info("To get started, enter your professional details in the sidebar.")
    else:
        tab1, tab2, tab3 = st.tabs(["Skills Assessment", "Career Paths", "Learning Plan"])
        
        with tab1:
            st.header("Your Skills Profile")
            if st.session_state.skills_data:
                render_skills_radar(st.session_state.skills_data)
        
        with tab2:
            st.header("Potential Career Paths")
            if st.session_state.career_goals_submitted and st.session_state.career_paths:
                render_career_path_timeline(st.session_state.career_paths)
        
        with tab3:
            st.header("Your Personalized Learning Plan")
            if st.session_state.career_goals_submitted and st.session_state.learning_path:
                render_learning_path(st.session_state.learning_path)
    
    # Footer
    st.divider()
    st.markdown("*AI Career Navigator - Powered by Gemini AI*")