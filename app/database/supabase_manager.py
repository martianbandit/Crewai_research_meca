from supabase import create_client
import os
from dotenv import load_dotenv

class SupabaseManager:
    def __init__(self):
        load_dotenv()
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

    def get_vehicles(self):
        response = self.supabase.table('vehicles').select("*").execute()
        return response.data

    def add_vehicle(self, make, model, year, vin):
        data = {
            'make': make,
            'model': model,
            'year': year,
            'vin': vin
        }
        return self.supabase.table('vehicles').insert(data).execute()

    def get_mechanics(self):
        response = self.supabase.table('mechanics').select("*").execute()
        return response.data

    def add_mechanic(self, first_name, last_name, specialization):
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'specialization': specialization
        }
        return self.supabase.table('mechanics').insert(data).execute()

    def get_parts(self):
        response = self.supabase.table('parts').select("*").execute()
        return response.data

    def add_part(self, part_number, description, manufacturer, price):
        data = {
            'part_number': part_number,
            'description': description,
            'manufacturer': manufacturer,
            'price': price
        }
        return self.supabase.table('parts').insert(data).execute()

    def create_work_order(self, work_order_data):
        return self.supabase.table('work_orders').insert(work_order_data).execute()