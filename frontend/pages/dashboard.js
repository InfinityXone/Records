import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const supabase = supabaseUrl && supabaseAnonKey ? createClient(supabaseUrl, supabaseAnonKey) : null;

export default function Dashboard() {
  const [ledger, setLedger] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchLedger = async () => {
      if (!supabase) return;
      setLoading(true);
      const { data, error } = await supabase
        .from('profit_ledger')
        .select('*')
        .order('timestamp', { ascending: false })
        .limit(20);
      if (!error) setLedger(data || []);
      setLoading(false);
    };
    fetchLedger();
  }, []);

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold text-primary-cyan mb-2">Financial Dashboard</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm text-left text-gray-400">
            <thead className="text-xs uppercase">
              <tr>
                <th scope="col" className="px-4 py-2">Timestamp</th>
                <th scope="col" className="px-4 py-2">Amount</th>
                <th scope="col" className="px-4 py-2">Source</th>
              </tr>
            </thead>
            <tbody>
              {ledger.map((entry) => (
                <tr key={entry.id} className="border-b border-gray-700">
                  <td className="px-4 py-2">
                    {new Date(entry.timestamp * 1000).toLocaleString()}
                  </td>
                    <td className="px-4 py-2 text-primary-lime">${'{'}entry.amount.toFixed(4){'}'}</td>
                    <td className="px-4 py-2">{entry.source}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {ledger.length === 0 && (
            <p className="mt-2 text-gray-500">No data available.</p>
          )}
        </div>
      )}
    </div>
  );
}