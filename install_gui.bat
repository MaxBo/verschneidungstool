call mamba create -y -n verschneidungstool_312_np1_26 python=3.12 setuptools pyqt=5 numpy=1.26 pandas=2.3 psycopg2 xlwt pip pandas openpyxl xarray pytest sqlalchemy
call mamba activate verschneidungstool_312_np1_26
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
