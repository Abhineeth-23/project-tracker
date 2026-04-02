<template>
  <div class="min-h-screen bg-slate-50 font-sans pb-12">
    <header class="bg-[#1976D2] text-white sticky top-0 z-40 shadow-md">
      <div class="px-4 md:px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-center sm:justify-start">
          <svg class="w-6 h-6 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zm0 7.5l-10-5v2.5l10 5 10-5v-2.5l-10 5zM2 12v2.5l10 5 10-5V12l-10 5-10-5z"/></svg>
          <h1 class="text-xl font-bold tracking-wide">Project Tracker</h1>
        </div>
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-between sm:justify-end">
          <span class="text-xs md:text-sm font-medium bg-black/20 px-3 py-1.5 rounded-full border border-white/10 flex items-center gap-2">
            <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            <span class="hidden sm:inline">{{ authStore.user?.role === 'viewer' ? 'Executive (View Only)' : 'Administrator (Admin)' }}</span>
            <span class="sm:hidden">{{ authStore.user?.role === 'viewer' ? 'Exec' : 'Admin' }}</span>
          </span>
          <button @click="handleLogout" class="hover:bg-white/20 px-2 py-2 rounded-lg transition-all flex items-center gap-1" title="Secure Logout">
            <span class="text-xs md:text-sm font-bold">Logout</span>
            <svg class="w-4 h-4 md:w-5 md:h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          </button>
        </div>
      </div>

      <div class="flex px-2 md:px-6 space-x-1 md:space-x-2 bg-[#1565C0] pt-2 overflow-x-auto no-scrollbar">
        <button v-for="tab in TABS" :key="tab.id" @click="activeTab = tab.id" :class="['px-4 md:px-5 py-3 text-xs md:text-sm font-semibold rounded-t-lg transition-all flex items-center gap-2 whitespace-nowrap shrink-0', activeTab === tab.id ? 'bg-slate-50 text-blue-700' : 'text-blue-100 hover:bg-white/10']">
          <span v-html="tab.icon"></span> {{ tab.label }}
        </button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 md:px-6 py-6 md:py-8">
      <div v-if="['daily', 'attendance', 'records'].includes(activeTab)" class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
        <div class="bg-white border border-slate-200 rounded-lg px-4 py-2 flex items-center shadow-sm w-full md:w-auto">
          <input type="date" v-model="selectedDate" class="outline-none text-sm font-medium text-slate-700 bg-transparent w-full">
        </div>
        
        <div class="flex flex-col sm:flex-row gap-2 w-full md:w-auto" v-if="activeTab === 'daily'">
          <button @click="generatePDF" class="w-full sm:w-auto justify-center text-red-600 border border-red-200 hover:bg-red-50 font-bold py-2 px-4 rounded-lg shadow-sm transition-all flex items-center gap-2 text-sm">
            <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clip-rule="evenodd"></path></svg>
            Daily Report
          </button>
          <button @click="generateAttendancePDF" class="w-full sm:w-auto justify-center text-blue-600 border border-blue-200 hover:bg-blue-50 font-bold py-2 px-4 rounded-lg shadow-sm transition-all flex items-center gap-2 text-sm">
            <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"></path><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"></path></svg>
            Attendance Only
          </button>
        </div>
        <button v-if="activeTab === 'attendance'" @click="copyAttendance" class="w-full md:w-auto bg-slate-800 text-white font-bold py-2 px-4 rounded-lg shadow-sm hover:bg-slate-700 transition-all text-sm">
          Copy Sheet
        </button>
      </div>

      <div v-if="activeTab === 'daily'" class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-8 relative overflow-hidden">
        <div class="mb-6 md:mb-8">
          <span class="text-[10px] md:text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-full border border-blue-100 uppercase tracking-wider">Official Record</span>
          <h2 class="text-2xl md:text-3xl font-extrabold text-slate-800 mt-4 mb-1">Project Daily Report</h2>
          <p class="text-sm md:text-base text-teal-600 font-semibold">{{ formattedSelectedDate }}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-8 md:mb-10">
          <div class="border border-slate-100 rounded-xl p-4 md:p-6 flex items-center gap-4 md:gap-6 shadow-sm">
            <div class="bg-blue-500 p-3 md:p-4 rounded-xl text-white"><svg class="w-6 h-6 md:w-8 md:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg></div>
            <div>
              <p class="text-[10px] md:text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Total Members</p>
              <p class="text-3xl md:text-4xl font-black text-slate-800">{{ uniqueMembersPresent }}</p>
            </div>
          </div>
          <div class="border border-slate-100 rounded-xl p-4 md:p-6 flex items-center gap-4 md:gap-6 shadow-sm">
            <div class="bg-teal-400 p-3 md:p-4 rounded-xl text-white"><svg class="w-6 h-6 md:w-8 md:h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg></div>
            <div>
              <p class="text-[10px] md:text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Active Teams</p>
              <p class="text-3xl md:text-4xl font-black text-slate-800">{{ activeTeamsCount }}</p>
            </div>
          </div>
        </div>

        <h3 class="text-base md:text-lg font-bold text-slate-800 flex items-center gap-2 mb-4">
          <svg class="w-4 h-4 md:w-5 md:h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
          Team Progress Updates
        </h3>
        <div class="border border-dashed border-slate-300 rounded-xl p-6 md:p-8 mb-8 md:mb-10 text-center bg-slate-50" v-if="Object.keys(teamProgressUpdates).length === 0">
           <p class="text-sm md:text-base text-slate-500 font-medium">No written project updates submitted for this date.</p>
        </div>
        <div v-else class="space-y-4 md:space-y-6 mb-8 md:mb-10">
           <div v-for="(logs, team) in teamProgressUpdates" :key="team" class="border border-slate-200 rounded-xl overflow-hidden shadow-sm bg-white">
              <div class="bg-blue-50 px-4 md:px-5 py-3 border-b border-blue-100 flex items-center justify-between">
                <span class="text-blue-800 font-bold text-sm tracking-wide">{{ team }}</span>
                <span class="text-[10px] md:text-xs font-bold bg-blue-200 text-blue-800 px-2 py-1 rounded">{{ logs.length }} Updates</span>
              </div>
              <div class="divide-y divide-slate-100">
                <div v-for="log in logs" :key="log.id" class="p-4 md:p-5 flex flex-col sm:flex-row gap-2 sm:gap-4 hover:bg-slate-50 transition-colors">
                  <div class="flex-1">
                    <p class="text-xs md:text-sm font-bold text-slate-800 mb-1">
                      {{ log.name }} <span class="text-slate-500 font-normal">({{ log.rollNumber }})</span>
                    </p>
                    <p class="text-sm text-slate-600 leading-relaxed">{{ log.todayLog }}</p>
                  </div>
                </div>
              </div>
           </div>
        </div>

        <h3 class="text-base md:text-lg font-bold text-slate-800 flex items-center gap-2 mb-4">
          <svg class="w-4 h-4 md:w-5 md:h-5 text-teal-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          Presence Breakdown
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 md:gap-4">
          <div v-for="slot in TIME_SLOTS" :key="slot.id" class="border border-slate-200 rounded-xl overflow-hidden shadow-sm flex flex-col">
            <div class="bg-slate-50 px-3 md:px-4 py-2 md:py-3 border-b border-slate-100 flex justify-between items-center">
              <span class="text-[10px] md:text-xs font-bold text-slate-600">{{ slot.label }}</span>
              <span class="bg-white text-slate-500 text-[10px] md:text-xs font-bold px-2 py-0.5 rounded border border-slate-200">{{ getMembersForHourUI(slot.id).length }}</span>
            </div>
            <div class="p-3 md:p-4 bg-white flex-1">
              <p v-if="getMembersForHourUI(slot.id).length === 0" class="text-xs text-slate-400 italic">Empty</p>
              <div v-else class="flex flex-col gap-1.5">
                <span v-for="member in getMembersForHourUI(slot.id)" :key="member" class="text-[10px] md:text-xs text-slate-700 bg-slate-100 px-2 py-1.5 rounded border border-slate-100">
                  {{ member }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'attendance'" class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-8">
        <h3 class="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
          <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
          Daily Attendance Summary
        </h3>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-x-8 gap-y-2">
          <div v-for="roll in dynamicOrderedRolls" :key="roll" class="flex justify-between items-center py-2.5 border-b border-slate-100">
            <span class="text-sm font-mono text-slate-700 font-semibold">{{ roll }}</span>
            <span :class="['text-xs font-bold px-2 py-1 rounded', formatHoursForRoll(roll) !== '0 hours' ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-400']">
              {{ formatHoursForRoll(roll) }}
            </span>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'records'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto no-scrollbar">
          <table class="w-full text-left border-collapse min-w-[700px]">
            <thead>
              <tr class="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider border-b border-slate-200">
                <th class="p-4 font-bold">Name & Roll</th>
                <th class="p-4 font-bold">Team</th>
                <th class="p-4 font-bold">Time Slots</th>
                <th class="p-4 font-bold">Logs</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredLogs.length === 0">
                <td colspan="4" class="p-8 text-center text-sm text-slate-500">No records found for this date.</td>
              </tr>
              <tr v-else v-for="log in filteredLogs" :key="log.id" class="border-b border-slate-100 hover:bg-slate-50">
                <td class="p-4"><p class="font-bold text-sm text-slate-800">{{ log.name }}</p><p class="text-xs text-slate-500">{{ log.rollNumber }}</p></td>
                <td class="p-4 text-sm font-medium text-blue-700 whitespace-nowrap">{{ log.team }}</td>
                <td class="p-4"><span class="bg-slate-100 text-xs px-2 py-1 rounded font-mono whitespace-nowrap">{{ log.hours?.length || 0 }} slots</span></td>
                <td class="p-4 text-xs text-slate-600 max-w-[200px] md:max-w-xs truncate" :title="log.todayLog">
                  <span v-if="log.todayLog && log.todayLog.trim().length > 0">{{ log.todayLog }}</span>
                  <span v-else class="text-slate-400 italic font-medium">Attendance only</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="activeTab === 'holidays'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div v-if="authStore.user?.role === 'admin'" class="col-span-1 bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6 h-fit">
          <h3 class="text-base md:text-lg font-bold text-teal-700 flex items-center gap-2 mb-6">
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>
            Declare Holiday
          </h3>
          <form @submit.prevent="submitHoliday" class="space-y-4">
            <div>
              <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Select Date</label>
              <input type="date" required v-model="newHolidayDate" class="w-full rounded-lg border border-slate-200 py-2.5 px-3 text-sm focus:ring-2 focus:ring-teal-500 outline-none">
            </div>
            <div>
              <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Holiday Title</label>
              <input type="text" required v-model="newHolidayName" placeholder="e.g. UGADI" class="w-full rounded-lg border border-slate-200 py-2.5 px-3 text-sm focus:ring-2 focus:ring-teal-500 outline-none">
            </div>
            <button type="submit" class="w-full bg-teal-600 hover:bg-teal-700 text-white font-bold py-3 rounded-lg shadow-sm transition-all mt-2 text-sm md:text-base">
              Push to Workspace
            </button>
          </form>
        </div>
        
        <div :class="[authStore.user?.role === 'admin' ? 'col-span-1 lg:col-span-2' : 'col-span-1 lg:col-span-3', 'bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6']">
          <h3 class="text-base md:text-lg font-bold text-blue-700 flex items-center gap-2 mb-6">
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
            Active Holidays Registry
          </h3>
          <div v-if="allHolidays.length === 0" class="border border-dashed border-slate-300 rounded-lg p-6 md:p-8 text-center bg-slate-50">
            <p class="text-slate-500 italic text-sm">No holidays have been declared yet.</p>
          </div>
          <div v-else class="space-y-3">
            <div v-for="holiday in allHolidays" :key="holiday.id" class="flex justify-between items-center border border-slate-100 p-3 md:p-4 rounded-lg bg-slate-50 hover:bg-white transition-colors shadow-sm">
              <div>
                <p class="font-bold text-slate-800 text-sm md:text-base">{{ holiday.name }}</p>
                <p class="text-[10px] md:text-xs text-slate-500 font-mono mt-1">{{ new Date(holiday.date).toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }) }}</p>
              </div>
              <button v-if="authStore.user?.role === 'admin'" @click="removeHoliday(holiday.id)" class="text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded transition-colors">
                <svg class="w-4 h-4 md:w-5 md:h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'users'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="p-4 md:p-6 bg-slate-50 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
          <h3 class="text-base md:text-lg font-bold text-slate-800">Workspace Members Registry</h3>
          <span class="bg-blue-100 text-blue-800 text-xs font-bold px-3 py-1 rounded-full">{{ allUsers.length }} Total Accounts</span>
        </div>
        <div class="overflow-x-auto no-scrollbar">
          <table class="w-full text-left border-collapse min-w-[700px]">
            <thead>
              <tr class="bg-white text-slate-500 text-[10px] md:text-xs uppercase tracking-wider border-b border-slate-200">
                <th class="p-4 font-bold">Full Name</th>
                <th class="p-4 font-bold">Roll Number</th>
                <th class="p-4 font-bold">Team Assignment</th>
                <th v-if="authStore.user?.role === 'admin'" class="p-4 font-bold text-right">Admin Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="allUsers.length === 0">
                <td colspan="4" class="p-8 text-center text-sm text-slate-500">Loading user database...</td>
              </tr>
              <tr v-else v-for="user in allUsers" :key="user.id" class="border-b border-slate-100 hover:bg-slate-50">
                <template v-if="editingUser && editingUser.id === user.id">
                  <td class="p-3"><input type="text" v-model="editingUser.name" class="w-full border rounded px-2 py-1 text-sm outline-none focus:border-blue-500"></td>
                  <td class="p-3"><input type="text" v-model="editingUser.rollNumber" class="w-full border rounded px-2 py-1 text-sm outline-none focus:border-blue-500"></td>
                  <td class="p-3">
                    <select v-model="editingUser.team" class="w-full border rounded px-2 py-1 text-sm outline-none focus:border-blue-500 bg-white">
                      <option v-for="team in AVAILABLE_TEAMS" :key="team" :value="team">{{ team }}</option>
                    </select>
                  </td>
                  <td class="p-3 text-right space-x-2 whitespace-nowrap">
                    <button @click="saveUserEdit" class="bg-green-500 text-white px-3 py-1.5 rounded text-xs font-bold hover:bg-green-600">Save</button>
                    <button @click="editingUser = null" class="bg-slate-200 text-slate-700 px-3 py-1.5 rounded text-xs font-bold hover:bg-slate-300">Cancel</button>
                  </td>
                </template>
                
                <template v-else>
                  <td class="p-4 font-semibold text-slate-800 text-sm flex items-center gap-2">
                    <span v-if="user.role === 'admin' || user.role === 'viewer'" class="bg-amber-100 text-amber-700 text-[10px] font-black px-1.5 py-0.5 rounded uppercase shrink-0">Admin</span>
                    <span class="truncate">{{ user.name }}</span>
                  </td>
                  <td class="p-4 text-sm font-mono text-slate-600">{{ user.rollNumber }}</td>
                  <td class="p-4 text-sm font-medium text-blue-700 whitespace-nowrap">{{ user.team }}</td>
                  <td v-if="authStore.user?.role === 'admin'" class="p-4 text-right whitespace-nowrap">
                    <button @click="startEdit(user)" class="text-blue-600 hover:underline text-xs font-bold mr-4">Edit Profile</button>
                    <button @click="removeUser(user.id)" class="text-red-600 hover:underline text-xs font-bold">Revoke Access</button>
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-if="activeTab === 'mom'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div v-if="authStore.user?.role === 'admin'" class="col-span-1 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden h-fit">
          <div class="bg-slate-800 px-6 py-4 border-b border-slate-700 flex justify-between items-center">
            <h3 class="text-base font-bold text-white flex items-center gap-2">Log Meeting</h3>
          </div>
          
          <div class="p-6">
            <div class="flex space-x-1 mb-6 bg-slate-100 p-1 rounded-lg">
              <button @click="momFormMode = 'text'" :class="['flex-1 py-2 rounded-md text-xs font-bold transition-all duration-200 tracking-wide', momFormMode === 'text' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700']">📝 Write Note</button>
              <button @click="momFormMode = 'file'" :class="['flex-1 py-2 rounded-md text-xs font-bold transition-all duration-200 tracking-wide', momFormMode === 'file' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700']">📎 Upload File</button>
            </div>

            <form @submit.prevent="submitMoM" class="space-y-4">
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Meeting Date</label>
                <input type="date" required v-model="newMomDate" class="w-full rounded-lg border border-slate-200 py-2.5 px-3 text-sm focus:ring-2 focus:ring-slate-500 outline-none">
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Agenda / Topic</label>
                <input type="text" required v-model="newMomAgenda" placeholder="e.g. Frontend Sync" class="w-full rounded-lg border border-slate-200 py-2.5 px-3 text-sm focus:ring-2 focus:ring-slate-500 outline-none">
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Attendees (Optional)</label>
                <input type="text" v-model="newMomAttendees" placeholder="e.g. John, Sarah, Mike" class="w-full rounded-lg border border-slate-200 py-2.5 px-3 text-sm focus:ring-2 focus:ring-slate-500 outline-none">
              </div>
              
              <div v-if="momFormMode === 'text'">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Meeting Notes</label>
                <textarea required v-model="newMomContent" rows="5" class="w-full rounded-lg border border-slate-200 p-3 text-sm focus:ring-2 focus:ring-slate-500 outline-none resize-none" placeholder="Enter key points and action items..."></textarea>
              </div>

              <div v-if="momFormMode === 'file'">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Attach Document (PDF, DOCX)</label>
                <input type="file" required @change="handleFileUpload" class="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100">
              </div>

              <button type="submit" :disabled="isSubmittingMoM" class="w-full bg-slate-800 hover:bg-slate-700 text-white font-bold py-3 rounded-lg shadow-sm transition-all mt-4 text-sm disabled:opacity-50">
                {{ isSubmittingMoM ? 'Saving...' : 'Save to Archive' }}
              </button>
            </form>
          </div>
        </div>

        <div :class="[authStore.user?.role === 'admin' ? 'col-span-1 lg:col-span-2' : 'col-span-1 lg:col-span-3', 'bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden']">
          <div class="bg-slate-50 px-6 py-4 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <h3 class="text-base md:text-lg font-bold text-slate-800">Minutes Archive</h3>
            <div class="relative w-full sm:w-64">
              <input type="text" v-model="momSearchQuery" placeholder="Search agendas or dates..." class="w-full rounded-full border border-slate-300 py-1.5 pl-9 pr-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none">
              <svg class="w-4 h-4 text-slate-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
          </div>
          
          <div class="p-6">
            <div v-if="filteredMoMs.length === 0" class="border border-dashed border-slate-300 rounded-lg p-10 text-center bg-slate-50">
              <p class="text-slate-500 font-medium">No meeting records found.</p>
            </div>
            
            <div v-else class="space-y-4">
              <div v-for="mom in filteredMoMs" :key="mom.id" class="border border-slate-200 rounded-xl overflow-hidden shadow-sm transition-all bg-white">
                
                <div @click="toggleMoM(mom.id)" class="px-5 py-4 cursor-pointer hover:bg-slate-50 flex items-center justify-between group">
                  <div class="flex items-center gap-4">
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

                <div v-if="expandedMoMs.includes(mom.id)" class="border-t border-slate-100 bg-slate-50 px-5 py-4">
                  <div class="mb-4">
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">Attendees</p>
                    <p class="text-sm text-slate-700">{{ mom.attendees || 'Not specified' }}</p>
                  </div>
                  
                  <div v-if="mom.content">
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Meeting Notes</p>
                    <div class="bg-white border border-slate-200 rounded-lg p-4 text-sm text-slate-700 whitespace-pre-wrap leading-relaxed">
                      {{ mom.content }}
                    </div>
                  </div>

                  <div v-if="mom.file_path" class="bg-white border border-slate-200 rounded-lg p-4 flex items-center justify-between">
                    <div class="flex items-center gap-3 overflow-hidden">
                      <svg class="w-6 h-6 text-slate-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                      <span class="text-sm font-medium text-slate-700 truncate">{{ mom.file_name }}</span>
                    </div>
                    <button @click="downloadMoM(mom.id, mom.file_name)" class="bg-slate-100 hover:bg-blue-50 text-blue-600 font-bold py-1.5 px-4 rounded text-xs transition-colors shrink-0 border border-slate-200">
                      Download
                    </button>
                  </div>
                  
                  <div v-if="authStore.user?.role === 'admin'" class="mt-4 flex justify-end">
                    <button @click="removeMoM(mom.id)" class="text-xs text-red-500 hover:text-red-700 font-bold underline">Delete Record</button>
                  </div>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

// --- ROUTER & STORE INITIATION ---
const router = useRouter()
const authStore = useAuthStore()

// --- LOGOUT FUNCTION ---
const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

// Constants
const TIME_SLOTS = [
  { id: 1, label: "9:15 AM - 10:15 AM" }, { id: 2, label: "10:15 AM - 11:15 AM" },
  { id: 3, label: "11:15 AM - 12:15 PM" }, { id: 4, label: "1:00 PM - 2:00 PM" },
  { id: 5, label: "2:00 PM - 3:00 PM" }, { id: 6, label: "3:00 PM - 4:00 PM" }
]

const TABS = [
  { id: 'daily', label: 'Daily Report', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>' },
  { id: 'attendance', label: 'Attendance', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>' },
  { id: 'records', label: 'Records', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path></svg>' },
  { id: 'mom', label: 'Minutes of Meet', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>' },
  { id: 'holidays', label: 'Holidays', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>' },
  { id: 'users', label: 'Users & Teams', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>' }
]

const AVAILABLE_TEAMS = ["Digi Yatra", "OCR", "FHIR", "MIRTH Connect", "ChatBot", "Blood Connect", "Management"]

// --- NEW PHASE 1 ADDITIONS ---

// 1. Rename to BASE
const BASE_ORDERED_ROLLS = [
  "25E51M0503", "24E51A6634", "24E51A6614", "24E51A6633", 
  "24E51A6628", "24E51A6641", "24E51A6609", "24E51A6665", 
  "23E51A6650", "23E51A6783", "24E55A0312", "23E51A67C5", 
  "23E51A0561", "23E51A0508", "23E51A6708", "23E51A6711", 
  "24E55A6604", "23E51A0514", "23E51A6799", "23E51A0503", 
  "24E51A6618", "24E51A6650", "23E51A05G4", "23E51A6673"
]

// 2. Add the intelligent merging logic
const dynamicOrderedRolls = computed(() => {
  const rolls = [...BASE_ORDERED_ROLLS] // Start with your required order
  
  // Scan the live database of users
  allUsers.value.forEach(user => {
    // If we find a new user not in the list, append them to the end
    // (We also ignore the 'ADMIN' and 'VIEWER' accounts so they don't show up in attendance)
    if (!rolls.includes(user.rollNumber) && user.rollNumber !== 'ADMIN' && user.rollNumber !== 'VIEWER') {
      rolls.push(user.rollNumber)
    }
  })
  
  return rolls
})

// NEW: Formats the specific hours array (e.g., "1, 3, 4, 5 hours")
const formatHoursForRoll = (roll) => {
  const log = filteredLogs.value.find(l => l.rollNumber === roll)
  if (log && log.hours && log.hours.length > 0) {
    // Sort the hours numerically just in case they were clicked out of order
    const sortedHours = [...log.hours].sort((a, b) => a - b)
    return `${sortedHours.join(', ')} hours`
  }
  return '0 hours' // Fallback for absent students
}

// Core State
const activeTab = ref('daily')
const selectedDate = ref(new Date().toISOString().split('T')[0])
const allLogs = ref([])
const allUsers = ref([])
const allHolidays = ref([])
const allMoMs = ref([]) // NEW: MoM Data

// Form State
const newHolidayDate = ref('')
const newHolidayName = ref('')
const editingUser = ref(null)

// NEW: MoM States
const momSearchQuery = ref('')
const expandedMoMs = ref([])
const momFormMode = ref('text')
const isSubmittingMoM = ref(false)
const newMomDate = ref(new Date().toISOString().split('T')[0])
const newMomAgenda = ref('')
const newMomAttendees = ref('')
const newMomContent = ref('')
const newMomFile = ref(null)

// --- API FETCHING ---
const fetchAllData = async () => {
  try {
    const [logsRes, usersRes, holidaysRes, momRes] = await Promise.all([
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/holidays/`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/`) // NEW
    ])
    
    const logsData = await logsRes.json()
    allLogs.value = Array.isArray(logsData) ? logsData : []
    
    const usersData = await usersRes.json()
    allUsers.value = Array.isArray(usersData) ? usersData : []

    const holidaysData = await holidaysRes.json()
    allHolidays.value = Array.isArray(holidaysData) ? holidaysData : []

    const momData = await momRes.json()
    allMoMs.value = Array.isArray(momData) ? momData : [] // NEW
  } catch (err) {
    console.error("Failed to load dashboard data from API.")
  }
}

onMounted(fetchAllData)

// --- MoM LOGIC ---
const handleFileUpload = (event) => {
  newMomFile.value = event.target.files[0]
}

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

const submitMoM = async () => {
  isSubmittingMoM.value = true
  try {
    let res;
    // Handle Text Notes
    if (momFormMode.value === 'text') {
      res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date: newMomDate.value,
          agenda: newMomAgenda.value,
          attendees: newMomAttendees.value,
          content: newMomContent.value,
          created_by: authStore.user?.name || 'Admin'
        })
      })
    } 
    // Handle File Uploads
    else {
      const formData = new FormData()
      formData.append('date', newMomDate.value)
      formData.append('agenda', newMomAgenda.value)
      formData.append('attendees', newMomAttendees.value)
      formData.append('created_by', authStore.user?.name || 'Admin')
      formData.append('file', newMomFile.value)

      res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/upload`, {
        method: 'POST',
        body: formData
      })
    }

    if (res.ok) {
      await fetchAllData()
      newMomAgenda.value = ''
      newMomAttendees.value = ''
      newMomContent.value = ''
      newMomFile.value = null
      const fileInput = document.querySelector('input[type="file"]')
      if(fileInput) fileInput.value = ''
    } else {
      alert("Failed to save Meeting Minutes.")
    }
  } catch (err) {
    alert("Network error. Could not connect to backend.")
  } finally {
    isSubmittingMoM.value = false
  }
}

const downloadMoM = async (id, filename) => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/download/${id}`)
    if (!res.ok) throw new Error('File not found')
    
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename || `Meeting_Notes_${id}`
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (error) {
    alert("Could not download file. It may have been cleared from ephemeral storage.")
  }
}

const removeMoM = async (id) => {
  if (!confirm("Are you sure you want to permanently delete this meeting record?")) return
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/${id}`, { method: 'DELETE' })
    if (res.ok) await fetchAllData()
  } catch (err) {
    console.error(err)
  }
}

// --- HOLIDAY LOGIC ---
const submitHoliday = async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/holidays/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date: newHolidayDate.value, name: newHolidayName.value })
    })
    if (res.ok) {
      await fetchAllData()
      newHolidayDate.value = ''
      newHolidayName.value = ''
    } else {
      const errorData = await res.json()
      alert(`Error: ${errorData.detail || 'Could not declare holiday.'}`)
    }
  } catch (err) {
    alert("Network error. Could not connect to backend.")
  }
}

const removeHoliday = async (id) => {
  if (!confirm("Are you sure you want to delete this holiday?")) return
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/holidays/${id}`, { method: 'DELETE' })
    if (res.ok) await fetchAllData()
  } catch (err) {
    console.error(err)
  }
}

// --- USER MANAGEMENT LOGIC ---
const startEdit = (user) => {
  editingUser.value = { ...user }
}

const saveUserEdit = async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/${editingUser.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editingUser.value)
    })
    if (res.ok) {
      await fetchAllData()
      editingUser.value = null
    } else {
      alert("Failed to update user profile.")
    }
  } catch (err) {
    alert("Network error.")
  }
}

const removeUser = async (id) => {
  if (!confirm("WARNING: Are you sure you want to permanently delete this user? This cannot be undone.")) return
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/${id}`, { method: 'DELETE' })
    if (res.ok) await fetchAllData()
  } catch (err) {
    console.error(err)
  }
}

// --- LOG COMPUTEDS & HELPERS ---
const filteredLogs = computed(() => {
  const dayLogs = allLogs.value.filter(log => log.date === selectedDate.value)
  const uniqueLogsMap = new Map()
  dayLogs.forEach(log => { uniqueLogsMap.set(log.rollNumber, log) })
  return Array.from(uniqueLogsMap.values())
})

const formattedSelectedDate = computed(() => new Date(selectedDate.value).toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' }))

const groupedLogs = computed(() => {
  const groups = {}
  filteredLogs.value.forEach(log => {
    if (!groups[log.team]) groups[log.team] = []
    groups[log.team].push(log)
  })
  return groups
})

const teamProgressUpdates = computed(() => {
  const groups = {}
  filteredLogs.value.forEach(log => {
    if (log.todayLog && log.todayLog.trim().length > 0) {
      if (!groups[log.team]) groups[log.team] = []
      groups[log.team].push(log)
    }
  })
  return groups
})

const uniqueMembersPresent = computed(() => {
  const uniqueRolls = new Set(filteredLogs.value.map(log => log.rollNumber))
  return uniqueRolls.size
})

const activeTeamsCount = computed(() => Object.keys(groupedLogs.value).length)

const getMembersForHourUI = (hourId) => {
  const members = filteredLogs.value
    .filter(log => log.hours?.includes(hourId))
    .map(log => `${log.name} (${log.rollNumber})`)
  return [...new Set(members)]
}

const getRollsForHourPDF = (hourId) => {
  const rolls = filteredLogs.value
    .filter(log => log.hours?.includes(hourId))
    .map(log => log.rollNumber)
  return [...new Set(rolls)]
}

// --- PDF & EXPORT ---
const generatePDF = () => {
  const doc = new jsPDF()
  doc.setFontSize(18)
  doc.text(`Project Daily Report - ${formattedSelectedDate.value}`, 14, 22)

  const presenceTable = TIME_SLOTS.map(slot => [
    slot.label, 
    getRollsForHourPDF(slot.id).join(', ') || 'None' 
  ])

  doc.setFontSize(14)
  doc.text("1. Hourly Presence Breakdown", 14, 35)
  autoTable(doc, {
    startY: 40,
    head: [['Time Slot', 'Roll Numbers Present']],
    body: presenceTable,
    theme: 'grid',
    headStyles: { fillColor: [21, 101, 192] },
    styles: { cellPadding: 3, overflow: 'linebreak' }
  })

  const finalY = doc.lastAutoTable?.finalY || 40
  doc.text("2. Team Progress Updates", 14, finalY + 15)
  
  const progressData = Object.entries(teamProgressUpdates.value).map(([team, logs]) => {
    const combinedUpdates = logs.map(log => `• ${log.todayLog.trim()}`).join('\n')
    return [team, combinedUpdates]
  })

  if (progressData.length === 0) {
    progressData.push(['-', 'No written updates provided today.'])
  }

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

const generateAttendancePDF = () => {
  const doc = new jsPDF()
  doc.setFontSize(18)
  doc.text(`Attendance Report - ${formattedSelectedDate.value}`, 14, 22)

  // USE THE NEW FORMATTER HERE
  const attendanceData = dynamicOrderedRolls.value.map(roll => [
    roll, 
    formatHoursForRoll(roll)
  ])

  autoTable(doc, {
    startY: 30,
    head: [['Roll Number', 'Hours Attended']],
    body: attendanceData,
    theme: 'grid',
    headStyles: { fillColor: [21, 101, 192] },
    styles: { cellPadding: 4 },
    columnStyles: { 0: { fontStyle: 'bold' } }
  })

  doc.save(`Attendance_Report_${selectedDate.value}.pdf`)
}

const copyAttendance = () => {
  let text = `Attendance for ${formattedSelectedDate.value}\n\n`
  
  // USE THE NEW FORMATTER HERE
  dynamicOrderedRolls.value.forEach(roll => {
    text += `${roll} - ${formatHoursForRoll(roll)}\n`
  })
  
  navigator.clipboard.writeText(text)
  alert("Attendance copied to clipboard!")
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>