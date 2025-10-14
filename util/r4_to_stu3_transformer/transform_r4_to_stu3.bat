@echo off
REM FHIR R4 to STU3 Transformer - Convenience shortcut for PZP project
REM Automatically discovers and transforms all supported resources

echo === FHIR R4 to STU3 Transformer (PZP Project) ===
echo.

REM Define input directories THIS NEEDS TO BE UPDATED IF YOUR PATHS DIFFER
set "INPUT_DIR1=C:\git\IKNL\iknl-pzp-fhir-r4\fsh-generated\resources"
set "INPUT_DIR2=C:\git\IKNL\iknl-pzp-fhir-stu3\util\example_generation_fsh\fsh-generated\resources"
set "OUTPUT_DIR=..\..\input\resources"

REM Check if input directories exist
if not exist "%INPUT_DIR1%" (
    echo ERROR: R4 repository directory not found: %INPUT_DIR1%
    echo Please ensure R4 IG has been built first
    pause
    exit /b 1
)

if not exist "%INPUT_DIR2%" (
    echo ERROR: STU3 FSH generated directory not found: %INPUT_DIR2%
    echo Please ensure FSH examples have been generated first
    pause
    exit /b 1
)

echo Transforming resources from R4 to STU3...
echo Input 1: %INPUT_DIR1%
echo Input 2: %INPUT_DIR2%
echo Output: %OUTPUT_DIR%
echo.
echo Auto-discovering available transformers...
echo.

REM Run the Python transformer (auto-discovers all transformers)
python fhir_r4_to_stu3_transformer.py "%INPUT_DIR1%" "%INPUT_DIR2%" "%OUTPUT_DIR%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Transformation failed with exit code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo SUCCESS: Transformation completed!
echo Converted files are in: %OUTPUT_DIR%\
echo.
echo TIP: To transform other resources, use:
echo   python fhir_r4_to_stu3_transformer.py input_dir1 input_dir2 output_dir --resources ResourceType
echo.
pause
