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
    """Get a matplotlib-compatible date number, ignoring the year (to represent day of year)
    Args:
        dt (datetime): date

    Returns:
        datetime: formated date
    """    
    try:
        return dates.date2num(dt.replace(year=datetime.now().year))
    except ValueError:
        return None

def date_to_mpl_time(dt):
    """Get a matplotlib-compatible date number, ignoring the date (to represent time of day)"""
    try:
        return dates.date2num(dt) % 1
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

    # cleaning for ploting
    observations_dataframe['observed_on'] = observations_dataframe['observed_on'].dropna().apply(to_local_tz)
    observations_dataframe['observed_time_mp'] = observations_dataframe['observed_on'].apply(date_to_mpl_time)
    observations_dataframe['observed_on_mp'] = observations_dataframe['observed_on'].apply(date_to_mpl_day_of_year)
    return observations['results'], observations_dataframe



if __name__ == "__main__":
    taxon_number = 52775
    observations_json, df = get_observations_data(taxon_number=taxon_number)
    # Save results for future usage
    with open('data_{}.json'.format(taxon_number), 'w') as f:
        json.dump(observations_json, f, indent=4, sort_keys=True, default=str)

    sns.jointplot(data=df, x='observed_on_mp', y='observed_time_mp', bins=20, kind='hist')
    grid = sns.JointGrid(data=df, x='observed_on_mp', y='observed_time_mp', height=10, dropna=True)
    grid.ax_marg_x.set_title('Observation times of Anax Genus in Granada')
    
    # formatting from pynaturalist DOCS
    # Format X axis labels & ticks
    xaxis = grid.ax_joint.get_xaxis()
    xaxis.label.set_text('Month')
    xaxis.set_major_locator(dates.DayLocator(interval=30))
    xaxis.set_major_formatter(dates.DateFormatter('%b %d'))
    #xaxis.set_minor_locator(dates.DayLocator(interval=7))
    #xaxis.set_minor_formatter(dates.DateFormatter('%d'))

    # Format Y axis labels & ticks
    yaxis = grid.ax_joint.get_yaxis()
    yaxis.label.set_text('Time of Day')
    yaxis.set_major_locator(dates.HourLocator(interval=2))
    yaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    #yaxis.set_minor_locator(dates.HourLocator())
    #yaxis.set_minor_formatter(dates.DateFormatter('%H:%M'))

    # Generate a joint plot with marginal plots
    # Using the hexbin plotting function, because hexagons are the bestagons.
    # Also because it looks just a little like butterfly scales.
    grid.plot_joint(plt.hexbin, gridsize=30, cmap=get_colormap('lightblue'))
    grid.plot_marginals(sns.histplot, color='lightblue', kde=False)