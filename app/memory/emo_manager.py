from memo import AsyncMemo

class MemoManager:
    def __init__(self):
        self.memo = AsyncMemo()

    async def get_vehicle_history(self, vin):
        # Récupère l'historique des interventions pour un véhicule
        history = await self.memo.async_get(f"vehicle_history_{vin}")
        return history if history else []

    async def update_vehicle_history(self, vin, new_work_order):
        # Ajoute un nouveau bon de travail à l'historique
        history = await self.get_vehicle_history(vin)
        history.append(new_work_order)
        await self.memo.async_set(f"vehicle_history_{vin}", history)