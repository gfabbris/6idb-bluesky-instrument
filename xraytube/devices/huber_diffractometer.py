__all__ = "fourc psic _geom_".split()

from ..session_logs import logger

logger.info(__file__)

import gi
gi.require_version('Hkl', '5.0')

from hkl.geometries import E4CV, E6C
from hkl.user import select_diffractometer, _geom_
from ophyd import EpicsMotor, PseudoSingle, Component as Cpt


class FourCircle(E4CV):
    """
    Our 4-circle.  Eulerian.  Vertical scattering orientation.
    """
    # the reciprocal axes are called "pseudo" in hklpy
    h = Cpt(PseudoSingle, '')
    k = Cpt(PseudoSingle, '')
    l = Cpt(PseudoSingle, '')

    # the motor axes are called "real" in hklpy
    omega = Cpt(EpicsMotor, "6idb1:m17")
    chi = Cpt(EpicsMotor, "6idb1:m19")
    phi = Cpt(EpicsMotor, "6idb1:m20")
    tth = Cpt(EpicsMotor, "6idb1:m18")
        
    def setup_kinds(self, hinted=[]):
        for item in "h k l".split():
            getattr(self, item).readback.kind = "normal"

        for item in "omega chi phi tth".split():
            getattr(self, item).user_readback.kind = "normal"

        for item in hinted:
            attr = getattr(item, "readback", None)
            if attr is None:
                attr = getattr(item, "user_readback", None)
            if attr is not None:
                attr.kind = "hinted"


fourc = FourCircle("", name="fourc")
fourc.setup_kinds()


class SixCircle(E6C):
    """
    Our 6-circle.  Eulerian.
    """
    # the reciprocal axes are called "pseudo" in hklpy
    h = Cpt(PseudoSingle, '')
    k = Cpt(PseudoSingle, '')
    l = Cpt(PseudoSingle, '')

    # the motor axes are called "real" in hklpy
    mu = Cpt(EpicsMotor, "6idb1:m28")
    omega = Cpt(EpicsMotor, "6idb1:m17")
    chi = Cpt(EpicsMotor, "6idb1:m19")
    phi = Cpt(EpicsMotor, "6idb1:m20")
    gamma = Cpt(EpicsMotor, "6idb1:m29")
    delta = Cpt(EpicsMotor, "6idb1:m18")
    
    def setup_kinds(self, hinted=[]):
        for item in "h k l".split():
            getattr(self, item).readback.kind = "normal"

        for item in "mu omega chi phi gamma delta".split():
            getattr(self, item).user_readback.kind = "normal"

        for item in hinted:
            attr = getattr(item, "readback", None)
            if attr is None:
                attr = getattr(item, "user_readback", None)
            if attr is not None:
                attr.kind = "hinted"


psic = SixCircle("", name="psic")
psic.setup_kinds()
select_diffractometer(psic)

