# Quick Start Guide

## 🚀 Get Started in 5 Steps

### 1️⃣ Install Dependencies
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt
```

### 2️⃣ Setup Neo4j (Choose One)

**Option A - Docker (Easiest):**
```powershell
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password123 neo4j:latest
```

**Option B - Desktop:**
Download from https://neo4j.com/download/

### 3️⃣ Configure Environment
```powershell
# Copy template
Copy-Item .env.example .env

# Edit .env and add:
# - OPENAI_API_KEY=your_key_here
# - NEO4J_PASSWORD=your_password
```

### 4️⃣ Add Your Model
```powershell
# Copy your trained model
Copy-Item best_modelVGG19_brain_tumor.keras models\
```

### 5️⃣ Run Setup & Start
```powershell
# Run setup check (optional but recommended)
python setup.py

# Start the application
python app.py
```

🎉 **Open browser to http://localhost:5000**

---

## 🔧 First Time Setup

After starting the app, initialize the knowledge base:
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/init-knowledge-base" -Method POST
```

---

## 📱 Using the App

1. Upload a brain MRI scan (PNG/JPG)
2. Optionally add patient info
3. Click "Start Analysis"
4. View results with:
   - Classification (Tumor/Normal)
   - Confidence score
   - Grad-CAM visualization
   - Comprehensive medical report

---

## ⚠️ Troubleshooting

**Model Not Found?**
- Copy `best_modelVGG19_brain_tumor.keras` to `models/` folder

**Neo4j Connection Failed?**
- Check Neo4j is running: `docker ps` or Neo4j Desktop
- Verify password in `.env` matches Neo4j

**OpenAI API Error?**
- Add valid API key to `.env` file

---

## 📚 More Help

See full documentation in `README.md`
