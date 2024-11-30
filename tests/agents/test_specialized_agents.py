import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from app.agents.specialized_agents import (
    ImageAnalysisExpert,
    ComplianceOfficer,
    SafetyInspector,
    CanBusSpecialist,
    IoTEngineer,
    VideoTranscriber,
    SpecializedCrew
)

@pytest.fixture
def mock_image_manager():
    manager = Mock()
    manager.analyze_damage.return_value = {
        "damages_detected": 2,
        "damage_areas": [
            {"severity": "high", "location": "front_bumper"},
            {"severity": "medium", "location": "hood"}
        ]
    }
    return manager

@pytest.fixture
def mock_compliance_tools():
    tools = Mock()
    tools.check_vehicle_compliance.return_value = {
        "fmcsa_compliant": True,
        "dot_compliant": True,
        "active_recalls": [],
        "issues": [],
        "safety_concerns": []
    }
    return tools

@pytest.fixture
def mock_canbus_tools():
    tools = Mock()
    tools.interpret_dtc_codes.return_value = {
        "codes_analyzed": 2,
        "repair_needed": True,
        "severity_level": "high",
        "repair_type": "engine"
    }
    return tools

@pytest.fixture
def mock_iot_tools():
    tools = Mock()
    tools.process_telemetry.return_value = {
        "sensor_data": {"temperature": 80, "pressure": 35},
        "alerts": [],
        "maintenance_recommendations": ["oil_change"]
    }
    return tools

@pytest.fixture
def mock_video_tools():
    tools = Mock()
    tools.search_repair_videos.return_value = [
        {
            "title": "Engine Repair Tutorial",
            "url": "https://youtube.com/watch?v=123",
            "duration": "10:30",
            "analysis": {
                "difficulty_level": "medium",
                "tools_needed": ["wrench", "diagnostic_tool"]
            }
        }
    ]
    return tools

@pytest.mark.asyncio
async def test_image_analysis_expert(mock_image_manager):
    expert = ImageAnalysisExpert(mock_image_manager)
    images = [b"test_image_data"]
    result = await expert.analyze_repair_images("WO123", images)
    
    assert "work_order_id" in result
    assert "analyses" in result
    assert len(result["analyses"]) == 1
    assert result["analyses"][0]["damages_detected"] == 2

@pytest.mark.asyncio
async def test_compliance_officer(mock_compliance_tools):
    officer = ComplianceOfficer(mock_compliance_tools)
    vehicle_data = {"vehicle_id": "V123", "vin": "1HGCM82633A123456"}
    result = await officer.verify_compliance(vehicle_data)
    
    assert result["fmcsa_compliant"]
    assert result["dot_compliant"]
    assert len(result["active_recalls"]) == 0

@pytest.mark.asyncio
async def test_canbus_specialist(mock_canbus_tools):
    specialist = CanBusSpecialist(mock_canbus_tools)
    dtc_codes = ["P0123", "P0456"]
    result = await specialist.analyze_dtc_codes(dtc_codes)
    
    assert result["codes_analyzed"] == 2
    assert result["repair_needed"]
    assert result["severity_level"] == "high"

@pytest.mark.asyncio
async def test_iot_engineer(mock_iot_tools):
    engineer = IoTEngineer(mock_iot_tools)
    result = await engineer.process_telemetry("V123")
    
    assert "sensor_data" in result
    assert "temperature" in result["sensor_data"]
    assert "maintenance_recommendations" in result
    assert "oil_change" in result["maintenance_recommendations"]

@pytest.mark.asyncio
async def test_video_transcriber(mock_video_tools):
    transcriber = VideoTranscriber(mock_video_tools)
    result = await transcriber.search_relevant_videos("engine_repair")
    
    assert len(result) == 1
    assert "Engine Repair Tutorial" in result[0]["title"]
    assert "difficulty_level" in result[0]["analysis"]

@pytest.mark.asyncio
async def test_specialized_crew_comprehensive_inspection(
    mock_image_manager,
    mock_compliance_tools,
    mock_canbus_tools,
    mock_iot_tools,
    mock_video_tools
):
    crew = SpecializedCrew(
        mock_image_manager,
        mock_compliance_tools,
        Mock(),  # safety_tools
        mock_canbus_tools,
        mock_iot_tools,
        mock_video_tools
    )
    
    result = await crew.process_comprehensive_inspection(
        vehicle_id="V123",
        images=[b"test_image_data"],
        dtc_codes=["P0123"]
    )
    
    assert "vehicle_id" in result
    assert "image_analysis" in result
    assert "compliance_status" in result
    assert "dtc_analysis" in result
    assert "telemetry_data" in result
    assert "relevant_videos" in result
    assert "recommendations" in result

@pytest.mark.asyncio
async def test_error_handling():
    # Test avec un gestionnaire d'images défectueux
    broken_manager = Mock()
    broken_manager.analyze_damage.side_effect = Exception("API Error")
    
    expert = ImageAnalysisExpert(broken_manager)
    
    with pytest.raises(Exception) as exc_info:
        await expert.analyze_repair_images("WO123", [b"test_image"])
    
    assert "API Error" in str(exc_info.value)

@pytest.mark.asyncio
async def test_empty_data_handling(mock_image_manager, mock_canbus_tools):
    # Test avec des données vides
    expert = ImageAnalysisExpert(mock_image_manager)
    result = await expert.analyze_repair_images("WO123", [])
    assert len(result["analyses"]) == 0
    
    specialist = CanBusSpecialist(mock_canbus_tools)
    result = await specialist.analyze_dtc_codes([])
    assert result["codes_analyzed"] == 0
