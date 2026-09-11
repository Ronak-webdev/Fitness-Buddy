/**
 * MealCard.jsx
 * ------------
 * Rendered when a message has type="meal".
 * Features macro breakdown badges, prep time, ingredient highlights, and practical nutrition tips.
 */

export default function MealCard({ data, message }) {
  if (!data) {
    return (
      <div className="bg-orange-50 border border-orange-200 rounded-2xl p-4 text-orange-800 text-sm">
        {message}
      </div>
    )
  }

  const meals = data.meals || []
  const dailyCalories = data.daily_calories

  return (
    <div className="bg-white border border-slate-200/80 rounded-2xl shadow-md overflow-hidden max-w-lg w-full">
      {/* Header */}
      <div className="bg-gradient-to-r from-orange-500 via-amber-500 to-yellow-500 px-5 py-4 text-white flex items-center justify-between">
        <div>
          <span className="text-[10px] uppercase font-extrabold bg-white/20 px-2 py-0.5 rounded-full backdrop-blur-xs">
            Nutrition Coach
          </span>
          <h3 className="font-extrabold text-base sm:text-lg mt-1 tracking-tight">
            Wholesome Meal Recommendations
          </h3>
          {dailyCalories && (
            <p className="text-orange-100 text-xs mt-0.5 font-medium">
              Daily Target: ~{dailyCalories} kcal / day
            </p>
          )}
        </div>
        <div className="w-11 h-11 rounded-xl bg-white/15 flex items-center justify-center text-2xl backdrop-blur-xs">
          🥗
        </div>
      </div>

      {/* Summary message / Coaching tip */}
      {message && (
        <div className="px-5 pt-3 pb-2.5 bg-orange-50/50 border-b border-orange-100/60 text-xs sm:text-sm text-slate-700 font-medium italic">
          "{message}"
        </div>
      )}

      {/* Meal list */}
      <div className="p-4 sm:p-5 space-y-3.5">
        {meals.map((meal, i) => (
          <div 
            key={i} 
            className="p-3.5 rounded-xl border border-orange-200/60 bg-gradient-to-br from-orange-50/30 via-white to-amber-50/20 hover:border-orange-300 transition-all shadow-xs"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-center gap-2">
                <span className="w-6 h-6 rounded-lg bg-orange-500 text-white flex items-center justify-center text-xs font-bold shrink-0">
                  {i + 1}
                </span>
                <p className="font-bold text-slate-800 text-sm">{meal.name}</p>
              </div>
              {meal.calories && (
                <span className="text-xs font-bold text-orange-700 bg-orange-100/80 px-2.5 py-0.5 rounded-full shrink-0">
                  ⚡ {meal.calories} kcal
                </span>
              )}
            </div>

            {meal.description && (
              <p className="text-xs text-slate-600 mt-2 leading-relaxed pl-8">
                {meal.description}
              </p>
            )}

            {/* Macros and details */}
            <div className="flex flex-wrap items-center gap-1.5 mt-3 pl-8">
              {meal.protein_g && (
                <span className="text-[11px] font-bold bg-emerald-50 border border-emerald-200 rounded-lg px-2.5 py-0.5 text-emerald-700 flex items-center gap-1">
                  🥩 {meal.protein_g}g Protein
                </span>
              )}
              {meal.prep_time_minutes && (
                <span className="text-[11px] font-semibold bg-blue-50 border border-blue-200 rounded-lg px-2.5 py-0.5 text-blue-700 flex items-center gap-1">
                  ⏱ {meal.prep_time_minutes} min
                </span>
              )}
              {(meal.tags || []).map((tag, ti) => (
                <span key={ti} className="text-[10px] font-medium bg-slate-100 border border-slate-200/60 rounded-lg px-2 py-0.5 text-slate-600 capitalize">
                  {tag.replace('_', ' ')}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Practical Nutrition Tip callout */}
      <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center gap-2.5 text-xs text-slate-500">
        <span className="text-base">💡</span>
        <p className="text-[11px] leading-relaxed">
          Tip: Pair these meals with adequate hydration (2.5L-3L daily) to optimize nutrient absorption.
        </p>
      </div>
    </div>
  )
}
