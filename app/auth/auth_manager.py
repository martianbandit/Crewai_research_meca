import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

class AuthManager:
    def __init__(self):
        # Configuration des utilisateurs (à remplacer par Supabase plus tard)
        self.config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'name': 'Admin',
                        'password': 'xxx'  # À remplacer par un hash sécurisé
                    }
                }
            }
        }
        self.authenticator = stauth.Authenticate(
            self.config['credentials'],
            'mechanic_app',
            'auth_key',
            cookie_expiry_days=30
        )

    def show_login_form(self):
        name, authentication_status, username = self.authenticator.login('Connexion', 'main')
        
        if authentication_status == False:
            st.error('Nom d\'utilisateur/mot de passe incorrect')
        elif authentication_status == None:
            st.warning('Veuillez entrer vos identifiants')
        
        st.session_state['authentication_status'] = authentication_status
        return authentication_status

    def logout(self):
        self.authenticator.logout('Déconnexion', 'sidebar')
        st.session_state['authentication_status'] = None