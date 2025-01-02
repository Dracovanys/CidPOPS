# Build import sys
import requests
import wget
import zipfile
import shutil
import os
import src.tool as tool
from bs4 import BeautifulSoup

root = os.path.dirname(os.path.abspath(__file__)).replace('\\src', '')
# Build root = os.path.dirname(os.path.abspath(sys.argv[0].replace('\\CidPOPS.exe', '')))

# Create "conf_apps" with all paths requested
def opl_setup(ps1_pfx: bool = True, setupType = 'usb'):

    # Check if setup folder exists
    if setupType == 'usb':
        setupFolder = f'{root}\\USB'
    if setupType == 'smb':
        setupFolder = f'{root}\\SMB'
    if setupType == 'hdd':
        setupFolder = f'{root}\\HDD'

    if not os.path.exists(setupFolder):
        print(f'[SETUP] Setup folder ({setupFolder}) not found!')
        return

    if os.path.exists(f'{setupFolder}\\conf_apps.cfg'):
        os.remove(f'{setupFolder}\\conf_apps.cfg')

    gameElfs = []
    for file in os.listdir(f'{setupFolder}\\POPS'):
        if str(file).find(".ELF") != -1:
            gameElfs.append(file)
    
    print('[SETUP] Creating "conf_apps.cfg" file...')
    for game in gameElfs:
        shortcutName = str(game).replace('XX.', '').replace('.ELF', '')
        if ps1_pfx:
            shortcutName = f'PS1 - {shortcutName}'
        with open(f'{setupFolder}\\conf_apps.cfg', 'a') as file:
            if setupType == 'usb':
                file.write(f'{shortcutName}=mass:/POPS/{game}\n')
            if setupType == 'hdd':
                file.write(f'{shortcutName}=hdd:/POPS/{game}\n')
            if setupType == 'smb':
                file.write(f'{shortcutName}=smb:/POPS/{game}\n')
    return

# Download POPStarter package according to setup type (usb, smb, hdd)
def get_popstarter(setupType = 'usb'):

    # Check if setup folder exists
    if setupType == 'usb':
        setupFolder = f'{root}\\USB'
    if setupType == 'smb':
        setupFolder = f'{root}\\SMB'
    if setupType == 'hdd':
        setupFolder = f'{root}\\HDD'
    if not os.path.exists(setupFolder):        
        print('[SETUP] Creating setup folder...')
        os.makedirs(setupFolder)

    # Check if POPStarter Quickstarter package is already downloaded
    if os.path.exists(f'{setupFolder}\\POPStarter_Quickstarter'):
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
    print(f'[SETUP] Downloading {str(setupType).upper()} Quickstarter Package...')
    if setupType == 'usb':
        wget.download(f'https://bitbucket.org/ShaolinAssassin/popstarter-documentation-stuff/downloads/{usb_file}')
        print(f'\n[SETUP] Download complete!')
        print(f'[SETUP] Extracting {usb_file}...')
        with zipfile.ZipFile(usb_file, 'r') as zip_ref:
            zip_ref.extractall(setupFolder)
        os.remove(usb_file)
        file = usb_file.replace('.zip', '')
    if setupType == 'smb':
        wget.download(f'https://bitbucket.org/ShaolinAssassin/popstarter-documentation-stuff/downloads/{smb_file}')
        print(f'\n[SETUP] Download complete!')
        print(f'[SETUP] Extracting {smb_file}...')
        with zipfile.ZipFile(smb_file, 'r') as zip_ref:
            zip_ref.extractall(setupFolder)
        os.remove(smb_file)
        file = smb_file.replace('.zip', '')
    if setupType == 'hdd':
        wget.download(f'https://bitbucket.org/ShaolinAssassin/popstarter-documentation-stuff/downloads/{hdd_file}')
        print(f'\n[SETUP] Download complete!')
        print(f'[SETUP] Extracting {hdd_file}...')
        with zipfile.ZipFile(hdd_file, 'r') as zip_ref:
            zip_ref.extractall(setupFolder)
        os.remove(hdd_file)
        file = hdd_file.replace('.zip', '')    
    os.rename(f'{setupFolder}\\{file}', f'{setupFolder}\\POPStarter_Quickstarter')    
    print(f'[SETUP] Extraction complete!')

# Create "POPS" folder and put all files there ("POPS_IOX.PAK", VCD files and POPStarter ELFs for each VCD files)
def create_popsFolder(popsIox_path, games, setupType = 'usb'):

    # Check if setup folder exists
    if setupType == 'usb':
        setupFolder = f'{root}\\USB'
    if setupType == 'smb':
        setupFolder = f'{root}\\SMB'
    if setupType == 'hdd':
        setupFolder = f'{root}\\HDD'
    if not os.path.exists(setupFolder):
        print('[SETUP] Creating setup folder...')
        os.makedirs(setupFolder)

    # Check if "POPS" folder is already created
    if os.path.exists(f'{setupFolder}\\POPS'):        
        print('[SETUP] POPS folder found! Please, delete it to continue.')
        return

    # Create POPS folder and move "POPS_IOX" to it
    print('[SETUP] Creating POPS folder...')
    os.makedirs(f'{setupFolder}\\POPS')

    if os.path.exists(popsIox_path):
        shutil.copy(popsIox_path, f'{setupFolder}\\POPS\\POPS_IOX.PAK')
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
            gamePath = tool.convert_VCD(gamePath)
            game_name = game_name.replace('.cue', '.VCD')
            print('[SETUP] Resuming copying process...')
        shutil.copy(gamePath, f'{setupFolder}\\POPS\\{game_name}')
        print(f'[SETUP] Game copied!')
        print(f'[SETUP] Creating POPStarter ELF file...')
        shutil.copy(f'{setupFolder}\\POPStarter_Quickstarter\\POPSTARTER.ELF', f'{setupFolder}\\POPS\\XX.{game_name.replace('.VCD', '')}.ELF')            
        print(f'[SETUP] POPStarter ELF file created!')
