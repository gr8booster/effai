import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const AGENTS = [
  { name: 'OrchestratorAI', desc: 'Coordinating your plan', icon: '🎯' },
  { name: 'EEFai', desc: 'Analyzing your situation', icon: '🤝' },
  { name: 'LegalAI', desc: 'Checking debt rights', icon: '⚖️' },
  { name: 'CFP-AI', desc: 'Calculating finances', icon: '💰' },
  { name: 'WriterAgent', desc: 'Preparing templates', icon: '✍️' },
  { name: 'IntakeAgent', desc: 'Processing documents', icon: '📄' },
  { name: 'MentorAgent', desc: 'Creating daily tasks', icon: '📚' },
  { name: 'SupportAgent', desc: 'Ready to help', icon: '💬' },
  { name: 'AuditAgent', desc: 'Securing your data', icon: '🔒' }
];

const Onboarding = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    state: '',
    income: '',
    expenses: '',
    savings: ''
  });
  const [loading, setLoading] = useState(false);
  const [agentProgress, setAgentProgress] = useState([]);
  const [analyzing, setAnalyzing] = useState(false);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateStep = () => {
    if (step === 1) {
      return formData.name && formData.email && formData.phone && formData.state;
    }
    if (step === 2) {
      return formData.income && formData.expenses;
    }
    if (step === 3) {
      const consent1 = document.getElementById('consent1')?.checked;
      const consent2 = document.getElementById('consent2')?.checked;
      const consent3 = document.getElementById('consent3')?.checked;
      return consent1 && consent2 && consent3;
    }
    return true;
  };

  const handleNext = () => {
    if (!validateStep()) {
      alert('Please fill in all required fields');
      return;
    }
    if (step < 4) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const simulateAgentWork = async () => {
    setAnalyzing(true);
    
    for (let i = 0; i < AGENTS.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 400));
      setAgentProgress(prev => [...prev, i]);
    }
  };

  const handleSubmit = async () => {
    if (!validateStep()) {
      alert('Please accept all consent terms');
      return;
    }
    
    setLoading(true);
    
    // Show 9 agents working
    await simulateAgentWork();
    
    try {
      // Create EEFai instance with full profile
      await axios.post(`${API_URL}/api/eefai/create?user_id=${formData.email}`);
      
      // Generate initial financial plan via CFP-AI
      const planResponse = await axios.post(`${API_URL}/api/cfp/simulate`, {
        user_id: formData.email,
        scenario: {
          balances: [],
          income: parseFloat(formData.income),
          expenses: parseFloat(formData.expenses),
          goal: {
            type: 'emergency',
            amount: 1000,
            deadline_days: 90
          }
        },
        trace_id: `onboard_${Date.now()}`
      });
      
      // Generate initial tasks via MentorAgent
      await axios.post(`${API_URL}/api/mentor/generate-tasks`, {
        user_id: formData.email,
        plan_id: 'initial_plan',
        milestone_id: 'emergency_fund_start',
        trace_id: `onboard_tasks_${Date.now()}`
      });
      
      // Send profile message to EEFai
      await axios.post(`${API_URL}/api/eefai/${formData.email}/message`, {
        user_id: formData.email,
        message: `Profile: ${formData.name}, ${formData.state}. Income: $${formData.income}, Expenses: $${formData.expenses}, Savings: $${formData.savings}`,
        trace_id: `profile_${Date.now()}`,
        attachments: []
      });
      
      // Store form data in localStorage for dashboard access
      localStorage.setItem('eefai_user', JSON.stringify({
        email: formData.email,
        name: formData.name,
        state: formData.state,
        income: formData.income,
        expenses: formData.expenses,
        savings: formData.savings,
        onboarded: true,
        onboarded_at: new Date().toISOString()
      }));
      
      navigate('/dashboard');
    } catch (error) {
      console.error('Onboarding error:', error);
      alert('Error during setup. Please try again.');
      setLoading(false);
      setAnalyzing(false);
      setAgentProgress([]);
    }
  };

  const renderStep = () => {
    switch(step) {
      case 1:
        return (
          <div className="space-y-4" data-testid="onboarding-step-1">
            <h2 className="text-2xl sm:text-3xl font-semibold text-neutral-900 font-heading">Welcome to EEFai</h2>
            <p className="text-neutral-600 text-sm sm:text-base">Let's get started by learning a bit about you.</p>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Full Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 sm:px-4 sm:py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="John Doe"
                  data-testid="input-name"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Email *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 sm:px-4 sm:py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="john@example.com"
                  data-testid="input-email"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Phone Number *
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 sm:px-4 sm:py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="(555) 123-4567"
                  data-testid="input-phone"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  State *
                </label>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 sm:px-4 sm:py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  data-testid="select-state"
                  required
                >
                  <option value="">Select your state</option>
                  <option value="AL">Alabama</option>
                  <option value="CA">California</option>
                  <option value="FL">Florida</option>
                  <option value="IL">Illinois</option>
                  <option value="NY">New York</option>
                  <option value="OH">Ohio</option>
                  <option value="TX">Texas</option>
                  <option value="PA">Pennsylvania</option>
                  <option value="GA">Georgia</option>
                  <option value="NC">North Carolina</option>
                  <option value="MI">Michigan</option>
                </select>
              </div>
            </div>
          </div>
        );
      
      case 2:
        return (
          <div className="space-y-4" data-testid="onboarding-step-2">
            <h2 className="text-2xl sm:text-3xl font-semibold text-neutral-900 font-heading">Financial Profile</h2>
            <p className="text-neutral-600 text-sm sm:text-base">Help us understand your financial situation.</p>
            
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Monthly Income *
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-2 sm:left-4 sm:top-3 text-neutral-500">$</span>
                  <input
                    type="number"
                    name="income"
                    value={formData.income}
                    onChange={handleInputChange}
                    className="w-full pl-7 sm:pl-8 pr-3 sm:pr-4 py-2 sm:py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="3000"
                    data-testid="input-income"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Monthly Expenses *
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-2 sm:left-4 sm:top-3 text-neutral-500">$</span>
                  <input
                    type="number"
                    name="expenses"
                    value={formData.expenses}
                    onChange={handleInputChange}
                    className="w-full pl-7 sm:pl-8 pr-3 sm:pr-4 py-2 sm:py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="2200"
                    data-testid="input-expenses"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-1">
                  Current Savings
                </label>
                <div className="relative">
                  <span className="absolute left-3 top-2 sm:left-4 sm:top-3 text-neutral-500">$</span>
                  <input
                    type="number"
                    name="savings"
                    value={formData.savings}
                    onChange={handleInputChange}
                    className="w-full pl-7 sm:pl-8 pr-3 sm:pr-4 py-2 sm:py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="500"
                    data-testid="input-savings"
                  />
                </div>
              </div>
            </div>
          </div>
        );
      
      case 3:
        return (
          <div className="space-y-4" data-testid="onboarding-step-3">
            <h2 className="text-2xl sm:text-3xl font-semibold text-neutral-900 font-heading">Consent & Disclaimers</h2>
            <p className="text-neutral-600 text-sm sm:text-base">Please review and accept our terms.</p>
            
            <div className="space-y-3 bg-neutral-50 p-4 sm:p-6 rounded-lg border border-neutral-200">
              <div className="space-y-2">
                <div className="flex items-start gap-2">
                  <input type="checkbox" id="consent1" className="mt-1" required data-testid="checkbox-consent-1" />
                  <label htmlFor="consent1" className="text-sm text-neutral-700">
                    I understand that EEFai provides educational information. This is not legal or financial advice.
                  </label>
                </div>
                
                <div className="flex items-start gap-2">
                  <input type="checkbox" id="consent2" className="mt-1" required data-testid="checkbox-consent-2" />
                  <label htmlFor="consent2" className="text-sm text-neutral-700">
                    I consent to EEFai storing my information securely.
                  </label>
                </div>
                
                <div className="flex items-start gap-2">
                  <input type="checkbox" id="consent3" className="mt-1" required data-testid="checkbox-consent-3" />
                  <label htmlFor="consent3" className="text-sm text-neutral-700">
                    I will review all letters before sending.
                  </label>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-neutral-200">
                <h4 className="font-medium text-neutral-900 text-sm mb-1">FDCPA Notice</h4>
                <p className="text-xs text-neutral-600">
                  Under the FDCPA, you have rights. EEFai helps you exercise them.
                </p>
              </div>
            </div>
          </div>
        );
      
      case 4:
        return (
          <div className="space-y-4" data-testid="onboarding-step-4">
            <h2 className="text-2xl sm:text-3xl font-semibold text-neutral-900 font-heading">You're All Set!</h2>
            <p className="text-neutral-600 text-sm sm:text-base">EEFai will create your personalized plan.</p>
            
            <div className="bg-primary-50 p-4 sm:p-6 rounded-lg border border-primary-200">
              <h3 className="font-semibold text-primary-900 mb-2 text-sm sm:text-base">What Happens Next?</h3>
              <ul className="space-y-1.5 text-sm text-primary-800">
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 font-bold">✓</span>
                  <span>EEFai analyzes your financial situation</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 font-bold">✓</span>
                  <span>Personalized emergency fund goal</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 font-bold">✓</span>
                  <span>Daily micro-tasks for better habits</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary-600 font-bold">✓</span>
                  <span>Upload debt letters for analysis</span>
                </li>
              </ul>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  // Agent Analysis Modal
  if (analyzing) {
    return (
      <div className="min-h-screen bg-neutral-900 bg-opacity-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-6 sm:p-8 max-w-md w-full">
          <h2 className="text-2xl font-bold text-center text-neutral-900 mb-6">Creating Your Plan</h2>
          
          <div className="space-y-3 mb-6">
            {AGENTS.map((agent, idx) => (
              <div 
                key={agent.name}
                className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 ${
                  agentProgress.includes(idx) 
                    ? 'bg-primary-50 border-2 border-primary-300' 
                    : 'bg-neutral-50 border border-neutral-200 opacity-50'
                }`}
              >
                <span className="text-2xl">{agent.icon}</span>
                <div className="flex-1">
                  <div className="font-medium text-sm text-neutral-900">{agent.name}</div>
                  <div className="text-xs text-neutral-600">{agent.desc}</div>
                </div>
                {agentProgress.includes(idx) && (
                  <span className="text-primary-600 font-bold text-lg">✓</span>
                )}
              </div>
            ))}
          </div>
          
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-primary-200 border-t-primary-600"></div>
            <p className="mt-4 text-sm text-neutral-600">Analyzing your finances...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50 flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-neutral-200 px-4 py-4 sm:px-6">
        <div className="max-w-2xl mx-auto">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-neutral-500">Step {step} of 4</span>
            <span className="text-sm font-medium text-primary-600">{Math.round((step / 4) * 100)}% Complete</span>
          </div>
          <div className="w-full h-2 bg-neutral-200 rounded-full">
            <div 
              className="h-2 bg-primary-600 rounded-full transition-all duration-300"
              style={{ width: `${(step / 4) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Content - Scrollable */}
      <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-6">
        <div className="max-w-2xl mx-auto">
          <div className="bg-white rounded-xl shadow-sm p-6 sm:p-8">
            {renderStep()}
          </div>
        </div>
      </div>
          
      {/* Buttons - Fixed at bottom with safe area */}
      <div className="bg-white border-t border-neutral-200 px-4 py-4 sm:px-6 pb-20">
        <div className="max-w-2xl mx-auto flex gap-3">
          {step > 1 && (
            <button
              onClick={handleBack}
              type="button"
              className="flex-1 px-6 py-3 border-2 border-neutral-300 text-neutral-700 rounded-lg hover:bg-neutral-50 transition-colors font-medium"
              data-testid="button-back"
            >
              Back
            </button>
          )}
          
          {step < 4 ? (
            <button
              onClick={handleNext}
              type="button"
              className="flex-1 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium shadow-sm"
              data-testid="button-next"
            >
              Continue
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              type="button"
              disabled={loading}
              className="flex-1 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium shadow-sm disabled:opacity-50"
              data-testid="button-submit"
            >
              {loading ? 'Processing...' : 'Get Started'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Onboarding;
