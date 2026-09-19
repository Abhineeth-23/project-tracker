<template>
  <div class="min-h-screen bg-slate-50 font-sans pb-12">
    <header :class="['text-white sticky top-0 z-40 shadow-sm transition-colors duration-200', activeCompany === 'Succeed International' ? 'bg-[#1e40af]' : 'bg-[#193099]']">
      <div class="px-4 md:px-6 py-3.5 flex flex-col sm:flex-row justify-between items-center gap-3">
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-center sm:justify-start">
          <div class="p-2 bg-white/10 rounded-md border border-white/15 shadow-sm shrink-0">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zm0 7.5l-10-5v2.5l10 5 10-5v-2.5l-10 5zM2 12v2.5l10 5 10-5V12l-10 5-10-5z"/></svg>
          </div>
          <div class="flex items-center gap-2 flex-wrap justify-center sm:justify-start">
            <div class="flex items-center gap-1.5">
              <span class="text-base md:text-lg font-bold tracking-tight text-white">{{ activeCompany }}</span>
              <span class="text-white/40">•</span>
              <span class="text-base md:text-lg font-bold text-white tracking-wide">HITAM</span>
            </div>
            <span class="hidden sm:inline text-white/30 font-light">|</span>
            <span class="text-xs md:text-sm font-medium text-white/80 tracking-wide">Project Tracker</span>
          </div>
        </div>
        <div class="flex items-center space-x-2.5 w-full sm:w-auto justify-between sm:justify-end flex-wrap">
          <!-- Workspace Switcher Pills -->
          <div class="flex items-center bg-black/20 p-1 rounded-md border border-white/15">
            <button 
              @click="switchCompany('CallHealth')" 
              :class="['px-2.5 py-1 rounded text-xs font-semibold transition-all', activeCompany === 'CallHealth' ? 'bg-white text-[#193099] shadow-sm' : 'text-white/80 hover:text-white']"
            >
              CallHealth
            </button>
            <button 
              @click="switchCompany('Succeed International')" 
              :class="['px-2.5 py-1 rounded text-xs font-semibold transition-all', activeCompany === 'Succeed International' ? 'bg-white text-blue-700 shadow-sm' : 'text-white/80 hover:text-white']"
            >
              Succeed Int'l
            </button>
          </div>

          <router-link to="/admin/select-company" class="hidden sm:inline-flex items-center gap-1 text-[11px] font-semibold text-white/90 hover:text-white px-2.5 py-1.5 rounded-md hover:bg-white/10 transition-all border border-white/10" title="Switch Workspace Hub">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
            <span>Hub</span>
          </router-link>

          <span class="text-xs md:text-sm font-medium bg-black/20 px-3 py-1.5 rounded-md border border-white/10 flex items-center gap-1.5">
            <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            <span class="hidden sm:inline">{{ authStore.user?.role === 'viewer' ? 'Executive' : 'Admin' }}</span>
            <span class="sm:hidden">{{ authStore.user?.role === 'viewer' ? 'Exec' : 'Admin' }}</span>
          </span>
          <button @click="handleLogout" class="hover:bg-white/20 px-2.5 py-1.5 rounded-md transition-all flex items-center gap-1" title="Secure Logout">
            <span class="text-xs md:text-sm font-medium">Logout</span>
            <svg class="w-4 h-4 md:w-5 md:h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
          </button>
        </div>
      </div>

      <div :class="['flex px-2 md:px-6 space-x-1 md:space-x-2 pt-1.5 overflow-x-auto no-scrollbar transition-colors border-t border-white/10', activeCompany === 'Succeed International' ? 'bg-[#1e3a8a]' : 'bg-[#12226e]']">
        <button v-for="tab in TABS" :key="tab.id" @click="activeTab = tab.id" :class="['px-4 md:px-5 py-2.5 text-xs md:text-sm font-semibold rounded-t-md transition-all flex items-center gap-2 whitespace-nowrap shrink-0', activeTab === tab.id ? (activeCompany === 'Succeed International' ? 'bg-slate-50 text-blue-700 font-bold' : 'bg-slate-50 text-[#193099] font-bold border-t-2 border-t-[#6fb733]') : 'text-blue-100 hover:bg-white/10']">
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

      <!-- Chronological Daily Progress Feed -->
      <div v-if="activeTab === 'progress'" class="space-y-6">
        <div class="bg-white p-4 md:p-6 rounded-lg border border-slate-200 shadow-sm flex flex-col md:flex-row gap-4 items-center justify-between">
          <div class="w-full md:w-auto">
            <h3 class="text-lg font-bold text-slate-800">Daily Workspace Progress</h3>
            <p class="text-xs text-slate-500 mt-0.5">Explore progress reports across all project teams</p>
          </div>
          
          <div class="flex flex-col sm:flex-row gap-2 w-full md:w-auto items-stretch sm:items-center">
            <div class="bg-slate-100 rounded-xl px-3 py-2 flex items-center border border-slate-200">
              <span class="text-xs font-bold text-slate-500 mr-2 uppercase">Date:</span>
              <input type="date" v-model="feedFilterDate" class="outline-none text-xs font-bold text-slate-700 bg-transparent cursor-pointer">
              <button v-if="feedFilterDate" @click="feedFilterDate = ''" class="ml-2 text-slate-400 hover:text-slate-600 text-xs font-bold font-mono">×</button>
            </div>
            <div class="relative flex-1 sm:flex-none">
              <input type="text" v-model="feedSearchQuery" placeholder="Search logs/names..." class="w-full sm:w-56 rounded-xl border border-slate-200 py-2 pl-8 pr-3 text-xs focus:ring-2 focus:ring-blue-500 outline-none">
              <svg class="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
            </div>
          </div>
        </div>

        <div v-if="filteredFeedDays.length === 0" class="border border-dashed border-slate-300 rounded-lg p-12 text-center bg-white shadow-sm">
          <svg class="w-12 h-12 text-slate-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <p class="text-sm font-semibold text-slate-500">No matching progress updates found.</p>
        </div>

        <div v-else class="space-y-8 relative before:absolute before:inset-y-0 before:left-4 md:before:left-6 before:w-0.5 before:bg-slate-200 pl-8 md:pl-12">
          <div v-for="day in paginatedFeedDays" :key="day.date" class="relative group">
            <div class="absolute left-[-32px] md:left-[-48px] w-6 h-6 md:w-8 md:h-8 rounded-full border-4 border-slate-50 bg-[#193099] shadow-sm z-10 flex items-center justify-center text-white text-[10px] font-bold">
              ✓
            </div>
            
            <div class="bg-white rounded-lg border border-slate-200 shadow-sm p-4 md:p-6 hover:shadow-md transition-shadow">
              <div class="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
                <div>
                  <h4 class="font-extrabold text-slate-800 text-sm md:text-base capitalize">
                    {{ formatFeedDate(day.date) }}
                  </h4>
                  <p class="text-[10px] text-teal-600 font-bold uppercase tracking-wider mt-0.5">
                    {{ day.date }}
                  </p>
                </div>
                <span class="bg-slate-100 text-slate-500 text-[10px] font-bold px-2 py-1 rounded border border-slate-200">
                  {{ day.totalHours }} hrs logged
                </span>
              </div>

              <div class="space-y-6">
                <div v-for="(members, team) in day.teams" :key="team" class="border border-slate-100 rounded-xl overflow-hidden shadow-sm bg-slate-50/50">
                  <div class="bg-teal-50 border-b border-teal-100/50 px-4 py-2 flex justify-between items-center">
                    <span class="text-teal-900 font-extrabold text-xs md:text-sm tracking-wide flex items-center gap-1.5">
                      <span class="w-2 h-2 rounded-full bg-teal-500"></span>
                      {{ team || 'Unassigned' }}
                    </span>
                    <span class="text-[10px] font-bold text-teal-600 bg-white border border-teal-100 px-2 py-0.5 rounded">
                      {{ members.length }} Updates
                    </span>
                  </div>
                  
                  <div class="p-3 divide-y divide-slate-100 bg-white">
                    <div v-for="member in members" :key="member.id" class="py-3 first:pt-0 last:pb-0">
                      <div class="flex justify-between items-start gap-2 mb-1">
                        <span class="text-xs font-bold text-slate-700">
                          {{ member.name }}
                          <span class="font-mono text-[10px] text-slate-400 font-normal ml-1">({{ member.rollNumber }})</span>
                        </span>
                        <span class="text-[9px] font-bold text-slate-400 bg-slate-100 border border-slate-200 px-1.5 py-0.5 rounded shrink-0">
                          {{ member.hours?.length || 0 }} slots
                        </span>
                      </div>
                      
                      <p class="text-xs text-slate-600 leading-relaxed bg-slate-50 rounded-lg p-2.5 border border-slate-100 font-medium">
                        {{ member.todayLog || 'Attendance only' }}
                      </p>
                      
                      <p v-if="member.tomorrowGoal" class="text-[10px] text-teal-700 mt-1.5 flex items-center gap-1">
                        <strong class="uppercase text-[9px] text-teal-500 font-black shrink-0">Next Goal:</strong>
                        <span class="italic font-medium">"{{ member.tomorrowGoal }}"</span>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination Controls -->
        <div v-if="filteredFeedDays.length > feedPageSize" class="mt-8 flex justify-center">
          <div class="inline-flex items-center justify-center bg-slate-800 text-white rounded-xl border border-slate-700 shadow-md p-1 font-mono text-sm">
            <button 
              type="button" 
              @click="prevPage" 
              :disabled="feedCurrentPage === 1" 
              class="px-3 py-1.5 rounded-lg hover:bg-slate-700 disabled:opacity-30 disabled:hover:bg-transparent transition-colors font-bold cursor-pointer"
            >
              &lt;
            </button>
            
            <span class="px-4 py-1.5 font-bold tracking-wide">
              {{ pageStartIdx }} - {{ pageEndIdx }} of {{ filteredFeedDays.length }}
            </span>
            
            <button 
              type="button" 
              @click="nextPage" 
              :disabled="feedCurrentPage * feedPageSize >= filteredFeedDays.length" 
              class="px-3 py-1.5 rounded-lg hover:bg-slate-700 disabled:opacity-30 disabled:hover:bg-transparent transition-colors font-bold cursor-pointer"
            >
              &gt;
            </button>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'attendance'" class="space-y-4">
        <!-- Interval Attendance Banner -->
        <div class="bg-blue-50 border border-blue-200 p-3.5 rounded-lg flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 shadow-sm">
          <div class="flex items-center gap-2 text-xs text-blue-900 font-medium">
            <svg class="w-4 h-4 text-blue-700 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>Need attendance across a custom date range? Generate and download multi-day attendance sheets in PDF or Excel.</span>
          </div>
          <button @click="activeTab = 'reports'; reportViewMode = 'attendance'" class="text-xs font-bold bg-[#193099] hover:bg-[#12226e] text-white px-3 py-1.5 rounded transition-colors whitespace-nowrap shadow-sm">
            Generate Multi-Date Sheet →
          </button>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-8">
          <h3 class="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>
            Daily Attendance Summary
          </h3>
        
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-x-8 gap-y-2">
            <div v-for="roll in dynamicOrderedRolls" :key="roll" class="flex justify-between items-center py-2.5 border-b border-slate-100">
              <span class="text-sm font-mono text-slate-700 font-semibold">{{ roll }}</span>
              <span :class="['text-xs font-bold px-2 py-1 rounded', formatHoursForRoll(roll) !== '0 hr' ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-400']">
                {{ formatHoursForRoll(roll) }}
              </span>
            </div>
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

      <!-- Dedicated Periodic Reports Tab -->
      <div v-if="activeTab === 'reports'" class="space-y-6">
        
        <!-- Header Banner & Scope Indicator -->
        <div class="bg-white p-5 md:p-6 rounded-lg border border-slate-200 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span :class="['w-2.5 h-2.5 rounded-full shrink-0', activeCompany === 'Succeed International' ? 'bg-blue-600' : 'bg-[#6fb733]']"></span>
              <span class="text-xs font-bold uppercase tracking-wider text-slate-500">{{ activeCompany }} Workspace</span>
            </div>
            <h2 class="text-xl md:text-2xl font-black text-slate-900 tracking-tight">Project Activity & Attendance Reports</h2>
            <p class="text-xs md:text-sm text-slate-500 mt-0.5">Filter activity logs by any date interval, export consolidated PDF/CSV reports, and inspect student & team metrics.</p>
          </div>

          <!-- Quick Action Buttons -->
          <div class="flex flex-wrap items-center gap-2 w-full md:w-auto">
            <!-- PDF Activity Report -->
            <button 
              @click="downloadReportPDF" 
              :class="['px-3.5 py-2 text-xs font-bold text-white rounded-md transition-colors flex items-center gap-1.5 shadow-sm', activeCompany === 'Succeed International' ? 'bg-blue-700 hover:bg-blue-800' : 'bg-[#193099] hover:bg-[#12226e]']"
              title="Export complete activity logs report as formatted PDF"
            >
              <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              Activity Report (PDF)
            </button>

            <!-- PDF Attendance Sheet -->
            <button 
              @click="downloadIntervalAttendancePDF" 
              class="px-3.5 py-2 text-xs font-bold text-slate-800 bg-amber-50 border border-amber-300 hover:bg-amber-100 rounded-md transition-colors flex items-center gap-1.5 shadow-sm"
              title="Download official attendance sheet for this interval as PDF"
            >
              <svg class="w-4 h-4 shrink-0 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
              Attendance Sheet (PDF)
            </button>

            <!-- CSV Attendance Matrix -->
            <button 
              @click="downloadIntervalAttendanceMatrixCSV" 
              class="px-3.5 py-2 text-xs font-bold text-blue-800 bg-blue-50 border border-blue-300 hover:bg-blue-100 rounded-md transition-colors flex items-center gap-1.5 shadow-sm"
              title="Export complete date-by-date attendance matrix as CSV/Excel"
            >
              <svg class="w-4 h-4 shrink-0 text-blue-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
              Attendance Matrix (Excel)
            </button>

            <!-- CSV Activity Logs -->
            <button 
              @click="downloadReportCSV" 
              class="px-3.5 py-2 text-xs font-bold text-emerald-800 bg-emerald-50 border border-emerald-300 hover:bg-emerald-100 rounded-md transition-colors flex items-center gap-1.5 shadow-sm"
              title="Export filtered activity records as CSV spreadsheet"
            >
              <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              Activity CSV
            </button>

            <!-- Copy Summary -->
            <button 
              @click="copyReportSummary" 
              class="px-3 py-2 text-xs font-semibold text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 rounded-md transition-colors flex items-center gap-1.5 shadow-sm"
              title="Copy text summary to clipboard"
            >
              <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
              Copy
            </button>
          </div>
        </div>

        <!-- Filter & Interval Configuration Card -->
        <div class="bg-white p-5 rounded-lg border border-slate-200 shadow-sm space-y-4">
          <!-- Row 1: Date Range & Preset Intervals -->
          <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 border-b border-slate-100 pb-4">
            <div class="flex flex-wrap items-center gap-3 w-full lg:w-auto">
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-700 uppercase tracking-wide">Interval:</span>
                <div class="flex items-center gap-1.5 bg-slate-50 border border-slate-300 rounded-md px-2.5 py-1.5 shadow-inner">
                  <span class="text-xs text-slate-500 font-medium">From:</span>
                  <input type="date" v-model="reportStartDate" class="text-xs font-semibold text-slate-800 bg-transparent outline-none">
                </div>
                <span class="text-slate-400 font-bold">→</span>
                <div class="flex items-center gap-1.5 bg-slate-50 border border-slate-300 rounded-md px-2.5 py-1.5 shadow-inner">
                  <span class="text-xs text-slate-500 font-medium">To:</span>
                  <input type="date" v-model="reportEndDate" class="text-xs font-semibold text-slate-800 bg-transparent outline-none">
                </div>
              </div>
            </div>

            <!-- Quick Presets -->
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="text-xs text-slate-400 font-medium mr-1">Presets:</span>
              <button 
                v-for="p in [
                  { id: 'today', label: 'Today' },
                  { id: '7days', label: '7 Days' },
                  { id: '14days', label: '14 Days' },
                  { id: '30days', label: '30 Days' },
                  { id: 'thisMonth', label: 'This Month' },
                  { id: 'allTime', label: 'All Time' }
                ]" 
                :key="p.id" 
                @click="setReportInterval(p.id)"
                :class="['px-2.5 py-1 rounded text-xs font-semibold border transition-all', activeReportPreset === p.id ? (activeCompany === 'Succeed International' ? 'bg-blue-50 text-blue-700 border-blue-300' : 'bg-green-50 text-[#193099] border-[#6fb733]') : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50']"
              >
                {{ p.label }}
              </button>
            </div>
          </div>

          <!-- Row 2: Secondary Dropdowns & Keyword Search -->
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 pt-1">
            <!-- Team Filter -->
            <div>
              <label class="block text-xs font-bold text-slate-600 uppercase mb-1">Filter Team</label>
              <select 
                v-model="reportTeamFilter" 
                class="w-full rounded-md border border-slate-300 py-1.5 px-2.5 text-xs text-slate-800 font-medium bg-white outline-none focus:ring-2 focus:ring-slate-400"
              >
                <option value="">All Teams ({{ allTeams.length }})</option>
                <option v-for="team in allTeams" :key="team.id || team.name" :value="team.name">
                  {{ team.name }}
                </option>
              </select>
            </div>

            <!-- Student Filter -->
            <div>
              <label class="block text-xs font-bold text-slate-600 uppercase mb-1">Filter Student</label>
              <select 
                v-model="reportStudentFilter" 
                class="w-full rounded-md border border-slate-300 py-1.5 px-2.5 text-xs text-slate-800 font-medium bg-white outline-none focus:ring-2 focus:ring-slate-400"
              >
                <option value="">All Students ({{ allUsers.filter(u => u.role !== 'admin' && u.role !== 'viewer').length }})</option>
                <option v-for="user in allUsers.filter(u => u.role !== 'admin' && u.role !== 'viewer')" :key="user.id" :value="user.rollNumber">
                  {{ user.name }} ({{ user.rollNumber }})
                </option>
              </select>
            </div>

            <!-- Minimum Hours -->
            <div>
              <label class="block text-xs font-bold text-slate-600 uppercase mb-1">Hours Logged</label>
              <select 
                v-model="reportMinHours" 
                class="w-full rounded-md border border-slate-300 py-1.5 px-2.5 text-xs text-slate-800 font-medium bg-white outline-none focus:ring-2 focus:ring-slate-400"
              >
                <option value="all">All Logs (Any)</option>
                <option value="with_hours">Logs with Hours (>0h)</option>
                <option value="half_day">Half-Day or more (≥3h)</option>
                <option value="full_day">Full-Day (≥5h)</option>
              </select>
            </div>

            <!-- Search Keyword -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <label class="block text-xs font-bold text-slate-600 uppercase">Search Details</label>
                <button 
                  v-if="reportTeamFilter || reportStudentFilter || reportSearchQuery || reportMinHours !== 'all'" 
                  @click="resetReportFilters" 
                  class="text-[11px] font-bold text-red-600 hover:underline"
                >
                  Clear All
                </button>
              </div>
              <input 
                type="text" 
                v-model="reportSearchQuery" 
                placeholder="Search tasks, roll, names..." 
                class="w-full rounded-md border border-slate-300 py-1.5 px-2.5 text-xs text-slate-800 outline-none focus:ring-2 focus:ring-slate-400"
              >
            </div>
          </div>
        </div>

        <!-- Metric KPI Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="bg-white p-4 md:p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col justify-between">
            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Submissions</span>
            <div class="mt-2 flex items-baseline justify-between">
              <span class="text-2xl md:text-3xl font-black text-slate-900">{{ filteredReportLogs.length }}</span>
              <span class="text-xs font-semibold text-slate-500">entries</span>
            </div>
            <span class="text-[11px] text-slate-400 mt-1">In selected range</span>
          </div>

          <div class="bg-white p-4 md:p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col justify-between">
            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Productive Hours</span>
            <div class="mt-2 flex items-baseline justify-between">
              <span :class="['text-2xl md:text-3xl font-black', activeCompany === 'Succeed International' ? 'text-blue-700' : 'text-[#193099]']">{{ reportTotalHours }}</span>
              <span class="text-xs font-semibold text-slate-500">hours logged</span>
            </div>
            <span class="text-[11px] text-slate-400 mt-1">Across all filtered logs</span>
          </div>

          <div class="bg-white p-4 md:p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col justify-between">
            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Students</span>
            <div class="mt-2 flex items-baseline justify-between">
              <span class="text-2xl md:text-3xl font-black text-slate-900">{{ reportActiveStudentsCount }}</span>
              <span class="text-xs font-semibold text-slate-500">of {{ allUsers.filter(u => u.role !== 'admin' && u.role !== 'viewer').length }} total</span>
            </div>
            <span class="text-[11px] text-slate-400 mt-1">{{ reportActiveTeamsCount }} teams active</span>
          </div>

          <div class="bg-white p-4 md:p-5 rounded-lg border border-slate-200 shadow-sm flex flex-col justify-between">
            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider">Avg Hours / Student</span>
            <div class="mt-2 flex items-baseline justify-between">
              <span class="text-2xl md:text-3xl font-black text-emerald-700">{{ reportAvgHoursPerStudent }}</span>
              <span class="text-xs font-semibold text-slate-500">hrs / member</span>
            </div>
            <span class="text-[11px] text-slate-400 mt-1">Productivity rate</span>
          </div>
        </div>

        <!-- View Mode Switcher -->
        <div class="bg-white rounded-lg border border-slate-200 p-1.5 flex items-center justify-between shadow-sm flex-wrap gap-2">
          <div class="flex items-center space-x-1">
            <button 
              @click="reportViewMode = 'logs'" 
              :class="['px-3.5 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-1.5', reportViewMode === 'logs' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100']"
            >
              <span>Detailed Activity Logs</span>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded-full font-bold', reportViewMode === 'logs' ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600']">{{ filteredReportLogs.length }}</span>
            </button>
            <button 
              @click="reportViewMode = 'students'" 
              :class="['px-3.5 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-1.5', reportViewMode === 'students' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100']"
            >
              <span>Student Contribution Matrix</span>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded-full font-bold', reportViewMode === 'students' ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600']">{{ studentReportMatrix.length }}</span>
            </button>
            <button 
              @click="reportViewMode = 'attendance'" 
              :class="['px-3.5 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-1.5', reportViewMode === 'attendance' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100']"
            >
              <span>Attendance Sheet</span>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded-full font-bold', reportViewMode === 'attendance' ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600']">{{ attendanceSheetData.length }}</span>
            </button>
            <button 
              @click="reportViewMode = 'teams'" 
              :class="['px-3.5 py-1.5 rounded-md text-xs font-bold transition-all flex items-center gap-1.5', reportViewMode === 'teams' ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100']"
            >
              <span>Team Breakdown</span>
              <span :class="['text-[10px] px-1.5 py-0.5 rounded-full font-bold', reportViewMode === 'teams' ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-600']">{{ teamReportMatrix.length }}</span>
            </button>
          </div>

          <!-- Secondary Quick Download button for student matrix or attendance mode -->
          <div v-if="reportViewMode === 'students'" class="flex items-center gap-2">
            <button 
              @click="downloadStudentMatrixPDF" 
              class="text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded border border-slate-300 flex items-center gap-1"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              Export Matrix PDF
            </button>
            <button 
              @click="downloadStudentMatrixCSV" 
              class="text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded border border-slate-300 flex items-center gap-1"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              Export Matrix CSV
            </button>
          </div>

          <div v-if="reportViewMode === 'attendance'" class="flex items-center gap-2">
            <button 
              @click="downloadIntervalAttendancePDF" 
              class="text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded border border-slate-300 flex items-center gap-1"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              Sheet PDF
            </button>
            <button 
              @click="downloadIntervalAttendanceMatrixCSV" 
              class="text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 px-3 py-1 rounded border border-slate-300 flex items-center gap-1"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
              Matrix CSV
            </button>
          </div>
        </div>

        <!-- View 1: Detailed Logs Table -->
        <div v-if="reportViewMode === 'logs'" class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div class="overflow-x-auto no-scrollbar">
            <table class="w-full text-left border-collapse min-w-[900px]">
              <thead>
                <tr class="bg-slate-50 text-slate-600 text-xs font-bold uppercase tracking-wider border-b border-slate-200">
                  <th class="py-3 px-4">Date</th>
                  <th class="py-3 px-4">Student</th>
                  <th class="py-3 px-4">Team</th>
                  <th class="py-3 px-4 text-center">Hours</th>
                  <th class="py-3 px-4">Work Completed</th>
                  <th class="py-3 px-4">Next Goal</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-if="filteredReportLogs.length === 0">
                  <td colspan="6" class="p-12 text-center text-slate-500">
                    <p class="text-sm font-semibold">No activity logs found for this date interval and criteria.</p>
                    <p class="text-xs text-slate-400 mt-1">Try expanding your date range or adjusting the filters above.</p>
                  </td>
                </tr>
                <tr v-else v-for="log in filteredReportLogs" :key="log.id" class="hover:bg-slate-50 transition-colors">
                  <td class="py-3 px-4 text-xs font-mono text-slate-700 whitespace-nowrap">{{ log.date }}</td>
                  <td class="py-3 px-4 whitespace-nowrap">
                    <p class="text-xs font-bold text-slate-800">{{ log.name }}</p>
                    <p class="text-[11px] font-mono text-slate-500">{{ log.rollNumber }}</p>
                  </td>
                  <td class="py-3 px-4 whitespace-nowrap">
                    <span class="inline-block bg-slate-100 text-slate-700 border border-slate-200 text-xs font-semibold px-2 py-0.5 rounded">
                      {{ log.team || 'Unassigned' }}
                    </span>
                  </td>
                  <td class="py-3 px-4 text-center whitespace-nowrap">
                    <span :class="['inline-block font-bold text-xs px-2 py-0.5 rounded-full border', (log.hours?.length || 0) >= 4 ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : ((log.hours?.length || 0) > 0 ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-slate-100 text-slate-500 border-slate-200')]">
                      {{ log.hours?.length || 0 }}h
                    </span>
                  </td>
                  <td class="py-3 px-4 text-xs text-slate-700 max-w-xs leading-relaxed">
                    <span v-if="log.todayLog && log.todayLog.trim()">{{ log.todayLog }}</span>
                    <span v-else class="text-slate-400 italic">Attendance only</span>
                  </td>
                  <td class="py-3 px-4 text-xs text-slate-600 max-w-[220px] leading-relaxed">
                    <span v-if="log.tomorrowGoal && log.tomorrowGoal.trim()">{{ log.tomorrowGoal }}</span>
                    <span v-else class="text-slate-400 italic">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="bg-slate-50 px-4 py-2.5 border-t border-slate-200 text-xs text-slate-500 flex justify-between items-center">
            <span>Showing {{ filteredReportLogs.length }} record{{ filteredReportLogs.length === 1 ? '' : 's' }}</span>
            <span>Interval: {{ reportStartDate }} to {{ reportEndDate }}</span>
          </div>
        </div>

        <!-- View 2: Student Contribution Matrix -->
        <div v-if="reportViewMode === 'students'" class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div class="overflow-x-auto no-scrollbar">
            <table class="w-full text-left border-collapse min-w-[800px]">
              <thead>
                <tr class="bg-slate-50 text-slate-600 text-xs font-bold uppercase tracking-wider border-b border-slate-200">
                  <th class="py-3 px-4">Roll Number</th>
                  <th class="py-3 px-4">Student Name</th>
                  <th class="py-3 px-4">Team</th>
                  <th class="py-3 px-4 text-center">Active Days</th>
                  <th class="py-3 px-4 text-center">Total Hours</th>
                  <th class="py-3 px-4 text-center">Avg Hours/Day</th>
                  <th class="py-3 px-4 text-right">Individual Report</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-if="studentReportMatrix.length === 0">
                  <td colspan="7" class="p-8 text-center text-slate-500 text-sm">No student data available.</td>
                </tr>
                <tr v-else v-for="student in studentReportMatrix" :key="student.rollNumber" class="hover:bg-slate-50 transition-colors">
                  <td class="py-3 px-4 text-xs font-mono font-bold text-slate-800">{{ student.rollNumber }}</td>
                  <td class="py-3 px-4 text-xs font-semibold text-slate-800">{{ student.name }}</td>
                  <td class="py-3 px-4 text-xs text-slate-600">
                    <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-200 text-xs font-medium">{{ student.team }}</span>
                  </td>
                  <td class="py-3 px-4 text-center text-xs font-semibold text-slate-700">{{ student.activeDays }}</td>
                  <td class="py-3 px-4 text-center whitespace-nowrap">
                    <span :class="['font-bold text-xs px-2 py-0.5 rounded-full border', student.totalHours >= 20 ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : (student.totalHours > 0 ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-slate-100 text-slate-400 border-slate-200')]">
                      {{ student.totalHours }} hrs
                    </span>
                  </td>
                  <td class="py-3 px-4 text-center text-xs font-mono text-slate-600">{{ student.avgHoursPerDay }}h</td>
                  <td class="py-3 px-4 text-right">
                    <button 
                      @click="downloadSingleStudentPDF(student.rollNumber)" 
                      :disabled="student.activeDays === 0"
                      class="text-xs font-bold text-blue-700 hover:text-blue-900 border border-blue-200 hover:bg-blue-50 px-2.5 py-1 rounded transition-colors disabled:opacity-40 disabled:pointer-events-none"
                    >
                      Export PDF
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- View 3: Dedicated Interval Attendance Sheet -->
        <div v-if="reportViewMode === 'attendance'" class="space-y-4">
          <!-- Summary Cards for Attendance -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
            <div class="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
              <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Active Working Days</span>
              <p class="text-2xl font-black text-slate-900 mt-1">{{ intervalWorkingDates.length }} <span class="text-xs font-medium text-slate-500">days</span></p>
              <span class="text-[10px] text-slate-400">In {{ reportStartDate }} to {{ reportEndDate }}</span>
            </div>
            <div class="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
              <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Average Attendance</span>
              <p :class="['text-2xl font-black mt-1', intervalAvgAttendanceRate >= 75 ? 'text-emerald-700' : 'text-amber-600']">{{ intervalAvgAttendanceRate }}%</p>
              <span class="text-[10px] text-slate-400">Across {{ attendanceSheetData.length }} enrolled students</span>
            </div>
            <div class="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
              <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Eligible (≥ 75%)</span>
              <p class="text-2xl font-black text-emerald-700 mt-1">{{ eligibleStudentsCount }} <span class="text-xs font-medium text-slate-500">students</span></p>
              <span class="text-[10px] text-slate-400">Clear for evaluation</span>
            </div>
            <div class="bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
              <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Shortage (&lt; 75%)</span>
              <p class="text-2xl font-black text-red-600 mt-1">{{ shortageStudentsCount }} <span class="text-xs font-medium text-slate-500">students</span></p>
              <span class="text-[10px] text-slate-400">Below attendance threshold</span>
            </div>
          </div>

          <!-- Attendance Table -->
          <div class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
            <div class="overflow-x-auto no-scrollbar">
              <table class="w-full text-left border-collapse min-w-[850px]">
                <thead>
                  <tr class="bg-slate-50 text-slate-600 text-xs font-bold uppercase tracking-wider border-b border-slate-200">
                    <th class="py-3 px-4">Roll Number</th>
                    <th class="py-3 px-4">Student Name</th>
                    <th class="py-3 px-4">Team</th>
                    <th class="py-3 px-4 text-center">Days Present</th>
                    <th class="py-3 px-4 text-center">Total Hours</th>
                    <th class="py-3 px-4 text-center">Attendance %</th>
                    <th class="py-3 px-4 text-center">Status</th>
                    <th class="py-3 px-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  <tr v-if="attendanceSheetData.length === 0">
                    <td colspan="8" class="p-8 text-center text-slate-500 text-sm">No attendance records found for this interval.</td>
                  </tr>
                  <tr v-else v-for="student in attendanceSheetData" :key="student.rollNumber" class="hover:bg-slate-50 transition-colors">
                    <td class="py-3 px-4 text-xs font-mono font-bold text-slate-800">{{ student.rollNumber }}</td>
                    <td class="py-3 px-4 text-xs font-semibold text-slate-800">{{ student.name }}</td>
                    <td class="py-3 px-4 text-xs text-slate-600">
                      <span class="bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-200 text-xs font-medium">{{ student.team }}</span>
                    </td>
                    <td class="py-3 px-4 text-center text-xs font-semibold text-slate-700 whitespace-nowrap">
                      {{ student.presentDays }} <span class="text-slate-400 font-normal">/ {{ intervalWorkingDates.length }}</span>
                    </td>
                    <td class="py-3 px-4 text-center text-xs font-bold text-slate-800 whitespace-nowrap">{{ student.totalHours }}h</td>
                    <td class="py-3 px-4 text-center">
                      <div class="flex items-center justify-center gap-2">
                        <div class="w-16 bg-slate-100 rounded-full h-2 overflow-hidden">
                          <div 
                            :class="['h-full rounded-full', student.percentage >= 75 ? 'bg-emerald-600' : (student.percentage >= 50 ? 'bg-amber-500' : 'bg-red-500')]" 
                            :style="{ width: `${Math.min(100, student.percentage)}%` }"
                          ></div>
                        </div>
                        <span :class="['text-xs font-bold font-mono', student.percentage >= 75 ? 'text-emerald-700' : (student.percentage >= 50 ? 'text-amber-700' : 'text-red-600')]">
                          {{ student.percentage }}%
                        </span>
                      </div>
                    </td>
                    <td class="py-3 px-4 text-center whitespace-nowrap">
                      <span :class="['text-[11px] font-bold px-2 py-0.5 rounded-full border', student.percentage >= 75 ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-red-50 text-red-700 border-red-200']">
                        {{ student.percentage >= 75 ? 'Eligible' : 'Shortage' }}
                      </span>
                    </td>
                    <td class="py-3 px-4 text-right">
                      <button 
                        @click="downloadSingleStudentPDF(student.rollNumber)" 
                        class="text-xs font-bold text-blue-700 hover:text-blue-900 border border-blue-200 hover:bg-blue-50 px-2.5 py-1 rounded transition-colors"
                      >
                        Student PDF
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="bg-slate-50 px-4 py-2.5 border-t border-slate-200 text-xs text-slate-500 flex justify-between items-center flex-wrap gap-2">
              <span>Showing attendance for {{ attendanceSheetData.length }} students across {{ intervalWorkingDates.length }} active dates</span>
              <div class="flex items-center gap-2">
                <button @click="downloadIntervalAttendancePDF" class="text-xs font-bold text-blue-700 hover:underline">Download PDF Sheet</button>
                <span>•</span>
                <button @click="downloadIntervalAttendanceMatrixCSV" class="text-xs font-bold text-emerald-700 hover:underline">Download Excel Matrix</button>
              </div>
            </div>
          </div>
        </div>

        <!-- View 4: Team Breakdown -->
        <div v-if="reportViewMode === 'teams'" class="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div class="overflow-x-auto no-scrollbar">
            <table class="w-full text-left border-collapse min-w-[700px]">
              <thead>
                <tr class="bg-slate-50 text-slate-600 text-xs font-bold uppercase tracking-wider border-b border-slate-200">
                  <th class="py-3 px-4">Team Name</th>
                  <th class="py-3 px-4 text-center">Enrolled Members</th>
                  <th class="py-3 px-4 text-center">Logs Submitted</th>
                  <th class="py-3 px-4 text-center">Cumulative Hours</th>
                  <th class="py-3 px-4">Project Share</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-if="teamReportMatrix.length === 0">
                  <td colspan="5" class="p-8 text-center text-slate-500 text-sm">No team data available.</td>
                </tr>
                <tr v-else v-for="team in teamReportMatrix" :key="team.name" class="hover:bg-slate-50 transition-colors">
                  <td class="py-3 px-4 text-xs font-bold text-slate-800">{{ team.name }}</td>
                  <td class="py-3 px-4 text-center text-xs text-slate-600 font-semibold">{{ team.memberCount }}</td>
                  <td class="py-3 px-4 text-center text-xs font-semibold text-slate-700">{{ team.logCount }}</td>
                  <td class="py-3 px-4 text-center whitespace-nowrap">
                    <span :class="['font-bold text-xs px-2.5 py-0.5 rounded-full border', activeCompany === 'Succeed International' ? 'bg-blue-50 text-blue-800 border-blue-200' : 'bg-green-50 text-[#193099] border-green-200']">
                      {{ team.totalHours }} hrs
                    </span>
                  </td>
                  <td class="py-3 px-4">
                    <div class="flex items-center gap-2 max-w-xs">
                      <div class="flex-1 bg-slate-100 rounded-full h-2 overflow-hidden">
                        <div 
                          :class="['h-full rounded-full transition-all duration-300', activeCompany === 'Succeed International' ? 'bg-blue-600' : 'bg-[#193099]']" 
                          :style="{ width: `${team.percentage}%` }"
                        ></div>
                      </div>
                      <span class="text-xs font-mono font-bold text-slate-600">{{ team.percentage }}%</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <div v-if="activeTab === 'suggestions'" class="space-y-6">
        <div class="bg-white p-4 md:p-6 rounded-lg border border-slate-200 shadow-sm">
          <h3 class="text-lg font-bold text-slate-800">Suggestions & Features</h3>
          <p class="text-xs text-slate-500 mt-0.5">Manage suggestions and feature requests submitted by all teams.</p>
        </div>

        <div v-if="Object.keys(groupedSuggestions).length === 0" class="border border-dashed border-slate-300 rounded-lg p-12 text-center bg-white shadow-sm">
          <p class="text-sm font-semibold text-slate-500">No suggestions or feature requests have been logged yet.</p>
        </div>

        <div v-else class="space-y-8">
          <div v-for="(teamItems, team) in groupedSuggestions" :key="team" class="bg-white rounded-lg border border-slate-200 shadow-sm overflow-hidden">
            <div class="bg-blue-50 px-4 md:px-6 py-4 border-b border-blue-100 flex items-center justify-between">
              <h4 class="font-bold text-blue-800 text-base flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                {{ team || 'Unassigned' }}
              </h4>
              <span class="text-xs font-bold text-blue-800 bg-blue-200 px-2.5 py-1 rounded-full">{{ teamItems.length }} Items</span>
            </div>
            <div class="p-4 md:p-6 space-y-4">
              <div v-for="item in teamItems" :key="item.id" class="border border-slate-200 rounded-xl p-4 shadow-sm flex flex-col lg:flex-row gap-4">
                <div class="flex-1">
                  <div class="flex flex-wrap items-center gap-2 mb-2">
                    <span :class="['text-[10px] font-bold px-2 py-0.5 rounded-full border', item.suggestionType === 'Suggestion' ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-purple-50 text-purple-700 border-purple-200']">
                      {{ item.suggestionType }}
                    </span>
                  </div>
                  <p class="text-sm text-slate-800 font-medium mb-2 whitespace-pre-line">{{ item.suggestionDescription }}</p>
                  <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider">
                    Logged by {{ item.name }} ({{ item.rollNumber }}) on {{ new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                  </p>
                </div>
                <div class="flex flex-col gap-2 shrink-0 lg:items-end">
                  <div v-if="item.suggestionDeadline">
                    <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider mb-1 lg:text-right">Target Deadline</p>
                    <p class="text-sm font-bold text-slate-800 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg inline-block">
                      {{ new Date(item.suggestionDeadline).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                    </p>
                  </div>
                  <div class="mt-auto pt-2 lg:pt-0">
                    <label class="block text-[10px] text-slate-500 font-bold uppercase tracking-wider mb-1 lg:text-right">Status</label>
                    <select 
                      v-model="item.suggestionStatus"
                      @change="updateSuggestionStatus(item.id, $event.target.value)"
                      :class="['text-xs font-bold px-3 py-1.5 rounded-lg border outline-none cursor-pointer', getStatusClass(item.suggestionStatus)]"
                    >
                      <option value="Pending">Pending</option>
                      <option value="In Progress">In Progress</option>
                      <option value="Resolved">Resolved</option>
                      <option value="Rejected">Rejected</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
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

      <div v-if="activeTab === 'users'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Manage Teams & Add Student CRUD Panel (Admin Only) -->
        <div v-if="authStore.user?.role === 'admin'" class="col-span-1 space-y-6">
          <!-- Manage Teams -->
          <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6 h-fit">
            <h3 class="text-base md:text-lg font-bold text-teal-700 flex items-center gap-2 mb-6">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
              Manage Teams
            </h3>
            <form @submit.prevent="submitTeam" class="space-y-4 mb-6">
              <div>
                <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">New Team Name</label>
                <div class="flex gap-2">
                  <input type="text" required v-model="newTeamName" placeholder="e.g. AI Devs" class="flex-1 rounded-lg border border-slate-200 py-2 px-3 text-sm focus:ring-2 focus:ring-teal-500 outline-none">
                  <button type="submit" :disabled="isSubmittingTeam" class="bg-teal-600 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded-lg shadow-sm text-sm disabled:opacity-50">
                    Add
                  </button>
                </div>
              </div>
            </form>
            
            <div class="space-y-2 border-t border-slate-100 pt-4">
              <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Active Teams</label>
              <div v-if="allTeams.length === 0" class="text-xs text-slate-400 italic">No teams registered</div>
              <div v-else class="space-y-1.5 max-h-[300px] overflow-y-auto pr-1">
                <div v-for="team in allTeams" :key="team.id" class="flex justify-between items-center bg-slate-50 border border-slate-200 p-2.5 rounded-lg text-sm hover:bg-white transition-colors">
                  <span class="font-semibold text-slate-700">{{ team.name }}</span>
                  <button @click="removeTeam(team)" class="text-red-500 hover:text-red-700 hover:bg-red-50 p-1.5 rounded transition-colors">
                    <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Add New Student Panel -->
          <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-4 md:p-6 h-fit">
            <h3 class="text-base md:text-lg font-bold text-teal-700 flex items-center gap-2 mb-6">
              <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path></svg>
              Add New Student
            </h3>
            <form @submit.prevent="submitCreateStudent" class="space-y-4">
              <div>
                <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Student Name</label>
                <input type="text" required v-model="newStudentName" placeholder="e.g. John Doe" class="w-full rounded-lg border border-slate-200 py-2 px-3 text-sm focus:ring-2 focus:ring-teal-500 outline-none">
              </div>
              <div>
                <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Roll Number</label>
                <input type="text" required v-model="newStudentRoll" placeholder="e.g. 24E51A6634" class="w-full rounded-lg border border-slate-200 py-2 px-3 text-sm focus:ring-2 focus:ring-teal-500 outline-none">
              </div>
              <div>
                <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Initial Team</label>
                <select v-model="newStudentTeam" class="w-full rounded-lg border border-slate-200 py-2 px-3 text-sm focus:ring-2 focus:ring-teal-500 outline-none bg-white">
                  <option value="">Unassigned (Assign Later)</option>
                  <option v-for="team in allTeams" :key="team.id" :value="team.name">{{ team.name }}</option>
                </select>
              </div>
              <div>
                <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Password</label>
                <input type="text" required v-model="newStudentPassword" placeholder="Password" class="w-full rounded-lg border border-slate-200 py-2 px-3 text-sm focus:ring-2 focus:ring-teal-500 outline-none">
              </div>
              <button type="submit" :disabled="isSubmittingStudent" class="w-full bg-teal-600 hover:bg-teal-700 text-white font-bold py-2.5 rounded-lg shadow-sm text-sm disabled:opacity-50">
                Create Student
              </button>
            </form>
          </div>
        </div>
        
        <!-- Workspace Members Registry Table -->
        <div :class="[authStore.user?.role === 'admin' ? 'col-span-1 lg:col-span-2' : 'col-span-1 lg:col-span-3', 'bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden']">
          <div class="p-4 md:p-6 bg-slate-50 border-b border-slate-200 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
            <h3 class="text-base md:text-lg font-bold text-slate-800">Workspace Members Registry</h3>
            <span class="bg-blue-100 text-blue-800 text-xs font-bold px-3 py-1 rounded-full">{{ allUsers.length }} Total Accounts</span>
          </div>
          <div class="overflow-x-auto no-scrollbar">
            <table class="w-full text-left border-collapse min-w-[500px]">
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
                        <option value="">Unassigned</option>
                        <option v-for="team in AVAILABLE_TEAMS.filter(t => t !== 'Management')" :key="team" :value="team">{{ team }}</option>
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
                    <td class="p-4 text-sm font-medium text-blue-700 whitespace-nowrap">
                      <span v-if="user.team" class="bg-blue-50 text-blue-700 px-2.5 py-1 rounded-full text-xs font-semibold border border-blue-100">{{ user.team }}</span>
                      <span v-else class="text-slate-400 italic text-xs">Unassigned</span>
                    </td>
                    <td v-if="authStore.user?.role === 'admin'" class="p-4 text-right whitespace-nowrap">
                      <button @click="startEdit(user)" class="text-blue-600 hover:underline text-xs font-bold mr-4">Edit Profile</button>
                      <button @click="removeUser(user.id)" class="text-red-600 hover:underline text-xs font-bold">Remove Student</button>
                    </td>
                  </template>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'mom'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <div v-if="authStore.user?.role === 'admin'" class="col-span-1 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden h-fit">
          <div class="bg-slate-800 px-6 py-4 border-b border-slate-700 flex justify-between items-center">
            <h3 class="text-base font-bold text-white flex items-center gap-2">Log Meeting</h3>
          </div>
          
          <div class="p-6">
            <div class="flex space-x-1 mb-6 bg-slate-100 p-1 rounded-lg">
              <button @click="momFormMode = 'text'" :class="['flex-1 py-2 rounded-md text-xs font-semibold transition-all duration-200 tracking-wide', momFormMode === 'text' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700']">Write Note</button>
              <button @click="momFormMode = 'file'" :class="['flex-1 py-2 rounded-md text-xs font-semibold transition-all duration-200 tracking-wide', momFormMode === 'file' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700']">Upload File</button>
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
              
              <div v-if="momFormMode === 'text'" class="flex flex-col">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Meeting Notes</label>
                <div class="bg-white rounded-lg border border-slate-200 overflow-hidden focus-within:ring-2 focus-within:ring-slate-500">
                  <QuillEditor 
                    theme="snow" 
                    v-model:content="newMomContent" 
                    contentType="html" 
                    placeholder="Enter key points, headings, and action items..."
                    class="min-h-[200px] text-sm"
                  />
                </div>
              </div>

              <div v-if="momFormMode === 'file'">
                <label class="block text-xs font-bold text-slate-500 uppercase mb-2">Attach Document (PDF, Image)</label>
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
                    
                    <div class="flex items-center gap-2 w-full sm:w-auto shrink-0">
                      <button @click.prevent="viewMoM(mom.id)" class="w-full sm:w-auto text-center bg-slate-800 hover:bg-slate-700 text-white font-bold py-2 px-4 rounded-lg text-xs transition-colors shrink-0 flex items-center justify-center gap-2 shadow-sm">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
                        Preview File
                      </button>
                      <button @click="downloadMoM(mom.id, mom.file_name)" class="w-full sm:w-auto text-center bg-slate-100 hover:bg-blue-50 text-blue-600 font-bold py-2 px-4 rounded-lg text-xs transition-colors shrink-0 border border-slate-200 flex items-center justify-center gap-2">
                        Download
                      </button>
                    </div>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

// Import the Rich Text Editor
import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

// --- ROUTER & STORE INITIATION ---
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Active Workspace Company
const activeCompany = ref(route.query.company || authStore.selectedCompany || 'CallHealth')

const switchCompany = (company) => {
  activeCompany.value = company
  authStore.setSelectedCompany(company)
  router.replace({ query: { ...route.query, company } })
  fetchAllData()
}

watch(() => route.query.company, (newComp) => {
  if (newComp && newComp !== activeCompany.value) {
    activeCompany.value = newComp
    authStore.setSelectedCompany(newComp)
    fetchAllData()
  }
})

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
  { id: 'progress', label: 'Daily Progress', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>' },
  { id: 'attendance', label: 'Attendance', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>' },
  { id: 'records', label: 'Records', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path></svg>' },
  { id: 'reports', label: 'Reports', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>' },
  { id: 'mom', label: 'Minutes of Meet', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>' },
  { id: 'suggestions', label: 'Suggestions', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>' },
  { id: 'holidays', label: 'Holidays', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path></svg>' },
  { id: 'users', label: 'Users & Teams', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>' }
]

const AVAILABLE_TEAMS = ref(["Digi Yatra", "OCR", "FHIR", "MIRTH Connect", "ChatBot", "Blood Connect", "Management"])

const BASE_ORDERED_ROLLS = [
  "25E51M0503", "24E51A6634", "24E51A6614", "24E51A6633", 
  "24E51A6628", "24E51A6641", "24E51A6609", "24E51A6665", 
  "23E51A6650", "23E51A6783", "24E55A0312", "23E51A67C5", 
  "23E51A0561", "23E51A0508", "23E51A6708", "23E51A6711", 
  "24E55A6604", "23E51A0514", "23E51A6799", "23E51A0503", 
  "24E51A6618", "24E51A6650", "23E51A05G4", "23E51A6673"
]

// Core State
const activeTab = ref('daily')
const selectedDate = ref(new Date().toISOString().split('T')[0])
const allLogs = ref([])
const allUsers = ref([])
const allHolidays = ref([])
const allMoMs = ref([])
const allTeams = ref([])

// Form State
const newHolidayDate = ref('')
const newHolidayName = ref('')
const newTeamName = ref('')
const isSubmittingTeam = ref(false)
const editingUser = ref(null)

// MoM States
const momSearchQuery = ref('')
const expandedMoMs = ref([])

// Progress Feed States
const feedFilterDate = ref('')
const feedSearchQuery = ref('')

// Add Student States
const newStudentName = ref('')
const newStudentRoll = ref('')
const newStudentTeam = ref('')
const newStudentPassword = ref('Student@123')
const isSubmittingStudent = ref(false)
const momFormMode = ref('text')
const isSubmittingMoM = ref(false)
const newMomDate = ref(new Date().toISOString().split('T')[0])
const newMomAgenda = ref('')
const newMomAttendees = ref('')
const newMomContent = ref('')
const newMomFile = ref(null)

// --- REPORTS SECTION STATE ---
const getDefaultReportStartDate = () => {
  const d = new Date()
  d.setDate(d.getDate() - 30)
  return d.toISOString().split('T')[0]
}
const reportStartDate = ref(getDefaultReportStartDate())
const reportEndDate = ref(new Date().toISOString().split('T')[0])
const reportTeamFilter = ref('')
const reportStudentFilter = ref('')
const reportSearchQuery = ref('')
const reportMinHours = ref('all')
const reportViewMode = ref('logs') // 'logs' | 'students' | 'teams'
const activeReportPreset = ref('30days')

const setReportInterval = (preset) => {
  activeReportPreset.value = preset
  const today = new Date()
  const todayStr = today.toISOString().split('T')[0]
  reportEndDate.value = todayStr
  
  if (preset === 'today') {
    reportStartDate.value = todayStr
  } else if (preset === '7days') {
    const d = new Date()
    d.setDate(d.getDate() - 7)
    reportStartDate.value = d.toISOString().split('T')[0]
  } else if (preset === '14days') {
    const d = new Date()
    d.setDate(d.getDate() - 14)
    reportStartDate.value = d.toISOString().split('T')[0]
  } else if (preset === '30days') {
    const d = new Date()
    d.setDate(d.getDate() - 30)
    reportStartDate.value = d.toISOString().split('T')[0]
  } else if (preset === 'thisMonth') {
    const d = new Date(today.getFullYear(), today.getMonth(), 1)
    reportStartDate.value = d.toISOString().split('T')[0]
  } else if (preset === 'allTime') {
    reportStartDate.value = '2024-01-01'
  }
}

const resetReportFilters = () => {
  reportTeamFilter.value = ''
  reportStudentFilter.value = ''
  reportSearchQuery.value = ''
  reportMinHours.value = 'all'
  setReportInterval('30days')
}

// --- API FETCHING ---
const fetchAllData = async () => {
  try {
    const comp = encodeURIComponent(activeCompany.value)
    const [logsRes, usersRes, holidaysRes, momRes, teamsRes] = await Promise.all([
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs?company=${comp}`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/?company=${comp}`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/holidays/?company=${comp}`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/?company=${comp}`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/teams?company=${comp}`)
    ])
    
    // Correctly parse the JSON once per response
    const logsData = await logsRes.json()
    allLogs.value = Array.isArray(logsData) ? logsData : []
    
    const usersData = await usersRes.json()
    allUsers.value = Array.isArray(usersData) ? usersData : []

    const holidaysData = await holidaysRes.json()
    allHolidays.value = Array.isArray(holidaysData) ? holidaysData : []

    const momData = await momRes.json()
    allMoMs.value = Array.isArray(momData) ? momData : []

    const teamsData = await teamsRes.json()
    if (Array.isArray(teamsData)) {
      allTeams.value = teamsData
      AVAILABLE_TEAMS.value = [...teamsData.map(t => t.name), "Management"]
    }
    
  } catch (err) {
    console.error("Failed to load dashboard data from API.", err)
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
    if (momFormMode.value === 'text') {
      res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date: newMomDate.value,
          agenda: newMomAgenda.value,
          attendees: newMomAttendees.value,
          content: newMomContent.value,
          company: activeCompany.value,
          created_by: authStore.user?.name || 'Admin'
        })
      })
    } else {
      const formData = new FormData()
      formData.append('date', newMomDate.value)
      formData.append('agenda', newMomAgenda.value)
      formData.append('attendees', newMomAttendees.value)
      formData.append('created_by', authStore.user?.name || 'Admin')
      formData.append('company', activeCompany.value)
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

const viewMoM = (id) => {
  const url = `${import.meta.env.VITE_API_BASE_URL}/api/mom/download/${id}?company=${encodeURIComponent(activeCompany.value)}`
  window.open(url, '_blank')
}

const downloadMoM = async (id, filename) => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/download/${id}?company=${encodeURIComponent(activeCompany.value)}`)
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
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/${id}?company=${encodeURIComponent(activeCompany.value)}`, { method: 'DELETE' })
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
      body: JSON.stringify({ 
        date: newHolidayDate.value, 
        name: newHolidayName.value,
        company: activeCompany.value 
      })
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
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/holidays/${id}?company=${encodeURIComponent(activeCompany.value)}`, { method: 'DELETE' })
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
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/${editingUser.value.id}?company=${encodeURIComponent(activeCompany.value)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...editingUser.value, company: activeCompany.value })
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
  if (!confirm("Are you sure you want to permanently remove this student from the project? This action cannot be undone.")) return
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/${id}?company=${encodeURIComponent(activeCompany.value)}`, { method: 'DELETE' })
    if (res.ok) await fetchAllData()
  } catch (err) {
    console.error(err)
  }
}

// --- LOG COMPUTEDS & HELPERS ---
const dynamicOrderedRolls = computed(() => {
  if (activeCompany.value === 'CallHealth') {
    const rolls = [...BASE_ORDERED_ROLLS]
    allUsers.value.forEach(user => {
      if (!rolls.includes(user.rollNumber) && user.rollNumber !== 'ADMIN' && user.rollNumber !== 'VIEWER') {
        rolls.push(user.rollNumber)
      }
    })
    return rolls
  } else {
    // Succeed International: strictly students registered for Succeed International
    return allUsers.value
      .filter(u => u.rollNumber !== 'ADMIN' && u.rollNumber !== 'VIEWER')
      .map(u => u.rollNumber)
      .sort()
  }
})

const filteredLogs = computed(() => {
  const dayLogs = allLogs.value.filter(log => log.date === selectedDate.value)
  const uniqueLogsMap = new Map()
  dayLogs.forEach(log => { uniqueLogsMap.set(log.rollNumber, log) })
  return Array.from(uniqueLogsMap.values())
})

const formatHoursForRoll = (roll) => {
  const log = filteredLogs.value.find(l => l.rollNumber === roll)
  if (log && log.hours && log.hours.length > 0) {
    const sortedHours = [...log.hours].sort((a, b) => a - b)
    return `${sortedHours.join(', ')} hr`
  }
  return '0 hr'
}

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

// Suggestions logic
const groupedSuggestions = computed(() => {
  const groups = {}
  allLogs.value
    .filter(log => log.suggestionDescription)
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .forEach(log => {
      if (!groups[log.team]) groups[log.team] = []
      groups[log.team].push(log)
    })
  return groups
})

const getStatusClass = (status) => {
  switch (status) {
    case 'Resolved': return 'bg-teal-50 text-teal-700 border-teal-200'
    case 'In Progress': return 'bg-blue-50 text-blue-700 border-blue-200'
    case 'Rejected': return 'bg-red-50 text-red-700 border-red-200'
    default: return 'bg-slate-50 text-slate-700 border-slate-300' // Pending
  }
}

const updateSuggestionStatus = async (logId, status) => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs/${logId}/suggestion-status?company=${encodeURIComponent(activeCompany.value)}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    })
    if (!res.ok) {
      alert("Failed to update status")
      await fetchAllData() // Revert to server state on failure
    }
  } catch (err) {
    alert("Network error updating status")
    await fetchAllData()
  }
}

// --- PDF & EXPORT ---
const generatePDF = () => {
  const doc = new jsPDF()
  doc.setFontSize(18)
  doc.text(`${activeCompany.value} Project Daily Report - ${formattedSelectedDate.value}`, 14, 22)

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

  doc.save(`${activeCompany.value.replace(/\s+/g, '_')}_Daily_Report_${selectedDate.value}.pdf`)
}

const generateAttendancePDF = () => {
  const doc = new jsPDF()
  doc.setFontSize(18)
  doc.text(`${activeCompany.value} Attendance Report - ${formattedSelectedDate.value}`, 14, 22)

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

  doc.save(`${activeCompany.value.replace(/\s+/g, '_')}_Attendance_${selectedDate.value}.pdf`)
}

const copyAttendance = () => {
  let text = `${activeCompany.value} Attendance for ${formattedSelectedDate.value}\n\n`
  
  dynamicOrderedRolls.value.forEach(roll => {
    text += `${roll} - ${formatHoursForRoll(roll)}\n`
  })
  
  navigator.clipboard.writeText(text)
  alert("Attendance copied to clipboard!")
}

// --- REPORTS COMPUTED LOGIC ---
const filteredReportLogs = computed(() => {
  let logs = allLogs.value || []
  
  if (reportStartDate.value) {
    logs = logs.filter(l => l.date >= reportStartDate.value)
  }
  if (reportEndDate.value) {
    logs = logs.filter(l => l.date <= reportEndDate.value)
  }
  if (reportTeamFilter.value) {
    logs = logs.filter(l => (l.team || '').toLowerCase() === reportTeamFilter.value.toLowerCase())
  }
  if (reportStudentFilter.value) {
    logs = logs.filter(l => (l.rollNumber || '').toLowerCase() === reportStudentFilter.value.toLowerCase())
  }
  if (reportMinHours.value === 'with_hours') {
    logs = logs.filter(l => Array.isArray(l.hours) && l.hours.length > 0)
  } else if (reportMinHours.value === 'half_day') {
    logs = logs.filter(l => Array.isArray(l.hours) && l.hours.length >= 3)
  } else if (reportMinHours.value === 'full_day') {
    logs = logs.filter(l => Array.isArray(l.hours) && l.hours.length >= 5)
  }
  if (reportSearchQuery.value && reportSearchQuery.value.trim()) {
    const q = reportSearchQuery.value.trim().toLowerCase()
    logs = logs.filter(l => 
      (l.name || '').toLowerCase().includes(q) ||
      (l.rollNumber || '').toLowerCase().includes(q) ||
      (l.team || '').toLowerCase().includes(q) ||
      (l.todayLog || '').toLowerCase().includes(q) ||
      (l.tomorrowGoal || '').toLowerCase().includes(q)
    )
  }
  return [...logs].sort((a, b) => {
    if (a.date !== b.date) return b.date.localeCompare(a.date)
    return (a.rollNumber || '').localeCompare(b.rollNumber || '')
  })
})

const reportTotalHours = computed(() => {
  return filteredReportLogs.value.reduce((acc, l) => acc + (Array.isArray(l.hours) ? l.hours.length : 0), 0)
})

const reportActiveStudentsCount = computed(() => {
  return new Set(filteredReportLogs.value.map(l => l.rollNumber).filter(Boolean)).size
})

const reportActiveTeamsCount = computed(() => {
  return new Set(filteredReportLogs.value.map(l => l.team).filter(Boolean)).size
})

const reportAvgHoursPerStudent = computed(() => {
  if (reportActiveStudentsCount.value === 0) return '0.0'
  return (reportTotalHours.value / reportActiveStudentsCount.value).toFixed(1)
})

const studentReportMatrix = computed(() => {
  const map = {}
  allUsers.value.forEach(u => {
    if (u.role === 'admin' || u.role === 'viewer') return
    map[u.rollNumber] = {
      rollNumber: u.rollNumber,
      name: u.name,
      team: u.team || 'Unassigned',
      logCount: 0,
      totalHours: 0,
      activeDates: new Set()
    }
  })
  
  filteredReportLogs.value.forEach(log => {
    if (!map[log.rollNumber]) {
      map[log.rollNumber] = {
        rollNumber: log.rollNumber,
        name: log.name,
        team: log.team || 'Unassigned',
        logCount: 0,
        totalHours: 0,
        activeDates: new Set()
      }
    }
    map[log.rollNumber].logCount += 1
    map[log.rollNumber].totalHours += Array.isArray(log.hours) ? log.hours.length : 0
    map[log.rollNumber].activeDates.add(log.date)
    if (log.team && (!map[log.rollNumber].team || map[log.rollNumber].team === 'Unassigned')) {
      map[log.rollNumber].team = log.team
    }
  })

  return Object.values(map).map(s => ({
    ...s,
    activeDays: s.activeDates.size,
    avgHoursPerDay: s.activeDates.size > 0 ? (s.totalHours / s.activeDates.size).toFixed(1) : '0.0'
  })).sort((a, b) => b.totalHours - a.totalHours || b.activeDays - a.activeDays)
})

const teamReportMatrix = computed(() => {
  const map = {}
  allTeams.value.forEach(t => {
    map[t.name] = {
      name: t.name,
      members: new Set(),
      logCount: 0,
      totalHours: 0
    }
  })
  allUsers.value.forEach(u => {
    if (u.team && map[u.team]) {
      map[u.team].members.add(u.rollNumber)
    }
  })
  filteredReportLogs.value.forEach(log => {
    const t = log.team || 'Unassigned'
    if (!map[t]) {
      map[t] = {
        name: t,
        members: new Set(),
        logCount: 0,
        totalHours: 0
      }
    }
    map[t].logCount += 1
    map[t].totalHours += Array.isArray(log.hours) ? log.hours.length : 0
    if (log.rollNumber) {
      map[t].members.add(log.rollNumber)
    }
  })
  const totalH = reportTotalHours.value || 1
  return Object.values(map).map(t => ({
    name: t.name,
    memberCount: t.members.size,
    logCount: t.logCount,
    totalHours: t.totalHours,
    percentage: Math.min(100, Math.round((t.totalHours / totalH) * 100))
  })).sort((a, b) => b.totalHours - a.totalHours)
})

// --- REPORTS EXPORT METHODS ---
const downloadReportCSV = () => {
  if (filteredReportLogs.value.length === 0) {
    alert("No records found for the selected interval to export.")
    return
  }
  const headers = ["Date", "Roll Number", "Student Name", "Team", "Total Hours", "Time Slots", "Tasks Completed", "Next Targets", "Company"]
  const rows = filteredReportLogs.value.map(log => {
    const hoursCount = Array.isArray(log.hours) ? log.hours.length : 0
    const hoursSlots = Array.isArray(log.hours) ? log.hours.join(';') : ''
    const cleanLog = (log.todayLog || '').replace(/"/g, '""').replace(/\r?\n|\r/g, ' ')
    const cleanGoal = (log.tomorrowGoal || '').replace(/"/g, '""').replace(/\r?\n|\r/g, ' ')
    return [
      `"${log.date}"`,
      `"${log.rollNumber || ''}"`,
      `"${log.name || ''}"`,
      `"${log.team || 'Unassigned'}"`,
      hoursCount,
      `"${hoursSlots}"`,
      `"${cleanLog}"`,
      `"${cleanGoal}"`,
      `"${log.company || activeCompany.value}"`
    ].join(',')
  })
  
  const csvContent = "\uFEFF" + [headers.join(','), ...rows].join('\r\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.setAttribute("href", url)
  link.setAttribute("download", `${activeCompany.value.replace(/\s+/g, '_')}_Report_${reportStartDate.value}_to_${reportEndDate.value}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

const downloadStudentMatrixCSV = () => {
  if (studentReportMatrix.value.length === 0) {
    alert("No student data available to export.")
    return
  }
  const headers = ["Roll Number", "Student Name", "Team", "Active Days", "Total Hours", "Avg Hours Per Day", "Company"]
  const rows = studentReportMatrix.value.map(s => [
    `"${s.rollNumber}"`,
    `"${s.name}"`,
    `"${s.team}"`,
    s.activeDays,
    s.totalHours,
    s.avgHoursPerDay,
    `"${activeCompany.value}"`
  ].join(','))

  const csvContent = "\uFEFF" + [headers.join(','), ...rows].join('\r\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.setAttribute("href", url)
  link.setAttribute("download", `${activeCompany.value.replace(/\s+/g, '_')}_Student_Matrix_${reportStartDate.value}_to_${reportEndDate.value}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

const downloadReportPDF = () => {
  if (filteredReportLogs.value.length === 0) {
    alert("No records found for the selected interval to export.")
    return
  }

  const doc = new jsPDF('landscape')
  const isSucceed = activeCompany.value === 'Succeed International'
  const primaryColor = isSucceed ? [30, 64, 175] : [25, 48, 153]
  const accentColor = isSucceed ? [59, 130, 246] : [111, 183, 51]

  doc.setFillColor(...accentColor)
  doc.rect(0, 0, 297, 3, 'F')

  doc.setFillColor(...primaryColor)
  doc.rect(0, 3, 297, 22, 'F')
  
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(15)
  doc.setFont('helvetica', 'bold')
  doc.text(`HITAM - ${activeCompany.value} Project Activity Report`, 14, 17)
  
  doc.setFontSize(9)
  doc.setFont('helvetica', 'normal')
  doc.text(`Interval: ${reportStartDate.value} to ${reportEndDate.value}   |   Exported: ${new Date().toLocaleDateString()}`, 175, 17)

  doc.setFillColor(248, 250, 252)
  doc.rect(14, 29, 269, 11, 'F')
  doc.setDrawColor(226, 232, 240)
  doc.rect(14, 29, 269, 11, 'S')

  doc.setTextColor(30, 41, 59)
  doc.setFontSize(9)
  doc.setFont('helvetica', 'bold')
  const teamScope = reportTeamFilter.value || 'All Teams'
  const studentScope = reportStudentFilter.value || 'All Students'
  doc.text(`Scope: ${teamScope}  |  ${studentScope}`, 18, 36.5)
  doc.text(`Total Submissions: ${filteredReportLogs.value.length}   |   Total Hours: ${reportTotalHours.value}h   |   Active Students: ${reportActiveStudentsCount.value}`, 145, 36.5)

  const tableData = filteredReportLogs.value.map(log => {
    const hoursCount = Array.isArray(log.hours) ? log.hours.length : 0
    return [
      log.date,
      log.rollNumber || '',
      log.name || '',
      log.team || 'Unassigned',
      `${hoursCount}h`,
      (log.todayLog || '-').trim(),
      (log.tomorrowGoal || '-').trim()
    ]
  })

  autoTable(doc, {
    startY: 44,
    head: [['Date', 'Roll No', 'Student Name', 'Team / Module', 'Hours', 'Tasks Completed (Daily Log)', 'Next Targets']],
    body: tableData,
    theme: 'grid',
    headStyles: { 
      fillColor: primaryColor, 
      textColor: [255, 255, 255], 
      fontStyle: 'bold',
      fontSize: 8,
      halign: 'left'
    },
    styles: { 
      fontSize: 7.5, 
      cellPadding: 2.5, 
      overflow: 'linebreak',
      textColor: [30, 41, 59]
    },
    columnStyles: {
      0: { cellWidth: 20, halign: 'center' },
      1: { cellWidth: 25, fontStyle: 'bold' },
      2: { cellWidth: 32 },
      3: { cellWidth: 28 },
      4: { cellWidth: 14, halign: 'center', fontStyle: 'bold' },
      5: { cellWidth: 88 },
      6: { cellWidth: 62 }
    },
    didDrawPage: (data) => {
      const pageCount = doc.internal.getNumberOfPages()
      doc.setFontSize(8)
      doc.setTextColor(140, 150, 160)
      doc.text(`Page ${data.pageNumber} of ${pageCount} - HITAM Project Tracker (${activeCompany.value})`, 14, 204)
    }
  })

  doc.save(`${activeCompany.value.replace(/\s+/g, '_')}_Report_${reportStartDate.value}_to_${reportEndDate.value}.pdf`)
}

const downloadStudentMatrixPDF = () => {
  if (studentReportMatrix.value.length === 0) {
    alert("No student data available to export.")
    return
  }

  const doc = new jsPDF('portrait')
  const isSucceed = activeCompany.value === 'Succeed International'
  const primaryColor = isSucceed ? [30, 64, 175] : [25, 48, 153]

  doc.setFillColor(...primaryColor)
  doc.rect(0, 0, 210, 22, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text(`HITAM - ${activeCompany.value} Student Contribution Matrix`, 14, 14)

  doc.setFontSize(9)
  doc.setFont('helvetica', 'normal')
  doc.text(`Interval: ${reportStartDate.value} to ${reportEndDate.value}`, 125, 14)

  const rows = studentReportMatrix.value.map(s => [
    s.rollNumber,
    s.name,
    s.team,
    `${s.activeDays} days`,
    `${s.totalHours} hrs`,
    `${s.avgHoursPerDay}h`
  ])

  autoTable(doc, {
    startY: 28,
    head: [['Roll Number', 'Student Name', 'Team', 'Active Days', 'Total Hours', 'Avg/Day']],
    body: rows,
    theme: 'grid',
    headStyles: { fillColor: primaryColor, textColor: 255, fontStyle: 'bold' },
    styles: { cellPadding: 3, fontSize: 8.5 }
  })

  doc.save(`${activeCompany.value.replace(/\s+/g, '_')}_Student_Matrix_${reportStartDate.value}_to_${reportEndDate.value}.pdf`)
}

const downloadSingleStudentPDF = (rollNumber) => {
  const studentLogs = (allLogs.value || []).filter(l => 
    (l.rollNumber || '').toLowerCase() === rollNumber.toLowerCase() &&
    (!reportStartDate.value || l.date >= reportStartDate.value) &&
    (!reportEndDate.value || l.date <= reportEndDate.value)
  ).sort((a, b) => b.date.localeCompare(a.date))

  if (studentLogs.length === 0) {
    alert(`No activity logs found for roll number ${rollNumber} in this interval.`)
    return
  }

  const studentName = studentLogs[0].name || rollNumber
  const teamName = studentLogs[0].team || 'Unassigned'
  const totalH = studentLogs.reduce((acc, l) => acc + (Array.isArray(l.hours) ? l.hours.length : 0), 0)

  const doc = new jsPDF('landscape')
  const isSucceed = activeCompany.value === 'Succeed International'
  const primaryColor = isSucceed ? [30, 64, 175] : [25, 48, 153]

  doc.setFillColor(...primaryColor)
  doc.rect(0, 0, 297, 22, 'F')
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(14)
  doc.setFont('helvetica', 'bold')
  doc.text(`Student Activity Report: ${studentName} (${rollNumber}) - ${activeCompany.value}`, 14, 14)

  doc.setFontSize(9)
  doc.text(`Team: ${teamName}  |  Interval: ${reportStartDate.value} to ${reportEndDate.value}  |  Total Logs: ${studentLogs.length}  |  Total Hours: ${totalH}h`, 14, 30)

  const tableData = studentLogs.map(l => [
    l.date,
    `${Array.isArray(l.hours) ? l.hours.length : 0}h`,
    (l.todayLog || '-').trim(),
    (l.tomorrowGoal || '-').trim()
  ])

  autoTable(doc, {
    startY: 35,
    head: [['Date', 'Hours', 'Tasks Completed', 'Next Target']],
    body: tableData,
    theme: 'grid',
    headStyles: { fillColor: primaryColor, textColor: 255, fontStyle: 'bold' },
    styles: { cellPadding: 3, fontSize: 8.5 },
    columnStyles: {
      0: { cellWidth: 26 },
      1: { cellWidth: 16, halign: 'center' },
      2: { cellWidth: 140 },
      3: { cellWidth: 85 }
    }
  })

  doc.save(`${rollNumber}_Report_${reportStartDate.value}_to_${reportEndDate.value}.pdf`)
}

const copyReportSummary = async () => {
  const lines = [
    `HITAM Project Tracker - ${activeCompany.value} Activity Summary`,
    `Interval: ${reportStartDate.value} to ${reportEndDate.value}`,
    `Filter: Team = ${reportTeamFilter.value || 'All'}, Student = ${reportStudentFilter.value || 'All'}`,
    `Total Logs: ${filteredReportLogs.value.length}`,
    `Total Hours Logged: ${reportTotalHours.value} hrs`,
    `Active Students: ${reportActiveStudentsCount.value}`,
    `Active Teams: ${reportActiveTeamsCount.value}`,
    `----------------------------------------------------`
  ]
  filteredReportLogs.value.slice(0, 50).forEach(l => {
    lines.push(`• [${l.date}] ${l.rollNumber} (${l.name} - ${l.team || 'N/A'}): ${l.hours?.length || 0}h - ${l.todayLog}`)
  })
  if (filteredReportLogs.value.length > 50) {
    lines.push(`... and ${filteredReportLogs.value.length - 50} more entries.`)
  }

  try {
    await navigator.clipboard.writeText(lines.join('\n'))
    alert("Report summary copied to clipboard!")
  } catch (err) {
    console.error("Failed to copy report", err)
  }
}

// --- INTERVAL ATTENDANCE SHEET LOGIC ---
const intervalDates = computed(() => {
  if (!reportStartDate.value || !reportEndDate.value) return []
  const dates = []
  const start = new Date(reportStartDate.value)
  const end = new Date(reportEndDate.value)
  if (start > end) return []
  
  const curr = new Date(start)
  let limit = 0
  while (curr <= end && limit < 366) {
    dates.push(curr.toISOString().split('T')[0])
    curr.setDate(curr.getDate() + 1)
    limit++
  }
  return dates
})

const intervalWorkingDates = computed(() => {
  const datesWithLogs = new Set(allLogs.value
    .filter(l => (!reportStartDate.value || l.date >= reportStartDate.value) && (!reportEndDate.value || l.date <= reportEndDate.value))
    .map(l => l.date)
  )
  const filtered = intervalDates.value.filter(d => datesWithLogs.has(d))
  return filtered.length > 0 ? filtered : intervalDates.value
})

const attendanceSheetData = computed(() => {
  const dates = intervalWorkingDates.value
  const totalDays = dates.length || 1

  let students = allUsers.value.filter(u => u.role !== 'admin' && u.role !== 'viewer')

  if (reportTeamFilter.value) {
    students = students.filter(s => (s.team || '').toLowerCase() === reportTeamFilter.value.toLowerCase())
  }
  if (reportStudentFilter.value) {
    students = students.filter(s => (s.rollNumber || '').toLowerCase() === reportStudentFilter.value.toLowerCase())
  }

  const userDateLogs = {}
  filteredReportLogs.value.forEach(log => {
    if (!userDateLogs[log.rollNumber]) {
      userDateLogs[log.rollNumber] = {}
    }
    const h = Array.isArray(log.hours) ? log.hours.length : 0
    userDateLogs[log.rollNumber][log.date] = (userDateLogs[log.rollNumber][log.date] || 0) + h
  })

  return students.map(student => {
    const dateHoursMap = userDateLogs[student.rollNumber] || {}
    let presentDays = 0
    let totalHours = 0

    dates.forEach(d => {
      const h = dateHoursMap[d] || 0
      if (h > 0) {
        presentDays++
        totalHours += h
      }
    })

    const percentage = totalDays > 0 ? Math.round((presentDays / totalDays) * 100) : 0

    return {
      rollNumber: student.rollNumber,
      name: student.name,
      team: student.team || 'Unassigned',
      dateHoursMap,
      presentDays,
      totalHours,
      percentage
    }
  }).sort((a, b) => b.percentage - a.percentage || b.totalHours - a.totalHours)
})

const intervalAvgAttendanceRate = computed(() => {
  if (attendanceSheetData.value.length === 0) return 0
  const sum = attendanceSheetData.value.reduce((acc, s) => acc + s.percentage, 0)
  return Math.round(sum / attendanceSheetData.value.length)
})

const eligibleStudentsCount = computed(() => {
  return attendanceSheetData.value.filter(s => s.percentage >= 75).length
})

const shortageStudentsCount = computed(() => {
  return attendanceSheetData.value.filter(s => s.percentage < 75).length
})

const downloadIntervalAttendancePDF = () => {
  if (attendanceSheetData.value.length === 0) {
    alert("No student attendance data found for the selected interval.")
    return
  }

  const doc = new jsPDF('portrait')
  const isSucceed = activeCompany.value === 'Succeed International'
  const primaryColor = isSucceed ? [30, 64, 175] : [25, 48, 153]
  const accentColor = isSucceed ? [59, 130, 246] : [111, 183, 51]

  // Top Accent Stripe
  doc.setFillColor(...accentColor)
  doc.rect(0, 0, 210, 3, 'F')

  // Top Header Banner
  doc.setFillColor(...primaryColor)
  doc.rect(0, 3, 210, 24, 'F')
  
  doc.setTextColor(255, 255, 255)
  doc.setFontSize(15)
  doc.setFont('helvetica', 'bold')
  doc.text(`HITAM - ${activeCompany.value} Project Attendance Sheet`, 14, 16)
  
  doc.setFontSize(8.5)
  doc.setFont('helvetica', 'normal')
  doc.text(`Interval: ${reportStartDate.value} to ${reportEndDate.value}   |   Active Project Days: ${intervalWorkingDates.value.length} days`, 14, 23)

  // Sub-header stats bar
  doc.setFillColor(248, 250, 252)
  doc.rect(14, 30, 182, 10, 'F')
  doc.setDrawColor(226, 232, 240)
  doc.rect(14, 30, 182, 10, 'S')

  doc.setTextColor(30, 41, 59)
  doc.setFontSize(8.5)
  doc.setFont('helvetica', 'bold')
  const teamScope = reportTeamFilter.value || 'All Teams'
  doc.text(`Filter: ${teamScope}  |  Enrolled: ${attendanceSheetData.value.length} students  |  Avg Attendance: ${intervalAvgAttendanceRate.value}%`, 18, 36.5)

  // Table Data
  const tableData = attendanceSheetData.value.map((student, idx) => [
    idx + 1,
    student.rollNumber,
    student.name,
    student.team,
    `${student.presentDays} / ${intervalWorkingDates.value.length}`,
    `${student.totalHours} hrs`,
    `${student.percentage}%`,
    student.percentage >= 75 ? 'Eligible' : 'Shortage'
  ])

  autoTable(doc, {
    startY: 44,
    head: [['S.No', 'Roll Number', 'Student Name', 'Team', 'Days (P/Total)', 'Total Hours', 'Attd %', 'Status']],
    body: tableData,
    theme: 'grid',
    headStyles: { 
      fillColor: primaryColor, 
      textColor: [255, 255, 255], 
      fontStyle: 'bold',
      fontSize: 8,
      halign: 'left'
    },
    styles: { 
      fontSize: 8, 
      cellPadding: 2.5, 
      textColor: [30, 41, 59]
    },
    columnStyles: {
      0: { cellWidth: 12, halign: 'center' },
      1: { cellWidth: 26, fontStyle: 'bold' },
      2: { cellWidth: 38 },
      3: { cellWidth: 32 },
      4: { cellWidth: 24, halign: 'center' },
      5: { cellWidth: 20, halign: 'center' },
      6: { cellWidth: 16, halign: 'center', fontStyle: 'bold' },
      7: { cellWidth: 14, halign: 'center' }
    },
    didDrawPage: (data) => {
      const pageCount = doc.internal.getNumberOfPages()
      doc.setFontSize(8)
      doc.setTextColor(140, 150, 160)
      doc.text(`Page ${data.pageNumber} of ${pageCount} - HITAM Project Tracker Attendance Sheet`, 14, 290)
    }
  })

  // Signatures section at the bottom of the last page
  const finalY = doc.lastAutoTable?.finalY || 200
  if (finalY < 250) {
    doc.setFontSize(8.5)
    doc.setTextColor(50, 50, 50)
    doc.text("Faculty / Mentor Signature: _______________________", 14, finalY + 22)
    doc.text("Project Coordinator / HoD: _______________________", 115, finalY + 22)
  }

  doc.save(`${activeCompany.value.replace(/\s+/g, '_')}_Attendance_Sheet_${reportStartDate.value}_to_${reportEndDate.value}.pdf`)
}

const downloadIntervalAttendanceMatrixCSV = () => {
  if (attendanceSheetData.value.length === 0) {
    alert("No student attendance data found for the selected interval.")
    return
  }

  const dates = intervalWorkingDates.value.length > 0 ? intervalWorkingDates.value : intervalDates.value
  
  const dateHeaders = dates.map(d => `"${d}"`)
  const headers = ["\"Roll Number\"", "\"Student Name\"", "\"Team\"", ...dateHeaders, "\"Days Present\"", "\"Total Days\"", "\"Total Hours\"", "\"Attendance %\"", "\"Status\""]

  const rows = attendanceSheetData.value.map(s => {
    const dailyHoursCells = dates.map(d => {
      const h = s.dateHoursMap[d] || 0
      return h > 0 ? `"${h}h"` : "\"A\""
    })
    return [
      `"${s.rollNumber}"`,
      `"${s.name}"`,
      `"${s.team}"`,
      ...dailyHoursCells,
      s.presentDays,
      dates.length,
      s.totalHours,
      `"${s.percentage}%"`,
      `"${s.percentage >= 75 ? 'Eligible' : 'Shortage'}"`
    ].join(',')
  })

  const csvContent = "\uFEFF" + [headers.join(','), ...rows].join('\r\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.setAttribute("href", url)
  link.setAttribute("download", `${activeCompany.value.replace(/\s+/g, '_')}_Attendance_Matrix_${reportStartDate.value}_to_${reportEndDate.value}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

const submitTeam = async () => {
  if (!newTeamName.value.trim()) return
  isSubmittingTeam.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/teams`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        name: newTeamName.value.trim(),
        company: activeCompany.value
      })
    })
    if (res.ok) {
      newTeamName.value = ''
      await fetchAllData()
      alert("Team added successfully!")
    } else {
      const errorData = await res.json()
      alert(`Error: ${errorData.detail || 'Could not add team'}`)
    }
  } catch (err) {
    alert("Network error. Could not connect to backend.")
  } finally {
    isSubmittingTeam.value = false
  }
}

const removeTeam = async (team) => {
  if (!confirm(`Are you sure you want to permanently delete the team "${team.name}"? This action cannot be undone.`)) return
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/teams/${team.id}?company=${encodeURIComponent(activeCompany.value)}`, { method: 'DELETE' })
    if (res.ok) {
      await fetchAllData()
    } else {
      alert("Failed to delete team.")
    }
  } catch (err) {
    console.error(err)
  }
}


const submitCreateStudent = async () => {
  if (!newStudentName.value.trim() || !newStudentRoll.value.trim() || !newStudentPassword.value.trim()) {
    alert("Please fill all required student fields.")
    return
  }
  
  isSubmittingStudent.value = true
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/admin-create-student`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: newStudentName.value.trim(),
        rollNumber: newStudentRoll.value.trim(),
        team: newStudentTeam.value,
        company: activeCompany.value,
        password: newStudentPassword.value.trim()
      })
    })
    if (res.ok) {
      newStudentName.value = ''
      newStudentRoll.value = ''
      newStudentTeam.value = ''
      newStudentPassword.value = 'Student@123'
      await fetchAllData()
      alert("Student created successfully!")
    } else {
      const errData = await res.json()
      alert(`Error: ${errData.detail || 'Could not create student.'}`)
    }
  } catch (err) {
    alert("Network error. Could not connect to backend.")
  } finally {
    isSubmittingStudent.value = false
  }
}

const feedCurrentPage = ref(1)
const feedPageSize = 5

// Watch feed filters to reset page to 1 on search or date filter change
watch([feedFilterDate, feedSearchQuery], () => {
  feedCurrentPage.value = 1
})

const pageStartIdx = computed(() => {
  if (filteredFeedDays.value.length === 0) return 0
  return (feedCurrentPage.value - 1) * feedPageSize + 1
})

const pageEndIdx = computed(() => {
  return Math.min(feedCurrentPage.value * feedPageSize, filteredFeedDays.value.length)
})

const paginatedFeedDays = computed(() => {
  const start = (feedCurrentPage.value - 1) * feedPageSize
  const end = start + feedPageSize
  return filteredFeedDays.value.slice(start, end)
})

const prevPage = () => {
  if (feedCurrentPage.value > 1) {
    feedCurrentPage.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const nextPage = () => {
  if (feedCurrentPage.value * feedPageSize < filteredFeedDays.value.length) {
    feedCurrentPage.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const filteredFeedDays = computed(() => {
  let logs = allLogs.value
  
  if (feedFilterDate.value) {
    logs = logs.filter(log => log.date === feedFilterDate.value)
  }
  
  if (feedSearchQuery.value) {
    const q = feedSearchQuery.value.toLowerCase()
    logs = logs.filter(log => 
      (log.name && log.name.toLowerCase().includes(q)) ||
      (log.rollNumber && log.rollNumber.toLowerCase().includes(q)) ||
      (log.team && log.team.toLowerCase().includes(q)) ||
      (log.todayLog && log.todayLog.toLowerCase().includes(q)) ||
      (log.tomorrowGoal && log.tomorrowGoal.toLowerCase().includes(q))
    )
  }
  
  const dateGroups = {}
  logs.forEach(log => {
    if (!dateGroups[log.date]) {
      dateGroups[log.date] = []
    }
    dateGroups[log.date].push(log)
  })
  
  const days = Object.entries(dateGroups).map(([date, dayLogs]) => {
    const teamGroups = {}
    let dayHours = 0
    dayLogs.forEach(log => {
      if (!teamGroups[log.team]) {
        teamGroups[log.team] = []
      }
      teamGroups[log.team].push(log)
      dayHours += (log.hours?.length || 0)
    })
    
    return {
      date,
      totalHours: dayHours,
      teams: teamGroups
    }
  })
  
  days.sort((a, b) => new Date(b.date) - new Date(a.date))
  return days
})

const formatFeedDate = (dateStr) => {
  const date = new Date(dateStr)
  if (isNaN(date.getTime())) return dateStr
  const today = new Date()
  const yesterday = new Date()
  yesterday.setDate(today.getDate() - 1)
  const formatOptions = { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' }
  
  if (date.toDateString() === today.toDateString()) {
    return 'Today'
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday'
  } else {
    return date.toLocaleDateString('en-US', formatOptions)
  }
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