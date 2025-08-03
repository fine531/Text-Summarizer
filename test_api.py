import requests

# Test the summarization API
def test_summarize_api():
    url = "http://localhost:8000/summarize"
    
    # Sample text to summarize
    sample_text = """
    FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ 
    based on standard Python type hints. The key features are: Fast: Very high performance, on par 
    with NodeJS and Go (thanks to Starlette and Pydantic). Fast to code: Increase the speed to develop 
    features by about 200% to 300%. Fewer bugs: Reduce about 40% of human (developer) induced errors. 
    Intuitive: Great editor support. Completion everywhere. Less time debugging. Easy: Designed to be 
    easy to use and learn. Less time reading docs. Short: Minimize code duplication. Multiple features 
    from each parameter declaration. Fewer bugs. Robust: Get production-ready code. With automatic 
    interactive documentation.
    """
    
    payload = {"text": sample_text.strip()}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ API Test Successful!")
            print(f"Original text length: {len(sample_text)} characters")
            print(f"Summary length: {len(result['summary'])} characters")
            print(f"\n📝 Summary: {result['summary']}")
        else:
            print(f"❌ API Test Failed! Status: {response.status_code}")
            print(f"Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"❌ Response Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Text Summarizer API...")
    test_summarize_api()
