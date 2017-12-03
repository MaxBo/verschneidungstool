call conda create -n verschneidungstool python=2.7
call activate verschneidungstool
call conda install -y pyqt=4 
call conda install -y numpy
call conda install -y -c https://conda.binstar.org/topper psycopg2-win-py27
cd extractiontools
call python setup.py install
cd ..
cd verschneidungstool
call python setup.py install
echo.
echo.
echo Installation der grafischen Oberflaeche fuer Verschneidungen beendet.
pause