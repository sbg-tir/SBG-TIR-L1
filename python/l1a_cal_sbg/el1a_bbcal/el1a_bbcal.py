import logging
import sys
import os
from osgeo import gdal

"""
This is the main function of the SBG L1A Blackbody (BB)Radiometric Calibration.
It creates for each image/scene radiometric gain/offset data per each band.
It starts with conversion of BB Focal Plan Array temperature (Kelvin) file to Radiance for each band.
There is a choice between two Kelvin-to-radiance Plank algorithms.
 Option 1: Center Wavelength Planck Function
             Source: http://ncc.nesdis.noaa.gov/data/planck.html
 Option 2: Integrate Between Bandwidth
               Source: Gouillioud,R., 2015. "ECOSTRESS_Error_Budget_2015-04-08.xlsm"
Output is pair of Radiance FPA files (temp_max and temp_min) for each OTTER bands.
It calls function el1a_2pt.py.
In there conversion of image DN to Radiance each band was done first prior to two point calibration.

Documented in SBG L1 Radiometric Calibration ATBD . TBD 
"""

# Add the parent directory of 'common' and 'el1a_2pt' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from common.log_utils import setup_log_file, log_message
from common.parse_utils import parse_pcf_file, parse_input_filename

from el1a_2pt.el1a_2pt import el1a_2pt
from setup_parameters_and_locals import setup_parameters_and_locals
from extract_uncalibrated_dn import extract_uncalibrated_dn
from extract_blackbody_data import extract_blackbody_data
from create_blackbody_radiance import create_blackbody_radiance
from prepare_for_el1a_2pt import prepare_for_el1a_2pt



def create_temp_directories(config):
    """
    Create the necessary temporary directories as specified in the PCF configuration.
    """
    try:
        directories = [
            'FPA_BB_TEMPERATURE',
            'FPA_BB_DN',
            'IMAGE_RAW_DN',
            'FPA_RADIANCE',
            'CALC_IMAGE_RADIANCE'
        ]

        for key in directories:
            directory = config.get(key)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                log_message(f"Created directory: {directory}")
            else:
                log_message(f"Directory already exists or not specified: {directory}")
    except Exception as e:
        log_message(logging.ERROR, f"Failed to create temporary directories: {e}")
        raise e


def get_blackbody_dn_dimensions(blackbody_dn_file):
    """
    Extract the dimensions (nl, ns) from a blackbody DN file using GDAL.
    """
    dataset = gdal.Open(blackbody_dn_file)
    if dataset is None:
        raise RuntimeError(f"Failed to open blackbody DN file: {blackbody_dn_file}")
    
    nl = dataset.RasterYSize
    ns = dataset.RasterXSize
    dataset = None  # Close the file
    return nl, ns



def el1a_bbcal(inph5i, inph5b, inpupf):
    try:
        # Setup the log file
        
        suffix = parse_input_filename(inph5i)
        
        log_file = setup_log_file(f"L1A_CAL_{suffix}.log")
        
        log_message(f"el1a_bbcal PROCESS STARTS.")

        log_message(f"PCF File Path: {inpupf}")  # Print to ensure it's set
        log_message(f"Image input HDF5 File Path: {inph5i}")  # Print to ensure it's set
        log_message(f"BlackBody input HDF5 File Path: {inph5b}\n")  # Print to ensure it's set

        config = parse_pcf_file(inpupf)

        result = setup_parameters_and_locals(config, inph5i, inph5b)
        log_message(f"Result from setup_parameters_and_locals: {result}\n")

        parm, local = result
        parm['suffix'] = suffix  # Set the derived suffix

        log_message("Creating necessary temporary directories...")
        create_temp_directories(config)

        log_message("\n.....Extracting Uncalibrated DN values...")
        uncalibrated_dn_files = extract_uncalibrated_dn(parm['inph5i'], parm['bands_to_process'], parm['outimg'], parm['suffix'], local['nl_image'], local['ns_image'])

        log_message("\n....Extracting blackbody data...")
        blackbody_data_files = extract_blackbody_data(parm['inph5b'], parm['bands_to_process'], parm['outbdn'], parm['suffix'])

        # Get dimensions from one of the blackbody DN files for radiance calculation
        nl, ns = get_blackbody_dn_dimensions(blackbody_data_files[0])
        log_message(f"Extracted dimensions - nl: {nl}, ns: {ns}")

        # Calculate and create Blackbody Radiance files before calling el1a_2pt
        log_message("\n....Calculating blackbody radiance...")

        for band in parm['bands_to_process']:  # Assuming what is set in config or if not default in setup param
            
            create_blackbody_radiance(
                parm['inph5b'],
                parm['inprad'],
                parm['outkel'],
                band, parm['band_parameters'],parm['planck_constants'], parm['planck_algorithm'],nl, ns,
                parm['temp_range_325'],
                parm['temp_range_295'],
                parm['suffix'],
                parm['debug'])
            
            log_message(f"Calculated blackbody radiance for band {band}")

        log_message("\n***********Preparing and calling el1a_2pt for each band ****************")
        
        for band in parm['bands_to_process']:
            if parm['debug'] > 0:
                print (f"************SUFFIX ******{suffix}")
            
            prepared_data = prepare_for_el1a_2pt(config, band, parm['suffix'], parm['debug'], uncalibrated_dn_files, blackbody_data_files)
            log_message(f"Prepared data for band {band}")
    
            # Check if any path is empty
            for key, value in prepared_data.items():
                if isinstance(value, str) and not value:
                    log_message(f"The parameter '{key}' is empty!", logging.WARNING)

            el1a_2pt(**prepared_data)

        log_message(f"el1a_bbcal processing complete.")
        log_message(f"Job completed successfully.\n")

    except Exception as e:
        log_message(f"An error occurred during processing: {e}", logging.ERROR)
        raise

