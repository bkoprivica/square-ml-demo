import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    df = pd.DataFrame({
        'feature1': np.random.rand(n_samples),
        'feature2': np.random.rand(n_samples),
        'feature3': np.random.rand(n_samples)
    })
    # Create a binary churn target based on a linear combination plus noise
    df['churn'] = (0.5 * df['feature1'] - 0.3 * df['feature2'] + 0.2 * df['feature3'] + np.random.randn(n_samples) * 0.1 > 0).astype(int)
    return df

def train_model():
    df = generate_synthetic_data()
    X = df[['feature1', 'feature2', 'feature3']]
    y = df['churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {acc:.2f}")
    
    # Save the model to disk for production use
    joblib.dump(model, "model.joblib")
    print("Model saved as model.joblib")

if __name__ == "__main__":
    train_model()
