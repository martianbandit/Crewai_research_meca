import os
import streamlit as st
import streamlit_authenticator as stauth
from app.auth.auth_manager import AuthManager
from app.database.supabase_manager import SupabaseManager
from app.agents.mechanic_agents import MechanicCrew
from app.memory.memo_manager import MemoManager
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Assistant Mécanique Pro",
    page_icon="🔧",
    layout="wide"
)

# Initialisation des gestionnaires
auth_manager = AuthManager()
db_manager = SupabaseManager()
memo_manager = MemoManager()

# Configuration de l'authentification
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# Interface de connexion
if st.session_state['authentication_status'] is not True:
    auth_manager.show_login_form()
else:
    # Menu principal
    st.sidebar.title("Menu Principal")
    menu_choice = st.sidebar.selectbox(
        "Navigation",
        ["Bons de travail", "Véhicules", "Pièces", "Mécaniciens"]
    )

    # Affichage du menu sélectionné
    if menu_choice == "Bons de travail":
        st.title("Gestion des Bons de Travail")
        
        # Création d'un nouveau bon de travail
        with st.form("work_order_form"):
            st.subheader("Nouveau Bon de Travail")
            
            # Sélection du véhicule depuis la base de données
            vehicles = db_manager.get_vehicles()
            selected_vehicle = st.selectbox(
                "Sélectionner un véhicule",
                options=vehicles,
                format_func=lambda x: f"{x['make']} {x['model']} ({x['year']}) - {x['vin']}"
            )
            
            # Sélection du mécanicien
            mechanics = db_manager.get_mechanics()
            selected_mechanic = st.selectbox(
                "Mécanicien assigné",
                options=mechanics,
                format_func=lambda x: f"{x['first_name']} {x['last_name']}"
            )
            
            # Description du problème
            problem_description = st.text_area("Description du problème:", height=100)
            symptoms = st.text_area("Symptômes observés:", height=100)
            
            submitted = st.form_submit_button("Générer le Bon de Travail")

        if submitted and problem_description:
            with st.spinner("Analyse en cours..."):
                # Création du contexte pour les agents
                context = {
                    "vehicle": selected_vehicle,
                    "mechanic": selected_mechanic,
                    "problem": problem_description,
                    "symptoms": symptoms
                }
                
                # Récupération de l'historique depuis memo
                history = memo_manager.get_vehicle_history(selected_vehicle['vin'])
                
                # Initialisation du crew avec le contexte et l'historique
                crew = MechanicCrew(context, history)
                result = crew.process_work_order()
                
                # Sauvegarde du bon de travail dans Supabase
                work_order = db_manager.create_work_order(result)
                
                # Mise à jour de la mémoire
                memo_manager.update_vehicle_history(selected_vehicle['vin'], result)
                
                # Affichage des résultats
                st.success("Bon de travail généré avec succès!")
                st.json(result)

    elif menu_choice == "Véhicules":
        st.title("Gestion des Véhicules")
        
        # Affichage de la liste des véhicules
        vehicles = db_manager.get_vehicles()
        st.dataframe(vehicles)
        
        # Formulaire d'ajout de véhicule
        with st.form("add_vehicle_form"):
            st.subheader("Ajouter un nouveau véhicule")
            make = st.text_input("Marque:")
            model = st.text_input("Modèle:")
            year = st.number_input("Année:", min_value=1900, max_value=2024)
            vin = st.text_input("Numéro VIN:")
            
            if st.form_submit_button("Ajouter"):
                db_manager.add_vehicle(make, model, year, vin)
                st.success("Véhicule ajouté avec succès!")
                st.rerun()

    elif menu_choice == "Pièces":
        st.title("Gestion des Pièces")
        
        # Affichage de la liste des pièces
        parts = db_manager.get_parts()
        st.dataframe(parts)
        
        # Formulaire d'ajout de pièce
        with st.form("add_part_form"):
            st.subheader("Ajouter une nouvelle pièce")
            part_number = st.text_input("Numéro de pièce:")
            description = st.text_input("Description:")
            manufacturer = st.text_input("Fabricant:")
            price = st.number_input("Prix:", min_value=0.0)
            
            if st.form_submit_button("Ajouter"):
                db_manager.add_part(part_number, description, manufacturer, price)
                st.success("Pièce ajoutée avec succès!")
                st.rerun()

    elif menu_choice == "Mécaniciens":
        st.title("Gestion des Mécaniciens")
        
        # Affichage de la liste des mécaniciens
        mechanics = db_manager.get_mechanics()
        st.dataframe(mechanics)
        
        # Formulaire d'ajout de mécanicien
        with st.form("add_mechanic_form"):
            st.subheader("Ajouter un nouveau mécanicien")
            first_name = st.text_input("Prénom:")
            last_name = st.text_input("Nom:")
            specialization = st.text_input("Spécialisation:")
            
            if st.form_submit_button("Ajouter"):
                db_manager.add_mechanic(first_name, last_name, specialization)
                st.success("Mécanicien ajouté avec succès!")
                st.rerun()

    # Bouton de déconnexion
    if st.sidebar.button("Déconnexion"):
        auth_manager.logout()