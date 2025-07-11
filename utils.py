from transformers import pipeline

# Load summarization pipeline once globally for efficiency
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_email(email_text, max_length=130, min_length=30):
    """
    Summarize the input email text using BART model.
    """
    summary = summarizer(email_text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']
