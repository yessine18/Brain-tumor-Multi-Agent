"""
Neo4j Knowledge Base for Brain Tumor Medical Information
"""

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class MedicalKnowledgeBase:
    """Neo4j-based medical knowledge base for brain tumors"""
    
    def __init__(self, uri: str, username: str, password: str):
        """
        Initialize Neo4j connection
        
        Args:
            uri: Neo4j database URI
            username: Database username
            password: Database password
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password), encrypted=False)
        import time
        last_err = None
        for attempt in range(5):
            try:
                self.driver.verify_connectivity()
                last_err = None
                break
            except Exception as e:
                last_err = e
                logger.warning(f"Neo4j connectivity attempt {attempt+1}/5 failed: {e}")
                time.sleep(2)
        if last_err:
            raise last_err
        
    def close(self):
        """Close the database connection"""
        self.driver.close()
    
    def initialize_knowledge_base(self):
        """Initialize the knowledge base with medical information about brain tumors"""
        with self.driver.session() as session:
            # Clear existing data (optional - for fresh start)
            session.run("MATCH (n) DETACH DELETE n")
            
            # Create brain tumor types
            session.run("""
                CREATE (glioma:TumorType {
                    name: 'Glioma',
                    description: 'Tumors that arise from glial cells in the brain',
                    prevalence: 'Most common primary brain tumor in adults'
                })
                CREATE (meningioma:TumorType {
                    name: 'Meningioma',
                    description: 'Tumors that develop from the meninges',
                    prevalence: 'Most common benign brain tumor'
                })
                CREATE (pituitary:TumorType {
                    name: 'Pituitary Adenoma',
                    description: 'Tumors of the pituitary gland',
                    prevalence: 'Common, usually benign'
                })
            """)
            
            # Create symptoms
            session.run("""
                CREATE (headache:Symptom {name: 'Persistent Headaches', severity: 'High'})
                CREATE (seizures:Symptom {name: 'Seizures', severity: 'High'})
                CREATE (vision:Symptom {name: 'Vision Problems', severity: 'Medium'})
                CREATE (nausea:Symptom {name: 'Nausea and Vomiting', severity: 'Medium'})
                CREATE (weakness:Symptom {name: 'Muscle Weakness', severity: 'High'})
                CREATE (cognitive:Symptom {name: 'Cognitive Changes', severity: 'Medium'})
                CREATE (balance:Symptom {name: 'Balance Problems', severity: 'Medium'})
            """)
            
            # Create causes/risk factors
            session.run("""
                CREATE (radiation:Cause {name: 'Previous Radiation Exposure', type: 'Environmental'})
                CREATE (genetic:Cause {name: 'Genetic Mutations', type: 'Genetic'})
                CREATE (family:Cause {name: 'Family History', type: 'Genetic'})
                CREATE (age:Cause {name: 'Age (Risk increases with age)', type: 'Demographic'})
                CREATE (immune:Cause {name: 'Weakened Immune System', type: 'Medical'})
            """)
            
            # Create treatments
            session.run("""
                CREATE (surgery:Treatment {
                    name: 'Surgical Resection',
                    description: 'Removal of tumor through surgery',
                    effectiveness: 'High for accessible tumors'
                })
                CREATE (radio:Treatment {
                    name: 'Radiation Therapy',
                    description: 'Use of high-energy radiation to kill tumor cells',
                    effectiveness: 'High when combined with other treatments'
                })
                CREATE (chemo:Treatment {
                    name: 'Chemotherapy',
                    description: 'Drug-based treatment to kill cancer cells',
                    effectiveness: 'Variable depending on tumor type'
                })
                CREATE (targeted:Treatment {
                    name: 'Targeted Therapy',
                    description: 'Drugs targeting specific molecular changes in tumor cells',
                    effectiveness: 'Growing effectiveness for specific tumor types'
                })
            """)
            
            # Create diagnostic methods
            session.run("""
                CREATE (mri:Diagnostic {
                    name: 'MRI Scan',
                    description: 'Magnetic Resonance Imaging for detailed brain images',
                    accuracy: 'Very High'
                })
                CREATE (ct:Diagnostic {
                    name: 'CT Scan',
                    description: 'Computed Tomography for brain imaging',
                    accuracy: 'High'
                })
                CREATE (biopsy:Diagnostic {
                    name: 'Biopsy',
                    description: 'Tissue sample analysis for definitive diagnosis',
                    accuracy: 'Gold Standard'
                })
            """)
            
            # Create relationships between tumor types and symptoms
            session.run("""
                MATCH (g:TumorType {name: 'Glioma'})
                MATCH (headache:Symptom {name: 'Persistent Headaches'})
                MATCH (seizures:Symptom {name: 'Seizures'})
                MATCH (cognitive:Symptom {name: 'Cognitive Changes'})
                MATCH (weakness:Symptom {name: 'Muscle Weakness'})
                CREATE (g)-[:CAUSES_SYMPTOM {frequency: 'Common'}]->(headache)
                CREATE (g)-[:CAUSES_SYMPTOM {frequency: 'Common'}]->(seizures)
                CREATE (g)-[:CAUSES_SYMPTOM {frequency: 'Frequent'}]->(cognitive)
                CREATE (g)-[:CAUSES_SYMPTOM {frequency: 'Common'}]->(weakness)
            """)
            
            # Create relationships with causes
            session.run("""
                MATCH (g:TumorType {name: 'Glioma'})
                MATCH (radiation:Cause {name: 'Previous Radiation Exposure'})
                MATCH (genetic:Cause {name: 'Genetic Mutations'})
                MATCH (family:Cause {name: 'Family History'})
                CREATE (radiation)-[:INCREASES_RISK_OF {risk_factor: 'Moderate'}]->(g)
                CREATE (genetic)-[:INCREASES_RISK_OF {risk_factor: 'High'}]->(g)
                CREATE (family)-[:INCREASES_RISK_OF {risk_factor: 'Moderate'}]->(g)
            """)
            
            # Create relationships with treatments
            session.run("""
                MATCH (g:TumorType {name: 'Glioma'})
                MATCH (surgery:Treatment {name: 'Surgical Resection'})
                MATCH (radio:Treatment {name: 'Radiation Therapy'})
                MATCH (chemo:Treatment {name: 'Chemotherapy'})
                MATCH (targeted:Treatment {name: 'Targeted Therapy'})
                CREATE (g)-[:TREATED_WITH {priority: 'Primary'}]->(surgery)
                CREATE (g)-[:TREATED_WITH {priority: 'Adjuvant'}]->(radio)
                CREATE (g)-[:TREATED_WITH {priority: 'Adjuvant'}]->(chemo)
                CREATE (g)-[:TREATED_WITH {priority: 'Emerging'}]->(targeted)
            """)
            
            # Create relationships with diagnostics
            session.run("""
                MATCH (g:TumorType {name: 'Glioma'})
                MATCH (mri:Diagnostic {name: 'MRI Scan'})
                MATCH (ct:Diagnostic {name: 'CT Scan'})
                MATCH (biopsy:Diagnostic {name: 'Biopsy'})
                CREATE (mri)-[:DIAGNOSES {accuracy: 'Primary method'}]->(g)
                CREATE (ct)-[:DIAGNOSES {accuracy: 'Secondary method'}]->(g)
                CREATE (biopsy)-[:DIAGNOSES {accuracy: 'Confirmatory'}]->(g)
            """)
            
            logger.info("Knowledge base initialized successfully")
    
    def query_tumor_information(self, tumor_detected: bool) -> Dict:
        """
        Query comprehensive information about brain tumors
        
        Args:
            tumor_detected: Whether a tumor was detected
            
        Returns:
            Dictionary containing medical information
        """
        if not tumor_detected:
            return {
                'status': 'Normal',
                'message': 'No tumor detected. Brain scan appears normal.',
                'recommendations': [
                    'Continue regular health checkups',
                    'Maintain healthy lifestyle',
                    'Monitor for any new symptoms'
                ]
            }
        
        with self.driver.session() as session:
            # Query symptoms
            symptoms_result = session.run("""
                MATCH (t:TumorType)-[r:CAUSES_SYMPTOM]->(s:Symptom)
                RETURN s.name as symptom, s.severity as severity, r.frequency as frequency
            """)
            symptoms = [dict(record) for record in symptoms_result]
            
            # Query causes
            causes_result = session.run("""
                MATCH (c:Cause)-[r:INCREASES_RISK_OF]->(t:TumorType)
                RETURN c.name as cause, c.type as type, r.risk_factor as risk
            """)
            causes = [dict(record) for record in causes_result]
            
            # Query treatments
            treatments_result = session.run("""
                MATCH (t:TumorType)-[r:TREATED_WITH]->(tr:Treatment)
                RETURN tr.name as treatment, tr.description as description, 
                       tr.effectiveness as effectiveness, r.priority as priority
                ORDER BY 
                    CASE r.priority 
                        WHEN 'Primary' THEN 1 
                        WHEN 'Adjuvant' THEN 2 
                        ELSE 3 
                    END
            """)
            treatments = [dict(record) for record in treatments_result]
            
            # Query diagnostics
            diagnostics_result = session.run("""
                MATCH (d:Diagnostic)-[r:DIAGNOSES]->(t:TumorType)
                RETURN d.name as method, d.description as description, d.accuracy as accuracy
            """)
            diagnostics = [dict(record) for record in diagnostics_result]
            
            return {
                'status': 'Tumor Detected',
                'symptoms': symptoms,
                'causes': causes,
                'treatments': treatments,
                'diagnostics': diagnostics,
                'recommendations': [
                    'Immediate consultation with a neurologist or neurosurgeon',
                    'Additional diagnostic tests (biopsy) for tumor characterization',
                    'Discussion of treatment options based on tumor type and location',
                    'Consider second opinion from specialized cancer center'
                ]
            }
    
    def get_symptoms_by_severity(self, severity: str) -> List[str]:
        """Get symptoms filtered by severity"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Symptom {severity: $severity})
                RETURN s.name as symptom
            """, severity=severity)
            return [record['symptom'] for record in result]
    
    def get_treatment_recommendations(self) -> List[Dict]:
        """Get all treatment recommendations"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (t:TumorType)-[r:TREATED_WITH]->(tr:Treatment)
                RETURN t.name as tumor_type, tr.name as treatment, 
                       tr.description as description, r.priority as priority
            """)
            return [dict(record) for record in result]


# Singleton instance
_kb_instance = None

def get_knowledge_base(uri: str, username: str, password: str) -> MedicalKnowledgeBase:
    """Get or create knowledge base instance"""
    global _kb_instance
    if _kb_instance is None:
        _kb_instance = MedicalKnowledgeBase(uri, username, password)
    return _kb_instance
