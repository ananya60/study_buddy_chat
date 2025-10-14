import streamlit as st
from transformers import pipeline

# -----------------------------
# Load Model (uses small CPU model)
# -----------------------------
@st.cache_resource
def load_model():
    return pipeline(
        "text-generation",
        model="distilgpt2",   # small & fast model
    )

generator = load_model()

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Study Buddy Chat", page_icon="🎓", layout="centered")

st.title("🎓 Study Buddy Chat")
st.write("Ask any question and your AI study buddy will help you out!")

# User input
user_input = st.text_input("💬 Type your question here:")

# Generate answer
if st.button("Ask"):
    if user_input.strip() == "":
        st.warning("Please enter a question!")
    else:
        with st.spinner("Thinking..."):
            response = generator(user_input, max_length=100, num_return_sequences=1)
            st.success(response[0]["generated_text"])
