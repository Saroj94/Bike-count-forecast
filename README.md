# 🚲 Seoul Bike Demand Forecast: A Deep Learning Solution
## Project Overview
This project delivers a robust, real-time forecasting model to predict the hourly demand for rental bikes in Seoul, South Korea. The goal is to move bike-sharing operations from reactive to proactive logistics, ensuring bikes are always where riders need them.By accurately predicting hourly demand, city operators can:
1. **Reduce Costs**: Minimize the time and effort spent manually re-distributing bikes.
2. **Improve Service**: Prevent stations from running out of bikes (stock-outs) or becoming completely full.

# 🛠️ Technical Solution & Model
This is a time-series regression problem—meaning past hourly weather and usage data directly influence future demand. To capture these complex, sequential patterns, we chose a Deep Learning approach.

**The Dataset**
The model is trained on the Seoul Bike Sharing Demand Dataset, which contains 8,760 hourly observations over one year, including variables for:
- Temporal Factors: Hour of the day, Seasons, Holiday status.
- Weather Conditions: Temperature, Humidity, Wind speed, Rainfall, Snowfall, and Solar Radiation.

**Model Selection**
I built and compared four different Recurrent Neural Network (RNN) architectures (Simple RNN, LSTM, GRU, and a CNN-LSTM hybrid).

The Simple RNN (Recurrent Neural Network) emerged as the best-performing model, demonstrating superior efficiency and accuracy for this specific sequence-based prediction task.

**Core Performance Metrics**
The model's performance was measured on a completely unseen test dataset:
- MAE (Mean Absolute Error)=241.66 Bikes,"On average, the model's prediction is off by only 242 bikes."
- R2 Score=0.6849,The model explains approximately 68.5% of the total variability in bike rental demand.

# 🚀 Deployment & MLOps Pipeline
| Component          | Technology                         | Role                                                                 |
|--------------------|------------------------------------|----------------------------------------------------------------------|
| Prediction API     | FastAPI                            | Provides a robust, high-performance endpoint for real-time predictions. |
| Containerization   | Docker                             | Packages the model, code, and environment for consistent deployment. |
| Image Registry     | Azure Container Registry (ACR)     | Securely stores the deployable Docker image.                          |
| CI/CD              | GitHub Actions                     | Automates the build, test, and deployment process upon code changes. |
| Hosting            | Azure Web Service                  | Provides serverless hosting with automatic scaling to handle varying traffic. |

This automated pipeline ensures that the prediction service is reliable, scalable during peak demand, and easy to update.

# 💡 Future Work & Optimization
While the Simple RNN is successful, it is currently a strong prototype. The next major phase is crucial:

1. Hyperparameter Tuning: We will conduct rigorous, automated tuning of the model's parameters (e.g., number of neurons, learning rate, input sequence length). We anticipate this will significantly increase the model's accuracy and performance.
2. Continuous Monitoring: Implementing a system to constantly monitor the model’s real-world accuracy and trigger alerts if prediction quality begins to degrade (model drift).

# 💻 Project Structure
The repository is organized into two main parts:
| File/Folder                | Description                                                                                                                        |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Bike_Rental_EDA.ipynb     | Exploratory Data Analysis (EDA): Initial data cleaning, description, visualization (charts, plots), and data quality verification. |
| Bike_Rental_DLmodel.ipynb | Deep Learning Modeling: Data preparation for sequential inputs, model building (RNN, LSTM, GRU), training, evaluation, and saving the final model. |
| bike-count-forecast/                  | Deployment Code: Contains the FastAPI application (`main.py`), Dockerfile, and the saved model/preprocessor files for serving the API. |
| notebook/                     | Original and preprocessed dataset files (e.g., `SeoulBikeData.csv`).                                                              |