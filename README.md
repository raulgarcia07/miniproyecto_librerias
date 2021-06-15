# SCRIPT BACKUP 

The weeko.py file allows you to copy a folder and save the files in a new folder that is created in the path where the script is executed and named according to the day of the week.

It is recommended to create and use a virtual environment:
```
python -m venv .venv 
or
python3 m venv .venv 

```
To use the virtual enviroment:
```
source .venv/bin/activate for Linux

\path\to\env\Scripts\activate for Windows
```

Install the libraries:
``` 
colorama
tqdm
pydub
```
or you can use:

```
pip install -r requirements.txt 

```

## HOW THE SCRIPT WORKS:

The script creates a copy of the files in the path that is written. The program will create the folder that corresponds to the day of the week and a log file if they are not created. All records will be saved in the log file.
During the copying process a progress bar is displayed and when copying is finished it will sound a tone.

To execute the script use:
```
python weeko.py "folder to copy" "optional arguments"

Example: python weeko.py images --verbose

```

The optional arguments are:

1. `-e` or `--exclude` : Exclude extensions files ,without dots and separate with commas, that that will not be copied. Example: --exclude txt,png .

2. `-v` or `--verbose` : Show files names and their hashes when are copied

3. `-l` or `--logfile` : By default the logfile is named weeko.log .With this option you can change the name and the path of the logfile. Example: -l ../logbackup.log

4. `-s` or `--subfolder`: Also copy the subfolders







