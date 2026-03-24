import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('trackerUser')) || null)
  const authError = ref('')

  async function login(rollNumber) {
    try {
      // FIX 2: Correct URL
      const res = await fetch('https://project-tracker-nb5j.onrender.com/api/users/login', {
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

  async function register(userData) {
    try {
      // FIX 2: Correct URL
      const res = await fetch('https://project-tracker-nb5j.onrender.com/api/users/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData) // FIX 3: Pass userData, not just rollNumber!
      })
      if (res.ok) {
        const data = await res.json()
        user.value = data
        localStorage.setItem('trackerUser', JSON.stringify(data))
        authError.value = ''
        return true
      } else {
        authError.value = 'Roll number already exists or invalid data.'
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