import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const useApi = () => {
    const createPlan = async (data) => {
        const response = await api.post('/create-plan', data);
        return response.data;
    };

    const getDailyTask = async (planId, day) => {
        const response = await api.get(`/daily-task?plan_id=${planId}&day=${day}`);
        return response.data;
    };

    const submitAnswer = async (data) => {
        const response = await api.post('/submit-answer', data);
        return response.data;
    };

    const getReadiness = async (planId) => {
        const response = await api.get(`/readiness?plan_id=${planId}`);
        return response.data;
    };

    return {
        createPlan,
        getDailyTask,
        submitAnswer,
        getReadiness,
    };
};
