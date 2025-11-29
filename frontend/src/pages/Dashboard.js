import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Dashboard = () => {
  const navigate = useNavigate();
  const [eefaiState, setEefaiState] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const userId = 'test_user_001'; // In production, get from auth

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const stateRes = await axios.get(`${API_URL}/api/eefai/${userId}/state`);
      setEefaiState(stateRes.data);
      
      // Simulate tasks - in production, get from backend
      setTasks([
        { id: 1, title: 'Set up emergency savings account', completed: false, time: 10 },
        { id: 2, title: 'Review collection letter', completed: false, time: 5 },
        { id: 3, title: 'Calculate monthly surplus', completed: true, time: 5 }
      ]);
    } catch (error) {
      console.error('Dashboard load error:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-neutral-600">Loading your dashboard...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-primary-600">EEFai Dashboard</h1>
            <nav className="flex gap-4">
              <button onClick={() => navigate('/upload')} className="text-neutral-600 hover:text-primary-600" data-testid="nav-upload">
                Upload Documents
              </button>
              <button onClick={() => navigate('/letters')} className="text-neutral-600 hover:text-primary-600" data-testid="nav-letters">
                Letters
              </button>
              <button onClick={() => navigate('/learning')} className="text-neutral-600 hover:text-primary-600" data-testid="nav-learning">
                Learning
              </button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Message */}
        <div className="bg-primary-50 rounded-lg p-6 mb-8 border border-primary-200">
          <h2 className="text-xl font-semibold text-primary-900 mb-2">Welcome Back!</h2>
          <p className="text-primary-800">EEFai is here to help you take control of your finances.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Emergency Fund</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">$500</div>
            <div className="mt-2 text-sm text-neutral-500">Goal: $1,000</div>
            <div className="mt-3 w-full h-2 bg-neutral-200 rounded-full">
              <div className="h-2 bg-secondary-500 rounded-full" style={{width: '50%'}} />
            </div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Monthly Surplus</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">$800</div>
            <div className="mt-2 text-sm text-secondary-600">Available for savings/debt</div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Active Debts</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">2</div>
            <div className="mt-2 text-sm text-neutral-500">Total: $3,000</div>
          </div>
        </div>

        {/* Daily Tasks */}
        <div className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200 mb-8">
          <h2 className="text-xl font-semibold text-neutral-900 mb-4">Today's Tasks</h2>
          <div className="space-y-3">
            {tasks.map(task => (
              <div key={task.id} className="flex items-center gap-3 p-4 bg-neutral-50 rounded-lg">
                <input 
                  type="checkbox" 
                  checked={task.completed}
                  onChange={() => {}}
                  className="w-5 h-5"
                  data-testid={`task-checkbox-${task.id}`}
                />
                <div className="flex-1">
                  <div className="font-medium text-neutral-900">{task.title}</div>
                  <div className="text-sm text-neutral-500">{task.time} minutes</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <button
            onClick={() => navigate('/upload')}
            className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200 hover:border-primary-300 transition-colors text-left"
            data-testid="action-upload"
          >
            <h3 className="text-lg font-semibold text-neutral-900 mb-2">Upload Debt Letter</h3>
            <p className="text-neutral-600">Get instant analysis and response drafts</p>
          </button>

          <button
            onClick={() => navigate('/letters')}
            className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200 hover:border-primary-300 transition-colors text-left"
            data-testid="action-letters"
          >
            <h3 className="text-lg font-semibold text-neutral-900 mb-2">Generate Letter</h3>
            <p className="text-neutral-600">Create debt validation or dispute letters</p>
          </button>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
