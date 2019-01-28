@echo off
setlocal

call settings.cmd

pushd "%DOKU_ANIMALS_HOME%\%ANIMAL%"

if not exist data\media\logo.png (
  call :cleanup data\attic || goto :ende
  call :cleanup data\cache || goto :ende
  call :cleanup data\index || goto :ende
  call :cleanup data\locks || goto :ende
  call :cleanup data\media_attic || goto :ende
  call :cleanup data\media_meta || goto :ende
  call :cleanup data\tmp || goto :ende
  xcopy /S/I/Y/Q common\*.* data
)

REM if exist data\pages\startseiteneu.txt (
  REM ren data\pages\startseiteneu.txt startseite.txt
  REM ren data\meta\startseiteneu.changes startseite.changes
REM )

popd 
pushd "%DOKU_HOME%"

php bin\indexer.php

:ende
popd

pause

goto :eof
:cleanup
if not exist %1 goto :eof
echo cleaning up %1
rd /s/q %1
if exist %1 exit /b 1
md %1
echo >nul 2>"%~1\_dummy"
