"""
Flask Web Application for Brain Tumor Analysis
Multi-Agent System
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, session
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import logging

from config import Config
from agents.crew import create_crew
from agents.knowledge_base import get_knowledge_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)
os.makedirs('static/results', exist_ok=True)

crew = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_crew():
    """Lazy load the crew instance"""
    global crew
    if crew is None:
        logger.info("Initializing multi-agent system...")
        crew = create_crew()
        logger.info("Crew initialized successfully")
    return crew


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and initiate analysis"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the file
            file.save(filepath)
            logger.info(f"File uploaded: {filepath}")
            
            # Get optional patient info
            patient_info = None
            if request.form.get('patient_name') or request.form.get('patient_age'):
                patient_info = {
                    'name': request.form.get('patient_name', 'N/A'),
                    'age': request.form.get('patient_age', 'N/A'),
                    'gender': request.form.get('patient_gender', 'N/A')
                }
            
            # Store in session for analysis
            session['current_image'] = filepath
            session['patient_info'] = patient_info
            
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath
            })
        
        return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or JPEG'}), 400
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/analyze', methods=['POST'])
def analyze():
    """Run the multi-agent analysis"""
    try:
        filepath = session.get('current_image')
        patient_info = session.get('patient_info')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'No image file found. Please upload an image first.'}), 400
        
        logger.info(f"Starting analysis for: {filepath}")
        
        # Get the crew and run analysis
        analysis_crew = get_crew()
        result = analysis_crew.analyze(filepath, patient_info)
        
        # Save the report
        report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = os.path.join(app.config['REPORTS_FOLDER'], report_filename)
        
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        logger.info(f"Analysis completed. Report saved to: {report_path}")
        
        # Move gradcam to static folder for web access
        if os.path.exists(result['gradcam_path']):
            gradcam_filename = os.path.basename(result['gradcam_path'])
            static_gradcam_path = os.path.join('static', 'results', gradcam_filename)
            os.makedirs(os.path.dirname(static_gradcam_path), exist_ok=True)
            
            # Copy file
            import shutil
            shutil.copy2(result['gradcam_path'], static_gradcam_path)
            result['gradcam_url'] = f"/static/results/{gradcam_filename}"
        
        # Move original image to static folder
        original_filename = os.path.basename(filepath)
        static_original_path = os.path.join('static', 'results', original_filename)
        import shutil
        shutil.copy2(filepath, static_original_path)
        result['image_url'] = f"/static/results/{original_filename}"
        
        return jsonify({
            'success': True,
            'result': result,
            'report_path': report_path
        })
    
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/reports/<filename>')
def download_report(filename):
    """Download a specific report"""
    return send_from_directory(app.config['REPORTS_FOLDER'], filename, as_attachment=True)


@app.route('/init-knowledge-base', methods=['GET', 'POST'])
def init_knowledge_base():
    """Initialize the Neo4j knowledge base (admin function)"""
    try:
        kb = get_knowledge_base(
            app.config['NEO4J_URI'],
            app.config['NEO4J_USERNAME'],
            app.config['NEO4J_PASSWORD']
        )
        kb.initialize_knowledge_base()
        return jsonify({'success': True, 'message': 'Knowledge base initialized successfully'})
    except Exception as e:
        logger.error(f"Knowledge base initialization error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


if __name__ == '__main__':
    # Check if model exists
    if not os.path.exists(app.config['MODEL_PATH']):
        logger.warning(f"Model not found at {app.config['MODEL_PATH']}")
        logger.warning("Please copy your trained model (best_modelVGG19_brain_tumor.keras) to the models/ directory")
    
    # Run the app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
