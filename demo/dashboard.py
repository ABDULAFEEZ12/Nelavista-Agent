import streamlit as st
import requests

st.title("Nelavista AGENT Demo 🚀")
st.write("Autonomous AWS-powered AI agent that executes developer tasks")

task = st.text_input("Enter a task description:")

if st.button("Run Agent"):
    if task:
        response = requests.post(
            "http://127.0.0.1:8000/agent",
            json={"text": task}
        )
        if response.status_code == 200:
            st.json(response.json())
        else:
            st.error("Error running agent")
    else:
        st.warning("Please enter a task")
