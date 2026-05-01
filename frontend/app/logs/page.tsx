"use client";
import { useEffect, useState } from "react";

type Log = {
  id: number;
  agent_name: string | null;
  prompt: string;
  response: string;
  tokens_used: number;
  success: boolean | null;
  created_at: string;
};

export default function LogsPage() {
  const [logs, setLogs] = useState<Log[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    const url = `http://localhost:8000/api/v1/logs?page=${page}&size=10&agent=${filter}`;
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setLogs(data.logs);
        setTotalPages(data.total_pages);
      });
  }, [page, filter]); // Re-fetch when page or filter changes

  return (
    <div className="p-6 max-w-6xl mx-auto">
      {/* Header and Filter code from before... */}

      {/* Table code from before... */}
      <div className="overflow-x-auto mt-6">
        <table className="min-w-full bg-white border border-gray-200 rounded-lg">
          <thead>
            <tr className="bg-gray-100">
              <th className="px-4 py-2 border">ID</th>
              <th className="px-4 py-2 border">Agent Name</th>
              <th className="px-4 py-2 border">Prompt</th>
              <th className="px-4 py-2 border">Response</th>
              <th className="px-4 py-2 border">Tokens Used</th>
              <th className="px-4 py-2 border">Success</th>
              <th className="px-4 py-2 border">Created At</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center py-4 text-gray-500">No logs found.</td>
              </tr>
            ) : (
              logs.map((log) => (
                <tr key={log.id} className="border-t">
                  <td className="px-4 py-2 border">{log.id}</td>
                  <td className="px-4 py-2 border">{log.agent_name || '-'}</td>
                  <td className="px-4 py-2 border max-w-xs truncate" title={log.prompt}>{log.prompt}</td>
                  <td className="px-4 py-2 border max-w-xs truncate" title={log.response}>{log.response}</td>
                  <td className="px-4 py-2 border">{log.tokens_used}</td>
                  <td className="px-4 py-2 border">{log.success === null ? '-' : log.success ? 'Yes' : 'No'}</td>
                  <td className="px-4 py-2 border">{new Date(log.created_at).toLocaleString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      <div className="flex justify-between items-center mt-6">
        <button 
          disabled={page === 1}
          onClick={() => setPage(p => p - 1)}
          className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >
          Previous
        </button>
        
        <span className="text-sm font-medium">
          Page {page} of {totalPages}
        </span>

        <button 
          disabled={page === totalPages}
          onClick={() => setPage(p => p + 1)}
          className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}