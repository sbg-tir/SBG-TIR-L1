
import sys
import os

# Ensure el1a_2pt directory is in the sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


import logging
from common.log_utils import log_message


from el1a_2pt_conversion import convert_dn_to_radiance, convert_bb_dn_to_radiance
from el1a_2pt_temp_conversion import convert_radiance_to_temperature
from el1a_2pt_gain_offset import calculate_gain_offset
from el1a_2pt_masking import create_masks


def el1a_2pt(config, outimg, outbdn, outwat, inprad, band, suffix, debug):
    """
    Main function to handle the processing of L1A data, including 2-point conversion
    and optional radiance to temperature conversion.

    :param pcf_file_path: Path to the L1A_PCF_UPF.txt file containing calibration parameters
    :param outimg: Directory where extracted DN image files are stored
    :param outbdn: Directory where extracted blackbody DN files are stored
    :param outwat: Directory for output gain/offset and radiance and temperature files
    :param inprad: Directory where blackbody radiance files are stored
    :param band: Band number being processed
    :param suffix: Suffix to use for file naming
    :param debug: Debug flag to control additional output
    :return: None
    """
    log_message(f"Starting el1a_2pt processing for Band {band} with suffix {suffix}")


    # Extract relevant corrections for each band
    corrections = {
        2: (config.get("B2IVAL", 0), config.get("B2SINC", 0)),
        3: (config.get("B3IVAL", 0), config.get("B3SINC", 0)),
        4: (config.get("B4IVAL", 0), config.get("B4SINC", 0)),
        5: (config.get("B5IVAL", 0), config.get("B5SINC", 0)),
        6: (config.get("B6IVAL", 0), config.get("B6SINC", 0))
    }

    # Extract Planck constants and other relevant values
    c1 = config.get("FIRST_CONSTANT_C1", 1.191042E08)
    c2 = config.get("SECOND_CONSTANT_C2", 14387.752)
    radout = config.get("RADIANCE_IMAGES", 1)
    rad2k = config.get("KELVIN_IMAGES", 1)

    # Extract center wavelength (CW) based on the band
    cw = config.get(f"B{band}_CW", 10.0)  # Default value for CW

    # Initialization (unique_id can be derived based on the current setup)
    #unique_id = f"{band}_{suffix}"
    unique_id = f"{suffix}"

    # Step 1: Create masks to identify good data, bad data, and stripes
    mask = create_masks(outimg, band, unique_id)
    
    # Step 2: Calculate Gain/Offset with Non-Linearity Correction
    calculate_gain_offset(inprad, outbdn, outwat, band, unique_id, corrections)

    # Step 3: 2-Point Conversion (DN to Radiance)
    if radout == 1:
        convert_dn_to_radiance(outwat, outimg, band, mask, unique_id, radout)
        convert_bb_dn_to_radiance (outwat, outbdn, inprad, band, mask, unique_id, radout)
        
        # Step 4: Radiance to Temperature Conversion
        if rad2k == 1:
            convert_radiance_to_temperature(outwat, band, unique_id, rad2k, cw, c1, c2)
    else:
        log_message(f"Skipping 2-point conversion and radiance-to-temperature conversion for Band {band} as radout is set to 0")
    
    # SWIR Processing Placeholder
    if band == 1:  # Assuming band 1 is SWIR
        log_message(f"Skipping SWIR processing for Band {band} as it is not required.")

    log_message(f"Finished el1a_2pt processing for Band {band} with suffix {suffix}********************\n")
