from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from ml.predictor import predictor

app = FastAPI(title="Heart Disease Prediction API")

# Allow CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    age: int = Field(..., ge=0, le=120, description="Age in years (or days, depending on dataset. Usually dataset is in days, but we will convert it if needed. Assuming years for frontend input).")
    gender: int = Field(..., description="1 or 2")
    height: float = Field(..., ge=50, le=250, description="Height in cm")
    weight: float = Field(..., ge=10, le=300, description="Weight in kg")
    ap_hi: int = Field(..., ge=0, le=300, description="Systolic blood pressure")
    ap_lo: int = Field(..., ge=0, le=200, description="Diastolic blood pressure")
    cholesterol: int = Field(..., ge=1, le=3, description="1: normal, 2: above normal, 3: well above normal")
    gluc: int = Field(..., ge=1, le=3, description="1: normal, 2: above normal, 3: well above normal")
    smoke: int = Field(..., ge=0, le=1, description="0: no, 1: yes")
    alco: int = Field(..., ge=0, le=1, description="0: no, 1: yes")
    active: int = Field(..., ge=0, le=1, description="0: no, 1: yes")

@app.post("/predict")
def predict_heart_disease(data: PatientData):
    try:
        # We might need to preprocess 'age' if the model expects age in days (common in Cardiovascular Disease dataset)
        # We will wait for the user to confirm. Assuming raw inputs for now.
        
        # Convert pydantic model to dict
        data_dict = data.dict()
        
        # Run prediction
        result = predictor.predict(data_dict)
        
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
