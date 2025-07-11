from flask import Flask, request, jsonify
from utils import summarize_email

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to Email Summarizer MCP 🚀"

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    email_text = data.get("email")
    if not email_text:
        return jsonify({"error": "No email text provided."}), 400
    result = summarize_email(email_text)
    return jsonify({"summary": result})

if __name__ == "__main__":
    app.run(debug=True)
