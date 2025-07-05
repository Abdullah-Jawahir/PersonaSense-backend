import requests
import json

# Test data matching the required format
test_data = {
    "Social_event_attendance": 5,
    "Going_outside": 3,
    "Friends_circle_size": 10,
    "Post_frequency": 2,
    "Stage_fear": "No",
    "Drained_after_socializing": "Yes",
    "Time_spent_Alone": 4
}

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing PersonaSense API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return
    
    # Test prediction endpoint
    try:
        response = requests.post(
            f"{base_url}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        
        if response.status_code == 200:
            prediction_data = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Prediction: {prediction_data['prediction']}")
            print(f"   Confidence: {prediction_data['confidence']}%")
            print(f"   User ID: {prediction_data['user_id']}")
            print(f"   Timestamp: {prediction_data['timestamp']}")
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Prediction error: {e}")

if __name__ == "__main__":
    test_api() 