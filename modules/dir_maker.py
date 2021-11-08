import pathlib
from datetime import datetime

"""
This module contains basic functions for creating a dealing with folder creation in the App
"""


# Creates a folder with the current date, to store the invoices it creates
def create_dir():
    today = datetime.today().strftime("%d_%m")
    folder = "Invoices"
    subfolder = f"invoices_{today}"
    final_folder = pathlib.Path.cwd().parent.parent.joinpath(folder, subfolder)
    try:
        final_folder.mkdir(parents=True,exist_ok=False)
    except:
        pass
    return final_folder


# This functions checks if the folder is created
def check_dir():
    today = datetime.today().strftime("%d_%m")
    folder = "Invoices"
    subfolder = f"invoices_{today}"
    final_folder = pathlib.Path.cwd().parent.parent.joinpath(folder, subfolder)
    return final_folder


if __name__ == "__main__":
    create_dir()
