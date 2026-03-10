import { api } from './graph'

export const generateReport = (simulationId: string) => {
    return api.post('/report/generate', { simulation_id: simulationId })
}
