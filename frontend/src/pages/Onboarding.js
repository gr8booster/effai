import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Onboarding = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    state: '',
    dob: '',
    income: '',
    expenses: '',
    debts: [],
    savings: ''
  });
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleNext = () => {
    if (step < 4) setStep(step + 1);
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Create EEFai instance
      await axios.post(`${API_URL}/api/eefai/create?user_id=${formData.email}`);
      
      // Send initial message to set up profile
      await axios.post(`${API_URL}/api/eefai/${formData.email}/message`, {
        user_id: formData.email,
        message: `Hello! My name is ${formData.name}. I live in ${formData.state}. My monthly income is $${formData.income} and expenses are $${formData.expenses}. I currently have $${formData.savings} in savings.`,
        trace_id: `onboard_${Date.now()}`,
        attachments: []
      });
      
      navigate('/dashboard');
    } catch (error) {
      console.error('Onboarding error:', error);
      alert('Error during onboarding. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    switch(step) {
      case 1:
        return (
          <div className="space-y-6" data-testid="onboarding-step-1">
            <h2 className="text-3xl font-semibold text-neutral-900 font-heading">Welcome to EEFai</h2>
            <p className="text-neutral-600">Let's get started by learning a bit about you.</p>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="John Doe"
                  data-testid="input-name"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Email *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="john@example.com"
                  data-testid="input-email"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Phone Number *
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                  placeholder="(555) 123-4567"
                  data-testid="input-phone"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  State *
                </label>
                <select
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
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
                </select>
              </div>
            </div>
          </div>
        );
      
      case 2:
        return (
          <div className="space-y-6" data-testid="onboarding-step-2">
            <h2 className="text-3xl font-semibold text-neutral-900 font-heading">Financial Profile</h2>
            <p className="text-neutral-600">Help us understand your financial situation.</p>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Monthly Income *
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-3 text-neutral-500">$</span>
                  <input
                    type="number"
                    name="income"
                    value={formData.income}
                    onChange={handleInputChange}
                    className="w-full pl-8 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="3000"
                    data-testid="input-income"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Monthly Expenses *
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-3 text-neutral-500">$</span>
                  <input
                    type="number"
                    name="expenses"
                    value={formData.expenses}
                    onChange={handleInputChange}
                    className="w-full pl-8 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="2200"
                    data-testid="input-expenses"
                    required
                  />
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-neutral-700 mb-2">
                  Current Savings
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-3 text-neutral-500">$</span>
                  <input
                    type="number"
                    name="savings"
                    value={formData.savings}
                    onChange={handleInputChange}
                    className="w-full pl-8 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
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
          <div className="space-y-6" data-testid="onboarding-step-3">
            <h2 className="text-3xl font-semibold text-neutral-900 font-heading">Consent & Disclaimers</h2>
            <p className="text-neutral-600">Please review and accept our terms.</p>
            
            <div className="space-y-4 bg-white p-6 rounded-lg border border-neutral-200">
              <div className="space-y-3">
                <div className="flex items-start">
                  <input type="checkbox" id="consent1" className="mt-1 mr-3" required data-testid="checkbox-consent-1" />
                  <label htmlFor="consent1" className="text-sm text-neutral-700">
                    I understand that EEFai provides educational information and tools to help me manage my finances. 
                    This is not legal or financial advice.
                  </label>
                </div>
                
                <div className="flex items-start">
                  <input type="checkbox" id="consent2" className="mt-1 mr-3" required data-testid="checkbox-consent-2" />
                  <label htmlFor="consent2" className="text-sm text-neutral-700">
                    I consent to EEFai storing my financial information securely to provide personalized guidance.
                  </label>
                </div>
                
                <div className="flex items-start">
                  <input type="checkbox" id="consent3" className="mt-1 mr-3" required data-testid="checkbox-consent-3" />
                  <label htmlFor="consent3" className="text-sm text-neutral-700">
                    I understand that letters generated by EEFai should be reviewed before sending, and I am responsible 
                    for the accuracy of information provided.
                  </label>
                </div>
              </div>
              
              <div className="mt-6 pt-6 border-t border-neutral-200">
                <h3 className="font-medium text-neutral-900 mb-2">FDCPA Notice</h3>
                <p className="text-sm text-neutral-600">
                  Under the Fair Debt Collection Practices Act (FDCPA), you have the right to request validation 
                  of any debt and to dispute inaccurate information. EEFai helps you exercise these rights.
                </p>
              </div>
            </div>
          </div>
        );
      
      case 4:
        return (
          <div className="space-y-6" data-testid="onboarding-step-4">
            <h2 className="text-3xl font-semibold text-neutral-900 font-heading">You're All Set!</h2>
            <p className="text-neutral-600">EEFai will now create your personalized financial plan.</p>
            
            <div className="bg-primary-50 p-6 rounded-lg border border-primary-200">
              <h3 className="font-semibold text-primary-900 mb-3">What Happens Next?</h3>
              <ul className="space-y-2 text-sm text-primary-800">
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>EEFai will analyze your financial situation</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>You'll get a personalized emergency fund goal</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>Daily micro-tasks will help you build better financial habits</span>
                </li>
                <li className="flex items-start">
                  <span className="mr-2">✓</span>
                  <span>You can upload debt letters for instant analysis</span>
                </li>
              </ul>
            </div>
          </div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <div className="bg-white rounded-2xl shadow-lg p-8">
          <div className="mb-8">
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
          
          {renderStep()}
          
          <div className="mt-8 flex gap-4">
            {step > 1 && (
              <button
                onClick={handleBack}
                className="flex-1 px-6 py-3 border-2 border-neutral-300 text-neutral-700 rounded-lg hover:bg-neutral-50 transition-colors"
                data-testid="button-back"
              >
                Back
              </button>
            )}
            
            {step < 4 ? (
              <button
                onClick={handleNext}
                className="flex-1 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                data-testid="button-next"
              >
                Continue
              </button>
            ) : (
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="flex-1 px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50"
                data-testid="button-submit"
              >
                {loading ? 'Setting up...' : 'Get Started'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Onboarding;
