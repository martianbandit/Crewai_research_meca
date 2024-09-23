import os
import streamlit as st
from PIL import Image
import cv2
import requests
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from langchain_openai import ChatOpenAI

# Définir les clés d'API et les variables d'environnement
os.environ["OPENAI_API_KEY"] = "your_openai_key"  # Remplacez par votre clé OpenAI
os.environ["SERPER_API_KEY"] = "your_serper_key"  # Remplacez par votre clé Serper
TINEYE_API_KEY = "your_tineye_api_key"  # Remplacez par votre clé TinEye

# Assurez-vous que Google Chrome est installé sur votre système

# Outil de recherche web
search_tool = SerperDevTool()

# Outil d'analyse d'image avec recherche web
class ImageAnalysisTool:
    def __init__(self):
        pass

    def analyze_image(self, image_path):
        # Charger l'image et en extraire des caractéristiques
        image = cv2.imread(image_path)
        if image is None:
            return "Erreur : l'image n'a pas pu être chargée."

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, 100, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) == 0:
            return "Aucun contour trouvé dans l'image."

        # Trouver le plus grand contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Enregistrer l'image avec contours
        contour_image_path = 'output_image_with_contour.jpg'
        cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 3)
        cv2.imwrite(contour_image_path, image)

        # Dimensions de l'objet
        dimensions = {'largeur': w, 'hauteur': h}
        
        # Recherche inversée d'image sur le web
        search_results = self.search_image_online(image_path)
        
        return {"dimensions": dimensions, "image_path": contour_image_path, "search_results": search_results}

    def search_image_online(self, image_path):
        # Rechercher l'image en ligne avec l'API TinEye (ou autre service)
        url = 'https://api.tineye.com/rest/search/'
        files = {'image': open(image_path, 'rb')}
        params = {'api_key': TINEYE_API_KEY}

        response = requests.post(url, files=files, params=params)
        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                return data["results"]  # Résultats de la recherche
            else:
                return "Aucune correspondance trouvée."
        else:
            return f"Erreur lors de la recherche d'image : {response.status_code}"

image_analysis_tool = ImageAnalysisTool()

# Outil de scraping web
class WebScraperTool:
    def __init__(self):
        # Configurer les options pour le mode headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Exécute Chrome en mode headless
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Initialiser le WebDriver avec les options
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

    def search_part(self, query):
        self.driver.get('https://www.traction.com')  # URL fictive
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.send_keys(query)
        search_box.submit()
        # Code simplifié pour la démonstration
        results = [{"name": "Pièce X", "price": "100€"}, {"name": "Pièce Y", "price": "120€"}]
        return results

    def close(self):
        self.driver.quit()

# Agents
text_search_agent = Agent(
    role='Expert en recherche web',
    goal='Trouver des informations détaillées sur des pièces de camion.',
    backstory="Spécialiste en recherche avancée pour trouver des détails techniques sur des pièces.",
    tools=[search_tool],
    verbose=True
)

image_analysis_agent = Agent(
    role='Analyste image & Recherche inversée',
    goal='Analyser des images de pièces et trouver des correspondances en ligne.',
    backstory="Expert en analyse d'image et en recherche d'images similaires sur le web.",
    tools=[image_analysis_tool],
    verbose=True
)

web_scraper_agent = Agent(
    role='Scraper Web',
    goal='Récupérer des informations spécifiques depuis des sites de vente de pièces.',
    backstory="Spécialiste en extraction d'informations depuis des sources en ligne.",
    tools=[],  # Nous ajouterons l'outil au moment de l'exécution
    verbose=True
)

response_writer_agent = Agent(
    role='Rédacteur technique',
    goal='Synthétiser les résultats de la recherche et de l’analyse d’images pour générer un rapport.',
    backstory="Expert en rédaction technique pour créer des rapports compréhensibles.",
    tools=[],
    verbose=True
)

# Tâches
text_search_task = Task(
    description="Rechercher des informations détaillées sur la pièce de camion.",
    agent=text_search_agent
)

image_analysis_task = Task(
    description="Analyser l'image de la pièce et rechercher des correspondances en ligne.",
    agent=image_analysis_agent
)

web_scraping_task = Task(
    description="Scraper des sites web pour obtenir des informations sur la pièce de camion.",
    agent=web_scraper_agent
)

report_writing_task = Task(
    description="Générer un rapport complet sur la pièce basée sur les recherches et l'analyse.",
    agent=response_writer_agent
)

# Crew
truck_parts_crew = Crew(
    agents=[text_search_agent, image_analysis_agent, web_scraper_agent, response_writer_agent],
    tasks=[text_search_task, image_analysis_task, web_scraping_task, report_writing_task],
    process=Process.sequential,  # Processus séquentiel pour enchaîner les tâches
    verbose=True
)

# Fonction pour exécuter le processus
def run_truck_parts_search(query=None, image_path=None):
    # Si une image est fournie, exécuter uniquement l'analyse d'image
    if image_path:
        image_results = image_analysis_tool.analyze_image(image_path)
        return {"Analyse d'image": image_results}

    # Si une recherche textuelle est fournie, exécuter la recherche web
    if query:
        # Initialiser le scraper
        web_scraper_tool = WebScraperTool()
        try:
            # Ajouter l'outil au scraper agent
            web_scraper_agent.tools = [web_scraper_tool]
            # Exécuter le crew
            results = truck_parts_crew.kickoff()
        finally:
            # Fermer le WebDriver pour libérer les ressources
            web_scraper_tool.close()
        return results

# Interface Streamlit
st.title("Recherche et Analyse de Pièces de Camions")

# Choix de l'entrée : texte ou image
input_type = st.radio("Choisissez le type d'entrée :", ("Texte", "Image"))

# Section de recherche par texte
if input_type == "Texte":
    search_query = st.text_input("Entrez la description ou le modèle de la pièce de camion :")
    if st.button("Rechercher"):
        st.write("Recherche en cours...")
        results = run_truck_parts_search(query=search_query)
        st.write("Résultats de la recherche :", results)

# Section d'analyse d'image
if input_type == "Image":
    uploaded_image = st.file_uploader("Téléchargez une image de la pièce de camion", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        img = Image.open(uploaded_image)
        img_path = f"uploaded_{uploaded_image.name}"
        img.save(img_path)
        st.image(img, caption='Image téléchargée', use_column_width=True)
        if st.button("Analyser l'image"):
            st.write("Analyse en cours...")
            results = run_truck_parts_search(image_path=img_path)
            st.write("Résultats de l'analyse :", results)

# Remarque : Nous avons supprimé web_scraper_tool.close() au niveau du module, car il est géré dans la fonction
