<template>
  <div class="min-h-screen bg-slate-50 p-8">
    <div class="max-w-6xl mx-auto">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-slate-800">Admin Dashboard</h1>
        <button @click="generatePDF" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-6 rounded-lg shadow-md transition-all">
          Download Daily PDF Report
        </button>
      </div>

      <div class="grid grid-cols-3 gap-6 mb-8">
        <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h3 class="text-slate-500 text-sm font-bold uppercase">Logs Today</h3>
          <p class="text-3xl font-bold text-blue-600">{{ todayLogs.length }}</p>
        </div>
      </div>
      
      </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

const todayLogs = ref([])

// Fetch all logs when the admin page loads
onMounted(async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs`)
    const data = await res.json()
    // Filter for only today's logs
    const today = new Date().toISOString().split('T')[0]
    todayLogs.value = data.filter(log => log.date === today)
  } catch (err) {
    console.error("Failed to fetch logs", err)
  }
})

const generatePDF = () => {
  const doc = new jsPDF()
  const todayDate = new Date().toLocaleDateString()
  
  doc.setFontSize(18)
  doc.text(`Project Daily Report - ${todayDate}`, 14, 22)

  // 1. Hourly Presence Breakdown (Using Time Slots & Roll Numbers)
  const TIME_SLOTS = {
    1: "9:15 AM - 10:15 AM", 2: "10:15 AM - 11:15 AM",
    3: "11:15 AM - 12:15 PM", 4: "1:00 PM - 2:00 PM",
    5: "2:00 PM - 3:00 PM", 6: "3:00 PM - 4:00 PM"
  }

  // Group by hour
  const hourlyData = { 1: [], 2: [], 3: [], 4: [], 5: [], 6: [] }
  todayLogs.value.forEach(log => {
    log.hours.forEach(hour => {
      if (hourlyData[hour]) hourlyData[hour].push(log.rollNumber) // Using Roll Number instead of Name!
    })
  })

  const presenceTable = Object.keys(hourlyData).map(hour => [
    TIME_SLOTS[hour], 
    hourlyData[hour].join(', ') || 'None'
  ])

  doc.setFontSize(14)
  doc.text("1. Hourly Presence Breakdown", 14, 35)
  doc.autoTable({
    startY: 40,
    head: [['Time Slot', 'Roll Numbers Present']],
    body: presenceTable,
    theme: 'grid',
    headStyles: { fillColor: [41, 128, 185] }
  })

  // 2. Team Progress Updates
  const finalY = doc.lastAutoTable.finalY || 40
  doc.text("2. Team Progress Updates", 14, finalY + 15)

  const progressData = todayLogs.value.map(log => [
    log.team,
    log.rollNumber,
    log.todayLog
  ])

  doc.autoTable({
    startY: finalY + 20,
    head: [['Team', 'Roll Number', 'Accomplished Today']],
    body: progressData,
    theme: 'grid',
    headStyles: { fillColor: [39, 174, 96] }
  })

  doc.save(`Project_Report_${todayDate.replace(/\//g, '-')}.pdf`)
}
</script>