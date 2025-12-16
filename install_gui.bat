call mamba create -y -n verschneidungstool_313 python=3.13 setuptools pyqt=5 numpy psycopg2 xlwt pip pandas openpyxl xarray pytest sqlalchemy
call mamba activate verschneidungstool_313
call python -m pip install -r requirements.txt
cd visumtransfer\visumtransfer
call pip install .
cd ..\..\verschneidungstool
call pip install .
cd ..
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause
