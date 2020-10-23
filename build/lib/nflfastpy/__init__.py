import pandas as pd
from nflfast_py.config import BASE_URL

def load_pbp_data(year=2020):
    df = pd.read_csv(BASE_URL.format(year=year), compression='gzip', low_memory=False)
    return df

