"""
EPICS scaler
"""

__all__ = ["scaler2", "scaler1" ]

from ophyd.scaler import ScalerCH
from ..session_logs import logger

logger.info(__file__)

scaler2 = ScalerCH("6idb1:scaler2", name="scaler2", labels=["scalers", "detectors"])
scaler2.wait_for_connection()

# choose just the channels with EPICS names
scaler2.select_channels()
# scaler2.stage_sigs["preset_time"] = 1

scaler1 = ScalerCH("6idb1:scaler1", name="scaler1", labels=["scalers", "detectors"])
scaler1.wait_for_connection()

# choose just the channels with EPICS names
scaler1.select_channels()
# scaler1.stage_sigs["preset_time"] = 1

for item in scaler1.channels.component_names:
    getattr(scaler1.channels, item).s.kind="normal"


for item in scaler2.channels.component_names:
    getattr(scaler2.channels, item).s.kind="normal"