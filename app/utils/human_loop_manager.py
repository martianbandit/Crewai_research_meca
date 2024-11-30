import streamlit as st
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import json
from pathlib import Path
import time

class HumanLoopManager:
    """Gestionnaire pour l'interaction humaine dans la boucle"""
    
    def __init__(self):
        self.feedback_path = Path("data/human_feedback")
        self.feedback_path.mkdir(parents=True, exist_ok=True)
        
        if 'human_feedback' not in st.session_state:
            st.session_state.human_feedback = {}
    
    def request_human_validation(
        self,
        task_id: str,
        task_type: str,
        data: Dict[str, Any],
        validation_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Demande une validation humaine pour une tâche"""
        
        st.subheader("🔍 Validation Humaine Requise")
        
        # Affichage des données à valider
        st.write("Veuillez vérifier et valider les informations suivantes :")
        
        validated_data = data.copy()
        
        # Interface de validation selon le type de tâche
        if task_type == "diagnostic":
            st.write("### Diagnostic Proposé")
            for key, value in data.items():
                if key == "severity":
                    validated_data[key] = st.select_slider(
                        "Niveau de Gravité",
                        options=["Faible", "Moyen", "Élevé", "Critique"],
                        value=value
                    )
                elif key == "recommendations":
                    validated_data[key] = st.text_area(
                        "Recommandations",
                        value=value,
                        height=150
                    )
                else:
                    validated_data[key] = st.text_input(key.capitalize(), value=value)
        
        elif task_type == "inspection":
            st.write("### Résultats d'Inspection")
            for component, status in data.items():
                validated_data[component] = st.selectbox(
                    f"État de {component}",
                    options=["Bon", "Moyen", "Mauvais", "Critique"],
                    index=["Bon", "Moyen", "Mauvais", "Critique"].index(status)
                )
        
        elif task_type == "maintenance":
            st.write("### Plan de Maintenance")
            for task, details in data.items():
                st.write(f"#### {task}")
                validated_data[task] = {
                    "priority": st.selectbox(
                        "Priorité",
                        options=["Basse", "Moyenne", "Haute", "Urgente"],
                        index=["Basse", "Moyenne", "Haute", "Urgente"].index(details["priority"]),
                        key=f"priority_{task}"
                    ),
                    "estimated_time": st.number_input(
                        "Temps Estimé (heures)",
                        min_value=0.5,
                        value=float(details["estimated_time"]),
                        step=0.5,
                        key=f"time_{task}"
                    ),
                    "notes": st.text_area(
                        "Notes",
                        value=details["notes"],
                        key=f"notes_{task}"
                    )
                }
        
        # Commentaires généraux
        feedback = st.text_area(
            "Commentaires additionnels",
            help="Ajoutez des commentaires ou des observations supplémentaires"
        )
        
        # Boutons de validation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Valider", type="primary"):
                self._save_feedback(task_id, validated_data, feedback, "validated")
                if validation_callback:
                    validation_callback(validated_data)
                return validated_data
        
        with col2:
            if st.button("❌ Rejeter"):
                self._save_feedback(task_id, validated_data, feedback, "rejected")
                return None
        
        # Par défaut, retourne None si aucune action n'est prise
        return None
    
    def _save_feedback(
        self,
        task_id: str,
        data: Dict[str, Any],
        feedback: str,
        status: str
    ):
        """Sauvegarde le feedback humain"""
        feedback_data = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "feedback": feedback,
            "status": status
        }
        
        # Sauvegarde en session
        st.session_state.human_feedback[task_id] = feedback_data
        
        # Sauvegarde dans un fichier
        feedback_file = self.feedback_path / f"{task_id}.json"
        try:
            with open(feedback_file, "w") as f:
                json.dump(feedback_data, f, indent=4)
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde du feedback: {str(e)}")
    
    def get_feedback_history(self, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Récupère l'historique des feedbacks"""
        if task_id:
            feedback_file = self.feedback_path / f"{task_id}.json"
            if feedback_file.exists():
                try:
                    with open(feedback_file, "r") as f:
                        return json.load(f)
                except Exception as e:
                    st.error(f"Erreur lors de la lecture du feedback: {str(e)}")
                    return {}
        else:
            feedback_history = {}
            for feedback_file in self.feedback_path.glob("*.json"):
                try:
                    with open(feedback_file, "r") as f:
                        feedback_data = json.load(f)
                        feedback_history[feedback_file.stem] = feedback_data
                except Exception as e:
                    st.error(f"Erreur lors de la lecture de {feedback_file}: {str(e)}")
            return feedback_history
    
    def show_feedback_dashboard(self):
        """Affiche un tableau de bord des feedbacks"""
        st.subheader("📊 Tableau de Bord des Validations Humaines")
        
        feedback_history = self.get_feedback_history()
        
        if not feedback_history:
            st.info("Aucun historique de validation disponible")
            return
        
        # Statistiques globales
        total = len(feedback_history)
        validated = sum(1 for f in feedback_history.values() if f["status"] == "validated")
        rejected = total - validated
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total des Validations", total)
        with col2:
            st.metric("Validées", validated)
        with col3:
            st.metric("Rejetées", rejected)
        
        # Affichage détaillé
        st.write("### Historique Détaillé")
        for task_id, feedback in feedback_history.items():
            with st.expander(f"Tâche {task_id} - {feedback['timestamp']}"):
                st.write(f"**Status:** {feedback['status']}")
                st.write("**Données validées:**")
                st.json(feedback["data"])
                if feedback["feedback"]:
                    st.write("**Commentaires:**", feedback["feedback"])
    
    def require_validation(self, confidence_score: float, threshold: float = 0.8) -> bool:
        """Détermine si une validation humaine est nécessaire"""
        return confidence_score < threshold
