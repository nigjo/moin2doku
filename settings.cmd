@echo off
REM -- no setlocal in this script!
REM make a copy of this file and adjust the paths

set PHP_HOME=c:\Program Files\php
set PYTHON_HOME=c:\Python27
REM -- MoinMoin settings 
set MOIN_HOME=c:\wwwroot\wiki\moin
set MOIN_CONFIG=%MOIN_HOME%\wiki\config
REM set MOIN_CONFIG=c:\wwwroot\moinfarmdata\config
set MOIN_DATA_HOME=%MOIN_HOME%\wiki\data
REM set MOIN_CONFIG=c:\wwwroot\moinfarmdata\<farmwiki>
REM -- DokuWiki settings
set DOKU_HOME=c:\wwwroot\wiki\dokuwiki
set DOKU_ANIMALS_HOME=%DOKU_HOME%
REM set DOKU_ANIMALS_HOME=c:\wwwroot\dokufarmdata
REM set animal=<yourFarmAnimalName>
REM comment this in to do a full converstion
REM set DOKU_FULL_HISTORY=-a

REM -- path to your php.ini used by your webserver
REM set PHP_INI_SCAN_DIR=c:\Program Files\ApacheHttpd\conf\

REM -- set this to your "production" dokuwiki if you want to update only.
REM set OUTDIR=%DOKU_ANIMALS_HOME%\%animal%\data

REM ----8<--------8<--------8<--------8<--------8<--------8<--------8<----
REM -- remove everything beyond the line from your copy
chcp 1252

if exist "%~dpn0.local.cmd" call "%~dpn0.local.cmd"

REM -- %animal% must be lowercase!
(
set animal=
set animal=%animal%
)

set PATH=%PATH%;%PYTHON_HOME%;%PHP_HOME%

set PYTHONPATH=.
set PYTHONPATH=%PYTHONPATH%;%MOIN_HOME%
set PYTHONPATH=%PYTHONPATH%;%MOIN_HOME%\MoinMoin\support
set PYTHONPATH=%PYTHONPATH%;%MOIN_CONFIG%
set PYTHONPATH=%PYTHONPATH%;
