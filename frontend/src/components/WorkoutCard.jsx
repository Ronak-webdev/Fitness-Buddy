/**
 * WorkoutCard.jsx
 * ---------------
 * Rendered when a message has type="workout".
 * Features interactive exercise checkboxes, duration timer, and workout completion logging.
 */

import { useState } from 'react'

export default function WorkoutCard({ data, message }) {
  const [completedExercises, setCompletedExercises] = useState({})
  const [workoutLogged, setWorkoutLogged] = useState(false)

  if (!data) {
    return (
      <div className="bg-brand-50 border border-brand-200 rounded-2xl p-4 text-brand-800 text-sm">
        {message}
      </div>
    )
  }

  const { title, duration_minutes, difficulty, sections = [] } = data

  const toggleExercise = (secIdx, exIdx) => {
    const key = `${secIdx}-${exIdx}`
    setCompletedExercises(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  // Calculate progress
  const totalExercises = sections.reduce((sum, s) => sum + (s.exercises || []).length, 0)
  const doneCount = Object.values(completedExercises).filter(Boolean).length
  const progressPercent = totalExercises > 0 ? Math.round((doneCount / totalExercises) * 100) : 0

  return (
    <div className="bg-white border border-slate-200/80 rounded-2xl shadow-md overflow-hidden max-w-lg w-full transition-all">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-brand-600 via-emerald-600 to-teal-600 px-5 py-4 text-white">
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] uppercase font-extrabold bg-white/20 px-2 py-0.5 rounded-full backdrop-blur-xs">
                {difficulty || 'All Levels'}
              </span>
              {duration_minutes && (
                <span className="text-[10px] uppercase font-bold bg-white/20 px-2 py-0.5 rounded-full backdrop-blur-xs flex items-center gap-1">
                  ⏱ {duration_minutes} min
                </span>
              )}
            </div>
            <h3 className="font-extrabold text-base sm:text-lg mt-1 tracking-tight">
              {title || 'Personalized Workout Routine'}
            </h3>
          </div>
          <div className="w-11 h-11 rounded-xl bg-white/15 flex items-center justify-center text-2xl backdrop-blur-xs">
            🏋️
          </div>
        </div>

        {/* Progress bar */}
        {totalExercises > 0 && (
          <div className="mt-3 pt-2 border-t border-white/15">
            <div className="flex justify-between text-[11px] font-medium text-emerald-100 mb-1">
              <span>Exercises Completed</span>
              <span>{doneCount} / {totalExercises} ({progressPercent}%)</span>
            </div>
            <div className="w-full bg-black/20 h-1.5 rounded-full overflow-hidden">
              <div 
                className="bg-white h-full transition-all duration-300 rounded-full"
                style={{ width: `${progressPercent}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>

      {/* Summary message */}
      {message && (
        <div className="px-5 pt-3 text-xs sm:text-sm text-slate-600 font-medium italic bg-slate-50/50 border-b border-slate-100 pb-2.5">
          "{message}"
        </div>
      )}

      {/* Sections & Exercises */}
      <div className="p-4 sm:p-5 space-y-4">
        {sections.map((section, si) => (
          <div key={si} className="space-y-2">
            <div className="flex items-center justify-between pb-1 border-b border-slate-100">
              <h4 className="text-xs font-bold uppercase tracking-wider text-brand-700 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-brand-500"></span>
                {section.name}
              </h4>
              <span className="text-[11px] text-slate-400 font-medium">
                {(section.exercises || []).length} exercise{(section.exercises || []).length !== 1 ? 's' : ''}
              </span>
            </div>

            <div className="space-y-2">
              {(section.exercises || []).map((ex, ei) => {
                const isChecked = !!completedExercises[`${si}-${ei}`]
                return (
                  <div 
                    key={ei}
                    onClick={() => toggleExercise(si, ei)}
                    className={`p-3 rounded-xl border transition-all duration-200 cursor-pointer flex items-start gap-3 select-none ${
                      isChecked 
                        ? 'bg-emerald-50/60 border-emerald-200 shadow-xs' 
                        : 'bg-slate-50/70 border-slate-200/80 hover:bg-slate-100/80 hover:border-slate-300'
                    }`}
                  >
                    {/* Checkbox */}
                    <div className={`w-5 h-5 rounded-md flex items-center justify-center text-xs shrink-0 mt-0.5 transition-colors ${
                      isChecked 
                        ? 'bg-brand-600 text-white font-bold' 
                        : 'border-2 border-slate-300 bg-white'
                    }`}>
                      {isChecked && '✓'}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-baseline justify-between gap-2">
                        <p className={`text-sm font-semibold ${isChecked ? 'line-through text-slate-400' : 'text-slate-800'}`}>
                          {ex.name}
                        </p>
                        {(ex.sets || ex.reps_or_duration) && (
                          <span className="text-[11px] font-bold text-brand-700 bg-brand-100/60 px-2 py-0.5 rounded-md shrink-0">
                            {ex.sets ? `${ex.sets} sets` : ''}
                            {ex.sets && ex.reps_or_duration ? ' × ' : ''}
                            {ex.reps_or_duration || ''}
                          </span>
                        )}
                      </div>

                      {/* Instructions */}
                      {(ex.instructions || ex.description) && (
                        <p className={`text-xs mt-1 leading-relaxed ${isChecked ? 'text-slate-400' : 'text-slate-500'}`}>
                          {ex.instructions || ex.description}
                        </p>
                      )}

                      {/* Muscles targeted */}
                      {ex.muscles_targeted && (
                        <p className="text-[10px] text-slate-400 font-medium mt-1">
                          🎯 Targets: {ex.muscles_targeted}
                        </p>
                      )}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        ))}
      </div>

      {/* Completion Action */}
      <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
        <span className="text-[11px] text-slate-500">
          Tap an exercise to mark as done
        </span>
        <button
          onClick={() => setWorkoutLogged(true)}
          disabled={workoutLogged}
          className={`px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm ${
            workoutLogged 
              ? 'bg-emerald-600 text-white cursor-default' 
              : 'bg-slate-900 text-white hover:bg-brand-600'
          }`}
        >
          {workoutLogged ? '✓ Logged to Streak!' : 'Complete Workout 💪'}
        </button>
      </div>
    </div>
  )
}
