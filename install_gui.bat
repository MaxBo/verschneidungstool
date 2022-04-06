call conda create -y -n verschneidungstool39 python=3.9 setuptools pyqt=5 numpy psycopg2 xlwt lxml pip pandas openpyxl xarray pytest pytables
call conda activate verschneidungstool39
cd visumtransfer
call python -m pip install .
cd ..\verschneidungstool
call python -m pip install .
cd ..
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause
