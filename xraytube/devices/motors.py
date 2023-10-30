"""
motors
"""

#    m1  m2  m3  m4  m5  m6  m7  m8
#__all__ = ["mtest", ]
__all__ = []

from ..session_logs import logger

logger.info(__file__)

from ophyd import MotorBundle, EpicsMotor, Component, EpicsSignal


# this motor is not connected yet (good for testing):
#  6idb1:m20 (phi motor)

#mtest = EpicsMotor("6idb1:m20", name="mtest", labels=("motor",))

# IOC = "FIXME:"
# m1 = EpicsMotor(f"{IOC}m1", name="m1", labels=("motor",))
# m2 = EpicsMotor(f"{IOC}m2", name="m2", labels=("motor",))
# m3 = EpicsMotor(f"{IOC}m3", name="m3", labels=("motor",))
# m4 = EpicsMotor(f"{IOC}m4", name="m4", labels=("motor",))
# m5 = EpicsMotor(f"{IOC}m5", name="m5", labels=("motor",))
# m6 = EpicsMotor(f"{IOC}m6", name="m6", labels=("motor",))
# m7 = EpicsMotor(f"{IOC}m7", name="m7", labels=("motor",))
# m8 = EpicsMotor(f"{IOC}m8", name="m8", labels=("motor",))
