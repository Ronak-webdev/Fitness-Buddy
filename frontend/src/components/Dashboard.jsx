import React from 'react'
import StreakBadge from './StreakBadge'

export default function Dashboard({ username, dashboard, onAction }) {
  const streak = dashboard?.streak || 0
  const fitnessGoal = dashboard?.goal || 'General Health'
  const fitnessLevel = dashboard?.fitness_level || 'Beginner'
  const dailyTip = dashboard?.daily_tip || 'Consistency in small habits builds life-changing strength.'

  return (
    <div className="h-full flex flex-col p-6 bg-white text-slate-800 overflow-y-auto">
      {/* User Profile Header */}
      <div className="flex items-center gap-3.5 pb-6 border-b border-emerald-100">
        <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center text-white font-bold text-lg shadow-sm">
          {username.charAt(0).toUpperCase()}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h2 className="text-base font-bold text-slate-900 truncate capitalize">
              {username}
            </h2>
            <span className="text-[10px] uppercase font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200 px-2 py-0.5 rounded-full">
              {fitnessLevel}
            </span>
          </div>
          <p className="text-xs text-slate-500 truncate mt-0.5 capitalize">
            {fitnessGoal.replace('_', ' ')}
          </p>
        </div>
      </div>

      {/* Streak Badge */}
      <div className="my-6">
        <div className="p-4 rounded-2xl bg-gradient-to-r from-emerald-50 to-teal-50/60 border border-emerald-100 flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">Consistency</p>
            <p className="text-lg font-extrabold text-emerald-950 mt-0.5">
              {streak} {streak === 1 ? 'Day' : 'Days'}
            </p>
          </div>
          <StreakBadge streak={streak} />
        </div>
      </div>

      {/* Minimal Quick Actions */}
      <div className="flex-1 space-y-3">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
          Quick Actions
        </h3>
        
        <button 
          onClick={() => onAction('Create a personalized 30-minute beginner home workout for a user with no equipment. Include warm-up, main exercises, cool-down, duration and simple instructions.')}
          className="w-full text-left p-3.5 rounded-xl bg-white hover:bg-emerald-50/80 border border-slate-200/80 hover:border-emerald-300 transition-all flex items-center justify-between group shadow-xs"
        >
          <div className="flex items-center gap-3">
            <span className="text-lg">🏋️</span>
            <div>
              <p className="text-xs font-semibold text-slate-800 group-hover:text-emerald-700">Home Workout</p>
              <p className="text-[11px] text-slate-400">30 min beginner routine</p>
            </div>
          </div>
          <span className="text-slate-400 group-hover:text-emerald-600 text-xs">→</span>
        </button>

        <button 
          onClick={() => onAction('Suggest three simple healthy high-protein Indian breakfast options with approximate calories, ingredients and practical nutrition tips.')}
          className="w-full text-left p-3.5 rounded-xl bg-white hover:bg-emerald-50/80 border border-slate-200/80 hover:border-emerald-300 transition-all flex items-center justify-between group shadow-xs"
        >
          <div className="flex items-center gap-3">
            <span className="text-lg">🥗</span>
            <div>
              <p className="text-xs font-semibold text-slate-800 group-hover:text-emerald-700">Healthy Meals</p>
              <p className="text-[11px] text-slate-400">High-protein breakfast</p>
            </div>
          </div>
          <span className="text-slate-400 group-hover:text-emerald-600 text-xs">→</span>
        </button>

        <button 
          onClick={() => onAction('I feel unmotivated and inconsistent with exercise. Give me practical motivation and a small habit-building challenge that I can complete today.')}
          className="w-full text-left p-3.5 rounded-xl bg-white hover:bg-emerald-50/80 border border-slate-200/80 hover:border-emerald-300 transition-all flex items-center justify-between group shadow-xs"
        >
          <div className="flex items-center gap-3">
            <span className="text-lg">✨</span>
            <div>
              <p className="text-xs font-semibold text-slate-800 group-hover:text-emerald-700">Daily Motivation</p>
              <p className="text-[11px] text-slate-400">Consistency & mindset</p>
            </div>
          </div>
          <span className="text-slate-400 group-hover:text-emerald-600 text-xs">→</span>
        </button>

        {/* Daily Tip */}
        <div className="mt-6 p-4 rounded-xl bg-emerald-50/60 border border-emerald-100">
          <p className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider mb-1">
            Coach Tip
          </p>
          <p className="text-xs text-emerald-900/80 leading-relaxed italic">
            "{dailyTip}"
          </p>
        </div>
      </div>
      
      {/* Footer Branding */}
      <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
        <span className="flex items-center gap-1.5 text-[11px] text-slate-500">
          <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          IBM Granite 4
        </span>
        <span className="text-[10px] bg-slate-100 px-2 py-0.5 rounded text-slate-500">
          IBM Bob
        </span>
      </div>
    </div>
  )
}
