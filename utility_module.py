# -*- coding: utf-8 -*-
# Python module for eAIP charts downloader

# imports
import pandas as pd
import datetime
import urllib
import shutil
import os.path
import re
from string import ascii_uppercase
from os import listdir

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

# Create the folder if it does not exists yet
def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        print(folder + " already exists")

# Compress folder if it exists (/!\ folder name - 1 /!\)
def compress_folder(folder):
    if os.path.isdir(folder):
        num_part = re.search("[0-9]{4}", folder)
        if os.path.isdir("AIRAC " + str(int(num_part.group())-1)):
            shutil.make_archive("AIRAC " + str(int(num_part.group())-1), 'zip', "AIRAC " + str(int(num_part.group())-1))
    if os.path.isfile("AIRAC " + str(int(num_part.group())-1) + ".zip" and os.path.isdir("AIRAC " + str(int(num_part.group())-1))):
        shutil.rmtree("AIRAC " + str(int(num_part.group())-1))
        print("Folder: AIRAC " + str(int(num_part.group())-1) + " deleted!")

# Return fixed part of French Metropolitan eAIP
# URL example: https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_16_JUL_2020/FRANCE/AIRAC-2020-07-16/pdf/FR-AD-2.LFBA-fr-FR.pdf
def fixed_french_metro_download_url(filename):
    return("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + latest_valid_AIRAC_date_formated(filename) + "/FRANCE/AIRAC-" + latest_valid_AIRAC_date(filename) + "/pdf/FR-AD-2.LF")

# Download the Metropolitan French eAIP charts in PDF format
def download_french_metro_charts(fixed_path, folder):

    num_part = re.search("[0-9]{4}", folder)
    string_airac_date = num_part.group()

    # Create the folder
    create_folder(folder)
    compress_folder(folder)

    # Change directory to the folder
    os.chdir(folder)

    # Download the charts in PDF
    for c1 in ascii_uppercase:
        for c2 in ascii_uppercase:
            full_path = fixed_path + c1 + c2 + "-fr-FR.pdf"
            # Check if the PDF file exists
            if os.path.isfile("LF" + c1 + c2 + "-eAIP-" + string_airac_date + ".pdf"):
                print("LF" + c1 + c2 + "-eAIP-" + string_airac_date + ".pdf" + " Already exists, skipping!")
                continue
            try:
                urllib.request.urlretrieve(full_path, "LF" + c1 + c2 + "-eAIP-" + string_airac_date + ".pdf")
            except urllib.error.HTTPError as e:
                print("LF" + c1 + c2 + " download error: " + str(e))


# Return fixed part of French Réunion eAIP
# URL example: https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_16_JUL_2020/RUN/AIRAC-2020-07-16/pdf/FR-AD-2.FMEE-fr-FR.pdf
def fixed_french_reunion_download_url(filename):
    return("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + latest_valid_AIRAC_date_formated(filename) + "/RUN/AIRAC-" + latest_valid_AIRAC_date(filename) + "/pdf/FR-AD-2.")

# Download the Reunion French eAIP charts in PDF format
def download_french_reunion_charts(fixed_path, folder):
    num_part = re.search("[0-9]{4}", folder)
    string_airac_date = num_part.group()

    # Create the folder and compress the old one, if it exists
    create_folder(folder)
    compress_folder(folder)

    # Change directory to the folder
    # os.chdir(folder)

    # Réunion airport list
    reunion_airport = ["FMCZ", "FMEE", "FMEP"]
    for ad in reunion_airport:
        if os.path.isfile(ad + "-eAIP-" + string_airac_date + ".pdf"):
            print(ad + "-eAIP-" + string_airac_date + ".pdf" + " Already exists, skipping!")
            continue
        try:
           # TODO: replace string with correct value from function :)
            full_path = fixed_path + ad + "-fr-FR.pdf"
            urllib.request.urlretrieve(full_path, ad + "-eAIP-" + string_airac_date + ".pdf")
        except urllib.error.HTTPError as e:
            print(ad + " download error: " + str(e))

# Write airport.txt
def write_airport_file(folder):
    if os.path.isdir(folder):
        print("Folder " + folder + " found!")
    else:
        print("Error! Folder " + folder + " NOT found")
        return(-1)
    
    airport_file = open("airport.txt", "wt")
    files = [f for f in listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    airport_name = set([file_name[:4] for file_name in files])
    print(airport_name)
    for airport in airport_name:
        airport_file.append(airport)
    airport_file.close()
    
# Read airport.txt
def read_airport_file(folder):
    print(os.path.join(folder, "airport.txt"))
    if os.path.isfile(os.path.join(folder, "airport.txt")):
        print("File airport.txt found!")
        os.chdir(folder)
        airport_in =[]
        with open("airport.txt") as file:
            for lines in file:
                lines = lines.strip() # Don't forget!!
                airport_in.append(lines)
        return(airport_in)
    else:
        print("File airport.txt not found!")
        return(-1)

# Download only the airport in airport.txt
def download_airport_in_file(folder, airport_in, filename):

    eAIP_date_string = latest_valid_AIRAC_date_formated(filename)
    num_part = re.search("[0-9]{4}", folder)
    string_airac_date = latest_valid_AIRAC_date(filename)

    for icao in airport_in:
        if not(os.path.isfile( icao + "-eAIP-" + eAIP_date_string + ".pdf")):
            try:
                urllib.request.urlretrieve("https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + eAIP_date_string + "/FRANCE/AIRAC-" + string_airac_date + "/pdf/FR-AD-2." + str(icao) + "-fr-FR.pdf", str(icao) + "-eAIP-" + eAIP_date_string + ".pdf")
            except urllib.error.HTTPError as e:
                print(icao + " download error: " + str(e))
        else:
            print(icao + "-eAIP-" + eAIP_date_string + ".pdf" + " file already exists, skipping!")