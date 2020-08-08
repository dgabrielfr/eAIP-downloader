# -*- coding: utf-8 -*-
# Python module for eAIP charts downloader

# imports
import pandas as pd
import datetime
import urllib
from string import ascii_uppercase

# Return current AIRAC version as string
def latest_valid_AIRAC_name(filename):
    today = datetime.date.today()
    name_series = pd.read_csv(filename, sep='\t', usecols=[1], header=None)
    df = pd.read_csv(filename, sep='\t', usecols=[4], header=None)
    date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date
    date_mask = (date_series <= today)
    eAIP_name = name_series[date_mask].max()
    return(eAIP_name)

# Return current AIRAC date as string 
def latest_valid_AIRAC_date(filename):
    today = datetime.date.today()
    df = pd.read_csv(filename, sep='\t', usecols=[4], header=None)
    date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date
    date_mask = (date_series <= today)
    eAIP_date = date_series[date_mask].max()
    eAIP_date_string = str(eAIP_date.strftime("%d_%b_%Y")).upper()
    return(eAIP_date_string)

# Build the airport list and save as "filename.txt"
def build_airport_list(filename):
    # if file already exist -> return the file
    if (os.path.isfile(filename)):
        return(filename)
    # else, we build the file
    else:
        with open(filename) as file:
            for c1 in ascii_uppercase:
                for c2 in ascii_uppercase:
                    try:
                        urllib.request.urlretrieve("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + eAIP_date_string + "/FRANCE/AIRAC-" + str(eAIP_date) + "/pdf/FR-AD-2.LF" + c1 + c2 + "-fr-FR.pdf",
                                                    "LF" + c1 + c2 + "-eAIP-" + eAIP_date_string + ".pdf")
                        filename.append("LF" + c1 + c2)
                    except urllib.error.HTTPError as e:
                        print("LF" + c1 +c2 + " not found")

# Download all the charts in the folder "folder"
def download_french_metro_charts(folder):
    create_folder(folder)
    # Check if airport.txt exist
    if (os.path.isfile("airport.txt")):
        with open("airport.txt") as file:
            for lines in file:
                lines = lines.strip() # Don't forget!!
                airport_in.append(lines)

        for icao in airport_in:
            if not(os.path.isfile( icao + "-eAIP-" + eAIP_date_string + ".pdf")):
                urllib.request.urlretrieve("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + eAIP_date_string + "/FRANCE/AIRAC-" + str(eAIP_date) + "/pdf/FR-AD-2." + str(icao) + "-fr-FR.pdf",
                                    str(icao) + "-eAIP-" + eAIP_date_string + ".pdf")

    # If airport.txt not available => download and build airport.txt
    else:
        for c1 in ascii_uppercase:
            for c2 in ascii_uppercase:
                try:
                    urllib.request.urlretrieve("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + eAIP_date_string + "/FRANCE/AIRAC-" + str(eAIP_date) + "/pdf/FR-AD-2.LF" + c1 + c2 + "-fr-FR.pdf",
                                                "LF" + c1 + c2 + "-eAIP-" + eAIP_date_string + ".pdf")
                    airport.append("LF" + c1 + c2)
                except urllib.error.HTTPError as e:
                    print("LF" + c1 +c2 + " not found")

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        print("Folder " +  folder + " already exist!")