import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ErrorBoundary from './components/ErrorBoundary';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard';
import DocumentUpload from './pages/DocumentUpload';
import LetterBuilder from './pages/LetterBuilder';
import MicroLearning from './pages/MicroLearning';
import AdminConsole from './pages/AdminConsole';
import CreditImprovement from './pages/CreditImprovement';
import Login from './pages/Login';
import SavingsPlanner from './pages/SavingsPlanner';
import DisputeManager from './pages/DisputeManager';
import './App.css';

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen bg-neutral-50">
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/onboarding" element={<Onboarding />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/upload" element={<DocumentUpload />} />
            <Route path="/letters" element={<LetterBuilder />} />
            <Route path="/learning" element={<MicroLearning />} />
            <Route path="/admin" element={<AdminConsole />} />
            <Route path="/credit" element={<CreditImprovement />} />
            <Route path="/savings-planner" element={<SavingsPlanner />} />
            <Route path="/dispute-manager" element={<DisputeManager />} />
          </Routes>
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
