import requests
import wget
import zipfile
import subprocess
import shutil
import os
from bs4 import BeautifulSoup

root = os.path.dirname(os.path.abspath(__file__))

# Merge Track files
def mergeTracks(cuePath):
    return

# Convert CUE files to VCD
def convertVCD(cuePath, attempt = 1):
        
    if attempt == 1:
        print(f'[SETUP] Starting VCD conversion process ({cuePath})...')
    elif attempt != 3:
        print(f'[SETUP] Restarting conversion process ({cuePath})...')
    else:
        print('[SETUP] 2 conversion attempts failed. Skipping CUE file...')
        return

    # Converting CUE file to VCD
    cmd = subprocess.Popen(f'cmd /k {root}\\tool\\CUE2POPS\\CUE2POPS.EXE "{cuePath}"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = cmd.communicate()

    # Treatment for Multi-Track CUE file
    if str(out).find('splitted dumps') != -1:
        print('[SETUP] Multi-Track file detected! Starting merging process...')
        mergeTracks(cuePath)
        attempt += 1
        convertVCD(cuePath, attempt)
        return    
    
    print('[SETUP] Conversion process complete!')

# Download POPStarter package according to setup type (usb, smb, hdd)
def get_popstarter(setup_type):

    # Check if POPStarter Quickstarter package is already downloaded
    if os.path.exists(f'{root}\\POPStarter_Quickstarter'):
        print('[SETUP] POPStarter_Quickstarter folder found! Skipping download process...')
        return

    # Get most recent POPStarter package link
    print('[SETUP] Getting newest Quickstarter Packages...')
    html = requests.get('https://bitbucket.org/ShaolinAssassin/popstarter-documentation-stuff/downloads').content.splitlines()
    for line in html:
        if str(line).find('Quickstarter_Pack') != -1:
            if str(line).find('USB') != -1:
                usb_file = str(line)[str(line).find('.zip') + 6:str(line).find('</a>', str(line).find('.zip'))]
                print(f'[SETUP] USB Package found: {usb_file}')
            if str(line).find('SMB') != -1:
                smb_file = str(line)[str(line).find('.zip') + 6:str(line).find('</a>', str(line).find('.zip'))]
                print(f'[SETUP] SMB Package found: {smb_file}')
            if str(line).find('HDD') != -1:
                hdd_file = str(line)[str(line).find('.zip') + 6:str(line).find('</a>', str(line).find('.zip'))]
                print(f'[SETUP] HDD Package found: {hdd_file}')

    # Download and extract POPStarter package
    print(f'[SETUP] Downloading {str(setup_type).upper()} Quickstarter Package...')
    if setup_type == 'usb':
        wget.download(f'https://bitbucket.org/ShaolinAssassin/popstarter-documentation-stuff/downloads/{usb_file}')
        print(f'\n[SETUP] Download complete!')
        print(f'[SETUP] Extracting {usb_file}...')
        with zipfile.ZipFile(usb_file, 'r') as zip_ref:
            zip_ref.extractall(root)
        os.remove(usb_file)
        file = usb_file.replace('.zip', '')
    if setup_type == 'smb':
        wget.download(f'https://bitbucket.org/ShaolinAssassin/popstarter-documentation-stuff/downloads/{smb_file}')
        print(f'\n[SETUP] Download complete!')
        print(f'[SETUP] Extracting {smb_file}...')
        with zipfile.ZipFile(smb_file, 'r') as zip_ref:
            zip_ref.extractall(root)
        os.remove(smb_file)
        file = smb_file.replace('.zip', '')
    if setup_type == 'hdd':
        wget.download(f'https://bitbucket.org/ShaolinAssassin/popstarter-documentation-stuff/downloads/{hdd_file}')
        print(f'\n[SETUP] Download complete!')
        print(f'[SETUP] Extracting {hdd_file}...')
        with zipfile.ZipFile(hdd_file, 'r') as zip_ref:
            zip_ref.extractall(root)
        os.remove(hdd_file)
        file = hdd_file.replace('.zip', '')    
    os.rename(f'{root}\\{file}', f'{root}\\POPStarter_Quickstarter')    
    print(f'[SETUP] Extraction complete!')

# Create "POPS" folder and put all files there ("POPS_IOX.PAK", VCD files and POPStarter ELFs for each VCD files)
def create_popsFolder(popsIox_path, games: list):

    # Check if "POPS" folder is already created
    if os.path.exists(f'{root}\\POPS'):        
        print('[SETUP] POPS folder found! Skipping download process...')
        return

    # Create POPS folder and move "POPS_IOX" to it        
    os.makedirs(f'{root}\\POPS')
    shutil.copy(f'{root}\\POPS_IOX.PAK', f'{root}\\POPS\\POPS_IOX.PAK')

    # Move games to "POPS" folder and create a POPStarter ELF for each one
    for game in games:
        if str(game).find('.cue'):
            convertVCD(game)
