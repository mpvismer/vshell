:: Demostrates customising the ipython shell
:: Either parse arguments on the command line to ipython or launch it with interactively running a script which does the configuration
@echo off
:: Command line configuration example, -c a string to execute on the command line at startup
:C:\Python27\Scripts\ipython.exe --quick -c "%logstart -ort session.log rotate;  %run -i 'ipython_config.py'; %autocall 2" 
:: Using a configuration script
C:\Python27\Scripts\ipython.exe -i vshell.py

pause