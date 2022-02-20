REM call conda create -y -n verschneidungstool39
REM python=3.9 setuptools pyqt=5 numpy psycopg2 xlwt lxml pip pandas openpyxl xarray pytest pytables
call conda activate strukturdaten
call python -m pip install -r requirements.txt
cd visumtransfer
call pip install .
cd ..\verschneidungstool
call pip install -e .
cd ..
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause
