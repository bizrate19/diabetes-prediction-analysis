import pandas as pd
import numpy as np
import os

def test_exploration_output():
    """Test that exploration notebook produces expected outputs"""
    print("🧪 Testing data exploration...")
    
    # Load raw data
    df = pd.read_csv('../data/raw/diabetes.csv')
    
    # Test data shape
    assert df.shape == (768, 9), f"Dataset should have 768 rows and 9 columns, got {df.shape}"
    
    # Test column names
    expected_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                      'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    assert list(df.columns) == expected_columns, f"Column names don't match expected. Got: {list(df.columns)}"
    
    # Test for biological impossibilities (should find zeros)
    biological_features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    zero_counts = {}
    
    for feature in biological_features:
        zero_count = (df[feature] == 0).sum()
        zero_counts[feature] = zero_count
        assert zero_count > 0, f"Should find zero values in {feature}, but found {zero_count}"
    
    print(f"✓ Found biological impossibilities: {zero_counts}")
    
    # Test target variable
    assert 'Outcome' in df.columns, "Target variable 'Outcome' missing"
    assert set(df['Outcome'].unique()).issubset({0, 1}), "Outcome should only contain 0 and 1"
    
    print("✅ All exploration tests passed!")

if __name__ == "__main__":
    test_exploration_output()