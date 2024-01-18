"""
Lakeshore temperature controllers
"""

__all__ = ['lakeshore336', ]

from apstools.devices import LakeShore336Device
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)

# Lakeshore 340 - Low temperature
lakeshore336 = LakeShore336Device(
    '6idb1:LS340:TC1:', name="lakeshore336", labels=("lakeshore",))
lakeshore336.control.readback.kind = "normal"
sd.baseline.append(lakeshore336)
