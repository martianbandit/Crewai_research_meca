import os
import streamlit as st
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

# Assurez-vous que Google Chrome est installé sur votre système

# Outil de recherche web
search_tool = SerperDevTool()

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
        self.driver.get('https://www.example-truckparts.com')  # URL fictive
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

web_scraper_agent = Agent(
    role='Scraper Web',
    goal='Récupérer des informations spécifiques depuis des sites de vente de pièces.',
    backstory="Spécialiste en extraction d'informations depuis des sources en ligne.",
    tools=[],  # Nous ajouterons l'outil au moment de l'exécution
    verbose=True
)

response_writer_agent = Agent(
    role='Rédacteur technique',
    goal='Synthétiser les résultats de la recherche pour générer un rapport.',
    backstory="Expert en rédaction technique pour créer des rapports compréhensibles.",
    tools=[],
    verbose=True
)

# Tâches
text_search_task = Task(
    description="Rechercher des informations détaillées sur la pièce de camion.",
    agent=text_search_agent,
    expected_output="Une liste d'informations détaillées sur la pièce de camion recherchée."
)

web_scraping_task = Task(
    description="Scraper des sites web pour obtenir des informations sur la pièce de camion.",
    agent=web_scraper_agent,
    expected_output="Des données spécifiques extraites des sites web, comme les prix et la disponibilité."
)

report_writing_task = Task(
    description="Générer un rapport complet sur la pièce basée sur les recherches.",
    agent=response_writer_agent,
    expected_output="Un rapport synthétique compilant toutes les informations collectées."
)

# Crew
truck_parts_crew = Crew(
    agents=[text_search_agent, web_scraper_agent, response_writer_agent],
    tasks=[text_search_task, web_scraping_task, report_writing_task],
    process=Process.sequential,  # Processus séquentiel pour enchaîner les tâches
    verbose=True
)

# Fonction pour exécuter le processus
def run_truck_parts_search(query):
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

search_query = st.text_input("Entrez la description ou le modèle de la pièce de camion :")
if st.button("Rechercher"):
    st.write("Recherche en cours...")
    results = run_truck_parts_search(query=search_query)
    st.write("Résultats de la recherche :", results)
