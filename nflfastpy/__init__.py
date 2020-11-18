import pandas as pd
from nflfastpy.config import BASE_URL, ROSTER_URL, TEAM_LOGO_URL, SCHEDULE_URL
from nflfastpy.errors import SeasonNotFoundError
import requests
import tempfile
import pyreadr
from matplotlib import image as mpl_image
import os
from nflfastpy._version import __version__

base_dir = os.path.dirname(__file__)

default_headshot = mpl_image.imread('https://raw.githubusercontent.com/fantasydatapros/nflfastpy/master/nflfastpy/images/headshot.png')

def load_pbp_data(year=2020):

    """
    Load NFL play by play data going back to 1999
    """
    
    if type(year) is not int:
        raise TypeError('Please provide an integer between 1999 and 2020 for the year argument.')

    if year < 1999 or year > 2020:
        raise SeasonNotFoundError('Play by play data is only available from 1999 to 2020')

    df = pd.read_csv(BASE_URL.format(year=year), compression='gzip', low_memory=False)

    return df

def load_roster_data():
    """
    Load team roster data 1999 -> 2019
    """
    df = pd.read_csv(ROSTER_URL, compression='gzip', low_memory=False)
    return df

def load_team_logo_data():
    """
    Load NFL team logo data
    """
    df = pd.read_csv(TEAM_LOGO_URL)
    return df

def load_schedule_data(year=2020):
    """
    Load schedule data going back to 1999
    """

    if type(year) is not int:
        raise TypeError('Please provide an integer between 1999 and 2020 for the year argument.')

    if year < 1999 or year > 2020:
        raise SeasonNotFoundError('Schedule data is only available from 1999 to 2020')

    url = SCHEDULE_URL.format(year=year)
    res = requests.get(url)

    file = tempfile.NamedTemporaryFile(mode='wb')
    file.write(res.content)

    schedule_data = pyreadr.read_r(file.name)
    df = schedule_data[None]

    return df



