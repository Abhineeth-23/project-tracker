<template>
  <div class="min-h-screen pb-12 bg-slate-50/50">
    <header class="bg-gradient-to-r from-blue-700 to-teal-600 text-white shadow-lg sticky top-0 z-40">
      <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
          <h1 class="text-xl font-bold tracking-wide">Project Tracker</h1>
        </div>
        <div class="flex items-center space-x-4">
          <span class="text-sm font-medium bg-black/20 px-4 py-1.5 rounded-full border border-white/10">
            {{ authStore.user?.name }} ({{ authStore.user?.team }})
          </span>
          <button @click="handleLogout" class="hover:bg-white/20 p-2 rounded-full transition-all">
            Logout
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-4 py-8">
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="bg-slate-50/80 px-6 py-5 border-b border-slate-100 flex items-center justify-between">
          <h2 class="text-lg font-bold text-slate-800">Progress Update</h2>
          <span class="bg-white border border-slate-200 text-slate-600 text-xs font-bold px-3 py-1 rounded-full">
            {{ new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' }) }}
          </span>
        </div>
        
        <div class="p-6">
          <form @submit.prevent="submitLog" class="space-y-6">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-3">Hours Present Today</label>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="hour in [1, 2, 3, 4, 5, 6]" 
                  :key="hour" 
                  type="button" 
                  @click="toggleHour(hour)" 
                  :class="['px-5 py-2.5 rounded-xl border text-sm font-medium transition-all', selectedHours.includes(hour) ? 'bg-blue-600 text-white border-blue-600' : 'bg-white border-slate-200 text-slate-600 hover:bg-blue-50']"
                >
                  Hour {{ hour }}
                </button>
              </div>
            </div>
            
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Accomplished today</label>
              <textarea v-model="todayLog" rows="3" class="w-full rounded-xl border border-slate-200 p-4 focus:ring-2 focus:ring-blue-500 outline-none resize-none"></textarea>
            </div>
            
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Goals for tomorrow</label>
              <textarea v-model="tomorrowGoal" rows="3" class="w-full rounded-xl border border-slate-200 p-4 focus:ring-2 focus:ring-teal-500 outline-none resize-none"></textarea>
            </div>
            
            <div v-if="message" :class="['p-4 rounded-xl text-sm font-medium', message.includes('Success') ? 'bg-teal-50 text-teal-800' : 'bg-red-50 text-red-800']">
              {{ message }}
            </div>
            
            <button type="submit" :disabled="isSubmitting" class="w-full bg-gradient-to-r from-blue-600 to-blue-500 text-white font-medium py-3.5 rounded-xl shadow-md hover:from-blue-700 transition-all disabled:opacity-70">
              {{ isSubmitting ? 'Saving...' : 'Submit Daily Update' }}
            </button>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Form State
const selectedHours = ref([])
const todayLog = ref('')
const tomorrowGoal = ref('')
const isSubmitting = ref(false)
const message = ref('')

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
    const res = await fetch('https://project-tracker-nb5j.onrender.com/api/logs', {
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
      message.value = 'Error saving log to database.'
    }
  } catch (err) {
    message.value = 'Network error connecting to backend.'
  } finally {
    isSubmitting.value = false
  }
}
</script>