from ophyd import ADComponent
from ophyd import ImagePlugin
from ophyd import PilatusDetector
from ophyd import SingleTrigger
from ophyd.areadetector.filestore_mixins import FileStoreHDF5IterativeWrite
from ophyd.areadetector.plugins import HDF5Plugin_V34 as HDF5Plugin
from ophyd.areadetector.plugins import OverlayPlugin_V34 as OverlayPlugin
from ophyd.areadetector.plugins import ROIPlugin_V34 as ROIPlugin
from ophyd.areadetector.plugins import StatsPlugin_V34 as StatsPlugin
from ophyd.areadetector.filestore_mixins import FileStoreIterativeWrite
from apstools.devices import AD_EpicsHdf5FileName
import os

PILATUS_FILES_ROOT = "/home/sector6/6idb"
BLUESKY_FILES_ROOT = "/beams/USER6IDB/data"
TEST_IMAGE_DIR = "pilatus100k/%Y/%m/%d/"

class MyHDF5EpicsIterativeWriter(AD_EpicsHdf5FileName, FileStoreIterativeWrite): pass
 
class MyHDF5Plugin(MyHDF5EpicsIterativeWriter, HDF5Plugin): ...
 
class MyPilatusDetector(SingleTrigger, PilatusDetector):
     """Pilatus detector"""

     image = ADComponent(ImagePlugin, "image1:")
     hdf1 = ADComponent(
        MyHDF5Plugin,
        "HDF1:",
        write_path_template=os.path.join(PILATUS_FILES_ROOT, TEST_IMAGE_DIR),
        read_path_template=os.path.join(BLUESKY_FILES_ROOT, TEST_IMAGE_DIR),
        kind="normal",
     )
     over1 = ADComponent(OverlayPlugin, 'Over1:')
     roi1 = ADComponent(ROIPlugin, 'ROI1:')
     roi2 = ADComponent(ROIPlugin, 'ROI2:')
     roi3 = ADComponent(ROIPlugin, 'ROI3:')
     roi4 = ADComponent(ROIPlugin, 'ROI4:')
     stats1 = ADComponent(StatsPlugin, 'Stats1:', kind="normal")
     stats2 = ADComponent(StatsPlugin, 'Stats2:')
     stats3 = ADComponent(StatsPlugin, 'Stats3:')
     stats4 = ADComponent(StatsPlugin, 'Stats4:')
     stats5 = ADComponent(StatsPlugin, 'Stats5:', kind="normal")

   #   read_attrs = "hdf1 roi1 roi2 roi3 roi4 stats2 stats2 stats3 stats4 stats5".split()
   #   hints = {"fields": "roi1 roi2 roi3 roi4 stats2 stats2 stats3 stats4 stats5".split()}

 
pilatus100k = MyPilatusDetector("s6_pilatus:", name="pilatus100k")
pilatus100k.hdf1.create_directory.put(-5)
pilatus100k.cam.stage_sigs["image_mode"] = "Single"
pilatus100k.cam.stage_sigs["num_images"] = 1
pilatus100k.cam.stage_sigs["acquire_time"] = 1
pilatus100k.cam.stage_sigs["trigger_mode"] = "Internal"
pilatus100k.cam.stage_sigs["acquire_period"] = 0.105
pilatus100k.hdf1.stage_sigs["file_write_mode"] = "Capture"
pilatus100k.hdf1.stage_sigs["lazy_open"] = 1
pilatus100k.hdf1.stage_sigs["compression"] = "blosc"
pilatus100k.hdf1.stage_sigs["file_template"] = "%s%s_%5.5d.h5"
del pilatus100k.hdf1.stage_sigs["capture"]
pilatus100k.hdf1.stage_sigs["capture"] = 1
pilatus100k.read_attrs += "hdf1 roi1 roi2 roi3 roi4 stats2 stats2 stats3 stats4 stats5".split()
