# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 21:00:21 2016

@author: MaxBohnet
"""


def write_header(file):
    """
    Write header to open file

    Parameters
    ----------
    file : open file object
    """
    header = """*
$VISION
* Gertz Gutsche Rümenapp Stadtentwicklung und Mobilität GbR Hamburg
*
* Tabelle: Versionsblock
*
$VERSION:VERSNR;FILETYPE;LANGUAGE
10;Trans;DEU

    """
    file.write(header)
