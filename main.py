import sys
import os
import argparse
from src import setup
# Build from src import setup_toBuild as setup
from src import tool

root = os.path.dirname(os.path.abspath(__file__))
# Build root = os.path.dirname(os.path.abspath(sys.argv[0].replace('\\CidPOPS.exe', '')))

# Setting up arguments
parser = argparse.ArgumentParser(description='A tool for setup your POPS! || By Dracovanys || Credits: israpps/ErikAndren (CUE2POPS); putnam/cgarz (binmerge); krHACKen/shaolinassassin (POPStarter)')
# parser.add_argument('setup_type', help='Specify setup type (usb, smb, hdd).')
parser.add_argument('games_dir', nargs='?', help='Directory where all your PS1 games are stored.')
parser.add_argument('pops_iox', nargs='?', help='Path to "POPS_IOX.PAK" if not on CidPOPS directory.')
parser.add_argument('-c', '--convertVCD', nargs='?', help='Convert a CUE file to VCD. (Usage.: -c "D:\\Downloads\\Crash Bandicoot (USA)\\Crash Bandicoot (USA).cue")')
parser.add_argument('-m', '--mergeTracks', nargs='?', help='Merge tracks and generate a new CUE file. (Usage.: -m "D:\\Downloads\\Crash Bandicoot (USA)\\Crash Bandicoot (USA).cue")')
parser.add_argument('--opl', action='store_true', help='Just create "conf_apps.cfg" file.')
parser.add_argument('--ps1_pfx', action='store_true', help='Add "PS1 - " prefix to all OPL shortcuts on "conf_apps.cfg" file (Ex.: "PS1 - Crash Bandicoot (USA)").')
args = parser.parse_args()

# Convert VCD
if args.convertVCD != None:
    tool.convert_VCD(args.convertVCD)
    sys.exit()

# Merge Tracks
if args.mergeTracks != None:
    tool.merge_tracks(args.mergeTracks)
    sys.exit()

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
    if args.ps1_pfx:
        setup.opl_setup()
    else:
        setup.opl_setup(ps1_pfx=False)
    sys.exit()