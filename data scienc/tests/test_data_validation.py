import pandas as pd
import numpy as np
import os

def test_data_validation():
    """Validate data quality after preprocessing"""
    print("🧪 Validating final data quality...")
    
    df = pd.read_csv('../data/processed/diabetes_processed.csv')
    
    # 1. Check for missing values
    missing_values = df.isnull().sum().sum()
    assert missing_values == 0, f"Found {missing_values} missing values in processed data"
    print("✓ No missing values")
    
    # 2. Check data types
    numerical_features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome',
                        'Age_Group_encoded', 'BMI_Category_encoded', 'Glucose_Level_encoded']
    
    type_issues = []
    for feature in numerical_features:
        if feature in df.columns and not pd.api.types.is_numeric_dtype(df[feature]):
            type_issues.append(f"{feature} should be numeric")
    
    assert len(type_issues) == 0, f"Data type issues: {type_issues}"
    print("✓ All data types correct")
    
    # 3. Check for duplicates
    duplicates = df.duplicated().sum()
    assert duplicates == 0, f"Found {duplicates} duplicate rows"
    print("✓ No duplicate rows")
    
    # 4. Check value ranges for encoded features
    encoding_issues = []
    encoded_features = ['Age_Group_encoded', 'BMI_Category_encoded', 'Glucose_Level_encoded']
    
    for feature in encoded_features:
        if feature in df.columns:
            unique_vals = df[feature].unique()
            if len(unique_vals) < 2:
                encoding_issues.append(f"{feature} has only {len(unique_vals)} unique value")
            if df[feature].min() < 0:
                encoding_issues.append(f"{feature} has negative values")
    
    assert len(encoding_issues) == 0, f"Encoding range issues: {encoding_issues}"
    print("✓ Encoded features have proper value ranges")
    
    # 5. Check that original biological values are realistic
    biological_features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    
    # Since data is scaled, we'll check that no extreme outliers exist
    outlier_issues = []
    for feature in biological_features:
        if feature in df.columns:
            # Check that values are within reasonable scaled range
            if df[feature].max() > 10 or df[feature].min() < -10:
                outlier_issues.append(f"{feature} has extreme values after scaling")
    
    assert len(outlier_issues) == 0, f"Extreme value issues: {outlier_issues}"
    print("✓ No extreme outliers in biological features")
    
    # 6. Check target variable distribution
    outcome_counts = df['Outcome'].value_counts()
    assert len(outcome_counts) == 2, "Target variable should have exactly 2 classes"
    assert outcome_counts.sum() == len(df), "Target variable should cover all samples"
    print("✓ Target variable distribution valid")
    
    print("🎉 All data quality validation tests passed!")

if __name__ == "__main__":
    test_data_validation()