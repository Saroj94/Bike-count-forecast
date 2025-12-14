from pydantic import BaseModel
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
import os

# Get the path for directory directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

## Define paths for scalers and encoders
ENCODER_X_PATH = os.path.join(BASE_DIR, 'models', 'scaler_X')
ENCODER_funcday_PATH =os.path.join(BASE_DIR, 'models', 'le_funcday')
ENCODER_seasons_PATH = os.path.join(BASE_DIR, 'models', 'le_seasons')
ENCODER_weekday_PATH = os.path.join(BASE_DIR, 'models', 'le_weekday')
ENCODER_month_PATH = os.path.join(BASE_DIR, 'models', 'le_month')
ENCODER_holiday_PATH = os.path.join(BASE_DIR, 'models', 'le_holiday')


# Initialize global variables
scaler_X = None
le_funcday = None
le_seasons = None
le_weekday = None
le_month = None
le_holiday = None

#load model and scalers at startup
def load_resources():
    global scaler_X, le_funcday, le_seasons, le_weekday, le_month, le_holiday
    try:
        with open(ENCODER_X_PATH, 'rb') as f:
            scaler_X = pickle.load(f)
        print(f"Feature scaler loaded from: {ENCODER_X_PATH}")


        with open(ENCODER_funcday_PATH, 'rb') as f:
            le_funcday = pickle.load(f)
        print(f"Label encoder for FuncDay loaded from: {ENCODER_funcday_PATH}")

        with open(ENCODER_seasons_PATH, 'rb') as f:
            le_seasons = pickle.load(f)
        print(f"Label encoder for Seasons loaded from: {ENCODER_seasons_PATH}")

        with open(ENCODER_weekday_PATH, 'rb') as f:
            le_weekday = pickle.load(f)
        print(f"Label encoder for WeekDay loaded from: {ENCODER_weekday_PATH}")

        with open(ENCODER_month_PATH, 'rb') as f:
            le_month = pickle.load(f)
        print(f"Label encoder for Month loaded from: {ENCODER_month_PATH}")

        with open(ENCODER_holiday_PATH, 'rb') as f:
            le_holiday = pickle.load(f)
        print(f"Label encoder for Holiday loaded from: {ENCODER_holiday_PATH}")
     
    except FileNotFoundError as e:
        print(f"Error: Missing file - {e}")
        raise
    except Exception as e:
        print(f"Error loading resources: {e}")
        raise

# Load scalers when module is imported
try:
    load_resources()
except Exception as e:
    print(f"Warning: Resources not loaded at import - {e}")

# Define User input data schema (features received from frontend)
class RequestData(BaseModel):
    Hour: float
    Temp: float
    Humidity: float
    Wind: float
    Visibility: float
    SolarRad: float
    Rainfall: float
    Snowfall: float
    Seasons: str
    Holiday: str
    FuncDay: str
    Day: float
    WeekDay: str
    Month: str
    Year: int

# Feature engineering function
def feature_engineering(data: RequestData) -> np.ndarray:
    """
    Apply feature engineering on user's input values
    Creates new features from Hour and Day
    """
    # Create dictionary from user input
    input_dict = {
        'Hour': data.Hour,
        'Temp': data.Temp,
        'Humidity': data.Humidity,
        'Wind': data.Wind,
        'Visibility': data.Visibility,
        'SolarRad': data.SolarRad,
        'Rainfall': data.Rainfall,
        'Snowfall': data.Snowfall,
        'Seasons': data.Seasons,
        'Holiday': data.Holiday,
        'FuncDay': data.FuncDay,
        'Day': data.Day,
        'WeekDay': data.WeekDay,
        'Month': data.Month,
        'Year': data.Year
    }
    
    # Convert to DataFrame for easier feature engineering
    df = pd.DataFrame([input_dict])
    
    ####FEATURE ENGINEERING FOR CYCLIC AND LABEL ENCODING####
    # After receiving data from users
    # Cyclic encoding for Hour (0-23)
    df['Hour_sin'] = np.sin(2 * np.pi * df['Hour']/24)
    df['Hour_cos'] = np.cos(2 * np.pi * df['Hour']/24)
    
    # Cyclic encoding for Day (1-31)
    df['Day_sin'] = np.sin(2 * np.pi * df['Day']/31)
    df['Day_cos'] = np.cos(2 * np.pi * df['Day']/31)

    # Label encoding for categorical features - handle None/null values
    df['FuncDay'] = df['FuncDay'].fillna(0).astype(str)
    df['Seasons'] = df['Seasons'].fillna(0).astype(str)
    df['WeekDay'] = df['WeekDay'].fillna(0).astype(str)
    df['Month'] = df['Month'].fillna(1).astype(str)
    df['Holiday'] = df['Holiday'].fillna(0).astype(str)
    
    df['FuncDay'] = le_funcday.transform(df['FuncDay'])
    df['Seasons'] = le_seasons.transform(df['Seasons'])
    df['WeekDay'] = le_weekday.transform(df['WeekDay'])
    df['Month'] = le_month.transform(df['Month'])
    df['Holiday'] = le_holiday.transform(df['Holiday']) 

    ##drop the original columns after creating cyclic features
    df.drop(['Hour','Day'], axis=1, inplace=True)
    
    # Define feature order (MUST match training order from notebook)
    feature_columns = ['Temp', 'Humidity', 'Wind', 'Visibility',
                       'SolarRad', 'Rainfall', 'Snowfall', 'Seasons', 
                       'Holiday', 'FuncDay', 'WeekDay', 'Month', 'Year',
                       'Hour_sin', 'Hour_cos', 'Day_sin', 'Day_cos']
    # Convert to numpy array in correct order
    features = df[feature_columns].values
    return features


def Preprocess(data: RequestData):
    """
    Complete pipeline: feature engineering -> scaling -> reshape
    """
    # Feature engineering (user input -> engineered features)
    features = feature_engineering(data)
    
    # Scale features using saved scaler
    features_scaled = scaler_X.transform(features)
    
    # Reshape for RNN (batch_size, timesteps, features)
    # Get the actual number of features from scaled data
    num_features = features_scaled.shape[1]
    x_input = np.repeat(features_scaled, 24, axis=0).reshape(1, 24, num_features)
    
    return x_input