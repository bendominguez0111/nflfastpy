import pandas as pd
from nflfastpy.config import BASE_URL, ROSTER_URL, ROSTER_2021_URL, TEAM_LOGO_URL, SCHEDULE_URL
from nflfastpy.errors import SeasonNotFoundError
from nflfastpy.utils import agg_stats
import requests
import tempfile
import pyreadr
from matplotlib import image as mpl_image
import os
from nflfastpy import utils
from nflfastpy._version import __version__

base_dir = os.path.dirname(__file__)

headshot_url = 'https://raw.githubusercontent.com/fantasydatapros/nflfastpy/master/nflfastpy/images/headshot.png'

default_headshot = mpl_image.imread(headshot_url)

def load_pbp_data(year=2021):

    """
    Load NFL play by play data going back to 1999
    """
    
    if type(year) is not int:
        raise TypeError('Please provide an integer between 1999 and 2021 for the year argument.')

    if year < 1999 or year > 2021:
        raise SeasonNotFoundError('Play by play data is only available from 1999 to 2021')

    df = pd.read_csv(BASE_URL.format(year=year), compression='gzip', low_memory=False)

    return df

def load_roster_data(year=2021):
    """
    Load team roster data by season goin back to 1999
    """

    if type(year) is not int:
        raise TypeError('Please provide an integer between 1999 and 2021 for the year argument.')

    if year < 1999 or year > 2021:
        raise SeasonNotFoundError('Roster data is only available from 1999 to 2021')

    season_roster_url = ROSTER_URL.format(year)
    df = pd.read_csv(season_roster_url, low_memory=False)
    
    return df

def load_2021_roster_data():
    """
    Load 2021 roster data
    """
    df = pd.read_csv(ROSTER_2021_URL, low_memory=False)
    return df

def load_team_logo_data():
    """
    Load NFL team logo data
    """
    df = pd.read_csv(TEAM_LOGO_URL)
    return df

def load_schedule_data(year=2021):
    """
    Load schedule data going back to 1999
    """

    if type(year) is not int:
        raise TypeError('Please provide an integer between 1999 and 2021 for the year argument.')

    if year < 1999 or year > 2021:
        raise SeasonNotFoundError('Schedule data is only available from 1999 to 2021')

    url = SCHEDULE_URL.format(year=year)
    res = requests.get(url)

    file = tempfile.NamedTemporaryFile(mode='wb')
    file.write(res.content)

    schedule_data = pyreadr.read_r(file.name)
    df = schedule_data[None]

    return df

def aggregate_stats(pbp, by_team=True):
    """
    TODO: fill in des here
    """

    out_df = agg_stats(pbp)

    return out_df






