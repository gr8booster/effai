import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const AdminConsole = () => {
  const [queue, setQueue] = useState([]);
  const [stats, setStats] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [activeTab, setActiveTab] = useState('queue');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    setLoading(true);
    try {
      const [queueRes, auditRes] = await Promise.all([
        axios.get(`${API_URL}/api/support/queue`),
        axios.get(`${API_URL}/api/audit/recent/20`)
      ]);
      
      setQueue(queueRes.data);
      setAuditLogs(auditRes.data);
      
      // Calculate stats
      const statsData = await calculateStats();
      setStats(statsData);
    } catch (error) {
      console.error('Admin data load error:', error);
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/admin/stats`);
      return response.data;
    } catch {
      // Fallback calculations
      return {
        total_users: queue.length,
        pending_reviews: queue.filter(i => i.status === 'pending').length,
        total_letters: auditLogs.filter(l => l.agent_id === 'WriterAgent').length,
        total_tasks: 0
      };
    }
  };

  const handleApprove = async (itemId) => {
    try {
      await axios.post(`${API_URL}/api/support/review/${itemId}`, {
        reviewer_id: 'admin',
        decision: 'approve',
        notes: 'Approved by admin console'
      });
      await loadAdminData();
    } catch (error) {
      console.error('Approval error:', error);
    }
  };

  const handleReject = async (itemId) => {
    try {
      await axios.post(`${API_URL}/api/support/review/${itemId}`, {
        reviewer_id: 'admin',
        decision: 'reject',
        notes: 'Rejected by admin console'
      });
      await loadAdminData();
    } catch (error) {
      console.error('Rejection error:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-neutral-600">Loading admin console...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Admin Console</h1>
        
        {/* Stats Dashboard */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-lg p-6 border shadow-sm">
            <div className="text-sm text-neutral-600 mb-1">Pending Reviews</div>
            <div className="text-3xl font-bold text-neutral-900">{stats?.pending_reviews || 0}</div>
          </div>
          <div className="bg-white rounded-lg p-6 border shadow-sm">
            <div className="text-sm text-neutral-600 mb-1">Total Users</div>
            <div className="text-3xl font-bold text-neutral-900">{stats?.total_users || 0}</div>
          </div>
          <div className="bg-white rounded-lg p-6 border shadow-sm">
            <div className="text-sm text-neutral-600 mb-1">Letters Generated</div>
            <div className="text-3xl font-bold text-neutral-900">{stats?.total_letters || 0}</div>
          </div>
          <div className="bg-white rounded-lg p-6 border shadow-sm">
            <div className="text-sm text-neutral-600 mb-1">Tasks Completed</div>
            <div className="text-3xl font-bold text-neutral-900">{stats?.total_tasks || 0}</div>
          </div>
        </div>
        
        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b border-neutral-200">
          {['queue', 'audit', 'users'].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 font-medium transition-colors ${
                activeTab === tab 
                  ? 'border-b-2 border-primary-600 text-primary-600' 
                  : 'text-neutral-600 hover:text-neutral-900'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>
        
        {/* Review Queue Tab */}
        {activeTab === 'queue' && (
          <div className="bg-white rounded-lg border">
            <div className="p-4 border-b">
              <h2 className="font-semibold">Review Queue ({queue.length})</h2>
            </div>
            <div className="p-4">
              {queue.length === 0 ? (
                <div className="text-neutral-500 text-center py-8">No items pending review</div>
              ) : (
                <div className="space-y-4">
                  {queue.map((item, idx) => (
                    <div key={idx} className="p-4 border rounded" data-testid={`queue-item-${idx}`}>
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <div className="font-medium text-lg">Item: {item.item_id}</div>
                          <div className="text-sm text-neutral-600">Agent: {item.agent_id}</div>
                          <div className="text-sm text-neutral-600">Reason: {item.flagged_reason}</div>
                        </div>
                        <span className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded">Pending</span>
                      </div>
                      <div className="mt-3 flex gap-2">
                        <button 
                          onClick={() => handleApprove(item.item_id)}
                          className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700" 
                          data-testid={`approve-${idx}`}
                        >
                          Approve
                        </button>
                        <button 
                          onClick={() => handleReject(item.item_id)}
                          className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700" 
                          data-testid={`reject-${idx}`}
                        >
                          Reject
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
        
        {/* Audit Logs Tab */}
        {activeTab === 'audit' && (
          <div className="bg-white rounded-lg border">
            <div className="p-4 border-b">
              <h2 className="font-semibold">Recent Audit Logs ({auditLogs.length})</h2>
            </div>
            <div className="p-4">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-neutral-200">
                  <thead>
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase">Provenance ID</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase">Agent</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase">Timestamp</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase">Hash</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-neutral-200">
                    {auditLogs.map((log, idx) => (
                      <tr key={idx} className="hover:bg-neutral-50">
                        <td className="px-4 py-3 text-sm font-mono">{log.provenance_id?.substring(0, 16)}...</td>
                        <td className="px-4 py-3 text-sm">{log.agent_id}</td>
                        <td className="px-4 py-3 text-sm">{new Date(log.timestamp_utc).toLocaleString()}</td>
                        <td className="px-4 py-3 text-sm font-mono text-xs">{log.output_hash?.substring(0, 12)}...</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
        
        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="bg-white rounded-lg border p-6">
            <h2 className="font-semibold mb-4">User Management</h2>
            <p className="text-neutral-600 text-sm">User search and filtering coming soon. Currently managing {stats?.total_users || 0} users.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminConsole;