# FastAPI App Issues Found & Solutions

## **Issues Identified:**

### **1. Working Directory Problem 🔴 (Critical)**
**Location:** `bike.py` and `preprocess.py`

The app loads files using relative paths that might fail in Azure:
```python
# These assume working directory is /app
model = tf.keras.models.load_model('rnn_model.h5')
with open('scaler_X', 'rb') as f:
    scaler_X = pickle.load(f)
```

**Problem:** In Azure App Service, the working directory might be different, causing FileNotFoundError.

---

### **2. File Path Issue in preprocess.py** 🔴

```python
# preprocess.py - Line 17-50
load_resources()  # Called at module import
```

This runs immediately when the module imports, which means if any file is missing, the entire app fails to start.

---

### **3. Missing `.gitignore` entries** 🟡

Your pickle files and model aren't in `.gitignore`, which is good for Docker deployment.

---

## **Solutions:**

### **Option 1: Make Paths More Robust (Recommended)**

Update `bike.py`:
```python
import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_model_loaded():
    global model, scaler_y, model_loaded
    if model_loaded:
        return
    
    try:
        model_path = os.path.join(BASE_DIR, 'rnn_model.h5')
        model = tf.keras.models.load_model(model_path)
        print(f"Model loaded from: {model_path}")
        
        scaler_path = os.path.join(BASE_DIR, 'scaler_y')
        with open(scaler_path, 'rb') as f:
            scaler_y = pickle.load(f)
        print(f"Target scaler loaded from: {scaler_path}")
        model_loaded = True
    except Exception as e:
        print(f"Error loading model: {e}")
        raise
```

Update `preprocess.py`:
```python
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_resources():
    global scaler_X, scaler_y, le_funcday, le_seasons, le_weekday, le_month, le_holiday
    try:
        files = {
            'scaler_X': os.path.join(BASE_DIR, 'scaler_X'),
            'scaler_y': os.path.join(BASE_DIR, 'scaler_y'),
            'le_funcday': os.path.join(BASE_DIR, 'le_funcday'),
            'le_seasons': os.path.join(BASE_DIR, 'le_seasons'),
            'le_weekday': os.path.join(BASE_DIR, 'le_weekday'),
            'le_month': os.path.join(BASE_DIR, 'le_month'),
            'le_holiday': os.path.join(BASE_DIR, 'le_holiday'),
        }
        
        for name, path in files.items():
            with open(path, 'rb') as f:
                if name == 'scaler_X':
                    scaler_X = pickle.load(f)
                elif name == 'scaler_y':
                    scaler_y = pickle.load(f)
                # ... and so on
            print(f"{name} loaded from: {path}")
     
    except FileNotFoundError as e:
        print(f"Error: Missing file - {e}")
        raise
    except Exception as e:
        print(f"Error loading resources: {e}")
        raise
```

---

### **Option 2: Add Error Handling for Missing Files** 🟡

Wrap `load_resources()` to not crash on startup:
```python
# At the end of preprocess.py
try:
    load_resources()
except Exception as e:
    print(f"Warning: Resources not loaded at startup: {e}")
    print("Resources will be loaded on first request")
```

---

### **Option 3: Add Health Check Endpoint** 🟢

Update `bike.py`:
```python
@app.get("/health")
async def health_check():
    ensure_model_loaded()
    return {
        "status": "healthy" if model_loaded else "not_ready",
        "model_loaded": model_loaded,
        "scalers_loaded": scaler_y is not None
    }
```

Use this to debug in Azure:
```bash
curl https://your-app.azurewebsites.net/health
```

---

### **Option 4: Add Startup Event** 🟢

Update `bike.py`:
```python
@app.on_event("startup")
async def startup_event():
    ensure_model_loaded()
    print("App started successfully with model loaded")
```

---

## **Steps to Fix:**

1. ✅ Update `bike.py` with `BASE_DIR` path logic
2. ✅ Update `preprocess.py` with `BASE_DIR` path logic
3. ✅ Add `/health` endpoint
4. ✅ Add startup event
5. ✅ Rebuild Docker image:
   ```bash
   docker build -t bikerent:latest .
   docker tag bikerent:latest bikerent-edfgadexcec7gufg.azurecr.io/bikerent:latest
   docker push bikerent-edfgadexcec7gufg.azurecr.io/bikerent:latest
   ```
6. ✅ Restart Azure App Service:
   ```bash
   az webapp restart --name bikerent --resource-group bikerent
   ```
7. ✅ Test endpoint:
   ```bash
   curl https://bikerent-dgf8e7akcua3gjgr.westeurope-01.azurewebsites.net/health
   ```

---

## **Summary of Changes Needed**

| File | Issue | Fix |
|------|-------|-----|
| `bike.py` | Hardcoded relative paths | Use `os.path.join(BASE_DIR, ...)` |
| `preprocess.py` | Hardcoded relative paths | Use `os.path.join(BASE_DIR, ...)` |
| `bike.py` | No error handling | Add try-except wrapper |
| `bike.py` | Missing health check | Add `/health` endpoint |
| `Dockerfile` | Looks good | No changes needed |

---

**Would you like me to implement these fixes?**

