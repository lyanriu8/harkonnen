# Harkonnen

Harkonnen is a full-stack application that analyzes social-media posts from influential public figures (politicians, CEOs, financial influencers) and correlates them with real financial market movements.

## 🧠 Core Features
### 🔍 NLP Pipeline
1. Scraping posts (Truth Social / X / via scrapers/APIs)
2. Preprocessing with regex + normalization
3. Sentiment analysis using FinBERT (ProsusAI)
4. Entity extraction with spaCy NER
5. Fuzzy ticker/company matching with CSV + difflib
6. Semantic RAG search with FAISS + MiniLM

### 📊 Market Analysis
- Yahoo Finance API integration
- Compute 1-day / 7-day (or configurable) price changes
- Influence scoring for posts and users

### 🖥 Frontend Dashboard
- Search and select influencers
- Visual timeline of posts with sentiment
- Plot stock price vs post timestamps
- Potential leaderboard + trading methodology explanation page

### Rough Architecture
``` text
└── harkonnen/
    ├── backend/                       
    │   ├── app/
    │   │   ├── api/
    │   │   ├── models/
    │   │   ├── nlp/
    │   └── tests/
    ├── frontend/
    │   ├── public/
    │   ├── src/
    │   │   ├── components/
    │   │   ├── pages/
    │   │   ├── config/
    │   │   ├── utils/
    │   │   ├── App.jsx
    │   │   └── main.jsx
    │   └── package.json
    └── venv/
```

# Setup
### Backend
``` bash
cd backend
python -m venv ../venv
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
``` bash
touch .env

#populate

APP_NAME="Harkonnen"
VERSION=1.0.0
API_PREFIX="/harkonnen"

HOST=0.0.0.0
PORT=8000

ALLOWED_ORIGINS= [ "http://localhost:5173", "http://localhost:3000"]

TRUTHSOCIAL_USERNAME=...
TRUTHSOCIAL_PASSWORD=...
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### API
Endpoint documentation available at `http://localhost:8000/docs#/`

