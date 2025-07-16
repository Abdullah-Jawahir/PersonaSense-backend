import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class AdvancedFeatureCreator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self
    def transform(self, df):
        df_processed = df.copy()
        df_processed['Social_Activity_Score'] = (
            df_processed['Social_event_attendance'] +
            df_processed['Going_outside'] +
            df_processed['Friends_circle_size'] +
            df_processed['Post_frequency']
        ) / 4
        df_processed['Solitude_Preference'] = df_processed['Time_spent_Alone'] / 10
        df_processed['Social_Energy_Drain'] = (
            (df_processed['Stage_fear'].astype(str) == 'Yes').astype(int) +
            (df_processed['Drained_after_socializing'].astype(str) == 'Yes').astype(int)
        ) / 2
        df_processed['Social_Confidence'] = 1 - (df_processed['Stage_fear'].astype(str) == 'Yes').astype(int)
        df_processed['Digital_Social_Activity'] = df_processed['Post_frequency'] / 10
        df_processed['Physical_Social_Activity'] = (
            df_processed['Social_event_attendance'] + df_processed['Going_outside']
        ) / 2
        df_processed['Social_Network_Category'] = pd.cut(
            df_processed['Friends_circle_size'],
            bins=[-np.inf, 5, 10, 15, np.inf],
            labels=['Very Small', 'Small', 'Medium', 'Large'],
            include_lowest=True
        )
        df_processed['Activity_Level'] = pd.cut(
            df_processed['Social_Activity_Score'],
            bins=[-np.inf, 3, 6, 9, np.inf],
            labels=['Low', 'Medium', 'High', 'Very High'],
            include_lowest=True
        )
        df_processed['Online_vs_Offline_Ratio'] = df_processed['Post_frequency'] / (df_processed['Social_event_attendance'] + 1e-6)
        df_processed['Social_Comfort_Zone'] = (
            df_processed['Social_Activity_Score'] * (1 - df_processed['Social_Energy_Drain'])
        )
        return df_processed 