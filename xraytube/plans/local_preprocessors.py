""" Local decorators """

from bluesky.utils import make_decorator
from bluesky.preprocessors import finalize_wrapper
from bluesky.plan_stubs import mv, rd, null
from ophyd import Kind
from ..devices import scaler1

from ..session_logs import logger
logger.info(__file__)


def extra_devices_wrapper(plan, extras, motors=[]):

    hinted_stash = []
    _diff = []

    def _stage():
		
        for motor in motors:
            if ("psic" in motor.name) or ("fourc" in motor.name):
                _diff.append(motor)
		
        for device in extras:
            # if device.name in ("psic", "fourc"):
            #     device.setup_kinds()
            # else:
            for _, component in device._get_components_of_kind(Kind.normal):
                if component.kind == Kind.hinted:
                    component.kind = Kind.normal
                    hinted_stash.append(component)
                  
        if len(_diff) != 0:
            _diff[0].parent.setup_kinds(hinted=_diff)

        yield from null()

    def _unstage():
        for component in hinted_stash:
            component.kind = Kind.hinted
        if len(_diff) != 0:
            _diff[0].parent.setup_kinds()
        yield from null()

    def _inner_plan():
        yield from _stage()
        return (yield from plan)

    if len(extras) != 0:
        return (yield from finalize_wrapper(_inner_plan(), _unstage()))
    else:
        return (yield from plan)


def configure_counts_wrapper(plan, detectors, count_time):
    """
    Set all devices with a `preset_monitor` to the same value.

    The original setting is stashed and restored at the end.

    Parameters
    ----------
    plan : iterable or iterator
        a generator, list, or similar containing `Msg` objects
    monitor : float or None
        If None, the plan passes through unchanged.

    Yields
    ------
    msg : Msg
        messages from plan, with 'set' messages inserted
    """
    original_times = {}
    original_monitor = []

    def _stage():
        if count_time < 0:
            if detectors != [scaler1]:
                raise ValueError('count_time can be < 0 only if the scaler1 '
                                 'is only detector used.')
            else:
                if scaler1.monitor == 'Seconds':
                    raise ValueError('count_time can be < 0 only if '
                                     'scaler1.monitor is not "Seconds".')
                original_times[scaler1] = yield from rd(scaler1.preset_monitor)
                yield from mv(scaler1.preset_monitor, abs(count_time))

        elif count_time > 0:
            for det in detectors:
                if det == scaler1:
                    original_monitor.append(scaler1.monitor)
                    det.monitor = 'Seconds'
                original_times[det] = yield from rd(det.preset_monitor)
                # yield from mv(det.preset_monitor, count_time)
                det.preset_monitor.put(count_time)
        else:
            raise ValueError('count_time cannot be zero.')

        yield from null()



    def _unstage():
        for det, time in original_times.items():
            # yield from mv(det.preset_monitor, time)
            det.preset_monitor.put(time)
            if det == scaler1 and len(original_monitor) == 1:
                det.monitor = original_monitor[0]
        yield from null()

    def _inner_plan():
        yield from _stage()
        return (yield from plan)

    if count_time is None:
        return (yield from plan)
    else:
        return (yield from finalize_wrapper(_inner_plan(), _unstage()))
        #return (yield from finalize_wrapper(reset(), _inner_plan()))


extra_devices_decorator = make_decorator(extra_devices_wrapper)
configure_counts_decorator = make_decorator(configure_counts_wrapper)
