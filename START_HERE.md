# 🚀 Quick Start - Two Options

## Option 1: Demo Mode (No Model Required) ⚡

**Start immediately without downloading the model:**

```powershell
# Make sure your .env has OPENAI_API_KEY set
python app_demo.py
```

Then open **http://localhost:5000** in your browser!

This will:
- ✅ Run the full web interface
- ✅ Accept MRI image uploads
- ✅ Generate simulated analysis reports
- ❌ Uses random predictions (not real AI)

---

## Option 2: Full Production Mode (With Real Model) 🎯

### Step 1: Download Model from Google Colab

1. Open your `binary_classification.ipynb` in Google Colab
2. Add this cell at the end and run it:

```python
from google.colab import files
import os

model_path = '/content/best_modelVGG19_brain_tumor.keras'

if os.path.exists(model_path):
    print(f"Model size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
    files.download(model_path)
    print("✅ Download started!")
else:
    print("❌ Model not found - retrain the model first")
```

3. Save the downloaded file

### Step 2: Copy Model to Project

```powershell
# After downloading, move it to the models folder
Move-Item "$env:USERPROFILE\Downloads\best_modelVGG19_brain_tumor.keras" "models\"
```

### Step 3: Initialize Neo4j Knowledge Base

```powershell
python -c "from agents.knowledge_base import get_knowledge_base; from config import Config; config = Config(); kb = get_knowledge_base(config.NEO4J_URI, config.NEO4J_USERNAME, config.NEO4J_PASSWORD); kb.initialize_knowledge_base(); print('✅ Knowledge base initialized!')"
```

### Step 4: Run Full Application

```powershell
python app.py
```

Then open **http://localhost:5000**

---

### What You Need Right Now

### ✅ Already Done:
- Python packages installed
- Neo4j running in Docker
- `.env` file created
- Groq integration ready (FREE and FAST!)

### ⚠️ To Do:
1. **Get FREE Groq API key** - See `GROQ_SETUP.md` (takes 2 minutes!)
2. **Edit `.env`** - Add your Groq API key
3. **Choose mode**: Demo or Production

---

## Quick Test (Demo Mode)

```powershell
# 1. Make sure .env has OPENAI_API_KEY
# 2. Start demo
python app_demo.py
```

That's it! Open http://localhost:5000 and upload any brain MRI image.

---

## Need Help?

- **Model not found**: Use demo mode or download from Colab
- **Neo4j connection error**: Restart Neo4j with `wsl bash -c "sudo docker start neo4j"`
- **OpenAI error**: Add API key to `.env` file
