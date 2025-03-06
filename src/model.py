import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

from .data import load_or_create_data, preprocess_data, tokenize_input
from .visualization import create_visualization


def load_model():
    """Load the trained model or train it if it doesn't exist"""
    try:
        with open(r'model/model.pkl', 'rb') as file:  # Use raw string
            model = pickle.load(file)
            return model
    except Exception:
        print("Model not found, training a new model...")
        return train_model()


def train_model():
    """Train the model and save it"""
    grouped = load_or_create_data()
    X, y, output = preprocess_data(grouped)

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test, _, output_test = train_test_split(
        X, y, output, test_size=0.2, random_state=42
    )

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = model.predict(X_test)

    # Create a DataFrame for the test set predictions
    test_predictions = pd.DataFrame({
        'Region ID': output_test['region_id'],
        'Time slot': output_test['Time'].dt.strftime('%Y-%m-%d') + '-' + output_test['time_slot'].astype(str),
        'Prediction value': np.round(predictions, 1)
    })

    # Save the test predictions to a CSV file
    test_predictions.to_csv('data/test_predictions.csv', index=False)

    # Create visualization
    create_visualization(X_test, y_test, model)

    # Evaluate the model
    evaluate_model(model, X_test, y_test, X, y)

    # Save the model to a file
    with open(r'model/model.pkl', 'rb') as file:  # Use raw string
        pickle.dump(model, file)

    return model


def evaluate_model(model, X_test, y_test, X, y):
    """Evaluate model performance"""
    # Make predictions
    predictions = model.predict(X_test)

    # Calculate MSE
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {round(mse, 3)}')

    # Perform cross-validation
    scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    avg_mse = -scores.mean()
    print(f'Average Mean Squared Error from Cross-Validation: {round(avg_mse, 3)}')

    return mse, avg_mse


def predict_gap(model, input_str):
    """Make a prediction for the given input string"""
    tokenized_input, time = tokenize_input(input_str)
    if tokenized_input is not None:
        # Make a prediction
        prediction = model.predict(tokenized_input)

        # Format the result
        region_id, time_slot = tokenized_input.iloc[0]
        result = {
            'region_id': int(region_id),
            'time': time.strftime("%Y-%m-%d %H:%M:%S"),
            'time_slot': int(time_slot),
            'prediction': round(float(prediction[0]), 1)
        }
        return result
    return None
