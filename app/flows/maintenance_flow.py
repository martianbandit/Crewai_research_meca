from typing import Dict, Any, List
from app.utils.vector_store_manager import VectorStoreManager
from app.utils.human_loop_manager import HumanLoopManager
from app.crews.mechanic_crew import MechanicCrew
import streamlit as st
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import json

class MaintenanceFlow:
    """Flow de maintenance avec planification intelligente"""
    
    def __init__(self):
        self.vector_store = VectorStoreManager()
        self.human_loop = HumanLoopManager()
        self.crew = MechanicCrew()
        
        # Chargement de la base de connaissances
        self.vector_store.load_vector_store("maintenance_kb")
        
        # Création du dossier pour les plans de maintenance
        self.plans_path = Path("data/maintenance_plans")
        self.plans_path.mkdir(parents=True, exist_ok=True)
    
    def process_maintenance_plan(
        self,
        vehicle_data: Dict[str, Any],
        maintenance_history: List[Dict[str, Any]],
        current_issues: List[str]
    ) -> Dict[str, Any]:
        """Génère un plan de maintenance complet"""
        
        # Génération de l'ID unique pour ce plan
        plan_id = str(uuid.uuid4())
        
        # 1. Recherche de cas similaires
        query = f"""
        Véhicule: {vehicle_data['make']} {vehicle_data['model']} {vehicle_data['year']}
        Kilométrage: {vehicle_data['mileage']}
        Problèmes actuels: {', '.join(current_issues)}
        """
        
        similar_cases = self.vector_store.similarity_search(query)
        
        # 2. Génération du plan par l'équipe d'agents
        maintenance_plan = self.crew.generate_maintenance_plan(
            vehicle_data=vehicle_data,
            maintenance_history=maintenance_history,
            current_issues=current_issues,
            similar_cases=similar_cases
        )
        
        # 3. Validation humaine si nécessaire
        if self.human_loop.require_validation(maintenance_plan["confidence_score"]):
            validated_plan = self.human_loop.request_human_validation(
                task_id=plan_id,
                task_type="maintenance",
                data=maintenance_plan
            )
            
            if validated_plan:
                maintenance_plan = validated_plan
                # Mise à jour de la base de connaissances
                self._update_knowledge_base(maintenance_plan)
        
        # 4. Sauvegarde du plan
        self._save_maintenance_plan(plan_id, maintenance_plan)
        
        return maintenance_plan
    
    def _update_knowledge_base(self, plan_data: Dict[str, Any]):
        """Met à jour la base de connaissances avec un nouveau plan"""
        
        knowledge_text = f"""
        Plan ID: {plan_data['plan_id']}
        Véhicule: {plan_data['vehicle_data']['make']} {plan_data['vehicle_data']['model']} {plan_data['vehicle_data']['year']}
        Kilométrage: {plan_data['vehicle_data']['mileage']}
        Tâches: {', '.join(plan_data['tasks'])}
        Priorités: {', '.join(f"{task}: {details['priority']}" for task, details in plan_data['task_details'].items())}
        Estimation totale: {plan_data['total_estimated_time']} heures
        """
        
        self.vector_store.add_texts(
            [knowledge_text],
            [{"plan_id": plan_data['plan_id']}]
        )
        
        self.vector_store.save_vector_store("maintenance_kb")
    
    def _save_maintenance_plan(self, plan_id: str, plan_data: Dict[str, Any]):
        """Sauvegarde le plan de maintenance"""
        plan_file = self.plans_path / f"{plan_id}.json"
        
        try:
            with open(plan_file, "w") as f:
                json.dump(plan_data, f, indent=4)
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde du plan: {str(e)}")
    
    def show_maintenance_interface(self):
        """Affiche l'interface de planification de maintenance"""
        st.title("🔧 Planification de Maintenance")
        
        # Formulaire de maintenance
        with st.form("maintenance_form"):
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
            
            # Problèmes actuels
            st.subheader("Problèmes Actuels")
            issues = st.text_area(
                "Décrivez les problèmes actuels",
                help="Entrez chaque problème sur une nouvelle ligne"
            ).split("\n")
            
            # Historique de maintenance
            st.subheader("Historique de Maintenance")
            maintenance_history = []
            
            num_entries = st.number_input(
                "Nombre d'entrées d'historique",
                min_value=0,
                max_value=10,
                value=1
            )
            
            for i in range(num_entries):
                with st.expander(f"Entrée {i+1}"):
                    date = st.date_input(
                        "Date",
                        value=datetime.now() - timedelta(days=30*i),
                        key=f"date_{i}"
                    )
                    
                    work_done = st.text_area(
                        "Travaux effectués",
                        key=f"work_{i}"
                    )
                    
                    cost = st.number_input(
                        "Coût",
                        min_value=0.0,
                        key=f"cost_{i}"
                    )
                    
                    maintenance_history.append({
                        "date": date.isoformat(),
                        "work_done": work_done,
                        "cost": cost
                    })
            
            # Bouton de soumission
            submitted = st.form_submit_button("Générer le Plan")
        
        if submitted and make and model:
            with st.spinner("Génération du plan en cours..."):
                # Préparation des données du véhicule
                vehicle_data = {
                    "make": make,
                    "model": model,
                    "year": year,
                    "mileage": mileage,
                    "vin": vin
                }
                
                # Nettoyage des données
                issues = [i.strip() for i in issues if i.strip()]
                
                # Génération du plan
                result = self.process_maintenance_plan(
                    vehicle_data=vehicle_data,
                    maintenance_history=maintenance_history,
                    current_issues=issues
                )
                
                # Affichage des résultats
                if result:
                    st.success("Plan de maintenance généré avec succès!")
                    
                    st.write("### Plan de Maintenance")
                    st.write(f"**ID du Plan:** {result['plan_id']}")
                    
                    # Tâches planifiées
                    st.write("**Tâches Planifiées:**")
                    for task, details in result['task_details'].items():
                        with st.expander(task):
                            st.write(f"**Priorité:** {details['priority']}")
                            st.write(f"**Temps estimé:** {details['estimated_time']} heures")
                            st.write(f"**Notes:** {details['notes']}")
                    
                    # Résumé
                    st.write("### Résumé")
                    st.write(f"**Temps total estimé:** {result['total_estimated_time']} heures")
                    st.write(f"**Coût estimé:** {result['estimated_cost']} €")
                    
                    # Recommandations
                    st.write("**Recommandations:**")
                    st.write(result['recommendations'])
                    
                    # Export du plan
                    if st.button("📄 Télécharger le Plan"):
                        from app.utils.export_manager import ExportManager
                        
                        plan_pdf = ExportManager.to_pdf(result)
                        st.download_button(
                            "Télécharger PDF",
                            plan_pdf,
                            f"maintenance_plan_{result['plan_id']}.pdf",
                            "application/pdf"
                        )
