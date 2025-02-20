
    
import uuid

def setup_parameters_and_locals(config, inph5i, inph5b):
    """
    Set up parameters (parm) and local variables for the el1a_bbcal processing.

    :param config: Configuration parameters from the L1A_PCF_UPF.txt file
    :param inph5i: Path to the raw image file
    :param inph5b: Path to the blackbody data file
    :return: Tuple containing the parm and local dictionaries
    """

    # Set up user-supplied parameters (parm)
    parm = {
        'inph5i': inph5i,
        'inph5b': inph5b,
        'debug':config.get('VERBOSE', 1), # Verbose Debug statements (0=No; 1=Yes; 2=Yes and delete temp files)
        
        'inpupf': None,  # Placeholder, can be updated later in the proces
        'suffix': None,  # Placeholder, can be updated later in the proces

        'bands_to_process': config.get('BANDS_TO_PROCESS', list(range(1, 7))), # Assuming band 1 to 6 by defualt
        
        'outimg': config.get('IMAGE_RAW_DN', './UncalibratedDN'),
        'outbdn': config.get('FPA_BB_DN', './BlackBodyDN'),
        'outwat': config.get('CALC_IMAGE_RADIANCE', './ImgRadiance'),
        'outkel': config.get('FPA_BB_TEMPERATURE', './BlackbodyTemp'),
        'inprad': config.get('FPA_RADIANCE', './BlackbodyRadiance'),
        
        'planck_algorithm': config.get('PLANCK_ALGORITHM', 1.0),
        
        'planck_constants': {
        'FIRST_CONSTANT_C1': float(config.get('FIRST_CONSTANT_C1', 1.191042E08)),
        'SECOND_CONSTANT_C2': float(config.get('SECOND_CONSTANT_C2', 14387.752)),
        'WATTS_CONVERT': float(config.get('WATTS_CONVERT', 8.73068E-13)),
        'ITERATION_TOLERANCE': float(config.get('ITERATION_TOLERANCE', 0.00000001))
        },

        # ECOSTRESS filter parameters grouped by band number
        'band_parameters': {
            1: {'CW': float(config.get('B1_CW', 0.0)), 'BW': float(config.get('B1_BW', 0.0)), 'LW': float(config.get('B1_LW', 0.0)), 'HW': float(config.get('B1_HW', 0.0))},
            2: {'CW': float(config.get('B2_CW', 0.0)), 'BW': float(config.get('B2_BW', 0.0)), 'LW': float(config.get('B2_LW', 0.0)), 'HW': float(config.get('B2_HW', 0.0))},
            3: {'CW': float(config.get('B3_CW', 0.0)), 'BW': float(config.get('B3_BW', 0.0)), 'LW': float(config.get('B3_LW', 0.0)), 'HW': float(config.get('B3_HW', 0.0))},
            4: {'CW': float(config.get('B4_CW', 0.0)), 'BW': float(config.get('B4_BW', 0.0)), 'LW': float(config.get('B4_LW', 0.0)), 'HW': float(config.get('B4_HW', 0.0))},
            5: {'CW': float(config.get('B5_CW', 0.0)), 'BW': float(config.get('B5_BW', 0.0)), 'LW': float(config.get('B5_LW', 0.0)), 'HW': float(config.get('B5_HW', 0.0))},
            6: {'CW': float(config.get('B6_CW', 0.0)), 'BW': float(config.get('B6_BW', 0.0)), 'LW': float(config.get('B6_LW', 0.0)), 'HW': float(config.get('B6_HW', 0.0))}
        },

               
      
        'temp_range_325': (float(config.get('TEMP_RANGE_MIN_325', 310)), float(config.get('TEMP_RANGE_MAX_325', 330))),
        'temp_range_295': (float(config.get('TEMP_RANGE_MIN_295', 275)), float(config.get('TEMP_RANGE_MAX_295', 305))),
        
        'daytime': None,   # Placeholder, can be updated later in the process
        'cal_date': None,  # Placeholder, can be updated later in the process
        'cal_time': None,  # Placeholder, can be updated later in the process

    }

    # Initialize local variables
    local = {
        'id': generate_unique_id(),  # Generate a unique identifier
        'nl_image': 11264,  # Number of lines of ground surface image
        'ns_image': 5400,  # Number of samples of ground surface image 
        'nl_bb': 11264, # Number of line of BB image equal to surface image
        'ns_bb': 1 # Nimber of sample of BB image. Note avereged from 64 samples. 
    }

    return parm, local

import datetime

def generate_unique_id():
    """
    Generates a unique identifier based on the current timestamp to us if needed.
    The format will be: YYYYMMDD_HHMMSS_microseconds.
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")

