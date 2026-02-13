import { useState } from 'react';
import './App.css';

function App() {
  const [requirement, setRequirement] = useState('');
  const [language, setLanguage] = useState('python');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!requirement.trim()) {
      setError('Please enter a requirement');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:3001/api/generate', {
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
