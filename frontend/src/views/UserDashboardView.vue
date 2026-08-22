<template>
  <div class="min-h-screen pb-12 bg-slate-50">
    <header class="bg-gradient-to-r from-blue-700 to-teal-600 text-white shadow-md sticky top-0 z-40">
      <div class="px-4 md:px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-3">
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-center sm:justify-start">
          <svg class="w-6 h-6 shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zm0 7.5l-10-5v2.5l10 5 10-5v-2.5l-10 5zM2 12v2.5l10 5 10-5V12l-10 5-10-5z"/></svg>
          <h1 class="text-lg md:text-2xl font-bold tracking-wide">CallHealth X HITAM Project Tracker</h1>
        </div>
        <div class="flex items-center space-x-3 w-full sm:w-auto justify-between sm:justify-end">
          <span class="text-xs md:text-sm font-medium bg-black/20 px-3 py-1.5 rounded-full border border-white/10 max-w-[250px] sm:max-w-none flex items-center gap-1.5">
            <svg class="w-3 h-3 md:w-4 md:h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
            <span class="truncate max-w-[80px] md:max-w-[120px]">{{ authStore.user?.name }}</span>
            <span class="opacity-50">|</span>
            <span class="font-bold text-teal-200 text-xs md:text-sm">{{ authStore.user?.team || 'Unassigned' }}</span>
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
        <div v-if="!authStore.user?.team" class="bg-amber-50 border border-amber-200 rounded-2xl p-6 text-center shadow-sm">
          <svg class="w-12 h-12 text-amber-500 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
          <h3 class="text-base font-bold text-amber-800 mb-1">Team Assignment Pending</h3>
          <p class="text-sm text-amber-700">You are registered successfully! However, you have not been assigned to any project team yet. Please contact the CDC Admin to assign your team to start logging daily progress.</p>
        </div>
        <div v-else class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
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
              
              <div class="border-t border-slate-200 pt-6 mt-6">
                <button type="button" @click="showSuggestionForm = !showSuggestionForm" class="flex items-center justify-between w-full text-left bg-slate-50 hover:bg-slate-100 p-3 rounded-xl border border-slate-200 transition-colors">
                  <span class="text-sm font-bold text-slate-700 flex items-center gap-2">
                    <svg class="w-5 h-5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    Add a Suggestion or Feature Request (Optional)
                  </span>
                  <svg :class="['w-5 h-5 text-slate-400 transition-transform duration-200', showSuggestionForm ? 'rotate-180' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                </button>
                
                <div v-if="showSuggestionForm" class="mt-4 space-y-4 bg-slate-50 p-4 rounded-xl border border-slate-200">
                  <div>
                    <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Type</label>
                    <div class="flex gap-4">
                      <label class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer">
                        <input type="radio" v-model="suggestionType" value="Suggestion" class="text-purple-600 focus:ring-purple-500"> Suggestion
                      </label>
                      <label class="flex items-center gap-2 text-sm text-slate-700 cursor-pointer">
                        <input type="radio" v-model="suggestionType" value="Feature Request" class="text-purple-600 focus:ring-purple-500"> Feature Request
                      </label>
                    </div>
                  </div>
                  
                  <div>
                    <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Description</label>
                    <textarea v-model="suggestionDescription" rows="2" class="w-full rounded-xl border border-slate-300 p-3 text-sm focus:ring-2 focus:ring-purple-500 outline-none resize-none" placeholder="Describe your suggestion or feature..."></textarea>
                  </div>
                  
                  <div>
                    <label class="block text-[10px] md:text-xs font-bold text-slate-500 uppercase mb-2">Target Deadline (Optional)</label>
                    <input type="date" v-model="suggestionDeadline" class="w-full sm:w-auto bg-white border border-slate-300 text-slate-700 text-sm px-3 py-2 rounded-xl outline-none focus:ring-2 focus:ring-purple-500">
                  </div>
                </div>
              </div>

              <div v-if="message" :class="['p-3 md:p-4 rounded-xl text-xs md:text-sm font-medium text-center', message.includes('Success') ? 'bg-teal-50 text-teal-800' : 'bg-red-50 text-red-800']">
                {{ message }}
              </div>
              
              <button type="submit" :disabled="isSubmitting || !isFormValid" :class="['w-full font-bold py-3.5 md:py-4 rounded-xl shadow-md transition-all duration-200 text-sm md:text-base', isSubmitting || !isFormValid ? 'bg-slate-200 text-slate-400 cursor-not-allowed border border-slate-300' : (editingLogId ? 'bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 text-white' : 'bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-700 text-white')]">
                {{ isSubmitting ? 'Saving...' : (!isFormValid ? 'Fill required fields to submit' : (editingLogId ? 'Update Existing Log' : 'Submit Daily Update')) }}
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

      <!-- Chronological Daily Progress Feed -->
      <div v-if="activeTab === 'progress'" class="space-y-6">
        <div class="bg-white p-4 md:p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-4 items-center justify-between">
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

        <div v-if="filteredFeedDays.length === 0" class="border border-dashed border-slate-300 rounded-2xl p-12 text-center bg-white shadow-sm">
          <svg class="w-12 h-12 text-slate-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <p class="text-sm font-semibold text-slate-500">No matching progress updates found.</p>
        </div>

        <div v-else class="space-y-8 relative before:absolute before:inset-y-0 before:left-4 md:before:left-6 before:w-0.5 before:bg-slate-200 pl-8 md:pl-12">
          <div v-for="day in paginatedFeedDays" :key="day.date" class="relative group">
            <div class="absolute left-[-32px] md:left-[-48px] w-6 h-6 md:w-8 md:h-8 rounded-full border-4 border-slate-50 bg-gradient-to-tr from-teal-500 to-blue-500 shadow-sm z-10 flex items-center justify-center text-white text-[10px] font-bold">
              ✓
            </div>
            
            <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 md:p-6 hover:shadow-md transition-shadow">
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

      <div v-if="activeTab === 'suggestions'" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="bg-slate-50 px-4 md:px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <h3 class="text-base md:text-lg font-bold text-slate-800">Team Suggestions & Features</h3>
          <span class="bg-purple-100 text-purple-800 text-xs font-bold px-3 py-1 rounded-full">{{ teamSuggestions.length }} Items</span>
        </div>
        <div class="p-4 md:p-6">
          <div v-if="teamSuggestions.length === 0" class="border border-dashed border-slate-300 rounded-lg p-10 text-center bg-slate-50">
            <p class="text-slate-500 italic text-sm">No suggestions or feature requests logged for your team yet.</p>
          </div>
          <div v-else class="space-y-4">
            <div v-for="item in teamSuggestions" :key="item.id" class="border border-slate-200 rounded-xl p-4 bg-white shadow-sm flex flex-col md:flex-row gap-4">
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <span :class="['text-[10px] font-bold px-2 py-0.5 rounded-full border', item.suggestionType === 'Suggestion' ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-purple-50 text-purple-700 border-purple-200']">
                    {{ item.suggestionType }}
                  </span>
                  <span :class="['text-[10px] font-bold px-2 py-0.5 rounded-full border', getStatusClass(item.suggestionStatus)]">
                    {{ item.suggestionStatus }}
                  </span>
                </div>
                <p class="text-sm text-slate-800 font-medium mb-2 whitespace-pre-line">{{ item.suggestionDescription }}</p>
                <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider">
                  Logged by {{ item.name }} on {{ new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                </p>
              </div>
              <div v-if="item.suggestionDeadline" class="md:text-right shrink-0">
                <p class="text-[10px] text-slate-500 font-bold uppercase tracking-wider mb-1">Target Deadline</p>
                <p class="text-sm font-bold text-slate-800 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg inline-block">
                  {{ new Date(item.suggestionDeadline).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                </p>
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
  { id: 'progress', label: 'Daily Progress', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>' },
  { id: 'attendance', label: 'My Attendance', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path></svg>' },
  { id: 'suggestions', label: 'Suggestions', icon: '<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>' },
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
const allLogs = ref([])
const allMoMs = ref([])
const allHolidays = ref([])
const availableTeams = ref(["Digi Yatra", "OCR", "FHIR", "MIRTH Connect", "ChatBot", "Blood Connect"])

const feedFilterDate = ref('')
const feedSearchQuery = ref('')

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

const showSuggestionForm = ref(false)
const suggestionType = ref('Suggestion')
const suggestionDescription = ref('')
const suggestionDeadline = ref('')

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
    suggestionType.value = existingLog.suggestionType || 'Suggestion'
    suggestionDescription.value = existingLog.suggestionDescription || ''
    suggestionDeadline.value = existingLog.suggestionDeadline || ''
    showSuggestionForm.value = !!existingLog.suggestionDescription
  } else {
    editingLogId.value = null
    selectedHours.value = []
    todayLog.value = ''
    tomorrowGoal.value = ''
    suggestionType.value = 'Suggestion'
    suggestionDescription.value = ''
    suggestionDeadline.value = ''
    showSuggestionForm.value = false
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
    // Refresh user profile if it's a student (id > 0)
    if (authStore.user && authStore.user.id > 0) {
      try {
        const userRes = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/users/${authStore.user.id}`)
        if (userRes.ok) {
          const freshUser = await userRes.json()
          authStore.user = freshUser
          localStorage.setItem('trackerUser', JSON.stringify(freshUser))
        }
      } catch (userErr) {
        console.error("Failed to refresh user profile:", userErr)
      }
    }

    const [logsRes, momRes, holidaysRes, teamsRes] = await Promise.all([
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/mom/`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/holidays/`),
      fetch(`${import.meta.env.VITE_API_BASE_URL}/api/teams`)
    ])
    
    // Process Teams
    if (teamsRes.ok) {
      const tData = await teamsRes.json()
      if (Array.isArray(tData)) {
        availableTeams.value = tData.map(t => t.name)
      }
    }
    
    // Process Logs using the new robust helper
    const rawLogs = await logsRes.json()
    if (Array.isArray(rawLogs)) {
      allLogs.value = rawLogs
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
        date: selectedDate.value,
        suggestionType: showSuggestionForm.value ? suggestionType.value : null,
        suggestionDescription: showSuggestionForm.value ? suggestionDescription.value : null,
        suggestionDeadline: showSuggestionForm.value ? suggestionDeadline.value : null,
      })
    })

    if (res.ok) {
      message.value = editingLogId.value ? 'Success! Log updated.' : 'Success! Log saved.'
      setTimeout(() => message.value = '', 3000)
      
      // Auto-refresh logs table using the new robust helper
      const newLogRes = await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/logs`)
      const newLogs = await newLogRes.json()
      if (Array.isArray(newLogs)) {
        allLogs.value = newLogs
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
  
  // Student can ONLY see progress of their assigned team!
  const userTeam = authStore.user?.team
  if (!userTeam) {
    return []
  }
  logs = logs.filter(log => log.team === userTeam)
  
  if (feedFilterDate.value) {
    logs = logs.filter(log => log.date === feedFilterDate.value)
  }
  
  if (feedSearchQuery.value) {
    const q = feedSearchQuery.value.toLowerCase()
    logs = logs.filter(log => 
      (log.name && log.name.toLowerCase().includes(q)) ||
      (log.rollNumber && log.rollNumber.toLowerCase().includes(q)) ||
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

// Suggestions Logic
const teamSuggestions = computed(() => {
  const userTeam = authStore.user?.team
  if (!userTeam) return []
  return allLogs.value
    .filter(log => log.team === userTeam && log.suggestionDescription)
    .sort((a, b) => new Date(b.date) - new Date(a.date))
})

const getStatusClass = (status) => {
  switch (status) {
    case 'Resolved': return 'bg-teal-50 text-teal-700 border-teal-200'
    case 'In Progress': return 'bg-blue-50 text-blue-700 border-blue-200'
    case 'Rejected': return 'bg-red-50 text-red-700 border-red-200'
    default: return 'bg-slate-100 text-slate-700 border-slate-300' // Pending
  }
}
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>