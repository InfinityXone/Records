import { useEffect, useState } from 'react';

const handshakeUrl = process.env.NEXT_PUBLIC_HANDSHAKE_URL || 'http://localhost:8000';

export default function ScraperManager() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    source: 'web',
    url: '',
    query: '',
    parse_rules: '',
    frequency: 'daily',
  });
  const [status, setStatus] = useState('');

  // Fetch existing jobs from the API
  const fetchJobs = async () => {
    try {
      const res = await fetch(`${handshakeUrl}/api/scraper-jobs`);
      const data = await res.json();
      setJobs(data.jobs || []);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  // Update form state
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  // Submit a new job to the server
  const createJob = async () => {
    setLoading(true);
    try {
      const payload = {
        source: form.source,
        url: form.url || null,
        query: form.query || null,
        parse_rules: form.parse_rules ? JSON.parse(form.parse_rules) : null,
        frequency: form.frequency,
      };
      await fetch(`${handshakeUrl}/api/scraper-jobs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      setStatus('Job created successfully');
      setForm({ source: 'web', url: '', query: '', parse_rules: '', frequency: 'daily' });
      await fetchJobs();
    } catch (err) {
      console.error(err);
      setStatus('Error creating job');
    } finally {
      setLoading(false);
    }
  };

  const deleteJob = async (id) => {
    if (!confirm('Are you sure you want to delete this job?')) return;
    try {
      await fetch(`${handshakeUrl}/api/scraper-jobs/${id}`, { method: 'DELETE' });
      await fetchJobs();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-4 space-y-6">
      <h1 className="text-2xl font-bold text-primary-cyan">Scraper Manager</h1>
      <p className="text-sm text-gray-400">
        Configure scraping jobs to discover new faucets, APIs or opportunities. Jobs run automatically on a schedule via Cron.
      </p>
      <div className="space-y-4 bg-gray-900 p-4 rounded-lg">
        <h2 className="text-xl font-semibold">Create New Job</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label className="flex flex-col">
            <span className="text-sm font-medium mb-1">Source</span>
            <select name="source" value={form.source} onChange={handleChange} className="bg-gray-800 border border-gray-700 rounded-lg p-2">
              <option value="web">Web</option>
              <option value="github">GitHub</option>
              <option value="darkweb">Dark Web</option>
            </select>
          </label>
          <label className="flex flex-col">
            <span className="text-sm font-medium mb-1">URL</span>
            <input
              type="text"
              name="url"
              value={form.url}
              onChange={handleChange}
              placeholder="https://example.com"
              className="bg-gray-800 border border-gray-700 rounded-lg p-2"
            />
          </label>
          <label className="flex flex-col">
            <span className="text-sm font-medium mb-1">Query</span>
            <input
              type="text"
              name="query"
              value={form.query}
              onChange={handleChange}
              placeholder="Search terms for GitHub"
              className="bg-gray-800 border border-gray-700 rounded-lg p-2"
            />
          </label>
          <label className="flex flex-col">
            <span className="text-sm font-medium mb-1">Parse Rules (JSON)</span>
            <input
              type="text"
              name="parse_rules"
              value={form.parse_rules}
              onChange={handleChange}
              placeholder='{ "selector": "a.link" }'
              className="bg-gray-800 border border-gray-700 rounded-lg p-2"
            />
          </label>
          <label className="flex flex-col">
            <span className="text-sm font-medium mb-1">Frequency</span>
            <select name="frequency" value={form.frequency} onChange={handleChange} className="bg-gray-800 border border-gray-700 rounded-lg p-2">
              <option value="hourly">Hourly</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
            </select>
          </label>
        </div>
        <button
          className="mt-2 px-4 py-2 bg-primary-blue hover:bg-primary-cyan text-black font-semibold rounded-lg"
          onClick={createJob}
          disabled={loading}
        >
          {loading ? 'Creating…' : 'Create Job'}
        </button>
        {status && <p className="text-primary-lime mt-2">{status}</p>}
      </div>
      <div className="bg-gray-900 p-4 rounded-lg">
        <h2 className="text-xl font-semibold mb-2">Existing Jobs</h2>
        {jobs.length === 0 && <p className="text-gray-500">No jobs configured yet.</p>}
        {jobs.length > 0 && (
          <table className="w-full text-sm">
            <thead>
              <tr>
                <th className="px-2 py-1 text-left">ID</th>
                <th className="px-2 py-1 text-left">Source</th>
                <th className="px-2 py-1 text-left">URL/Query</th>
                <th className="px-2 py-1 text-left">Frequency</th>
                <th className="px-2 py-1 text-left">Status</th>
                <th className="px-2 py-1 text-left">Last Run</th>
                <th className="px-2 py-1 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr key={job.id} className="border-t border-gray-700">
                  <td className="px-2 py-1">{job.id}</td>
                  <td className="px-2 py-1 capitalize">{job.source}</td>
                  <td className="px-2 py-1">
                    {job.url || job.query || '-'}
                  </td>
                    <td className="px-2 py-1 capitalize">{job.frequency}</td>
                  <td className="px-2 py-1 capitalize">{job.status}</td>
                  <td className="px-2 py-1">
                    {job.last_run ? new Date(job.last_run).toLocaleString() : 'Never'}
                  </td>
                  <td className="px-2 py-1">
                    <button
                      onClick={() => deleteJob(job.id)}
                      className="text-red-400 hover:text-red-600"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}