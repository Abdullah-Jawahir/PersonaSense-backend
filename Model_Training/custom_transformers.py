import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class FeatureSelector(BaseEstimator, TransformerMixin):
    """Select specific features from the dataset"""
    
    def __init__(self, feature_names):
        self.feature_names = feature_names
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return X[self.feature_names]
    
    def get_feature_names_out(self, input_features=None):
        return self.feature_names


class AdvancedFeatureCreator(BaseEstimator, TransformerMixin):
    """
    Custom transformer for creating advanced features for personality prediction.
    
    This transformer creates composite features that capture complex behavioral patterns
    and personality traits from the raw input features.
    """
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        """
        Fit the transformer. No parameters to learn.
        
        Parameters:
        -----------
        X : pandas DataFrame
            Input features
        y : array-like, optional
            Target variable (not used)
            
        Returns:
        --------
        self : AdvancedFeatureCreator
        """
        return self
    
    def transform(self, X):
        """
        Transform the input data by creating advanced features.
        
        Parameters:
        -----------
        X : pandas DataFrame
            Input features with columns:
            - Social_event_attendance
            - Going_outside
            - Friends_circle_size
            - Post_frequency
            - Time_spent_Alone
            - Stage_fear
            - Drained_after_socializing
            
        Returns:
        --------
        X_transformed : pandas DataFrame
            Original features plus new engineered features
        """
        # Create a copy to avoid modifying the original data
        X_transformed = X.copy()
        
        # 1. Social Activity Score (composite feature)
        X_transformed['Social_Activity_Score'] = (
            X_transformed['Social_event_attendance'] +
            X_transformed['Going_outside'] +
            X_transformed['Friends_circle_size'] +
            X_transformed['Post_frequency']
        ) / 4

        # 2. Solitude Preference Score
        X_transformed['Solitude_Preference'] = X_transformed['Time_spent_Alone'] / 10  # Normalize to 0-1

        # 3. Social Energy Drain Score
        # Ensure original columns are treated as strings before conversion to handle potential NaNs
        X_transformed['Social_Energy_Drain'] = (
            (X_transformed['Stage_fear'].astype(str) == 'Yes').astype(int) +
            (X_transformed['Drained_after_socializing'].astype(str) == 'Yes').astype(int)
        ) / 2

        # 4. Social Confidence Score (inverse of fear)
        X_transformed['Social_Confidence'] = 1 - (X_transformed['Stage_fear'].astype(str) == 'Yes').astype(int)

        # 5. Digital Social Activity
        X_transformed['Digital_Social_Activity'] = X_transformed['Post_frequency'] / 10  # Normalize

        # 6. Physical Social Activity
        X_transformed['Physical_Social_Activity'] = (
            X_transformed['Social_event_attendance'] +
            X_transformed['Going_outside']
        ) / 2

        # 7. Social Network Size Category
        X_transformed['Social_Network_Category'] = pd.cut(
            X_transformed['Friends_circle_size'],
            bins=[-np.inf, 5, 10, 15, np.inf],
            labels=['Very Small', 'Small', 'Medium', 'Large'],
            include_lowest=True,
            right=True
        )

        # 8. Activity Level Category
        X_transformed['Activity_Level'] = pd.cut(
            X_transformed['Social_Activity_Score'],
            bins=[-np.inf, 3, 6, 9, np.inf],
            labels=['Low', 'Medium', 'High', 'Very High'],
            include_lowest=True,
            right=True
        )

        # 9. Interaction patterns - Add a small constant to avoid division by zero
        X_transformed['Online_vs_Offline_Ratio'] = X_transformed['Post_frequency'] / (X_transformed['Social_event_attendance'] + 1e-6)

        # 10. Social comfort zone
        X_transformed['Social_Comfort_Zone'] = (
            X_transformed['Social_Activity_Score'] *
            (1 - X_transformed['Social_Energy_Drain'])
        )

        return X_transformed

    def get_feature_names_out(self, input_features=None):
        """
        Get output feature names for transformation.
        
        Parameters:
        -----------
        input_features : array-like of str or None
            Input feature names
            
        Returns:
        --------
        feature_names_out : array of str
            Transformed feature names
        """
        if input_features is None:
            input_features = [
                'Social_event_attendance', 'Going_outside', 'Friends_circle_size',
                'Post_frequency', 'Time_spent_Alone', 'Stage_fear', 'Drained_after_socializing'
            ]
        
        # Original features plus new engineered features
        new_features = [
            'Social_Activity_Score', 'Solitude_Preference', 'Social_Energy_Drain',
            'Social_Confidence', 'Digital_Social_Activity', 'Physical_Social_Activity',
            'Social_Network_Category', 'Activity_Level', 'Online_vs_Offline_Ratio',
            'Social_Comfort_Zone'
        ]
        
        return list(input_features) + new_features
