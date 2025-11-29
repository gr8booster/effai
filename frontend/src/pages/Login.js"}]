import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const Login = () => {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const endpoint = isLogin ? 'login' : 'register';
      const params = isLogin 
        ? { email: formData.email, password: formData.password }
        : { email: formData.email, password: formData.password, name: formData.name };

      const response = await axios.post(`${API_URL}/api/auth/${endpoint}`, null, { params });
      
      // Store token and user info
      localStorage.setItem('auth_token', response.data.access_token);
      localStorage.setItem('eefai_user', JSON.stringify({
        email: response.data.email,
        name: response.data.name,
        onboarded: true
      }));

      // Check if user has EEFai instance
      try {
        await axios.get(`${API_URL}/api/eefai/${response.data.email}/state`);
        // Has profile - go to dashboard
        navigate('/dashboard');
      } catch {
        // No profile - need onboarding
        navigate('/onboarding');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed');
      setLoading(false);
    }
  };

  return (
    <div className=\"min-h-screen bg-neutral-50 flex items-center justify-center p-4\">
      <div className=\"max-w-md w-full bg-white rounded-2xl shadow-lg p-8\">
        <div className=\"text-center mb-8\">
          <h1 className=\"text-4xl font-bold text-primary-600 mb-2\">EEFai</h1>
          <p className=\"text-neutral-600\">Your Emergency & Expense Friend</p>
        </div>

        <div className=\"flex gap-2 mb-6\">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-2 rounded-lg font-medium transition-colors ${
              isLogin ? 'bg-primary-600 text-white' : 'bg-neutral-100 text-neutral-600'
            }`}
          >
            Login
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-2 rounded-lg font-medium transition-colors ${
              !isLogin ? 'bg-primary-600 text-white' : 'bg-neutral-100 text-neutral-600'
            }`}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} className=\"space-y-4\">
          {!isLogin && (
            <div>
              <label className=\"block text-sm font-medium text-neutral-700 mb-1\">Name</label>
              <input
                type=\"text\"
                value={formData.name}
                onChange={(e) => setFormData({...formData, name: e.target.value})}
                className=\"w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500\"
                required={!isLogin}
                data-testid=\"input-name\"
              />
            </div>
          )}

          <div>
            <label className=\"block text-sm font-medium text-neutral-700 mb-1\">Email</label>
            <input
              type=\"email\"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className=\"w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500\"
              required
              data-testid=\"input-email\"
            />
          </div>

          <div>
            <label className=\"block text-sm font-medium text-neutral-700 mb-1\">Password</label>
            <input
              type=\"password\"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className=\"w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500\"
              required
              minLength={6}
              data-testid=\"input-password\"
            />
          </div>

          {error && (
            <div className=\"bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm\">
              {error}
            </div>
          )}

          <button
            type=\"submit\"
            disabled={loading}
            className=\"w-full px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium disabled:opacity-50\"
            data-testid=\"submit-button\"
          >
            {loading ? 'Please wait...' : (isLogin ? 'Login' : 'Create Account')}
          </button>
        </form>

        <div className=\"mt-6 text-center\">
          <p className=\"text-sm text-neutral-600\">
            {isLogin ? \"New to EEFai?\" : \"Already have an account?\"}{' '}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className=\"text-primary-600 hover:text-primary-700 font-medium\"
            >
              {isLogin ? 'Sign up' : 'Login'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
