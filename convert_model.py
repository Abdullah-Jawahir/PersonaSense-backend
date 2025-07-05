import pickle
import joblib
import os

# Paths
pkl_path = os.path.join("Model Training", "full_personality_prediction_pipeline.pkl")
joblib_path = os.path.join("Model Training", "full_personality_prediction_pipeline.joblib")

if not os.path.exists(pkl_path):
    print(f"❌ Pickle file not found: {pkl_path}")
    exit(1)

# Load the model using joblib since it was saved with joblib.dump()
model = joblib.load(pkl_path)

joblib.dump(model, joblib_path)
print(f"✅ Model converted and saved to {joblib_path}")
