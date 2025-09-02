import { useState, useEffect } from 'react';

const colorOptions = [
  { name: 'Cyan', value: '#00FFFF' },
  { name: 'Lime', value: '#A7F432' },
  { name: 'Blue', value: '#1E90FF' },
  { name: 'Pink', value: '#FF69B4' },
];

export default function Settings() {
  const [accent, setAccent] = useState('');

  useEffect(() => {
    const saved = localStorage.getItem('accentColor');
    if (saved) setAccent(saved);
  }, []);

  const applyAccent = (value) => {
    setAccent(value);
    document.documentElement.style.setProperty('--accent-cyan', value);
    localStorage.setItem('accentColor', value);
  };

  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold text-primary-cyan">Settings</h1>
      <div>
        <h2 className="text-lg font-semibold mb-2">Accent Color</h2>
        <div className="flex space-x-2">
          {colorOptions.map((opt) => (
            <button
              key={opt.value}
              className={`p-2 rounded-lg border-2 ${accent === opt.value ? 'border-primary-lime' : 'border-gray-600'}`}
              style={{ backgroundColor: opt.value }}
              onClick={() => applyAccent(opt.value)}
            >
              {opt.name}
            </button>
          ))}
        </div>
      </div>
      <div>
        <h2 className="text-lg font-semibold mb-2">Features</h2>
        <p className="text-gray-400 text-sm">
          Additional configuration options (coming soon) will allow you to enable or disable agents, adjust dashboard widgets, and tweak your UI.
        </p>
      </div>
    </div>
  );
}