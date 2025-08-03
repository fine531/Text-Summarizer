# Text Summarizer API

A minimal FastAPI application that summarizes text using Hugging Face's `facebook/bart-large-cnn` model.

## Features

- REST API with FastAPI
- Text summarization using Hugging Face Inference API
- Environment variable configuration
- JSON input/output
- Error handling for API failures

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your Hugging Face API token

3. Run the application:
```bash
uvicorn main:app --reload
```

## Usage

### API Endpoints

- `GET /` - Health check
- `POST /summarize` - Summarize text

### Example Request

```bash
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your long text to summarize goes here..."}'
```

### Example Response

```json
{
  "summary": "Summarized version of your text..."
}
```

## API Documentation

Once the server is running, visit:
- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc
