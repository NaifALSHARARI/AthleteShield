# AthleteShield: Athlete Injury Prediction System

## Overview
AthleteShield is a project that uses machine learning techniques to predict athlete injuries. This system aims to help coaches and sports physicians identify players at risk of injury in advance by analyzing several factors such as playing time, training loads, previous injuries, age, and other risk factors.

## How the Project Works
The project follows these steps:

1. **Data Collection**: The project uses a CSV data file (`player_data_extended_v2.csv`) containing player information such as:
   - Playing time (minutes_played)
   - Training load (training_load)
   - Previous injuries (prev_injuries)
   - Age (age)
   - Injury risk indicator (injury_risk)

2. **Data Processing**: The data is prepared for analysis using `transformers.py` which performs operations such as:
   - Filling missing values
   - Data normalization
   - Categorical variable transformation
   - Splitting data into training and testing sets

3. **Model Building**: `train_model.py` is used to build and train the machine learning model based on the prepared data.

4. **Injury Prediction**: `predictor.py` is used to predict the probability of player injuries based on input data.

5. **User Interface**: The project uses the Django framework to provide an interactive web interface that allows users to:
   - Add player information
   - View risk reports
   - Create recovery plans

## Running the Project
To run the project on your local machine:

1. Make sure Python is installed (version 3.8 or newer)
2. Clone the repository:
   ```
   git clone https://github.com/NaifALSHARARI/AthleteShield.git
   cd AthleteShield
   ```
3. Install required libraries:
   ```
   pip install -r requirements.txt
   ```
4. Run the development server:
   ```
   python manage.py runserver
   ```
5. Open your browser at: http://127.0.0.1:8000/

## Technologies Used
- Python
- Django
- scikit-learn
- pandas
- NumPy
- HTML/CSS/JavaScript

## Project Structure
- `wsgi.py`: Web application entry point
- `train_model.py`: Prediction model training script
- `transformers.py`: Data transformation and preparation
- `predictor.py`: Injury probability prediction
- `player_data_extended_v2.csv`: Player data for training
- `training_app/`: Main Django application
  - `templates/`: HTML templates
  - `models.py`: Database models
  - `views.py`: Handlers and views

## Future Development
- Add real-time biometric data indicators
- Improve model accuracy using advanced machine learning techniques
- Add mobile application interface