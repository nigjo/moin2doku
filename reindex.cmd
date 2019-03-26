@echo off
setlocal

call settings.cmd

pushd "%DOKU_ANIMALS_HOME%\%ANIMAL%"

if not exist data\pages\ (
  echo WARNUNG:
  echo Es wurden kein "pages" Verzeichnis gefunden. Wurde die neue Version bereits
  echo ins Zielverzeichnis kopiert?
  pause
  goto :eof
)

if not exist data\media\logo.png (
  echo working in %CD%
  rem call :cleanup data\attic || goto :ende
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

php bin\indexer.php || goto :ende

popd
pushd "%DOKU_ANIMALS_HOME%\%ANIMAL%"

if exist data\meta\_dokuwiki.changes del data\meta\_dokuwiki.changes
if exist data\meta\_dokuwiki.changes del data\meta\_dokuwiki.changes
(
  for /F "delims=*" %%D in ('dir /b/S/A:D data\meta\*.*') do (
    if exist "%%D\*.changes" type "%%D\*.changes" 2>nul
  )
) > _dokuwiki_unsorted.changes
sort _dokuwiki_unsorted.changes /O data\meta\_dokuwiki.changes
del _dokuwiki_unsorted.changes

echo --- compressing old files
for /F "delims=*" %%T in ('dir data\attic\*.txt /s/b') do (
  "c:\Program Files\7-Zip\7z.exe" a -bso0 "%%T.gz" "%%T" && del "%%T" || goto :ende
)
echo --- done

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
