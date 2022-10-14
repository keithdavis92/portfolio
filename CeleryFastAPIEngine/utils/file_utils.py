import glob
import os

from constants import TEMP_FILES_FOLDER


def clean_temp_files():
    files = glob.glob(f"{TEMP_FILES_FOLDER}/*")
    for f in files:
        os.remove(f)
