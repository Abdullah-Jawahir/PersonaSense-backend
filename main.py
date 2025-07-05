from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from typing import Dict, Any
import uuid
from datetime import datetime

app = FastAPI(title="PersonaSense API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://localhost:8080", "https://personasense.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
MODEL_PATH = "Model Training/full_personality_prediction_pipeline.joblib"

try:
    model_pipeline = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model_pipeline = None

class PersonalityData(BaseModel):
    Social_event_attendance: int
    Going_outside: int
    Friends_circle_size: int
    Post_frequency: int
    Stage_fear: str
    Drained_after_socializing: str
    Time_spent_Alone: int

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    user_id: str
    timestamp: str

@app.get("/")
async def root():
    return {"message": "PersonaSense API is running! 🚀"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_pipeline is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_personality(data: PersonalityData):
    """
    Predict personality type based on user responses
    """
    if model_pipeline is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Generate unique user ID
        user_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Create DataFrame with the required format
        df = pd.DataFrame([{
            'id': user_id,
            'Social_event_attendance': data.Social_event_attendance,
            'Going_outside': data.Going_outside,
            'Friends_circle_size': data.Friends_circle_size,
            'Post_frequency': data.Post_frequency,
            'Stage_fear': data.Stage_fear,
            'Drained_after_socializing': data.Drained_after_socializing,
            'Time_spent_Alone': data.Time_spent_Alone
        }])
        
        # Save to CSV (optional, for debugging/analysis)
        csv_path = f"predictions/user_{user_id}_{timestamp[:10]}.csv"
        os.makedirs("predictions", exist_ok=True)
        df.to_csv(csv_path, index=False)
        
        # Make prediction
        prediction = model_pipeline.predict(df)[0]
        
        # Get prediction probabilities for confidence
        try:
            probabilities = model_pipeline.predict_proba(df)[0]
            confidence = max(probabilities) * 100
        except:
            confidence = 85.0  # Default confidence if probabilities not available
        
        return PredictionResponse(
            prediction=prediction,
            confidence=round(confidence, 2),
            user_id=user_id,
            timestamp=timestamp
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 