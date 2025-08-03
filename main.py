"""
Text Summarizer API using Flask and Hugging Face BART model.
"""
import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if not HF_TOKEN:
    raise ValueError("HUGGING_FACE_TOKEN environment variable is required")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@app.route("/")
def root():
    """Serve the main UI"""
    return send_from_directory('static', 'index.html')

@app.route("/api")
def api_info():
    """Get API information."""
    return jsonify({
        "message": "Text Summarizer API - Use POST /summarize to summarize text"
    })

@app.route("/summarize", methods=["POST"])
def summarize_text():
    """Summarize text using Hugging Face API"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided"}), 400
            
        text = data['text']
        
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": 150,
                "min_length": 30,
                "do_sample": False
            }
        }
        
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            summary = result[0]["summary_text"] if result and len(result) > 0 else "No summary generated"
            return jsonify({"summary": summary})
        elif response.status_code == 503:
            return jsonify({"error": "Model is loading, please try again in a few moments"}), 503
        else:
            return jsonify({"error": f"API Error: {response.status_code}"}), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
