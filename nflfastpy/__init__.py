import pandas as pd
from nflfastpy.config import BASE_URL, ROSTER_URL, TEAM_LOGO_URL
from nflfastpy.utils import convert_to_gsis_id

def load_pbp_data(year=2020):
    df = pd.read_csv(BASE_URL.format(year=year), compression='gzip', low_memory=False)
    return df

def load_roster_data():
    df = pd.read_csv(ROSTER_URL, compression='gzip', low_memory=False)
    return df

def load_team_logo_data():
    df = pd.read_csv(TEAM_LOGO_URL)
    return df