@echo off
%~d0
cd %~dp0
if EXIST "%~f1" (goto check2) else (if exist *.cue (for %%i in (*.cue) do CUE2POPS.EXE "%~p0%%i") else goto fail)
pause
goto terminate
:check2
if not exist "%~f1\*.*" goto convert
cd "%~f1"
if not exist *.cue goto fail
for %%i in (*.cue) do "%~dp0\CUE2POPS.EXE" "%~f1\%%i"
pause
goto terminate
:fail
echo. 
echo Error: Please drag/drop a cuesheet or a dir to the batch file.
echo. 
pause
goto terminate
:convert
CUE2POPS.EXE "%~f1"
:terminate
exit
