import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard';
import DocumentUpload from './pages/DocumentUpload';
import LetterBuilder from './pages/LetterBuilder';
import MicroLearning from './pages/MicroLearning';
import AdminConsole from './pages/AdminConsole';
import CreditImprovement from './pages/CreditImprovement';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-neutral-50">
        <Routes>
          <Route path="/" element={<Navigate to="/onboarding" replace />} />
          <Route path="/onboarding" element={<Onboarding />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<DocumentUpload />} />
          <Route path="/letters" element={<LetterBuilder />} />
          <Route path="/learning" element={<MicroLearning />} />
          <Route path="/admin" element={<AdminConsole />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
