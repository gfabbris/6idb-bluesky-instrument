from ..devices.vortex import MySaturn

__all__ = ['load_vortex']

def load_vortex():
    vortex = MySaturn("6idVortex:", name = "vortex")
    vortex.default_kinds()
    return vortex
