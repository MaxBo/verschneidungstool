from ._version import __version__

# Keep package importable in build isolation (where `qgis` is unavailable).
# The Qt compatibility aliases are only needed at runtime inside QGIS.
try:
    from .qt_compat import install_legacy_qt_aliases
except ModuleNotFoundError:
    install_legacy_qt_aliases = None
else:
    install_legacy_qt_aliases()
