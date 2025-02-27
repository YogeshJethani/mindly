import streamlit as st
from utils.auth import authenticate, create_user

def login_page():
    """Display login page."""
    st.title("🧭 AI Career Navigator")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if email and password:
                    success, result = authenticate(email, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.session_state.user_name = result["name"]
                        st.session_state.user_id = str(result["_id"])
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("Please enter both email and password")
    
    with tab2:
        with st.form("signup_form"):
            st.subheader("Create Account")
            name = st.text_input("Full Name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Sign Up")
            
            if submit:
                if name and email and password and confirm_password:
                    if password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = create_user(email, password, name)
                        if success:
                            st.success(message)
                            st.info("Please login with your new account")
                        else:
                            st.error(message)
                else:
                    st.warning("Please fill all fields")