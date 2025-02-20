import os
import sys
import numpy as np
from osgeo import gdal

# Add the parent directory of 'common' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



import logging
from common.log_utils import log_message

def planck_radiance(T, wavelength, c1, c2):
    """
    Calculate the spectral radiance using the Planck function.

    :param T: Temperature in Kelvin
    :param wavelength: Wavelength in micrometers (um)
    :param c1: First radiation constant
    :param c2: Second radiation constant
    :return: Spectral radiance in W/(m^2·sr·um)
    """

    exponent = c2 / (wavelength * T)
    
    # Prevent overflow by capping the exponent
    exponent = np.clip(exponent, 0, 700)
    
    radiance = (c1 * wavelength**-5) / (np.exp(exponent) - 1)
    
    return radiance

def plank_radiance_iterate(T, cw, bw, lw, hw, c1, c2):
    pass

def read_blackbody_rtd_data(file_path, dataset_path):
    """
    Read the blackbody RTD data from a file using GDAL.

    :param file_path: Path to the blackbody HDF5 file
    :param dataset_path: Path to the dataset within the HDF5 file
    :return: Numpy array containing the RTD data
    """
    dataset = gdal.Open(dataset_path)
    if dataset is None:
        raise RuntimeError(f"Failed to open dataset: {dataset_path}")
    
    data = dataset.ReadAsArray()
    dataset = None  # Close the file
    return data



def calculate_best_temperature(temperatures, temp_range=None):
    """
    Analyze the RTD combinations and select the best temperature based on the lowest standard deviation.
    
    :param temperatures: List of temperature readings from the sensors
    :param temp_range: Tuple specifying the valid temperature range (min, max), or None if no range check is required
    :return: Best temperature and its standard deviation, or default if no valid combination
    """
    combinations = [
        temperatures[:5],  # RTDs 1,2,3,4,5
        temperatures[:4],  # RTDs 1,2,3,4
        temperatures[:3],  # RTDs 1,2,3
        temperatures[1:5], # RTDs 2,3,4,5
        temperatures[1:4], # RTDs 2,3,4
        temperatures[2:],  # RTDs 3,4,5
        temperatures[[0,2,3,4]], # RTDs 1,3,4,5
        temperatures[[0,2,3]],   # RTDs 1,3,4
        temperatures[[0,1,3,4]], # RTDs 1,2,4,5
        temperatures[[0,1,3]],   # RTDs 1,2,4
        temperatures[1:3]+[temperatures[4]], # RTDs 2,4,5
        temperatures[[0,1,2,4]], # RTDs 1,2,3,5
        temperatures[[1,2,4]],   # RTDs 2,3,5
        temperatures[[0,1,4]],   # RTDs 1,2,5
        temperatures[[0,2,4]],   # RTDs 1,3,5
        temperatures[[0,3,4]]    # RTDs 1,4,5
    ]

    best_temp = None
    best_std = float('inf')
    
    for combo in combinations:
        mean_temp = np.mean(combo)
        std_temp = np.std(combo)

        # Apply the temperature range filter if specified
        if temp_range is not None:
            if not (temp_range[0] <= mean_temp <= temp_range[1]):
                continue

        if std_temp < best_std:
            best_std = std_temp
            best_temp = mean_temp
    
    if best_temp is None or best_std > 0.3:
        return None, None
    
    return best_temp, best_std



def save_data_vicar(data, filepath, nl, ns, dtype=gdal.GDT_Float32):
    """
    Save data to a VICAR .rel file using GDAL.

    :param data: The data to save.
    :param filepath: The path to save the file to.
    :param nl: Number of lines (height of the image).
    :param ns: Number of samples (width of the image).
    :param dtype: Data type for saving (default is Float32).
    :return: None.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Use GDAL to create the VICAR file
    driver = gdal.GetDriverByName('VICAR')
    dataset = driver.Create(filepath, ns, nl, 1, dtype)
    
    if dataset is None:
        raise RuntimeError(f"Failed to create VICAR file at {filepath}")

    # Write the data to the VICAR file
    dataset.GetRasterBand(1).WriteArray(data)
    dataset.FlushCache()
    dataset = None  # Close the file
    
    print(f"Saved data to {filepath}")

def create_blackbody_radiance(inph5b, out_dir_rad, out_dir_kel, band, bw_parameters, planck_constants, algorithm, nl, ns, temp_range_325, temp_range_295, unique_id, debug):
    """
    This calculate and save the blackbody radiance using the Planck function with provided constants.
    It will first extract blackbody temperature from the HDF5 file and calculate the best one. These BB temps are also saved in a file.  

    :param inph5b: Path to the blackbody HDF5 file
    :param out_dir_rad: Directory to save the BB radiance files
    :param out_dir_kel: Directory to save teh BB temp files
    :param band: The spectral band being processed
    :param planck_constants: a dictionary with c1, c2, (from config L1A_PCF_UPF.txt)
    :param wavelength: The center wavelength for the band (in micrometers)
    :param nl: Number of lines (height of the image)
    :param ns: Number of samples (width of the image)
    :param temp_range_325: Tuple for allowable temp range for Hot BB
    :param temp_range_295: Tuple for allowable temp range for Cold BB  
    :param unique_id: used from unique file name extention
    :return: None
    """

    rtd325_path = f'HDF5:"{inph5b}"://rtdBlackbodyGradients/RTD_325K'
    rtd295_path = f'HDF5:"{inph5b}"://rtdBlackbodyGradients/RTD_295K'

    # Load the RTD data
    rtd325 = read_blackbody_rtd_data(inph5b, rtd325_path)
    rtd295 = read_blackbody_rtd_data(inph5b, rtd295_path)

    # Calculate statistics (best mean and standard deviation)
    t325, std_325 = calculate_best_temperature(rtd325, temp_range_325)
    t295, std_295 = calculate_best_temperature(rtd295, temp_range_295)

    if t325 is None or t295 is None:
        raise RuntimeError("Error: No valid temperature found for RTD 325K or RTD 295K.")
        sys.exit(1)  # Exit the program with status code 1 (indicating error)

    if debug > 0:
        print(f"Calculated t325: {t325} with std dev: {std_325}")
        print(f"Calculated t295: {t295} with std dev: {std_295}")

    # Calculate the radiance using the Planck function either based on central wavelength or iterate over band parameters
    
    c1 = planck_constants['FIRST_CONSTANT_C1']
    c2 = planck_constants['SECOND_CONSTANT_C2']
    
    band_params = bw_parameters.get(band)
    if band_params:
        cw = band_params['CW']
        bw = band_params['BW']
        lw = band_params['LW']
        hw = band_params['HW']
        # Use the parameters for processing
        log_message (f"Processing Band {band} with CW={cw}, BW={bw}, LW={lw}, HW={hw}")
    else:
        raise RuntimeError(f"Parameters for Band {band} not found.")
        
    if (algorithm == 1): # Use Plank function with central wavelength
        radiance_325 = planck_radiance(t325, cw, c1, c2)
        radiance_295 = planck_radiance(t295, cw, c1, c2)
    elif (algorithm == 2): # Use Planck function that iterate betweeen waveband borders
        radiance_325 = planck_radiance_iterate(t325, cw, bw, lw, hw, c1, c2)
        radiance_295 = planck_radiance_iterate(t295, cw, bw, lw, hw, c1, c2)
    else:
        raise RuntimeError(f"********ERROR no Planck algorithm specifed ************")
    if debug > 0:
        print(f"Calculated radiance_325: {radiance_325}")
        print(f"Calculated radiance_295: {radiance_295}")

    # Ensure both output directories exist
    if not os.path.exists(out_dir_rad):
        raise FileNotFoundError(f"The output directory '{out_dir_rad}' does not exist.")
        sys.exit(1)

    if not os.path.exists(out_dir_kel):
        raise FileNotFoundError(f"The output directory '{out_dir_kel}' does not exist.")
        sys.exit(1)


    # Save the calculated radiance as VICAR files
    save_data_vicar(np.full((nl, ns), radiance_325, dtype=np.float32), 
                    os.path.join(out_dir_rad, f'b{band}_325rad_{unique_id}.rel'), nl, ns)
    save_data_vicar(np.full((nl, ns), radiance_295, dtype=np.float32), 
                    os.path.join(out_dir_rad, f'b{band}_295rad_{unique_id}.rel'), nl, ns)

    # Save the calculated temperatures as FPA VICAR files
    save_data_vicar(np.full((nl, ns), t325, dtype=np.float32), 
                    os.path.join(out_dir_kel, f'fpa_325_{unique_id}.rel'), nl, ns)
    save_data_vicar(np.full((nl, ns), t295, dtype=np.float32), 
                    os.path.join(out_dir_kel, f'fpa_295_{unique_id}.rel'), nl, ns)

    log_message(f"Saved radiance and FPA temperatures for band {band} to {out_dir_rad} and {out_dir_kel}")
