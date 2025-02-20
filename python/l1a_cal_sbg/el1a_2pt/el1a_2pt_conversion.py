# el1a_2pt_conversion.py

import numpy as np
import logging
from osgeo import gdal
from el1a_2pt_masking import load_vicar_image
from el1a_2pt_gain_offset import read_vicar_data

def write_tiff_image(array, file_path):
    """
    Saves a NumPy array as a TIFF image using GDAL.

    :param array: NumPy array containing the image data.
    :param file_path: Path to save the TIFF image.
    :return: None
    """
    # Determine the dimensions of the array
    rows, cols = array.shape
    
    # Create a new TIFF file
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(file_path, cols, rows, 1, gdal.GDT_Float32)
    
    if dataset is None:
        raise ValueError(f"Could not create TIFF file at {file_path}")
   
    
    # Write the array to the TIFF file
    dataset.GetRasterBand(1).WriteArray(array)
    
    # Flush to disk and close the dataset
    dataset.FlushCache()
    dataset = None
    
    print(f"TIFF image saved to {file_path}")
    

def convert_dn_to_radiance(outwat, outimg, band, mask, unique_id, radout):
    """
    Converts DN values to radiance using the calculated gain and offset for the given band.

    :param outwat: Directory for output gain/offset and radiance and temperature files
    :param outimg: Directory where extracted uncalibrated DN image files are stored
    :param band: Band number being processed
    :param mask: The mask identifying valid pixels
    :param unique_id: Unique identifier for this run
    :param radout: Flag to control whether radiance images should be output (1 = Yes, 0 = No)
    :return: None
    """
    if radout == 0:
        logging.info(f"Radiance output is disabled for Band {band}")
        return

    logging.info(f"***Converting DN to Radiance for Band {band}")

    # Load the calculated offset and gain
    offset = load_vicar_image(f"{outwat}/b{band}_offset_{unique_id}.rel")
    gain = load_vicar_image(f"{outwat}/b{band}_gain_{unique_id}.rel")

    # Load the uncalibrated DN image
    dn_image = load_vicar_image(f"{outimg}/b{band}_image_{unique_id}.hlf")
    
    print(f"Shape of offset: {offset.shape}")
    print(f"Shape of gain: {gain.shape}")
    print(f"Shape of dn_image: {dn_image.shape}")
    
   # Ensure that the mask, offset, gain, and dn_image have compatible shapes
    if mask is not None:
        mask = mask.squeeze()
    offset = offset.squeeze()
    gain = gain.squeeze()
    dn_image = dn_image.squeeze()

    # Apply mask if necessary (assuming mask = 1 for valid data)
    if mask is not None:
        radiance = np.where(mask == 1, offset + gain * dn_image, np.nan)
        print("Radiance mask used")
    else:
        radiance = offset + gain * dn_image

    # Save the resulting radiance as a TIFF file
    radiance_file = f"{outwat}/b{band}_radiance{unique_id}.tif"
    write_tiff_image(radiance, radiance_file)

    print(f"Radiance image saved to {radiance_file}")

    # Optionaly generate and log histogram for the radiance image
    # generate_and_save_histogram(radiance, f"{outwat}/histogram_radiance_band{band}_{unique_id}.png", "Radiance Image Histogram")

    logging.info(f"Finished 2-Point DN-to-Radiance Conversion for Band {band}")

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

def convert_bb_dn_to_radiance(outwat, outbdn, inprad, band, mask, unique_id, radout):
    """
    Converts BB DN values to radiance using the calculated gain and offset for the given band.

    :param outwat: Directory where output gain/offsets and radiance and temperature files are stored
    :param outbdn: Directory where extracted blackbody DN files are stored
    :param inprad: Directory where blackbody radiance files are stored
    :param band: Band number being processed
    :param mask: The mask identifying valid pixels
    :param unique_id: Unique identifier for this run
    :param radout: Flag to control whether radiance images should be output (1 = Yes, 0 = No)
    :return: None
    """
    if radout == 0:
        logging.info(f"Radiance output is disabled for Band {band}")
        return

    logging.info(f"***Converting DN to Radiance for Band {band}")

    # Load the calculated offset and gain
    offset = load_vicar_image(f"{outwat}/b{band}_offset_{unique_id}.rel")
    gain = load_vicar_image(f"{outwat}/b{band}_gain_{unique_id}.rel")

    # Read BB dn data
    dn325 = read_vicar_data(f"{outbdn}/dn325b{band}_{unique_id}.rel")
    dn295 = read_vicar_data(f"{outbdn}/dn295b{band}_{unique_id}.rel")
    
    print(f"Shape of offset: {offset.shape}")
    print(f"Shape of gain: {gain.shape}")
    print(f"Shape of dn325: {dn325.shape}")
    print(f"Shape of dn395: {dn325.shape}")
    print(f"Shape of maks: {mask.shape}")
    
   # Ensure that the mask, offset, gain, and dn325 and dn295 have compatible shapes
    if mask is not None:
        mask_reduced = mask[:, 0:1]
    offset_reduced = offset[:, 0:1]
    gain_reduced = gain[:, 0:1]
   
 
    print(f"Shape of offset: {offset_reduced.shape}")
    print(f"Shape of gain: {gain_reduced.shape}")
    print(f"Shape of dn325: {dn325.shape}")
    print(f"Shape of dn395: {dn325.shape}")
    print(f"Shape of maks: {mask_reduced.shape}")

    # Apply mask if necessary (assuming mask = 1 for valid data)
    if mask is not None:
        radiance325 = np.where(mask_reduced == 1, offset_reduced + gain_reduced * dn325, np.nan)
        radiance295 = np.where(mask_reduced == 1, offset_reduced + gain_reduced * dn295, np.nan)
        
        print("Radiance mask used")
    else:
        radiance325 = offset_reduced + gain_reduced * dn325
        radiance295 = offset_reduced + gain_reduced * dn295
        
    print(f"Shape of radiance325: {radiance325.shape}")
    print(f"Shape of radiance295: {radiance295.shape}")
    

    # Save the resulting radiance as a TIFF file
    radiance_file_325 = f"{inprad}/b{band}_BB_radiance_325_{unique_id}.tif"
    radiance_file_295 = f"{inprad}/b{band}_BB_radiance_295_{unique_id}.tif"
    
    write_tiff_image(radiance325, radiance_file_325)
    write_tiff_image(radiance295, radiance_file_295)


    print(f"BB Radiance image saved to {radiance_file_325} and {radiance_file_295}")

    logging.info(f"Finished 2-Point BlackBody  DN-to-Radiance Conversion for Band {band}")
