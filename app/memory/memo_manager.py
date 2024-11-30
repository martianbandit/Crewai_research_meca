from typing import Dict, List, Optional
import memoization as memo
from datetime import datetime, timedelta

class MemoManager:
    """Gestionnaire de mémoire utilisant memoization pour optimiser les accès fréquents"""

    def __init__(self):
        self.cache_duration = timedelta(hours=1)  # Durée par défaut du cache

    @memo.memoize(duration=3600)  # Cache d'une heure
    async def get_work_order(self, work_order_id: str) -> Optional[Dict]:
        """Récupère un bon de travail avec mise en cache"""
        # Implémentation de la récupération depuis Supabase
        pass

    @memo.memoize(duration=3600)
    async def get_work_orders_by_vehicle(self, vehicle_id: str) -> List[Dict]:
        """Récupère tous les bons de travail d'un véhicule"""
        # Implémentation de la récupération depuis Supabase
        pass

    @memo.memoize(duration=3600)
    async def get_vehicle(self, vehicle_id: str) -> Optional[Dict]:
        """Récupère les informations d'un véhicule"""
        # Implémentation de la récupération depuis Supabase
        pass

    @memo.memoize(duration=3600)
    async def get_vehicle_by_vin(self, vin: str) -> Optional[Dict]:
        """Récupère un véhicule par son VIN"""
        # Implémentation de la récupération depuis Supabase
        pass

    @memo.memoize(duration=3600)
    async def get_part(self, part_id: str) -> Optional[Dict]:
        """Récupère les informations d'une pièce"""
        # Implémentation de la récupération depuis Supabase
        pass

    @memo.memoize(duration=3600)
    async def get_parts_by_vehicle(self, vehicle_id: str) -> List[Dict]:
        """Récupère toutes les pièces compatibles avec un véhicule"""
        # Implémentation de la récupération depuis Supabase
        pass

    def invalidate_work_order_cache(self, work_order_id: str):
        """Invalide le cache d'un bon de travail spécifique"""
        memo.clear(self.get_work_order, work_order_id)
        
    def invalidate_vehicle_cache(self, vehicle_id: str):
        """Invalide le cache d'un véhicule spécifique"""
        memo.clear(self.get_vehicle, vehicle_id)
        memo.clear(self.get_work_orders_by_vehicle, vehicle_id)
        memo.clear(self.get_parts_by_vehicle, vehicle_id)

    def invalidate_part_cache(self, part_id: str):
        """Invalide le cache d'une pièce spécifique"""
        memo.clear(self.get_part, part_id)

    def clear_all_cache(self):
        """Vide tout le cache"""
        memo.clear_all()