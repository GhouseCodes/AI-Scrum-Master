import React from 'react';
import Dashboard from './components/Dashboard';
import SprintBoard from './components/SprintBoard';
import Backlog from './components/Backlog';
import Analytics from './components/Analytics';
import Retrospective from './components/Retrospective';
import VoiceInput from './components/VoiceInput';
import './styles/main.css';

function App() {
  const [currentSection, setCurrentSection] = React.useState('dashboard');

  const renderSection = () => {
    switch (currentSection) {
      case 'dashboard':
        return <Dashboard />;
      case 'sprint':
        return <SprintBoard />;
      case 'backlog':
        return <Backlog />;
      case 'analytics':
        return <Analytics />;
      case 'retro':
        return <Retrospective />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <i className="fas fa-robot"></i>
            <h1>AI Scrum Master</h1>
          </div>
          <nav>
            <button onClick={() => setCurrentSection('dashboard')}>Dashboard</button>
            <button onClick={() => setCurrentSection('sprint')}>Sprint Board</button>
            <button onClick={() => setCurrentSection('backlog')}>Backlog</button>
            <button onClick={() => setCurrentSection('analytics')}>Analytics</button>
            <button onClick={() => setCurrentSection('retro')}>Retro</button>
          </nav>
        </div>
      </header>
      <main className="main-content">
        {renderSection()}
      </main>
      <VoiceInput />
    </div>
  );
}

export default App;
