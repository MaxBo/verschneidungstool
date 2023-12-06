call mamba create -y -n verschneidungstool_reghan python=3.10 setuptools pyqt=5.12 numpy psycopg2 xlwt lxml pip pandas openpyxl xarray pytest pytables
call mamba activate verschneidungstool_reghan
cd visumtransfer\visumtransfer
call python -m pip install .
cd ..\..\verschneidungstool
call python -m pip install .
cd ..
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause
