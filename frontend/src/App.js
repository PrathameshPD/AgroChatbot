import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import './App.css';
import MainPage from './MainPage';
import Header from './Header';

function App() {
  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => Math.random().toString(36).substring(7));

  useEffect(() => {
    const googleTranslateElementInit = () => {
      if (window.google && window.google.translate) {
        new window.google.translate.TranslateElement(
          {
            pageLanguage: 'en',
            includedLanguages: 'en,hi,ta,te,kn',
            layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE
          },
          'google_translate_element'
        );
      }
    };

    if (!document.getElementById('google-translate-script')) {
      const script = document.createElement('script');
      script.id = 'google-translate-script';
      script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
      script.async = true;
      document.body.appendChild(script);
      window.googleTranslateElementInit = googleTranslateElementInit;
    } else {
      googleTranslateElementInit();
    }
  }, []);

  const handleChatToggle = () => {
    setChatOpen(!chatOpen);
  };

  const handleSendMessage = async (e) => {
    e?.preventDefault();
    if (input.trim() && !isLoading) {
      const newMessages = [...messages, { text: input, sender: 'user' }];
      setMessages(newMessages);
      setInput('');
      setIsLoading(true);

      try {
        const formData = new FormData();
        formData.append('query', input);
        formData.append('session_id', sessionId);

        const response = await fetch('http://localhost:8000/ask', {
          method: 'POST',
          body: formData,
        });

        const data = await response.json();
        setMessages([...newMessages, { text: data.response, sender: 'bot' }]);
      } catch (error) {
        console.error('Error fetching from backend:', error);
        setMessages([...newMessages, { text: 'Error connecting to the bot.', sender: 'bot' }]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <>
      <Header />
      <Routes>
        <Route
          path="/"
          element={
            <MainPage
              chatOpen={chatOpen}
              handleChatToggle={handleChatToggle}
              messages={messages}
              input={input}
              setInput={setInput}
              handleSendMessage={handleSendMessage}
              isLoading={isLoading}
            />
          }
        />
      </Routes>
    </>
  );
}

export default App;