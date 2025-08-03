import { useState, useRef, useEffect } from 'react'

function ChatBot({ accessToken, onClose }) {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! I am your calendar assistant. How can I help you?' }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const chatEndRef = useRef(null)

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isLoading])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return
    const userMessage = input.trim()
    setMessages(prev => [...prev, { sender: 'user', text: userMessage }])
    setInput('')
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:8010/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: userMessage,
          timestamp: new Date().toISOString(),
          access_token: accessToken
        })
      })
      if (response.ok) {
        const data = await response.json()
        setMessages(prev => [...prev, { sender: 'bot', text: data.message }])
      } else {
        setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, I encountered an error. Please try again.' }])
      }
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, I cannot connect to the server. Please check if the backend is running.' }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 2000, pointerEvents: 'none', background: 'rgba(0,0,0,0.18)' }}>
      <div style={{ width: 520, height: 600, background: '#fff', border: '1px solid #ccc', borderRadius: 20, boxShadow: '0 8px 48px rgba(0,0,0,0.22)', zIndex: 2001, display: 'flex', flexDirection: 'column', pointerEvents: 'auto', position: 'relative' }}>
        <div style={{ padding: 22, borderBottom: '1px solid #eee', fontWeight: 'bold', background: '#1976d2', color: '#fff', fontSize: 22, borderTopLeftRadius: 20, borderTopRightRadius: 20, textAlign: 'center', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <span style={{ marginRight: 12, fontSize: 26 }}>🤖</span> Calendar Bot
          <button onClick={onClose} style={{ position: 'absolute', right: 18, top: 18, background: 'transparent', border: 'none', color: '#fff', fontSize: 22, cursor: 'pointer', fontWeight: 'bold' }} title="Close">×</button>
        </div>
        <div style={{ flex: 1, overflowY: 'auto', padding: 24, background: '#fafbfc', fontSize: 16 }}>
          {messages.map((msg, i) => (
            <div key={i} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left', margin: '12px 0' }}>
              <span style={{ display: 'inline-block', background: msg.sender === 'user' ? '#e0f7fa' : '#e8eaf6', color: '#333', borderRadius: 14, padding: '10px 20px', maxWidth: '80%', wordBreak: 'break-word', fontSize: 16 }}>{msg.text}</span>
            </div>
          ))}
          {isLoading && (
            <div style={{ textAlign: 'left', margin: '12px 0' }}>
              <span style={{ display: 'inline-block', background: '#e8eaf6', color: '#333', borderRadius: 14, padding: '10px 20px', fontSize: 16 }}>Thinking...</span>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>
        <div style={{ display: 'flex', borderTop: '1px solid #eee', background: '#f7f7f7', borderBottomLeftRadius: 20, borderBottomRightRadius: 20, padding: 0 }}>
          <input
            style={{ flex: 1, border: 'none', padding: 18, borderRadius: 0, outline: 'none', fontSize: 17, background: 'transparent',color: '#333' }}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') handleSend() }}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <button
            style={{
              border: 'none',
              background: isLoading ? '#ccc' : '#1976d2',
              color: '#fff',
              padding: '0 32px',
              cursor: isLoading ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
              fontSize: 18
            }}
            onClick={handleSend}
            disabled={isLoading}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatBot

/**lets add Notion also to become a one bot that can do anything in the notion would that be possible */