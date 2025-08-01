// src/api.js
const API_ROOT = window.API_ROOT || 'http://129.159.230.51:5000/api';

export function apiFetch(path, options = {}) {
  const token = localStorage.getItem('access_token');
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  if (token) headers['Authorization'] = 'Bearer ' + token;
  return fetch(`${API_ROOT}${path}`, {
    ...options,
    headers,
  }).then(async res => {
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw { ...data, status: res.status };
    return data;
  });
}