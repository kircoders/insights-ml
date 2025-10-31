import { useState } from 'react';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [targetColumn, setTargetColumn] = useState('');
  const [question, setQuestion] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!file || !targetColumn || !question) {
    alert("Please fill out all fields!");
    return;
  }

  try {
    // STEP 1: Send to /analyze
    const analyzeForm = new FormData();
    analyzeForm.append("file", file);
    analyzeForm.append("target_column", targetColumn);

    const analyzeRes = await fetch(`${import.meta.env.VITE_BACKEND_URL}/analyze`, {
      method: "POST",
      body: analyzeForm,
    });

    if (!analyzeRes.ok) {
      const error = await analyzeRes.json();
      throw new Error(error.detail || "Failed to analyze dataset");
    }

    const analyzeData = await analyzeRes.json();
    console.log("✅ /analyze success:", analyzeData);

    // STEP 2: Send to /ask
    const askForm = new FormData();
    askForm.append("question", question);

    const askRes = await fetch(`${import.meta.env.VITE_BACKEND_URL}/ask`, {
      method: "POST",
      body: askForm,
    });

    if (!askRes.ok) {
      const error = await askRes.json();
      throw new Error(error.detail || "Failed to ask GPT");
    }

    const askData = await askRes.json();
    console.log("✅ /ask success:", askData);

    // Show result to user
    alert("GPT says:\n\n" + askData.answer);
    } catch (err: any) {
      alert("❌ Error: " + err.message);
    }
};

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>📊 InsightBot</h1>
      <p>Welcome! Upload a dataset to get started.</p>

      <form onSubmit={handleSubmit}>
        {/* File input */}
        <div style={{ marginTop: '2rem' }}>
          <label>CSV File: </label>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        {/* Question input */}
        <div style={{ marginTop: '2rem' }}>
          <label>What question do you have about your dataset? </label>
          <input
            type="text"
            placeholder="e.g. Does hours studied impact final_score?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            style={{ width: '400px' }}
          />
        </div>

        {/* Target column input */}
        <div style={{ marginTop: '2rem' }}>
          <label>Target Column: </label>
          <input
            type="text"
            placeholder="e.g. final_score"
            value={targetColumn}
            onChange={(e) => setTargetColumn(e.target.value)}
            style={{ width: '200px' }}
          />
        </div>

        {/* Submit button */}
        <button type="submit" style={{ marginTop: '2rem', display: 'block' }}>
          Submit
        </button>
      </form>
    </div>
  );
}

export default App;
