"""
custom bluesky plan for scan
"""


def scan1(ctime=1):
    scaler2.stage_sigs["preset_time"] = ctime
    yield from bp.scan([pilatus100k,scaler2,pilatus100k.stats5.total], psic.phi, 22, 23, 5)
