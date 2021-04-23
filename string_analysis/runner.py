from . import generateTermFiles
from . import term_cloud
from . import constants
from . import download_util
import glob
import re
from os import path, getcwd
import sys
from typing import List
import zipfile

def main(args):

    if is_update_flag(args) or not resources_exist():
        run_update()

    if not is_update_flag(args):
        run_main(args)

def is_update_flag(args):
    try:
        return args[1] == "-u"
    except IndexError:
        return False

def resources_exist():
    return path.exists(constants.OBO_FILELOCATION) and path.exists(constants.GAF_FILELOCATION)

def run_update():
    print("Updating resources")
    print("Downloading obo file...")
    download_util.download_file(constants.URL_OBO, constants.OBO_FILELOCATION)
    print("Downloading gaf file...")
    download_util.download_file(constants.URL_GAF, constants.GAF_ZIP_FILE, ftp=True)
    print("Unzipping gaf file...")
    download_util.unzip(constants.GAF_ZIP_FILE, constants.GAF_FILELOCATION)

def run_main(args):
    try:
        filenames = get_filenames(args)
        background = get_background(args)
        generateTermFiles.generate(
            filenames,
            constants.OBO_FILELOCATION,
            constants.GAF_FILELOCATION,
            background,
            constants.TEXTFILE_FOLDER)
        term_cloud.generate(get_termfilenames(),constants.COLORS, generate_outdir())
    except ValueError as e:
        print(str(e))

def get_termfilenames() -> List[str]:
    return glob.glob(path.join(constants.TEXTFILE_FOLDER,"*.txt"))

def generate_outdir():
    return path.join(getcwd(), "images")

def get_background(args) -> List[str]:
    try:
        user_input = args[2]
        with open(user_input, "r") as f:
            background = [l.strip() for l in f.readlines()]
        verify_background(background)
        return background
        
    except IndexError:
        raise ValueError("Please include a text file containing a line seperated list of Accession Numbers")
        
    except FileNotFoundError:
        raise  ValueError(f"The file {user_input} was not found")
    
def verify_background(background:List[str]):
    for i, line in enumerate(background):
        if len(line.split()) > 1:
            raise ValueError(f"Background file may only contain Accession Numbers. {line} (line {i})did not match this pattern")

def get_filenames(args):
    try:
        user_input = args[1]
    except IndexError:
        raise ValueError ("Please include a file or directory containing the csv files to process")

    if path.isdir(user_input):
        filenames = glob.glob(path.join(user_input, "*.csv"))
    elif path.isfile(user_input):
        if ".csv" not in user_input:
            raise ValueError("Input must be a directory or a .csv file")
        filenames = [user_input]
    else:
        raise  ValueError(f"The file or directory '{user_input}' does not exist")
    
    return filenames

    
