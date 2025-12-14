from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from preprocess import Preprocess,RequestData
import uvicorn
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
import os

# Get the path and directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths for model and encoders/scalers
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'rnn_model.h5')
ENCODER_PATH = os.path.join(BASE_DIR, 'models')

# Jinja2 Templates setup
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Initialize FastAPI app
app = FastAPI(    
    title="Bike Rental Forecasting System",
    description="Forecasting bike rental demand using RNN model",
    version="1.0.0")

# Enable CORS for all origins 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and scalers
model = None
scaler_y = None
model_loaded = False

# load model and scalers
def ensure_model_loaded():
    global model, scaler_y, model_loaded
    if model_loaded:
        return
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Model loaded successfully!")
        
        scaler_path = os.path.join(ENCODER_PATH, 'scaler_y')
        with open(scaler_path, 'rb') as f:
            scaler_y = pickle.load(f)
        print("Target scaler loaded successfully!")

        model_loaded = True
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        raise
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


# Serve index.html using Jinja2
@app.get("/", response_class=HTMLResponse)
async def get_root(request: Request):
    """
    Serve index.html with optional dynamic data
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_title": "Bike Rental Prediction System",
            "version": "1.0",
        }
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        ensure_model_loaded()
        return {
            "status": "healthy",
            "model_loaded": model_loaded,
            "scalers_loaded": scaler_y is not None,
            "base_dir": BASE_DIR
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "model_loaded": False
        }

@app.on_event("startup")  
async def startup_event():
    print("Starting Bike Rental Forecasting API...")
    print(f"Base directory: {BASE_DIR}")
    try:
        ensure_model_loaded()
        print("API started successfully with model loaded")
    except Exception as e:
        print(f"Warning: Model not loaded at startup - {e}")
        print("API started, model will load on first request")

# Prediction endpoint
@app.post("/predict")
async def predict(data: RequestData):
    try:
        ensure_model_loaded()
        if model is None or scaler_y is None:
            raise HTTPException(status_code=503, detail="Model not loaded")  # ← FIX 2: Added status_code
        
        preprocess_featured = Preprocess(data)
        pred = model.predict(preprocess_featured, verbose=0)
        final_prediction = scaler_y.inverse_transform(pred)
        return {
            "Prediction": float(final_prediction[0][0]),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    # dynamic PORT environment variable for cloud deployment
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port) 