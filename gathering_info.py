#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   gathering_info.py
@Time    :   2022/07/09 13:06:13
@Author  :   Bart Ortiz 
@Version :   1.0
@Contact :   bortiz@ugr.es
@License :   CC-BY-SA or GPL3
@Desc    :   Script to contact to inaturalist API and get the information in a dataframe
'''

from pyinaturalist import Observation, get_observations,pprint
import json 
import pandas as pd
import json
from datetime import datetime
from dateutil import tz
from os.path import exists
from pprint import pprint

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib import dates
from matplotlib import pyplot as plt

from pyinaturalist import get_observations, get_places_autocomplete

def date_to_mpl_day_of_year(dt):
    """Get a matplotlib-compatible date number, ignoring the year (to represent day of year)"""
    try:
        return dates.date2num(dt.replace(year=datetime.now().year))
    except ValueError:
        return None

def date_to_mpl_time(dt):
    """Get a matplotlib-compatible date number, ignoring the date (to represent time of day)"""
    try:
        return date_to_num(dt) % 1
    except ValueError:
        return None

def to_local_tz(dt):
    """Convert a datetime object to the local time zone"""
    try:
        return dt.astimezone(tz.tzlocal())
    except (TypeError, ValueError):
        return None

def get_xlim():
    """Get limits of x axis for first and last days of the year"""
    now = datetime.now()
    xmin = dates.date2num(datetime(now.year, 1, 1))
    xmax = dates.date2num(datetime(now.year, 12, 31))
    return xmin, xmax

def get_colormap(color):
    """Make a colormap (gradient) based on the given color; copied from seaborn.axisgrid"""
    color_rgb = mpl.colors.colorConverter.to_rgb(color)
    colors = [sns.set_hls_values(color_rgb, l=l) for l in np.linspace(1, 0, 12)]
    return sns.blend_palette(colors, as_cmap=True)

def pdir(obj, sort_types=False, non_callables=False):
    attrs = {attr: type(getattr(obj, attr)).__name__ for attr in dir(obj)}
    if sort_types:
        attrs = {k: v for k, v in sorted(attrs.items(), key=lambda x: x[1])}
    if non_callables:
        attrs = {k: v for k, v in attrs.items() if v not in ['function', 'method', 'method-wrapper', 'builtin_function_or_method']}
    pprint(attrs, sort_dicts=not sort_types)


def get_observations_data(place_id=30001, taxon_number = None):
    """ Get observations from inaturalist API and return a json + a dataframe 

    Args:
        place_id (int, optional): place where you need to search . Defaults to 30001 (which is my living town).
        taxon_number (_type_, optional): id descripto of the genus /species you look for. Defaults to None.

    Returns:
        _type_: json with the observations + a dataframe with the observations
    """
    observations = get_observations(
    place_id=place_id,
    taxon_id=taxon_number,
    geo=True,
    geoprivacy='open',
    page='all',
    )
    print("Found {n_obs} observations".format(n_obs=len(observations['results'])))
    observations_dataframe = pd.json_normalize(observations['results'])

    return observations_json, observations_dataframe



if __name__ == "__main__":
    observations_json, observations_dataframe = get_observations_data()
    # Save results for future usage
    with open('data_spiders.json', 'w') as f:
        json.dump(observations_json, f, indent=4, sort_keys=True, default=str)


