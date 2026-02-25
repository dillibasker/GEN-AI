import { useState } from 'react';
import './App.css';
import jsPDF from "jspdf";

function App() {
  const [requirement, setRequirement] = useState('');
  const [language, setLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const API_URL = import.meta.env.VITE_API_URL;

  const handleGenerate = async () => {
    if (!requirement.trim()) {
      setError('Please enter a requirement');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ requirement, language }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Generation failed');
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = () => {
  if (!result) return;

  const doc = new jsPDF();
  let y = 10;

  const addSection = (title, content) => {
    if (!content) return;

    doc.setFontSize(14);
    doc.text(title, 10, y);
    y += 8;

    doc.setFontSize(10);
    const lines = doc.splitTextToSize(content, 180);
    doc.text(lines, 10, y);
    y += lines.length * 6 + 10;

    // New page if overflow
    if (y > 270) {
      doc.addPage();
      y = 10;
    }
  };

  doc.setFontSize(16);
  doc.text("Multi-Agent Code Generation Report", 10, y);
  y += 12;

  addSection("Requirement", requirement);
  addSection("Plan", result.plan);
  addSection("Design", result.design);
  addSection("Generated Code", result.code);
  addSection("Test Result", result.test_result);
  addSection("Summary", result.summary);

  doc.save("Multi-Agent-Code-Report.pdf");
};
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Multi-Agent Code Generator</h1>
        <p>AI-powered code generation with orchestration</p>
      </header>

      <main className="main">
        <div className="input-section">
          <div className="form-group">
            <label htmlFor="requirement">What do you want to build?</label>
            <textarea
              id="requirement"
              value={requirement}
              onChange={(e) => setRequirement(e.target.value)}
              placeholder="E.g., Create a function to sort an array of numbers..."
              rows={4}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="language">Target Language</label>
            <select
              id="language"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              disabled={loading}
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
            </select>
          </div>

          <button
            className="generate-btn"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Generating...
              </>
            ) : (
              'Generate Code'
            )}
          </button>

          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}
        </div>

        {result && (
          <div className="results-section">
            <ResultCard
              title="Plan"
              icon="📋"
              content={result.plan}
              onCopy={() => copyToClipboard(result.plan)}
            />
            <ResultCard
              title="Design"
              icon="🎨"
              content={result.design}
              onCopy={() => copyToClipboard(result.design)}
            />
            <ResultCard
              title="Generated Code"
              icon="💻"
              content={result.code}
              onCopy={() => copyToClipboard(result.code)}
              isCode
            />
            <ResultCard
              title="Test Result"
              icon="✓"
              content={result.test_result}
              onCopy={() => copyToClipboard(result.test_result)}
            />

            {/* ✅ NEW SUMMARY CARD */}
            {result.summary && (
              <ResultCard
                title="Summary"
                icon="🧠"
                content={result.summary}
                onCopy={() => copyToClipboard(result.summary)}
              />
            )}
          </div>
        )}

        {result && (
          <div className="download-section">
            <button
              className="generate-btn download-btn"
              onClick={downloadPDF}
            >
              📄 Download PDF Report
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

function ResultCard({ title, icon, content, onCopy, isCode }) {
  return (
    <div className="result-card">
      <div className="result-header">
        <h2>
          <span className="icon">{icon}</span>
          {title}
        </h2>
        <button className="copy-btn" onClick={onCopy} title="Copy to clipboard">
          Copy
        </button>
      </div>
      <div className={`result-content ${isCode ? 'code' : ''}`}>
        <pre>{content}</pre>
      </div>
    </div>
  );
}

export default App;