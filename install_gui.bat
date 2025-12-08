call mamba create -y -n verschneidungstool_reghan313 python=3.13 setuptools pyqt=5.15 numpy psycopg2 xlwt lxml pip pandas openpyxl xarray pytest pytables
call mamba activate verschneidungstool_reghan313
cd visumtransfer\visumtransfer
call python -m pip install .
cd ..\..\verschneidungstool
call python -m pip install .
cd ..
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause
