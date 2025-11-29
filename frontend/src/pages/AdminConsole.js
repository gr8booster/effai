import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

const AdminConsole = () => {
  const [queue, setQueue] = useState([]);

  useEffect(() => {
    loadQueue();
  }, []);

  const loadQueue = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/support/queue`);
      setQueue(response.data);
    } catch (error) {
      console.error('Queue load error:', error);
    }
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Admin Review Console</h1>
        
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
                    <div className="font-medium">Item ID: {item.item_id}</div>
                    <div className="text-sm text-neutral-600">Agent: {item.agent_id}</div>
                    <div className="mt-2">
                      <button className="px-4 py-2 bg-green-600 text-white rounded mr-2" data-testid={`approve-${idx}`}>
                        Approve
                      </button>
                      <button className="px-4 py-2 bg-red-600 text-white rounded" data-testid={`reject-${idx}`}>
                        Reject
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminConsole;
