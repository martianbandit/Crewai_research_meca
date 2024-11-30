import streamlit as st
from streamlit_custom_notification_box import custom_notification_box
from datetime import datetime
import json
from pathlib import Path
import time

class NotificationManager:
    """Gestionnaire de notifications pour l'interface Streamlit"""
    
    NOTIFICATION_TYPES = {
        "info": {
            "icon": "ℹ️",
            "color": "#0083B8"
        },
        "success": {
            "icon": "✅",
            "color": "#00C851"
        },
        "warning": {
            "icon": "⚠️",
            "color": "#FFB300"
        },
        "error": {
            "icon": "❌",
            "color": "#FF4444"
        }
    }
    
    def __init__(self):
        if 'notifications' not in st.session_state:
            st.session_state.notifications = []
        
        self.notifications_file = Path("data/notifications.json")
        self.notifications_file.parent.mkdir(exist_ok=True)
        
        self._load_notifications()
    
    def _load_notifications(self):
        """Charge les notifications depuis le fichier"""
        try:
            if self.notifications_file.exists():
                with open(self.notifications_file, "r") as f:
                    stored_notifications = json.load(f)
                st.session_state.notifications = stored_notifications
        except Exception as e:
            st.error(f"Erreur lors du chargement des notifications : {str(e)}")
    
    def _save_notifications(self):
        """Sauvegarde les notifications dans le fichier"""
        try:
            with open(self.notifications_file, "w") as f:
                json.dump(st.session_state.notifications, f, indent=4)
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde des notifications : {str(e)}")
    
    def add_notification(self, message, type="info"):
        """Ajoute une nouvelle notification"""
        notification = {
            "id": int(time.time() * 1000),
            "message": message,
            "type": type,
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        
        st.session_state.notifications.insert(0, notification)
        self._save_notifications()
        
        # Affiche la notification
        self.show_notification(notification)
    
    def show_notification(self, notification):
        """Affiche une notification"""
        style = self.NOTIFICATION_TYPES.get(notification["type"], 
                                          self.NOTIFICATION_TYPES["info"])
        
        custom_notification_box(
            border_left_color=style["color"],
            border_right_color=style["color"],
            border_top_color=style["color"],
            border_bottom_color=style["color"],
            icon=style["icon"],
            title=notification["type"].capitalize(),
            message=notification["message"],
            duration=5
        )
    
    def mark_as_read(self, notification_id):
        """Marque une notification comme lue"""
        for notification in st.session_state.notifications:
            if notification["id"] == notification_id:
                notification["read"] = True
                break
        self._save_notifications()
    
    def clear_notifications(self):
        """Supprime toutes les notifications"""
        st.session_state.notifications = []
        self._save_notifications()
    
    def get_unread_count(self):
        """Retourne le nombre de notifications non lues"""
        return sum(1 for n in st.session_state.notifications if not n["read"])
    
    def show_notification_center(self):
        """Affiche le centre de notifications"""
        if not st.session_state.notifications:
            st.info("Aucune notification")
            return
        
        for notification in st.session_state.notifications:
            with st.expander(
                f"{notification['type'].capitalize()} - "
                f"{datetime.fromisoformat(notification['timestamp']).strftime('%d/%m/%Y %H:%M')}",
                expanded=not notification["read"]
            ):
                st.write(notification["message"])
                if not notification["read"]:
                    if st.button("Marquer comme lu", key=f"read_{notification['id']}"):
                        self.mark_as_read(notification["id"])
                        st.experimental_rerun()
        
        if st.button("Effacer toutes les notifications"):
            self.clear_notifications()
            st.experimental_rerun()
