# -*- coding: utf-8 -*-

import datetime, urllib.request, urllib.error, os.path, bz2, shutil
import pandas as pd
import utility_module as utm

from string import ascii_uppercase

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

fixed_url_path = utm.fixed_french_reunion_download_url(filename)
utm.download_french_reunion_charts(fixed_url_path, "AIRAC " + eAIP_name_string)
utm.write_airport_file("AIRAC " + eAIP_name_string)