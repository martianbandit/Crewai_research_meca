import streamlit as st
import extra_streamlit_components as stx
from streamlit_option_menu import option_menu
from datetime import datetime
import os
from pathlib import Path
import json

from app.flows.diagnostic_flow import DiagnosticFlow
from app.flows.inspection_flow import InspectionFlow
from app.flows.maintenance_flow import MaintenanceFlow
from app.utils.theme_manager import ThemeManager
from app.utils.export_manager import ExportManager
from app.utils.notification_manager import NotificationManager
from app.utils.animation_manager import AnimationManager
from app.utils.search_manager import SearchManager

# Configuration de la page
st.set_page_config(
    page_title="Assistant Mécanique Pro",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation des gestionnaires
theme_manager = ThemeManager()
notification_manager = NotificationManager()
animation_manager = AnimationManager()
search_manager = SearchManager()

# Initialisation des flows
if 'diagnostic_flow' not in st.session_state:
    st.session_state.diagnostic_flow = DiagnosticFlow()
if 'inspection_flow' not in st.session_state:
    st.session_state.inspection_flow = InspectionFlow()
if 'maintenance_flow' not in st.session_state:
    st.session_state.maintenance_flow = MaintenanceFlow()

# Chargement du thème
current_theme = theme_manager.load_theme_preference()
theme_manager.load_theme(current_theme)
theme_manager.apply_animations()

# Sidebar
with st.sidebar:
    st.image("assets/logo.png", width=100)
    
    # Menu principal avec animations
    selected = option_menu(
        "Menu Principal",
        ["Tableau de Bord", "Diagnostic", "Inspection", "Maintenance", "Historique", "Paramètres"],
        icons=['speedometer2', 'cpu', 'tools', 'wrench', 'clock-history', 'gear'],
        menu_icon="cast",
        default_index=0,
    )
    
    # Affichage du nombre de notifications non lues
    unread_count = notification_manager.get_unread_count()
    if unread_count > 0:
        st.sidebar.markdown(f"📫 **{unread_count}** notifications non lues")
    
    # Filtres de recherche
    filters = search_manager.create_search_filters()

# Fonction pour créer une carte animée
def animated_card(title, value, delta=None, color="#FF4B4B"):
    with st.container():
        animation_manager.apply_entrance_animation(f"card_{title}")
        st.markdown(f"""
        <div style='
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid {color};
            margin-bottom: 1rem;
        '>
            <h3 style='color: {color}'>{title}</h3>
            <h2>{value}</h2>
            {f"<p style='color: {'green' if float(delta) > 0 else 'red'}'>{delta}</p>" if delta else ""}
        </div>
        """, unsafe_allow_html=True)

# Pages principales
if selected == "Tableau de Bord":
    st.title("Tableau de Bord")
    animation_manager.show_loading_animation()
    
    # Métriques principales
    col1, col2, col3 = st.columns(3)
    with col1:
        animated_card("Diagnostics Aujourd'hui", "8", "+2")
    with col2:
        animated_card("Inspections en Cours", "5", "-1")
    with col3:
        animated_card("Maintenances Planifiées", "12", "+3")
    
    # Graphiques et statistiques
    # ... (code des graphiques)

elif selected == "Diagnostic":
    st.session_state.diagnostic_flow.show_diagnostic_interface()

elif selected == "Inspection":
    st.session_state.inspection_flow.show_inspection_interface()

elif selected == "Maintenance":
    st.session_state.maintenance_flow.show_maintenance_interface()

elif selected == "Historique":
    st.title("Historique")
    
    # Sélection du type d'historique
    history_type = st.selectbox(
        "Type d'historique",
        ["Diagnostics", "Inspections", "Maintenances"]
    )
    
    # Récupération et filtrage des données selon le type
    if history_type == "Diagnostics":
        data_path = Path("data/diagnostic_reports")
    elif history_type == "Inspections":
        data_path = Path("data/inspection_reports")
    else:
        data_path = Path("data/maintenance_plans")
    
    # Chargement des données
    data = []
    if data_path.exists():
        for file in data_path.glob("*.json"):
            try:
                with open(file, "r") as f:
                    data.append(json.load(f))
            except Exception as e:
                st.error(f"Erreur lors de la lecture de {file}: {str(e)}")
    
    # Application des filtres
    filtered_data = search_manager.apply_filters(data, filters)
    
    # Affichage des résultats
    search_manager.create_data_table(filtered_data)
    search_manager.create_search_summary(filtered_data, len(data))

elif selected == "Paramètres":
    st.title("Paramètres")
    
    # Thème
    theme = st.selectbox(
        "Thème",
        ["light", "dark"],
        index=0 if current_theme == "light" else 1
    )
    
    if theme != current_theme:
        theme_manager.save_theme_preference(theme)
        st.experimental_rerun()
    
    # Notifications
    st.subheader("Centre de Notifications")
    notification_manager.show_notification_center()
    
    # Validation humaine
    st.subheader("Paramètres de Validation Humaine")
    confidence_threshold = st.slider(
        "Seuil de confiance pour la validation humaine",
        min_value=0.0,
        max_value=1.0,
        value=0.8,
        step=0.1
    )
    
    # Base de connaissances
    st.subheader("Base de Connaissances")
    if st.button("Réindexer la Base de Connaissances"):
        with st.spinner("Réindexation en cours..."):
            # Réindexation des bases de connaissances
            vector_store = VectorStoreManager()
            
            # Diagnostic KB
            diagnostic_docs = vector_store.load_documents(["data/diagnostic_reports"])
            vector_store.create_vector_store(diagnostic_docs, "diagnostic_kb")
            
            # Inspection KB
            inspection_docs = vector_store.load_documents(["data/inspection_reports"])
            vector_store.create_vector_store(inspection_docs, "inspection_kb")
            
            # Maintenance KB
            maintenance_docs = vector_store.load_documents(["data/maintenance_plans"])
            vector_store.create_vector_store(maintenance_docs, "maintenance_kb")
            
            st.success("Base de connaissances réindexée avec succès!")

# Footer avec animation
st.markdown("---")
animation_manager.apply_fade_animation("footer")
st.markdown(
    """
    <div id="footer" style='text-align: center'>
        Développé avec ❤️ par l'équipe Codeium |
        <a href="https://docs.example.com">Documentation</a> |
        <a href="mailto:support@example.com">Support</a>
    </div>
    """,
    unsafe_allow_html=True
)