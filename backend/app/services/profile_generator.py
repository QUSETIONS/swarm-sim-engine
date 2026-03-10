class ProfileGenerator:
    def generate_profiles(self, entities: list) -> list:
        profiles = []
        for i, entity in enumerate(entities):
            profiles.append({
                "agent_id": i + 1,
                "username": f"{entity.get('name', 'user').lower()}_{str(i+1).zfill(3)}",
                "name": entity.get("name", "Unknown"),
                "persona": "Grounded in graph context",
                "bio": entity.get("summary", ""),
                "profession": "participant",
                "interested_topics": [],
                "stance_seed": 0.5
            })
        return profiles
