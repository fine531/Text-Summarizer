import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# Streamlit app
st.title("📝 Text Summarizer")
st.markdown("**Powered by Hugging Face BART Model**")

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_TOKEN = st.secrets.get("HUGGING_FACE_TOKEN", "")

if not HF_TOKEN:
    st.error("Please add HUGGING_FACE_TOKEN to Streamlit secrets")
    st.stop()

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Input text area
text_input = st.text_area(
    "Enter text to summarize:",
    height=200,
    placeholder="Paste your text here..."
)

# Summarize button
if st.button("Summarize Text", type="primary"):
    if text_input.strip():
        with st.spinner("Summarizing..."):
            try:
                payload = {
                    "inputs": text_input,
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
                    
                    st.success("Summary generated!")
                    st.subheader("📋 Summary:")
                    st.write(summary)
                    
                elif response.status_code == 503:
                    st.warning("Model is loading, please try again in a few moments")
                else:
                    st.error(f"API Error: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter some text to summarize")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Hugging Face")
