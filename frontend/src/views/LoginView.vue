<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
    <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-400/20 rounded-full blur-3xl"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-teal-400/20 rounded-full blur-3xl"></div>

    <div class="bg-white rounded-2xl shadow-xl shadow-blue-900/5 w-full max-w-md overflow-hidden relative z-10 border border-slate-100">
      <div class="bg-gradient-to-r from-blue-600 to-teal-500 p-8 text-center">
        <h1 class="text-2xl font-bold text-white tracking-wide">Project Tracker</h1>
      </div>
      
      <div class="p-8">
        <div class="flex space-x-1 mb-8 bg-slate-100 p-1.5 rounded-lg">
          <button @click="authMode = 'login'" :class="['flex-1 py-2 rounded-md text-xs font-bold transition-all duration-200 uppercase tracking-wide', authMode === 'login' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-500 hover:text-blue-600']">Student</button>
          
          <button @click="authMode = 'register'" :class="['flex-1 py-2 rounded-md text-xs font-bold transition-all duration-200 uppercase tracking-wide', authMode === 'register' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-500 hover:text-blue-600']">Register</button>
          <button @click="authMode = 'admin'" :class="['flex-1 py-2 rounded-md text-xs font-bold transition-all duration-200 uppercase tracking-wide', authMode === 'admin' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-500 hover:text-slate-800']">Admin</button>
        </div>

        <div v-if="authStore.authError" class="mb-6 p-3 bg-red-50 text-red-700 text-sm rounded-lg border border-red-100">
          {{ authStore.authError }}
        </div>
        
        <form v-if="authMode === 'login'" @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Roll Number</label>
            <input type="text" required v-model="loginRoll" class="w-full rounded-xl border border-slate-200 py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. 2XE51AXXXX">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Password</label>
            <input type="password" required v-model="loginPass" class="w-full rounded-xl border border-slate-200 py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="••••••••">
          </div>
          <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-blue-500 text-white font-medium py-3 rounded-xl shadow-md transition-all active:scale-[0.98]">
            Login to Workspace
          </button>
        </form>

        <form v-if="authMode === 'register'" @submit.prevent="handleRegister" class="space-y-5">
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Name</label>
            <input type="text" required v-model="regName" class="w-full rounded-xl border border-slate-200 py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="John Doe">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Roll Number</label>
            <input type="text" required v-model="regRoll" class="w-full rounded-xl border border-slate-200 py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. 2XE51AXXXX">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Password</label>
            <input type="password" required v-model="regPass" class="w-full rounded-xl border border-slate-200 py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Create a password">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Team Assignment</label>
            <select v-model="regTeam" class="w-full rounded-xl border border-slate-200 py-3 px-4 focus:ring-2 focus:ring-blue-500 outline-none bg-white">
              <option v-for="team in TEAMS" :key="team" :value="team">{{ team }}</option>
            </select>
          </div>
          <button type="submit" class="w-full bg-gradient-to-r from-teal-500 to-teal-400 text-white font-medium py-3 rounded-xl shadow-md transition-all active:scale-[0.98]">
            Create Account
          </button>
        </form>

        <form v-if="authMode === 'admin'" @submit.prevent="handleAdminLogin" class="space-y-5">
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Admin Username</label>
            <input type="text" required v-model="adminUser" class="w-full rounded-xl border border-slate-200 py-3 px-4 focus:ring-2 focus:ring-slate-800 outline-none bg-slate-50">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Password</label>
            <input type="password" required v-model="adminPass" class="w-full rounded-xl border border-slate-200 py-3 px-4 focus:ring-2 focus:ring-slate-800 outline-none bg-slate-50">
          </div>
          <button type="submit" class="w-full bg-slate-800 text-white font-medium py-3 rounded-xl shadow-md transition-all active:scale-[0.98] hover:bg-slate-700">
            Access Admin Panel
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// State
const authMode = ref('login')
const TEAMS = ["Digi Yatra", "OCR", "FHIR", "MIRTH Connect", "ChatBot", "Blood Connect"]

// Form Inputs
const loginRoll = ref('')
const regName = ref('')
const regRoll = ref('')
const regTeam = ref('Digi Yatra')
const adminUser = ref('')
const adminPass = ref('')
const loginPass = ref('')
const regPass = ref('')

const handleLogin = async () => {
  const success = await authStore.login(loginRoll.value, loginPass.value)
  if (success) {
    if (authStore.user.role === 'admin') router.push('/admin')
    else router.push('/dashboard')
  }
}

const handleRegister = async () => {
  const success = await authStore.register({
    name: regName.value,
    rollNumber: regRoll.value,
    team: regTeam.value,
    password: regPass.value // Add password here
  })
  if (success) router.push('/dashboard')
}

const handleAdminLogin = async () => {
  const success = await authStore.adminLogin(adminUser.value, adminPass.value)
  if (success) router.push('/admin')
}
</script>