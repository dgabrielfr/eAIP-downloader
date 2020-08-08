# -*- coding: utf-8 -*-
# Python (3) script from maintening French eAIP information up-to date
# Version 0.3
# CHANGES
# Read data from a CSV file
# Should now return the current valid AIRAC instead of the nearest one in time (with may not have been released yet)
# Save the previous AIRAC to a zip file
# TODO: fix bug :
#   When the airport.txt exists -> does not download the PDF files if missing
#   So add a condition before writing the airport.txt file?
#   The bug will not happens in normal use :)

import datetime, urllib.request, urllib.error, os.path, bz2, shutil
import pandas as pd
from string import ascii_uppercase

import utility_module as utm

scriptpath = os.path.dirname(__file__)
filename = os.path.join(scriptpath, "airac_date.txt")

# Get AIRAC date and name as string
eAIP_name_string = utm.latest_valid_AIRAC_name(filename)
eAIP_date_string = utm.latest_valid_AIRAC_date(filename)

# Download folder
# TODO: link to GUI!
folder = os.path.join(scriptpath, "AIRAC " + eAIP_name_string)
fixed_url_path = utm.fixed_french_metro_download_url(filename)
utm.download_french_metro_charts(fixed_url_path, "AIRAC " + eAIP_name_string)
# utm.download_french_reunion_charts("AIRAC " + eAIP_name_string)