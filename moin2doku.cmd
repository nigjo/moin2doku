@echo off
setlocal

call settings.cmd

if not "%1"=="" goto :singlePage %1

if "%OUTDIR%"=="" (
  call :deldir out\attic || (pause & goto :eof)
  call :deldir out\media || (pause & goto :eof)
  call :deldir out\meta || (pause & goto :eof)
  call :deldir out\pages || (pause & goto :eof)
  if exist %~n0.pages.log del %~n0.pages.log
  if not exist out md out
  set OUTDIR=%CD%\out
)

call python moin2doku.py %DOKU_FULL_HISTORY% -d "%OUTDIR:\=/%" >"%~n0.log" 2>"%~n0.err.log"

goto :eof
:deldir
if exist %1 rd /s/q %1
if exist %1 exit /B 1

goto :eof
:singlePage
if "%OUTDIR%"=="" set OUTDIR=%CD%\out
call python moin2doku.py %DOKU_FULL_HISTORY% -p "%MOIN_DATA_HOME%\pages\%~1" -f -d "%OUTDIR:\=/%" >>"%~n0.log" 2>>"%~n0.err.log" || type "%~n0.err.log"
if %ERRORLEVEL% == 0 if exist "%DOKU_ANIMALS_HOME%\%ANIMAL%\conf\local.php" (
  rem touching "%DOKU_ANIMALS_HOME%\%ANIMAL%\conf\local.php" to invalidate cache
  pushd "%DOKU_ANIMALS_HOME%\%ANIMAL%\conf"
  copy /y/b local.php +,, >nul
  popd
)

goto :eof
