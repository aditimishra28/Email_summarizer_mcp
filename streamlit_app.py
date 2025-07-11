import streamlit as st
from transformers import pipeline
from gmail_utils import gmail_authenticate, get_recent_emails

# Load summarizer pipeline
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")
summarizer = load_summarizer()

# Streamlit page config
st.set_page_config(page_title="Email Summarizer MCP", page_icon="✉️")

# Title and description
st.title("✉️ AI Email Summarizer")
st.write("""
Welcome to your AI Email Summarizer.  
**Step 1:** Authorize Gmail access.  
**Step 2:** Select an email to summarize.  
**Step 3:** Get concise summaries instantly!
""")

# Gmail authentication button
if st.button("🔑 Authenticate with Gmail"):
    service = gmail_authenticate()
    st.session_state['service'] = service
    st.success("✅ Gmail authenticated successfully!")

# Display fetched emails and summarization option
if 'service' in st.session_state:
    st.write("### 📥 Your Recent Emails")
    emails = get_recent_emails(st.session_state['service'], max_results=5)

    for i, email in enumerate(emails):
        with st.expander(f"{i+1}. {email['subject']}"):
            st.write(email['body'])

            if st.button(f"📝 Summarize Email {i+1}"):
                with st.spinner("Generating summary..."):
                    summary = summarizer(email['body'], max_length=130, min_length=30, do_sample=False)
                    st.subheader("✅ Summary:")
                    st.success(summary[0]['summary_text'])

else:
    st.info("🔔 Please authenticate with Gmail to fetch and summarize your emails.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Hugging Face Transformers, Gmail API, and Streamlit.")


