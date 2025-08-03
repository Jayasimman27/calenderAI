import { useState } from 'react'
import { useGoogleLogin } from '@react-oauth/google'
import { jwtDecode } from 'jwt-decode'
import { Calendar, dateFnsLocalizer } from 'react-big-calendar'
import format from 'date-fns/format'
import parse from 'date-fns/parse'
import startOfWeek from 'date-fns/startOfWeek'
import getDay from 'date-fns/getDay'
import enUS from 'date-fns/locale/en-US'
import 'react-big-calendar/lib/css/react-big-calendar.css'
import './App.css'
import ChatBot from './ChatBot'
import LoginPage from './LoginPage'

const locales = {
  'en-US': enUS,
}
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
})

function App() {
  const [myEvents, setMyEvents] = useState([])
  const [user, setUser] = useState(null)
  const [accessToken, setAccessToken] = useState(null)
  const [loading, setLoading] = useState(false)
  const [chatOpen, setChatOpen] = useState(true)

  async function fetchGoogleCalendarEvents(token) {
    setLoading(true)
    try {
      const now = new Date().toISOString()
      const maxTime = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString() // 30 days ahead
      const response = await fetch(
        `https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=${now}&timeMax=${maxTime}&singleEvents=true&orderBy=startTime`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      const data = await response.json()
      if (data.items) {
        const events = data.items.map(event => ({
          title: event.summary || '(No Title)',
          start: event.start.dateTime ? new Date(event.start.dateTime) : new Date(event.start.date),
          end: event.end.dateTime ? new Date(event.end.dateTime) : new Date(event.end.date),
          allDay: !event.start.dateTime,
        }))
        setMyEvents(events)
      }
    } catch (err) {
      alert('Failed to fetch Google Calendar events')
    }
    setLoading(false)
  }

  const login = useGoogleLogin({
    scope: 'https://www.googleapis.com/auth/calendar',
    flow: 'implicit',
    onSuccess: tokenResponse => {
      // Fetch user info using the access token
      fetch('https://www.googleapis.com/oauth2/v3/userinfo', {
        headers: { Authorization: `Bearer ${tokenResponse.access_token}` }
      })
        .then(res => res.json())
        .then(profile => {
          setUser(profile)
          setAccessToken(tokenResponse.access_token)
          fetchGoogleCalendarEvents(tokenResponse.access_token)
        })
    },
    onError: () => alert('Login Failed')
  })

  return (
    <div style={{ minHeight: '100vh', background: '#f5f7fa' }}>
      {!user ? (
        <LoginPage onLogin={login} />
      ) : (
        <>
          <div style={{ marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h1 style={{ color: '#1976d2' }}>TailorTalk Calendar</h1>
            <div>
              <span>Welcome, {user.name}</span>
              <button style={{ marginLeft: '1rem' }} onClick={() => { setUser(null); setAccessToken(null); setMyEvents([]); }}>
                Logout
              </button>
            </div>
          </div>
          {!chatOpen && (
            <button
              style={{ marginBottom: 24, background: '#1976d2', color: '#fff', border: 'none', borderRadius: 8, padding: '12px 32px', fontSize: 18, fontWeight: 'bold', cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.08)' }}
              onClick={() => setChatOpen(true)}
            >
              Open Calendar Bot
            </button>
          )}
          {!chatOpen && !loading && (
            <Calendar
              localizer={localizer}
              events={myEvents}
              startAccessor="start"
              endAccessor="end"
              style={{ height: 600, background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px rgba(0,0,0,0.08)', padding: 24 }}
            />
          )}
          {loading && <div>Loading events...</div>}
          {chatOpen && <ChatBot accessToken={accessToken} onClose={() => setChatOpen(false)} />}
        </>
      )}
    </div>
  )
}

export default App
