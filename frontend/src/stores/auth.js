import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('trackerUser')) || null)
  const authError = ref('')
  const selectedCompany = ref(localStorage.getItem('adminSelectedCompany') || 'CallHealth')

  function setSelectedCompany(company) {
    selectedCompany.value = company
    localStorage.setItem('adminSelectedCompany', company)
  }

  async function login(rollNumber, password) {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rollNumber, password })
      })
      if (res.ok) {
        const data = await res.json()
        user.value = data
        localStorage.setItem('trackerUser', JSON.stringify(data))
        authError.value = ''
        return true
      } else {
        authError.value = 'Invalid roll number or password.'
        return false
      }
    } catch (err) {
      authError.value = 'Network error.'
      return false
    }
  }

  async function register(userData) {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      })
      if (res.ok) {
        const data = await res.json()
        user.value = data
        localStorage.setItem('trackerUser', JSON.stringify(data))
        authError.value = ''
        return true
      } else {
        const errData = await res.json().catch(() => ({}))
        authError.value = errData.detail || 'Roll number already exists or invalid data.'
        return false
      }
    } catch (err) {
      authError.value = 'Network error.'
      return false
    }
  }

  async function adminLogin(username, password) {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/admin-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      if (res.ok) {
        const data = await res.json()
        user.value = data
        localStorage.setItem('trackerUser', JSON.stringify(data))
        authError.value = ''
        return true
      } else {
        authError.value = 'Invalid username or password.'
        return false
      }
    } catch (err) {
      authError.value = 'Network error.'
      return false
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('trackerUser')
    localStorage.removeItem('adminSelectedCompany')
  }

  return { user, authError, selectedCompany, setSelectedCompany, login, register, adminLogin, logout }
})