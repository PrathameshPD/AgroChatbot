import React from 'react';
import './App.css';

const Header = () => {
  return (
    <header className="App-header">
      <div className="logo">AgroVerse</div>
      <div className="language-selector-container">
        <div id="google_translate_element"></div>
      </div>
    </header>
  );
};

export default Header;
