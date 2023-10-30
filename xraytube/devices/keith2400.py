from ophyd import Component, Device, EpicsSignal
from apstools.devices import PVPositionerSoftDoneWithStop

from ..session_logs import logger

logger.info(__file__)
all__ = ["keith2400"]


class VoltageCurrentPositioner(PVPositionerSoftDoneWithStop):

    setpoint = Component(
        EpicsSignal, "{prefix}{_setpoint_pv}",
        write_pv="{prefix}{_setpoint_pv_set}"
    )

    def __init__(self, *args, setpoint_pv_set="", **kwargs):
        self._setpoint_pv_set = setpoint_pv_set
        super().__init__(*args, **kwargs)


class Keithley2400Device(Device):
    voltage = Component(
        VoltageCurrentPositioner,
        readback_pv="measVoltAI",
        setpoint_pv="setVoltRdAI",
        setpoint_pv_set="setVoltAO"
    )
    voltage_range = Component(EpicsSignal, "vRangeMO")

    current = Component(
        VoltageCurrentPositioner,
        readback_pv="measCurrAI",
        setpoint_pv="setCurrRdAI",
        setpoint_pv_set="setCurrAO"
    )
    current_range = Component(EpicsSignal, "iRangeMO")

    sense_function = Component(
        EpicsSignal, "senseFunctionMO", string=True, kind="config"
    )
    source_function = Component(
        EpicsSignal, "sourceFunctionMO", string=True, kind="config"
    )


keith2400 = Keithley2400Device("6idb1:K24K:", name="keith2400")
# TODO: Alternative to skip the line below is to create a loading function.
# sd.baseline.append(keith2400)
