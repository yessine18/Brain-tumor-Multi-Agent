# Brain Tumor Analysis - Multi-Agent AI System

A medical image analysis system using **Multi-Agent Architecture**, **LangChain**, **Groq LLM**, **Neo4j**, and **Deep Learning** to classify brain MRI scans and generate comprehensive medical reports.

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
2. **Neo4j Database** (Docker)
3. **Groq API Key** (free tier available at https://console.groq.com)
4. **Trained Model**: `best_modelVGG19_brain_tumor.keras`

## 🚀 Installation

### Step 1: Clone and Setup

```bash
cd MULTI-AGENT
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Install Neo4j (Docker)

```bash
# Use alternative ports to avoid conflicts
docker run -d --name neo4j \
  -p 7475:7474 -p 7688:7687 \
  -e NEO4J_AUTH=neo4j/password123 \
  neo4j:5.13
```

### Step 3: Configure Environment

Create `.env` file:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
NEO4J_URI=bolt://localhost:7688
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password123
FLASK_SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
```

### Step 4: Add Your Trained Model

Place your trained model in the `models/` directory:
```
models/best_modelVGG19_brain_tumor.keras
```

### Step 5: Initialize Knowledge Base

Start the app, then visit:
```
http://localhost:5000/init-knowledge-base
```

## 🎮 Usage

### Start the Application

```bash
python app.py
```

Access at: **http://localhost:5000**

### Using the Web Interface

1. Open browser to `http://localhost:5000`
2. Upload an MRI scan (PNG, JPG, or JPEG)
3. Optional: Enter patient information
4. Click "Start Analysis"
5. Review the comprehensive report with:
   - Classification result and confidence
   - Grad-CAM visualization
   - Medical explanation from LLM
   - Treatment recommendations
   - Next steps

## 📁 Project Structure

```
MULTI-AGENT/
├── agents/
│   ├── crew.py              # Multi-agent orchestration
│   └── knowledge_base.py    # Neo4j medical knowledge base
├── models/
│   ├── classifier.py        # Brain tumor classification + Grad-CAM
│   └── best_modelVGG19_brain_tumor.keras
├── templates/
│   └── index.html           # Web interface
├── static/
│   └── results/             # Generated visualizations
├── uploads/                 # Uploaded MRI scans
├── reports/                 # Generated JSON reports
├── app.py                   # Flask application
├── config.py                # Configuration
├── requirements.txt         # Dependencies
└── .env                     # Environment variables
```

## 🔧 Configuration

Environment variables in `.env`:

- `GROQ_API_KEY`: Your Groq API key (get free at https://console.groq.com)
- `NEO4J_URI`: Neo4j connection URI (bolt://localhost:7688)
- `NEO4J_USERNAME`: Neo4j username (neo4j)
- `NEO4J_PASSWORD`: Neo4j password
- `FLASK_SECRET_KEY`: Flask session secret
- `FLASK_DEBUG`: Debug mode (True/False)

## 🤖 How It Works

### Agent Workflow

```
1. Upload MRI → 2. Classification Agent → 3. Medical Expert → 4. Report Generator
                      ↓                          ↓                    ↓
                  VGG19 Model              Neo4j Knowledge      Groq LLM
                  Grad-CAM                 Medical Context      (Llama 3.3 70B)
```

### Classification Agent
- Loads VGG19 model
- Preprocesses MRI image
- Runs binary classification (Tumor/Normal)
- Generates Grad-CAM visualization
- Returns confidence score

### Medical Expert Agent
- Queries Neo4j knowledge base for:
  - Common symptoms
  - Causes and risk factors
  - Treatment options
  - Diagnostic methods
- Provides medical context to LLM

### Report Generator Agent
- Synthesizes all information
- Uses Groq LLM (Llama 3.3 70B) to create:
  - Executive summary
  - Classification results
  - Visual analysis interpretation
  - Medical explanation
  - Treatment recommendations
  - Disclaimers

## 📊 API Endpoints

- `GET /` - Web interface
- `POST /upload` - Upload MRI scan
- `POST /analyze` - Run analysis
- `GET /init-knowledge-base` - Initialize Neo4j knowledge base
- `GET /health` - Health check
- `GET /reports/<filename>` - Download report

## 🛠️ Troubleshooting

### Model Not Found
```
Error: Model not found at models/best_modelVGG19_brain_tumor.keras
```
**Solution**: Place your trained model in the `models/` directory

### Neo4j Connection Error
```
Error: Couldn't connect to localhost:7688
```
**Solution**: 
- Ensure Neo4j Docker container is running: `docker ps`
- Start container: `docker start neo4j`
- Check ports: Neo4j should be on 7475 (HTTP) and 7688 (Bolt)

### NumPy Version Error
```
AttributeError: _ARRAY_API not found
```
**Solution**: 
```bash
pip install "numpy<2.0"
```

### Groq API Error
```
Error: Invalid API key
```
**Solution**: Get a free API key at https://console.groq.com and add to `.env`

## 🔐 Security Notes

- Never commit `.env` file to version control
- Keep your Groq API key secure
- Change Flask secret key in production
- Use HTTPS in production
- This is a demo/research tool, not for clinical use

## 📄 License

This project is for educational and research purposes only. Not intended for clinical diagnosis.

## 🎓 Technologies

- **VGG19**: Transfer learning for tumor classification
- **Grad-CAM**: Explainable AI visualization
- **LangChain**: LLM orchestration
- **Groq**: Fast LLM inference (Llama 3.3 70B)
- **Neo4j**: Medical knowledge graph database
- **Flask**: Web application framework
- **TensorFlow/Keras**: Deep learning framework

---

**⚠️ Medical Disclaimer**: This system is for educational and research purposes only. Always consult qualified healthcare professionals for medical diagnosis and treatment.
