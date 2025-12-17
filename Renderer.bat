@echo off
title AspidaRenderer
color d
setlocal EnableDelayedExpansion
mode 38, 18



:loop
cls
color d


echo Type 5 to enter file name you want to render
echo.
echo.
echo Type 0 to render your file
echo.
echo.
echo Type 9 to exit
echo.
echo.
echo Type 11 to wipe all data
echo.

set /p input=
if /I %input% EQU 5 goto namer
if /I %input% EQU 11 goto wiper
if /I %input% EQU 9 exit
if /I %input% EQU 0 goto render

goto loop

:namer 
cls
color d
echo Please input the name of your file
echo.
echo With extensions like .wav or .mp4
echo.
echo Type 9 to exit
echo.

set /p inpii=

if /I %inpii% EQU 9 exit 

echo %inpii% > temp.txt

goto loop


:wiper

echo Deleting...


powershell rm temp.txt
echo A | powershell rm media
echo A | powershell rm __pycache__

timeout /t 1 >nul

goto loop






:render 
mode 200, 100

powershell manim -p AA.py AspidaAudio


timeout /t 1 >nul

exit
