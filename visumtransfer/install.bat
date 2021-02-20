call conda create -y -n generatevisem python=3.5
call activate generatevisem
call conda install -y pandas
call conda install -y pytables
call conda install -y h5py
call conda install -y netcdf4
call pip install h5netcdf
call conda install -y -c jiffyclub zbox xarray
call pip install orca
call conda install -y psycopg2
call conda install -y sqlalchemy
call pip install recordclass
call conda install -y openpyxl
call conda install -y -c conda-forge pyqt
call pip install ..\wheels\ViTables-2.1-py3-none-any.whl
call pip install -e .
