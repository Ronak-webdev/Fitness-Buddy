/**
 * MotivationCard.jsx
 * ------------------
 * Rendered when a message has type="motivation".
 * Minimalist white and soft green gradient motivation card.
 */

import StreakBadge from './StreakBadge.jsx'

export default function MotivationCard({ data, message }) {
  const streak = data?.streak ?? 0
  const badge = data?.badge

  return (
    <div className="bg-gradient-to-br from-emerald-50/70 via-white to-teal-50/50 border border-emerald-200/80 rounded-2xl p-5 max-w-lg w-full text-slate-800 shadow-sm">
      <div className="flex items-start gap-3.5">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center text-lg shrink-0 shadow-xs mt-0.5">
          ✨
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-2">
            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-800 bg-emerald-100/80 px-2.5 py-0.5 rounded-full border border-emerald-200">
              Mindset &amp; Motivation
            </span>
            {streak > 0 && <StreakBadge streak={streak} />}
          </div>

          <p className="text-slate-800 font-medium text-sm leading-relaxed whitespace-pre-wrap">
            {message}
          </p>

          {badge && (
            <div className="mt-3 inline-flex items-center gap-1.5 px-3 py-1 rounded-xl bg-white border border-emerald-200 text-xs text-emerald-800 font-semibold shadow-2xs">
              <span>🏅 Milestone:</span>
              <span className="text-emerald-700 font-bold">{badge}</span>
            </div>
          )}

          {/* Daily micro challenge */}
          <div className="mt-3.5 pt-3 border-t border-emerald-100 flex items-center gap-2 text-xs text-slate-500">
            <span className="text-sm">🎯</span>
            <span className="text-[11px] font-medium text-emerald-900/80">
              Daily Challenge: Consistency beats intensity. Move for 15 minutes today!
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
