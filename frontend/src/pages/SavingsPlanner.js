import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Disclaimer from '../components/Disclaimer';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const SavingsPlanner = () => {
  const navigate = useNavigate();
  const [savingsPlan, setSavingsPlan] = useState(null);
  const [goal, setGoal] = useState({ amount: 1000, deadline_days: 90 });
  const [loading, setLoading] = useState(false);
  const user = JSON.parse(localStorage.getItem('eefai_user') || '{}');
  const userId = user.email || 'guest';

  useEffect(() => {
    if (userId !== 'guest') {
      generatePlan();
    }
  }, []);

  const generatePlan = async () => {
    setLoading(true);
    try {
      const stateRes = await axios.get(`${API_URL}/api/eefai/${userId}/state`);
      const profile = stateRes.data.profile || {};

      const planRes = await axios.post(`${API_URL}/api/cfp/simulate`, {
        user_id: userId,
        scenario: {
          balances: profile.debts || [],
          income: profile.income || 0,
          expenses: profile.expenses || 0,
          goal: { type: 'emergency', amount: goal.amount, deadline_days: goal.deadline_days }
        },
        trace_id: `savings_plan_${Date.now()}`
      });

      setSavingsPlan(planRes.data);
    } catch (error) {
      console.error('Plan generation error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGoalChange = (field, value) => {
    setGoal({ ...goal, [field]: parseInt(value) || 0 });
  };

  return (
    <div className="min-h-screen bg-neutral-50 p-6">
      <div className="max-w-4xl mx-auto">
        <button onClick={() => navigate('/dashboard')} className="mb-4 text-primary-600 hover:text-primary-700 font-medium">
          ← Back to Dashboard
        </button>
        
        <h1 className="text-3xl font-bold mb-4">Emergency Savings Planner (CFP-AI)</h1>
        <Disclaimer page="general" />

        <div className="bg-white rounded-lg p-6 mb-6 border">
          <h2 className="text-xl font-semibold mb-4">Set Your Goal</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2">Goal Amount</label>
              <div className="relative">
                <span className="absolute left-4 top-3 text-neutral-500">$</span>
                <input
                  type="number"
                  value={goal.amount}
                  onChange={(e) => handleGoalChange('amount', e.target.value)}
                  className="w-full pl-8 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-neutral-700 mb-2">Deadline (days)</label>
              <input
                type="number"
                value={goal.deadline_days}
                onChange={(e) => handleGoalChange('deadline_days', e.target.value)}
                className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
          <button
            onClick={generatePlan}
            disabled={loading}
            className="mt-4 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium disabled:opacity-50"
          >
            {loading ? 'Generating Plan...' : 'Generate Savings Plan'}
          </button>
        </div>

        {savingsPlan && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg p-6 border">
              <h2 className="text-xl font-semibold mb-4">Your Personalized Plan</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="text-center p-4 bg-primary-50 rounded-lg">
                  <div className="text-3xl font-bold text-primary-600 font-mono">${savingsPlan.calculations.monthly_surplus}</div>
                  <div className="text-sm text-neutral-600 mt-1">Monthly Surplus</div>
                </div>
                <div className="text-center p-4 bg-secondary-50 rounded-lg">
                  <div className="text-3xl font-bold text-secondary-600 font-mono">{savingsPlan.calculations.savings_plan?.length || 0}</div>
                  <div className="text-sm text-neutral-600 mt-1">Weeks to Goal</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-3xl font-bold text-green-600 font-mono">${goal.amount}</div>
                  <div className="text-sm text-neutral-600 mt-1">Target Amount</div>
                </div>
              </div>

              <h3 className="font-semibold mb-3">Weekly Savings Schedule (CFP-AI Calculated)</h3>
              <div className="max-h-96 overflow-y-auto">
                <table className="w-full">
                  <thead className="bg-neutral-50 sticky top-0">
                    <tr>
                      <th className="px-4 py-2 text-left text-sm font-medium text-neutral-600">Week</th>
                      <th className="px-4 py-2 text-left text-sm font-medium text-neutral-600">Date</th>
                      <th className="px-4 py-2 text-right text-sm font-medium text-neutral-600">Amount</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-neutral-200">
                    {savingsPlan.calculations.savings_plan?.map((entry, idx) => (
                      <tr key={idx} className="hover:bg-neutral-50">
                        <td className="px-4 py-2 text-sm">Week {idx + 1}</td>
                        <td className="px-4 py-2 text-sm">{entry.date}</td>
                        <td className="px-4 py-2 text-sm text-right font-mono">${entry.amount.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
              <h3 className="font-semibold text-blue-900 mb-2">CFP-AI Assumptions</h3>
              <ul className="space-y-1 text-sm text-blue-800">
                {savingsPlan.assumptions?.map((assumption, idx) => (
                  <li key={idx}>• {assumption}</li>
                ))}
              </ul>
              <div className="mt-4 text-xs text-blue-600 font-mono">
                Checksum: {savingsPlan.checksum?.substring(0, 16)}... (Verified by CFP-AI)
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SavingsPlanner;
