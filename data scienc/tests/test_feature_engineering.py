import pandas as pd
import numpy as np
import os

def test_feature_engineering():
    """Test that feature engineering produces expected outputs"""
    print("🧪 Testing feature engineering...")
    
    # Check if processed file exists
    processed_path = '../data/processed/diabetes_processed.csv'
    assert os.path.exists(processed_path), f"Processed data file not found at {processed_path}"
    
    # Load processed data
    df_processed = pd.read_csv(processed_path)
    
    # Test new features exist
    expected_new_features = ['Age_Group', 'BMI_Category', 'Glucose_Level', 
                           'Age_Group_encoded', 'BMI_Category_encoded', 'Glucose_Level_encoded']
    
    missing_features = []
    for feature in expected_new_features:
        if feature not in df_processed.columns:
            missing_features.append(feature)
    
    assert len(missing_features) == 0, f"Missing engineered features: {missing_features}"
    print(f"✓ All engineered features present: {expected_new_features}")
    
    # Test scaling (mean ≈ 0, std ≈ 1) with tolerance
    numerical_features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    
    scaling_issues = []
    for feature in numerical_features:
        mean_val = df_processed[feature].mean()
        std_val = df_processed[feature].std()
        
        if abs(mean_val) > 0.01:
            scaling_issues.append(f"{feature} mean not zero (mean: {mean_val:.6f})")
        if abs(std_val - 1) > 0.01:
            scaling_issues.append(f"{feature} std not 1 (std: {std_val:.6f})")
    
    assert len(scaling_issues) == 0, f"Scaling issues: {scaling_issues}"
    print("✓ All numerical features properly scaled")
    
    # Test categorical encoding
    categorical_features = ['Age_Group_encoded', 'BMI_Category_encoded', 'Glucose_Level_encoded']
    encoding_issues = []
    
    for feature in categorical_features:
        if not pd.api.types.is_numeric_dtype(df_processed[feature]):
            encoding_issues.append(f"{feature} not numeric")
        if df_processed[feature].min() < 0:
            encoding_issues.append(f"{feature} has negative values")
    
    assert len(encoding_issues) == 0, f"Encoding issues: {encoding_issues}"
    print("✓ All categorical features properly encoded")
    
    # Test data integrity
    df_clean = pd.read_csv('../data/interim/diabetes_cleaned.csv')
    assert len(df_processed) == len(df_clean), f"Lost samples during feature engineering. Clean: {len(df_clean)}, Processed: {len(df_processed)}"
    
    print("✅ All feature engineering tests passed!")

if __name__ == "__main__":
    test_feature_engineering()