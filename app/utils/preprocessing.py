import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_and_normalize(path):
    df = pd.read_csv(path)
    scaler = MinMaxScaler()
    return scaler.fit_transform(df)