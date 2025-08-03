"""
Text Summarizer API using FastAPI and Hugging Face BART model.

This module provides a web API for text summarization using the
facebook/bart-large-cnn model through Hugging Face's Inference API.
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Text Summarizer API",
    description="Summarize text using Hugging Face BART model"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models for request and response
class TextInput(BaseModel):
    """Input model for text to be summarized."""
    text: str

class SummaryOutput(BaseModel):
    """Output model for summarized text."""
    summary: str

# Hugging Face API configuration
HF_API_URL = (
    "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
)
HF_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if not HF_TOKEN:
    raise ValueError("HUGGING_FACE_TOKEN environment variable is required")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

@app.get("/")
async def root():
    """Serve the main UI"""
    return FileResponse('static/index.html')

@app.get("/api")
async def api_info():
    """Get API information."""
    return {
        "message": "Text Summarizer API - Use POST /summarize to summarize text"
    }

@app.post("/summarize", response_model=SummaryOutput)
async def summarize_text(input_data: TextInput):
    """
    Summarize the provided text using Hugging Face's BART model.
    """
    try:
        # Prepare the payload for Hugging Face API
        payload = {
            "inputs": input_data.text,
            "parameters": {
                "max_length": 150,
                "min_length": 30,
                "do_sample": False
            }
        }
        
        # Make request to Hugging Face API
        response = requests.post(
            HF_API_URL, 
            headers=headers, 
            json=payload, 
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            # Extract the summary text from the response
            summary = (
                result[0]["summary_text"] 
                if result and len(result) > 0 
                else "No summary generated"
            )
            return SummaryOutput(summary=summary)
        elif response.status_code == 503:
            raise HTTPException(
                status_code=503, 
                detail="Model is loading, please try again in a few moments"
            )
        else:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Error from Hugging Face API: {response.text}"
            )

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Request failed: {str(e)}"
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        ) from e

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
