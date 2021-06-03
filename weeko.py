import argparse
import os
import logging
import shutil
import hashlib
import sys
import time
from sys import exit
from datetime import date
from colorama import Fore
from tqdm import tqdm
from pydub import AudioSegment 
from pydub.playback import play 


def detect_sepator():
    file_separator = "/"
    if os.name == "nt":
        file_separator = "\\"
    return file_separator


def backup(path_to_copy, excluded_extension, verbose, log_path):

    file_separator = detect_sepator()
    create_log(log_path)
    log_config(log_path)
    weekday_folder = day_of_the_week()
    check_folder(weekday_folder)
    
    list_excluded_extensions = []
    # This if is written because , if it is written default="" in the argparse argument it excludes files without extension by default
    if excluded_extension is not None: 
        list_excluded_extensions = excluded_extension.split(",")
    set_excluded_extensions = {"." + value.strip() if len(value.strip()) > 0 else value.strip() for value in list_excluded_extensions} # This set add the character . to the extensions excludes if is not empty
    
    try:
        print(f"{Fore.YELLOW}") 
        for file in tqdm(os.listdir(path_to_copy)):
            time.sleep(0.25)
            _ , ext = os.path.splitext(file)

            path_file_source = path_to_copy + file_separator + file
            path_file_dest = weekday_folder + file_separator + file

            if os.path.isfile(path_file_source) and ext not in set_excluded_extensions:
                shutil.copyfile(path_file_source, path_file_dest)

                hash_md5 = hash_file(path_file_source)

                logging.debug(f"copy of file: {path_file_source} with MD5: {hash_md5} created in: {weekday_folder}")

                if verbose:
                    print(f"{Fore.RED}File: {Fore.YELLOW}{path_file_source} {Fore.RED}MD5: {Fore.YELLOW}{hash_md5}")
                
    except KeyboardInterrupt:
        print(f"{Fore.MAGENTA}Backup {Fore.RED}NOT {Fore.MAGENTA}completed")
        print(Fore.RESET) 

    else:          
        print(f"{Fore.MAGENTA}Backup Completed")
        print(Fore.RESET)

        try:
            wav_file = AudioSegment.from_file(file = "tone.wav", format = "wav")[0:5000] # play from 0 to 5 sec
            play(wav_file)

        except KeyboardInterrupt:
            pass
                
   
def check_folder(folder):
    try:
        os.stat(folder)
    except IOError:
        os.mkdir(folder)
        logging.debug(f"Folder {folder} created")
            

def hash_file(path_file):
    file_hash = hashlib.md5() 
    with open(path_file, 'rb') as f: 
        data = f.read(2048) 
        while len(data) > 0: 
            file_hash.update(data) 
            data = f.read(2048) 
    return file_hash.hexdigest()


def create_log(file):
    dirlog = os.path.dirname(file)
    if len(dirlog) == 0:
        dirlog = "./"  

    try:
        os.stat(dirlog)

    except IOError:
        print("The folder of the log does not exit")
        sys.exit()
    
    try:
        open(file, 'a').close()

    except IOError:
        print("Failed open the log, the log does not have name")
        sys.exit()


def log_config(file):
    logging.basicConfig(
    filename=file,
    level=logging.DEBUG,
    format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S',)


def day_of_the_week():
    weekDays = ("lunes","martes","miercoles","jueves","viernes","sabado","domingo")
    day_number = date.today().weekday()
    return weekDays[day_number]


def check_path(path_folder):
    try:
        while os.path.isdir(path_folder) == False:
            path_folder = input("The insert path can not be located, write a correct path:\n")
        return path_folder

    except KeyboardInterrupt:
        sys.exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="folder path to copy")
    parser.add_argument("-e", "--exclude", help="exclude extensions of files using the format. \
                        Extensions must write without dot and separate with commas. \
                        If you want exclude no extensions files write empty strings. \
                        Examples --exclude=\"\" -e=\"py,\" --exclude , -e txt,")
    parser.add_argument("-v", "--verbose", 
                        help="shows the names of the copied files and the hashes", 
                        action="store_true")
    parser.add_argument("-l", "--logfile", help="change path log", default="weeko.log")
                        
    options = parser.parse_args()
    path_folder = check_path(options.path)
    backup(path_folder, options.exclude, options.verbose, options.logfile)


if __name__ == "__main__":
    main()   
