call conda create -n verschneidungstool python=3.7
call activate verschneidungstool
call conda install -y pyqt=5
call conda install -y numpy
call conda install -y psycopg2
call conda install -y xlwt
call conda install -y lxml
cd extractiontools
call python setup.py install
cd ..
cd verschneidungstool
call python setup.py install
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause
