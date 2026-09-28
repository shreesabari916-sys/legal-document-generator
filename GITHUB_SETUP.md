# GitHub Setup

1. Copy `.env.example` to `.env`.
2. Put your own API key in `.env`.
3. Install dependencies: `pip install -r requirements.txt`
4. Start backend: `uvicorn backend.main:app --reload`
5. Start frontend in another terminal: `streamlit run frontend/app.py`

## Push to your own GitHub repository

```bash
git init
git add .
git commit -m "Initial LegalEase project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/LegalEase.git
git push -u origin main
```

Never commit `.env` or API keys.
