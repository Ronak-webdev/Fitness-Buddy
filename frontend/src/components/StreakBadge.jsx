/**
 * StreakBadge.jsx
 * ---------------
 * Displays the user's current workout streak with an animated flame and milestone tier.
 */

export default function StreakBadge({ streak = 0 }) {
  const isHigh = streak >= 7
  const isMid = streak >= 3

  return (
    <div className={`inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border shadow-sm transition-all duration-300 ${
      isHigh 
        ? 'bg-gradient-to-r from-orange-500 to-amber-500 text-white border-orange-400 shadow-orange-500/20' 
        : isMid 
        ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white border-emerald-400 shadow-emerald-500/20'
        : 'bg-slate-100 text-slate-700 border-slate-200'
    }`}>
      <span className="text-base flame-animated">
        {streak >= 3 ? '🔥' : '⚡'}
      </span>
      <span className="font-bold text-xs tracking-wide">
        {streak} {streak === 1 ? 'DAY STREAK' : 'DAYS STREAK'}
      </span>
      {streak > 0 && (
        <span className={`text-[10px] uppercase px-1.5 py-0.5 rounded-md font-semibold ${
          isHigh ? 'bg-white/20 text-white' : isMid ? 'bg-white/20 text-white' : 'bg-slate-200 text-slate-600'
        }`}>
          {isHigh ? 'On Fire' : isMid ? 'Consistent' : 'Active'}
        </span>
      )}
    </div>
  )
}
