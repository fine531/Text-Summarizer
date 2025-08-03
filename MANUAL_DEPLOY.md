# Manual Deployment Guide

## 🚀 Quick Manual Deployment Options:

### **Option 1: Streamlit Cloud (EASIEST!)**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Deploy from `fine531/Text-Summarizer`
4. Main file: `streamlit_app.py`
5. Requirements: `requirements_streamlit.txt`
6. Add secret: `HUGGING_FACE_TOKEN` = your token
7. Deploy! ✅

### **Option 2: Railway**
1. Go to [railway.app](https://railway.app)
2. "Deploy from GitHub repo"
3. Select your repository
4. Add environment variable
5. Auto-deploy! ✅

### **Option 3: Heroku CLI**
```bash
# Install Heroku CLI first
heroku login
heroku create your-app-name
heroku config:set HUGGING_FACE_TOKEN=your_token
git push heroku main
```

### **Option 4: PythonAnywhere**
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Upload your files
3. Create web app
4. Configure WSGI file
5. Set environment variables

### **Option 5: Replit**
1. Go to [replit.com](https://replit.com)
2. Import from GitHub
3. Add secrets in environment
4. Run and deploy

## 🎯 Recommended: Streamlit Cloud
- Simplest setup
- Free hosting
- Great for Python apps
- No server configuration needed

Choose the option that works best for you!
