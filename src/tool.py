import os
import subprocess

root = os.path.dirname(os.path.abspath(__file__)).replace('\\src', '')

# Merge Track files
def merge_tracks(cuePath):
    binmerge = f'{root}\\util\\binmerge.exe'

    print('[TOOL] Starting merging process...')
    filename = cuePath[cuePath.rfind('\\') + 1:].replace('.cue', '')
    mergedPath = f'{cuePath[:cuePath.rfind('\\')]}\\{filename}_Merged'
    if not os.path.exists(mergedPath):
        os.makedirs(mergedPath)
    os.system(f'{binmerge} -o "{mergedPath}" "{cuePath}" "{filename}"')
    print('[TOOL] Merge complete!')
    return f'{mergedPath}\\{filename}.cue'

# Convert CUE files to VCD
def convert_VCD(cuePath, attempt = 1):
    if attempt == 1:
        print(f'[TOOL] Starting VCD conversion process ({cuePath})...')
    elif attempt != 3:
        print(f'[TOOL] Restarting conversion process ({cuePath})...')
    else:
        print('[TOOL] 2 conversion attempts failed. Skipping CUE file...')
        return

    # Converting CUE file to VCD
    cmd = subprocess.Popen(f'cmd /k {root}\\util\\CUE2POPS\\CUE2POPS.EXE "{cuePath}"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = cmd.communicate()
    
    if str(out).find('Cannot open') != -1:
        print(f'[TOOL][ERROR] There is some problem with CUE file and its BINs, please check it! Skipping game...')
        return 'ERROR'

    # Treatment for Multi-Track CUE file
    if str(out).find('splitted dumps') != -1:
        print('[TOOL] Multi-Track file detected! Starting merging process...')
        cuePath = merge_tracks(cuePath)
        attempt += 1
        return convert_VCD(cuePath, attempt)
    
    print('[TOOL] Conversion process complete!')
    return cuePath.replace('.cue', '.VCD')

# Get MD5 hash from a file
def get_md5(filePath):
    return str(subprocess.run(f'certutil -hashfile "{filePath}" MD5', capture_output=True)).split('\\r\\n')[1]