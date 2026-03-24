<template>
  <div class="min-h-screen bg-slate-50 font-sans pb-12">
    <header class="bg-[#1976D2] text-white sticky top-0 z-40 shadow-md">
      <div class="px-6 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
          <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zm0 7.5l-10-5v2.5l10 5 10-5v-2.5l-10 5zM2 12v2.5l10 5 10-5V12l-10 5-10-5z"/></svg>
          <h1 class="text-xl font-bold tracking-wide">Project Tracker</h1>
        </div>
        <div class="flex items-center space-x-4">
          <span class="text-sm font-medium bg-black/20 px-4 py-1.5 rounded-full border border-white/10 flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            Administrator (Admin)
          </span>
          <button @click="$router.push('/')" class="hover:bg-white/20 p-2 rounded-full transition-all" title="Back to Workspace">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          </button>
        </div>
      </div>

      <div class="flex px-6 space-x-2 bg-[#1565C0] pt-2">
        <button v-for="tab in TABS" :key="tab.id" @click="activeTab = tab.id" :class="['px-5 py-3 text-sm font-semibold rounded-t-lg transition-all flex items-center gap-2', activeTab === tab.id ? 'bg-slate-50 text-blue-700' : 'text-blue-100 hover:bg-white/10']">
          <span v-html="tab.icon"></span> {{ tab.label }}
        </button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
      <div class="flex justify-between items-center mb-6">
        <div class="bg-white border border-slate-200 rounded-lg px-4 py-2 flex items-center shadow-sm">
          <input type="date" v-model="selectedDate" class="outline-none text-sm font-medium text-slate-700 bg-transparent">
        </div>
        
        <button v-if="activeTab === 'daily'" @click="generatePDF" class="text-red-600 border border-red-200 hover:bg-red-50 font-bold py-2 px-4 rounded-lg shadow-sm transition-all flex items-center gap-2 text-sm">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clip-rule="evenodd"></path></svg>
          Download Data PDF
        </button>
        <button v-if="activeTab === 'attendance'" @click="copyAttendance" class="bg-slate-800 text-white font-bold py-2 px-4 rounded-lg shadow-sm hover:bg-slate-700 transition-all text-sm">
          Copy Sheet
        </button>
      </div>

      <div v-if="activeTab === 'daily'" class="bg-white rounded-xl shadow-sm border border-slate-200 p-8 relative overflow-hidden">
        <div class="mb-8">
          <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-full border border-blue-100 uppercase tracking-wider">Official Record</span>
          <h2 class="text-3xl font-extrabold text-slate-800 mt-4 mb-1">Project Daily Report</h2>
          <p class="text-teal-600 font-semibold">{{ formattedSelectedDate }}</p>
        </div>

        <div class="grid grid-cols-2 gap-6 mb-10">
          <div class="border border-slate-100 rounded-xl p-6 flex items-center gap-6 shadow-sm">
            <div class="bg-blue-500 p-4 rounded-xl text-white"><svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg></div>
            <div>
              <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Total Members Present</p>
              <p class="text-4xl font-black text-slate-800">{{ uniqueMembersPresent }}</p>
            </div>
          </div>
          <div class="border border-slate-100 rounded-xl p-6 flex items-center gap-6 shadow-sm">
            <div class="bg-teal-400 p-4 rounded-xl text-white"><svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg></div>
            <div>
              <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Active Teams Today</p>
              <p class="text-4xl font-black text-slate-800">{{ activeTeamsCount }}</p>
            </div>
          </div>
        </div>

        <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2 mb-4">
          <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
          Team Progress Updates
        </h3>
        <div class="border border-dashed border-slate-300 rounded-xl p-8 mb-10 text-center bg-slate-50" v-if="Object.keys(groupedLogs).length === 0">
           <p class="text-slate-500 font-medium">No project updates submitted for this date.</p>
        </div>
        <div v-else class="space-y-6 mb-10">
           <div v-for="(logs, team) in groupedLogs" :key="team" class="border border-slate-200 rounded-xl overflow-hidden shadow-sm bg-white">
              <div class="bg-blue-50 px-5 py-3 border-b border-blue-100 flex items-center justify-between">
                <span class="text-blue-800 font-bold text-sm tracking-wide">{{ team }}</span>
                <span class="text-xs font-bold bg-blue-200 text-blue-800 px-2 py-1 rounded">{{ logs.length }} Updates</span>
              </div>
              <div class="divide-y divide-slate-100">
                <div v-for="log in logs" :key="log.id" class="p-5 flex gap-4 hover:bg-slate-50 transition-colors">
                  <div class="flex-1">
                    <p class="text-sm font-bold text-slate-800 mb-1">
                      {{ log.name }} <span class="text-slate-500 font-normal">({{ log.rollNumber }})</span>
                    </p>
                    <p class="text-sm text-slate-600 leading-relaxed">{{ log.todayLog }}</p>
                  </div>
                </div>
              </div>
           </div>
        </div>

        <h3 class="text-lg font-bold text-slate-800 flex items-center gap-2 mb-4">
          <svg class="w-5 h-5 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          Presence Breakdown
        </h3>
        <div class="grid grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="slot in TIME_SLOTS" :key="slot.id" class="border border-slate-200 rounded-xl overflow-hidden shadow-sm flex flex-col">
            <div class="bg-slate-50 px-4 py-3 border-b border-slate-100 flex justify-between items-center">
              <span class="text-xs font-bold text-slate-600">{{ slot.label }}</span>
              <span class="bg-white text-slate-500 text-xs font-bold px-2 py-0.5 rounded border border-slate-200">{{ getMembersForHourUI(slot.id).length }}</span>
            </div>
            <div class="p-4 bg-white flex-1">
              <p v-if="getMembersForHourUI(slot.id).length === 0" class="text-xs text-slate-400 italic">Empty</p>
              <div v-else class="flex flex-col gap-1.5">
                <span v-for="member in getMembersForHourUI(slot.id)" :key="member" class="text-xs text-slate-700 bg-slate-100 px-2 py-1.5 rounded border border-slate-100">
                  {{ member }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'attendance'" class="bg-white rounded-xl shadow-sm border border-slate-200 p-8">
        <div v-for="slot in TIME_SLOTS" :key="slot.id" class="mb-6">
          <h4 class="text-sm font-bold text-blue-700 mb-2">{{ slot.label }}:</h4>
          <p class="text-sm text-slate-400 italic pl-4" v-if="getRollsForHourPDF(slot.id).length === 0">None</p>
          <ul class="list-disc pl-8 space-y-1" v-else>
            <li class="text-sm text-slate-800 font-mono" v-for="roll in getRollsForHourPDF(slot.id)" :key="roll">{{ roll }}</li>
          </ul>
        </div>
      </div>

      <div v-if="activeTab === 'records'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider border-b border-slate-200">
              <th class="p-4 font-bold">Name & Roll</th>
              <th class="p-4 font-bold">Team</th>
              <th class="p-4 font-bold">Time Slots</th>
              <th class="p-4 font-bold">Logs</th>
              <th class="p-4 font-bold text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredLogs.length === 0">
              <td colspan="5" class="p-8 text-center text-slate-500">No records found for this date.</td>
            </tr>
            <tr v-else v-for="log in filteredLogs" :key="log.id" class="border-b border-slate-100 hover:bg-slate-50">
              <td class="p-4"><p class="font-bold text-sm text-slate-800">{{ log.name }}</p><p class="text-xs text-slate-500">{{ log.rollNumber }}</p></td>
              <td class="p-4 text-sm font-medium text-blue-700">{{ log.team }}</td>
              <td class="p-4"><span class="bg-slate-100 text-xs px-2 py-1 rounded font-mono">{{ log.hours?.length || 0 }} slots</span></td>
              <td class="p-4 text-xs text-slate-600 max-w-xs truncate" :title="log.todayLog">{{ log.todayLog }}</td>
              <td class="p-4 text-right">
                <button class="text-blue-600 hover:underline text-xs font-bold mr-3">Edit</button>
                <button class="text-red-600 hover:underline text-xs font-bold">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="activeTab === 'holidays' || activeTab === 'users'" class="bg-white rounded-xl shadow-sm border border-slate-200 p-8 text-center">
        <svg class="w-16 h-16 text-slate-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
        <h3 class="text-xl font-bold text-slate-700 mb-2">API Connection Required</h3>
        <p class="text-slate-500">We need to update the FastAPI backend before we can manage Holidays, Users, and Teams.</p>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable' // BUG FIX 3: Explicit Import

// Constants
const TIME_SLOTS = [
  { id: 1, label: "9:15 AM - 10:15 AM" }, { id: 2, label: "10:15 AM - 11:15 AM" },
  { id: 3, label: "11:15 AM - 12:15 PM" }, { id: 4, label: "1:00 PM - 2:00 PM" },
  { id: 5, label: "2:00 PM - 3:00 PM" }, { id: 6, label: "3:00 PM - 4:00 PM" }
]

const TABS = [
  { id: 'daily', label: 'Daily Report', icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>' },
  { id: 'attendance', label: 'Attendance', icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>' },
  { id: 'records', label: 'Records', icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path></svg>' },
  { id: 'holidays', label: 'Holidays', icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>' },
  { id: 'users', label: 'Users & Teams', icon: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>' }
]

// State
const activeTab = ref('daily')
const selectedDate = ref(new Date().toISOString().split('T')[0])
const allLogs = ref([])

// Fetch Data
onMounted(async () => {
  try {
    // BUG FIX 1: Included /api/ in the fetch URL
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs`)
    const data = await res.json()
    // BUG FIX 2: Safe fallback to prevent crash if data isn't an array
    allLogs.value = Array.isArray(data) ? data : []
  } catch (err) {
    console.error("Failed to load logs")
    allLogs.value = []
  }
})

// Computed Properties
const filteredLogs = computed(() => allLogs.value.filter(log => log.date === selectedDate.value))
const formattedSelectedDate = computed(() => new Date(selectedDate.value).toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' }))

// Group logs by Team
const groupedLogs = computed(() => {
  const groups = {}
  filteredLogs.value.forEach(log => {
    if (!groups[log.team]) groups[log.team] = []
    groups[log.team].push(log)
  })
  return groups
})

const uniqueMembersPresent = computed(() => {
  const uniqueRolls = new Set(filteredLogs.value.map(log => log.rollNumber))
  return uniqueRolls.size
})

const activeTeamsCount = computed(() => {
  return Object.keys(groupedLogs.value).length
})

// UI Helper: Returns Name + Roll Number
const getMembersForHourUI = (hourId) => {
  return filteredLogs.value
    .filter(log => log.hours?.includes(hourId)) // BUG FIX 4: Optional chaining
    .map(log => `${log.name} (${log.rollNumber})`)
}

// PDF Helper: Returns strictly Roll Numbers
const getRollsForHourPDF = (hourId) => {
  return filteredLogs.value
    .filter(log => log.hours?.includes(hourId)) // BUG FIX 4
    .map(log => log.rollNumber)
}

// PDF Generator
const generatePDF = () => {
  const doc = new jsPDF()
  doc.setFontSize(18)
  doc.text(`Project Daily Report - ${formattedSelectedDate.value}`, 14, 22)

  // 1. Hourly Presence (Roll Numbers Only for PDF)
  const presenceTable = TIME_SLOTS.map(slot => [
    slot.label, 
    getRollsForHourPDF(slot.id).join(', ') || 'None' 
  ])

  doc.setFontSize(14)
  doc.text("1. Hourly Presence Breakdown", 14, 35)
  
  // BUG FIX 3: Passed doc explicitly into autoTable
  autoTable(doc, {
    startY: 40,
    head: [['Time Slot', 'Roll Numbers Present']],
    body: presenceTable,
    theme: 'grid',
    headStyles: { fillColor: [21, 101, 192] },
    styles: { cellPadding: 3, overflow: 'linebreak' }
  })

  // 2. Team Progress (Combined logs without individual names/rolls)
  const finalY = doc.lastAutoTable?.finalY || 40
  doc.text("2. Team Progress Updates", 14, finalY + 15)
  
  const progressData = Object.entries(groupedLogs.value).map(([team, logs]) => {
    // Combine logs into a unified list of tasks
    const combinedUpdates = logs.map(log => `• ${log.todayLog}`).join('\n')
    return [team, combinedUpdates]
  })

  autoTable(doc, {
    startY: finalY + 20,
    head: [['Team', 'Progress Updates']],
    body: progressData,
    theme: 'grid',
    headStyles: { fillColor: [45, 212, 191] },
    styles: { cellPadding: 4, overflow: 'linebreak' },
    columnStyles: { 0: { cellWidth: 40, fontStyle: 'bold' } }
  })

  doc.save(`Project_Report_${selectedDate.value}.pdf`)
}

// Copy Sheet logic (Uses Roll Numbers Only)
const copyAttendance = () => {
  let text = `Attendance for ${formattedSelectedDate.value}\n\n`
  TIME_SLOTS.forEach(slot => {
    const rolls = getRollsForHourPDF(slot.id).join(', ') || 'None'
    text += `${slot.label}:\n${rolls}\n\n`
  })
  navigator.clipboard.writeText(text)
  alert("Attendance copied to clipboard!")
}
</script>