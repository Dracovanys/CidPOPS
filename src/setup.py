# Build import sys
import requests
import wget
import zipfile
import shutil
from difflib import SequenceMatcher
import os
from bs4 import BeautifulSoup

if __name__ == "__main__":
    import tool
else:
    import src.tool as tool

class POP():
    def __init__(self, name, vcd_md5, cue_md5):
        self.name = name
        self.vcd_md5 = vcd_md5
        self.cue_md5 = cue_md5
    
    def __str__(self):
        return f'[Name: {self.name} | VCD_MD5: {self.vcd_md5} | CUE_MD5: {self.cue_md5}]'

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
            shortcutName = f'PS1_{shortcutName}'
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

# Return a list of all VCD files (with its MD5 hashes) already setup on POPS folder
def get_pops(pops_folder):

    # Get/Create "pops.cid" file
    pops = []
    if not os.path.exists(f'{pops_folder}\\pops.cid'):
        print('[SETUP] "pops.cid" file not found! Creating it...')

        # Get all VCD files on folder
        vcd_files = []
        for file in os.listdir(pops_folder):
            if str(file).find('.VCD') != -1:
                vcd_files.append(str(file))
        
        # Get MD5 hash from file and create "pops.cid" file
        for file in vcd_files:
            pop = POP(file, tool.get_md5(f'{pops_folder}\\{file}'),'None')
            pops.append(pop)
        
        with open(f'{pops_folder}\\pops.cid', 'w') as file:
            for pop in pops:
                file.write(f'{pop.name}, {pop.vcd_md5}, {pop.cue_md5}\n')
                print(f'[SETUP] Game found: {pop.name}')
        print(f'[SETUP] "pops.cid" created.')
    else:        
        print('[SETUP] "pops.cid" file found! Getting games...')
        with open(f'{pops_folder}\\pops.cid', 'r') as file:
            for line in file.readlines():
                _line = line.split(', ')
                pop = POP(_line[0], _line[1], _line[2].replace('\n', ''))
                print(f'[SETUP] Game found: {pop.name}')
                pops.append(pop)
    print('[SETUP] POPS folder loaded.')
    return pops

# Create "DISCS.TXT" and VMCDIR.TXT for multi-disc games
def multiDisc_setup(pops_folder):
    print('[SETUP] Looking for multi-disc games...')

    # Get all games with "Disc" tag
    games = []
    for file in os.listdir(pops_folder):
        if file.find('Disc') != -1 and file.find('.VCD') != -1:
            games.append(file)
    if len(games) > 1:
        print(f'[SETUP] {len(games)} multi-disc games found!')
    else:
        print(f'[SETUP] Less than 2 multi-disc games found. Skipping process...')
        return

    # Group each disc
    games_discs = []
    for game_main in games:
        discs = [game_main]
        for game_compare in games:
            if game_compare == game_main:
                continue
            if SequenceMatcher(None, game_main, game_compare).ratio() * 100 >= 95.0:
                discs.append(game_compare)
                games.remove(game_compare)
        discs.sort()
        games_discs.append(discs)
    
    # Create "DISCS.TXT"
    for game in games_discs:
        if len(game) > 4:
            print(f'[SETUP] "{game[0]}" ')
        for disc in game:
            print(f'[SETUP] Creating {disc.replace('.VCD', '').replace('.vcd', '')} folder...')
            if not os.path.exists(f'{pops_folder}\\{disc.replace('.VCD', '').replace('.vcd', '')}'):
                os.makedirs(f'{pops_folder}\\{disc.replace('.VCD', '').replace('.vcd', '')}')
            with open(f'{pops_folder}\\{disc.replace('.VCD', '').replace('.vcd', '')}\\VMCDIR.TXT', 'w') as file:
                file.write(game[0].replace('.VCD', '').replace('.vcd', ''))
            with open(f'{pops_folder}\\{disc.replace('.VCD', '').replace('.vcd', '')}\\DISCS.TXT', 'w') as file:
                for disc in game:
                    file.write(f'{disc}\n')
        
    print('[SETUP] All multi-disc games setup!')

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
    pops = []
    previous_pops_len = 0
    pops_updated = False
    if os.path.exists(f'{setupFolder}\\POPS'):        
        print('[SETUP] POPS folder found! Getting games...')
        pops = get_pops(f'{setupFolder}\\POPS')
        previous_pops_len = len(pops)
    else:
        print('[SETUP] Creating POPS folder...')
        os.makedirs(f'{setupFolder}\\POPS')

    # Move "POPS_IOX" to POPS folder
    if os.path.exists(popsIox_path):
        if not os.path.exists(f'{setupFolder}\\POPS\\POPS_IOX.PAK'):
            shutil.copy(popsIox_path, f'{setupFolder}\\POPS\\POPS_IOX.PAK')
    else:
        print('[SETUP] "POPS_IOX.PAK" not detected! Please put "POPS_IOX.PAK" file on the root of CidPOPS folder.')
        return

    # Move games to "POPS" folder and create a POPStarter ELF for each one
    print('[SETUP] Moving games to "POPS" folder...')
    if type(games) == str:

        # Get all game files inside specified "games" folder
        _games = []
        for file in os.listdir(games):
            if str(file.lower()).find('.cue') != -1 or str(file.lower()).find('.vcd') != -1:
                _games.append(f'{games}\\{file}')
        games = _games
    
    # Convert games to VCD (if necessary) and copy to POPS folder
    for gamePath in games:
        skip_copy = False
        game_name = gamePath[gamePath.rfind('\\') + 1:]
        print(f'[SETUP] Moving "{game_name}" to "POPS" folder...')

        # Get CUE_MD5 if CUE file
        cue_md5 = 'None'
        if gamePath.lower().find('.cue') != -1:
            cue_md5 = tool.get_md5(gamePath)
            for pop in pops:
                if cue_md5 == pop.cue_md5:
                    print(f'[SETUP] Game already present on "POPS" folder! (Same hash as (converted to VCD): "{pop.name}")')
                    skip_copy = True

        # Convert CUE to VCD
        if str(gamePath).find('.cue') != -1 and not skip_copy:
            gamePath = tool.convert_VCD(gamePath)
            if gamePath == 'ERROR':
                continue
            game_name = game_name.replace('.cue', '.VCD')
            print('[SETUP] Resuming move process...')

        # Get VCD_MD5 if CUE file
        if gamePath.lower().find('.vcd') != -1 and not skip_copy:
            vcd_md5 = tool.get_md5(gamePath)
            for pop in pops:
                if vcd_md5 == pop.vcd_md5:
                    print(f'[SETUP] Game already present on "POPS" folder! (Same hash as: "{pop.name}")')
                    pop = POP(game_name, vcd_md5, cue_md5)
                    skip_copy = True
                    pops_updated = True

        if not skip_copy:
            shutil.copy(gamePath, f'{setupFolder}\\POPS\\{game_name}')
            pops.append(POP(game_name, vcd_md5, cue_md5))
            print(f'[SETUP] Game copied!')        

        if not os.path.exists(f'{setupFolder}\\POPS\\XX.{game_name.replace('.VCD', '').replace('.cue', '')}.ELF'):
            shutil.copy(f'{setupFolder}\\POPStarter_Quickstarter\\POPSTARTER.ELF', f'{setupFolder}\\POPS\\XX.{game_name.replace('.VCD', '').replace('.cue', '')}.ELF')            
            print(f'[SETUP] POPStarter ELF file created!')

    # Setting up multi-disc games    
    multiDisc_setup(f'{setupFolder}\\POPS')

    # Create/Update "pops.cid" file
    if os.path.exists(f'{setupFolder}\\POPS\\pops.cid'):
        text = f'[SETUP] "pops.cid" file updated!'
    else:
        text = f'[SETUP] "pops.cid" file created!'
    if pops_updated or (len(pops) > previous_pops_len):
        with open(f'{setupFolder}\\POPS\\pops.cid', 'w') as file:
            for pop in pops:
                file.write(f'{pop.name}, {pop.vcd_md5}, {pop.cue_md5}\n')
            print(text)
