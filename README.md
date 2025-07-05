# PersonaSense Backend API

This is the FastAPI backend for the PersonaSense personality prediction application.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the FastAPI server:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API:**
   - API will be available at: `http://localhost:8000`
   - Interactive docs (Swagger UI): `http://localhost:8000/docs`
   - Alternative docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### GET `/`
- Health check endpoint
- Returns a simple message confirming the API is running

### GET `/health`
- Detailed health check
- Returns status, model loading status, and timestamp

### POST `/predict`
- Main prediction endpoint
- Accepts personality quiz data and returns AI prediction

**Request Body:**
```json
{
  "Social_event_attendance": 5,
  "Going_outside": 3,
  "Friends_circle_size": 10,
  "Post_frequency": 2,
  "Stage_fear": "No",
  "Drained_after_socializing": "Yes",
  "Time_spent_Alone": 4
}
```

**Response:**
```json
{
  "prediction": "Introvert",
  "confidence": 87.5,
  "user_id": "uuid-string",
  "timestamp": "2024-01-01T12:00:00"
}
```

## Model

The backend uses a pre-trained machine learning model located at:
`Model Training/full_personality_prediction_pipeline.pkl`

This model predicts personality types (Introvert/Extrovert) based on user responses to the personality quiz.

## Data Storage

- Predictions are saved as CSV files in the `predictions/` directory
- Each prediction gets a unique user ID and timestamp
- Files are named: `user_{user_id}_{date}.csv`

## CORS

The API is configured to accept requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (Alternative dev server)
- `http://127.0.0.1:5173` (Alternative localhost)

## Error Handling

- Returns 500 error if model fails to load
- Returns 500 error if prediction fails
- Includes detailed error messages for debugging 