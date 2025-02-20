# el1a_2pt_temp_conversion.py

import numpy as np
import logging

from el1a_2pt_conversion import write_tiff_image

from osgeo import gdal

def load_tiff_image(file_path):
    """
    Loads a TIFF image using GDAL and returns it as a NumPy array.

    :param file_path: Path to the TIFF image file.
    :return: NumPy array containing the image data.
    """
    dataset = gdal.Open(file_path)
    if not dataset:
        raise ValueError(f"Unable to open TIFF file {file_path}")
    
    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray()
    
    return data

def convert_radiance_to_temperature(outwat, band, unique_id, rad2k, cw, c1, c2):
    """
    Converts radiance to temperature for the given band.

    :param outwat: Directory where output gain/offset radiance and temperature files are stored
    :param band: Band number being processed
    :param unique_id: Unique identifier for this run
    :param rad2k: Flag to control whether radiance is converted to temperature (1 = Yes, 0 = No)
    :param cw: Center wavelength for the band
    :param c1: First Planck constant
    :param c2: Second Planck constant
    :return: None
    """
    if rad2k == 0:
        logging.info(f"Skipping radiance-to-temperature conversion for Band {band} as rad2k is set to 0")
        return

    logging.info(f"***Converting Radiance to Temperature for Band {band}")

    # Load the radiance image
    radiance_file = f"{outwat}/b{band}_radiance{unique_id}.tif"
    radiance = load_tiff_image(radiance_file)

  
    # Optionally convert radiance to temperature using the Planck equation
    if rad2k:
        temperature = c2 / (cw * np.log((c1 / (cw**5 * radiance)) + 1))
        # Save the resulting temperature as a TIFF file
        temperature_file = f"{outwat}/b{band}_temperature{unique_id}.tif"
        write_tiff_image(temperature, temperature_file)
        logging.info(f"Temperature image saved to {temperature_file}")
    else:
        logging.info("Radiance to temperature conversion skipped as rad2k is False.")
        
    # Optionally generate and log histogram for the temperature image
    # generate_and_save_histogram(temperature, f"{outwat}/histogram_temperature_band{band}_{unique_id}.png", "Temperature Image Histogram")

    logging.info(f"Finished Radiance-to-Temperature Conversion for Band {band}")

def generate_and_save_histogram(data, output_path, title):
    """
    Generates and saves a histogram of the given data.

    :param data: The data for which to generate the histogram
    :param output_path: The file path where the histogram will be saved
    :param title: The title of the histogram
    :return: None
    """
    import matplotlib.pyplot as plt

    plt.figure()
    plt.hist(data.flatten(), bins=100, color='blue', alpha=0.7)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    logging.info(f"Saved histogram to {output_path}")
