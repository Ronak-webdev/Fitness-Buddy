/**
 * MessageBubble.jsx
 * -----------------
 * Renders a single chat turn with modern avatars, timestamps, and card routing.
 */

import WorkoutCard from './WorkoutCard.jsx'
import MealCard from './MealCard.jsx'
import MotivationCard from './MotivationCard.jsx'

export default function MessageBubble({ message }) {
  const { role, type, content, data } = message
  const isUser = role === 'user'

  // ---- User bubble ----
  if (isUser) {
    return (
      <div className="flex justify-end my-1 group">
        <div className="flex items-end gap-2 max-w-[85%] sm:max-w-md">
          <div className="bg-gradient-to-r from-brand-600 to-emerald-600 text-white rounded-2xl rounded-br-xs px-4 py-3 text-sm leading-relaxed shadow-md shadow-brand-500/10">
            {content}
          </div>
          <div className="w-7 h-7 rounded-full bg-slate-200 text-slate-700 flex items-center justify-center text-xs font-bold shrink-0 mb-1">
            👤
          </div>
        </div>
      </div>
    )
  }

  // ---- Assistant: specialised cards ----
  if (type === 'workout') {
    return (
      <div className="flex justify-start my-2">
        <div className="flex items-start gap-2.5 max-w-[95%] sm:max-w-xl">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-brand-600 to-teal-400 text-white flex items-center justify-center text-sm shrink-0 shadow-sm mt-1">
            🏋️
          </div>
          <WorkoutCard data={data} message={content} />
        </div>
      </div>
    )
  }

  if (type === 'meal') {
    return (
      <div className="flex justify-start my-2">
        <div className="flex items-start gap-2.5 max-w-[95%] sm:max-w-xl">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-orange-500 to-amber-400 text-white flex items-center justify-center text-sm shrink-0 shadow-sm mt-1">
            🥗
          </div>
          <MealCard data={data} message={content} />
        </div>
      </div>
    )
  }

  if (type === 'motivation') {
    return (
      <div className="flex justify-start my-2">
        <div className="flex items-start gap-2.5 max-w-[95%] sm:max-w-xl">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-purple-600 to-pink-500 text-white flex items-center justify-center text-sm shrink-0 shadow-sm mt-1">
            ✨
          </div>
          <MotivationCard data={data} message={content} />
        </div>
      </div>
    )
  }

  // ---- Defensive Fallback: If content is JSON string representing a workout or meal ----
  if (typeof content === 'string' && content.trim().startsWith('{') && content.trim().endsWith('}')) {
    try {
      const parsed = JSON.parse(content.trim())
      if (parsed.sections && parsed.title) {
        return (
          <div className="flex justify-start my-2">
            <div className="flex items-start gap-2.5 max-w-[95%] sm:max-w-xl">
              <div className="w-8 h-8 rounded-xl bg-brand-600 text-white flex items-center justify-center text-sm shrink-0 shadow-sm mt-1">🏋️</div>
              <WorkoutCard data={parsed} message={message.message || "Here is your personalised workout routine! 💪"} />
            </div>
          </div>
        )
      } else if (parsed.meals) {
        return (
          <div className="flex justify-start my-2">
            <div className="flex items-start gap-2.5 max-w-[95%] sm:max-w-xl">
              <div className="w-8 h-8 rounded-xl bg-orange-500 text-white flex items-center justify-center text-sm shrink-0 shadow-sm mt-1">🥗</div>
              <MealCard data={parsed} message={parsed.tip || "Here are some wholesome meal suggestions! 🥗"} />
            </div>
          </div>
        )
      }
    } catch {
      // Not JSON, continue with normal text bubble
    }
  }

  // ---- Assistant: plain text bubble ----
  return (
    <div className="flex justify-start my-1.5">
      <div className="flex items-start gap-2.5 max-w-[85%] sm:max-w-lg">
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center text-sm shrink-0 shadow-xs mt-0.5">
          🤖
        </div>
        <div className="bg-white border border-emerald-100 rounded-2xl rounded-tl-xs px-4 py-3 text-sm text-slate-800 leading-relaxed shadow-xs">
          <div className="flex items-center gap-1.5 mb-1">
            <span className="text-[11px] font-bold text-slate-400">Fitness Buddy</span>
            <span className="text-[10px] bg-emerald-50 text-emerald-700 font-semibold px-1.5 py-0.2 rounded">Coach</span>
          </div>
          <p className="whitespace-pre-wrap">{content}</p>
        </div>
      </div>
    </div>
  )
}

// Typing indicator — shown while isLoading is true
export function TypingIndicator() {
  return (
    <div className="flex justify-start my-2">
      <div className="flex items-start gap-2.5">
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 text-white flex items-center justify-center text-sm shrink-0 shadow-xs mt-0.5">
          🤖
        </div>
        <div className="bg-white border border-emerald-100 rounded-2xl rounded-tl-xs px-4 py-3 shadow-xs flex items-center gap-2">
          <span className="text-xs text-slate-400 font-medium">Granite thinking</span>
          <div className="flex gap-1.5">
            <span className="w-2 h-2 bg-emerald-500 rounded-full bounce-dot" />
            <span className="w-2 h-2 bg-emerald-500 rounded-full bounce-dot" />
            <span className="w-2 h-2 bg-emerald-500 rounded-full bounce-dot" />
          </div>
        </div>
      </div>
    </div>
  )
}
