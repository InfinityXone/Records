import { useState, useEffect } from 'react';

const handshakeUrl = process.env.NEXT_PUBLIC_HANDSHAKE_URL || 'http://localhost:8000';

export default function Agents() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [agentType, setAgentType] = useState('Infinity Agent One');
  const [replicas, setReplicas] = useState(1);
  const agentOptions = [
    'Infinity Agent One',
    'FinSynapse',
    'Codex',
    'Guardian',
    'PickyBot',
    'Atlas',
    'Echo',
    'Aria',
  ];

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await fetch(`${handshakeUrl}/api/agents`);
        const json = await res.json();
        setMetrics(json);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  const deployAgents = async () => {
    // Use the dedicated API endpoint to request deployment of new agents
    try {
      await fetch(`${handshakeUrl}/api/agents/deploy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent: agentType, count: parseInt(replicas, 10) }),
      });
      alert('Deployment request sent');
    } catch (err) {
      console.error(err);
      alert('Failed to send deployment request');
    }
  };

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold text-primary-cyan">Agent Metrics</h1>
      {loading && <p>Loading...</p>}
      {metrics && (
        <div className="space-y-4">
          <div className="border border-gray-700 rounded-lg p-4">
            <h2 className="text-lg font-semibold text-primary-lime">Current Swarm State</h2>
            <p className="text-sm">Active Agents: {metrics.state.active_agents || 'N/A'}</p>
            <p className="text-sm">Swarm Mode: {metrics.state.swarm_mode || 'N/A'}</p>
            <p className="text-sm">Heartbeat: {metrics.state.heartbeat || 'N/A'}</p>
            <p className="text-sm">Notes: {metrics.state.notes || 'N/A'}</p>
          </div>
          <div className="border border-gray-700 rounded-lg p-4">
            <h2 className="text-lg font-semibold text-primary-lime">Recent Activity</h2>
            <table className="min-w-full text-sm">
              <thead className="text-xs uppercase">
                <tr>
                  <th className="px-2 py-1">Nodes</th>
                  <th className="px-2 py-1">Tasks</th>
                  <th className="px-2 py-1">Success Ratio</th>
                </tr>
              </thead>
              <tbody>
                {metrics.activity.map((a) => (
                  <tr key={a.id} className="border-b border-gray-700">
                    <td className="px-2 py-1">{a.nodes}</td>
                    <td className="px-2 py-1">{a.tasks_completed}</td>
                    <td className="px-2 py-1">{(a.success_ratio * 100).toFixed(2)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="border border-gray-700 rounded-lg p-4">
            <h2 className="text-lg font-semibold text-primary-lime">Deploy New Agents</h2>
            <div className="flex flex-col space-y-2 max-w-sm">
              <label className="text-sm text-gray-300">Agent Type</label>
              <select
                className="p-2 rounded-lg bg-white/10 text-gray-100"
                value={agentType}
                onChange={(e) => setAgentType(e.target.value)}
              >
                {agentOptions.map((opt) => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
              <label className="text-sm text-gray-300">Replicas</label>
              <input
                type="number"
                min="1"
                className="p-2 rounded-lg bg-white/10 text-gray-100"
                value={replicas}
                onChange={(e) => setReplicas(e.target.value)}
              />
              <button
                className="px-4 py-2 bg-primary-blue hover:bg-primary-cyan text-black font-semibold rounded-lg"
                onClick={deployAgents}
              >
                Deploy
              </button>
            </div>
          </div>
        </div>

        {/* System service status */}
        <div className="border border-gray-700 rounded-lg p-4">
          <h2 className="text-lg font-semibold text-primary-lime">System Services</h2>
          <p className="text-sm">Resource Allocator: <span className="text-primary-lime">Active</span></p>
          <p className="text-sm">Knowledge Scanner: <span className="text-primary-lime">Active</span></p>
        </div>
      )}
    </div>
  );
}