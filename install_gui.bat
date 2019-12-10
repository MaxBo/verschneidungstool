call conda create -y -n verschneidungstool38 python=3.8 setuptools pyqt=5 numpy psycopg2 xlwt lxml
call activate verschneidungstool38
call python setup.py install
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause
