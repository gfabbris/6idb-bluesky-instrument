"""
Lakeshore temperature controllers
"""

__all__ = ['lakeshore340',]

from .lakeshore340 import LS340Device
from ..framework import sd

from ..session_logs import logger
logger.info(__file__)

# Lakeshore 340 - Low temperature
lakeshore340 = LS340Device('6idb1:LS340:TC1:', name="lakeshore340",
                           labels=("lakeshore",))
lakeshore340.control.readback.kind = "normal"
lakeshore340._auto_ranges = {'10 mA': None, '33 mA': None,
                             '100 mA': (0, 8), '333 mA': (8, 20),
                             '1 A': (20, 305)}

sd.baseline.append(lakeshore340)