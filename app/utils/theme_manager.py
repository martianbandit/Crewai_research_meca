import streamlit as st
from hydralit_components import HyLoader, Loaders
import json
from pathlib import Path

class ThemeManager:
    """Gestionnaire de thèmes pour l'interface Streamlit"""
    
    THEMES = {
        "light": {
            "primary": "#FF4B4B",
            "secondary": "#0083B8",
            "background": "#FFFFFF",
            "text": "#262730",
            "success": "#00C851",
            "warning": "#FFB300",
            "error": "#FF4444"
        },
        "dark": {
            "primary": "#FF6B6B",
            "secondary": "#00A1E0",
            "background": "#0E1117",
            "text": "#FAFAFA",
            "success": "#00E676",
            "warning": "#FFC107",
            "error": "#FF5252"
        }
    }
    
    @staticmethod
    def load_theme(theme_name="light"):
        """Charge un thème spécifique"""
        theme = ThemeManager.THEMES.get(theme_name, ThemeManager.THEMES["light"])
        
        # Applique le thème via CSS personnalisé
        st.markdown(f"""
        <style>
            :root {{
                --primary-color: {theme["primary"]};
                --secondary-color: {theme["secondary"]};
                --background-color: {theme["background"]};
                --text-color: {theme["text"]};
                --success-color: {theme["success"]};
                --warning-color: {theme["warning"]};
                --error-color: {theme["error"]};
            }}
            
            .stButton>button {{
                background-color: var(--primary-color) !important;
                color: white !important;
            }}
            
            .stTextInput>div>div>input {{
                border-color: var(--primary-color) !important;
            }}
            
            .stProgress>div>div>div {{
                background-color: var(--primary-color) !important;
            }}
            
            .stAlert {{
                border-color: var(--primary-color) !important;
            }}
            
            .reportview-container {{
                background-color: var(--background-color) !important;
            }}
            
            .main {{
                color: var(--text-color) !important;
            }}
            
            h1, h2, h3, h4, h5, h6 {{
                color: var(--text-color) !important;
            }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def show_loader(message, loader_type=Loaders.standard_loaders.pacman):
        """Affiche un loader animé"""
        with HyLoader(message, loader_type):
            # Simule un chargement
            import time
            time.sleep(3)
    
    @staticmethod
    def apply_animations():
        """Applique des animations CSS"""
        st.markdown("""
        <style>
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes slideIn {
                from { transform: translateX(-100%); }
                to { transform: translateX(0); }
            }
            
            .fade-in {
                animation: fadeIn 0.5s ease-in;
            }
            
            .slide-in {
                animation: slideIn 0.5s ease-out;
            }
            
            /* Animation pour les cartes */
            .element-container:hover {
                transform: translateY(-5px);
                transition: transform 0.3s ease;
            }
            
            /* Animation pour les boutons */
            .stButton>button:hover {
                transform: scale(1.05);
                transition: transform 0.2s ease;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def save_theme_preference(theme_name):
        """Sauvegarde la préférence de thème"""
        config_path = Path("config/user_preferences.json")
        config_path.parent.mkdir(exist_ok=True)
        
        try:
            if config_path.exists():
                with open(config_path, "r") as f:
                    preferences = json.load(f)
            else:
                preferences = {}
            
            preferences["theme"] = theme_name
            
            with open(config_path, "w") as f:
                json.dump(preferences, f, indent=4)
                
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde des préférences : {str(e)}")
    
    @staticmethod
    def load_theme_preference():
        """Charge la préférence de thème"""
        config_path = Path("config/user_preferences.json")
        
        try:
            if config_path.exists():
                with open(config_path, "r") as f:
                    preferences = json.load(f)
                return preferences.get("theme", "light")
            return "light"
            
        except Exception:
            return "light"
