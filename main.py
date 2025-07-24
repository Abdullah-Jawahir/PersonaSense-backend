from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from typing import Optional
import uuid
from datetime import datetime
import sys


# App Initialization
app = FastAPI(title="PersonaSense API", version="1.0.0")

# CORS settings (frontend access control)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "https://personasense.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load Trained Pipeline
MODEL_PATH = "Model_Training/final_pipeline.joblib"
TARGET_ENCODER_PATH = "Model_Training/target_encoder.joblib"

try:
    model_pipeline = joblib.load(MODEL_PATH)
    target_encoder = joblib.load(TARGET_ENCODER_PATH)
    print("Model pipeline loaded successfully!")
    print("Target encoder loaded successfully!")
except Exception as e:
    print(f"Error loading model components: {e}")
    model_pipeline = None
    target_encoder = None


# Request & Response Models
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


# Routes
@app.get("/")
async def root():
    return {"message": "PersonaSense API is live and running!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_pipeline is not None,
        "target_encoder_loaded": target_encoder is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_personality(data: PersonalityData):
    """
    Predict personality type based on user-submitted social behavior inputs.
    """
    if model_pipeline is None or target_encoder is None:
        raise HTTPException(status_code=500, detail="Model pipeline or target encoder not loaded.")

    try:
        # Generate user ID and timestamp
        user_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        # Prepare input DataFrame
        input_df = pd.DataFrame([{
            "Social_event_attendance": data.Social_event_attendance,
            "Going_outside": data.Going_outside,
            "Friends_circle_size": data.Friends_circle_size,
            "Post_frequency": data.Post_frequency,
            "Stage_fear": data.Stage_fear,
            "Drained_after_socializing": data.Drained_after_socializing,
            "Time_spent_Alone": data.Time_spent_Alone
        }])

        # Optional: Save input for audit/debugging
        os.makedirs("predictions", exist_ok=True)
        input_df.to_csv(f"predictions/input_{user_id}_{timestamp[:10]}.csv", index=False)

        # Make prediction using the pipeline (returns encoded prediction)
        prediction_encoded = model_pipeline.predict(input_df)[0]
        
        # Convert encoded prediction back to original label
        prediction = target_encoder.inverse_transform([prediction_encoded])[0]

        # Get prediction confidence
        try:
            proba = model_pipeline.predict_proba(input_df)[0]
            confidence = max(proba) * 100
        except Exception as prob_error:
            print(f"Warning: Could not get prediction probabilities: {prob_error}")
            confidence = 85.0  # fallback if predict_proba is not supported

        # Return response
        return PredictionResponse(
            prediction=prediction,
            confidence=round(confidence, 2),
            user_id=user_id,
            timestamp=timestamp
        )

    except Exception as e:
        print(f"Prediction error details: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# Run with Uvicorn (local dev)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
