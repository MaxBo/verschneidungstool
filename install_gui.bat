call mamba create -y -n verschneidungstool_310_2023 python=3.10 setuptools pyqt=5.12 numpy psycopg2 xlwt lxml pip pandas openpyxl xarray pytest pytables sqlalchemy
call mamba activate verschneidungstool_310_2023
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
