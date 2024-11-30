from typing import Dict, Any, List
from app.utils.vector_store_manager import VectorStoreManager
from app.utils.human_loop_manager import HumanLoopManager
from app.crews.mechanic_crew import MechanicCrew
import streamlit as st
import uuid
from datetime import datetime
from pathlib import Path
import json

class InspectionFlow:
    """Flow d'inspection avec analyse d'image et validation humaine"""
    
    def __init__(self):
        self.vector_store = VectorStoreManager()
        self.human_loop = HumanLoopManager()
        self.crew = MechanicCrew()
        
        # Chargement de la base de connaissances
        self.vector_store.load_vector_store("inspection_kb")
        
        # Création du dossier pour les rapports
        self.reports_path = Path("data/inspection_reports")
        self.reports_path.mkdir(parents=True, exist_ok=True)
    
    def process_inspection(
        self,
        vehicle_data: Dict[str, Any],
        images: List[Any],
        checklist: Dict[str, bool]
    ) -> Dict[str, Any]:
        """Traite une inspection complète"""
        
        # Génération de l'ID unique pour cette inspection
        inspection_id = str(uuid.uuid4())
        
        # 1. Analyse des images par l'équipe d'agents
        image_analysis = self.crew.analyze_images(images)
        
        # 2. Recherche de cas similaires
        query = f"""
        Véhicule: {vehicle_data['make']} {vehicle_data['model']} {vehicle_data['year']}
        État: {image_analysis['condition_summary']}
        Problèmes détectés: {', '.join(image_analysis['detected_issues'])}
        """
        
        similar_cases = self.vector_store.similarity_search(query)
        
        # 3. Génération du rapport d'inspection
        inspection_result = self.crew.generate_inspection_report(
            vehicle_data=vehicle_data,
            image_analysis=image_analysis,
            checklist=checklist,
            similar_cases=similar_cases
        )
        
        # 4. Validation humaine si nécessaire
        if self.human_loop.require_validation(inspection_result["confidence_score"]):
            validated_result = self.human_loop.request_human_validation(
                task_id=inspection_id,
                task_type="inspection",
                data=inspection_result
            )
            
            if validated_result:
                inspection_result = validated_result
                # Mise à jour de la base de connaissances
                self._update_knowledge_base(inspection_result)
        
        # 5. Sauvegarde du rapport
        self._save_inspection_report(inspection_id, inspection_result)
        
        return inspection_result
    
    def _update_knowledge_base(self, inspection_data: Dict[str, Any]):
        """Met à jour la base de connaissances avec une nouvelle inspection"""
        
        knowledge_text = f"""
        Inspection ID: {inspection_data['inspection_id']}
        Véhicule: {inspection_data['vehicle_data']['make']} {inspection_data['vehicle_data']['model']} {inspection_data['vehicle_data']['year']}
        État général: {inspection_data['general_condition']}
        Points critiques: {', '.join(inspection_data['critical_points'])}
        Recommandations: {inspection_data['recommendations']}
        """
        
        self.vector_store.add_texts(
            [knowledge_text],
            [{"inspection_id": inspection_data['inspection_id']}]
        )
        
        self.vector_store.save_vector_store("inspection_kb")
    
    def _save_inspection_report(self, inspection_id: str, report_data: Dict[str, Any]):
        """Sauvegarde le rapport d'inspection"""
        report_file = self.reports_path / f"{inspection_id}.json"
        
        try:
            with open(report_file, "w") as f:
                json.dump(report_data, f, indent=4)
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde du rapport: {str(e)}")
    
    def show_inspection_interface(self):
        """Affiche l'interface d'inspection"""
        st.title("🔎 Inspection Détaillée")
        
        # Formulaire d'inspection
        with st.form("inspection_form"):
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
            
            # Upload d'images
            st.subheader("Photos du Véhicule")
            uploaded_images = st.file_uploader(
                "Téléchargez les photos",
                accept_multiple_files=True,
                type=['png', 'jpg', 'jpeg']
            )
            
            # Checklist d'inspection
            st.subheader("Checklist d'Inspection")
            
            checklist = {}
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Extérieur**")
                checklist["carrosserie"] = st.checkbox("Carrosserie")
                checklist["pneus"] = st.checkbox("Pneus")
                checklist["vitres"] = st.checkbox("Vitres")
                checklist["phares"] = st.checkbox("Phares")
            
            with col2:
                st.write("**Mécanique**")
                checklist["moteur"] = st.checkbox("Moteur")
                checklist["freins"] = st.checkbox("Freins")
                checklist["suspension"] = st.checkbox("Suspension")
                checklist["transmission"] = st.checkbox("Transmission")
            
            # Notes supplémentaires
            notes = st.text_area("Notes supplémentaires")
            
            # Bouton de soumission
            submitted = st.form_submit_button("Lancer l'Inspection")
        
        if submitted and make and model and uploaded_images:
            with st.spinner("Inspection en cours..."):
                # Préparation des données du véhicule
                vehicle_data = {
                    "make": make,
                    "model": model,
                    "year": year,
                    "mileage": mileage,
                    "vin": vin,
                    "notes": notes
                }
                
                # Lancement de l'inspection
                result = self.process_inspection(
                    vehicle_data=vehicle_data,
                    images=uploaded_images,
                    checklist=checklist
                )
                
                # Affichage des résultats
                if result:
                    st.success("Inspection complétée avec succès!")
                    
                    st.write("### Résultats de l'Inspection")
                    st.write(f"**ID de l'Inspection:** {result['inspection_id']}")
                    st.write(f"**État Général:** {result['general_condition']}")
                    
                    # Points critiques
                    st.write("**Points Critiques:**")
                    for point in result['critical_points']:
                        st.write(f"- {point}")
                    
                    # Recommandations
                    st.write("**Recommandations:**")
                    st.write(result['recommendations'])
                    
                    # Analyse des images
                    if "image_analysis" in result:
                        st.write("### Analyse des Images")
                        for i, analysis in enumerate(result["image_analysis"]):
                            with st.expander(f"Image {i+1}"):
                                st.write(f"**Détails:** {analysis['details']}")
                                st.write(f"**Problèmes détectés:** {', '.join(analysis['issues'])}")
                    
                    # Export du rapport
                    if st.button("📄 Télécharger le Rapport"):
                        from app.utils.export_manager import ExportManager
                        
                        report_pdf = ExportManager.to_pdf(result)
                        st.download_button(
                            "Télécharger PDF",
                            report_pdf,
                            f"inspection_{result['inspection_id']}.pdf",
                            "application/pdf"
                        )
