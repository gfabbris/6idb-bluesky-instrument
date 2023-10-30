from ..devices import fourc, psic
from bluesky.plans import scan as bp_scan
from toolz import partition
from bluesky.preprocessors import (
    reset_positions_decorator, relative_set_decorator
)


__all__ = ["ascan", "lup"]


def ascan(detectors, *args, num=None, per_step=None, md=None):
    """
    Scan over one multi-motor trajectory.

    This is a local tweak of bluesky.plans.scan.

    Parameters
    ----------
    detectors : list
        list of 'readable' objects
    *args :
        For one dimension, ``motor, start, stop``.
        In general:

        .. code-block:: python

            motor1, start1, stop1,
            motor2, start2, start2,
            ...,
            motorN, startN, stopN

        Motors can be any 'settable' object (motor, temp controller, etc.)
    num : integer
        number of points
    per_step : callable, optional
        hook for customizing action of inner loop (messages per step).
        See docstring of :func:`bluesky.plan_stubs.one_nd_step` (the default)
        for details.
    md : dict, optional
        metadata

    See Also
    --------
    :func:`bluesky.plans.relative_inner_product_scan`
    :func:`bluesky.plans.grid_scan`
    :func:`bluesky.plans.scan_nd`
    """

    motors = [motor for motor, start, stop in partition(3, args)]
    stash = []
    for motor in motors:
        if "fourc" in motor.name:
            attr = getattr(motor, "readback", None)
            if attr is None:
                attr = getattr(motor, "user_readback")
            attr.kind = "hinted"
            stash.append(attr)
            if fourc not in detectors:
                detectors.append(fourc)

        if "psic" in motor.name:
            attr = getattr(motor, "readback", None)
            if attr is None:
                attr = getattr(motor, "user_readback")
            attr.kind = "hinted"
            stash.append(attr)

            if psic not in detectors:
                detectors.append(psic)
    
    yield from bp_scan(detectors, *args, num=num, per_step=per_step, md=md)

    for attr in stash:
        attr.kind="normal"

def lup(detectors, *args, num=None, per_step=None, md=None):
    """
    Scan over one multi-motor trajectory relative to current position.
    This is a local version of `bluesky.plans.rel_scan`. Note that the
    `per_step` cannot be set here, as it is used for dichro scans.
    Parameters
    ----------
    *args :
        For one dimension, ``motor, start, stop, number of points``.
        In general:
        .. code-block:: python
            motor1, start1, stop1,
            motor2, start2, start2,
            ...,
            motorN, startN, stopN,
            number of points
        Motors can be any 'settable' object (motor, temp controller, etc.)
    time : float, optional
        If a number is passed, it will modify the counts over time. All
        detectors need to have a .preset_monitor signal.
    detectors : list, optional
        List of detectors to be used in the scan. If None, will use the
        detectors defined in `counters.detectors`.
    lockin : boolean, optional
        Flag to do a lock-in scan. Please run pr_setup.config() prior do a
        lock-in scan.
    dichro : boolean, optional
        Flag to do a dichro scan. Please run pr_setup.config() prior do a
        dichro scan. Note that this will switch the x-ray polarization at every
        point using the +, -, -, + sequence, thus increasing the number of
        points by a factor of 4
    fixq : boolean, optional
        Flag for fixQ scans. If True, it will fix the diffractometer hkl
        position during the scan. This is particularly useful for energy scan.
        Note that hkl is moved ~after~ the other motors!
    per_step: callable, optional
        hook for customizing action of inner loop (messages per step).
        See docstring of :func:`bluesky.plan_stubs.one_nd_step` (the default)
        for details.
    md : dictionary, optional
        Metadata to be added to the run start.
    See Also
    --------
    :func:`bluesky.plans.rel_scan`
    :func:`ascan`
    """

    _md = {'plan_name': 'rel_scan'}
    md = md or {}
    _md.update(md)
    motors = [motor for motor, _, _ in partition(3, args)]

    @reset_positions_decorator(motors)
    @relative_set_decorator(motors)
    def inner_lup():
        return (yield from ascan(
            detectors, *args, num=None, per_step=None, md=None)
        )

    return (yield from inner_lup())
