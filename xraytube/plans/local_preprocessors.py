""" Local decorators """

from bluesky.utils import make_decorator
from bluesky.preprocessors import finalize_wrapper
from bluesky.plan_stubs import mv, rd, null
from ophyd import Kind
from ..devices import scalerd

from ..session_logs import logger
logger.info(__file__)


def extra_devices_wrapper(plan, extras):

    hinted_stash = []

    def _stage():
        for device in extras:
            for _, component in device._get_components_of_kind(Kind.normal):
                if component.kind == Kind.hinted:
                    component.kind = Kind.normal
                    hinted_stash.append(component)
        yield from null()

    def _unstage():
        for component in hinted_stash:
            component.kind = Kind.hinted
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

    def setup():
        if count_time < 0:
            if detectors != [scalerd]:
                raise ValueError('count_time can be < 0 only if the scalerd '
                                 'is only detector used.')
            else:
                if scalerd.monitor == 'Time':
                    raise ValueError('count_time can be < 0 only if '
                                     'scalerd.monitor is not "Time".')
                original_times[scalerd] = yield from rd(scalerd.preset_monitor)
                yield from mv(scalerd.preset_monitor, abs(count_time))

        elif count_time > 0:
            for det in detectors:
                if det == scalerd:
                    original_monitor.append(scalerd.monitor)
                    det.monitor = 'Time'
                original_times[det] = yield from rd(det.preset_monitor)
                yield from mv(det.preset_monitor, count_time)
        else:
            raise ValueError('count_time cannot be zero.')

    def reset():
        for det, time in original_times.items():
            yield from mv(det.preset_monitor, time)
            if det == scalerd and len(original_monitor) == 1:
                det.monitor = original_monitor[0]

    def _inner_plan():
        yield from setup()
        return (yield from plan)

    if count_time is None:
        return (yield from plan)
    else:
        return (yield from finalize_wrapper(_inner_plan(), reset()))


extra_devices_decorator = make_decorator(extra_devices_wrapper)
configure_counts_decorator = make_decorator(configure_counts_wrapper)
