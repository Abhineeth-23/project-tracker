import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('trackerUser')) || null)
  const authError = ref('')

  async function login(rollNumber) {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rollNumber })
      })
      if (res.ok) {
        const data = await res.json()
        user.value = data
        localStorage.setItem('trackerUser', JSON.stringify(data))
        authError.value = ''
        return true
      } else {
        authError.value = 'Roll number not found. Please register.'
        return false
      }
    } catch (err) {
      authError.value = 'Network error.'
      return false
    }
  }

  // --- NEW REGISTER FUNCTION ---
  async function register(userData) {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/users/register', {
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
        authError.value = 'Roll number already exists.'
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
  }

  // Make sure to export register!
  return { user, authError, login, register, logout }
})