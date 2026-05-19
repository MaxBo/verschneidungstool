from qgis.PyQt import QtCore, QtGui, QtWidgets


def _set_alias(target, legacy_name: str, value):
    if value is None:
        return
    if getattr(target, legacy_name, None) is None:
        try:
            setattr(target, legacy_name, value)
        except Exception:
            # Some bindings expose read-only attributes; skip silently.
            pass


def _alias_from_group(target, legacy_name: str, group_name: str, member_name: str):
    if getattr(target, legacy_name, None) is not None:
        return
    group = getattr(target, group_name, None)
    if group is None:
        return
    _set_alias(target, legacy_name, getattr(group, member_name, None))


def install_legacy_qt_aliases():
    # QtCore.Qt enums moved under scoped enum groups in Qt6.
    qt_aliases = (
        ("ApplicationModal", "WindowModality", "ApplicationModal"),
        ("NonModal", "WindowModality", "NonModal"),
        ("Checked", "CheckState", "Checked"),
        ("Unchecked", "CheckState", "Unchecked"),
        ("PartiallyChecked", "CheckState", "PartiallyChecked"),
        ("ItemIsUserCheckable", "ItemFlag", "ItemIsUserCheckable"),
        ("ItemIsEnabled", "ItemFlag", "ItemIsEnabled"),
        ("ItemIsTristate", "ItemFlag", "ItemIsTristate"),
        ("ItemIsAutoTristate", "ItemFlag", "ItemIsAutoTristate"),
        ("ItemIsUserTristate", "ItemFlag", "ItemIsUserTristate"),
        ("RightDockWidgetArea", "DockWidgetArea", "RightDockWidgetArea"),
        ("LeftDockWidgetArea", "DockWidgetArea", "LeftDockWidgetArea"),
        ("TopDockWidgetArea", "DockWidgetArea", "TopDockWidgetArea"),
        ("BottomDockWidgetArea", "DockWidgetArea", "BottomDockWidgetArea"),
        ("WA_DeleteOnClose", "WidgetAttribute", "WA_DeleteOnClose"),
        ("QueuedConnection", "ConnectionType", "QueuedConnection"),
        ("Horizontal", "Orientation", "Horizontal"),
        ("MatchFixedString", "MatchFlag", "MatchFixedString"),
        ("ScrollBarAlwaysOn", "ScrollBarPolicy", "ScrollBarAlwaysOn"),
        ("LeftToRight", "LayoutDirection", "LeftToRight"),
        ("AA_EnableHighDpiScaling", "ApplicationAttribute", "AA_EnableHighDpiScaling"),
    )
    for legacy_name, group_name, member_name in qt_aliases:
        _alias_from_group(QtCore.Qt, legacy_name, group_name, member_name)

    # QProcess exit-state aliases.
    _alias_from_group(QtCore.QProcess, "NormalExit", "ExitStatus", "NormalExit")
    _alias_from_group(QtCore.QProcess, "CrashExit", "ExitStatus", "CrashExit")
    _alias_from_group(QtCore.QProcess, "Crashed", "ExitStatus", "CrashExit")

    # QMessageBox enums.
    qmb_aliases = (
        ("Warning", "Icon", "Warning"),
        ("Information", "Icon", "Information"),
        ("Critical", "Icon", "Critical"),
        ("Question", "Icon", "Question"),
        ("NoButton", "StandardButton", "NoButton"),
        ("Ok", "StandardButton", "Ok"),
        ("Cancel", "StandardButton", "Cancel"),
        ("Yes", "StandardButton", "Yes"),
        ("No", "StandardButton", "No"),
        ("YesRole", "ButtonRole", "YesRole"),
        ("NoRole", "ButtonRole", "NoRole"),
    )
    for legacy_name, group_name, member_name in qmb_aliases:
        _alias_from_group(QtWidgets.QMessageBox, legacy_name, group_name, member_name)

    # QSizePolicy policy values.
    for policy_name in (
        "Fixed",
        "Minimum",
        "Maximum",
        "Preferred",
        "Expanding",
        "MinimumExpanding",
        "Ignored",
    ):
        _alias_from_group(QtWidgets.QSizePolicy, policy_name, "Policy", policy_name)

    # QFrame shape/shadow enums.
    for shape_name in ("NoFrame", "Box", "Panel", "StyledPanel", "HLine", "VLine", "WinPanel"):
        _alias_from_group(QtWidgets.QFrame, shape_name, "Shape", shape_name)
    for shadow_name in ("Plain", "Raised", "Sunken"):
        _alias_from_group(QtWidgets.QFrame, shadow_name, "Shadow", shadow_name)

    # QDialogButtonBox buttons.
    for button_name in ("Ok", "Cancel", "Yes", "No", "Apply", "Close"):
        _alias_from_group(QtWidgets.QDialogButtonBox, button_name, "StandardButton", button_name)

    # QLineEdit echo modes.
    for echo_name in ("Normal", "NoEcho", "Password", "PasswordEchoOnEdit"):
        _alias_from_group(QtWidgets.QLineEdit, echo_name, "EchoMode", echo_name)

    # QTextEdit line wrap mode.
    _alias_from_group(QtWidgets.QTextEdit, "NoWrap", "LineWrapMode", "NoWrap")

    # QIcon mode/state.
    for mode_name in ("Normal", "Disabled", "Active", "Selected"):
        _alias_from_group(QtGui.QIcon, mode_name, "Mode", mode_name)
    for state_name in ("On", "Off"):
        _alias_from_group(QtGui.QIcon, state_name, "State", state_name)

    # QTextCursor move operation.
    for move_name in ("Start", "End", "Up", "Down"):
        _alias_from_group(QtGui.QTextCursor, move_name, "MoveOperation", move_name)

    # QFont weight alias.
    _alias_from_group(QtGui.QFont, "Bold", "Weight", "Bold")
