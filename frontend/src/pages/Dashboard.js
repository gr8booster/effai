import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Dashboard = () => {
  const navigate = useNavigate();
  const [userData, setUserData] = useState(null);
  const [financialPlan, setFinancialPlan] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Get user from localStorage
  const user = JSON.parse(localStorage.getItem('eefai_user') || '{}');
  const userId = user.email || 'test_user_001';

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Load EEFai state
      const stateRes = await axios.get(`${API_URL}/api/eefai/${userId}/state`);
      setUserData(stateRes.data);
      
      // Load financial plan from CFP-AI
      const planRes = await axios.post(`${API_URL}/api/cfp/simulate`, {
        user_id: userId,
        scenario: {
          balances: stateRes.data.profile?.debts || [],
          income: stateRes.data.profile?.income || 0,
          expenses: stateRes.data.profile?.expenses || 0,
          goal: {
            type: 'emergency',
            amount: 1000,
            deadline_days: 90
          }
        },
        trace_id: `dashboard_load_${Date.now()}`
      });
      setFinancialPlan(planRes.data);
      
      // Load tasks from MentorAgent
      const tasksRes = await axios.post(`${API_URL}/api/mentor/generate-tasks`, {
        user_id: userId,
        plan_id: stateRes.data.current_plan_id || 'default_plan',
        milestone_id: 'emergency_fund_start',
        trace_id: `tasks_load_${Date.now()}`
      });
      setTasks(tasksRes.data.tasks || []);
      
    } catch (err) {
      console.error('Dashboard load error:', err);
      setError(err.message);
      // Fallback to localStorage data if API fails
      if (user.income) {
        setUserData({ profile: user });
        setFinancialPlan({
          calculations: {
            monthly_surplus: user.income - user.expenses
          }
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleTaskComplete = async (taskId) => {
    try {
      await axios.post(`${API_URL}/api/mentor/tasks/${taskId}/complete`, null, {
        params: { user_id: userId }
      });
      // Refresh tasks
      setTasks(tasks.map(t => t.task_id === taskId ? {...t, completed: true} : t));
    } catch (err) {
      console.error('Task completion error:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-primary-200 border-t-primary-600 mb-4"></div>
          <p className="text-neutral-600">Loading your financial dashboard...</p>
        </div>
      </div>
    );
  }

  if (error && !userData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-neutral-50">
        <div className="text-center max-w-md">
          <h2 className="text-xl font-semibold text-neutral-900 mb-2">Unable to load dashboard</h2>
          <p className="text-neutral-600 mb-4">{error}</p>
          <button
            onClick={loadDashboardData}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const profile = userData?.profile || user;
  const monthlySurplus = financialPlan?.calculations?.monthly_surplus || (profile.income - profile.expenses);
  const currentSavings = profile.savings || 0;
  const emergencyGoal = 1000;
  const savingsProgress = (currentSavings / emergencyGoal) * 100;
  const activeDebts = profile.debts?.length || 0;
  const totalDebt = profile.debts?.reduce((sum, d) => sum + (d.balance || 0), 0) || 0;

  return (
    <div className="min-h-screen bg-neutral-50">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-primary-600">EEFai</h1>
            <nav className="flex gap-4">
              <button onClick={() => navigate('/upload')} className="text-neutral-600 hover:text-primary-600 text-sm" data-testid="nav-upload">
                Upload
              </button>
              <button onClick={() => navigate('/letters')} className="text-neutral-600 hover:text-primary-600 text-sm" data-testid="nav-letters">
                Letters
              </button>
              <button onClick={() => navigate('/learning')} className="text-neutral-600 hover:text-primary-600 text-sm" data-testid="nav-learning">
                Learning
              </button>
              <button onClick={() => navigate('/credit')} className="text-neutral-600 hover:text-primary-600 text-sm" data-testid="nav-credit">
                Credit
              </button>
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Welcome */}
        <div className="bg-gradient-to-r from-primary-50 to-secondary-50 rounded-lg p-6 mb-6 border border-primary-200">
          <h2 className="text-xl font-semibold text-primary-900 mb-2">Welcome Back, {profile.name || 'Friend'}!</h2>
          <p className="text-primary-800">EEFai is here to help you build financial stability.</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {/* Emergency Fund */}
          <div className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200" data-testid="widget-emergency-fund">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Emergency Fund</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">${currentSavings}</div>
            <div className="mt-2 text-sm text-neutral-500">Goal: ${emergencyGoal}</div>
            <div className="mt-3 w-full h-2 bg-neutral-200 rounded-full overflow-hidden">
              <div 
                className="h-2 bg-secondary-500 rounded-full transition-all duration-500"
                style={{width: `${Math.min(savingsProgress, 100)}%`}}
              />
            </div>
            <div className="mt-2 text-xs text-secondary-600">{Math.round(savingsProgress)}% complete</div>
          </div>

          {/* Monthly Surplus */}
          <div className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200" data-testid="widget-surplus">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Monthly Surplus</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">${monthlySurplus}</div>
            <div className="mt-2 text-sm text-secondary-600">Available for savings/debt</div>
            <div className="mt-3 text-xs text-neutral-500">
              Income: ${profile.income} - Expenses: ${profile.expenses}
            </div>
          </div>

          {/* Active Debts */}
          <div className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200" data-testid="widget-debts">
            <h3 className="text-sm font-medium text-neutral-600 mb-2">Active Debts</h3>
            <div className="text-3xl font-bold text-neutral-900 font-mono">{activeDebts}</div>
            <div className="mt-2 text-sm text-neutral-500">Total: ${totalDebt.toFixed(2)}</div>
            {activeDebts > 0 && (
              <button className="mt-3 text-xs text-primary-600 hover:text-primary-700 font-medium">
                View payoff plan →
              </button>
            )}
          </div>
        </div>

        {/* Daily Tasks */}
        <div className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200 mb-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-neutral-900">Today's Tasks</h2>
            <span className="text-sm text-neutral-500">{tasks.filter(t => !t.completed).length} remaining</span>
          </div>
          
          {tasks.length === 0 ? (
            <div className="text-center py-8 text-neutral-500">
              <p>Loading tasks...</p>
            </div>
          ) : (
            <div className="space-y-3">
              {tasks.map(task => (
                <div key={task.task_id} className="flex items-start gap-3 p-4 bg-neutral-50 rounded-lg hover:bg-neutral-100 transition-colors">
                  <input 
                    type="checkbox" 
                    checked={task.status === 'completed'}
                    onChange={() => handleTaskComplete(task.task_id)}
                    className="mt-1 w-5 h-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500"
                    data-testid={`task-checkbox-${task.task_id}`}
                  />
                  <div className="flex-1">
                    <div className="font-medium text-neutral-900">{task.description}</div>
                    <div className="text-sm text-neutral-500 mt-1">
                      <span className="inline-flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {task.time_est_min} minutes
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            onClick={() => navigate('/upload')}
            className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200 hover:border-primary-300 hover:shadow-md transition-all text-left group"
            data-testid="action-upload"
          >
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-200 transition-colors">
                <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Upload Debt Letter</h3>
                <p className="text-neutral-600 text-sm">Get instant FDCPA analysis and response drafts</p>
              </div>
            </div>
          </button>

          <button
            onClick={() => navigate('/letters')}
            className="bg-white rounded-lg p-6 shadow-sm border border-neutral-200 hover:border-primary-300 hover:shadow-md transition-all text-left group"
            data-testid="action-letters"
          >
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center group-hover:bg-secondary-200 transition-colors">
                <svg className="w-6 h-6 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-neutral-900 mb-1">Generate Letter</h3>
                <p className="text-neutral-600 text-sm">Create debt validation or dispute letters</p>
              </div>
            </div>
          </button>
        </div>

        {/* Data Source Indicator */}
        <div className="mt-6 text-center">
          <p className="text-xs text-neutral-400">
            Data powered by EEFai's 9 AI agents • Last updated: {new Date().toLocaleTimeString()}
          </p>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
