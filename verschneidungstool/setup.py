# -*- coding: utf-8 -*-
#
from setuptools import setup, find_packages

setup(
    name="verschneidungstool",
    version="1.8.1",
    url='https://github.com/MaxBo/verschneidungstool',
    author='Christoph Franke',
    description="graphical user interface for computing intersections on travel analysis zones",
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Traffic Planners",
        "License :: Other/Proprietary License",
        "Natural Language :: German",
        "Operating System :: Windows",
        "Programming Language :: Python",
    ],
    keywords='VERSCHNEIDUNGSTOOL',
    download_url='',
    license='other',
    packages=find_packages('src'),
    namespace_packages=['verschneidungstool'],
    package_dir={'': 'src'},
    package_data={'': ['dlls/*', 'docs/*'], },
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'setuptools',
        'psycopg2',
        'lxml',
        'openpyxl',
        'sqlalchemy',
    ],

    # PyQT 4 needed, no disutils available for the package.
    # install it seperately

    entry_points={
        'console_scripts': [
            'verschneidungstool=verschneidungstool.main:startmain',
        ],
    },
)
