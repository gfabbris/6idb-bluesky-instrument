__all__ = "fourc psic p09 sixcq sixcpsi _geom_ sixcpsi_name".split()


from ..session_logs import logger

logger.info(__file__)

import gi
gi.require_version('Hkl', '5.0')

from hkl.geometries import E4CV, E6C, Petra3_p09_eh2
from hkl.user import select_diffractometer, _geom_
from ophyd import EpicsMotor, PseudoSingle, Kind, Component as Cpt


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
    # This is needed to prevent busy plotting.
    @property
    def hints(self):
        fields = []
        for _, component in self._get_components_of_kind(Kind.hinted):
            if (~Kind.normal & Kind.hinted) & component.kind:
                c_hints = component.hints
                fields.extend(c_hints.get('fields', []))
        return {'fields': fields}

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

    # This is needed to prevent busy plotting.
    @property
    def hints(self):
        fields = []
        for _, component in self._get_components_of_kind(Kind.hinted):
            if (~Kind.normal & Kind.hinted) & component.kind:
                c_hints = component.hints
                fields.extend(c_hints.get('fields', []))
        return {'fields': fields}


psic = SixCircle("", name="psic")
psic.setup_kinds()

def sixcpsi_name():
    """Return the currently-selected diffractometer (or ``None``)."""
    return sixcpsi

class SixcQ(E6C):
    """
    Our 6-circle.  Eulerian.
    """
    # the reciprocal axes are called "pseudo" in hklpy
    q = Cpt(PseudoSingle, '')
    alpha = Cpt(PseudoSingle, '')

    # the motor axes are called "real" in hklpy
    mu = Cpt(EpicsMotor, "6idb1:m28")
    omega = Cpt(EpicsMotor, "6idb1:m17")
    chi = Cpt(EpicsMotor, "6idb1:m19")
    phi = Cpt(EpicsMotor, "6idb1:m20")
    gamma = Cpt(EpicsMotor, "6idb1:m29")
    delta = Cpt(EpicsMotor, "6idb1:m18")

sixcq = SixcQ("", name="sixcq", engine="q2")

class SixcPSI(E6C):
    """
    Our 6-circle.  Eulerian.
    """
    # the reciprocal axes are called "pseudo" in hklpy
    psi = Cpt(PseudoSingle, '')
 
    # the motor axes are called "real" in hklpy
    mu = Cpt(EpicsMotor, "6idb1:m28")
    omega = Cpt(EpicsMotor, "6idb1:m17")
    chi = Cpt(EpicsMotor, "6idb1:m19")
    phi = Cpt(EpicsMotor, "6idb1:m20")
    gamma = Cpt(EpicsMotor, "6idb1:m29")
    delta = Cpt(EpicsMotor, "6idb1:m18")

sixcpsi = SixcPSI("", name="sixcpsi", engine="psi")



class P09(Petra3_p09_eh2):
    """
    Petra PO9 without omega.  Eulerian.
    """
    # the reciprocal axes are called "pseudo" in hklpy
    h = Cpt(PseudoSingle, '')
    k = Cpt(PseudoSingle, '')
    l = Cpt(PseudoSingle, '')

    # the motor axes are called "real" in hklpy
    #mu = eta --- spec psic
    #omega = mu --- spec psic 
    #chi = chi --- spec psic
    #phi = phi --- spec psic
    #delta = nu --- spec psic
    #gamma = del --- spec psic

    mu = Cpt(EpicsMotor, "6idb1:m17")
    omega = Cpt(EpicsMotor, "6idb1:m28")
    chi = Cpt(EpicsMotor, "6idb1:m19")
    phi = Cpt(EpicsMotor, "6idb1:m20")
    delta = Cpt(EpicsMotor, "6idb1:m29")
    gamma = Cpt(EpicsMotor, "6idb1:m18")


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

    # This is needed to prevent busy plotting.
    @property
    def hints(self):
        fields = []
        for _, component in self._get_components_of_kind(Kind.hinted):
            if (~Kind.normal & Kind.hinted) & component.kind:
                c_hints = component.hints
                fields.extend(c_hints.get('fields', []))
        return {'fields': fields}


p09 = P09("", name="p09")
p09.setup_kinds()


select_diffractometer(psic)
