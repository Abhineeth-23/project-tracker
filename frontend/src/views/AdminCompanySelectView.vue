<template>
  <div class="min-h-screen bg-slate-50 flex flex-col justify-between p-4 md:p-8 text-slate-800">
    <!-- Clean Enterprise Header -->
    <header class="max-w-5xl w-full mx-auto flex items-center justify-between py-4 px-6 bg-white border border-slate-200 rounded-lg shadow-sm">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-md bg-[#193099] flex items-center justify-center text-white shrink-0">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-base font-bold text-slate-900">HITAM Live Project Tracker</h1>
            <span class="text-[11px] font-semibold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">Admin Hub</span>
          </div>
          <p class="text-xs text-slate-500">Select an environment to manage teams, reports, and student submissions</p>
        </div>
      </div>

      <div class="flex items-center gap-3">
        <div class="hidden sm:flex flex-col text-right">
          <span class="text-xs font-semibold text-slate-900">{{ authStore.user?.name || 'Administrator' }}</span>
          <span class="text-[10px] text-slate-500 uppercase tracking-wider font-mono">{{ authStore.user?.role }}</span>
        </div>
        <button @click="handleLogout" class="px-3 py-1.5 rounded-md bg-white hover:bg-slate-100 border border-slate-200 text-xs font-medium text-slate-700 transition-colors flex items-center gap-1.5">
          <span>Sign Out</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
        </button>
      </div>
    </header>

    <!-- Main Content / Cards Grid -->
    <main class="max-w-5xl w-full mx-auto my-8">
      <div class="text-center mb-8">
        <h2 class="text-2xl font-bold text-slate-900 tracking-tight">Choose Your Workspace</h2>
        <p class="text-sm text-slate-600 mt-1.5 max-w-lg mx-auto">
          Both projects operate with isolated database environments, team rosters, and student submissions.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- CallHealth Card (White, #193099 Navy, #6fb733 Green) -->
        <div 
          @click="selectCompany('CallHealth')"
          class="bg-white border border-slate-200 border-t-4 border-t-[#193099] rounded-lg p-6 cursor-pointer hover:shadow-md hover:border-slate-300 transition-all flex flex-col justify-between"
        >
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="text-xs font-bold uppercase tracking-wider text-[#193099]">CallHealth Environment</span>
              <span class="text-[11px] font-semibold px-2 py-0.5 rounded bg-emerald-50 text-[#6fb733] border border-emerald-200">Active</span>
            </div>

            <div class="space-y-1 mb-4">
              <h3 class="text-xl font-bold text-slate-900">CallHealth</h3>
              <p class="text-xs text-slate-600">
                Digital Health Services, FHIR integrations, OCR automation, and clinical systems tracker.
              </p>
            </div>

            <!-- Stats Summary -->
            <div class="grid grid-cols-2 gap-3 py-3 my-4 bg-slate-50 border border-slate-200 rounded-md text-xs px-3">
              <div>
                <span class="text-slate-500 block text-[10px] uppercase font-semibold">Configured Teams</span>
                <span class="text-base font-bold text-[#193099]">{{ callHealthTeamsCount }} Teams</span>
              </div>
              <div>
                <span class="text-slate-500 block text-[10px] uppercase font-semibold">Registered Students</span>
                <span class="text-base font-bold text-[#6fb733]">{{ callHealthStudentsCount }} Students</span>
              </div>
            </div>
          </div>

          <div class="pt-2">
            <button class="w-full py-2.5 px-4 rounded-md bg-[#193099] hover:bg-[#12226e] text-white font-semibold text-xs transition-colors flex items-center justify-center gap-2">
              <span>Launch CallHealth Workspace</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
            </button>
          </div>
        </div>

        <!-- Succeed International Card (White, Blue) -->
        <div 
          @click="selectCompany('Succeed International')"
          class="bg-white border border-slate-200 border-t-4 border-t-blue-700 rounded-lg p-6 cursor-pointer hover:shadow-md hover:border-slate-300 transition-all flex flex-col justify-between"
        >
          <div>
            <div class="flex items-center justify-between mb-4">
              <span class="text-xs font-bold uppercase tracking-wider text-blue-700">Succeed Environment</span>
              <span class="text-[11px] font-semibold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-200">Active</span>
            </div>

            <div class="space-y-1 mb-4">
              <h3 class="text-xl font-bold text-slate-900">Succeed International</h3>
              <p class="text-xs text-slate-600">
                Global Enterprise Software, Cloud Engineering, Full-Stack solutions, and modern software delivery.
              </p>
            </div>

            <!-- Stats Summary -->
            <div class="grid grid-cols-2 gap-3 py-3 my-4 bg-slate-50 border border-slate-200 rounded-md text-xs px-3">
              <div>
                <span class="text-slate-500 block text-[10px] uppercase font-semibold">Configured Teams</span>
                <span class="text-base font-bold text-blue-900">{{ succeedTeamsCount }} Teams</span>
              </div>
              <div>
                <span class="text-slate-500 block text-[10px] uppercase font-semibold">Registered Students</span>
                <span class="text-base font-bold text-blue-700">{{ succeedStudentsCount }} Students</span>
              </div>
            </div>
          </div>

          <div class="pt-2">
            <button class="w-full py-2.5 px-4 rounded-md bg-blue-700 hover:bg-blue-800 text-white font-semibold text-xs transition-colors flex items-center justify-center gap-2">
              <span>Launch Succeed International</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" /></svg>
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Clean Corporate Footer -->
    <footer class="max-w-5xl w-full mx-auto text-center py-4 border-t border-slate-200 text-xs text-slate-500">
      <p>HITAM Industry-Academia Collaborative Engineering Portal</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const callHealthTeamsCount = ref(0)
const callHealthStudentsCount = ref(0)
const succeedTeamsCount = ref(0)
const succeedStudentsCount = ref(0)

onMounted(async () => {
  try {
    const [chTeamsRes, siTeamsRes, chUsersRes, siUsersRes] = await Promise.all([
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/teams?company=CallHealth`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/teams?company=Succeed%20International`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users?company=CallHealth`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users?company=Succeed%20International`)
    ])

    if (chTeamsRes.ok) {
      const data = await chTeamsRes.json()
      callHealthTeamsCount.value = Array.isArray(data) ? data.length : 0
    }
    if (siTeamsRes.ok) {
      const data = await siTeamsRes.json()
      succeedTeamsCount.value = Array.isArray(data) ? data.length : 0
    }
    if (chUsersRes.ok) {
      const data = await chUsersRes.json()
      callHealthStudentsCount.value = Array.isArray(data) ? data.filter(u => u.role === 'student' || u.role === 'user').length : 0
    }
    if (siUsersRes.ok) {
      const data = await siUsersRes.json()
      succeedStudentsCount.value = Array.isArray(data) ? data.filter(u => u.role === 'student' || u.role === 'user').length : 0
    }
  } catch (err) {
    console.error("Failed to load workspace counts", err)
  }
})

const selectCompany = (company) => {
  authStore.setSelectedCompany(company)
  router.push({ path: '/admin', query: { company } })
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>
