"""
Slits
"""
__all__ = ['sl1', 'sl2', 'sl3', 'sl4']

from ophyd import Device, FormattedComponent, EpicsMotor, MotorBundle, Component
from apstools.devices import PVPositionerSoftDoneWithStop
from ..framework import sd
from ..session_logs import logger
logger.info(__file__)


class SlitDevice(Device):

    # Setting motors
    top = FormattedComponent(EpicsMotor, '{prefix}{_motorsDict[top]}',
                             labels=('motors', 'slits'))

    bot = FormattedComponent(EpicsMotor, '{prefix}{_motorsDict[bot]}',
                             labels=('motors', 'slits'))

    out = FormattedComponent(EpicsMotor, '{prefix}{_motorsDict[out]}',
                             labels=('motors', 'slits'))

    inb = FormattedComponent(EpicsMotor, '{prefix}{_motorsDict[inb]}',
                             labels=('motors', 'slits'))

    # Setting pseudo positioners
    vcen = FormattedComponent(
        PVPositionerSoftDoneWithStop,
        '{prefix}{_slit_prefix}',
        readback_pv='Vt2.D',
        setpoint_pv='Vcenter.VAL',
        labels=('slits',)
    )

    vsize = FormattedComponent(
        PVPositionerSoftDoneWithStop,
        '{prefix}{_slit_prefix}',
        readback_pv='Vt2.C',
        setpoint_pv='Vsize.VAL',
        labels=('slits',)
    )

    hcen = FormattedComponent(
        PVPositionerSoftDoneWithStop,
        '{prefix}{_slit_prefix}',
        readback_pv='Ht2.D',
        setpoint_pv='Hcenter.VAL',
        labels=('slits',)
    )

    hsize = FormattedComponent(
        PVPositionerSoftDoneWithStop,
        '{prefix}{_slit_prefix}',
        readback_pv='Ht2.C',
        setpoint_pv='Hsize.VAL',
        labels=('slits',)
    )

    def __init__(self, PV, name, motorsDict, slitnum, **kwargs):

        self._motorsDict = motorsDict
        self._slit_prefix = f'Slit_{slitnum}'

        super().__init__(prefix=PV, name=name, **kwargs)


class Slits4GapCenter_6IDB(MotorBundle):
    hcen = Component(EpicsMotor, "m5", labels=("motor",))
    hsize = Component(EpicsMotor, "m6", labels=("motor",))
    vcen = Component(EpicsMotor, "m7", labels=("motor",))
    vsize = Component(EpicsMotor, "m8", labels=("motor",))


# slit1
sl1 = SlitDevice('6idb1:', 'sl1',
                   {'top': 'm42', 'bot': 'm41', 'out': 'm43', 'inb': 'm44'},
                   1)
sl1.vcen.tolerance.put(0.003)
sl1.vsize.tolerance.put(0.009)
sd.baseline.append(sl1)

# slit2
sl2 = SlitDevice('6idb1:', 'sl2',
                   {'top': 'm45', 'bot': 'm46', 'out': 'm47', 'inb': 'm48'},
                   2)
sd.baseline.append(sl2)

# slit3
sl3 = SlitDevice('6idb1:', 'sl3',
                    {'top': 'm1', 'bot': 'm2', 'out': 'm4', 'inb': 'm3'},
                    3)
sd.baseline.append(sl3)

# slit4
sl4 = Slits4GapCenter_6IDB("6idb1:", name="sl4", labels=("slits",))
