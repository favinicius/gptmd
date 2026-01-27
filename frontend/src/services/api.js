import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const analyzeInstruction = async (instruction, files) => {
    const formData = new FormData();
    formData.append('instruction', instruction);
    if (files) {
        files.forEach(file => {
            formData.append('files', file);
        });
    }
    const response = await api.post('/analyze', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
};

export const planLogistics = async (intent) => {
    const response = await api.post('/plan-logistics', intent);
    return response.data;
};

export const calculatePricing = async (intent) => {
    const response = await api.post('/pricing', intent);
    return response.data;
};

export const generateRedaction = async (intent, proposal) => {
    const response = await api.post('/redaction', { intent, proposal });
    return response.data;
};

export const assembleProposal = async (intent, proposal, textBlocks) => {
    const response = await api.post('/assemble', { intent, proposal, textBlocks });
    return response.data;
};

// --- CRUD Registers ---
export const getHardware = async (params = {}) => {
    const response = await api.get('/registers/hardware', { params });
    return response.data;
};

export const createHardware = async (item) => {
    const response = await api.post('/registers/hardware', item);
    return response.data;
};

export const updateHardware = async (id, item) => {
    const response = await api.put(`/registers/hardware/${id}`, item);
    return response.data;
};

export const deleteHardware = async (id) => {
    const response = await api.delete(`/registers/hardware/${id}`);
    return response.data;
};

export const getRoles = async () => {
    const response = await api.get('/registers/labor/roles');
    return response.data;
};

export const getActivities = async (params = {}) => {
    const response = await api.get('/registers/labor/activities', { params });
    return response.data;
};

export const getLogistics = async () => {
    const response = await api.get('/registers/logistics');
    return response.data;
};

export default api;
