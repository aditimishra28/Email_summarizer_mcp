import streamlit as st
from transformers import pipeline

# Load summarizer pipeline globally to avoid reloading every run
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

st.title("✉️ Email Summarizer MCP")
st.write("Summarize your emails into concise bullet points using BART model (no API key needed).")

# Text input
email_text = st.text_area("Paste your email text here:", height=200)

if st.button("Summarize"):
    if not email_text.strip():
        st.warning("Please enter email text to summarize.")
    else:
        with st.spinner("Summarizing..."):
            summary = summarizer(email_text, max_length=130, min_length=30, do_sample=False)
            st.subheader("📋 Summary:")
            st.success(summary[0]['summary_text'])

st.markdown("---")
st.caption("Built with ❤️ using Hugging Face Transformers and Streamlit.")
