# PersonaSense Backend API

This is the FastAPI backend for the PersonaSense personality prediction application.

## Setup

1. **Navigate to the backend directory:**

   ```bash
   cd PersonaSense-backend
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   * **Windows:**

     ```bash
     .\venv\Scripts\activate
     ```
   * **macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the FastAPI server:**

   ```bash
   python main.py
   ```

   Or using uvicorn directly:

   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API:**

   * API: `http://localhost:8000`
   * Swagger UI: `http://localhost:8000/docs`
   * ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### GET `/`

* **Description:** Health check endpoint
* **Returns:** Simple message confirming the API is running

### GET `/health`

* **Description:** Detailed health check
* **Returns:** Status, model loading status, and timestamp

### POST `/predict`

* **Description:** Main prediction endpoint. Accepts personality quiz data and returns AI prediction.

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

```
Model_Training/final_pipeline.joblib
```

This model predicts personality types (Introvert/Extrovert) based on user responses to the personality quiz.

## Data Storage

* Predictions are saved as CSV files in the `predictions/` directory
* Each prediction gets a unique user ID and timestamp
* Files are named:

  ```
  user_{user_id}_{date}.csv
  ```

## CORS

The API is configured to accept requests from:

* `http://localhost:8080` (Vite dev server - I)
* `http://localhost:5173` (Alternative dev server)
* `http://localhost:3000` (Alternative dev server)
* `http://127.0.0.1:5173` (Alternative localhost)

## Error Handling

* Returns **500 error** if model fails to load
* Returns **500 error** if prediction fails
* Includes detailed error messages for debugging
