import asyncio
from datetime import datetime
from app.agents.specialized_agents import SpecializedCrew
from app.utils.image_manager import ImageManager
from app.utils.specialized_tools import (
    ComplianceTools,
    SafetyTools,
    CanBusTools,
    IoTTools,
    VideoTools
)

async def example_image_analysis():
    """Exemple d'analyse d'image de dommages"""
    print("\n=== Exemple d'Analyse d'Image ===")
    
    # Configuration
    image_manager = ImageManager(supabase_url="YOUR_URL", supabase_key="YOUR_KEY")
    
    # Chargement d'une image de test
    with open("examples/data/damage_photo.jpg", "rb") as f:
        image_data = f.read()
    
    # Création de l'expert en analyse d'images
    expert = ImageAnalysisExpert(image_manager)
    
    # Analyse des dommages
    result = await expert.analyze_repair_images(
        work_order_id="WO_TEST_001",
        images=[image_data]
    )
    
    print("Résultats de l'analyse :")
    print(f"- Nombre de dommages détectés : {result['analyses'][0]['damages_detected']}")
    for damage in result['analyses'][0]['damage_areas']:
        print(f"- Dommage {damage['severity']} détecté à : {damage['location']}")

async def example_compliance_check():
    """Exemple de vérification de conformité"""
    print("\n=== Exemple de Vérification de Conformité ===")
    
    # Configuration
    compliance_tools = ComplianceTools(api_key="YOUR_API_KEY")
    
    # Création de l'agent de conformité
    officer = ComplianceOfficer(compliance_tools)
    
    # Données du véhicule
    vehicle_data = {
        "vehicle_id": "TRUCK_001",
        "vin": "1HGCM82633A123456",
        "make": "Freightliner",
        "model": "Cascadia",
        "year": 2020
    }
    
    # Vérification de la conformité
    result = await officer.verify_compliance(vehicle_data)
    
    print("Résultats de la vérification :")
    print(f"- FMCSA conforme : {result['fmcsa_compliant']}")
    print(f"- DOT conforme : {result['dot_compliant']}")
    if result['active_recalls']:
        print("Rappels actifs :")
        for recall in result['active_recalls']:
            print(f"  - {recall}")
    else:
        print("Aucun rappel actif")

async def example_canbus_analysis():
    """Exemple d'analyse CAN Bus"""
    print("\n=== Exemple d'Analyse CAN Bus ===")
    
    # Configuration
    canbus_tools = CanBusTools()
    
    # Création du spécialiste CAN Bus
    specialist = CanBusSpecialist(canbus_tools)
    
    # Codes DTC d'exemple
    dtc_codes = ["P0123", "P0456", "P1234"]
    
    # Analyse des codes
    result = await specialist.analyze_dtc_codes(dtc_codes)
    
    print("Résultats de l'analyse DTC :")
    print(f"- Codes analysés : {result['codes_analyzed']}")
    print(f"- Réparation nécessaire : {result['repair_needed']}")
    print(f"- Niveau de sévérité : {result['severity_level']}")
    
    # Surveillance CAN Bus en temps réel
    canbus_data = await specialist.monitor_canbus("TRUCK_001")
    print("\nDonnées CAN Bus en temps réel :")
    print(f"- Messages reçus : {canbus_data['message_count']}")

async def example_iot_monitoring():
    """Exemple de surveillance IoT"""
    print("\n=== Exemple de Surveillance IoT ===")
    
    # Configuration
    iot_tools = IoTTools(mqtt_broker="localhost", mqtt_port=1883)
    
    # Création de l'ingénieur IoT
    engineer = IoTEngineer(iot_tools)
    
    # Traitement de la télémétrie
    result = await engineer.process_telemetry("TRUCK_001")
    
    print("Données de télémétrie :")
    print(f"- Température : {result['sensor_data']['temperature']}°C")
    print(f"- Pression : {result['sensor_data']['pressure']} PSI")
    
    if result['alerts']:
        print("\nAlertes :")
        for alert in result['alerts']:
            print(f"- {alert}")
    
    print("\nRecommandations de maintenance :")
    for rec in result['maintenance_recommendations']:
        print(f"- {rec}")

async def example_video_analysis():
    """Exemple d'analyse de tutoriels vidéo"""
    print("\n=== Exemple d'Analyse Vidéo ===")
    
    # Configuration
    video_tools = VideoTools()
    
    # Création de l'expert vidéo
    expert = VideoTranscriber(video_tools)
    
    # Recherche de vidéos
    videos = await expert.search_relevant_videos("engine_repair_cascadia")
    
    print("Vidéos pertinentes trouvées :")
    for video in videos:
        print(f"\nTitre : {video['title']}")
        print(f"URL : {video['url']}")
        print(f"Durée : {video['duration']}")
        print(f"Niveau de difficulté : {video['analysis']['difficulty_level']}")
        print("Outils nécessaires :")
        for tool in video['analysis']['tools_needed']:
            print(f"- {tool}")

async def example_comprehensive_inspection():
    """Exemple d'inspection complète avec tous les agents"""
    print("\n=== Exemple d'Inspection Complète ===")
    
    # Configuration de tous les outils
    image_manager = ImageManager(supabase_url="YOUR_URL", supabase_key="YOUR_KEY")
    compliance_tools = ComplianceTools(api_key="YOUR_API_KEY")
    safety_tools = SafetyTools()
    canbus_tools = CanBusTools()
    iot_tools = IoTTools(mqtt_broker="localhost", mqtt_port=1883)
    video_tools = VideoTools()
    
    # Création de l'équipe spécialisée
    crew = SpecializedCrew(
        image_manager,
        compliance_tools,
        safety_tools,
        canbus_tools,
        iot_tools,
        video_tools
    )
    
    # Chargement des données de test
    with open("examples/data/damage_photo.jpg", "rb") as f:
        image_data = f.read()
    
    # Exécution de l'inspection complète
    result = await crew.process_comprehensive_inspection(
        vehicle_id="TRUCK_001",
        images=[image_data],
        dtc_codes=["P0123", "P0456"]
    )
    
    print("Résultats de l'inspection complète :")
    print("\nAnalyse d'images :")
    for analysis in result['image_analysis']['analyses']:
        print(f"- {analysis['damages_detected']} dommages détectés")
    
    print("\nStatut de conformité :")
    print(f"- FMCSA : {result['compliance_status']['fmcsa_compliant']}")
    print(f"- DOT : {result['compliance_status']['dot_compliant']}")
    
    print("\nAnalyse DTC :")
    print(f"- Sévérité : {result['dtc_analysis']['severity_level']}")
    print(f"- Réparation nécessaire : {result['dtc_analysis']['repair_needed']}")
    
    print("\nDonnées de télémétrie :")
    for key, value in result['telemetry_data']['sensor_data'].items():
        print(f"- {key}: {value}")
    
    print("\nVidéos pertinentes trouvées :")
    for video in result['relevant_videos']:
        print(f"- {video['title']}")
    
    print("\nRecommandations :")
    for key, value in result['recommendations'].items():
        print(f"- {key}: {value}")

async def main():
    """Exécution de tous les exemples"""
    try:
        await example_image_analysis()
        await example_compliance_check()
        await example_canbus_analysis()
        await example_iot_monitoring()
        await example_video_analysis()
        await example_comprehensive_inspection()
    except Exception as e:
        print(f"Erreur lors de l'exécution des exemples : {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
