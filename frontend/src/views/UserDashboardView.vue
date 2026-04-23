<template>
  <div class="min-h-screen pb-12 bg-slate-50">
    <header class="bg-gradient-to-r from-blue-700 to-teal-600 text-white shadow-md sticky top-0 z-40">
      <div class="px-4 md:px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-3">
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-center sm:justify-start">
          <svg class="w-6 h-6 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zm0 7.5l-10-5v2.5l10 5 10-5v-2.5l-10 5zM2 12v2.5l10 5 10-5V12l-10 5-10-5z"/></svg>
          <h1 class="text-xl md:text-2xl font-bold tracking-wide">Project Tracker</h1>
        </div>
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-between sm:justify-end">
          <span class="text-xs md:text-sm font-medium bg-black/20 px-3 py-1.5 rounded-full border border-white/10 truncate max-w-[200px] sm:max-w-none flex items-center gap-1.5">
            <svg class="w-3 h-3 md:w-4 md:h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            <span class="truncate">{{ authStore.user?.name }} ({{ authStore.user?.team }})</span>
          </span>
          <button @click="handleLogout" class="hover:bg-white/20 p-2 md:px-3 md:py-2 rounded-lg transition-all flex items-center gap-1.5 shrink-0">
            <span class="hidden sm:inline text-sm font-bold">Logout</span>
            <svg class="w-4 h-4 md:w-5 md:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          </button>
        </div>
      </div>

      <div class="flex px-2 md:px-6 space-x-1 md:space-x-2 bg-black/20 pt-2 overflow-x-auto no-scrollbar">
        <button v-for="tab in TABS" :key="tab.id" @click="activeTab = tab.id" :class="['px-4 md:px-5 py-3 text-xs md:text-sm font-semibold rounded-t-lg transition-all flex items-center gap-2 whitespace-nowrap shrink-0', activeTab === tab.id ? 'bg-slate-50 text-blue-700' : 'text-blue-50 hover:bg-white/10']">
          <span v-html="tab.icon"></span> {{ tab.label }}
        </button>
      </div>
    </header>

    <main class="max-w-4xl mx-auto px-4 sm:px-6 py-6 md:py-8">
      
      <div v-if="activeTab === 'daily'">
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="bg-slate-50/80 px-4 md:px-6 py-4 border-b border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
            <h2 class="text-base md:text-lg font-bold text-slate-800">
              {{ editingLogId ? 'Edit Past Update' : 'Submit Progress Update' }}
            </h2>
            
            <div class="relative flex items-center group cursor-pointer w-full sm:w-auto">
              <input 
                type="date" 
                v-model="selectedDate" 
                :max="todayString"
                class="bg-white border border-slate-300 text-slate-700 text-xs md:text-sm font-bold px-3 py-1.5 rounded-full outline-none focus:ring-2 focus:ring-blue-500 shadow-sm cursor-pointer w-full"
              />
            </div>
          </div>
          
          <div class="p-4 md:p-6">
            <form @submit.prevent="submitLog" class="space-y-6">
              
              <div>
                <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-3">Hours Present on {{ selectedDateFormatted }}</label>
                <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  <button 
                    v-for="slot in TIME_SLOTS" 
                    :key="slot.id" 
                    type="button" 
                    @click="toggleHour(slot.id)" 
                    :class="['px-2 py-2.5 rounded-xl border text-[10px] md:text-xs font-bold transition-all text-center tracking-tight', selectedHours.includes(slot.id) ? 'bg-blue-600 text-white border-blue-600 shadow-sm shadow-blue-200' : 'bg-white border-slate-200 text-slate-600 hover:bg-blue-50']"
                  >
                    {{ slot.label }}
                  </button>
                </div>
              </div>
              
              <div v-if="previousGoal" class="bg-blue-50 border border-blue-100 rounded-xl p-4 md:p-5 relative overflow-hidden">
                <div class="absolute right-0 top-0 opacity-10 transform translate-x-4 -translate-y-4">
                  <svg class="w-24 h-24 text-blue-500" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zm0 7.5l-10-5v2.5l10 5 10-5v-2.5l-10 5zM2 12v2.5l10 5 10-5V12l-10 5-10-5z"/></svg>
                </div>
                <h3 class="text-[10px] md:text-xs font-bold text-blue-600 uppercase mb-1.5 flex items-center gap-1.5 relative z-10">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                  Goal set on {{ previousDate }}
                </h3>
                <p class="text-sm md:text-base text-blue-900 font-medium italic relative z-10">"{{ previousGoal }}"</p>
              </div>
              
              <div>
                <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Accomplished</label>
                <textarea v-model="todayLog" rows="3" class="w-full rounded-xl border border-slate-200 p-3 md:p-4 text-sm md:text-base focus:ring-2 focus:ring-blue-500 outline-none resize-none" placeholder="What did you work on?"></textarea>
              </div>
              
              <div>
                <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Goals for next time</label>
                <textarea v-model="tomorrowGoal" rows="3" class="w-full rounded-xl border border-slate-200 p-3 md:p-4 text-sm md:text-base focus:ring-2 focus:ring-teal-500 outline-none resize-none" placeholder="What's next?"></textarea>
              </div>
              
              <div v-if="message" :class="['p-3 md:p-4 rounded-xl text-xs md:text-sm font-medium text-center', message.includes('Success') ? 'bg-teal-50 text-teal-800' : 'bg-red-50 text-red-800']">
                {{ message }}
              </div>
              
              <button type="submit" :disabled="isSubmitting || !isFormValid" :class="['w-full font-bold py-3.5 md:py-4 rounded-xl shadow-md transition-all duration-200 text-sm md:text-base', isSubmitting || !isFormValid ? 'bg-slate-200 text-slate-400 cursor-not-allowed border border-slate-300' : (editingLogId ? 'bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 text-white' : 'bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 text-white')]">
                {{ isSubmitting ? 'Saving...' : (!isFormValid ? 'Fill all fields to submit' : (editingLogId ? 'Update Existing Log' : 'Submit Daily Update')) }}
              </button>
              
            </form>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'attendance'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="p-4 md:p-6 bg-slate-50 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
          <h3 class="text-base md:text-lg font-bold text-slate-800">My Attendance History</h3>
          <span class="bg-blue-100 text-blue-800 text-xs font-bold px-3 py-1 rounded-full">{{ myLogs.length }} Days Logged</span>
        </div>
        <div class="overflow-x-auto no-scrollbar">
          <table class="w-full text-left border-collapse min-w-[600px]">
            <thead>
              <tr class="bg-white text-slate-500 text-[10px] md:text-xs uppercase tracking-wider border-b border-slate-200">
                <th class="p-4 font-bold">Date</th>
                <th class="p-4 font-bold">Hours Present</th>
                <th class="p-4 font-bold">Accomplished Task</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="myLogs.length === 0">
                <td colspan="3" class="p-8 text-center text-sm text-slate-500">You haven't logged any days yet.</td>
              </tr>
              <tr v-else v-for="log in myLogs" :key="log.id" class="border-b border-slate-100 hover:bg-slate-50 cursor-pointer" @click="jumpToEdit(log.date)" title="Click to edit this day">
                <td class="p-4 font-semibold text-blue-600 hover:underline text-sm whitespace-nowrap">{{ new Date(log.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }) }}</td>
                <td class="p-4 text-sm font-medium text-slate-700 whitespace-nowrap">{{ log.hours?.length || 0 }} slots</td>
                <td class="p-4 text-xs text-slate-600 max-w-[300px] truncate" :title="log.todayLog">
                  <span v-if="log.todayLog && log.todayLog.trim().length > 0">{{ log.todayLog }}</span>
                  <span v-else class="text-slate-400 italic">Attendance only</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="activeTab === 'mom'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="bg-slate-50 px-4 md:px-6 py-4 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <h3 class="text-base md:text-lg font-bold text-slate-800">Meeting Minutes Archive</h3>
          <div class="relative w-full sm:w-64">
            <input type="text" v-model="momSearchQuery" placeholder="Search agendas or dates..." class="w-full rounded-full border border-slate-300 py-1.5 pl-9 pr-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none">
            <svg class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
          </div>
        </div>
        <div class="p-4 md:p-6">
          <div v-if="filteredMoMs.length === 0" class="border border-dashed border-slate-300 rounded-lg p-10 text-center bg-slate-50">
            <p class="text-slate-500 font-medium">No meeting records found.</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="mom in filteredMoMs" :key="mom.id" class="border border-slate-200 rounded-xl overflow-hidden shadow-sm transition-all bg-white">
              <div @click="toggleMoM(mom.id)" class="px-4 md:px-5 py-4 cursor-pointer hover:bg-slate-50 flex items-center justify-between group">
                <div class="flex items-center gap-3 md:gap-4">
                  <div :class="['p-2.5 rounded-lg text-white shrink-0', mom.file_path ? 'bg-amber-500' : 'bg-blue-500']">
                    <svg v-if="mom.file_path" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13"></path></svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                  </div>
                  <div>
                    <h4 class="font-bold text-slate-800 text-sm md:text-base group-hover:text-blue-600 transition-colors">{{ mom.agenda }}</h4>
                    <p class="text-[10px] md:text-xs text-slate-500 font-mono mt-0.5">{{ new Date(mom.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) }} • Logged by {{ mom.created_by }}</p>
                  </div>
                </div>
                <svg :class="['w-5 h-5 text-slate-400 transition-transform duration-200', expandedMoMs.includes(mom.id) ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
              </div>
              <div v-if="expandedMoMs.includes(mom.id)" class="border-t border-slate-100 bg-slate-50 px-4 md:px-5 py-4">
                <div class="mb-4">
                  <p class="text-[10px] md:text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Attendees</p>
                  <p class="text-sm text-slate-700">{{ mom.attendees || 'Not specified' }}</p>
                </div>
                <div v-if="mom.content">
                  <p class="text-[10px] md:text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Meeting Notes</p>
                  <div class="bg-white border border-slate-200 rounded-lg p-4 text-sm text-slate-700 leading-relaxed overflow-hidden">
                    <div v-html="mom.content" class="prose prose-sm max-w-none prose-slate"></div>
                  </div>
                </div>

                <div v-if="mom.file_path" class="bg-white border border-slate-200 rounded-lg p-3 md:p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mt-3">
                  <div class="flex items-center gap-3 overflow-hidden w-full">
                    <svg class="w-5 h-5 text-slate-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                    <span class="text-xs md:text-sm font-medium text-slate-700 truncate">{{ mom.file_name }}</span>
                  </div>
                  <button @click.prevent="viewMoM(mom.id)" class="w-full sm:w-auto text-center bg-slate-800 hover:bg-slate-700 text-white font-bold py-2 px-4 rounded-lg text-xs transition-colors shrink-0 flex items-center justify-center gap-2 shadow-sm">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                    Preview File
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'holidays'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="bg-slate-50 px-4 md:px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h3 class="text-base md:text-lg font-bold text-slate-800">Declared Holidays</h3>
        </div>
        <div class="p-4 md:p-6">
          <div v-if="allHolidays.length === 0" class="border border-dashed border-slate-300 rounded-lg p-10 text-center bg-slate-50">
            <p class="text-slate-500 italic text-sm">No upcoming holidays scheduled.</p>
          </div>
          <div v-else class="space-y-3 max-w-2xl mx-auto">
            <div v-for="holiday in allHolidays" :key="holiday.id" class="flex justify-between items-center border border-slate-100 p-4 rounded-lg bg-blue-50/50 hover:bg-white transition-colors shadow-sm">
              <div class="flex items-center gap-4">
                <div class="bg-teal-500 text-white p-2 rounded-lg shrink-0">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path></svg>
                </div>
                <div>
                  <p class="font-bold text-slate-800">{{ holiday.name }}</p>
                  <p class="text-[10px] md:text-xs text-slate-500 font-mono mt-1">{{ new Date(holiday.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// --- TAB CONFIGURATION ---
const activeTab = ref('daily')
const TABS = [
  { id: 'daily', label: 'Update Log', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>' },
  { id: 'attendance', label: 'My Attendance', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>' },
  { id: 'mom', label: 'Minutes of Meet', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>' },
  { id: 'holidays', label: 'Holidays', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>' }
]

const TIME_SLOTS = [
  { id: 1, label: "9:15 AM - 10:15 AM" }, { id: 2, label: "10:15 AM - 11:15 AM" },
  { id: 3, label: "11:15 AM - 12:15 PM" }, { id: 4, label: "1:00 PM - 2:00 PM" },
  { id: 5, label: "2:00 PM - 3:00 PM" }, { id: 6, label: "3:00 PM - 4:00 PM" }
]

// --- STATE ---
const myLogs = ref([])
const allMoMs = ref([])
const allHolidays = ref([])

// Date Picker State
const todayString = new Date().toISOString().split('T')[0]
const selectedDate = ref(todayString)
const selectedDateFormatted = computed(() => new Date(selectedDate.value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }))

// Edit Mode State
const editingLogId = ref(null)

const selectedHours = ref([])
const todayLog = ref('')
const tomorrowGoal = ref('')
const isSubmitting = ref(false)
const message = ref('')

const previousGoal = ref('')
const previousDate = ref('')

const momSearchQuery = ref('')
const expandedMoMs = ref([])

// --- HELPER: Process User Logs ---
const processUserLogs = (rawLogs) => {
  // 1. Filter firmly by Roll Number (ignores mismatched user IDs)
  const userLogs = rawLogs.filter(log => log.rollNumber === authStore.user.rollNumber)
  
  // 2. Deduplicate dates (keeps the highest ID / most recent edit if there are multiple entries)
  const uniqueLogsMap = new Map()
  userLogs.forEach(log => {
    if (!uniqueLogsMap.has(log.date) || uniqueLogsMap.get(log.date).id < log.id) {
      uniqueLogsMap.set(log.date, log)
    }
  })
  
  // 3. Sort newest first
  return Array.from(uniqueLogsMap.values()).sort((a, b) => new Date(b.date) - new Date(a.date))
}

// --- LOGIC: Handle Date Changes ---
const handleDateChange = () => {
  const existingLog = myLogs.value.find(log => log.date === selectedDate.value)
  
  if (existingLog) {
    editingLogId.value = existingLog.id
    selectedHours.value = [...(existingLog.hours || [])]
    todayLog.value = existingLog.todayLog || ''
    tomorrowGoal.value = existingLog.tomorrowGoal || ''
  } else {
    editingLogId.value = null
    selectedHours.value = []
    todayLog.value = ''
    tomorrowGoal.value = ''
  }

  const pastLogs = myLogs.value.filter(log => log.date < selectedDate.value)
  if (pastLogs.length > 0 && pastLogs[0].tomorrowGoal && pastLogs[0].tomorrowGoal.trim() !== '') {
    previousGoal.value = pastLogs[0].tomorrowGoal
    previousDate.value = new Date(pastLogs[0].date).toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })
  } else {
    previousGoal.value = ''
    previousDate.value = ''
  }
}

watch(selectedDate, handleDateChange)

// --- API FETCHING ---
onMounted(async () => {
  try {
    const [logsRes, momRes, holidaysRes] = await Promise.all([
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/holidays/`)
    ])
    
    // Process Logs using the new robust helper
    const rawLogs = await logsRes.json()
    if (Array.isArray(rawLogs)) {
      myLogs.value = processUserLogs(rawLogs)
      handleDateChange()
    }

    const mData = await momRes.json()
    allMoMs.value = Array.isArray(mData) ? mData : []

    const hData = await holidaysRes.json()
    allHolidays.value = Array.isArray(hData) ? hData : []

  } catch (err) {
    console.error("Failed to load dashboard data.", err)
  }
})

// --- DAILY UPDATE LOGIC ---
const isFormValid = computed(() => {
  return selectedHours.value.length > 0 && 
         todayLog.value.trim().length > 0 && 
         tomorrowGoal.value.trim().length > 0
})

const toggleHour = (hour) => {
  if (selectedHours.value.includes(hour)) {
    selectedHours.value = selectedHours.value.filter(h => h !== hour)
  } else {
    selectedHours.value.push(hour)
    selectedHours.value.sort((a, b) => a - b)
  }
}

const submitLog = async () => {
  isSubmitting.value = true
  message.value = ''
  
  try {
    const method = editingLogId.value ? 'PUT' : 'POST'
    const url = editingLogId.value 
      ? `${import.meta.env.VITE_API_BASE_URL}/api/logs/${editingLogId.value}`
      : `${import.meta.env.VITE_API_BASE_URL}/api/logs`

    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: authStore.user.id,
        name: authStore.user.name,
        rollNumber: authStore.user.rollNumber,
        team: authStore.user.team,
        hours: selectedHours.value,
        todayLog: todayLog.value,
        tomorrowGoal: tomorrowGoal.value,
        date: selectedDate.value
      })
    })

    if (res.ok) {
      message.value = editingLogId.value ? 'Success! Log updated.' : 'Success! Log saved.'
      setTimeout(() => message.value = '', 3000)
      
      // Auto-refresh logs table using the new robust helper
      const newLogRes = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs`)
      const newLogs = await newLogRes.json()
      if (Array.isArray(newLogs)) {
        myLogs.value = processUserLogs(newLogs)
      }
    } else {
      const errorData = await res.json()
      message.value = errorData.detail || 'Error saving log.'
    }
  } catch (err) {
    message.value = 'Network error connecting to backend.'
  } finally {
    isSubmitting.value = false
  }
}

const jumpToEdit = (dateStr) => {
  selectedDate.value = dateStr
  activeTab.value = 'daily'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// --- MOM LOGIC ---
const toggleMoM = (id) => {
  if (expandedMoMs.value.includes(id)) {
    expandedMoMs.value = expandedMoMs.value.filter(mId => mId !== id)
  } else {
    expandedMoMs.value.push(id)
  }
}

const filteredMoMs = computed(() => {
  if (!momSearchQuery.value) return allMoMs.value
  const query = momSearchQuery.value.toLowerCase()
  return allMoMs.value.filter(mom => 
    mom.agenda.toLowerCase().includes(query) || 
    mom.date.includes(query) ||
    (mom.attendees && mom.attendees.toLowerCase().includes(query))
  )
})

const viewMoM = (id) => {
  const url = `${import.meta.env.VITE_API_BASE_URL}/api/mom/download/${id}`
  window.open(url, '_blank')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>