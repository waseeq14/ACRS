import axios from 'axios';

const getCSRFToken = () => {
  const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
  return csrfToken ? csrfToken[1] : null;
};

const api = axios.create({
  baseURL: `${process.env.REACT_APP_BACKEND_URL}`,
  withCredentials: true,
});

// Intercept requests to add CSRF token
api.interceptors.request.use((config) => {
  const csrfToken = getCSRFToken();
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

export default api;