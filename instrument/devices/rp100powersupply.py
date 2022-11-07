from ophyd import Component
from ophyd import Device
from ophyd import EpicsSignal
from ophyd import EpicsSignalRO
# from ophyd import EpicsSignalWithRBV  #  PV:name and PV:name_RBV
    # EpicsSignalWithRBV same as EpicsSignal, "PV:name" , write_pv=""

class RP100_Output1_Device(Device):
    slew = Component(EpicsSignal, "rOutput1_Slew", write_pv="wOutput1_Slew")
    temperature = Component(EpicsSignal, "VoltageLimit1.B", write_pv="VoltageLimit1.INPB")
    voltage = Component(EpicsSignalRO, "rOutput1_Voltage")
    voltage_pv = Component(EpicsSignal, "VoltageLimit1.INPA")

class RP100_Output2_Device(Device):
    slew = Component(EpicsSignal, "rOutput2_Slew", write_pv="wOutput2_Slew")
    voltage = Component(EpicsSignalRO, "rOutput2_Voltage")
    voltage_pv = Component(EpicsSignal, "VoltageLimit2.INPA")
    temperature = Component(EpicsSignal, "VoltageLimit2.B", write_pv="VoltageLimit2.INPB")

class RP100_Device(Device):
    output1 = Component(RP100_Output1_Device, "")
    output2 = Component(RP100_Output2_Device, "")

rp100 = RP100_Device("6idRazorbill:D1:", name="rp100")
