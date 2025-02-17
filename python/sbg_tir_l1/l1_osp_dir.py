import importlib.util
import geocal
import numpy as np
from functools import partial, cached_property
from .misc import band_to_landsat_band
import os
from loguru import logger


# Temp, this should probably get moved into geocal. But for now place here
# This should also get expanded, right now this doesn't handle resizing etc.
def _create_subset_file(self, fname, driver, Desired_map_info = None,
                        Translate_arg = None):
    r = geocal.SubRasterImage(self, Desired_map_info)
    geocal.GdalRasterImage.save(fname, driver, r, geocal.GdalRasterImage.Int16)

geocal.GdalRasterImage.create_subset_file = _create_subset_file    

class L1OspDir:
    '''This class handles the L1OspDir, such as reading the l1b_geo_config
    file.'''
    def __init__(self, l1_osp_dir):
        self.l1_osp_dir = l1_osp_dir
        logger.info(f"l1_osp_dir: {self.l1_osp_dir}")
        self.load_config()

    def setup_spice(self): 
        '''Setup the SPICEDATA environment variable'''
        v = self.spice_data_dir
        if(v is None):
            raise RuntimeError("Need to set spice_data_dir in the l1b_geo_config.py file")
        os.environ["SPICEDATA"] = str(v)
        geocal.SpiceHelper.spice_setup("geocal.ker", True)
        logger.info(f"SPICEDATA: {self.spice_data_dir}")

    # We use to just forward any variable in the l1b_geo_config module
    # to this class as an attribute. However this became a bit of a
    # global variable, where there was no central place giving all the
    # values - so you would need to search through the code or use
    # a sample config file to figure out what needed to be captured.
    # We changed now to just listing explicitly here all the variables
    # that can be read.
    #
    # This also gives a single place to change things of the logic needs
    # to get replaced with something more complicated than just reading
    # it from the config file
    #def __getattr__(self, name):
    #    '''Forward attributes to the l1b_geo_config if it is found there.'''
    #    if(hasattr(self.l1b_geo_config, name)):
    #        return getattr(self.l1b_geo_config,name)
    #    raise AttributeError
    def _gattr(self,name,default):
        if(hasattr(self.l1b_geo_config, name)):
            return getattr(self.l1b_geo_config,name)
        return default
    
    # List of variables that we read, possibly with a default value and
    # description
    CONFIG_VARIABLES = [
      ["pge_name", None, "The name of the PGE"],
      ["l1a_pge_name", None, "The name of the L1A PGE"],
      ["pge_version", None, "The  version of the PGE"],
      ["product_version", None, "The  version of the product file"],
      ["build_version", None, "The build version"],
      ["match_rad_band", None, "The band we do image matching on"],
      ["number_line_per_scene", None, "The number of lines we use per scene"],
      ["number_process", 1, "The number of processors to use in processing"],
      ["do_final_projection", False, "Do a final projection of the scenes, useful for doing diagnostics"],
      ["skip_sba", False, "Skip the SBA step, and just use the reported camera, ephemeris, attitude values without correction"],
      ["use_scene_index", False, "Use the scene number for indexing scene based files. Otherwise we use the start time in the file name as the index"],
      ["rad_match_scale", 1000, "Scaling to use on radiance data to produce image used for image matching"],
      ["generate_kmz", False, "Generate KMZ output"],
      ["generate_erdas", False, "Generate ERDAS output"],
      ["generate_quicklook", False, "Generate quicklook output"],
      ["map_band_list", None, "List of bands to use for producing KMZ and quicklook"],
      ["kmz_use_jpeg", False, "Use JPEG instead of PNG for KMZ file"],
      ["map_resolution", None, "Resolution to use for maps"],
      ["map_number_subpixel",3, "Number of subpixels to use when resampling to a map"],
      ["glt_rotated",True,"Generate GLT as a rotated map rather than North is up"],
      ["num_tiepoint_x", None, "Number of tiepoints to try for in x direction for each scene"],
      ["num_tiepoint_y", None, "Number of tiepoints to try for in y direction for each scene"],
      ["min_tp_per_scene", None, "Minimum number of tiepoints for a scene to consider the matching successful"],
      ["fftsize", 256, "Size of FFT we use with phase correlation matcher"],
      ["magnify", 4.0, "Enlarge footprint of fft window by this factor"],
      ["magmin", 2.0, "Minimum magnifier as correlation proceeds"],
      ["toler",1.5,"Tolerance for accepting tiepoints"],
      ["redo",36,"At end of matching, this number of points will be redone"],
      ["ffthalf", 2, "0 = no halving of fftsize near edge,1 = single halving of fftsize near edge,double halving of fftsize near edge"],
      ["seed",562,"seed for randomizing picmtch5 grid"],
      ["spice_data_dir", None, "the location of the SPICE data to use"],
      ["instrument_to_sc_euler", None, "The instrument to sc Euler angles"],
      ["camera_focal_length", None, "The camera focal length"],
      ["datum", None, "The datum file to use"],
      ["srtm_dir", None, "The location of the SRTM data"],
      ["match_resolution", None, "The resolution to use when matching, in meters"],
      ["ortho_base_dir", None, "The base directory for the landsat ortho base"],
      ["landsat_band", None, "The band of the landsat ortho base to use"],
      ]

    @cached_property
    def dem(self):
        '''The DEM to use.'''
        # Allow the config file to override this
        if(hasattr(self.l1b_geo_config, "dem")):
            logger.info(f"DEM: {self.l1b_geo_config.dem}")
            return self.l1b_geo_config.dem
        # Default is SrtmDem
        datum = self.datum
        srtm_dir = self.srtm_dir
        if(not datum):
            datum = os.environ["AFIDS_VDEV_DATA"] + "/EGM96_20_x100.HLF"
        if(not srtm_dir):
            srtm_dir = os.environ["ELEV_ROOT"]
        logger.info(f"Datum: {datum}")
        logger.info(f"SRTM Dir: {srtm_dir}")
        return geocal.SrtmDem(srtm_dir,False, geocal.DatumGeoid96(datum))

    @cached_property
    def ortho_base(self):
        '''The ortho base file to use.'''
        # Allow the config file to override this
        if(hasattr(self.l1b_geo_config, "ortho_base")):
            logger.info(f"Orthobase: {self.l1b_geo_config.ortho_base}")
            return self.l1b_geo_config.ortho_base
        # Otherwise, use the default Landsat7Global object
        logger.info(f"OrthoBase dir: {self.ortho_base_dir}")
        logger.info(f"Landsat band: {self.landsat_band}")
        return geocal.Landsat7Global(self.ortho_base_dir,
                                     band_to_landsat_band(self.landsat_band))

    def match_mapinfo(self, igc):
        '''Determine the MapInfo we should using for matching the given
        ImageGroundConnection with our orthobase'''
        ortho_scale = round(self.match_resolution /
                            self.ortho_base.map_info.resolution_meter)
        mibase = self.ortho_base.map_info.scale(ortho_scale, ortho_scale)
        return igc.cover(mibase)

    def write_ortho_base_subset(self, ref_fname, map_info):
        '''Create a VICAR file with the given name, containing the
        reference image we should match against.'''
        self.ortho_base.create_subset_file(ref_fname,
                                           "VICAR",
                                           Desired_map_info = map_info,
                                           Translate_arg = "-ot Int16")
        
            
    def camera(self):
        logger.info(f"Camera file: {self.l1_osp_dir /'camera.xml'}")
        cam = geocal.read_shelve(self.l1_osp_dir / "camera.xml")

        return cam
        

    def _oldcamera_(self):
        # Not ready yet, but keep code here
        logger.info(f"Camera file: {self.l1_osp_dir /'camera.xml'}")
        cam = geocal.read_shelve(self.l1_osp_dir / "camera.xml")
        # We store the euler angles and focal length separately, so we can
        # more easily update this. Get the updated values from the
        # config file.
        
        # We have used both GlasGfm and CameraParaxial as a camera. They
        # have the camera angles expressed differently
        if(isinstance(cam, geocal.SubCamera)):
            camfull = cam.full_camera
        else:
            camfull = cam
        if(self.instrument_to_sc_euler):
            if(hasattr(camfull, "euler")):
                camfull.euler = self.instrument_to_sc_euler
            else:
                camfull.angoff = [self.instrument_to_sc_euler[2],
                                  self.instrument_to_sc_euler[1],
                                  self.instrument_to_sc_euler[0]]
        if(self.camera_focal_length):
            camfull.focal_length = self.camera_focal_length
        logger.info("Camera euler angles %s", geocal.quat_to_euler(camfull.frame_to_sc))
        logger.info("Camera focal length %s", camfull.focal_length)
        return cam

    def load_config(self):
        spec = importlib.util.spec_from_file_location("l1b_geo_config",
                                                      self.l1_osp_dir / "l1b_geo_config.py")
        self.l1b_geo_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.l1b_geo_config)
        self.setup_spice()

    def geocal_accuracy_qa(self, t1, t2, number_tp):
        return self.l1b_geo_config.geocal_accuracy_qa(t1, t2, number_tp)

    def __getstate__(self):
        return {'l1_osp_dir' : self.l1_osp_dir}

    def __setstate__(self, state):
        self.l1_osp_dir = state['l1_osp_dir']
        self.load_config()
    
# Handle all our config variables, by creating properties to manage
# them
for vname, default, desc in L1OspDir.CONFIG_VARIABLES:
    setattr(L1OspDir, vname,
            property(fget=partial(L1OspDir._gattr, name=vname, default=default),
                     doc=desc))

    
    
