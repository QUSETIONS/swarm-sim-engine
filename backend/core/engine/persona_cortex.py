from core.utils.llm_client import LLMClient
from core.engine.memory_retriever import RetrievalTools
import random

class AgentLogic:
    @staticmethod
    def generate_action(simulation_id: str, project_id: str, agent_profile: dict, base_context: str) -> dict:
        """
        Generate an agent action using a real LLM, augmented by memory retrieval.
        """
        
        recent_memory = RetrievalTools.query_logs(simulation_id, project_id, agent_profile.get("uuid"))
        
        system_prompt = f"""
        You are an elite autonomous agent operating within a complex simulation engine.
        Your Name: {agent_profile.get('name')}
        Your Role/Personality: {agent_profile.get('summary')}
        
        Current Simulation State: {base_context}
        
        --- Your Recent Memory & Cognitive Graph ---
        {recent_memory}
        --------------------------------------------
        
        # OPERATING FRAMEWORK (OODA Loop):
        1. Observe: Analyze your memories and the current state.
        2. Orient: Align your observations with your specific Role/Personality.
        3. Decide: Formulate a strategy. Will you communicate (reply), act autonomously (post), or execute code (execute_python)?
        4. Act: Formulate your final response.
        
        Rules for Roles:
        - 'Coordinator' or 'Leader': Assign tasks and guide strategy via 'reply'.
        - 'Specialist' or 'Analyst': Perform deep execution/analysis via tools and report back.
        
        Available Tools:
        If you need to verify a vulnerability or write code, specify it in 'tool_call'.
        - "execute_python": params: {{"script": "valid python script to run in isolated docker sandbox. E.g. print('test')"}}
        
        Decide your *very next* action. 
        Output MUST be valid, strictly formatted JSON matching this schema exactly. NO markdown wrappers, NO extra text:
        {{
            "action": "post" or "reply",
            "content": "a short text indicating what you are doing or saying",
            "thought": "Your OODA loop inner monologue: [Observe]... [Orient]... [Decide]...",
            "target_id": "ID of another agent if replying, or 'none'",
            "tool_call": {{ "name": "tool_name", "params": {{ "key": "value" }} }}, // Optional, return null if no tool needed
            "metadata": {{
                "location": "Plaza|Cafe|Library|Park|Home", // Or specific target module if in execution mode
                "emotion": "your current mood"
            }}
        }}
        """
        
        user_prompt = "What is your next action in the town?"
        
        client = LLMClient()
        llm_response = client.generate_json(system_prompt, user_prompt)
        
        # Ensure fallback sanity
        target_id = llm_response.get("target_id", "none")
        if target_id == "none" or target_id == agent_profile.get("uuid"):
             target_id = None
             
        # Pick a target randomly if LLM fails to specify a distinct one but wants to reply
        if llm_response.get("action") == "reply" and not target_id:
             all_ids = ["1", "2", "3", "4", "5"]
             all_ids = [uid for uid in all_ids if uid != agent_profile.get("uuid")]
             if all_ids:
                 target_id = random.choice(all_ids)
                 
        content = llm_response.get("content", f"Just observing the {llm_response.get('metadata', {}).get('location', 'town')}.")
        
        # Execute Sandbox Tool if requested
        tool_call = llm_response.get("tool_call")
        if tool_call and isinstance(tool_call, dict) and tool_call.get("name"):
            from core.engine.sandbox_tool import SandboxTool
            tool_result = SandboxTool.execute(tool_call.get("name"), tool_call.get("params", {}))
            content += f"\n\n{tool_result}"
        
        return {
            "agent_id": agent_profile.get("uuid"),
            "agent_name": agent_profile.get("name"),
            "action": llm_response.get("action", "post"),
            "content": content,
            "thought": llm_response.get("thought", "Maybe I should take a walk."),
            "target_id": target_id,
            "metadata": llm_response.get("metadata", { "location": "Plaza", "emotion": "neutral" })
        }
