import { useState } from 'react';

const handshakeUrl = process.env.NEXT_PUBLIC_HANDSHAKE_URL || 'http://localhost:8000';

export default function Predict() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch the latest predictions from the API
  const fetchPredictions = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${handshakeUrl}/api/predictions`);
      const data = await res.json();
      setPredictions(data.predictions || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const runPrediction = async () => {
    setLoading(true);
    try {
      // Trigger a prediction directive for FinSynapse
      await fetch(`${handshakeUrl}/directive`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent: 'FinSynapse', command: 'PREDICT', payload: { topic: 'crypto' } }),
      });
      // Fetch updated predictions after a short delay
      setTimeout(fetchPredictions, 2000);
    } catch (err) {
      console.error(err);
    } finally {
      // Loader will be hidden when predictions are fetched
    }
  };

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold text-primary-cyan">X1‑Predict</h1>
      <p className="text-gray-400">
        Use your swarm to gather market data and produce financial predictions.  Press
        the button below to trigger a prediction run and view the latest
        results.
      </p>
      <button
        className="px-4 py-2 bg-primary-blue hover:bg-primary-cyan text-black font-semibold rounded-lg"
        onClick={runPrediction}
        disabled={loading}
      >
        {loading ? 'Running…' : 'Run Prediction'}
      </button>
      {/* Predictions table */}
      {predictions.length > 0 && (
        <div className="overflow-x-auto mt-6 border border-gray-700 rounded-lg p-2">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-xs uppercase">
                <th className="px-2 py-1 text-left">ID</th>
                <th className="px-2 py-1 text-left">Symbol</th>
                <th className="px-2 py-1 text-left">Prediction</th>
                <th className="px-2 py-1 text-left">Date</th>
              </tr>
            </thead>
            <tbody>
              {predictions.map((p) => (
                <tr key={p.id} className="border-t border-gray-700">
                  <td className="px-2 py-1">{p.id}</td>
                  <td className="px-2 py-1">{p.symbol}</td>
                  <td className="px-2 py-1">{JSON.stringify(p.prediction)}</td>
                  <td className="px-2 py-1">{new Date(p.predicted_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}