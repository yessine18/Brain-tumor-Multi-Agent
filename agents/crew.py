"""
Multi-Agent System for Brain Tumor Analysis
"""

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from typing import Dict
from datetime import datetime

from models.classifier import BrainTumorClassifier
from agents.knowledge_base import get_knowledge_base
from config import Config


class BrainTumorCrew:
    """
    Multi-agent system for brain tumor analysis
    
    Agent 1: Classification - Binary classification (Tumor vs Normal) with Grad-CAM visualization
    Agent 2: Explanation - Medical context from Neo4j knowledge graph + LLM analysis
    Agent 3: Report Generation - Comprehensive medical report synthesis
    """
    
    def __init__(self, config: Config):
        self.config = config
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=config.GROQ_API_KEY
        )
        
        # Initialize classifier and knowledge base
        self.classifier = BrainTumorClassifier(config.MODEL_PATH)
        self.classifier.load_model()
        
        self.kb = get_knowledge_base(
            config.NEO4J_URI,
            config.NEO4J_USERNAME,
            config.NEO4J_PASSWORD
        )
    
    def agent_classify(self, image_path: str) -> Dict:
        """Agent 1: Classification Agent - Binary tumor detection with Grad-CAM visualization"""
        # Run classification
        result = self.classifier.predict(image_path)
        
        # Generate Grad-CAM
        gradcam_path = image_path.replace('.', '_gradcam.')
        self.classifier.save_gradcam(image_path, gradcam_path)
        
        # Create classification report
        report = f"""
AGENT 1 - CLASSIFICATION REPORT
================================

MRI Image Analysis Complete

Diagnosis: {result['class']}
Confidence Level: {result['confidence']:.1%}
Tumor Detected: {'Yes' if result['tumor_detected'] else 'No'}
Raw Prediction Score: {result['raw_prediction']:.4f}

Explainability Analysis:
- Grad-CAM visualization has been generated
- Heatmap shows which brain regions influenced the classification decision
- Visualization saved to: {gradcam_path}

Model Information:
- Architecture: VGG19 Transfer Learning
- Training: Binary classification (Tumor vs Normal)
- Confidence Threshold: 0.5
"""
        
        return {
            'report': report,
            'classification': result,
            'gradcam_path': gradcam_path
        }
    
    def agent_explain(self, classification_result: Dict) -> Dict:
        """Agent 2: Explanation Agent - Queries Neo4j knowledge graph and generates medical insights"""
        # Query knowledge base
        kb_info = self.kb.query_tumor_information(classification_result['tumor_detected'])
        
        # Create prompt for LLM
        prompt = PromptTemplate(
            input_variables=["diagnosis", "confidence", "kb_info"],
            template="""You are a medical expert providing comprehensive analysis of brain MRI results.

Classification Results:
- Diagnosis: {diagnosis}
- Confidence: {confidence}

Medical Knowledge Base Information:
{kb_info}

Please provide a comprehensive medical explanation including:
1. What this diagnosis means in medical terms
2. Common symptoms and warning signs
3. Possible causes and risk factors
4. Available treatment options
5. Recommended next steps
6. Important medical considerations

Write in clear, professional medical language while being understandable."""
        )
        
        kb_str = str(kb_info)
        
        formatted_prompt = prompt.format(
            diagnosis=classification_result['class'],
            confidence=f"{classification_result['confidence']:.1%}",
            kb_info=kb_str
        )
        
        # Get LLM response
        explanation = self.llm.invoke(formatted_prompt).content
        
        report = f"""
AGENT 2 - MEDICAL EXPLANATION
==============================

{explanation}

Knowledge Base Statistics:
- Symptoms Identified: {len(kb_info.get('symptoms', []))}
- Risk Factors: {len(kb_info.get('causes', []))}
- Treatment Options: {len(kb_info.get('treatments', []))}
"""
        
        return {
            'report': report,
            'kb_info': kb_info,
            'explanation': explanation
        }
    
    def agent_report(self, classification_data: Dict, explanation_data: Dict, patient_info: Dict = None) -> str:
        """Agent 3: Report Generation Agent - Synthesizes comprehensive medical report"""
        # Create comprehensive report prompt
        prompt = PromptTemplate(
            input_variables=["patient_info", "classification", "explanation", "timestamp"],
            template="""You are a medical documentation specialist creating a comprehensive medical report.

Patient Information:
{patient_info}

Classification Results:
{classification}

Medical Analysis:
{explanation}

Report Timestamp: {timestamp}

Generate a complete, professionally formatted medical report with the following sections:

# COMPREHENSIVE BRAIN MRI ANALYSIS REPORT

## EXECUTIVE SUMMARY
[Brief overview of findings]

## PATIENT INFORMATION
[Patient details if provided]

## DIAGNOSTIC RESULTS
[Classification findings with confidence levels]

## VISUAL ANALYSIS
[Grad-CAM and explainability findings]

## MEDICAL INTERPRETATION
[Detailed medical explanation]

## TREATMENT RECOMMENDATIONS
[Recommended treatment options if tumor detected]

## NEXT STEPS
[Immediate and follow-up actions]

## IMPORTANT DISCLAIMERS
[Medical disclaimers and limitations]

Format the report professionally with clear sections and bullet points where appropriate."""
        )
        
        patient_str = "No patient information provided"
        if patient_info:
            patient_str = f"""
Name: {patient_info.get('name', 'N/A')}
Age: {patient_info.get('age', 'N/A')}
Gender: {patient_info.get('gender', 'N/A')}
"""
        
        formatted_prompt = prompt.format(
            patient_info=patient_str,
            classification=classification_data['report'],
            explanation=explanation_data['report'],
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # Get final report from LLM
        final_report = self.llm.invoke(formatted_prompt).content
        
        return final_report
    
    def analyze(self, image_path: str, patient_info: Dict = None) -> Dict:
        """
        Run the complete multi-agent analysis workflow
        
        Args:
            image_path: Path to the MRI image
            patient_info: Optional patient information
            
        Returns:
            Complete analysis results
        """
        print("\n" + "="*60)
        print("MULTI-AGENT BRAIN TUMOR ANALYSIS SYSTEM")
        print("="*60 + "\n")
        
        # Step 1: Classification Agent
        print("🤖 Agent 1: Running classification analysis...")
        classification_data = self.agent_classify(image_path)
        print("✓ Classification complete")
        
        # Step 2: Medical Explanation Agent
        print("\n🧑‍⚕️ Agent 2: Generating medical explanation...")
        explanation_data = self.agent_explain(classification_data['classification'])
        print("✓ Medical explanation complete")
        
        # Step 3: Report Generation Agent
        print("\n📋 Agent 3: Generating comprehensive report...")
        final_report = self.agent_report(classification_data, explanation_data, patient_info)
        print("✓ Report generation complete")
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60 + "\n")
        
        # Compile results
        return {
            'timestamp': datetime.now().isoformat(),
            'image_path': image_path,
            'patient_info': patient_info,
            'classification': classification_data['classification'],
            'report': final_report,
            'gradcam_path': classification_data['gradcam_path']
        }


def create_crew(config: Config = None) -> BrainTumorCrew:
    """Factory function to create a BrainTumorCrew instance"""
    if config is None:
        config = Config()
    return BrainTumorCrew(config)
