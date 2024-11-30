from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from .utils.tools import (
    NHTSATools,
    PartsSearchTool,
    GeoLocationTool,
    TechnicalDocumentationTool,
    DiagnosticTool,
    MaintenanceScheduleTool
)

class MechanicCrew:
    def __init__(self, context, history):
        self.context = context
        self.history = history
        self.llm = ChatOpenAI(temperature=0.7)
        
        # Initialisation des outils
        self.nhtsa_tools = NHTSATools()
        self.parts_tool = PartsSearchTool()
        self.geo_tool = GeoLocationTool()
        self.doc_tool = TechnicalDocumentationTool()
        self.diagnostic_tool = DiagnosticTool()
        self.maintenance_tool = MaintenanceScheduleTool()

    def create_agents(self):
        # Agent Diagnostic Expert
        diagnostic_expert = Agent(
            role='Expert en Diagnostic',
            goal='Analyser les symptômes et établir un diagnostic précis',
            backstory="""Expert en diagnostic de camions lourds avec 20 ans d'expérience.
            Spécialisé dans l'analyse des problèmes complexes et l'utilisation
            des outils de diagnostic modernes.""",
            tools=[
                self.diagnostic_tool.analyze_symptoms,
                self.nhtsa_tools.get_recalls,
                self.doc_tool.search_service_bulletins
            ],
            llm=self.llm,
            verbose=True
        )

        # Agent Recherche Technique
        technical_researcher = Agent(
            role='Chercheur Technique',
            goal='Rechercher et compiler les informations techniques pertinentes',
            backstory="""Spécialiste en recherche technique automobile avec une expertise
            particulière dans la documentation des constructeurs et les bulletins
            de service.""",
            tools=[
                self.doc_tool.get_technical_docs,
                self.nhtsa_tools.decode_vin,
                self.maintenance_tool.get_maintenance_schedule
            ],
            llm=self.llm,
            verbose=True
        )

        # Agent Spécialiste Pièces
        parts_specialist = Agent(
            role='Spécialiste Pièces',
            goal='Identifier et localiser les pièces nécessaires',
            backstory="""Expert en identification et sourcing de pièces de camions.
            Connaissance approfondie des catalogues et des fournisseurs.""",
            tools=[
                self.parts_tool.search_part,
                self.geo_tool.find_nearby_dealers
            ],
            llm=self.llm,
            verbose=True
        )

        # Agent Rédacteur Technique
        technical_writer = Agent(
            role='Rédacteur Technique',
            goal='Rédiger des bons de travail détaillés et professionnels',
            backstory="""Spécialiste en documentation technique avec une expertise
            en rédaction de bons de travail conformes aux normes de l'industrie.""",
            tools=[],
            llm=self.llm,
            verbose=True
        )

        # Agent Planificateur de Maintenance
        maintenance_planner = Agent(
            role='Planificateur de Maintenance',
            goal='Planifier et optimiser les interventions de maintenance',
            backstory="""Expert en planification de maintenance préventive et
            corrective pour flottes de camions.""",
            tools=[
                self.maintenance_tool.get_maintenance_schedule,
                self.geo_tool.find_nearby_dealers
            ],
            llm=self.llm,
            verbose=True
        )

        return [
            diagnostic_expert,
            technical_researcher,
            parts_specialist,
            technical_writer,
            maintenance_planner
        ]

    def create_tasks(self, agents):
        # Tâche de Diagnostic
        diagnostic_task = Task(
            description=f"""
            Analyser les symptômes suivants et l'historique du véhicule :
            Symptômes : {self.context['symptoms']}
            Historique : {self.history}
            VIN : {self.context['vehicle']['vin']}
            
            1. Analyser les symptômes décrits
            2. Vérifier les rappels et bulletins de service
            3. Établir un diagnostic préliminaire
            """,
            agent=agents[0]
        )

        # Tâche de Recherche Technique
        research_task = Task(
            description=f"""
            Rechercher toute la documentation technique pertinente :
            Véhicule : {self.context['vehicle']['make']} {self.context['vehicle']['model']} {self.context['vehicle']['year']}
            Diagnostic : [Utiliser le résultat de la tâche précédente]
            
            1. Rechercher les procédures de réparation
            2. Identifier les bulletins techniques applicables
            3. Vérifier l'historique des rappels
            """,
            agent=agents[1]
        )

        # Tâche de Recherche de Pièces
        parts_task = Task(
            description="""
            Identifier et localiser toutes les pièces nécessaires :
            1. Rechercher les références des pièces
            2. Vérifier la disponibilité
            3. Identifier les fournisseurs les plus proches
            4. Comparer les prix et délais
            """,
            agent=agents[2]
        )

        # Tâche de Rédaction
        writing_task = Task(
            description="""
            Rédiger un bon de travail complet incluant :
            1. Diagnostic détaillé
            2. Procédures de réparation
            3. Liste des pièces nécessaires
            4. Estimation des coûts et délais
            5. Recommandations additionnelles
            """,
            agent=agents[3]
        )

        # Tâche de Planification
        planning_task = Task(
            description=f"""
            Planifier l'intervention de maintenance :
            Véhicule : {self.context['vehicle']['make']} {self.context['vehicle']['model']}
            Kilométrage : {self.context.get('mileage', 'Non spécifié')}
            
            1. Vérifier le programme de maintenance
            2. Identifier les interventions dues
            3. Optimiser le planning des travaux
            4. Proposer un calendrier d'intervention
            """,
            agent=agents[4]
        )

        return [
            diagnostic_task,
            research_task,
            parts_task,
            writing_task,
            planning_task
        ]

    def process_work_order(self):
        agents = self.create_agents()
        tasks = self.create_tasks(agents)

        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result