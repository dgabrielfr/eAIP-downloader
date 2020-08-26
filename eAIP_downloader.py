# -*- coding: utf-8 -*-

import datetime, urllib.request, urllib.error, os.path, bz2, shutil
import pandas as pd
import utility_module as utm
import os
from tkinter import *
from tkinter.filedialog import *

def browse_file(filename):
    filename = askopenfilename(title="Open airport.txt file", 
                               filetypes=[('text file', '.txt'), ('all files', '.*')])
    inp_browser.insert(0, filename)
    path_to_airac_date = getpath()
    activate_download_btn()
    show_airac()


def browse_folder(folder):
    folder = askdirectory(title="Open folder")
    inp_browser_folder.insert(0, folder)
    activate_download_btn()
    folder_path_SV.set(folder)

def show_airac():
    AIRAC_version_SV.set("Current AIRAC version is: " + utm.latest_valid_AIRAC_name(path_to_airac_date_SV.get()))
    # Alternative (2020-08-13)
    # AIRAC_date_SV.set("Current AIRAC date is: " +  utm.latest_valid_AIRAC_date(path_to_airac_date_SV.get()))
    AIRAC_date_SV.set("Current AIRAC date is: " +  utm.latest_valid_AIRAC_date_formated(path_to_airac_date_SV.get()))
    
def activate_download_btn():
    btn_download.config(state="normal")

def getpath():
    return(path_to_airac_date_SV.get())

def getDLpath():
    return(folder_path_SV.get())

window = Tk()
window.title = "GUI prototype"

path_to_airac_date_SV = StringVar()
folder_path_SV = StringVar()
AIRAC_version_SV = StringVar()
AIRAC_date_SV = StringVar()

path_to_airac_date = getpath()
path_to_download = getDLpath()

# File Browser
label_browser = Label(window, text="Press the button to browse to airac_date file:", width=40)
label_browser.grid(row = 1, column = 1, padx=5, pady=5)

# Need to use a lambda so as not to launch the function
btn_browser = Button(window, text="Browse to file:", 
                     command=lambda: browse_file(path_to_airac_date))
btn_browser.grid(row = 1, column=2, padx=5, pady=5)
inp_browser = Entry(window, textvariable=path_to_airac_date_SV, width=50)
inp_browser.grid(row = 1, column = 3, padx=5, pady=5)


# Get AIRAC date and name as string
eAIP_name_string = utm.latest_valid_AIRAC_name(path_to_airac_date)
eAIP_date_string = utm.latest_valid_AIRAC_date(path_to_airac_date)

# Folder browser
label_folder_browser = Label(window, text="Press the button to browse to the download folder", width=40)
label_folder_browser.grid(row = 2, column = 1, padx=5, pady=5)

# Need to use a lambda so as not to launch the function
btn_folder_browser = Button(window, text="Browse to folder:", command=lambda: browse_folder(path_to_download))
btn_folder_browser.grid(row = 2, column = 2, padx=5, pady=5)
inp_browser_folder = Entry(window, width=50)
inp_browser_folder.grid(row = 2, column = 3, padx=5, pady=5)
inp_browser_folder.setvar(path_to_airac_date)

label_airac = Label(window, textvariable=AIRAC_version_SV)
label_airac.grid(row = 3, column=0, columnspan=2, padx=5, pady=5)

label_airac = Label(window, textvariable=AIRAC_date_SV)
label_airac.grid(row = 4, column=0, columnspan=2, padx=5, pady=5)

# Download button
fixed_url_path = utm.fixed_french_metro_download_url(getDLpath())
btn_download = Button(window, text="Download", 
                            command=lambda: utm.download_french_metro_charts(fixed_url_path, getDLpath()))


btn_download.config(state="disabled")
btn_download.grid(row = 3, column = 2, padx=5, pady=5, columnspan=2, rowspan=2, sticky=W+E)

"""
airport_in = utm.read_airport_file(folder_path_SV.get())
if airport_in != -1:
    utm.download_airport_in_file(folder_path_SV.get(), airport_in, path_to_airac_date)
    os._exit(1)
if path_to_airac_date_SV.get() != "":
    fixed_url_path = utm.fixed_french_metro_download_url(path_to_airac_date)
    utm.download_french_metro_charts(fixed_url_path, "AIRAC " + eAIP_name_string)

    fixed_url_path = utm.fixed_french_reunion_download_url(path_to_airac_date)
    utm.download_french_reunion_charts(fixed_url_path, "AIRAC " + eAIP_name_string)
    utm.write_airport_file(folder_path_SV.get())
else:
    print("ERROR! path to file airac_date.txt is not correct!")
"""

window.mainloop()