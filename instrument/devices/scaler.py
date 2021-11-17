"""
EPICS scaler
"""

__all__ = ["scaler2", ]

from ophyd.scaler import ScalerCH
from ..session_logs import logger

logger.info(__file__)

scaler2 = ScalerCH("6idb1:scaler2", name="scaler2", labels=["scalers", "detectors"])
scaler2.wait_for_connection()

# choose just the channels with EPICS names
scaler2.select_channels()
