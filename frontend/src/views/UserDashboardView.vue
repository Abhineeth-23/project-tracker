<template>
  <div class="min-h-screen pb-12 bg-slate-50/50">
    <header class="bg-gradient-to-r from-blue-700 to-teal-600 text-white shadow-lg sticky top-0 z-40">
      <div class="max-w-6xl mx-auto px-4 md:px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-3">
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-center sm:justify-start">
          <h1 class="text-xl md:text-2xl font-bold tracking-wide">Project Tracker</h1>
        </div>
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-between sm:justify-end">
          <span class="text-xs md:text-sm font-medium bg-black/20 px-3 py-1.5 rounded-full border border-white/10 truncate max-w-[200px] sm:max-w-none flex items-center gap-1.5">
            <svg class="w-3 h-3 md:w-4 md:h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            <span class="truncate">{{ authStore.user?.name }}</span>
          </span>
          <button @click="handleLogout" class="hover:bg-white/20 p-2 md:px-3 md:py-2 rounded-lg transition-all flex items-center gap-1.5 shrink-0">
            <span class="hidden sm:inline text-sm font-bold">Logout</span>
            <svg class="w-4 h-4 md:w-5 md:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-4 sm:px-6 py-6 md:py-8">
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="bg-slate-50/80 px-4 md:px-6 py-4 border-b border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-2">
          <h2 class="text-base md:text-lg font-bold text-slate-800">Progress Update</h2>
          <span class="bg-white border border-slate-200 text-slate-600 text-[10px] md:text-xs font-bold px-3 py-1 rounded-full">
            {{ new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' }) }}
          </span>
        </div>
        
        <div class="p-4 md:p-6">
          <form @submit.prevent="submitLog" class="space-y-6">
            
            <div>
              <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-3">Hours Present Today</label>
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
            
            <div>
              <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Accomplished today</label>
              <textarea v-model="todayLog" rows="3" class="w-full rounded-xl border border-slate-200 p-3 md:p-4 text-sm md:text-base focus:ring-2 focus:ring-blue-500 outline-none resize-none" placeholder="What did you work on?"></textarea>
            </div>
            
            <div>
              <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Goals for tomorrow</label>
              <textarea v-model="tomorrowGoal" rows="3" class="w-full rounded-xl border border-slate-200 p-3 md:p-4 text-sm md:text-base focus:ring-2 focus:ring-teal-500 outline-none resize-none" placeholder="What's next?"></textarea>
            </div>
            
            <div v-if="message" :class="['p-3 md:p-4 rounded-xl text-xs md:text-sm font-medium text-center', message.includes('Success') ? 'bg-teal-50 text-teal-800' : 'bg-red-50 text-red-800']">
              {{ message }}
            </div>
            
            <button type="submit" :disabled="isSubmitting || !isFormValid" :class="['w-full font-bold py-3.5 md:py-4 rounded-xl shadow-md transition-all duration-200 text-sm md:text-base', isSubmitting || !isFormValid ? 'bg-slate-200 text-slate-400 cursor-not-allowed border border-slate-300' : 'bg-gradient-to-r from-blue-600 to-blue-500 text-white hover:from-blue-700 active:scale-[0.98]']">
              {{ isSubmitting ? 'Saving...' : (!isFormValid ? 'Fill all fields to submit' : 'Submit Daily Update') }}
            </button>
            
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Constants
const TIME_SLOTS = [
  { id: 1, label: "9:15 AM - 10:15 AM" },
  { id: 2, label: "10:15 AM - 11:15 AM" },
  { id: 3, label: "11:15 AM - 12:15 PM" },
  { id: 4, label: "1:00 PM - 2:00 PM" },
  { id: 5, label: "2:00 PM - 3:00 PM" },
  { id: 6, label: "3:00 PM - 4:00 PM" }
]

// Form State
const selectedHours = ref([])
const todayLog = ref('')
const tomorrowGoal = ref('')
const isSubmitting = ref(false)
const message = ref('')

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

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const submitLog = async () => {
  isSubmitting.value = true
  message.value = ''
  
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: authStore.user.id,
        name: authStore.user.name,
        rollNumber: authStore.user.rollNumber,
        team: authStore.user.team,
        hours: selectedHours.value,
        todayLog: todayLog.value,
        tomorrowGoal: tomorrowGoal.value,
        date: new Date().toISOString().split('T')[0]
      })
    })

    if (res.ok) {
      message.value = 'Success! Log saved.'
      selectedHours.value = []
      todayLog.value = ''
      tomorrowGoal.value = ''
      setTimeout(() => message.value = '', 3000)
    } else {
      const errorData = await res.json()
      message.value = errorData.detail || 'Error saving log to database.'
    }
  } catch (err) {
    message.value = 'Network error connecting to backend.'
  } finally {
    isSubmitting.value = false
  }
}
</script>