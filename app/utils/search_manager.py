import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re

class SearchManager:
    """Gestionnaire de recherche et de filtrage"""
    
    @staticmethod
    def create_search_filters():
        """Crée les filtres de recherche dans la sidebar"""
        with st.sidebar.expander("Filtres de Recherche", expanded=False):
            # Filtre par date
            date_filter = st.date_input(
                "Période",
                value=(
                    datetime.now() - timedelta(days=30),
                    datetime.now()
                )
            )
            
            # Filtre par statut
            status_filter = st.multiselect(
                "Statut",
                ["En Service", "En Maintenance", "Hors Service"],
                default=["En Service"]
            )
            
            # Filtre par type de véhicule
            vehicle_type_filter = st.multiselect(
                "Type de Véhicule",
                ["Camion", "Remorque", "Bus", "Utilitaire"],
                default=["Camion"]
            )
            
            # Filtre par criticité
            severity_filter = st.select_slider(
                "Niveau de Criticité",
                options=["Faible", "Moyen", "Élevé"],
                value="Moyen"
            )
            
            # Recherche textuelle
            text_search = st.text_input("Recherche", "")
            
            return {
                "date_range": date_filter,
                "status": status_filter,
                "vehicle_type": vehicle_type_filter,
                "severity": severity_filter,
                "text_search": text_search
            }
    
    @staticmethod
    def apply_filters(data: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Applique les filtres sur les données"""
        filtered_data = data.copy()
        
        # Filtre par date
        if isinstance(filters["date_range"], tuple):
            start_date, end_date = filters["date_range"]
            filtered_data = [
                item for item in filtered_data
                if start_date <= datetime.fromisoformat(item["date"]).date() <= end_date
            ]
        
        # Filtre par statut
        if filters["status"]:
            filtered_data = [
                item for item in filtered_data
                if item["status"] in filters["status"]
            ]
        
        # Filtre par type de véhicule
        if filters["vehicle_type"]:
            filtered_data = [
                item for item in filtered_data
                if item["vehicle_type"] in filters["vehicle_type"]
            ]
        
        # Filtre par criticité
        if filters["severity"]:
            filtered_data = [
                item for item in filtered_data
                if item["severity"] == filters["severity"]
            ]
        
        # Recherche textuelle
        if filters["text_search"]:
            search_terms = filters["text_search"].lower().split()
            filtered_data = [
                item for item in filtered_data
                if any(
                    term in str(value).lower()
                    for value in item.values()
                    for term in search_terms
                )
            ]
        
        return filtered_data
    
    @staticmethod
    def create_data_table(data: List[Dict[str, Any]], 
                         columns: Optional[List[str]] = None):
        """Crée un tableau de données filtrable"""
        if not data:
            st.warning("Aucune donnée à afficher")
            return
        
        df = pd.DataFrame(data)
        
        if columns:
            df = df[columns]
        
        # Ajoute des options de tri et de filtrage
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Options d'export
        if st.button("Exporter les données"):
            from app.utils.export_manager import ExportManager
            
            format = st.selectbox(
                "Format d'export",
                ["Excel", "CSV", "JSON"]
            )
            
            if format == "Excel":
                output = ExportManager.to_excel(data)
                st.download_button(
                    "Télécharger Excel",
                    output,
                    "donnees.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            elif format == "CSV":
                csv = df.to_csv(index=False)
                st.download_button(
                    "Télécharger CSV",
                    csv,
                    "donnees.csv",
                    "text/csv"
                )
            else:
                json_str = df.to_json(orient="records")
                st.download_button(
                    "Télécharger JSON",
                    json_str,
                    "donnees.json",
                    "application/json"
                )
    
    @staticmethod
    def highlight_search_terms(text: str, search_terms: List[str]) -> str:
        """Met en surbrillance les termes recherchés dans le texte"""
        if not search_terms:
            return text
        
        pattern = "|".join(map(re.escape, search_terms))
        return re.sub(
            f'({pattern})',
            r'<span style="background-color: yellow">\1</span>',
            text,
            flags=re.IGNORECASE
        )
    
    @staticmethod
    def create_search_summary(filtered_data: List[Dict[str, Any]], 
                            total_count: int):
        """Crée un résumé des résultats de recherche"""
        st.write(f"""
        **Résultats de la recherche**
        - Total des éléments : {total_count}
        - Éléments filtrés : {len(filtered_data)}
        - Taux de filtrage : {(1 - len(filtered_data)/total_count)*100:.1f}%
        """)
