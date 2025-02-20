
import os
import logging
from common.log_utils import log_message

def parse_pcf_file(pcf_file_path):
    """
    Parse the Processing Control File (PCF) and return a dictionary of configuration parameters.
    
    :param pcf_file_path: Path to the PCF file
    :return: Dictionary of configuration parameters
    """
    config = {}
    try:
        with open(pcf_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("#") or not line:
                    continue  # Skip comments and empty lines
                
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Convert numerical values to float if possible
                    try:
                        value = float(value)
                    except ValueError:
                        # If it's a string that contains a comma, assume it's a list of integers
                        if ',' in value:
                            value = [int(v.strip()) for v in value.split(',')]
                    
                    config[key] = value
                    
        log_message(f"Parsed PCF file: {config}\n", logging.INFO)
    except Exception as e:
        log_message(f"Failed to parse PCF file: {e}", logging.ERROR)
        raise e

    return config

def parse_input_filename(input_filename):
    """
    Parse the input filename to extract the scene ID and create a suffix.
    """
    basename = os.path.basename(input_filename)
    
    orbit = basename[12:17]
    scene = basename[18:21]
    date = basename[22:30]
    time = basename[31:37]
    build = basename[38:42]
    version = basename[43:45]
    
    suffix = f"{orbit}_{scene}_{date}T{time}_{build}_{version}"
    return suffix
