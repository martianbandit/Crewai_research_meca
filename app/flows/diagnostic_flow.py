from typing import Dict, Any, List
from app.utils.vector_store_manager import VectorStoreManager
from app.utils.human_loop_manager import HumanLoopManager
from app.crews.mechanic_crew import MechanicCrew
import streamlit as st
import uuid
from datetime import datetime

class DiagnosticFlow:
    """Flow de diagnostic avec RAG et validation humaine"""
    
    def __init__(self):
        self.vector_store = VectorStoreManager()
        self.human_loop = HumanLoopManager()
        self.crew = MechanicCrew()
        
        # Chargement de la base de connaissances
        self.vector_store.load_vector_store("diagnostic_kb")
    
    def process_diagnostic(
        self,
        vehicle_data: Dict[str, Any],
        symptoms: List[str],
        dtc_codes: List[str]
    ) -> Dict[str, Any]:
        """Traite un diagnostic complet"""
        
        # Génération de l'ID unique pour ce diagnostic
        diagnostic_id = str(uuid.uuid4())
        
        # 1. Recherche de cas similaires dans la base de connaissances
        query = f"""
        Véhicule: {vehicle_data['make']} {vehicle_data['model']} {vehicle_data['year']}
        Symptômes: {', '.join(symptoms)}
        Codes DTC: {', '.join(dtc_codes)}
        """
        
        similar_cases = self.vector_store.similarity_search(query)
        
        # 2. Analyse par l'équipe d'agents
        diagnostic_result = self.crew.analyze_diagnostic(
            vehicle_data=vehicle_data,
            symptoms=symptoms,
            dtc_codes=dtc_codes,
            similar_cases=similar_cases
        )
        
        # 3. Vérification du niveau de confiance
        if self.human_loop.require_validation(diagnostic_result["confidence_score"]):
            # Demande de validation humaine
            validated_result = self.human_loop.request_human_validation(
                task_id=diagnostic_id,
                task_type="diagnostic",
                data=diagnostic_result
            )
            
            if validated_result:
                diagnostic_result = validated_result
                # Ajout à la base de connaissances
                self._update_knowledge_base(diagnostic_result)
        
        # 4. Enrichissement du résultat
        diagnostic_result.update({
            "diagnostic_id": diagnostic_id,
            "timestamp": datetime.now().isoformat(),
            "vehicle_data": vehicle_data,
            "symptoms": symptoms,
            "dtc_codes": dtc_codes
        })
        
        return diagnostic_result
    
    def _update_knowledge_base(self, diagnostic_data: Dict[str, Any]):
        """Met à jour la base de connaissances avec un nouveau cas"""
        
        # Préparation du texte pour la base de connaissances
        knowledge_text = f"""
        Diagnostic ID: {diagnostic_data['diagnostic_id']}
        Véhicule: {diagnostic_data['vehicle_data']['make']} {diagnostic_data['vehicle_data']['model']} {diagnostic_data['vehicle_data']['year']}
        Symptômes: {', '.join(diagnostic_data['symptoms'])}
        Codes DTC: {', '.join(diagnostic_data['dtc_codes'])}
        Diagnostic: {diagnostic_data['diagnostic']}
        Gravité: {diagnostic_data['severity']}
        Recommandations: {diagnostic_data['recommendations']}
        """
        
        # Ajout à la base vectorielle
        self.vector_store.add_texts(
            [knowledge_text],
            [{"diagnostic_id": diagnostic_data['diagnostic_id']}]
        )
        
        # Sauvegarde de la base
        self.vector_store.save_vector_store("diagnostic_kb")
    
    def show_diagnostic_interface(self):
        """Affiche l'interface de diagnostic"""
        st.title("🔍 Diagnostic Intelligent")
        
        # Formulaire de diagnostic
        with st.form("diagnostic_form"):
            # Informations du véhicule
            st.subheader("Information du Véhicule")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                make = st.text_input("Marque")
                year = st.number_input("Année", min_value=1900, max_value=2024)
            
            with col2:
                model = st.text_input("Modèle")
                mileage = st.number_input("Kilométrage", min_value=0)
            
            with col3:
                vin = st.text_input("Numéro VIN")
            
            # Symptômes
            st.subheader("Symptômes")
            symptoms = st.text_area(
                "Décrivez les symptômes",
                help="Entrez chaque symptôme sur une nouvelle ligne"
            ).split("\n")
            
            # Codes DTC
            st.subheader("Codes DTC")
            dtc_codes = st.text_input(
                "Codes d'erreur",
                help="Entrez les codes séparés par des virgules"
            ).split(",")
            
            # Bouton de soumission
            submitted = st.form_submit_button("Lancer le Diagnostic")
        
        if submitted and make and model and symptoms:
            with st.spinner("Analyse en cours..."):
                # Préparation des données du véhicule
                vehicle_data = {
                    "make": make,
                    "model": model,
                    "year": year,
                    "mileage": mileage,
                    "vin": vin
                }
                
                # Nettoyage des données
                symptoms = [s.strip() for s in symptoms if s.strip()]
                dtc_codes = [c.strip() for c in dtc_codes if c.strip()]
                
                # Lancement du diagnostic
                result = self.process_diagnostic(
                    vehicle_data=vehicle_data,
                    symptoms=symptoms,
                    dtc_codes=dtc_codes
                )
                
                # Affichage des résultats
                if result:
                    st.success("Diagnostic complété avec succès!")
                    
                    st.write("### Résultats du Diagnostic")
                    st.write(f"**ID du Diagnostic:** {result['diagnostic_id']}")
                    st.write(f"**Diagnostic:** {result['diagnostic']}")
                    st.write(f"**Niveau de Gravité:** {result['severity']}")
                    st.write("**Recommandations:**")
                    st.write(result['recommendations'])
                    
                    # Cas similaires
                    if "similar_cases" in result:
                        st.write("### Cas Similaires")
                        for case in result["similar_cases"][:3]:
                            with st.expander(f"Cas {case['diagnostic_id']}"):
                                st.write(case['content'])
