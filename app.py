import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Firebase App
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {e}")
db = firestore.client()

def signup(name, email, password):
    users_ref = db.collection('users')
    user = users_ref.where("email", "==", email).get()
    
    if user:
        st.error("User with this email already exists!")
    else:
        encrypted_password = generate_password_hash(password)
        users_ref.add({
            "name": name,
            "email": email,
            "password": encrypted_password
        })
        st.success("Signup successful! Redirecting to Login...")
        st.session_state.page = "Login"  # Redirect to Login page immediately

def login(identifier, password):
    users_ref = db.collection('users')
    user = users_ref.where("email", "==", identifier).get()
    if not user:
        user = users_ref.where("name", "==", identifier).get()

    if not user:
        st.error("User not found!")
    else:
        user_data = user[0].to_dict()
        if check_password_hash(user_data["password"], password):
            st.success(f"Welcome, {user_data['name']}! Redirecting to Dashboard...")
            st.session_state.page = "Dashboard"  # Redirect to Dashboard
        else:
            st.error("Incorrect password!")

def dashboard():
    st.title("Dashboard")
    st.write("Welcome to your dashboard!")
    if st.button("Logout"):
        st.session_state.page = "Login"  # Logout and go to Login page

def main():
    # Initialize session state for page navigation
    if "page" not in st.session_state:
        st.session_state.page = "Signup"  # Default to Signup page

    # Page navigation
    if st.session_state.page == "Signup":
        st.title("Signup")
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        
        if st.button("Signup"):
            if name and email and password:
                signup(name, email, password)
            else:
                st.warning("Please fill all the fields.")

        if st.button("Go to Login"):
            st.session_state.page = "Login"  # Navigate to Login page

    elif st.session_state.page == "Login":
        st.title("Login")
        identifier = st.text_input("Name or Email", key="login_identifier")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if identifier and password:
                login(identifier, password)
            else:
                st.warning("Please fill all the fields.")
        
        if st.button("Go to Signup"):
            st.session_state.page = "Signup"  # Navigate back to Signup page

    elif st.session_state.page == "Dashboard":
        dashboard()

if __name__ == '__main__':
    main()
