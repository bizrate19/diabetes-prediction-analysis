import numpy as np
from pathlib import Path
import os
import pandas as pd

try:
    import yaml
except Exception:
    yaml = None

class DataCleaner:
    def __init__(self, config_path='config/config.yaml'):
        # Determine project root (parent of src)
        project_root = Path(__file__).resolve().parents[1]

        # Resolve config path relative to project root
        cfg_path = Path(config_path)
        if not cfg_path.is_absolute():
            cfg_path = project_root / cfg_path

        if cfg_path.exists():
            if yaml is None:
                raise RuntimeError("PyYAML is required to read config files. Install with: pip install pyyaml")
            with cfg_path.open('r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f) or {}
        else:
            # sensible defaults when no config present
            self.config = {
                "paths": {
                    "raw_data": str(project_root / "data" / "raw" / "diabetes.csv"),
                    "processed_dir": str(project_root / "data" / "processed")
                },
                "params": {"random_seed": 42}
            }

        # normalize raw data path
        raw = Path(self.config.get("paths", {}).get("raw_data", "data/raw/diabetes.csv"))
        if not raw.is_absolute():
            raw = project_root / raw
        self.raw_path = raw

    def load_data(self):
        if not self.raw_path.exists():
            raise FileNotFoundError(
                f"Raw data not found at: {self.raw_path}\n"
                "Place your CSV at that path or create config/config.yaml with 'paths.raw_data' pointing to it."
            )
        return pd.read_csv(self.raw_path)
    
    def identify_missing_values(self, df):
        """Identify zeros in features where zero is biologically impossible"""
        zero_missing_features = self.config['cleaning']['zero_missing_features']
        missing_report = {}
        
        for feature in zero_missing_features:
            if feature in df.columns:
                zero_count = (df[feature] == 0).sum()
                missing_report[feature] = {
                    'zero_count': zero_count,
                    'percentage': (zero_count / len(df)) * 100
                }
        
        return missing_report
    
    def handle_missing_values(self, df):
        """Replace zeros with NaN and impute with median"""
        zero_missing_features = self.config['cleaning']['zero_missing_features']
        
        # Replace zeros with NaN
        df_clean = df.copy()
        for feature in zero_missing_features:
            if feature in df_clean.columns:
                df_clean[feature] = df_clean[feature].replace(0, np.nan)
        
        # Impute missing values with median
        for feature in zero_missing_features:
            if feature in df_clean.columns:
                median_val = df_clean[feature].median()
                df_clean[feature].fillna(median_val, inplace=True)
        
        return df_clean
    
    def detect_outliers(self, df):
        """Detect outliers using IQR method"""
        numerical_features = ['Glucose', 'BloodPressure', 'SkinThickness', 
                           'Insulin', 'BMI', 'Age']
        outlier_report = {}
        
        for feature in numerical_features:
            if feature in df.columns:
                Q1 = df[feature].quantile(0.25)
                Q3 = df[feature].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
                outlier_report[feature] = {
                    'count': len(outliers),
                    'percentage': (len(outliers) / len(df)) * 100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
        
        return outlier_report
    
    def save_cleaned_data(self, df, path=None):
        """Save cleaned dataset"""
        if path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(current_dir, self.config['data']['processed_path'])
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Data saved to: {path}")