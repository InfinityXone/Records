import { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';

// Initialise Supabase client using NEXT_PUBLIC_* env variables
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const supabase = supabaseUrl && supabaseAnonKey ? createClient(supabaseUrl, supabaseAnonKey) : null;

const handshakeUrl = process.env.NEXT_PUBLIC_HANDSHAKE_URL || 'http://localhost:8000';

export default function Home() {
  const [selectedAgent, setSelectedAgent] = useState('PromptWriter');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [agents, setAgents] = useState([
    'PromptWriter',
    'FaucetHunter',
    'KeyHarvester',
    'Atlas',
    'Replicator',
    'AnomalyHunter',
    'WalletMonitor',
    'FinSynapse',
    'Guardian',
    'PickyBot',
    'Codex',
  ]);

  useEffect(() => {
    // Subscribe to agent_logs via Supabase and stream new messages
    if (!supabase) return;
    const channel = supabase.channel('agent_logs_changes').on(
      'postgres_changes',
      { event: 'INSERT', schema: 'public', table: 'agent_logs' },
      (payload) => {
        const { new: log } = payload;
        setMessages((prev) => [...prev, { sender: log.agent, content: JSON.stringify(log) }]);
      },
    );
    channel.subscribe();
    return () => {
      channel.unsubscribe();
    };
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;
    // Append the user message locally
    setMessages((prev) => [...prev, { sender: 'you', content: input }]);
    // Send directive to handshake server
    try {
      await fetch(`${handshakeUrl}/directive`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent: selectedAgent,
          command: input.split(' ')[0].toUpperCase(),
          payload: { text: input },
        }),
      });
    } catch (err) {
      console.error(err);
    }
    setInput('');
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 p-4 overflow-y-auto glass">
        <h2 className="text-xl font-semibold mb-4 text-primary-cyan">Agents</h2>
        <ul className="space-y-1">
          {agents.map((agent) => (
            <li
              key={agent}
              className={`p-2 rounded-lg cursor-pointer transition-colors ${selectedAgent === agent ? 'bg-primary-blue/30' : 'hover:bg-white/10'}`}
              onClick={() => setSelectedAgent(agent)}
            >
              {agent}
            </li>
          ))}
        </ul>
      </aside>
      {/* Chat area */}
      <main className="flex-1 flex flex-col">
        <header className="p-4 glass mb-2">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-primary-lime">Infinity X One Cockpit</h1>
              <p className="text-sm text-gray-400">Chat with your agents and monitor the swarm</p>
            </div>
            {/* Navigation links */}
            <nav className="space-x-3 hidden md:flex">
              <a href="/dashboard" className="text-primary-cyan hover:text-primary-lime text-sm">Dashboard</a>
              <a href="/faucets" className="text-primary-cyan hover:text-primary-lime text-sm">Faucets</a>
              <a href="/wallets" className="text-primary-cyan hover:text-primary-lime text-sm">Wallets</a>
              <a href="/agents" className="text-primary-cyan hover:text-primary-lime text-sm">Agents</a>
              <a href="/predict" className="text-primary-cyan hover:text-primary-lime text-sm">Predict</a>
              <a href="/scraper" className="text-primary-cyan hover:text-primary-lime text-sm">Scraper</a>
              <a href="/settings" className="text-primary-cyan hover:text-primary-lime text-sm">Settings</a>
            </nav>
          </div>
        </header>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, index) => (
            <div key={index} className={`max-w-md ${msg.sender === 'you' ? 'self-end text-right' : 'self-start'}`}>
              <div className="text-xs text-gray-500">{msg.sender}</div>
              <div className="bg-white/10 px-3 py-2 rounded-lg inline-block text-sm">
                {msg.content}
              </div>
            </div>
          ))}
        </div>
        <footer className="p-4 glass mt-2">
          <div className="flex items-center space-x-2">
            <input
              type="text"
              className="flex-1 p-2 rounded-lg bg-white/10 text-gray-100 focus:outline-none"
              placeholder={`Send command to ${selectedAgent}...`}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') sendMessage();
              }}
            />
            <button
              className="px-4 py-2 bg-primary-blue hover:bg-primary-cyan text-black font-semibold rounded-lg"
              onClick={sendMessage}
            >
              Send
            </button>
          </div>
        </footer>
      </main>
    </div>
  );
}