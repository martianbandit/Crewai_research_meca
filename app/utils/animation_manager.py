import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
from pathlib import Path

class AnimationManager:
    """Gestionnaire d'animations pour l'interface Streamlit"""
    
    # Cache pour les animations Lottie
    _lottie_cache = {}
    
    @staticmethod
    def load_lottie_url(url: str):
        """Charge une animation Lottie depuis une URL"""
        if url in AnimationManager._lottie_cache:
            return AnimationManager._lottie_cache[url]
        
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            animation = r.json()
            AnimationManager._lottie_cache[url] = animation
            return animation
        except Exception:
            return None
    
    @staticmethod
    def load_lottie_file(filepath: str):
        """Charge une animation Lottie depuis un fichier"""
        if filepath in AnimationManager._lottie_cache:
            return AnimationManager._lottie_cache[filepath]
        
        try:
            with open(filepath, "r") as f:
                animation = json.load(f)
                AnimationManager._lottie_cache[filepath] = animation
                return animation
        except Exception:
            return None
    
    @staticmethod
    def show_loading_animation():
        """Affiche une animation de chargement"""
        loading_animation = AnimationManager.load_lottie_url(
            "https://assets5.lottiefiles.com/packages/lf20_usmfx6bp.json"
        )
        if loading_animation:
            st_lottie(loading_animation, height=200, key="loading")
    
    @staticmethod
    def show_success_animation():
        """Affiche une animation de succès"""
        success_animation = AnimationManager.load_lottie_url(
            "https://assets9.lottiefiles.com/packages/lf20_lk80fpsm.json"
        )
        if success_animation:
            st_lottie(success_animation, height=200, key="success")
    
    @staticmethod
    def show_error_animation():
        """Affiche une animation d'erreur"""
        error_animation = AnimationManager.load_lottie_url(
            "https://assets1.lottiefiles.com/packages/lf20_afwjhfb2.json"
        )
        if error_animation:
            st_lottie(error_animation, height=200, key="error")
    
    @staticmethod
    def apply_entrance_animation(element_key: str):
        """Applique une animation d'entrée à un élément"""
        st.markdown(f"""
        <style>
            #{element_key} {{
                animation: slideIn 0.5s ease-out;
            }}
            
            @keyframes slideIn {{
                from {{ transform: translateX(-100%); opacity: 0; }}
                to {{ transform: translateX(0); opacity: 1; }}
            }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_hover_animation(element_key: str):
        """Applique une animation au survol d'un élément"""
        st.markdown(f"""
        <style>
            #{element_key}:hover {{
                transform: scale(1.05);
                transition: transform 0.3s ease;
            }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_pulse_animation(element_key: str):
        """Applique une animation de pulsation à un élément"""
        st.markdown(f"""
        <style>
            #{element_key} {{
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_fade_animation(element_key: str, direction="in"):
        """Applique une animation de fondu à un élément"""
        if direction == "in":
            st.markdown(f"""
            <style>
                #{element_key} {{
                    animation: fadeIn 0.5s ease-in;
                }}
                
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <style>
                #{element_key} {{
                    animation: fadeOut 0.5s ease-out;
                }}
                
                @keyframes fadeOut {{
                    from {{ opacity: 1; }}
                    to {{ opacity: 0; }}
                }}
            </style>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_bounce_animation(element_key: str):
        """Applique une animation de rebond à un élément"""
        st.markdown(f"""
        <style>
            #{element_key} {{
                animation: bounce 1s infinite;
            }}
            
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
            }}
        </style>
        """, unsafe_allow_html=True)
