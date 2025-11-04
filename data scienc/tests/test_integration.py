
import pandas as pd
import numpy as np
import os

def test_integration():
    """Test the entire preprocessing pipeline integration"""
    print("🧪 Testing full pipeline integration...")
    
    # Test 1: Raw data exists and is valid
    raw_path = '../data/raw/diabetes.csv'
    assert os.path.exists(raw_path), f"Raw data not found at {raw_path}"
    df_raw = pd.read_csv(raw_path)
    assert df_raw.shape == (768, 9), f"Raw data shape incorrect: {df_raw.shape}"
    print("✓ Raw data validated")
    
    # Test 2: Cleaned data exists and is cleaned
    cleaned_path = '../data/interim/diabetes_cleaned.csv'
    assert os.path.exists(cleaned_path), f"Cleaned data not found at {cleaned_path}"
    df_clean = pd.read_csv(cleaned_path)
    assert df_clean.isnull().sum().sum() == 0, "Cleaned data has missing values"
    print("✓ Cleaned data validated")
    
    # Test 3: Processed data exists with new features
    processed_path = '../data/processed/diabetes_processed.csv'
    assert os.path.exists(processed_path), f"Processed data not found at {processed_path}"
    df_processed = pd.read_csv(processed_path)
    assert len(df_processed.columns) >= 15, f"Processed data should have engineered features, got {len(df_processed.columns)}"
    print("✓ Processed data validated")
    
    # Test 4: Data integrity maintained throughout pipeline
    assert len(df_raw) == len(df_clean) == len(df_processed), f"Lost samples during processing. Raw: {len(df_raw)}, Clean: {len(df_clean)}, Processed: {len(df_processed)}"
    print("✓ Data integrity maintained")
    
    # Test 5: Target variable unchanged
    assert (df_raw['Outcome'] == df_processed['Outcome']).all(), "Target variable modified during processing"
    print("✓ Target variable preserved")
    
    # Test 6: File sizes make sense (processed should be larger due to new features)
    raw_size = os.path.getsize(raw_path)
    processed_size = os.path.getsize(processed_path)
    assert processed_size > raw_size, "Processed file should be larger due to engineered features"
    print("✓ File sizes consistent with feature engineering")
    
    print("✅ Full pipeline integration test passed!")

if __name__ == "__main__":
    test_integration()