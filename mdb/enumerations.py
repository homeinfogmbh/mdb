"""Common enums."""

from enum import Enum


__all__ = ['State']


class State(Enum):
    """German states."""

    BW = 'Baden-Württemberg'
    BY = 'Bayern'
    BE = 'Berlin'
    BB = 'Brandenburg'
    HB = 'Bremen'
    HH = 'Hamburg'
    HE = 'Hessen'
    MV = 'Mecklenburg-Vorpommern'
    NI = 'Niedersachsen'
    NW = 'Nordrhein-Westfalen'
    RP = 'Rheinland-Pfalz'
    SL = 'Saarland'
    SN = 'Sachsen'
    ST = 'Sachsen-Anhalt'
    SH = 'Schleswig-Holstein'
    TH = 'Thüringen'
