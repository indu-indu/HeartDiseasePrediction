import React, { useState } from 'react';
import PredictionForm from './components/PredictionForm';
import ResultCard from './components/ResultCard';
import Disclaimer from './components/Disclaimer';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Prediction failed. Please try again.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header-area">
        <h1 className="brand">Heart<span className="brand-highlight">Guard</span></h1>
        <p className="hero-subtitle">
          Clinical Cardiovascular Risk Assessment System.
        </p>
      </div>

      <PredictionForm onSubmit={handlePredict} loading={loading} />

      {error && (
        <div style={{ color: 'var(--danger)', marginTop: '2rem', fontSize: '0.9rem' }}>
          Error: {error}
        </div>
      )}

      {result && <ResultCard result={result} />}

      <Disclaimer />
    </div>
  );
}

export default App;
