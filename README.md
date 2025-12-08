# Brain Tumor Analysis - Multi-Agent AI System

A sophisticated medical image analysis system using **CrewAI**, **LangChain**, **Neo4j**, and **Deep Learning** to classify brain MRI scans and generate comprehensive medical reports.

## 🎯 Features

- **Multi-Agent AI System**: Three specialized AI agents working together
  - 🤖 **Classification Agent**: Uses VGG19 deep learning model to detect tumors
  - 🧑‍⚕️ **Medical Expert Agent**: Provides medical explanations using Neo4j knowledge base
  - 📋 **Report Generator Agent**: Creates comprehensive medical reports

- **Explainable AI**: Grad-CAM visualizations showing which brain regions influenced the diagnosis
- **Knowledge Base**: Neo4j graph database with medical information about brain tumors
- **Web Interface**: Easy-to-use Flask web application
- **Comprehensive Reports**: Detailed analysis including diagnosis, confidence, symptoms, causes, and treatments

## 📋 Prerequisites

1. **Python 3.9+**
2. **Neo4j Database** (Community Edition or Docker)
3. **OpenAI API Key** (or other LLM provider)
4. **Trained Model**: `best_modelVGG19_brain_tumor.keras`

## 🚀 Installation

### Step 1: Clone and Setup

```powershell
# Navigate to project directory
cd "C:\Users\USER\Desktop\MULTI-AGENT"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install Neo4j

#### Option A: Docker (Recommended)
```powershell
docker run -d `
  --name neo4j `
  -p 7474:7474 -p 7687:7687 `
  -e NEO4J_AUTH=neo4j/your_password `
  neo4j:latest
```

#### Option B: Desktop Application
Download from: https://neo4j.com/download/

### Step 3: Configure Environment

1. Copy the example environment file:
```powershell
Copy-Item .env.example .env
```

2. Edit `.env` and add your credentials:
```env
OPENAI_API_KEY=sk-your-openai-key-here
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password
FLASK_SECRET_KEY=your-secret-key-here
```

### Step 4: Add Your Trained Model

Copy your trained model to the `models/` directory:
```powershell
# If your model is in the current directory
Copy-Item best_modelVGG19_brain_tumor.keras models\
```

### Step 5: Initialize Knowledge Base

```powershell
# Run Python shell
python

# In Python:
from agents.knowledge_base import get_knowledge_base
from config import Config

config = Config()
kb = get_knowledge_base(config.NEO4J_URI, config.NEO4J_USERNAME, config.NEO4J_PASSWORD)
kb.initialize_knowledge_base()
exit()
```

Or use the web interface after starting the app (see below).

## 🎮 Usage

### Start the Application

```powershell
python app.py
```

The application will start at: **http://localhost:5000**

### Using the Web Interface

1. **Open your browser** to `http://localhost:5000`
2. **Upload an MRI scan** (PNG, JPG, or JPEG)
3. **Optional**: Enter patient information
4. **Click "Start Analysis"**
5. **Wait** for the multi-agent system to complete analysis
6. **Review** the comprehensive report with:
   - Classification result and confidence
   - Grad-CAM visualization
   - Medical explanation
   - Treatment recommendations
   - Next steps

### Initialize Knowledge Base (First Time)

After starting the app, you can initialize the Neo4j knowledge base by making a POST request:

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/init-knowledge-base" -Method POST
```

Or use curl:
```powershell
curl -X POST http://localhost:5000/init-knowledge-base
```

## 📁 Project Structure

```
MULTI-AGENT/
├── agents/
│   ├── crew.py              # CrewAI multi-agent system
│   └── knowledge_base.py    # Neo4j medical knowledge base
├── models/
│   ├── classifier.py        # Brain tumor classification model
│   └── best_modelVGG19_brain_tumor.keras  # Your trained model
├── templates/
│   └── index.html           # Web interface
├── static/
│   └── results/             # Generated visualizations
├── uploads/                 # Uploaded MRI scans
├── reports/                 # Generated JSON reports
├── app.py                   # Flask application
├── config.py                # Configuration
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (create from .env.example)
```

## 🔧 Configuration

Edit `config.py` or set environment variables in `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `NEO4J_URI`: Neo4j connection URI (default: bolt://localhost:7687)
- `NEO4J_USERNAME`: Neo4j username (default: neo4j)
- `NEO4J_PASSWORD`: Neo4j password
- `MODEL_PATH`: Path to trained model
- `UPLOAD_FOLDER`: Directory for uploaded images
- `REPORTS_FOLDER`: Directory for generated reports

## 🧪 Testing

### Test with Sample Image

```powershell
# Using curl
curl -X POST -F "file=@path\to\brain_scan.jpg" http://localhost:5000/upload
curl -X POST http://localhost:5000/analyze
```

### Health Check

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

## 🤖 How It Works

### Agent Workflow

```
1. Upload MRI → 2. Classification Agent → 3. Medical Expert → 4. Report Generator
                      ↓                          ↓
                  VGG19 Model              Neo4j Knowledge Base
                  Grad-CAM                 (Symptoms, Causes, Treatments)
```

### Classification Agent
- Loads the VGG19 model
- Preprocesses the MRI image
- Runs classification (Tumor/Normal)
- Generates Grad-CAM visualization
- Returns confidence score

### Medical Expert Agent
- Queries Neo4j knowledge base
- Retrieves information about:
  - Common symptoms
  - Possible causes and risk factors
  - Treatment options
  - Diagnostic methods
- Provides medical context

### Report Generator Agent
- Synthesizes all information
- Creates comprehensive report with:
  - Executive summary
  - Classification results
  - Visual analysis
  - Medical explanation
  - Recommendations
  - Disclaimers

## 📊 API Endpoints

- `GET /` - Web interface
- `POST /upload` - Upload MRI scan
- `POST /analyze` - Run analysis
- `GET /reports/<filename>` - Download report
- `POST /init-knowledge-base` - Initialize Neo4j
- `GET /health` - Health check

## 🛠️ Troubleshooting

### Model Not Found
```
Error: Model not found at models/best_modelVGG19_brain_tumor.keras
```
**Solution**: Copy your trained model to the `models/` directory

### Neo4j Connection Error
```
Error: Failed to connect to Neo4j
```
**Solution**: 
- Ensure Neo4j is running
- Check credentials in `.env`
- Verify port 7687 is not blocked

### OpenAI API Error
```
Error: Invalid API key
```
**Solution**: 
- Add valid OpenAI API key to `.env`
- Or use alternative LLM provider in `agents/crew.py`

### TensorFlow/CUDA Warnings
```
Warning: Could not load dynamic library 'cudart64_110.dll'
```
**Solution**: TensorFlow will use CPU (slower but works). For GPU support, install CUDA toolkit.

## 🔐 Security Notes

- **Never commit `.env` file** to version control
- Keep your OpenAI API key secure
- Change default Flask secret key in production
- Use HTTPS in production
- Implement authentication for production use
- This is a demo/research tool, not for clinical use

## 📄 License

This project is for educational and research purposes only. Not intended for clinical diagnosis.

## 🤝 Contributing

This is a demonstration project. For production use, consider:
- Adding user authentication
- Implementing HIPAA compliance
- Adding model versioning
- Implementing audit logging
- Adding more comprehensive error handling

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in the terminal
3. Ensure all prerequisites are installed

## 🎓 Credits

- **VGG19 Model**: Transfer learning from ImageNet
- **CrewAI**: Multi-agent orchestration
- **LangChain**: LLM integration
- **Neo4j**: Medical knowledge graph
- **Flask**: Web framework

---

**⚠️ Medical Disclaimer**: This system is for educational and research purposes only. Always consult qualified healthcare professionals for medical diagnosis and treatment.
