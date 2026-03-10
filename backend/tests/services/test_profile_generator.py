from core.engine.profile_generator import ProfileGenerator

def test_profile_generator_maps_entities_to_agents():
    entities = [{"uuid": "1", "name": "Alice", "labels": ["Person"], "summary": "student"}]
    profiles = ProfileGenerator().generate_profiles(entities)
    assert profiles[0]["username"] == "alice_001"
    assert profiles[0]["persona"]
