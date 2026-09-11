/**
 * ProfileSetup.jsx
 * ----------------
 * Clean, minimalistic welcome screen with white & green gradient theme.
 */

import { useState } from 'react'

export default function ProfileSetup({ onStart }) {
  const [name, setName] = useState('')
  const [goal, setGoal] = useState('general_health')
  const [level, setLevel] = useState('beginner')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const goals = [
    { id: 'general_health', label: 'General Fitness', icon: '⚡' },
    { id: 'weight_loss', label: 'Fat Loss', icon: '🔥' },
    { id: 'muscle_gain', label: 'Muscle Gain', icon: '💪' },
    { id: 'endurance', label: 'Endurance', icon: '🏃' },
  ]

  const levels = [
    { id: 'beginner', label: 'Beginner' },
    { id: 'intermediate', label: 'Intermediate' },
    { id: 'advanced', label: 'Advanced' },
  ]

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (name.trim().length < 2) {
      setError('Please enter at least 2 characters.')
      return
    }
    setError('')
    setLoading(true)
    try {
      await onStart(name.trim())
    } catch (err) {
      setError(err.message || 'Could not start session. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-white to-teal-50 flex items-center justify-center p-4 selection:bg-emerald-500 selection:text-white font-sans">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl shadow-emerald-500/5 border border-emerald-100 p-8">
        
        {/* Header Badges */}
        <div className="flex items-center justify-between mb-6">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            AICTE-2026 Problem #13
          </span>
          <span className="text-xs text-slate-400 font-medium">
            IBM Bob Project
          </span>
        </div>

        {/* Hero Title */}
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-500 mx-auto flex items-center justify-center text-2xl shadow-md shadow-emerald-500/20 mb-3 text-white">
            🏋️
          </div>
          <h1 className="text-2xl font-bold text-slate-900">
            Fitness Buddy
          </h1>
          <p className="text-slate-500 text-xs mt-1">
            Personal AI Coach powered by <span className="font-semibold text-emerald-600">IBM Granite</span>
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Name input */}
          <div>
            <label htmlFor="username" className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
              What is your name?
            </label>
            <input
              id="username"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. Ronak, Priya, Alex..."
              maxLength={30}
              autoFocus
              className="w-full bg-slate-50/70 border border-slate-200 rounded-xl px-4 py-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white focus:border-transparent transition-all"
            />
          </div>

          {/* Goal Selector */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-2">
              Primary Goal
            </label>
            <div className="grid grid-cols-2 gap-2">
              {goals.map((g) => (
                <button
                  key={g.id}
                  type="button"
                  onClick={() => setGoal(g.id)}
                  className={`px-3 py-2.5 rounded-xl border text-xs font-medium flex items-center gap-2 transition-all ${
                    goal === g.id
                      ? 'bg-emerald-600 text-white border-emerald-600 shadow-sm'
                      : 'bg-white text-slate-700 border-slate-200 hover:bg-emerald-50/60'
                  }`}
                >
                  <span>{g.icon}</span>
                  <span>{g.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Level Selector */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-2">
              Experience Level
            </label>
            <div className="grid grid-cols-3 gap-2">
              {levels.map((l) => (
                <button
                  key={l.id}
                  type="button"
                  onClick={() => setLevel(l.id)}
                  className={`py-2 px-1 rounded-xl border text-center text-xs font-medium transition-all ${
                    level === l.id
                      ? 'bg-slate-800 text-white border-slate-800'
                      : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  {l.label}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <p className="text-red-500 text-xs font-medium bg-red-50 p-2.5 rounded-lg border border-red-200">{error}</p>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-6 rounded-xl font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 shadow-md shadow-emerald-500/20 transition-all disabled:opacity-50 text-sm flex items-center justify-center gap-2"
          >
            {loading ? 'Starting...' : "Start My Routine 💪"}
          </button>
        </form>

        <p className="text-center text-[11px] text-slate-400 mt-6">
          IBM Cloud Lite · IBM Granite · Db2 Persistence
        </p>
      </div>
    </div>
  )
}
