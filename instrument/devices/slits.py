"""
slits
"""

__all__ = """
    slit3
    slit4
""".split()

from ..session_logs import logger

logger.info(__file__)

from ophyd import MotorBundle, EpicsMotor, Component


# 6idb1:m1.DESC                  SL3_Top
# 6idb1:m2.DESC                  SL3_Bottom
# 6idb1:m3.DESC                  SL3_Inboard
# 6idb1:m4.DESC                  SL3_Outboard
# 6idb1:m5.DESC                  SL4_HCEN
# 6idb1:m6.DESC                  SL4_HGap
# 6idb1:m7.DESC                  SL4_VCEN
# 6idb1:m8.DESC                  SL4_VGap


class Slits4Blades_6IDB(MotorBundle):
    top = Component(EpicsMotor, "m1", labels=("motor",))
    bottom = Component(EpicsMotor, "m2", labels=("motor",))
    inboard = Component(EpicsMotor, "m3", labels=("motor",))
    outboard = Component(EpicsMotor, "m4", labels=("motor",))


class Slits4GapCenter_6IDB(MotorBundle):
    hcen = Component(EpicsMotor, "m5", labels=("motor",))
    hgap = Component(EpicsMotor, "m6", labels=("motor",))
    vcen = Component(EpicsMotor, "m7", labels=("motor",))
    vgap = Component(EpicsMotor, "m8", labels=("motor",))


slit3 = Slits4Blades_6IDB("6idb1:", name="slit3", labels=("slits",))
slit4 = Slits4GapCenter_6IDB("6idb1:", name="slit4", labels=("slits",))
