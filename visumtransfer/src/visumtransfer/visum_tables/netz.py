# -*- coding: utf-8 -*-

from visumtransfer.visum_table import VisumTable


class Gebiete(VisumTable):
    name = 'Gebiete'
    code = 'GEBIET'
    _cols = 'NR;XKOORD;YKOORD'
    _pkey = 'NR'


class Anbindung(VisumTable):
    name = 'Anbindungen'
    code = 'ANBINDUNG'
    _cols = 'BEZNR;KNOTNR;RICHTUNG;VSYSSET'
    _pkey = 'BEZNR;KNOTNR;RICHTUNG;VSYSSET'


class Punkt(VisumTable):
    name = 'Punkte'
    code = 'PUNKT'
    _cols = 'ID;XKOORD;YKOORD'
    _pkey = 'ID'


class Zwischenpunkt(VisumTable):
    name = 'Zwischenpunkte'
    code = 'ZWISCHENPUNKT'
    _cols = 'KANTEID;INDEX;XKOORD;YKOORD'
    _pkey = 'KANTEID;INDEX'


class POI1(VisumTable):
    name = 'Points of Interest'
    code = 'POIOFCAT_1'
    _cols = 'KATNR;NR;XKOORD;YKOORD'
    _pkey = 'KATNR;NR'


class Screenlinepolygon(VisumTable):
    name = 'Screenlinepolygone'
    code = 'SCREENLINEPOLY'
    _cols = 'SCREENLINENR;INDEX;XKOORD;YKOORD'
    _pkey = 'SCREENLINENR;INDEX'


class Knoten(VisumTable):
    name = 'Knoten'
    code = 'KNOTEN'
    _cols = 'NR;XKOORD;YKOORD'
    _pkey = 'NR'


class Strecke(VisumTable):
    name = 'Strecken'
    code = 'STRECKE'
    _cols = 'NR;VONKNOTNR;NACHKNOTNR;LAENGE;VONKNOTENORIENTIERUNG;NACHKNOTENORIENTIERUNG'
    _pkey = 'NR;VONKNOTNR;NACHKNOTNR'


class Streckenpolygone(VisumTable):
    name = 'Streckenpolygone'
    code = 'STRECKENPOLY'
    _cols = 'VONKNOTNR;NACHKNOTNR;INDEX;XKOORD;YKOORD;ZKOORD'
    _pkey = 'VONKNOTNR;NACHKNOTNR;INDEX'


class Abbieger(VisumTable):
    name = 'Abbieger'
    code = 'ABBIEGER'
    _cols = 'VONKNOTNR;UEBERKNOTNR;NACHKNOTNR;TYPNR;VSYSSET;KAPIV;T0IV;Z_ABB_GES;Z_ABB_L;Z_ZAEHLDATUM'
    _pkey = 'VONKNOTNR;UEBERKNOTNR;NACHKNOTNR'
