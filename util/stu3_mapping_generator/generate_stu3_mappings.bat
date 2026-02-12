@echo off
REM STU3 Mapping Table Generator
REM Generates mapping table from STU3 StructureDefinition JSON files

echo === STU3 Mapping Table Generator ===
echo.

REM Change to repository root (two directories up from this script)
cd /d "%~dp0..\.."

REM Run the Python script from the util/stu3_mapping_generator directory
python util\stu3_mapping_generator\stu3_mapping_table_generator.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Script failed with exit code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo SUCCESS: STU3 mapping table generated successfully!
echo Output: input/includes/zib2017_stu3_mappings.md
echo.
pause
