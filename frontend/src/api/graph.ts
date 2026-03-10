import axios from 'axios'

export const api = axios.create({ baseURL: '/api' })

export const generateOntology = (files: File[], requirement: string) => {
    const formData = new FormData()
    files.forEach(f => formData.append('files', f))
    formData.append('simulation_requirement', requirement)
    return api.post('/graph/ontology/generate', formData)
}

export const buildGraph = (projectId: string) => {
    return api.post('/graph/build', { project_id: projectId })
}
