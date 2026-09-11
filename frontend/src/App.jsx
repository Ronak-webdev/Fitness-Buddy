import { useEffect } from 'react'
import { useChat } from './hooks/useChat'
import ProfileSetup from './components/ProfileSetup'
import ChatWindow from './components/ChatWindow'
import Dashboard from './components/Dashboard'

export default function App() {
  const {
    username,
    isNewUser,
    startSession,
    messages,
    isLoading,
    sendMessage,
    dashboard,
    fetchDashboard
  } = useChat()

  // Fetch dashboard stats when user logs in
  useEffect(() => {
    if (username && !isNewUser) {
      fetchDashboard()
    }
  }, [username, isNewUser, fetchDashboard])

  if (!username) {
    return <ProfileSetup onStart={startSession} />
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col md:flex-row font-sans text-slate-800">
      {/* Left sidebar: Clean Minimalist Dashboard */}
      <aside className="w-full md:w-72 lg:w-80 md:h-screen shrink-0 border-b md:border-b-0 md:border-r border-emerald-100/80 bg-white shadow-xs">
        <Dashboard 
          username={username} 
          dashboard={dashboard} 
          onAction={sendMessage} 
        />
      </aside>

      {/* Main chat area */}
      <main className="flex-1 h-[calc(100vh-auto)] md:h-screen flex flex-col bg-gradient-to-b from-emerald-50/20 to-white overflow-hidden">
        <ChatWindow 
          messages={messages} 
          isLoading={isLoading} 
          onSend={sendMessage} 
        />
      </main>
    </div>
  )
}
