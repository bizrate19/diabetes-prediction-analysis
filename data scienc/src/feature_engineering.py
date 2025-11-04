import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
import yaml

class FeatureEngineer:
    def __init__(self, config_path='config/config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
    
    def create_age_groups(self, df):
        """Create age groups"""
        age_bins = self.config['feature_engineering']['age_bins']
        age_labels = self.config['feature_engineering']['age_labels']
        df['Age_Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)
        return df
    
    def create_bmi_categories(self, df):
        """Create BMI categories"""
        bmi_bins = self.config['feature_engineering']['bmi_bins']
        bmi_labels = self.config['feature_engineering']['bmi_labels']
        df['BMI_Category'] = pd.cut(df['BMI'], bins=bmi_bins, labels=bmi_labels)
        return df
    
    def create_glucose_levels(self, df):
        """Create glucose level categories"""
        glucose_bins = self.config['feature_engineering']['glucose_bins']
        glucose_labels = self.config['feature_engineering']['glucose_labels']
        df['Glucose_Level'] = pd.cut(df['Glucose'], bins=glucose_bins, labels=glucose_labels)
        return df
    
    def encode_categorical_features(self, df):
        """Encode categorical features"""
        categorical_features = ['Age_Group', 'BMI_Category', 'Glucose_Level']
        label_encoders = {}
        
        for feature in categorical_features:
            le = LabelEncoder()
            df[f'{feature}_encoded'] = le.fit_transform(df[feature])
            label_encoders[feature] = le
        
        return df, label_encoders
    
    def scale_features(self, df, method='StandardScaler'):
        """Scale numerical features"""
        numerical_features = ['Pregnancies', 'Glucose', 'BloodPressure', 
                           'SkinThickness', 'Insulin', 'BMI', 'Age', 
                           'DiabetesPedigreeFunction']
        
        if method == 'StandardScaler':
            scaler = StandardScaler()
        elif method == 'MinMaxScaler':
            scaler = MinMaxScaler()
        else:
            raise ValueError("Unsupported scaling method")
        
        df_scaled = df.copy()
        df_scaled[numerical_features] = scaler.fit_transform(df[numerical_features])
        
        return df_scaled, scaler