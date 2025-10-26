@echo off
setlocal enabledelayedexpansion

set "source=..\Landing page\Aegis.PNG"
set "target_dir=images"

if not exist "%target_dir%" mkdir "%target_dir%"

copy /Y "%source%" "%target_dir%\icon16.png"
copy /Y "%source%" "%target_dir%\icon48.png"
copy /Y "%source%" "%target_dir%\icon128.png"

echo Logos copiados exitosamente a la carpeta %target_dir%\
pause
