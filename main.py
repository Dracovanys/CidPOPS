import os
import argparse
from src import setup
from src import tool

root = os.path.dirname(os.path.abspath(__file__))

# Setting up arguments
parser = argparse.ArgumentParser(description='A tool for setup your POPS.')
# parser.add_argument('setup_type', help='Specify setup type (usb, smb, hdd).')
parser.add_argument('games_dir', nargs='?', help='Directory where all PS1 games are stored.')
parser.add_argument('pops_iox', nargs='?', help='Path to "POPS_IOX.PAK" if not on CidPOPS directory.')
parser.add_argument('-c', '--convertVCD', nargs='?', help='Convert a CUE file to VCD. (Usage.: -c "D:\\Downloads\\Crash Bandicoot (USA)\\Crash Bandicoot (USA).cue")')
parser.add_argument('-m', '--mergeTracks', nargs='?', help='Merge Tracks and generate a new CUE file. (Usage.: -m "D:\\Downloads\\Crash Bandicoot (USA)\\Crash Bandicoot (USA).cue")')
parser.add_argument('--opl', action='store_true', help='Just create "conf_apps.cfg" file.')
parser.add_argument('--ps1_pfx', action='store_true', help='Add "PS1 - " prefix to all OPL shortcuts on "conf_apps.cfg" file (Ex.: "PS1 - Crash Bandicoot (USA)").')
args = parser.parse_args()

# Convert VCD
if args.convertVCD != None:
    tool.convert_VCD(args.convertVCD)
    exit()

# Merge Tracks
if args.mergeTracks != None:
    tool.merge_tracks(args.mergeTracks)
    exit()

create_confApps = False
if args.games_dir != None:
    setup.get_popstarter()

    if args.pops_iox != None:
        setup.create_popsFolder(args.pops_iox, args.games_dir)
    else:
        setup.create_popsFolder(f'{root}\\POPS_IOX.PAK', args.games_dir)
    create_confApps = True

# Create "conf_apps.cfg"
if args.opl or create_confApps == True:
    gameElfs = []
    for file in os.listdir(f'{root}\\USB\\POPS'):
        if str(file).find(".ELF") != -1:
            gameElfs.append(file)
    if args.ps1_pfx:
        setup.opl_setup(gameElfs)
    else:
        setup.opl_setup(gameElfs, ps1_pfx=False)
    exit()