import React, { useState } from 'react';

const PredictionForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    age: '',
    gender: 1, // Defaulting to 1. 1 and 2 are typical in this dataset.
    height: '',
    weight: '',
    ap_hi: '',
    ap_lo: '',
    cholesterol: 1,
    gluc: 1,
    smoke: 0,
    alco: 0,
    active: 1
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    if (type === 'radio') {
      setFormData(prev => ({ ...prev, [name]: Number(value) }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value === '' ? '' : Number(value) }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="form-grid">
      <div className="form-group">
        <label>Age (years)</label>
        <input type="number" name="age" min="1" max="120" required value={formData.age} onChange={handleChange} placeholder="e.g. 50" />
      </div>

      <div className="form-group">
        <label>Gender</label>
        <div className="toggle-group">
          <label className={`toggle-label ${formData.gender === 1 ? 'active' : ''}`}>
            <input type="radio" name="gender" value={1} checked={formData.gender === 1} onChange={handleChange} /> Male
          </label>
          <label className={`toggle-label ${formData.gender === 2 ? 'active' : ''}`}>
            <input type="radio" name="gender" value={2} checked={formData.gender === 2} onChange={handleChange} /> Female
          </label>
        </div>
      </div>

      <div className="form-group">
        <label>Height (cm)</label>
        <input type="number" name="height" min="50" max="250" required value={formData.height} onChange={handleChange} placeholder="e.g. 170" />
      </div>

      <div className="form-group">
        <label>Weight (kg)</label>
        <input type="number" name="weight" min="10" max="300" step="0.1" required value={formData.weight} onChange={handleChange} placeholder="e.g. 70" />
      </div>

      <div className="form-group">
        <label>Systolic BP (ap_hi)</label>
        <input type="number" name="ap_hi" min="50" max="300" required value={formData.ap_hi} onChange={handleChange} placeholder="e.g. 120" />
      </div>

      <div className="form-group">
        <label>Diastolic BP (ap_lo)</label>
        <input type="number" name="ap_lo" min="30" max="200" required value={formData.ap_lo} onChange={handleChange} placeholder="e.g. 80" />
      </div>

      <div className="form-group">
        <label>Cholesterol</label>
        <select name="cholesterol" value={formData.cholesterol} onChange={handleChange}>
          <option value={1}>Normal</option>
          <option value={2}>Above Normal</option>
          <option value={3}>Well Above Normal</option>
        </select>
      </div>

      <div className="form-group">
        <label>Glucose</label>
        <select name="gluc" value={formData.gluc} onChange={handleChange}>
          <option value={1}>Normal</option>
          <option value={2}>Above Normal</option>
          <option value={3}>Well Above Normal</option>
        </select>
      </div>

      <div className="form-group">
        <label>Smoking</label>
        <div className="toggle-group">
          <label className={`toggle-label ${formData.smoke === 0 ? 'active' : ''}`}>
            <input type="radio" name="smoke" value={0} checked={formData.smoke === 0} onChange={handleChange} /> No
          </label>
          <label className={`toggle-label ${formData.smoke === 1 ? 'active' : ''}`}>
            <input type="radio" name="smoke" value={1} checked={formData.smoke === 1} onChange={handleChange} /> Yes
          </label>
        </div>
      </div>

      <div className="form-group">
        <label>Alcohol Intake</label>
        <div className="toggle-group">
          <label className={`toggle-label ${formData.alco === 0 ? 'active' : ''}`}>
            <input type="radio" name="alco" value={0} checked={formData.alco === 0} onChange={handleChange} /> No
          </label>
          <label className={`toggle-label ${formData.alco === 1 ? 'active' : ''}`}>
            <input type="radio" name="alco" value={1} checked={formData.alco === 1} onChange={handleChange} /> Yes
          </label>
        </div>
      </div>

      <div className="form-group full-width">
        <label>Physical Activity</label>
        <div className="toggle-group">
          <label className={`toggle-label ${formData.active === 0 ? 'active' : ''}`}>
            <input type="radio" name="active" value={0} checked={formData.active === 0} onChange={handleChange} /> No
          </label>
          <label className={`toggle-label ${formData.active === 1 ? 'active' : ''}`}>
            <input type="radio" name="active" value={1} checked={formData.active === 1} onChange={handleChange} /> Yes
          </label>
        </div>
      </div>

      <button type="submit" className="btn-submit" disabled={loading}>
        {loading ? <span className="loader"></span> : 'Analyze Risk'}
      </button>
    </form>
  );
};

export default PredictionForm;
