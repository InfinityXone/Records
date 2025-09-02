import { useEffect, useState } from 'react';

const handshakeUrl = process.env.NEXT_PUBLIC_HANDSHAKE_URL || 'http://localhost:8000';

export default function Wallets() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(`${handshakeUrl}/api/wallets`);
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

  // Helper to get assets for a specific wallet
  const getAssets = (walletId) => {
    return data && data.assets ? data.assets.filter((a) => a.wallet_id === walletId) : [];
  };

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold text-primary-cyan mb-2">Wallets</h1>
      {loading && <p>Loading...</p>}
      {data && (
        <div className="space-y-6">
          {data.wallets.map((wallet) => (
            <div key={wallet.id} className="border border-gray-700 rounded-lg p-4">
              <h2 className="text-lg font-semibold text-primary-lime">{wallet.address}</h2>
              <p className="text-sm text-gray-500">Chain: {wallet.chain || 'unknown'}</p>
              <p className="text-sm">Balance: ${'{'}wallet.balance || 0{'}'}</p>
              <div className="mt-2">
                <h3 className="font-medium text-primary-blue">Assets</h3>
                <ul className="ml-4 list-disc text-sm">
                  {getAssets(wallet.id).map((asset) => (
                    <li key={asset.coin}>
                      {asset.coin}: {asset.balance} (${'{'}asset.usd_value || 0{'}'})
                    </li>
                  ))}
                  {getAssets(wallet.id).length === 0 && <li>No assets recorded</li>}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
      {data && data.wallets.length === 0 && <p>No wallets found.</p>}
    </div>
  );
}