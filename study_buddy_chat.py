import streamlit as st
import re

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Relevant Study Buddy", page_icon="🎓", layout="centered")
st.title("🎓 Study Buddy (Relevant Answers)")
st.write("Upload your notes and get relevant answers to your questions!")

# -----------------------------
# Chat session storage
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Upload notes
# -----------------------------
uploaded_file = st.file_uploader("Upload your study notes (.txt)", type=["txt"])
notes_text = ""
sentences = []

if uploaded_file is not None:
    notes_text = uploaded_file.read().decode("utf-8")
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?]) +', notes_text)
    st.success(f"Notes loaded successfully! Total sentences: {len(sentences)}")

# -----------------------------
# Function to compute Jaccard similarity
# -----------------------------
def jaccard_similarity(a, b):
    a_set = set(a.lower().split())
    b_set = set(b.lower().split())
    if not a_set or not b_set:
        return 0
    return len(a_set & b_set) / len(a_set | b_set)

# -----------------------------
# Function to get most relevant answer
# -----------------------------
def get_answer(question, top_n=1):
    if not sentences:
        return "Please upload study notes first!"
    
    scored_sentences = []
    for sentence in sentences:
        score = jaccard_similarity(question, sentence)
        scored_sentences.append((score, sentence))
    
    # Sort sentences by similarity score descending
    scored_sentences.sort(reverse=True, key=lambda x: x[0])
    
    # If top score is 0 → no relevant answer found
    if scored_sentences[0][0] == 0:
        return "Sorry, I couldn't find a relevant answer. Try rephrasing."
    
    # Return top N relevant sentences
    relevant_sentences = [s for score, s in scored_sentences[:top_n]]
    return " ".join(relevant_sentences)

# -----------------------------
# User input
# -----------------------------
user_question = st.text_input("💬 Type your question here:")

if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question!")
    else:
        answer = get_answer(user_question, top_n=2)  # top 2 sentences
        st.session_state.history.append({"question": user_question, "answer": answer})

# -----------------------------
# Display chat history
# -----------------------------
for chat in st.session_state.history:
    st.markdown(f"**You:** {chat['question']}")
    st.markdown(f"**Study Buddy:** {chat['answer']}")
    st.markdown("---")
