from ophyd import Component
from ophyd import Device
from ophyd import EpicsSignal
from ophyd import EpicsSignalRO
# from ophyd import EpicsSignalWithRBV  #  PV:name and PV:name_RBV
    # EpicsSignalWithRBV same as EpicsSignal, "PV:name", read_pv="_RBV", write_pv=""

class keith2400_input(Device):    
#    voltage = Component(EpicsSignal, "setVoltAO")
    voltage = Component(EpicsSignal, "setVoltRdAI",write_pv="setVoltAO")
    voltageRange = Component(EpicsSignal, "vRangeMO")

#    currnet = Component(EpicsSignal, "setCurrAO")
    current = Component(EpicsSignal, "setCurrRdAI",write_pv="setCurrAO")
    currentRange = Component(EpicsSignal, "iRangeMO")

class keith2400_meas(Device):
    voltage = Component(EpicsSignalRO, "measVoltAI")
    current = Component(EpicsSignalRO, "measCurrAI")
    sense_function = Component(EpicsSignal, "senseFunctionMO", string=True, kind ="config")


class keith2400_Device(Device):
    inp = Component(keith2400_input, "")
    meas = Component(keith2400_meas, "")
    source_function = Component(EpicsSignal, "sourceFunctionMO", string=True, kind ="config")
 
keith2400 = keith2400_Device("6idb1:K24K:", name="keith2400")
