/**
 * frontend/src/hooks/useChat.js
 * --------------------------------
 * THE ONLY FILE that communicates with the backend API.
 * All other components must import from this hook.
 *
 * Exposes:
 *   messages       - array of { role, type, content, data }
 *   isLoading      - true while awaiting a backend response
 *   sendMessage(text) - sends a user message and appends response
 *   startSession(username) - POST /api/profile/start
 *   fetchDashboard()       - GET /api/dashboard
 *   fetchProfile()         - GET /api/profile
 *   username               - the current session username (or null)
 *   isNewUser              - true if user hasn't completed onboarding
 */

import { useState, useCallback, useRef } from 'react'

const API_BASE = '/api'

// Shared fetch helper — always sends cookies (credentials: 'include')
async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }

  return res.json()
}

export function useChat() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [username, setUsername] = useState(null)
  const [isNewUser, setIsNewUser] = useState(false)
  const [dashboard, setDashboard] = useState(null)
  const [profile, setProfile] = useState(null)

  // Prevent double-sends during React StrictMode double-invoke
  const sendingRef = useRef(false)

  // ------------------------------------------------------------------
  // Session management
  // ------------------------------------------------------------------

  const startSession = useCallback(async (name) => {
    const data = await apiFetch(`/profile/start?username=${encodeURIComponent(name)}`, {
      method: 'POST',
    })
    setUsername(name.trim().toLowerCase())
    setIsNewUser(data.is_new_user)
    return data
  }, [])

  // ------------------------------------------------------------------
  // Dashboard & profile
  // ------------------------------------------------------------------

  const fetchDashboard = useCallback(async () => {
    const data = await apiFetch('/dashboard')
    setDashboard(data)
    return data
  }, [])

  const fetchProfile = useCallback(async () => {
    const data = await apiFetch('/profile')
    setProfile(data)
    return data
  }, [])

  // ------------------------------------------------------------------
  // Chat
  // ------------------------------------------------------------------

  const sendMessage = useCallback(async (text) => {
    if (!text.trim() || sendingRef.current) return
    sendingRef.current = true

    // Optimistically append the user's message
    const userMsg = { role: 'user', type: 'text', content: text, data: null }
    setMessages((prev) => [...prev, userMsg])
    setIsLoading(true)

    try {
      const data = await apiFetch('/chat', {
        method: 'POST',
        body: JSON.stringify({ message: text }),
      })

      // data = { type, message, data }
      const assistantMsg = {
        role: 'assistant',
        type: data.type,
        content: data.message,
        data: data.data || null,
      }
      setMessages((prev) => [...prev, assistantMsg])

      // Refresh dashboard stats after every message (streak may change)
      fetchDashboard().catch(() => {})
    } catch (err) {
      const errMsg = {
        role: 'assistant',
        type: 'text',
        content: `Sorry, something went wrong: ${err.message}. Please try again.`,
        data: null,
      }
      setMessages((prev) => [...prev, errMsg])
    } finally {
      setIsLoading(false)
      sendingRef.current = false
    }
  }, [fetchDashboard])

  // ------------------------------------------------------------------
  // Clear chat (local only — does not delete Db2 history)
  // ------------------------------------------------------------------

  const clearMessages = useCallback(() => setMessages([]), [])

  return {
    messages,
    isLoading,
    sendMessage,
    clearMessages,
    startSession,
    fetchDashboard,
    fetchProfile,
    username,
    isNewUser,
    dashboard,
    profile,
  }
}
