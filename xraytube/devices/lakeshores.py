"""
Lakeshore temperature controllers
"""

__all__ = ['lakeshore340', ]

from apstools.devices import LakeShore340Device
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)

# Lakeshore 340 - Low temperature
lakeshore340 = LakeShore340Device(
    '6idb1:LS340:TC1:', name="lakeshore340", labels=("lakeshore",))
lakeshore340.control.readback.kind = "normal"
sd.baseline.append(lakeshore340)
