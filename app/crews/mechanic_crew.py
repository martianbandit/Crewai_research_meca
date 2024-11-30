from typing import Dict, List, Optional
from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from app.tools.image_tools import DamageDetectionTool, TextExtractionTool, ReportGeneratorTool
from app.tools.diagnostic_tools import DTCAnalysisTool, CANBusMonitorTool, DiagnosticScanTool
from app.tools.compliance_tools import ComplianceCheckTool, RecallCheckTool, SafetyAuditTool
from app.tools.iot_tools import TelemetryMonitorTool, PredictiveAnalysisTool, SensorConfigTool
from app.tools.video_tools import VideoSearchTool, TranscriptionTool, ContentAnalysisTool

class MechanicCrew(CrewBase):
    """Équipe d'experts en mécanique de camions"""

    agents_config = str(Path(__file__).parent.parent.parent / "config" / "agents.yaml")

    def __init__(self, llm=None, verbose=False):
        """
        Initialise l'équipe avec tous les outils nécessaires
        
        Args:
            llm: Le modèle de langage à utiliser (optionnel)
            verbose: Active les logs détaillés (optionnel)
        """
        super().__init__()
        self.llm = llm
        self.verbose = verbose
        
        # Initialisation des outils
        self._init_tools()

    def _init_tools(self):
        """Initialise tous les outils nécessaires"""
        # Outils d'analyse d'images
        self.damage_detector = DamageDetectionTool()
        self.text_extractor = TextExtractionTool()
        self.report_generator = ReportGeneratorTool()
        
        # Outils de diagnostic
        self.dtc_analyzer = DTCAnalysisTool()
        self.canbus_monitor = CANBusMonitorTool()
        self.diagnostic_scanner = DiagnosticScanTool()
        
        # Outils de conformité
        self.compliance_checker = ComplianceCheckTool()
        self.recall_checker = RecallCheckTool()
        self.safety_auditor = SafetyAuditTool()
        
        # Outils IoT
        self.telemetry_monitor = TelemetryMonitorTool()
        self.predictive_analyzer = PredictiveAnalysisTool()
        self.sensor_configurator = SensorConfigTool()
        
        # Outils vidéo
        self.video_searcher = VideoSearchTool()
        self.video_transcriber = TranscriptionTool()
        self.content_analyzer = ContentAnalysisTool()

    @agent
    def image_expert(self) -> Agent:
        """Expert en analyse d'images"""
        return Agent(
            config=self.agents_config['image_analysis_expert'],
            tools=[
                self.damage_detector,
                self.text_extractor,
                self.report_generator
            ],
            llm=self.llm,
            verbose=self.verbose
        )

    @agent
    def compliance_officer(self) -> Agent:
        """Officier de conformité"""
        return Agent(
            config=self.agents_config['compliance_officer'],
            tools=[
                self.compliance_checker,
                self.recall_checker,
                self.safety_auditor
            ],
            llm=self.llm,
            verbose=self.verbose
        )

    @agent
    def safety_inspector(self) -> Agent:
        """Inspecteur sécurité"""
        return Agent(
            config=self.agents_config['safety_inspector'],
            tools=[self.safety_auditor],
            llm=self.llm,
            verbose=self.verbose
        )

    @agent
    def canbus_specialist(self) -> Agent:
        """Spécialiste CAN Bus"""
        return Agent(
            config=self.agents_config['canbus_specialist'],
            tools=[
                self.dtc_analyzer,
                self.canbus_monitor,
                self.diagnostic_scanner
            ],
            llm=self.llm,
            verbose=self.verbose
        )

    @agent
    def iot_engineer(self) -> Agent:
        """Ingénieur IoT"""
        return Agent(
            config=self.agents_config['iot_engineer'],
            tools=[
                self.telemetry_monitor,
                self.predictive_analyzer,
                self.sensor_configurator
            ],
            llm=self.llm,
            verbose=self.verbose
        )

    @agent
    def video_expert(self) -> Agent:
        """Expert vidéo"""
        return Agent(
            config=self.agents_config['video_transcriber'],
            tools=[
                self.video_searcher,
                self.video_transcriber,
                self.content_analyzer
            ],
            llm=self.llm,
            verbose=self.verbose
        )

    @task(description="Analyse des dommages du véhicule")
    def analyze_vehicle_damage(self, vehicle_id: str, images: List[bytes]) -> Task:
        return Task(
            agent=self.image_expert,
            expected_output="Rapport détaillé d'analyse des dommages",
            context={
                "vehicle_id": vehicle_id,
                "images": images
            }
        )

    @task(description="Vérification de la conformité")
    def check_compliance(self, vehicle_data: Dict) -> Task:
        return Task(
            agent=self.compliance_officer,
            expected_output="Rapport de conformité réglementaire",
            context=vehicle_data
        )

    @task(description="Analyse des codes d'erreur")
    def analyze_dtc_codes(self, vehicle_id: str, dtc_codes: List[str]) -> Task:
        return Task(
            agent=self.canbus_specialist,
            expected_output="Rapport d'analyse DTC avec recommandations",
            context={
                "vehicle_id": vehicle_id,
                "dtc_codes": dtc_codes
            }
        )

    @task(description="Surveillance de la télémétrie")
    def monitor_telemetry(self, vehicle_id: str) -> Task:
        return Task(
            agent=self.iot_engineer,
            expected_output="Rapport de télémétrie et recommandations",
            context={"vehicle_id": vehicle_id}
        )

    @task(description="Recherche de tutoriels")
    def find_repair_tutorials(self, repair_type: str) -> Task:
        return Task(
            agent=self.video_expert,
            expected_output="Liste de tutoriels analysés",
            context={"repair_type": repair_type}
        )

    @crew(process=Process.sequential)
    def inspect_vehicle(self, 
                       vehicle_id: str, 
                       images: List[bytes], 
                       dtc_codes: List[str]) -> Crew:
        """
        Inspection complète du véhicule
        
        Args:
            vehicle_id: Identifiant du véhicule
            images: Liste des images à analyser
            dtc_codes: Liste des codes DTC à analyser
            
        Returns:
            Crew: L'équipe configurée avec les tâches d'inspection
        """
        return Crew(
            agents=[
                self.image_expert,
                self.compliance_officer,
                self.canbus_specialist,
                self.iot_engineer,
                self.video_expert
            ],
            tasks=[
                self.analyze_vehicle_damage(vehicle_id, images),
                self.check_compliance({"id": vehicle_id}),
                self.analyze_dtc_codes(vehicle_id, dtc_codes),
                self.monitor_telemetry(vehicle_id)
            ],
            verbose=self.verbose
        )
