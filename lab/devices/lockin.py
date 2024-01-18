"""
Lock in
"""

__all__ = ['lockin1', ]

from .srs830 import LockinDevice
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)


lockin1 = LockinDevice('4idd:SRS810:1:', name='lockin1', labels=('detectors',))
sd.baseline.append(lockin1)

lockin2 = LockinDevice('4idd:SRS810:1:', name='lockin2', labels=('detectors',))
sd.baseline.append(lockin2)
