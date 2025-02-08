import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

export const analyzeDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/analyze', formData);
    return response.data;
  } catch (error) {
    console.error('Error analyzing document:', error);
    if (error.response) {
      // Backend'den gelen hata mesajını kullan
      throw new Error(error.response.data.detail || 'Bir hata oluştu');
    } else if (error.request) {
      // İstek yapıldı ama yanıt alınamadı
      throw new Error('Sunucuya bağlanılamadı');
    } else {
      // İstek oluşturulurken hata oluştu
      throw new Error('İstek oluşturulurken bir hata oluştu');
    }
  }
}; 