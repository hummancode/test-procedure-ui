@echo off
REM ============================================================================
REM Build Script for Test Procedure Application (ANACONDA VERSION)
REM Creates a standalone executable with PyInstaller using Anaconda environment
REM ============================================================================

echo ========================================
echo Building Test Procedure Application
echo Publisher: X
echo Version: 1.0
echo Using: Anaconda Environment
echo ========================================
echo.

REM ============================================================================
REM CONFIGURATION - CHANGE THIS TO YOUR ENVIRONMENT NAME
REM ============================================================================
set CONDA_ENV_NAME=test_station_kiosk
REM Replace 'your_env_name' with your actual Anaconda environment name
REM Example: set CONDA_ENV_NAME=testproc
REM ============================================================================

echo Activating Anaconda environment: %CONDA_ENV_NAME%
echo.

REM Try to activate Anaconda environment
call conda activate %CONDA_ENV_NAME%
if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Failed to activate Anaconda environment '%CONDA_ENV_NAME%'
    echo ========================================
    echo.
    echo Please check:
    echo 1. Anaconda/Miniconda is installed
    echo 2. Environment name is correct
    echo 3. Run this from Anaconda Prompt OR
    echo 4. Run 'conda init' first
    echo.
    echo Current environments:
    call conda env list
    echo.
    pause
    exit /b 1
)

echo Environment activated successfully!
echo.

REM Verify Python version
echo Python version:
python --version
echo.

REM Verify PyInstaller is installed in this environment
python -c "import PyInstaller; print('PyInstaller version:', PyInstaller.__version__)" 2>NUL
if errorlevel 1 (
    echo.
    echo PyInstaller not found in environment '%CONDA_ENV_NAME%'!
    echo Installing PyInstaller...
    echo.
    conda install -c conda-forge pyinstaller -y
    if errorlevel 1 (
        pip install pyinstaller
        if errorlevel 1 (
            echo Failed to install PyInstaller!
            pause
            exit /b 1
        )
    )
)

echo PyInstaller found!
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

REM Create icon if it doesn't exist (optional)
if not exist resources\icons mkdir resources\icons
if not exist resources\icons\app_icon.ico (
    echo WARNING: app_icon.ico not found in resources\icons\
    echo The executable will be built without a custom icon.
    echo.
)

REM Build the executable using the spec file
echo.
echo Building executable...
echo.
pyinstaller TestProcedure.spec --clean --noconfirm

if errorlevel 1 (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo Common issues:
    echo - Missing dependencies: pip install -r requirements.txt
    echo - Wrong environment activated
    echo - Missing spec file
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD SUCCESSFUL!
echo ========================================
echo.
echo Executable location: dist\TestProcedure\TestProcedure.exe
echo.
echo You can now distribute the entire 'dist\TestProcedure' folder
echo.

REM Optional: Create a simple README in the dist folder
echo Creating distribution README...
(
echo Test Prosedürü Uygulaması v1.0
echo.
echo KURULUM:
echo --------
echo 1. Tüm "TestProcedure" klasörünü istediğiniz konuma kopyalayın
echo 2. TestProcedure.exe dosyasını çalıştırın
echo.
echo NOTLAR:
echo -------
echo - İlk çalıştırmada "data" klasörü otomatik oluşturulacaktır
echo - Güncelleme ayarları için: Dosya ^> Güncelleme Ayarları
echo - Excel raporları için: Test sırasında "Raporla" butonuna tıklayın
echo.
echo Publisher: X
echo Copyright (c) 2026 X
echo.
echo Built with Python from Anaconda environment: %CONDA_ENV_NAME%
) > dist\TestProcedure\README.txt

echo Distribution README created.
echo.

REM Optional: Copy data folder if needed
if exist data (
    echo Copying data folder to distribution...
    xcopy data dist\TestProcedure\data\ /E /I /Y
)

REM Optional: Copy resources folder if needed
if exist resources (
    echo Copying resources folder to distribution...
    xcopy resources dist\TestProcedure\resources\ /E /I /Y
)

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Environment used: %CONDA_ENV_NAME%
echo Python location: 
python -c "import sys; print(sys.executable)"
echo.
echo Next steps:
echo 1. Test the executable: dist\TestProcedure\TestProcedure.exe
echo 2. If it works, compress "dist\TestProcedure" folder to ZIP
echo 3. Distribute to users
echo.
echo Note: The executable is STANDALONE - users don't need Python/Anaconda!
echo.

pause
