from typing import List, Dict, Optional
from crewai import Agent
from app.utils.image_manager import ImageManager
from app.utils.tools import (
    NHTSATools, 
    CanBusTools, 
    IoTTools, 
    VideoTools,
    ComplianceTools,
    SafetyTools
)

class ImageAnalysisExpert(Agent):
    """Expert en analyse d'images pour l'inspection des véhicules"""
    
    def __init__(self, image_manager: ImageManager, **kwargs):
        super().__init__(
            name="Expert Analyse d'Images",
            goal="Analyser les images de véhicules pour détecter les anomalies et documenter les réparations",
            backstory="""Expert en analyse d'images avec une spécialisation en vision par ordinateur 
            et reconnaissance de dommages sur les véhicules lourds. Plus de 10 ans d'expérience en 
            inspection visuelle assistée par IA."""
        )
        self.image_manager = image_manager

    async def analyze_repair_images(self, work_order_id: str, images: List[bytes]) -> Dict:
        """Analyse les images d'une réparation"""
        results = []
        for img in images:
            analysis = await self.image_manager.analyze_damage(img)
            results.append(analysis)
        return {
            "work_order_id": work_order_id,
            "analyses": results
        }

class ComplianceOfficer(Agent):
    """Agent responsable de la conformité réglementaire"""
    
    def __init__(self, compliance_tools: ComplianceTools, **kwargs):
        super().__init__(
            name="Officier de Conformité",
            goal="Assurer la conformité avec les réglementations gouvernementales",
            backstory="""Expert en réglementation du transport routier avec une connaissance 
            approfondie des normes FMCSA, DOT, et des réglementations internationales."""
        )
        self.compliance_tools = compliance_tools

    async def verify_compliance(self, vehicle_data: Dict) -> Dict:
        """Vérifie la conformité d'un véhicule"""
        return await self.compliance_tools.check_vehicle_compliance(vehicle_data)

class SafetyInspector(Agent):
    """Inspecteur de sécurité et santé"""
    
    def __init__(self, safety_tools: SafetyTools, **kwargs):
        super().__init__(
            name="Inspecteur Sécurité",
            goal="Évaluer et assurer la sécurité des opérations",
            backstory="""Professionnel de la sécurité certifié avec expertise en prévention 
            des accidents et conformité OSHA pour l'industrie du transport."""
        )
        self.safety_tools = safety_tools

    async def perform_safety_audit(self, workplace_data: Dict) -> Dict:
        """Effectue un audit de sécurité"""
        return await self.safety_tools.conduct_safety_audit(workplace_data)

class CanBusSpecialist(Agent):
    """Spécialiste en diagnostic CAN Bus et DTC"""
    
    def __init__(self, canbus_tools: CanBusTools, **kwargs):
        super().__init__(
            name="Spécialiste CAN Bus",
            goal="Analyser et interpréter les données CAN Bus et codes d'erreur",
            backstory="""Expert en systèmes électroniques embarqués avec spécialisation 
            en protocoles CAN, diagnostic OBD et interprétation DTC."""
        )
        self.canbus_tools = canbus_tools

    async def analyze_dtc_codes(self, dtc_data: List[str]) -> Dict:
        """Analyse les codes d'erreur DTC"""
        return await self.canbus_tools.interpret_dtc_codes(dtc_data)

    async def monitor_canbus(self, vehicle_id: str) -> Dict:
        """Surveille les données CAN Bus en temps réel"""
        return await self.canbus_tools.monitor_canbus_data(vehicle_id)

class IoTEngineer(Agent):
    """Ingénieur IoT pour la télémétrie des véhicules"""
    
    def __init__(self, iot_tools: IoTTools, **kwargs):
        super().__init__(
            name="Ingénieur IoT",
            goal="Gérer et analyser les données IoT des véhicules",
            backstory="""Spécialiste en IoT industriel avec expertise en télémétrie 
            véhiculaire et analyse de données en temps réel."""
        )
        self.iot_tools = iot_tools

    async def process_telemetry(self, vehicle_id: str) -> Dict:
        """Traite les données de télémétrie"""
        return await self.iot_tools.process_vehicle_telemetry(vehicle_id)

    async def configure_sensors(self, vehicle_id: str, config: Dict) -> bool:
        """Configure les capteurs IoT"""
        return await self.iot_tools.configure_vehicle_sensors(vehicle_id, config)

class VideoTranscriber(Agent):
    """Expert en transcription et analyse de vidéos YouTube"""
    
    def __init__(self, video_tools: VideoTools, **kwargs):
        super().__init__(
            name="Expert Vidéo",
            goal="Extraire et analyser le contenu des vidéos techniques",
            backstory="""Spécialiste en analyse de contenu vidéo avec expertise 
            en extraction d'informations techniques et tutoriels de réparation."""
        )
        self.video_tools = video_tools

    async def process_tutorial(self, video_url: str) -> Dict:
        """Traite un tutoriel vidéo"""
        transcript = await self.video_tools.get_video_transcript(video_url)
        analysis = await self.video_tools.analyze_tutorial_content(transcript)
        return {
            "url": video_url,
            "transcript": transcript,
            "analysis": analysis,
            "key_points": analysis["key_points"],
            "tools_needed": analysis["tools_needed"],
            "difficulty_level": analysis["difficulty_level"]
        }

    async def search_relevant_videos(self, repair_type: str) -> List[Dict]:
        """Recherche des vidéos pertinentes"""
        return await self.video_tools.search_repair_videos(repair_type)

# Création d'une équipe spécialisée
class SpecializedCrew:
    """Équipe d'agents spécialisés"""
    
    def __init__(self, 
                 image_manager: ImageManager,
                 compliance_tools: ComplianceTools,
                 safety_tools: SafetyTools,
                 canbus_tools: CanBusTools,
                 iot_tools: IoTTools,
                 video_tools: VideoTools):
        self.image_expert = ImageAnalysisExpert(image_manager)
        self.compliance_officer = ComplianceOfficer(compliance_tools)
        self.safety_inspector = SafetyInspector(safety_tools)
        self.canbus_specialist = CanBusSpecialist(canbus_tools)
        self.iot_engineer = IoTEngineer(iot_tools)
        self.video_expert = VideoTranscriber(video_tools)

    async def process_comprehensive_inspection(self, 
                                            vehicle_id: str, 
                                            images: List[bytes],
                                            dtc_codes: List[str]) -> Dict:
        """Effectue une inspection complète avec tous les agents"""
        
        # Analyse des images
        image_analysis = await self.image_expert.analyze_repair_images(
            vehicle_id, images
        )

        # Vérification de la conformité
        compliance_check = await self.compliance_officer.verify_compliance({
            "vehicle_id": vehicle_id,
            "inspection_data": image_analysis
        })

        # Analyse DTC
        dtc_analysis = await self.canbus_specialist.analyze_dtc_codes(dtc_codes)

        # Données IoT
        telemetry = await self.iot_engineer.process_telemetry(vehicle_id)

        # Recherche de vidéos pertinentes
        if dtc_analysis["repair_needed"]:
            repair_videos = await self.video_expert.search_relevant_videos(
                dtc_analysis["repair_type"]
            )
        else:
            repair_videos = []

        return {
            "vehicle_id": vehicle_id,
            "timestamp": datetime.now().isoformat(),
            "image_analysis": image_analysis,
            "compliance_status": compliance_check,
            "dtc_analysis": dtc_analysis,
            "telemetry_data": telemetry,
            "relevant_videos": repair_videos,
            "recommendations": {
                "repairs_needed": dtc_analysis["repair_needed"],
                "compliance_issues": compliance_check["issues"],
                "safety_concerns": compliance_check["safety_concerns"],
                "maintenance_schedule": telemetry["maintenance_recommendations"]
            }
        }
