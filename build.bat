@echo off 

:: Preparing environment for build
rd /s /q "%~dp0\release"
build.py

:: Generate CidPOPS executable
pyinstaller --onefile --distpath "release" --icon="%~dp0\assets\icon.ico" -n "CidPOPS" --add-data util:util main_toBuild.py

:: Cleaning routine
rd /s /q "%~dp0\build"
del "%~dp0\*_toBuild.py"
del "%~dp0\src\*_toBuild.py"
del "%~dp0\*.spec"