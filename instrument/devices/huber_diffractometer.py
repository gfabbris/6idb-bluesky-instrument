__all__ = "fourc psic".split()

from ..session_logs import logger

logger.info(__file__)

import gi
gi.require_version('Hkl', '5.0')

from hkl.geometries import E4CV
from ophyd import EpicsMotor, PseudoSingle
from ophyd import Component as Cpt

class FourCircle(E4CV):
    """
    Our 4-circle.  Eulerian.  Vertical scattering orientation.
    """
    # the reciprocal axes are called "pseudo" in hklpy
    h = Cpt(PseudoSingle, '', kind="hinted")
    k = Cpt(PseudoSingle, '', kind="hinted")
    l = Cpt(PseudoSingle, '', kind="hinted")

    # the motor axes are called "real" in hklpy
    omega = Cpt(EpicsMotor, "6idb1:m17", kind="hinted")
    chi = Cpt(EpicsMotor, "6idb1:m19", kind="hinted")
    phi = Cpt(EpicsMotor, "6idb1:m20", kind="hinted")
    tth = Cpt(EpicsMotor, "6idb1:m18", kind="hinted")


fourc = FourCircle("", name="fourc")


from hkl.geometries import E6C

class SixCircle(E6C):
    """
#    Our 6-circle.  Eulerian.  
    """
    # the reciprocal axes are called "pseudo" in hklpy
    h = Cpt(PseudoSingle, '', kind="hinted")
    k = Cpt(PseudoSingle, '', kind="hinted")
    l = Cpt(PseudoSingle, '', kind="hinted")

    # the motor axes are called "real" in hklpy
    mu = Cpt(EpicsMotor, "6idb1:m28", kind="hinted")
    omega = Cpt(EpicsMotor, "6idb1:m17", kind="hinted")
    chi = Cpt(EpicsMotor, "6idb1:m19", kind="hinted")
    phi = Cpt(EpicsMotor, "6idb1:m20", kind="hinted")
    gamma = Cpt(EpicsMotor, "6idb1:m29", kind="hinted")
    delta = Cpt(EpicsMotor, "6idb1:m18", kind="hinted")


psic = SixCircle("", name="psic")

from hkl.user import select_diffractometer
select_diffractometer(psic)
