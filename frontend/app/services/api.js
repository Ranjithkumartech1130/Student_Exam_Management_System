import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const login = (username, password) => api.post('/admin/login/', { username, password });
export const getRooms = () => api.get('/admin/rooms/');
export const addRoom = (room_number, capacity) => api.post('/admin/rooms/add/', { room_number, capacity });
export const toggleRoom = (id) => api.post(`/admin/rooms/${id}/toggle/`);
export const uploadCSV = (formData) => api.post('/admin/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
});
export const generateSeating = () => api.post('/admin/generate-seating/');
export const refreshAllocation = () => api.post('/admin/refresh-allocation/');
export const getRecords = () => api.get('/admin/records/');


export const studentLogin = (register_no, date_of_birth) => api.post('/student/login/', { register_no, date_of_birth });
export const defaultParams = {};

export default api;
