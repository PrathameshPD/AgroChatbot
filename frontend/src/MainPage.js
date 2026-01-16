import React, { useState } from 'react';
import './App.css';

// Simple Link Renderer to handle [text](url) without external dependencies
const LinkRenderer = ({ text }) => {
  const parts = text.split(/(\[.*?\]\(.*?\))/g);
  return (
    <div>
      {parts.map((part, i) => {
        const match = part.match(/\[(.*?)\]\((.*?)\)/);
        if (match) {
          return (
            <a key={i} href={match[2]} target="_blank" rel="noopener noreferrer" style={{ color: '#2E7D32', fontWeight: 'bold' }}>
              {match[1]}
            </a>
          );
        }
        return <span key={i}>{part}</span>;
      })}
    </div>
  );
};

const MainPage = ({
  chatOpen,
  handleChatToggle,
  messages,
  input,
  setInput,
  handleSendMessage,
  isLoading,
}) => {
  return (
    <div className="App">
      <div className="hero-section">
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <h1>Welcome to AgroVerse</h1>
          <p>
            As we all know, farmers are the backbone of agriculture in any country.
            Hence, we provide favorable aspects to support them through technology.
          </p>
        </div>
      </div>

      <div className="chat-toggle notranslate" onClick={handleChatToggle} role="button" aria-label="Toggle chat">
        💬
      </div>

      {chatOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <h2>AgroBot</h2>
            <button onClick={handleChatToggle} className="close-chat-btn notranslate">×</button>
          </div>

          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.sender === 'bot' ? (
                  <LinkRenderer text={msg.text} />
                ) : (
                  <div>{msg.text}</div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="message bot loading">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            )}
          </div>

          <div className="chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Type a message..."
              disabled={isLoading}
            />
            <button className="send-btn" onClick={handleSendMessage} disabled={isLoading}>
              {isLoading ? '...' : 'Send'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MainPage;