# -*- coding: utf-8 -*-
# Python module for eAIP charts downloader

# imports
import pandas as pd
import datetime
import urllib
import os.path
from string import ascii_uppercase

# Return current AIRAC version as string
def latest_valid_AIRAC_name(filename):
    today = datetime.date.today()
    name_series = pd.read_csv(filename, sep='\t', usecols=[1], header=None)
    df = pd.read_csv(filename, sep='\t', usecols=[4], header=None)
    date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date
    date_mask = (date_series <= today)
    eAIP_name = name_series[date_mask].max()
    return(str(eAIP_name[1]))

# Return current AIRAC date as string 
def latest_valid_AIRAC_date_formated(filename):
    today = datetime.date.today()
    df = pd.read_csv(filename, sep='\t', usecols=[4], header=None)
    date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date
    date_mask = (date_series <= today)
    eAIP_date = date_series[date_mask].max()
    eAIP_date_string = str(eAIP_date.strftime("%d_%b_%Y")).upper()
    return(eAIP_date_string)

# Return current AIRAC date as string 
def latest_valid_AIRAC_date(filename):
    today = datetime.date.today()
    df = pd.read_csv(filename, sep='\t', usecols=[4], header=None)
    date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date
    date_mask = (date_series <= today)
    eAIP_date = str(date_series[date_mask].max())
    return(eAIP_date)

# Return fixed part of French Metropolitan eAIP
# exemple url https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_16_JUL_2020/FRANCE/AIRAC-2020-07-16/pdf/FR-AD-2.LFBA-fr-FR.pdf
def fixed_french_metro_download_url(filename):
    return("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + latest_valid_AIRAC_date_formated(filename) + "/FRANCE/AIRAC-" + latest_valid_AIRAC_date(filename) + "/pdf/FR-AD-2.LF")

# Download the Metropolitan French eAIP charts in PDF format
def download_french_metro_charts(fixed_path):
    print("TODO!!!")
