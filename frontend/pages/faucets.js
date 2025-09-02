import { useEffect, useState } from 'react';

const handshakeUrl = process.env.NEXT_PUBLIC_HANDSHAKE_URL || 'http://localhost:8000';

export default function Faucets() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${handshakeUrl}/api/faucets`);
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold text-primary-cyan mb-2">Faucet Registry</h1>
      {loading && <p>Loading...</p>}
      {data && (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-left text-gray-400">
            <thead className="text-xs uppercase">
              <tr>
                <th className="px-4 py-2">Source</th>
                <th className="px-4 py-2">Type</th>
                <th className="px-4 py-2">Share</th>
                <th className="px-4 py-2">Success Rate</th>
              </tr>
            </thead>
            <tbody>
              {data.faucets.map((faucet) => (
                <tr key={faucet.id} className="border-b border-gray-700">
                  <td className="px-4 py-2">{faucet.source}</td>
                  <td className="px-4 py-2">{faucet.type}</td>
                  <td className="px-4 py-2">{faucet.share}</td>
                  <td className="px-4 py-2">{(faucet.success_rate * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
          <h2 className="mt-4 text-lg font-semibold text-primary-lime">Recent Yields</h2>
          <ul className="text-sm list-disc pl-6">
            {data.yields.map((y) => (
              <li key={y.id}>
                {new Date(y.timestamp).toLocaleString()}: ${'{'}y.yield_usd.toFixed(4){'}'}
              </li>
            ))}
          </ul>
        </div>
      )}
      {data && data.faucets.length === 0 && <p>No faucets found.</p>}
    </div>
  );
}