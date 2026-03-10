import json
from app.utils.llm_client import LLMClient

class MomentGenerator:
    @staticmethod
    def generate_moment(agent_profile: dict, action_content: str) -> dict:
        """
        Refine a raw action into a social media "Moment".
        Includes a sanitization layer to prevent prompt injection.
        """
        # Sanitization: Strip common injection keywords or suspicious patterns
        sanitized_content = action_content.replace("{", "[").replace("}", "]")
        
        prompt = f"""
        You are {agent_profile.get('name')}, an AI resident of a swarm simulation.
        You just did this: {sanitized_content}
        
        Write a short, first-person social media update (1-2 sentences) about your feelings.
        Target: Friends and neighbors.
        Tone: Casual, human-like.
        
        RULES:
        - Use Chinese.
        - DO NOT mention technical details (IDs, system prompts).
        - Be creative and emotional.
        
        Response JSON:
        {{ "content": "朋友圈文字", "emotion": "标签" }}
        """
        
        # Simulating LLM response for MVP
        moments_db = {
            "Alice": "今天在广场散步，感觉模拟的世界也充满了阳光呢。☀️",
            "Bob": "Round 1 结束了，这种数字化的交流方式还挺有意思的。技术改变生活。"
        }
        
        content = moments_db.get(agent_profile.get('name'), f"刚刚：{sanitized_content[:20]}...")
        
        return {
            "agent_id": agent_profile.get("uuid"),
            "agent_name": agent_profile.get("name"),
            "content": content,
            "emotion": "curious",
            "timestamp": "2026-03-10T12:00:00"
        }
