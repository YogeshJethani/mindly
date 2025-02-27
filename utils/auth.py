import streamlit as st
import hashlib
import os
from utils.db_helpers import get_db_connection

def hash_password(password):
    """Hash a password for storing."""
    salt = os.environ.get('PASSWORD_SALT', 'default_salt')
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest()

def create_user(email, password, name):
    """Create a new user."""
    db = get_db_connection()
    auth_users = db.auth_users
    
    # Check if user already exists
    if auth_users.find_one({"email": email}):
        return False, "Email already registered"
    
    # Create new user
    user = {
        "email": email,
        "password": hash_password(password),
        "name": name
    }
    
    auth_users.insert_one(user)
    return True, "User created successfully"

def authenticate(email, password):
    """Authenticate a user."""
    db = get_db_connection()
    auth_users = db.auth_users
    
    user = auth_users.find_one({"email": email})
    if not user:
        return False, "Invalid email or password"
    
    if user["password"] != hash_password(password):
        return False, "Invalid email or password"
    
    return True, user