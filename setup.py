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
    binmerge = f'{root}\\tool\\binmerge.exe'

    print('[SETUP] Starting merging process...')
    filename = cuePath[cuePath.rfind('\\') + 1:].replace('.cue', '')
    mergedPath = f'{cuePath[:cuePath.rfind('\\')]}\\{filename}_Merged'
    if not os.path.exists(mergedPath):
        os.makedirs(mergedPath)
    os.system(f'{binmerge} -o "{mergedPath}" "{cuePath}" "{filename}"')
    print('[SETUP] Merge complete!')
    return f'{mergedPath}\\{filename}.cue'

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
        cuePath = mergeTracks(cuePath)
        attempt += 1
        return convertVCD(cuePath, attempt)
    
    print('[SETUP] Conversion process complete!')
    return cuePath.replace('.cue', '.VCD')

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
def create_popsFolder(popsIox_path, games):

    # Check if "POPS" folder is already created
    if os.path.exists(f'{root}\\POPS'):        
        print('[SETUP] POPS folder found! Please, delete it to continue.')
        return

    # Create POPS folder and move "POPS_IOX" to it
    print('[SETUP] Creating POPS folder...')
    os.makedirs(f'{root}\\POPS')

    if os.path.exists(f'{root}\\POPS_IOX.PAK'):
        shutil.copy(f'{root}\\POPS_IOX.PAK', f'{root}\\POPS\\POPS_IOX.PAK')
    else:
        print('[SETUP] "POPS_IOX.PAK" not detected! Please put "POPS_IOX.PAK" file on the root of CidPOPS folder.')
        return

    # Move games to "POPS" folder and create a POPStarter ELF for each one
    print('[SETUP] Moving games to "POPS" folder...')
    if type(games) == str:
        _games = []
        for file in os.listdir(games):
            if str(file.lower()).find('.cue') != -1 or str(file.lower()).find('.vcd') != -1:
                _games.append(f'{games}\\{file}')
        games = _games
    for gamePath in games:
        game_name = gamePath[gamePath.rfind('\\') + 1:]
        print(f'[SETUP] Moving "{game_name}" to "POPS" folder...')
        if str(gamePath).find('.cue') != -1:
            gamePath = convertVCD(gamePath)
            game_name = game_name.replace('.cue', '.VCD')
            print('[SETUP] Resuming copying process...')
        shutil.copy(gamePath, f'{root}\\POPS\\{game_name}')
        print(f'[SETUP] Game copied!')
        print(f'[SETUP] Creating POPStarter ELF file...')
        shutil.copy(f'{root}\\POPStarter_Quickstarter\\POPSTARTER.ELF', f'{root}\\POPS\\XX.{game_name.replace('.VCD', '')}.ELF')            
        print(f'[SETUP] POPStarter ELF file created!')
