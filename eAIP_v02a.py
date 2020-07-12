# -*- coding: utf-8 -*-
# Python (3) script from maintening eAIP information up-to date
# Version 0.2a
# CHANGES
# Read data from a CSV fie
# Should no return the current valid AIRAC instead of the nearest one in time (with may not have been released yet)

import datetime, urllib.request, urllib.error, os.path
import pandas as pd
from string import ascii_uppercase

def latest_valid_airac(date_series, date):
    date_mask = (date_series < date)
    return date_series[date_mask].max()

# Read CSV file and extract only the AIRAC publication date
# Caution to datetime type
df = pd.read_csv("airac_date.txt", sep='\t', usecols=[4], header=None)
date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date

# today date
today = datetime.date.today()

eAIP_date = latest_valid_airac(date_series, today)
print("Current AIRAC date is:")
print(eAIP_date)

# available airport list
# TODO: load from external file if available
airport = []
airport_in = []

# eAIP_date = datetime.date(2018, 3, 1)
eAIP_date_string = str(eAIP_date.strftime("%d_%b_%Y")).upper()
# print(eAIP_date_string)

# check if airport.txt exist

if (os.path.isfile("airport.txt")):
    with open("airport.txt") as file:
        for lines in file:
            lines = lines.strip() # Don't forget!!
            airport_in.append(lines)

    for icao in airport_in:
        print (icao)
        if not(os.path.isfile( icao + "-eAIP-" + eAIP_date_string + ".pdf")):
            urllib.request.urlretrieve("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + eAIP_date_string + "/FRANCE/AIRAC-" + str(eAIP_date) + "/pdf/FR-AD-2." + str(icao) + "-fr-FR.pdf",
                                   str(icao) + "-eAIP-" + eAIP_date_string + ".pdf")

# if airport.txt not available => download and build airport.txt
else:
    for c1 in ascii_uppercase:
        for c2 in ascii_uppercase:
          try:
            urllib.request.urlretrieve("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + eAIP_date_string + "/FRANCE/AIRAC-" + str(eAIP_date) + "/pdf/FR-AD-2.LF" + c1 + c2 + "-fr-FR.pdf",
                                         "LF" + c1 + c2 + "-eAIP-" + eAIP_date_string + ".pdf")
            airport.append("LF" + c1 + c2)
          except urllib.error.HTTPError as e:
              print("LF" + c1 +c2 + " not found")

    airport_file = open("airport.txt", 'w')
    for item in airport:
        airport_file.write("%s\n" %item)
