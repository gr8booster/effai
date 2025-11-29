import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Disclaimer from '../components/Disclaimer';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Dashboard = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [financialPlan, setFinancialPlan] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const user = JSON.parse(localStorage.getItem('eefai_user') || '{}');
  const userId = user.email || 'guest';

  useEffect(() => {
    if (userId === 'guest') {
      navigate('/login');
      return;
    }
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Load EEFai state
      const stateRes = await axios.get(`${API_URL}/api/eefai/${userId}/state`);
      setUserData(stateRes.data);
      
      // Load financial plan
      const planRes = await axios.post(`${API_URL}/api/cfp/simulate`, {
        user_id: userId,
        scenario: {
          balances: stateRes.data.profile?.debts || [],
          income: stateRes.data.profile?.income || 0,
          expenses: stateRes.data.profile?.expenses || 0,
          goal: { type: 'emergency', amount: 1000, deadline_days: 90 }
        },
        trace_id: `dashboard_${Date.now()}`
      });
      setFinancialPlan(planRes.data);
      
      // Load REAL active tasks from backend
      const tasksRes = await axios.get(`${API_URL}/api/mentor/tasks/active?user_id=${userId}`);
      setTasks(tasksRes.data.tasks || []);
      
    } catch (err) {
      console.error('Dashboard error:', err);
      setError(err.message);
      setUserData({ profile: user });
      setFinancialPlan({ calculations: { monthly_surplus: (user.income || 0) - (user.expenses || 0) } });
    } finally {
      setLoading(false);
    }
  };

  const handleTaskComplete = async (taskId) => {
    try {
      await axios.post(`${API_URL}/api/mentor/tasks/${taskId}/complete?user_id=${userId}`);
      await loadDashboardData();
    } catch (err) {
      console.error('Task error:', err);
      alert('Failed to complete task');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary-200 border-t-primary-600 mb-4"></div>
          <p className="text-neutral-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const profile = userData?.profile || user;
  const monthlySurplus = financialPlan?.calculations?.monthly_surplus || ((profile.income || 0) - (profile.expenses || 0));
  const currentSavings = profile.savings || 0;
  const emergencyGoal = 1000;
  const savingsProgress = Math.min((currentSavings / emergencyGoal) * 100, 100);
  const activeDebts = (profile.debts || []).length;
  const totalDebt = (profile.debts || []).reduce((sum, d) => sum + (d.balance || 0), 0);

  return (
    <div className="min-h-screen bg-neutral-50">
      <header className="bg-white border-b border-neutral-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-primary-600">EEFai</h1>
            <nav className="flex gap-4">
              <button onClick={() => navigate('/dashboard')} className="text-neutral-600 hover:text-primary-600 text-sm font-medium">Dashboard</button>
              <button onClick={() => navigate('/savings-planner')} className="text-neutral-600 hover:text-primary-600 text-sm font-medium">Savings</button>
              <button onClick={() => navigate('/letters')} className="text-neutral-600 hover:text-primary-600 text-sm font-medium">Letters</button>
              <button onClick={() => navigate('/dispute-manager')} className="text-neutral-600 hover:text-primary-600 text-sm font-medium">Disputes</button>
              <button onClick={() => navigate('/credit')} className="text-neutral-600 hover:text-primary-600 text-sm font-medium">Credit</button>
              <button onClick={() => navigate('/learning')} className="text-neutral-600 hover:text-primary-600 text-sm font-medium">Learning</button>
              <button onClick={() => navigate('/upload')} className="text-neutral-600 hover:text-primary-600 text-sm font-medium">Upload</button>
              <button onClick={() => navigate('/admin')} className="text-neutral-600 hover:text-primary-600 text-sm font-medium">Admin</button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Disclaimer page="general" />
        
        <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg p-6 mb-6 border border-primary-200">
          <h2 className="text-xl font-semibold text-primary-900 mb-2">Welcome Back, {profile.name || 'Friend'}!</h2>
          <p className="text-primary-800">Your personalized financial plan powered by 9 AI agents.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-lg p-6 shadow-sm border">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Emergency Fund</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">${currentSavings}</div>
            <div className="mt-2 text-sm text-neutral-500">Goal: ${emergencyGoal}</div>
            <div className="mt-3 w-full h-2 bg-neutral-200 rounded-full">
              <div className="h-2 bg-secondary-500 rounded-full" style={{width: `${savingsProgress}%`}} />
            </div>
            <div className="mt-2 text-xs text-secondary-600">{Math.round(savingsProgress)}% complete</div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Monthly Surplus</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">${monthlySurplus}</div>
            <div className="mt-2 text-sm text-secondary-600">Available for goals</div>
            <div className="mt-3 text-xs text-neutral-500">Income ${profile.income || 0} - Expenses ${profile.expenses || 0}</div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-sm border">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Active Debts</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">{activeDebts}</div>
            <div className="mt-2 text-sm text-neutral-500">Total: ${totalDebt.toFixed(2)}</div>
          </div>
        </div>

        <div className="bg-white rounded-lg p-6 shadow-sm border mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-neutral-900">Your Tasks (Powered by MentorAgent)</h2>
            <span className="text-sm text-neutral-500">{tasks.filter(t => t.status !== 'completed').length} active</span>
          </div>
          
          {tasks.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-neutral-500 mb-4">No active tasks. Great job staying on top of things!</p>
              <button 
                onClick={async () => {
                  await axios.post(`${API_URL}/api/mentor/generate-tasks`, {
                    user_id: userId,
                    plan_id: 'default',
                    milestone_id: 'emergency_fund_start',
                    trace_id: `gen_${Date.now()}`
                  });
                  await loadDashboardData();
                }}
                className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                Generate New Tasks
              </button>
            </div>
          ) : (
            <div className="space-y-3">
              {tasks.map(task => (
                <div key={task.task_id} className="flex items-start gap-3 p-4 bg-neutral-50 rounded-lg hover:bg-neutral-100 transition-colors">
                  <input 
                    type="checkbox" 
                    checked={task.status === 'completed'}
                    onChange={() => handleTaskComplete(task.task_id)}
                    className="mt-1 w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500 cursor-pointer"
                  />
                  <div className="flex-1">
                    <div className="font-medium text-neutral-900">{task.description}</div>
                    <div className="text-sm text-neutral-500 mt-1 flex items-center gap-1">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {task.time_est_min} min
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button onClick={() => navigate('/savings-planner')} className="bg-white rounded-lg p-6 shadow-sm border hover:border-primary-300 hover:shadow-md transition-all text-left group">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center group-hover:bg-secondary-200">
                <span className="text-2xl">💰</span>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Emergency Savings Planner</h3>
                <p className="text-neutral-600 text-sm">CFP-AI generates weekly savings schedule</p>
              </div>
            </div>
          </button>

          <button onClick={() => navigate('/dispute-manager')} className="bg-white rounded-lg p-6 shadow-sm border hover:border-primary-300 hover:shadow-md transition-all text-left group">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center group-hover:bg-blue-200">
                <span className="text-2xl">⚖️</span>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Credit Dispute Manager</h3>
                <p className="text-neutral-600 text-sm">FCRA-compliant dispute letters</p>
              </div>
            </div>
          </button>

          <button onClick={() => navigate('/upload')} className="bg-white rounded-lg p-6 shadow-sm border hover:border-primary-300 hover:shadow-md transition-all text-left group">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-200">
                <span className="text-2xl">📄</span>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Upload Debt Letter</h3>
                <p className="text-neutral-600 text-sm">AI OCR analysis via IntakeAgent</p>
              </div>
            </div>
          </button>

          <button onClick={() => navigate('/letters')} className="bg-white rounded-lg p-6 shadow-sm border hover:border-primary-300 hover:shadow-md transition-all text-left group">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center group-hover:bg-green-200">
                <span className="text-2xl">✍️</span>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Generate Letters</h3>
                <p className="text-neutral-600 text-sm">4 templates via WriterAgent with PDF</p>
              </div>
            </div>
          </button>

          <button onClick={() => navigate('/credit')} className="bg-white rounded-lg p-6 shadow-sm border hover:border-primary-300 hover:shadow-md transition-all text-left group">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center group-hover:bg-purple-200">
                <span className="text-2xl">📊</span>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Credit Improvement</h3>
                <p className="text-neutral-600 text-sm">AI-powered score estimation & tips</p>
              </div>
            </div>
          </button>

          <button onClick={() => navigate('/learning')} className="bg-white rounded-lg p-6 shadow-sm border hover:border-primary-300 hover:shadow-md transition-all text-left group">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center group-hover:bg-yellow-200">
                <span className="text-2xl">📚</span>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Learning Center</h3>
                <p className="text-neutral-600 text-sm">70 financial lessons by MentorAgent</p>
              </div>
            </div>
          </button>

          <button onClick={() => navigate('/admin')} className="bg-white rounded-lg p-6 shadow-sm border border-red-200 hover:border-red-400 hover:shadow-md transition-all text-left group">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center group-hover:bg-red-200">
                <span className="text-2xl">🔧</span>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Admin Console</h3>
                <p className="text-neutral-600 text-sm">System stats, review queue, audit logs</p>
              </div>
            </div>
          </button>

          <div className="bg-gradient-to-br from-primary-50 to-secondary-50 rounded-lg p-6 border-2 border-primary-200">
            <h3 className="font-semibold text-primary-900 mb-2">✨ New Features Added</h3>
            <ul className="space-y-1 text-sm text-primary-800">
              <li>• 70-lesson learning library (was 2)</li>
              <li>• AI-powered task generation (personalized)</li>
              <li>• Savings planner with weekly schedules</li>
              <li>• Credit dispute workflow</li>
              <li>• Admin analytics dashboard</li>
              <li>• Event-driven architecture</li>
              <li>• Performance caching (Redis)</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
