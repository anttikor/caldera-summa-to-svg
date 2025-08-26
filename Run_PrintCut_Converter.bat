@echo off
REM Batch file to run PrintCut to SVG Converter
REM This batch file launches the executable from the dist folder

echo Starting PrintCut to SVG Converter...
echo.

REM Check if the executable exists
if exist "dist\PrintCut_to_SVG_Converter.exe" (
    start "" "dist\PrintCut_to_SVG_Converter.exe"
    echo PrintCut to SVG Converter launched successfully!
) else (
    echo ERROR: Executable not found in dist\PrintCut_to_SVG_Converter.exe
    echo Please make sure the application has been built with PyInstaller.
    echo.
    pause
)

echo.
echo If the application didn't start, you can also run it directly from:
echo dist\PrintCut_to_SVG_Converter.exe
echo.
pause