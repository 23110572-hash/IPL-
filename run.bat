@echo off
echo ===================================================
echo     Starting IPL Premium Analytics Dashboard
echo ===================================================
echo.
echo Starting local web server...

:: Start the Python HTTP server in a new command window and KEEP IT OPEN
start "IPL Analytics Server" cmd /k "py -m http.server 8000"

:: Wait 3 seconds to ensure the server is fully up and running
ping 127.0.0.1 -n 3 > nul

echo Opening dashboard in your default web browser...
:: Launch the default browser pointing to the dashboard page
start http://localhost:8000/dashboard/

echo.
echo Dashboard is now running! 
echo To stop the server, simply close the other command prompt window that opened.
echo.
