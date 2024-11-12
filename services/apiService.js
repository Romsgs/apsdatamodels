const axios = require('axios');
require('dotenv').config();

const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;

const getAccessToken = async () => {
  const url = 'https://developer.api.autodesk.com/authentication/v2/token';
  const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
  const data = new URLSearchParams({
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    grant_type: 'client_credentials',
    scope: 'data:read data:write data:create data:search',
  });

  try {
    const response = await axios.post(url, data, { headers });
    const accessToken = response.data.access_token;
    console.log('Token de acesso obtido com sucesso.');
    return accessToken;
  } catch (error) {
    console.error('Falha ao obter o token de acesso.');
    console.error('Erro:', error.response ? error.response.data : error.message);
    return null;
  }
};

const getProjects = async () => {
  try {
    const accessToken = await getAccessToken();
    if (!accessToken) {
      throw new Error('Não foi possível obter o token de acesso.');
    }

    const api = axios.create({
      baseURL: 'https://developer.api.autodesk.com/',
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    const response = await api.get('project/v1/hubs');
    const projects = response.data.data.map((hub) => ({
      id: hub.id,
      name: hub.attributes.name,
      // Adicione outros campos conforme necessário
    }));
    return projects;
  } catch (error) {
    console.error('Erro ao obter projetos:', error.message);
    return [];
  }
};

module.exports = {
  getAccessToken,
  getProjects,
};
