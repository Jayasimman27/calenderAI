import React from 'react'

function LoginPage({ onLogin }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', background: '#f5f7fa' }}>
      <h1 style={{ marginBottom: 24, color: '#1976d2' }}>Welcome to TailorTalk Calendar</h1>
      <div style={{ background: '#fff', padding: 32, borderRadius: 12, boxShadow: '0 2px 16px rgba(0,0,0,0.08)' }}>
        <button
          onClick={onLogin}
          style={{
            background: '#1976d2', color: '#fff', border: 'none', borderRadius: 8, padding: '12px 32px', fontSize: 18, fontWeight: 'bold', cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.08)'
          }}
        >
          Sign in with Google
        </button>
      </div>
    </div>
  )
}

export default LoginPage 