@echo off
color d

:loop
echo.
echo.
echo Type 0 to install needed libraries 
echo.
echo.
echo Type 9 to exit
echo.
echo.

set /p jaka=

if /I %jaka% EQU 0 goto setup

if /I %jaka% EQU 9 exit 


goto loop


:setup



powershell pip install manim 



powershell pip install pydub

pause

exit
