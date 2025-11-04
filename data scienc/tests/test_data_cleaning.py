
import pandas as pd
import numpy as np
import os

def test_cleaning_output():
    """Test that cleaning notebook produces expected outputs"""
    print("🧪 Testing data cleaning...")
    
    # Check if cleaned file exists
    cleaned_path = '../data/interim/diabetes_cleaned.csv'
    assert os.path.exists(cleaned_path), f"Cleaned data file not found at {cleaned_path}"
    
    # Load cleaned data
    df_clean = pd.read_csv(cleaned_path)
    
    # Test no missing values
    missing_total = df_clean.isnull().sum().sum()
    assert missing_total == 0, f"Cleaned data should have no missing values, found {missing_total}"
    
    # Test no zero values in biological features
    biological_features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    zero_counts = {}
    
    for feature in biological_features:
        zero_count = (df_clean[feature] == 0).sum()
        zero_counts[feature] = zero_count
        assert zero_count == 0, f"Cleaned data should have no zeros in {feature}, found {zero_count}"
    
    print(f"✓ No zeros in biological features: {zero_counts}")
    
    # Test data integrity (same number of rows)
    df_raw = pd.read_csv('../data/raw/diabetes.csv')
    assert len(df_clean) == len(df_raw), f"Should not lose any rows during cleaning. Raw: {len(df_raw)}, Clean: {len(df_clean)}"
    
    # Test all original columns present
    expected_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                      'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    for col in expected_columns:
        assert col in df_clean.columns, f"Missing column in cleaned data: {col}"
    
    print("✅ All cleaning tests passed!")

if __name__ == "__main__":
    test_cleaning_output()
