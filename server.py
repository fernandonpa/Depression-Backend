from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from catboost import CatBoostClassifier
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://depression-frontend-zeta.vercel.app", "http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models
MODEL_PATH_STUDENT = "models/catboost_model_s.cbm"
MODEL_PATH_WP = "models/catboost_model_wf.cbm"

try:
    model_student = CatBoostClassifier()
    model_student.load_model(MODEL_PATH_STUDENT)
    
    model_wp = CatBoostClassifier()
    model_wp.load_model(MODEL_PATH_WP)
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    model_student = None
    model_wp = None

class PredictionRequest(BaseModel):
    Name: str
    Gender: str
    Age: int
    City: str
    Working_Professional_or_Student: str
    Profession: Optional[str] = None
    Academic_Pressure: Optional[float] = None
    Work_Pressure: Optional[float] = None
    CGPA: Optional[float] = None
    Study_Satisfaction: Optional[float] = None
    Job_Satisfaction: Optional[float] = None
    Sleep_Duration: str
    Dietary_Habits: str
    Degree: Optional[str] = None
    Have_you_ever_had_suicidal_thoughts: str
    Work_Study_Hours: int
    Financial_Stress: float
    Family_History_of_Mental_Illness: str

@app.post("/predict")
async def predict_depression(request: PredictionRequest):
    try:
        # Convert request to dictionary and transform to match model expectations
        data_dict = request.dict()
        
        # Transform the data to match pipeline.py format
        transformed_data = {
            "Name": data_dict["Name"],
            "Gender": data_dict["Gender"],
            "Age": data_dict["Age"],
            "City": data_dict["City"],
            "Working Professional or Student": data_dict["Working_Professional_or_Student"],  # Key change
            "Profession": data_dict["Profession"],
            "Academic Pressure": data_dict["Academic_Pressure"],
            "Work Pressure": data_dict["Work_Pressure"],
            "CGPA": data_dict["CGPA"],
            "Study Satisfaction": data_dict["Study_Satisfaction"],
            "Job Satisfaction": data_dict["Job_Satisfaction"],
            "Sleep Duration": data_dict["Sleep_Duration"],
            "Dietary Habits": data_dict["Dietary_Habits"],
            "Degree": data_dict["Degree"],
            "Have you ever had suicidal thoughts ?": data_dict["Have_you_ever_had_suicidal_thoughts"],  # Key change
            "Work/Study Hours": data_dict["Work_Study_Hours"],  # Key change
            "Financial Stress": data_dict["Financial_Stress"],
            "Family History of Mental Illness": data_dict["Family_History_of_Mental_Illness"]
        }
        
        # Create DataFrame
        df = pd.DataFrame([transformed_data]).astype(str)
        
        # Determine which model to use
        category = df["Working Professional or Student"].iloc[0]
        
        if category == "Student" and model_student:
            model = model_student
        elif category == "Working Professional" and model_wp:
            model = model_wp
        else:
            raise HTTPException(status_code=400, detail="Invalid category or model not loaded")
        
        # Make prediction
        prediction = model.predict(df)
        probability = model.predict_proba(df)[:, 1]
        
        return {
            "prediction": int(prediction[0]),
            "probability": float(probability[0])
        }
        
    except Exception as e:
        print(f"Prediction error: {e}")  # Add logging
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": model_student is not None and model_wp is not None}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)