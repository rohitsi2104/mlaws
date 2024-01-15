import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from joblib import dump

def process_csv(csv_file, target_column):
    try:
        # Load CSV data
        data = pd.read_csv(csv_file)

        # Check if the target column exists in the DataFrame
        if target_column not in data.columns:
            raise ValueError(f"Target column '{target_column}' not found in the CSV file.")

        # Handle missing values
        data.fillna(data.mean(), inplace=True)

        # Handle categorical columns
        categorical_columns = data.select_dtypes(include='object').columns
        data = pd.get_dummies(data, columns=categorical_columns)

        # Assume target_column is for regression
        X = data.drop(columns=[target_column])
        y = data[target_column]

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Build and evaluate a simple RandomForestRegressor
        model = RandomForestRegressor()
        model.fit(X_train, y_train)
        evaluation_results = model.score(X_test, y_test)
        with open("model", 'wb') as f:
            dump(model, f)

        return model, evaluation_results

    except Exception as e:
        return None, f"Error processing CSV file: {str(e)}"
