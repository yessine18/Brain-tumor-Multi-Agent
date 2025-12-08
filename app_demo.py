"""
Demo/Test Mode - Run the app without the trained model
This creates a mock classifier for testing the multi-agent system
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify, send_from_directory, session
import json
from datetime import datetime
import logging
from werkzeug.utils import secure_filename
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORTS_FOLDER'] = 'reports'
app.config['DEBUG'] = True
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ensure directories exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('reports', exist_ok=True)
os.makedirs('static/results', exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(filepath)
            logger.info(f"File uploaded: {filepath}")
            
            patient_info = None
            if request.form.get('patient_name') or request.form.get('patient_age'):
                patient_info = {
                    'name': request.form.get('patient_name', 'N/A'),
                    'age': request.form.get('patient_age', 'N/A'),
                    'gender': request.form.get('patient_gender', 'N/A')
                }
            
            session['current_image'] = filepath
            session['patient_info'] = patient_info
            
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        filepath = session.get('current_image')
        patient_info = session.get('patient_info')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'No image file found'}), 400
        
        logger.info(f"Starting DEMO analysis for: {filepath}")
        
        # DEMO MODE - Mock results
        import random
        tumor_detected = random.choice([True, False])
        confidence = random.uniform(0.75, 0.95)
        
        # Create mock Grad-CAM (copy original image)
        gradcam_filename = os.path.basename(filepath).replace('.', '_gradcam.')
        gradcam_path = os.path.join('static', 'results', gradcam_filename)
        shutil.copy2(filepath, gradcam_path)
        
        # Copy original to static
        original_filename = os.path.basename(filepath)
        static_original_path = os.path.join('static', 'results', original_filename)
        shutil.copy2(filepath, static_original_path)
        
        # Generate demo report
        report = f"""
# COMPREHENSIVE BRAIN MRI ANALYSIS REPORT (DEMO MODE)

## ⚠️ IMPORTANT NOTICE
This is a DEMO analysis. The actual trained model is not loaded.
To use the real model, download it from Google Colab and place it in models/ folder.

## EXECUTIVE SUMMARY
Brain MRI scan has been analyzed using simulated AI classification.
Diagnosis: {'Tumor Detected' if tumor_detected else 'Normal'}
Confidence Level: {confidence:.1%}

## PATIENT INFORMATION
{f"Name: {patient_info.get('name', 'N/A')}" if patient_info else "No patient information provided"}
{f"Age: {patient_info.get('age', 'N/A')}" if patient_info else ""}
{f"Gender: {patient_info.get('gender', 'N/A')}" if patient_info else ""}
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## DIAGNOSTIC RESULTS
- **Classification**: {'TUMOR' if tumor_detected else 'NORMAL'}
- **Confidence Score**: {confidence:.1%}
- **Model**: VGG19 (Simulated)
- **Analysis Method**: Deep Learning Image Classification

## VISUAL ANALYSIS
Grad-CAM visualization has been generated (demo mode - showing original image).
In production mode, this would show heatmaps of brain regions influencing the decision.

## MEDICAL INTERPRETATION

{'### Tumor Detection' if tumor_detected else '### Normal Scan'}

{'''This analysis suggests the presence of abnormal tissue that may indicate a brain tumor.

**Common Symptoms to Monitor:**
- Persistent headaches
- Seizures or convulsions
- Vision problems
- Cognitive changes
- Balance and coordination issues

**Possible Risk Factors:**
- Previous radiation exposure
- Genetic predisposition
- Family history of brain tumors
- Age-related factors

**Recommended Treatment Approaches:**
1. **Surgical Resection**: Primary treatment for accessible tumors
2. **Radiation Therapy**: Adjuvant treatment to target remaining cells
3. **Chemotherapy**: For specific tumor types
4. **Targeted Therapy**: Emerging treatments for certain molecular profiles

''' if tumor_detected else '''
The scan appears normal with no obvious signs of tumor or abnormality detected.

**Recommendations for Maintaining Brain Health:**
- Regular health checkups
- Healthy lifestyle habits
- Monitor for any new symptoms
- Report persistent headaches or neurological changes

**When to Seek Medical Attention:**
- New or worsening headaches
- Vision changes
- Unexplained seizures
- Cognitive or memory issues
'''}

## NEXT STEPS

{'**IMMEDIATE ACTIONS REQUIRED:**' if tumor_detected else '**ROUTINE FOLLOW-UP:**'}

{'''1. Schedule urgent consultation with neurologist or neurosurgeon
2. Additional diagnostic tests (biopsy for tissue analysis)
3. MRI contrast study for detailed tumor characterization
4. Consultation with neuro-oncologist
5. Consider second opinion from specialized cancer center
6. Discuss treatment options with medical team
7. Begin treatment planning based on tumor type and location
''' if tumor_detected else '''
1. Continue regular health monitoring
2. Schedule routine follow-up appointments
3. Maintain healthy lifestyle
4. Report any new symptoms immediately
5. No immediate medical intervention required
'''}

## TECHNICAL DETAILS
- **Image Resolution**: Standard MRI resolution
- **Model Architecture**: VGG19 Transfer Learning
- **Training Dataset**: Brain MRI Images for Tumor Detection
- **Classification Threshold**: 0.5
- **Explainability Method**: Grad-CAM (Gradient-weighted Class Activation Mapping)

## IMPORTANT DISCLAIMERS

⚠️ **Medical Disclaimer**: This analysis is for educational and research purposes only. 
This is a DEMONSTRATION using simulated results. Always consult qualified healthcare 
professionals for actual medical diagnosis and treatment.

⚠️ **AI Limitations**: AI systems are diagnostic aids, not replacements for medical expertise.
All findings should be confirmed by licensed medical professionals with access to complete 
patient history and additional diagnostic information.

⚠️ **Not for Clinical Use**: This system has not been approved for clinical diagnosis.
Do not make medical decisions based solely on this analysis.

---

**Report Generated By**: Multi-Agent Brain Tumor Analysis System (Demo Mode)
**Timestamp**: {datetime.now().isoformat()}
**Session ID**: {session.get('session_id', 'demo-' + datetime.now().strftime('%Y%m%d%H%M%S'))}
"""
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'image_path': filepath,
            'patient_info': patient_info,
            'classification': {
                'class': 'Tumor' if tumor_detected else 'Normal',
                'confidence': confidence,
                'tumor_detected': tumor_detected,
                'raw_prediction': confidence if tumor_detected else 1 - confidence
            },
            'report': report,
            'gradcam_path': gradcam_path,
            'gradcam_url': f"/static/results/{gradcam_filename}",
            'image_url': f"/static/results/{original_filename}"
        }
        
        # Save report
        report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
        
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"Demo analysis completed")
        
        return jsonify({
            'success': True,
            'result': result,
            'report_path': report_path
        })
    
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy (demo mode)',
        'timestamp': datetime.now().isoformat(),
        'mode': 'DEMO - No model loaded'
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧪 DEMO MODE - Multi-Agent Brain Tumor Analysis")
    print("="*60)
    print("\n⚠️  Running in DEMO mode without the trained model")
    print("📥 To use the real model:")
    print("   1. Download from Google Colab using download_model_from_colab.py")
    print("   2. Place in models/ folder")
    print("   3. Run 'python app.py' instead\n")
    print("🌐 Starting Flask server at http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
