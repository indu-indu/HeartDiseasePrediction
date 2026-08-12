import React from 'react';

const ResultCard = ({ result }) => {
  const isHighRisk = result.prediction === 1;
  const confPercent = Math.round(result.confidence * 100);

  return (
    <div className={`result-card ${isHighRisk ? 'risk-high' : 'risk-low'}`}>
      <div className="result-label">
        {isHighRisk ? 'Elevated Cardiovascular Risk' : 'Low Cardiovascular Risk'}
      </div>
      
      <div className="confidence">
        {confPercent}%
      </div>
      
      <div className="result-msg">
        Model confidence score
      </div>
      
      {result.message && (
        <div style={{ marginTop: '1rem', fontSize: '0.8rem', color: 'rgba(0,0,0,0.4)', marginBottom: '1rem' }}>
          System note: {result.message}
        </div>
      )}
    </div>
  );
};

export default ResultCard;
