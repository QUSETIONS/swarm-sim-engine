import { api } from './graph'

export const generateProfiles = (entities: any[]) => {
    return api.post('/simulation/profiles/generate', { entities })
}

export const generateConfig = (data: any) => {
    return api.post('/simulation/config/generate', data)
}

export const startSimulation = (simulationId: string) => {
    return api.post('/simulation/start', { simulation_id: simulationId })
}

export const interviewAgent = (agentId: string, message: string) => {
    return api.post('/simulation/interview', { agent_id: agentId, message })
}

let activeSocket: WebSocket | null = null;
let messageListeners: ((data: any) => void)[] = [];

export const connectSimulationLogStream = (
    simulationId: string,
    onMessage: (data: any) => void,
    onClose?: () => void
) => {
    messageListeners.push(onMessage);

    if (activeSocket && activeSocket.readyState === WebSocket.OPEN) {
        return activeSocket; // Already connected
    }

    if (activeSocket) {
        activeSocket.close();
    }

    const isDevMode = window.location.port === '5173' || window.location.port === '5174';
    const backendHost = isDevMode ? '127.0.0.1:5000' : window.location.host;
    const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const wsUrl = `${wsProtocol}://${backendHost}/api/ws/simulation/${simulationId}`;
    activeSocket = new WebSocket(wsUrl);

    activeSocket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            messageListeners.forEach(cb => cb(data));
        } catch (e) {
            console.error("WS Parse Error", e);
        }
    };

    activeSocket.onclose = () => {
        console.log("WebSocket disconnected.");
        if (onClose) onClose();
    };

    return activeSocket;
};

export const closeSimulationLogStream = (onMessageToRemove?: (data: any) => void) => {
    if (onMessageToRemove) {
        messageListeners = messageListeners.filter(cb => cb !== onMessageToRemove);
    }

    if (messageListeners.length === 0 && activeSocket) {
        activeSocket.close();
        activeSocket = null;
    }
};
