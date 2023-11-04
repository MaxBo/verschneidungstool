call conda create -y -n verschneidungstool_311_2023 python=3.11 setuptools pyqt=5 numpy psycopg2 xlwt lxml pip pandas openpyxl xarray pytest pytables sqlalchemy
call conda activate verschneidungstool_311_2023
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
