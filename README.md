
# CidPOPS

A tool to set up your POPS! Created based on the quickstart created by ShaolinAssassin, CidPOPS offers the following features:

 - Conversion of CUE files to VCD format (CUE2POPS).
 - Merging of multiple tracks (binmerge).
 - Creation of POPSTARTER files for each VCD.
 - Automatic writting of the "conf_apps.cfg" file for POPS access in OPL.
 - Deep verification of CUE and BIN files to prevent errors.
 - Automated multi-disc setup.

## Usage/Example

Currently, it is only possible to use CidPOPS on Windows OS through a terminal. Additionally, I have only programmed the setup for USB, but in the near future, I will be programming setups for SMB and HDD. Below is the help text for the program:

```
usage: main.py [-h] [-c [CONVERTVCD]] [-m [MERGETRACKS]] [-md5 [GETMD5]] [--opl] [--ps1_pfx] [games_dir] [pops_iox]

A tool to setup your POPS! || Version: 1.1 || By Dracovanys || Credits: israpps/ErikAndren (CUE2POPS); putnam/cgarz (binmerge); krHACKen/shaolinassassin
(POPStarter)

positional arguments:
  games_dir             Directory where all your PS1 games are stored.
  pops_iox              Path to "POPS_IOX.PAK" if not on CidPOPS directory.

options:
  -h, --help            show this help message and exit
  -c [CONVERTVCD], --convertVCD [CONVERTVCD]
                        Convert a CUE file to VCD. (Usage.: -c "D:\Downloads\Crash Bandicoot (USA)\Crash Bandicoot (USA).cue")
  -m [MERGETRACKS], --mergeTracks [MERGETRACKS]
                        Merge tracks and generate a new CUE file. (Usage.: -m "D:\Downloads\Crash Bandicoot (USA)\Crash Bandicoot (USA).cue")
  -md5 [GETMD5], --getMD5 [GETMD5]
                        Return MD5 hash of a file. (Usage.: --md5 "D:\Downloads\Crash Bandicoot (USA)\Crash Bandicoot (USA).cue")
  --opl                 Just create "conf_apps.cfg" file.
  --ps1_pfx             Add "PS1_" prefix to all OPL shortcuts on "conf_apps.cfg" file (Ex.: "PS1 - Crash Bandicoot (USA)").
```

### POPS Setup (For USB only, at the moment)

First of all, it is essential that you download and place the "POPS_IOX.PAK" file in the same folder as CidPOPS. I did not include it in the project due to copyright reasons, so you will need to find it. An original "POPS_IOX.PAK" file will have the following MD5 code:

```
a625d0b3036823cdbf04a3c0e1648901
```

To run the setup, simply execute the CidPOPS.exe file with the following syntax:

```
CidPOPS.exe [Path to your BINs and CUEs folder]

Ex.: CidPOPS.exe "D:\Games\PS1"
```

If you are using OPL, you can add the tag "--ps1_pfx" after the path to the game folder so that the shortcuts created in the "conf_apps.cfg" file have the prefix "PS1 - ":

```
CidPOPS.exe "D:\Games\PS1" --ps1_pfx
```

This way, the games will be more organized in the OPL apps list:

```
Apollo Save Tool
PS1 - Crash Bandicoot (USA)
PS1 - Final Fantasy IX (USA)
uLaunchELF
```

After that, a folder (USB) will be created at the root of the CidPOPS folder with the following items:

 - **POPS**: The main folder, this is where the converted VCDs and POPStarter ELFs will be. Copy this folder to your USB device. If you want to repeat the process, you'll need to delete it.
 - **POPStarter_Quickstarter**: At the moment, you won't need to interact with this folder, but I recommend keeping it here so you don't need to download it again.
 - **conf_apps.cfg**: If you're using OPL, it's also a good idea to copy this file to your USB device, or if you already have this file, you can just insert the contents of this one into the existing file.

That's it! Now you have a USB device fully set up with your favorite PS1 games!

### CUE to VCD Conversion

If you already have a pre-configured USB device and just want to add more games, CidPOPS has the integrated tool "[CUE2POPS](https://github.com/israpps/cue2pops)", which allows you to convert CUE files to VCD. To use this functionality, execute the following command:

```
CidPOPS.exe -c [Path to the CUE file]

Ex.: CidPOPS.exe -c "D:\Games\PS1\Crash Bandicoot (USA).cue"
```

If the specified CUE file has multiple tracks, such as the game Tomb Raider, which has 50 (!), CidPOPS will trigger another integrated tool called "[binmerge](https://github.com/putnam/binmerge)", which will automatically merge all the tracks and resume the conversion process.

### Merging multiple tracks

It is also possible to simply merge the multiple BIN tracks related to a CUE file, without needing to convert them, by using the conversion functionality. Just execute the following command:

```
CidPOPS.exe -m [Path to the CUE file]

Ex.: CidPOPS.exe -m "D:\Games\PS1\Crash Bandicoot (USA).cue"
```

After that, in the same folder as the CUE file, another folder with the "_Merged" tag will be created. Inside it, you will find the new CUE file with the single merged track.

## Future Improvements

 - Automated setup for SMB and HDD.
 - GUI using the Tkinter library.

## Credits and Acknowledgements

My sincere thanks to the developers of the tools that contribute to CidPOPS and key people from the Sony PlayStation 2 community:

- [@israpps](https://github.com/israpps) (CUE2POPS)
- [@ErikAndren](https://github.com/ErikAndren) (CUE2POPS)
- [@putnam](https://github.com/putnam) (binmerge)
- [@cgarz](https://github.com/cgarz) (binmerge)
- krHACKen (POPStarter)
- ShaolinAssassin ([POPStarter](https://bitbucket.org/ShaolinAssassin/popstarter-documentation-stuff/wiki/Home))
