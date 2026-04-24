"use client";
import { useState } from "react";
import { sendChatMessage } from "@/lib/api";

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendChatMessage(input);
      setMessages((prev) => [...prev, { role: "ai", text: data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "ai", text: "Error: Could not connect to server." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto p-4">
      {/* Chat Bubbles Container */}
      <div className="flex-1 overflow-y-auto space-y-4 p-4 border rounded-lg bg-gray-50">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === "user" ? "bg-blue-600 text-white" : "bg-white border text-black"}`}>
              {msg.text}
            </div>
          </div>
        ))}
        {loading && <div className="text-gray-400 text-sm">AI is thinking...</div>}
      </div>

      {/* Input Box */}
      <div className="mt-4 flex gap-2">
        <input 
          className="flex-1 p-2 border rounded shadow-sm text-black"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your message..."
        />
        <button 
          onClick={handleSend}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
}