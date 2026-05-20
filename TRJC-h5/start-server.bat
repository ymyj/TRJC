@echo off
echo Starting server at http://localhost:8080/
echo.
echo Please open your browser and navigate to http://localhost:8080/
echo.

:: Try python first
python -m http.server 8080 2>nul
if %errorlevel% == 0 goto :end

:: Try python3
python3 -m http.server 8080 2>nul
if %errorlevel% == 0 goto :end

:: Try node http-server if available
npx http-server -p 8080 2>nul
if %errorlevel% == 0 goto :end

echo No suitable server found. Please install Python or Node.js.
pause

:end
