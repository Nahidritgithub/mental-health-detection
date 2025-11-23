import React, { useState } from "react";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await fetch("http://localhost:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Server error");
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="max-w-2xl w-full bg-white shadow-lg rounded-2xl p-6">
        <h1 className="text-2xl font-bold mb-4 text-center text-indigo-600">
          🧠 Mental Health Risk Detection
        </h1>

        <form onSubmit={handleSubmit}>
          <textarea
            rows={5}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
            placeholder="Type something to analyze..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          ></textarea>

          <div className="flex justify-between mt-4">
            <button
              type="submit"
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700"
              disabled={loading}
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>

            <button
              type="button"
              onClick={() => {
                setText("");
                setResult(null);
                setError(null);
              }}
              className="border px-4 py-2 rounded-lg"
            >
              Clear
            </button>
          </div>
        </form>

        {error && (
          <div className="mt-4 bg-red-100 text-red-700 p-3 rounded-lg">
            Error: {error}
          </div>
        )}

        {result && (
          <div className="mt-6 p-4 bg-green-50 border rounded-lg">
            <h2 className="font-semibold text-gray-800 mb-2">Prediction</h2>
            <div className="space-y-1 text-gray-700">
              <p>
                <strong>Label:</strong> {result.label}
              </p>
              <p>
                <strong>Confidence:</strong>{" "}
                {(result.confidence * 100).toFixed(2)}%
              </p>
              <p>
                <strong>Sentiment:</strong> {result.sentiment}
              </p>
            </div>
          </div>
        
        )}
      </div>
    </div>
  );
}