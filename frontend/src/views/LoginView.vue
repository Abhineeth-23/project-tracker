<template>
  <div class="min-h-screen flex items-center justify-center p-4 bg-slate-50">
    <div class="bg-white rounded-lg shadow-sm w-full max-w-md overflow-hidden border border-slate-200">
      <!-- Clean Solid Header (Navy) -->
      <div class="bg-[#193099] p-6 text-center text-white">
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded bg-white/10 text-[11px] font-medium text-blue-100 mb-2.5 border border-white/15">
          <svg class="w-3.5 h-3.5 text-blue-200 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          <span>Industry–Academia Collaboration</span>
        </div>
        <h1 class="text-xl font-bold text-white tracking-tight">
          HITAM Live Project Tracker
        </h1>
        <p class="text-xs text-blue-100 mt-1">Unified Multi-Tenant Workspace</p>
      </div>
      
      <div class="p-6">
        <div class="flex space-x-1 mb-6 bg-slate-100 p-1 rounded-md">
          <button @click="authMode = 'login'" :class="['flex-1 py-1.5 rounded text-xs font-semibold transition-all uppercase tracking-wide', authMode === 'login' ? 'bg-white text-[#193099] shadow-sm' : 'text-slate-600 hover:text-slate-900']">Student</button>
          <button @click="switchToRegister" :class="['flex-1 py-1.5 rounded text-xs font-semibold transition-all uppercase tracking-wide', authMode === 'register' ? 'bg-white text-[#193099] shadow-sm' : 'text-slate-600 hover:text-slate-900']">Register</button>
          <button @click="authMode = 'admin'" :class="['flex-1 py-1.5 rounded text-xs font-semibold transition-all uppercase tracking-wide', authMode === 'admin' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-600 hover:text-slate-900']">Admin</button>
        </div>

        <div v-if="authStore.authError" class="mb-4 p-2.5 bg-red-50 text-red-700 text-xs rounded-md border border-red-200 text-center font-medium">
          {{ authStore.authError }}
        </div>
        
        <!-- Student Login -->
        <form v-if="authMode === 'login'" @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Roll Number</label>
            <input type="text" required v-model="loginRoll" class="w-full rounded-md border border-slate-300 py-2 px-3 text-sm focus:ring-2 focus:ring-[#193099] focus:border-[#193099] outline-none" placeholder="e.g. 24E51A6634">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Password</label>
            <div class="relative">
              <input :type="showLoginPass ? 'text' : 'password'" required v-model="loginPass" class="w-full rounded-md border border-slate-300 py-2 pl-3 pr-10 text-sm focus:ring-2 focus:ring-[#193099] focus:border-[#193099] outline-none" placeholder="••••••••">
              <button type="button" @click="showLoginPass = !showLoginPass" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600">
                <svg v-if="!showLoginPass" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a10.05 10.05 0 011.53-3.16l2.16 2.16m3.85-3.85a3.001 3.001 0 00-3.85-3.85l2.16-2.16c.55-.16 1.13-.25 1.73-.25 4.478 0 8.268 2.943 9.542 7a10.05 10.05 0 01-2.14 3.74m-4.66-4.66l-5.6 5.6M3 3l18 18" /></svg>
              </button>
            </div>
          </div>
          <button type="submit" :disabled="authStore.isLoading" class="w-full bg-[#193099] hover:bg-[#12226e] text-white font-semibold py-2.5 rounded-md transition-colors text-sm disabled:opacity-70">
            Login to Workspace
          </button>
        </form>

        <!-- Student Registration -->
        <form v-if="authMode === 'register'" @submit.prevent="handleRegister" class="space-y-3.5">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
            <input type="text" required v-model="regName" class="w-full rounded-md border border-slate-300 py-2 px-3 text-sm focus:ring-2 focus:ring-[#193099] focus:border-[#193099] outline-none" placeholder="John Doe">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Roll Number</label>
            <input type="text" required v-model="regRoll" class="w-full rounded-md border border-slate-300 py-2 px-3 text-sm focus:ring-2 focus:ring-[#193099] focus:border-[#193099] outline-none" placeholder="e.g. 24E51A6634">
          </div>

          <!-- Select Company -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Select Company</label>
            <select 
              v-model="regCompany" 
              @change="onCompanyChange" 
              required
              class="w-full rounded-md border border-slate-300 py-2 px-3 text-sm focus:ring-2 focus:ring-[#193099] focus:border-[#193099] outline-none bg-white text-slate-800 font-medium"
            >
              <option value="CallHealth">CallHealth</option>
              <option value="Succeed International">Succeed International</option>
            </select>
          </div>

          <!-- Dynamic Team Selection -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="block text-xs font-semibold text-slate-700">Select Team ({{ regCompany }})</label>
              <span v-if="isFetchingTeams" class="text-[10px] text-[#193099] font-medium">Loading teams...</span>
            </div>
            <select 
              v-model="regTeam" 
              :disabled="isFetchingTeams"
              class="w-full rounded-md border border-slate-300 py-2 px-3 text-sm focus:ring-2 focus:ring-[#193099] focus:border-[#193099] outline-none bg-white text-slate-800 disabled:bg-slate-50 disabled:text-slate-400"
            >
              <option value="">Unassigned (Assign Later)</option>
              <option v-for="team in availableRegTeams" :key="team.id || team.name" :value="team.name">
                {{ team.name }}
              </option>
              <option v-if="!isFetchingTeams && availableRegTeams.length === 0" disabled value="">
                No teams found for {{ regCompany }}
              </option>
            </select>
            <p class="text-[11px] text-slate-500 mt-1">
              Showing {{ availableRegTeams.length }} team{{ availableRegTeams.length === 1 ? '' : 's' }} in {{ regCompany }}
            </p>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Password</label>
            <div class="relative">
              <input :type="showRegPass ? 'text' : 'password'" required v-model="regPass" class="w-full rounded-md border border-slate-300 py-2 pl-3 pr-10 text-sm focus:ring-2 focus:ring-[#193099] focus:border-[#193099] outline-none" placeholder="Create a password">
              <button type="button" @click="showRegPass = !showRegPass" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600">
                <svg v-if="!showRegPass" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a10.05 10.05 0 011.53-3.16l2.16 2.16m3.85-3.85a3.001 3.001 0 00-3.85-3.85l2.16-2.16c.55-.16 1.13-.25 1.73-.25 4.478 0 8.268 2.943 9.542 7a10.05 10.05 0 01-2.14 3.74m-4.66-4.66l-5.6 5.6M3 3l18 18" /></svg>
              </button>
            </div>
          </div>
          <button type="submit" :disabled="authStore.isLoading" class="w-full bg-[#193099] hover:bg-[#12226e] text-white font-semibold py-2.5 rounded-md transition-colors text-sm disabled:opacity-70">
            Create Account
          </button>
        </form>

        <!-- Admin Login -->
        <form v-if="authMode === 'admin'" @submit.prevent="handleAdminLogin" class="space-y-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Admin Username</label>
            <input type="text" required v-model="adminUser" class="w-full rounded-md border border-slate-300 py-2 px-3 text-sm focus:ring-2 focus:ring-slate-800 focus:border-slate-800 outline-none">
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Password</label>
            <div class="relative">
              <input :type="showAdminPass ? 'text' : 'password'" required v-model="adminPass" class="w-full rounded-md border border-slate-300 py-2 pl-3 pr-10 text-sm focus:ring-2 focus:ring-slate-800 focus:border-slate-800 outline-none">
              <button type="button" @click="showAdminPass = !showAdminPass" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600">
                <svg v-if="!showAdminPass" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                <svg v-else class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a10.05 10.05 0 011.53-3.16l2.16 2.16m3.85-3.85a3.001 3.001 0 00-3.85-3.85l2.16-2.16c.55-.16 1.13-.25 1.73-.25 4.478 0 8.268 2.943 9.542 7a10.05 10.05 0 01-2.14 3.74m-4.66-4.66l-5.6 5.6M3 3l18 18" /></svg>
              </button>
            </div>
          </div>
          <button type="submit" :disabled="authStore.isLoading" class="w-full bg-slate-800 hover:bg-slate-900 text-white font-semibold py-2.5 rounded-md transition-colors text-sm disabled:opacity-70">
            Access Admin Panel
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const authMode = ref('login')
const showLoginPass = ref(false)
const showRegPass = ref(false)
const showAdminPass = ref(false)

const loginRoll = ref('')
const loginPass = ref('')
const regName = ref('')
const regRoll = ref('')
const regCompany = ref('CallHealth')
const regTeam = ref('')
const regPass = ref('')
const adminUser = ref('')
const adminPass = ref('')

const availableRegTeams = ref([])
const isFetchingTeams = ref(false)

const fetchTeamsForCompany = async (company) => {
  isFetchingTeams.value = true
  regTeam.value = ''
  availableRegTeams.value = []
  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
    const res = await fetch(`${baseUrl}/api/teams?company=${encodeURIComponent(company)}`)
    if (res.ok) {
      const data = await res.json()
      if (Array.isArray(data)) {
        // Strictly filter to ensure only teams belonging to this company are shown
        const compTarget = (company || '').trim().toLowerCase()
        availableRegTeams.value = data.filter(t => {
          if (!t || !t.name) return false
          const tc = (t.company || '').trim().toLowerCase()
          if (compTarget.includes('succeed')) {
            return tc.includes('succeed')
          } else {
            return tc.includes('callhealth') || !tc.includes('succeed')
          }
        })
      } else {
        availableRegTeams.value = []
      }
    } else {
      availableRegTeams.value = []
    }
  } catch (err) {
    console.error("Failed to load company teams:", err)
    availableRegTeams.value = []
  } finally {
    isFetchingTeams.value = false
  }
}

// Watch regCompany so whenever the user changes the dropdown, teams immediately refresh
watch(regCompany, (newVal) => {
  if (newVal) {
    fetchTeamsForCompany(newVal)
  }
})

const onCompanyChange = () => {
  fetchTeamsForCompany(regCompany.value)
}

const switchToRegister = () => {
  authMode.value = 'register'
  fetchTeamsForCompany(regCompany.value)
}

onMounted(() => {
  fetchTeamsForCompany(regCompany.value)
})

const handleLogin = async () => {
  const success = await authStore.login(loginRoll.value, loginPass.value)
  if (success) {
    if (authStore.user.role === 'admin' || authStore.user.role === 'viewer') {
      router.push('/admin/select-company')
    } else {
      router.push('/dashboard')
    }
  }
}

const handleRegister = async () => {
  const success = await authStore.register({
    name: regName.value,
    rollNumber: regRoll.value,
    company: regCompany.value,
    team: regTeam.value,
    password: regPass.value
  })
  if (success) router.push('/dashboard')
}

const handleAdminLogin = async () => {
  const success = await authStore.adminLogin(adminUser.value, adminPass.value)
  if (success) router.push('/admin/select-company')
}
</script>