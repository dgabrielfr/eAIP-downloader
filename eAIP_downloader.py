# -*- coding: utf-8 -*-

import datetime, urllib.request, urllib.error, os.path, bz2, shutil
import pandas as pd
import utility_module as utm
import os
from tkinter import *
from tkinter.filedialog import *

# Test
def open_file_browser(filename):
    filename = askopenfilename(title="Open folder", filetypes=[('text file', '.txt'), ('all files', '.*')])
    print(filename)
    return(filename)

# GUI
Window = Tk()
folder_label = Label(Window, text="Choose folder path: ")
filename = ""
label_browse = Label(Window, text="Press the button to browse")
label_browse.pack()
btn_browse = Button(Window, text="Browse", command=open_file_browser(filename))
btn_browse.pack()
value = StringVar() 
value.set("texte par défaut")
# entree = Entry(Window, textvariable=string, width=30)
# entree.pack()

scriptpath = os.path.dirname(__file__)
filename = os.path.join(scriptpath, "airac_date.txt")

# Get AIRAC date and name as string
eAIP_name_string = utm.latest_valid_AIRAC_name(filename)
eAIP_date_string = utm.latest_valid_AIRAC_date(filename)

# Download, create and compress folder
folder = os.path.join(scriptpath, "AIRAC " + eAIP_name_string)
airport_in = utm.read_airport_file(folder)
if airport_in != -1:
    utm.download_airport_in_file(folder, airport_in, filename)
    os._exit(1)
fixed_url_path = utm.fixed_french_metro_download_url(filename)
utm.download_french_metro_charts(fixed_url_path, "AIRAC " + eAIP_name_string)

fixed_url_path = utm.fixed_french_reunion_download_url(filename)
utm.download_french_reunion_charts(fixed_url_path, "AIRAC " + eAIP_name_string)
utm.write_airport_file(folder)

Window.mainloop()