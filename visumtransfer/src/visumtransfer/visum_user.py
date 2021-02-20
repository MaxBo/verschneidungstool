# -*- coding: utf-8 -*-


def get_visum_user(Visum) -> str:
    """Return the Visum User"""
    license = Visum.LicenseManager.CurrentLicenseInfo
    return license.AttValue('LicenseName')


