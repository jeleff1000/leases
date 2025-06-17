import streamlit as st
import pandas as pd
import os

# File paths
user_file_path = "users.parquet"
repository_path = "file_repository"

# Ensure repository directory exists
if not os.path.exists(repository_path):
    os.makedirs(repository_path)

# Set up the homepage
st.title("Welcome to Guidehouse Lease Repository")

# Session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if st.session_state.logged_in:
    # Display welcome message
    user_name = st.session_state.user_email.split("@")[0]
    st.subheader(f"Welcome, {user_name}!")

    # Knowledge base dropdown
    st.subheader("Select Your Knowledge Base")
    knowledge_base = st.selectbox(
        "Choose a topic:",
        ["All", "Federal Leasing Basics", "Lease Acquisition Process", "Lease Administration", "Space Planning"]
    )
    if st.button("Submit"):
        st.write(f"You selected: {knowledge_base}")

    # File repository section
    st.subheader("File Repository")
    uploaded_files = os.listdir(repository_path)
    if uploaded_files:
        st.write("Uploaded Files:")
        for file in uploaded_files:
            st.write(file)
    else:
        st.write("No files uploaded yet.")

    # File upload box
    st.subheader("Upload a File")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        file_path = os.path.join(repository_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    # Chatbot section
    st.subheader("Chatbot")
    user_input = st.text_input("Say something to the chatbot")
    if user_input:
        st.write(f"Chatbot: {user_input}")
else:
    # Create tabs for Login and Register
    tab = st.radio("Choose an option:", ["Login", "Register"])

    if tab == "Login":
        st.subheader("Login")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Login"):
            if email.endswith("@guidehousefederal.com"):
                if os.path.exists(user_file_path):
                    users = pd.read_parquet(user_file_path)
                    if (users["email"] == email).any() and (users["password"] == password).any():
                        st.session_state.logged_in = True
                        st.session_state.user_email = email
                        st.success("Login successful!")
                    else:
                        st.error("Invalid email or password.")
                else:
                    st.error("No registered users found. Please register first.")
            else:
                st.error("Invalid email domain. Please use your @guidehousefederal.com email.")
    elif tab == "Register":
        st.subheader("Register")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        if st.button("Register"):
            if not email.endswith("@guidehousefederal.com"):
                st.error("Invalid email domain. Please use your @guidehousefederal.com email.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                new_user = pd.DataFrame({"email": [email], "password": [password]})
                if os.path.exists(user_file_path):
                    users = pd.read_parquet(user_file_path)
                    users = pd.concat([users, new_user], ignore_index=True)
                else:
                    users = new_user
                users.to_parquet(user_file_path, index=False)
                st.success("Registration successful!")