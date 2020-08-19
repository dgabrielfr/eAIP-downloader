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

def browse_folder(folder):
    folder = askdirectory(title="Open folder")
    inp_browser_folder.insert(0, folder)

filename = ""
folder = ""

window = Tk()
window.title = "GUI prototype"

file_path = StringVar()
folder_path = StringVar()
fixed_url_path = StringVar()

# File Browser
label_browser = Label(window, text="Press the button to browse to airport file:")
label_browser.grid(row = 1, column = 1, padx=5, pady=5)

# Need to use a lambda so as not to launch the function
btn_browser = Button(window, text="Browse to file:", 
                     command=lambda: browse_file(filename))
btn_browser.grid(row = 1, column=2, padx=5, pady=5)
inp_browser = Entry(window)
inp_browser.grid(row = 1, column = 3, padx=5, pady=5)
# print(filename) # ""

# Get AIRAC date and name as string
eAIP_name_string = utm.latest_valid_AIRAC_name(filename)
eAIP_date_string = utm.latest_valid_AIRAC_date(filename)

# Folder browser
label_folder_browser = Label(window, text="Press the button to browse to the download folder")
label_folder_browser.grid(row = 2, column = 1, padx=5, pady=5)

# Need to use a lambda so as not to launch the function
btn_folder_browser = Button(window, text="Browse to folder:", command=lambda: browse_folder(folder))
btn_folder_browser.grid(row = 2, column = 2, padx=5, pady=5)
inp_browser_folder = Entry(window)
inp_browser_folder.grid(row = 2, column = 3, padx=5, pady=5)
inp_browser_folder.setvar(filename)


def aux_func(fixed_url_path, folder):
    msg = "Calling aux_func with args: "
    print(msg, fixed_url_path, folder)

    print("Filename: ", filename)

    utm.download_french_metro_charts(fixed_url_path, folder)


# Download button
btn_download = Button(window, text="Download", 
                      command=lambda: aux_func(fixed_url_path, folder))



btn_download.grid(row = 3, column = 2, padx=5, pady=5)

window.mainloop()

# Download, create and compress folder
# folder = inp_browser_folder.get()
print(folder)
airport_in = utm.read_airport_file(folder)
if airport_in != -1:
    utm.download_airport_in_file(folder, airport_in, filename)
    os._exit(1)
fixed_url_path = utm.fixed_french_metro_download_url(filename)
utm.download_french_metro_charts(fixed_url_path, "AIRAC " + eAIP_name_string)

fixed_url_path = utm.fixed_french_reunion_download_url(filename)
utm.download_french_reunion_charts(fixed_url_path, "AIRAC " + eAIP_name_string)
utm.write_airport_file(folder)

