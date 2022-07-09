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

from pyinaturalist import get_observations, pprint

observations = get_observations(user_id='niconoe', per_page=5)

pprint(observations)













