from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Maps simulation_id to a list of connected WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, simulation_id: str):
        await websocket.accept()
        if simulation_id not in self.active_connections:
            self.active_connections[simulation_id] = []
        self.active_connections[simulation_id].append(websocket)
        logger.info(f"WebSocket connected for simulation {simulation_id}")

    def disconnect(self, websocket: WebSocket, simulation_id: str):
        if simulation_id in self.active_connections:
            self.active_connections[simulation_id].remove(websocket)
            if not self.active_connections[simulation_id]:
                del self.active_connections[simulation_id]
        logger.info(f"WebSocket disconnected from simulation {simulation_id}")

    async def broadcast_to_simulation(self, simulation_id: str, message: dict):
        if simulation_id in self.active_connections:
            # We want to gracefully handle broken dead connections
            disconnected = []
            for connection in self.active_connections[simulation_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except Exception as e:
                    logger.warning(f"Failed to send WS message: {e}")
                    disconnected.append(connection)
            
            for d in disconnected:
                self.disconnect(d, simulation_id)

manager = ConnectionManager()

@router.websocket("/{simulation_id}")
async def websocket_endpoint(websocket: WebSocket, simulation_id: str):
    await manager.connect(websocket, simulation_id)
    try:
        while True:
            # We don't really expect client to send us commands right now, 
            # but we keep the loop alive.
            data = await websocket.receive_text()
            # If client sends ping or arbitrary data, just ignore for now.
    except WebSocketDisconnect:
        manager.disconnect(websocket, simulation_id)
