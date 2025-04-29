import axios from 'axios';

const getCSRFToken = () => {
  const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
  return csrfToken ? csrfToken[1] : null;
};

const api = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_URL}`,
  withCredentials: true,
});

const fetchCSRFToken = async () => {
  const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/get-csrf-token`, { withCredentials: true} );
  return response.data.csrfToken;
};

// Intercept requests to add CSRF token
api.interceptors.request.use(async (config) => {
  // const csrfToken = getCSRFToken();
  const csrfToken = await fetchCSRFToken();
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

export default api;