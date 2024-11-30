import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from crewai_tools import SerperDevTool
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class NHTSATools:
    def __init__(self):
        self.base_url = "https://api.nhtsa.gov/vehicles"
    
    def get_recalls(self, make, model, year):
        url = f"{self.base_url}/recalls?make={make}&model={model}&modelYear={year}"
        response = requests.get(url)
        return response.json()
    
    def decode_vin(self, vin):
        url = f"{self.base_url}/decodevin/{vin}?format=json"
        response = requests.get(url)
        return response.json()

class PartsSearchTool:
    def __init__(self):
        self.serper = SerperDevTool()
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=self.chrome_options
        )
    
    def search_part(self, query, make, model):
        # Recherche via Serper
        serper_results = self.serper.search(f"{query} {make} {model} truck part")
        
        # Recherche sur des sites spécialisés
        specialized_sites = [
            "https://www.rockauto.com",
            "https://www.navistarservice.com",
            "https://www.paccar.com/parts/",
            "https://www.alliantpower.com"
        ]
        
        all_results = []
        for site in specialized_sites:
            try:
                self.driver.get(site)
                search_box = self.driver.find_element(By.NAME, "q")
                search_box.send_keys(f"{make} {model} {query}")
                search_box.submit()
                
                # Extraction des résultats
                results = self.driver.find_elements(By.CLASS_NAME, "part-result")
                for result in results[:3]:
                    all_results.append({
                        "source": site,
                        "title": result.find_element(By.CLASS_NAME, "title").text,
                        "part_number": result.find_element(By.CLASS_NAME, "part-number").text,
                        "price": result.find_element(By.CLASS_NAME, "price").text,
                        "availability": result.find_element(By.CLASS_NAME, "availability").text
                    })
            except Exception as e:
                print(f"Erreur pour {site}: {str(e)}")
        
        return {
            "serper_results": serper_results,
            "specialized_results": all_results
        }

class GeoLocationTool:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="mechanic_assistant")
    
    def find_nearby_dealers(self, make, latitude, longitude, radius=50):
        # Recherche des concessionnaires à proximité
        query = f"{make} truck dealer"
        location = f"{latitude}, {longitude}"
        
        dealers = []
        try:
            locations = self.geolocator.geocode(query, exactly_one=False, limit=10)
            for loc in locations:
                dealer_coords = (loc.latitude, loc.longitude)
                current_coords = (latitude, longitude)
                distance = geodesic(dealer_coords, current_coords).miles
                
                if distance <= radius:
                    dealers.append({
                        "name": loc.address,
                        "distance": round(distance, 2),
                        "coordinates": dealer_coords
                    })
        except Exception as e:
            print(f"Erreur de géolocalisation: {str(e)}")
        
        return sorted(dealers, key=lambda x: x["distance"])

class TechnicalDocumentationTool:
    def __init__(self):
        self.browse_ai_key = os.getenv("BROWSE_AI_KEY")
        self.base_urls = {
            "manuals": "https://www.truckntrailer.com/manuals/",
            "bulletins": "https://www.tsi-uptime.com/bulletins/",
            "diagrams": "https://www.mitchelldiag.com/"
        }
    
    def get_technical_docs(self, make, model, year, doc_type):
        url = self.base_urls.get(doc_type)
        if not url:
            return []
        
        try:
            response = requests.get(
                url,
                params={
                    "make": make,
                    "model": model,
                    "year": year
                },
                headers={"Authorization": f"Bearer {self.browse_ai_key}"}
            )
            return response.json()
        except Exception as e:
            print(f"Erreur de récupération des documents: {str(e)}")
            return []
    
    def search_service_bulletins(self, keywords):
        try:
            response = requests.get(
                self.base_urls["bulletins"],
                params={"q": keywords},
                headers={"Authorization": f"Bearer {self.browse_ai_key}"}
            )
            return response.json()
        except Exception as e:
            print(f"Erreur de recherche des bulletins: {str(e)}")
            return []

class DiagnosticTool:
    def __init__(self):
        self.diagnostic_db = pd.read_csv("diagnostic_database.csv")  # Base de données locale
    
    def analyze_symptoms(self, symptoms, vehicle_info):
        # Analyse des symptômes par rapport à la base de données
        relevant_cases = self.diagnostic_db[
            (self.diagnostic_db["make"] == vehicle_info["make"]) &
            (self.diagnostic_db["model"] == vehicle_info["model"])
        ]
        
        # Analyse de similarité des symptômes
        matches = []
        for _, case in relevant_cases.iterrows():
            similarity = self._calculate_similarity(symptoms, case["symptoms"])
            if similarity > 0.7:  # Seuil de similarité
                matches.append({
                    "case_id": case["id"],
                    "diagnosis": case["diagnosis"],
                    "solution": case["solution"],
                    "parts_needed": case["parts_needed"],
                    "similarity": similarity
                })
        
        return sorted(matches, key=lambda x: x["similarity"], reverse=True)
    
    def _calculate_similarity(self, symptoms1, symptoms2):
        # Implémentation simple de similarité textuelle
        # À améliorer avec des techniques NLP plus avancées
        words1 = set(symptoms1.lower().split())
        words2 = set(symptoms2.lower().split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)

class MaintenanceScheduleTool:
    def get_maintenance_schedule(self, make, model, year, mileage):
        # Récupération du programme d'entretien recommandé
        schedule = {
            "upcoming_services": [],
            "past_due": [],
            "recommendations": []
        }
        
        # Logique pour déterminer les services nécessaires
        # À implémenter selon les spécifications du constructeur
        
        return schedule