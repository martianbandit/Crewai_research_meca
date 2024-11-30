from typing import Dict, Any, List, Optional
import json
from pathlib import Path
from datetime import datetime, timedelta
import streamlit as st
from app.utils.async_manager import AsyncManager

class MemoryManager:
    """Gestionnaire de mémoire optimisé"""
    
    def __init__(self):
        self.memory_path = Path("data/memory")
        self.memory_path.mkdir(parents=True, exist_ok=True)
        self.cache_duration = timedelta(hours=1)
        
        # Initialisation du cache en mémoire
        if 'memory_cache' not in st.session_state:
            st.session_state.memory_cache = {}
    
    @AsyncManager.cache_result(ttl_seconds=3600)
    def get_vehicle_history(self, vin: str) -> List[Dict[str, Any]]:
        """Récupère l'historique d'un véhicule avec mise en cache"""
        cache_key = f"vehicle_history_{vin}"
        
        # Vérification du cache en mémoire
        if cache_key in st.session_state.memory_cache:
            cache_entry = st.session_state.memory_cache[cache_key]
            if datetime.now() - cache_entry['timestamp'] < self.cache_duration:
                return cache_entry['data']
        
        # Lecture depuis le fichier
        history_file = self.memory_path / f"{vin}.json"
        if history_file.exists():
            try:
                with open(history_file, "r") as f:
                    history = json.load(f)
                    
                # Mise en cache
                st.session_state.memory_cache[cache_key] = {
                    'data': history,
                    'timestamp': datetime.now()
                }
                return history
            except Exception as e:
                st.error(f"Erreur lors de la lecture de l'historique: {str(e)}")
                return []
        return []
    
    @AsyncManager.run_async
    def update_vehicle_history(
        self,
        vin: str,
        new_data: Dict[str, Any],
        operation_type: str
    ) -> bool:
        """Met à jour l'historique d'un véhicule de manière asynchrone"""
        try:
            # Récupération de l'historique existant
            history = self.get_vehicle_history(vin)
            
            # Ajout de la nouvelle entrée
            entry = {
                "timestamp": datetime.now().isoformat(),
                "operation_type": operation_type,
                "data": new_data
            }
            history.append(entry)
            
            # Sauvegarde dans le fichier
            history_file = self.memory_path / f"{vin}.json"
            with open(history_file, "w") as f:
                json.dump(history, f, indent=4)
            
            # Mise à jour du cache
            cache_key = f"vehicle_history_{vin}"
            st.session_state.memory_cache[cache_key] = {
                'data': history,
                'timestamp': datetime.now()
            }
            
            return True
        except Exception as e:
            st.error(f"Erreur lors de la mise à jour de l'historique: {str(e)}")
            return False
    
    def clear_cache(self, vin: Optional[str] = None):
        """Nettoie le cache en mémoire"""
        if vin:
            cache_key = f"vehicle_history_{vin}"
            if cache_key in st.session_state.memory_cache:
                del st.session_state.memory_cache[cache_key]
        else:
            st.session_state.memory_cache = {}
    
    def optimize_storage(self):
        """Optimise le stockage en supprimant les anciennes entrées"""
        try:
            for history_file in self.memory_path.glob("*.json"):
                with open(history_file, "r") as f:
                    history = json.load(f)
                
                # Suppression des entrées de plus de 6 mois
                cutoff_date = datetime.now() - timedelta(days=180)
                filtered_history = [
                    entry for entry in history
                    if datetime.fromisoformat(entry['timestamp']) > cutoff_date
                ]
                
                # Sauvegarde de l'historique filtré
                with open(history_file, "w") as f:
                    json.dump(filtered_history, f, indent=4)
        except Exception as e:
            st.error(f"Erreur lors de l'optimisation du stockage: {str(e)}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Récupère les statistiques de la mémoire"""
        stats = {
            "total_vehicles": 0,
            "total_entries": 0,
            "storage_size": 0,
            "cache_entries": len(st.session_state.memory_cache)
        }
        
        try:
            for history_file in self.memory_path.glob("*.json"):
                stats["total_vehicles"] += 1
                stats["storage_size"] += history_file.stat().st_size
                
                with open(history_file, "r") as f:
                    history = json.load(f)
                    stats["total_entries"] += len(history)
        except Exception as e:
            st.error(f"Erreur lors du calcul des statistiques: {str(e)}")
        
        return stats
