import streamlit as st
from dotenv import load_dotenv
import os
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Check API key
if not api_key:
    st.error("GEMINI_API_KEY is missing. Please add it to your .env file.")
    st.stop()

# Create Gemini client
client = genai.Client(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="Course AI Chatbot",
    page_icon="🎓",
    layout="centered"
)

# Title
st.title("🎓 Course AI Chatbot")
st.write("Ask questions about your courses and subjects!")

# Course/subject selection
subject = st.selectbox(
    "Select Subject",
    [
        "General",
        "Python",
        "Java",
        "DBMS",
        "Data Structures",
        "Operating Systems",
        "Computer Networks",
        "Artificial Intelligence",
        "Machine Learning",
        "Business Economics"
    ]
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_question = st.chat_input("Ask your question...")

if user_question:

    # Display user message
    with st.chat_message("user"):
        st.write(user_question)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # AI instructions
    prompt = f"""
You are a helpful AI tutor for college students.

The selected subject is: {subject}

Answer the student's question clearly and simply.

Rules:
1. Explain concepts in beginner-friendly language.
2. Give examples when useful.
3. For programming questions, provide correct code.
4. For exam questions, give point-wise answers.
5. If the student asks for a 5-mark answer, give a suitable 5-mark answer.
6. If the student asks for a 10-mark answer, give a suitable 10-mark answer.
7. Use headings and bullet points when useful.
8. Do not give unnecessary information.
9. If the question is unrelated to academics, politely say that you are a course AI tutor.

Student question:
{user_question}
"""

    try:
        # Get AI response
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        answer = response.text

        # Display AI response
        with st.chat_message("assistant"):
            st.write(answer)

        # Save AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    except Exception as e:
        st.error(f"Error: {e}")
        