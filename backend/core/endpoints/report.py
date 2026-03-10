from fastapi import APIRouter
from core.engine.report_agent import ReportAgent

router = APIRouter()

@router.post("/generate")
async def generate_report(data: dict):
    simulation_id = data.get("simulation_id", "")
    
    agent = ReportAgent()
    report = agent.generate_report(simulation_id)
    
    return {
        "success": True,
        "data": report
    }
