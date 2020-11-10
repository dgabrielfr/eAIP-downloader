import tkinter as tk

import pandas as pd
import tkinter as tk
from tkinter import ttk
import datetime
import urllib
import urllib.request
import shutil
import os.path
import re
from string import ascii_uppercase
from os import listdir

import os

from tkinter.filedialog import *

def searchfile():
    if os.path.isfile("airac_date.txt"):
        update("airac_date.txt")
        btn_browser.config(state = "disable")
        btn_browser['text'] = "File found!"
        btn_download.config(state = "normal")
        btn_download.config(bg = "green")
        btn_download.config(fg = "white")

def update(filename):
    path_to_AIRAC.set(filename)
    label_AIRAC_name['text'] = "AIRAC name: " + latest_valid_AIRAC_name(filename)
    label_AIRAC_date['text'] = "AIRAC date: " + latest_valid_AIRAC_date_formated(filename)

def openBrowser():
    filename = askopenfilename(title="Open airac.txt file", 
                               filetypes=[('text file', '.txt'), ('all files', '.*')])
    if filename != "":
        update(filename)
        btn_download.config(state = "normal")
        btn_download.config(bg = "green")
        btn_download.config(fg = "white")

def latest_valid_AIRAC_name(path_to_airac_date):
    """
    Return the latest AIRAC name (ex: 2009) as string

    Args:
        path_to_airac_date (string): The path to the airac_date.txt file

    Returns:
        string: The latest AIRAC name with 4 digits (ex: 2009)
    """
    if path_to_airac_date == "":
        return(-1)
    today = datetime.date.today()
    name_series = pd.read_csv(path_to_airac_date, sep='\t', usecols=[1], header=None)
    df = pd.read_csv(path_to_airac_date, sep='\t', usecols=[4], header=None)
    date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date
    date_mask = (date_series <= today)
    eAIP_name = name_series[date_mask].max()
    return(str(eAIP_name[1]))

def latest_valid_AIRAC_date_formated(path_to_airac_date):
    """
    Return the latest AIRAC date (ex: 13 AUG 20) as string

    Args:
        path_to_airac_date (string): The path to the airac_date.txt

    Returns:
        string: The latest AIRAC date in the "%d_%b_%Y" format (ex: 13 AUG 20)
    """
    today = datetime.date.today()
    if (path_to_airac_date != ""):
        df = pd.read_csv(path_to_airac_date, sep='\t', usecols=[4], header=None)
        date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date
        date_mask = (date_series <= today)
        eAIP_date = date_series[date_mask].max()
        eAIP_date_string = str(eAIP_date.strftime("%d_%b_%Y")).upper()
        return(eAIP_date_string)
    else:
        print("Error, string should not be void!")
        return("")
    
def latest_valid_AIRAC_date(filename):
    if filename == "":
        return(-1)
    today = datetime.date.today()
    df = pd.read_csv(filename, sep='\t', usecols=[4], header=None)
    date_series = pd.to_datetime(df[4], format='%d %b %y').dt.date
    date_mask = (date_series <= today)
    eAIP_date = str(date_series[date_mask].max())
    return(eAIP_date)   


def download(filename):
    """
    Return the fixed part of the French Metropolitan eAIP url download
    example: https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_16_JUL_2020/FRANCE/AIRAC-2020-07-16/pdf/FR-AD-2.LFBA-fr-FR.pdf

    Args:
        filename (string): the path to the airac_date.txt file

    Return:
          String: fixed part of the French Metropolitan eAIP url download 

    """
    download_french_metro_charts(filename, "https://www.sia.aviation-civile.gouv.fr/dvd/eAIP_" + str(latest_valid_AIRAC_date_formated(filename)) + "/FRANCE/AIRAC-" + str(latest_valid_AIRAC_date(filename)) + "/pdf/FR-AD-2.LF")

def download_french_metro_charts(filename, fixed_path):
    """
    1/ Download the French Metropolitan charts in PDF form

    Args:
        filename (string): the path to the airac_date.txt
        fixed_path (string): the fixed part of the download path
    """

    # Download the charts in PDF
    for c1 in ascii_uppercase:
        for c2 in ascii_uppercase:
            # pgb_download.step()
            # window.update()
            full_path = fixed_path + c1 + c2 + "-fr-FR.pdf"
            # Check if the PDF file exists
            if os.path.isfile("LF" + c1 + c2 + "-eAIP-" + latest_valid_AIRAC_name(filename) + ".pdf"):
                print("LF" + c1 + c2 + "-eAIP-" + latest_valid_AIRAC_name(filename) + ".pdf" + " Already exists, skipping!")
                continue
            try:
                urllib.request.urlretrieve(full_path, "LF" + c1 + c2 + "-eAIP-" + latest_valid_AIRAC_name(filename) + ".pdf")
            except urllib.error.HTTPError as e:
                print("LF" + c1 + c2 + " download error: " + str(e))

def dl(folder):
    print("The download folder is set to: " + folder)

window = tk.Tk()
window.geometry("500x200")
window.title = "eAIP downloader GUI prototype"

path_to_AIRAC = tk.StringVar()
path_to_Folder = tk.StringVar()

label_browser = tk.Label(window, text="Browse to AIRAC_date.txt: ", width = 30)
label_browser.grid(row = 1, column = 1, padx = 5, pady = 5)

btn_browser = tk.Button(window, text = "Browse", width = 30, command = openBrowser)
btn_browser.grid(row = 1, column = 2, padx = 5, pady = 5)

label_folder = tk.Label(window, text="Enter the folder path :", width = 30)
label_folder.grid(row = 2, column = 1, padx = 5, pady = 5)
ent_folder = tk.Entry(window, width = 30)
ent_folder.grid(row = 2, column = 2, padx = 5, pady = 5)
# pgb_download = ttk.Progressbar(window, length = 200, maximum = 676, cursor='spider', mode = "determinate", orient=tk.HORIZONTAL)
# pgb_download.grid(row = 3, column = 1, padx = 5, pady = 5) 
btn_download = tk.Button(window, text="Download", width = 30, command = lambda: download(path_to_AIRAC.get()))
btn_download.config(state="disabled")
btn_download.grid(row = 3, column = 2, padx = 5, pady = 5)

frame = tk.LabelFrame(window, text="Airac Informations: ")
frame.grid(row = 4, column = 0, columnspan=3, padx=5, pady = 5)
label_AIRAC_name = tk.Label(frame)
label_AIRAC_name.pack()
label_AIRAC_date = tk.Label(frame)
label_AIRAC_date.pack()

searchfile()

window.mainloop()