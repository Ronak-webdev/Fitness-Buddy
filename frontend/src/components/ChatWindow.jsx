/**
 * ChatWindow.jsx
 * --------------
 * The main chat interface — modern header + scrollable message list + input bar.
 */

import { useState, useRef, useEffect } from 'react'
import MessageBubble, { TypingIndicator } from './MessageBubble.jsx'

// Quick-action suggestion chips shown when the conversation is empty
const SUGGESTIONS = [
  { text: 'Create a personalized 30-minute beginner home workout for a user with no equipment. Include warm-up, main exercises, cool-down, duration and simple instructions.', label: '🏋️ 30m Beginner Home Workout', tag: 'Workout' },
  { text: 'Suggest three simple healthy high-protein Indian breakfast options with approximate calories, ingredients and practical nutrition tips.', label: '🥗 High-Protein Indian Breakfast', tag: 'Nutrition' },
  { text: 'I feel unmotivated and inconsistent with exercise. Give me practical motivation and a small habit-building challenge that I can complete today.', label: '✨ Overcome Laziness & Daily Habit', tag: 'Motivation' },
  { text: 'Give me a 5-minute quick full body stretch before bed', label: '🌙 5-min Bedtime Stretch', tag: 'Quick' },
]

export default function ChatWindow({ messages, isLoading, onSend }) {
  const [input, setInput] = useState('')
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  // Auto-scroll to the latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleSubmit = (e) => {
    e.preventDefault()
    const text = input.trim()
    if (!text || isLoading) return
    onSend(text)
    setInput('')
    inputRef.current?.focus()
  }

  const handleSuggestion = (promptText) => {
    onSend(promptText)
  }

  return (
    <div className="flex flex-col h-full bg-slate-50/50">
      {/* Top Coach Header Bar */}
      <div className="h-16 px-6 bg-white border-b border-slate-200/80 flex items-center justify-between shadow-xs shrink-0">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-emerald-500 to-teal-400 text-white flex items-center justify-center font-bold text-lg shadow-sm">
              🤖
            </div>
            <span className="absolute -top-0.5 -right-0.5 w-3 h-3 bg-emerald-500 border-2 border-white rounded-full"></span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-bold text-slate-800 text-sm">Fitness Buddy Coach</h3>
              <span className="text-[10px] bg-emerald-50 text-emerald-700 font-semibold px-2 py-0.5 rounded-full border border-emerald-200">
                IBM Granite 4
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Personalized Workouts · Nutrition · Consistency
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="hidden sm:inline-flex items-center gap-1.5 text-xs text-slate-500 bg-slate-100 px-2.5 py-1 rounded-lg border border-slate-200/60">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            Agentic AI Active
          </span>
        </div>
      </div>

      {/* Message list */}
      <div className="flex-1 overflow-y-auto chat-scroll p-4 sm:p-6 space-y-4">
        {messages.length === 0 && !isLoading && (
          <div className="max-w-xl mx-auto text-center py-10">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-500 to-teal-400 text-white flex items-center justify-center text-3xl mx-auto mb-4 shadow-glow">
              💪
            </div>
            <h2 className="text-xl font-bold text-slate-800 mb-2">
              Ready to crush your goals today?
            </h2>
            <p className="text-slate-500 text-sm mb-6 max-w-md mx-auto">
              I can design personalized home workouts, suggest healthy meals with macro details, and keep your consistency streak alive!
            </p>

            <div className="space-y-2 text-left">
              <p className="text-xs font-bold uppercase tracking-wider text-slate-400 px-1">
                Recommended Prompts:
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {SUGGESTIONS.map((s, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSuggestion(s.text)}
                    className="p-3 text-left bg-white hover:bg-brand-50/60 border border-slate-200 hover:border-brand-400 rounded-xl transition-all duration-200 shadow-xs group"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-bold text-brand-600 bg-brand-50 px-2 py-0.5 rounded-md">
                        {s.tag}
                      </span>
                      <span className="text-slate-300 group-hover:text-brand-500 text-xs transition-transform group-hover:translate-x-0.5">→</span>
                    </div>
                    <p className="text-xs font-semibold text-slate-800 group-hover:text-brand-700">
                      {s.label}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {isLoading && <TypingIndicator />}

        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div className="border-t border-slate-200/80 bg-white p-4 shrink-0 shadow-lg">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto flex gap-2.5 items-center">
          <div className="relative flex-1">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask for a workout, high-protein meal, or motivation tip..."
              maxLength={2000}
              disabled={isLoading}
              className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-5 py-3.5 text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500 focus:bg-white focus:border-transparent disabled:bg-slate-100 transition-all shadow-inner"
            />
          </div>
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="bg-gradient-to-r from-brand-600 to-emerald-600 hover:from-brand-500 hover:to-emerald-500 disabled:opacity-40 text-white rounded-2xl w-12 h-12 flex items-center justify-center shrink-0 shadow-md shadow-brand-500/20 hover:shadow-brand-500/40 transition-all duration-200"
            aria-label="Send message"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5">
              <path d="M3.105 3.105a.75.75 0 01.815-.132l12 5.25a.75.75 0 010 1.374l-12 5.25a.75.75 0 01-1.002-.967l2.016-4.393-2.016-4.393a.75.75 0 01.187-.989z" />
            </svg>
          </button>
        </form>
        <div className="text-center mt-2">
          <p className="text-[11px] text-slate-400">
            Fitness Buddy uses IBM Granite &amp; multi-agent reasoning to generate tailored routines.
          </p>
        </div>
      </div>
    </div>
  )
}
