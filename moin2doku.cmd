@echo off
setlocal

call settings.cmd

if not "%1"=="" goto :singlePage %1

if "%OUTDIR%"=="" (
  call :deldir out\media || (pause & goto :eof)
  call :deldir out\meta || (pause & goto :eof)
  call :deldir out\pages || (pause & goto :eof)
  if exist %~n0.pages.log del %~n0.pages.log
  if not exist out md out
  set OUTDIR=%CD%\out
)

call python moin2doku.py -d "%OUTDIR:\=/%" >"%~n0.log" 2>"%~n0.err.log"

goto :eof
:deldir
if exist %1 rd /s/q %1
if exist %1 exit /B 1

goto :eof
:singlePage
if "%OUTDIR%"=="" set OUTDIR=%CD%\out
call python moin2doku.py -p "%MOIN_DATA_HOME%\pages\%~1" -f -d "%OUTDIR:\=/%" >>"%~n0.log" 2>>"%~n0.err.log"

goto :eof
