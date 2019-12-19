call conda create -y -n verschneidungstool37 python=3.7 setuptools pyqt=5 numpy psycopg2 xlwt lxml
call activate verschneidungstool37
call python setup.py install
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause
