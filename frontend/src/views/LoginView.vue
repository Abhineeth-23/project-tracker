<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-slate-50">
    <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-400/20 rounded-full blur-3xl"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-teal-400/20 rounded-full blur-3xl"></div>

    <div class="bg-white rounded-2xl shadow-xl shadow-blue-900/5 w-full max-w-md overflow-hidden relative z-10 border border-slate-100">
      <div class="bg-gradient-to-r from-blue-600 to-teal-500 p-6 md:p-8 text-center">
        <h1 class="text-xl md:text-2xl font-bold text-white tracking-wide">Project Tracker</h1>
      </div>
      
      <div class="p-5 md:p-8">
        <div class="flex space-x-1 mb-6 md:mb-8 bg-slate-100 p-1 md:p-1.5 rounded-lg">
          <button @click="authMode = 'login'" :class="['flex-1 py-2 md:py-2.5 rounded-md text-[10px] md:text-xs font-bold transition-all duration-200 uppercase tracking-wide', authMode === 'login' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-500 hover:text-blue-600']">Student</button>
          <button @click="authMode = 'register'" :class="['flex-1 py-2 md:py-2.5 rounded-md text-[10px] md:text-xs font-bold transition-all duration-200 uppercase tracking-wide', authMode === 'register' ? 'bg-white text-blue-700 shadow-sm' : 'text-slate-500 hover:text-blue-600']">Register</button>
          <button @click="authMode = 'admin'" :class="['flex-1 py-2 md:py-2.5 rounded-md text-[10px] md:text-xs font-bold transition-all duration-200 uppercase tracking-wide', authMode === 'admin' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-500 hover:text-slate-800']">Admin</button>
        </div>

        <div v-if="authStore.authError" class="mb-5 p-3 bg-red-50 text-red-700 text-xs md:text-sm rounded-lg border border-red-100 text-center font-medium">
          {{ authStore.authError }}
        </div>
        
        <form v-if="authMode === 'login'" @submit.prevent="handleLogin" class="space-y-4 md:space-y-5">
          <div>
            <label class="block text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Roll Number</label>
            <input type="text" required v-model="loginRoll" class="w-full rounded-xl border border-slate-200 py-2.5 md:py-3 px-3 md:px-4 text-sm md:text-base focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. 24E51A6634">
          </div>
          <div>
            <label class="block text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Password</label>
            <div class="relative">
              <input :type="showLoginPass ? 'text' : 'password'" required v-model="loginPass" class="w-full rounded-xl border border-slate-200 py-2.5 md:py-3 pl-3 pr-10 md:pl-4 md:pr-12 text-sm md:text-base focus:ring-2 focus:ring-blue-500 outline-none" placeholder="••••••••">
              <button type="button" @click="showLoginPass = !showLoginPass" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600">
                <svg v-if="!showLoginPass" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a10.05 10.05 0 011.53-3.16l2.16 2.16m3.85-3.85a3.001 3.001 0 00-3.85-3.85l2.16-2.16c.55-.16 1.13-.25 1.73-.25 4.478 0 8.268 2.943 9.542 7a10.05 10.05 0 01-2.14 3.74m-4.66-4.66l-5.6 5.6M3 3l18 18" /></svg>
              </button>
            </div>
          </div>
          <button type="submit" :disabled="authStore.isLoading" class="w-full bg-gradient-to-r from-blue-600 to-blue-500 text-white font-medium py-3 rounded-xl shadow-md transition-all active:scale-[0.98] text-sm md:text-base mt-2 disabled:opacity-70">
            Login to Workspace
          </button>
        </form>

        <form v-if="authMode === 'register'" @submit.prevent="handleRegister" class="space-y-4 md:space-y-5">
          <div>
            <label class="block text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Full Name</label>
            <input type="text" required v-model="regName" class="w-full rounded-xl border border-slate-200 py-2.5 md:py-3 px-3 md:px-4 text-sm md:text-base focus:ring-2 focus:ring-blue-500 outline-none" placeholder="John Doe">
          </div>
          <div>
            <label class="block text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Roll Number</label>
            <input type="text" required v-model="regRoll" class="w-full rounded-xl border border-slate-200 py-2.5 md:py-3 px-3 md:px-4 text-sm md:text-base focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. 24E51A6634">
          </div>
          <div>
            <label class="block text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Team Assignment</label>
            <select v-model="regTeam" class="w-full rounded-xl border border-slate-200 py-2.5 md:py-3 px-3 md:px-4 text-sm md:text-base focus:ring-2 focus:ring-blue-500 outline-none bg-white">
              <option v-for="team in TEAMS" :key="team" :value="team">{{ team }}</option>
            </select>
          </div>
          <div>
            <label class="block text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Password</label>
            <div class="relative">
              <input :type="showRegPass ? 'text' : 'password'" required v-model="regPass" class="w-full rounded-xl border border-slate-200 py-2.5 md:py-3 pl-3 pr-10 md:pl-4 md:pr-12 text-sm md:text-base focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Create a password">
              <button type="button" @click="showRegPass = !showRegPass" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600">
                <svg v-if="!showRegPass" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a10.05 10.05 0 011.53-3.16l2.16 2.16m3.85-3.85a3.001 3.001 0 00-3.85-3.85l2.16-2.16c.55-.16 1.13-.25 1.73-.25 4.478 0 8.268 2.943 9.542 7a10.05 10.05 0 01-2.14 3.74m-4.66-4.66l-5.6 5.6M3 3l18 18" /></svg>
              </button>
            </div>
          </div>
          <button type="submit" :disabled="authStore.isLoading" class="w-full bg-gradient-to-r from-teal-500 to-teal-400 text-white font-medium py-3 rounded-xl shadow-md transition-all active:scale-[0.98] text-sm md:text-base mt-2 disabled:opacity-70">
            Create Account
          </button>
        </form>

        <form v-if="authMode === 'admin'" @submit.prevent="handleAdminLogin" class="space-y-4 md:space-y-5">
          <div>
            <label class="block text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Admin Username</label>
            <input type="text" required v-model="adminUser" class="w-full rounded-xl border border-slate-200 py-2.5 md:py-3 px-3 md:px-4 text-sm md:text-base focus:ring-2 focus:ring-slate-800 outline-none bg-slate-50">
          </div>
          <div>
            <label class="block text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Password</label>
            <div class="relative">
              <input :type="showAdminPass ? 'text' : 'password'" required v-model="adminPass" class="w-full rounded-xl border border-slate-200 py-2.5 md:py-3 pl-3 pr-10 md:pl-4 md:pr-12 text-sm md:text-base focus:ring-2 focus:ring-slate-800 outline-none bg-slate-50">
              <button type="button" @click="showAdminPass = !showAdminPass" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600">
                <svg v-if="!showAdminPass" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a10.05 10.05 0 011.53-3.16l2.16 2.16m3.85-3.85a3.001 3.001 0 00-3.85-3.85l2.16-2.16c.55-.16 1.13-.25 1.73-.25 4.478 0 8.268 2.943 9.542 7a10.05 10.05 0 01-2.14 3.74m-4.66-4.66l-5.6 5.6M3 3l18 18" /></svg>
              </button>
            </div>
          </div>
          <button type="submit" :disabled="authStore.isLoading" class="w-full bg-slate-800 text-white font-medium py-3 rounded-xl shadow-md transition-all active:scale-[0.98] hover:bg-slate-700 text-sm md:text-base mt-2 disabled:opacity-70">
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

// Visibility Toggles
const showLoginPass = ref(false)
const showRegPass = ref(false)
const showAdminPass = ref(false)

// Form Inputs
const loginRoll = ref('')
const loginPass = ref('')
const regName = ref('')
const regRoll = ref('')
const regTeam = ref('Digi Yatra')
const regPass = ref('')
const adminUser = ref('')
const adminPass = ref('')

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
    password: regPass.value
  })
  if (success) router.push('/dashboard')
}

const handleAdminLogin = async () => {
  const success = await authStore.adminLogin(adminUser.value, adminPass.value)
  if (success) router.push('/admin')
}
</script>