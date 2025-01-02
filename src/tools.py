import os
import subprocess

root = os.path.dirname(os.path.abspath(__file__)).replace('\\src', '')

# Merge Track files
def merge_tracks(cuePath):
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
def convert_VCD(cuePath, attempt = 1):
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
        cuePath = merge_tracks(cuePath)
        attempt += 1
        return convert_VCD(cuePath, attempt)
    
    print('[SETUP] Conversion process complete!')
    return cuePath.replace('.cue', '.VCD')
