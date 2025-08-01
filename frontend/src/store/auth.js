import { reactive, readonly } from 'vue'
import { jwtDecode } from 'jwt-decode'

const state = reactive({
  user: null,
  token: null,
})

function login(token) {
  try {
    const decoded = jwtDecode(token)
    state.user = {
      id: decoded.sub,
      role: decoded.role,
      // email and name are not in the token, will be fetched separately
    }
    state.token = token
    localStorage.setItem('access_token', token)
  } catch (e) {
    console.error('Invalid token', e)
    logout()
  }
}

function logout() {
  state.user = null
  state.token = null
  localStorage.removeItem('access_token')
  // Redirect to login page
  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}

// Check for existing token on startup
const token = localStorage.getItem('access_token')
if (token) {
  login(token)
}

export const auth = readonly({
  state,
  login,
  logout,
})