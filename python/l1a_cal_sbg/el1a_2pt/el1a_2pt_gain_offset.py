
# el1a_2pt_gain_offset.py

import numpy as np
import logging
from osgeo import gdal

def read_vicar_data(file_path):
    dataset = gdal.Open(file_path)
    if not dataset:
        raise ValueError(f"Unable to open file {file_path}")

    # Read the data as a NumPy array
    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray()

    return data


def save_offset_gain(offset, gain, outwat, band, unique_id):
    """
    Saves the offset and gain arrays to VICAR-compatible .rel files using GDAL.

    :param offset: Calculated offset array
    :param gain: Calculated gain array
    :param outwat: Directory for output gain/offset and radiance and temperature files
    :param band: Band number being processed
    :param unique_id: Unique identifier for this process
    :return: None
    """
    def write_vicar_image(array, file_path):
        """
        Saves a NumPy array as a VICAR image using GDAL.

        :param array: NumPy array containing the image data.
        :param file_path: Path to save the VICAR image.
        :return: None
        """
        rows, cols = array.shape
        
        # Create a new VICAR file
        driver = gdal.GetDriverByName('VICAR')
        dataset = driver.Create(file_path, cols, rows, 1, gdal.GDT_Float32)
        
        if dataset is None:
            raise ValueError(f"Could not create VICAR file at {file_path}")
        
        # Write the array to the VICAR file
        dataset.GetRasterBand(1).WriteArray(array)
        
        # Flush to disk and close the dataset
        dataset.FlushCache()
        dataset = None
        
        print(f"VICAR image saved to {file_path}")

    # Ensure offset and gain are 2D arrays
    if offset.ndim == 3:
        offset = offset.squeeze()
    if gain.ndim == 3:
        gain = gain.squeeze()

    print(f"Shape of offset save: {offset.shape}")
    print(f"Shape of gain save: {gain.shape}")


    # Save the offset and gain arrays as VICAR files
    offset_file = f"{outwat}/b{band}_offset_{unique_id}.rel"
    gain_file = f"{outwat}/b{band}_gain_{unique_id}.rel"
    
    write_vicar_image(offset, offset_file)
    write_vicar_image(gain, gain_file)

    print(f"Offset and Gain VICAR images saved to {outwat}")

    

def calculate_gain_offset(inprad, outbdn, outwat, band, unique_id, corrections):
    """
    Calculates the gain and offset for the given band and applies them to the image data.
    Also applies non-linearity correction where applicable.

    :param inprad: Directory where blackbody radiance files are stored
    :param outbdn: Directory where extrcated blackbody DN files are stored
    :param outwat: Directory for output gain/offset and radiance and temperature files
    :param band: Band number being processed
    :param unique_id: Unique identifier for this run
    :param corrections: Dictionary containing linearity corrections for each band
    :return: None
    """
    logging.info(f"***Calculating Gain/Offset for Band {band}")

    # Load the blackbody radiance data
    rad325 = read_vicar_data(f"{inprad}/b{band}_325rad_{unique_id}.rel")
    rad295 = read_vicar_data(f"{inprad}/b{band}_295rad_{unique_id}.rel")

    # Load the extracted blackbody DN data
    dn325 = read_vicar_data(f"{outbdn}/dn325b{band}_{unique_id}.rel")
    dn295 = read_vicar_data(f"{outbdn}/dn295b{band}_{unique_id}.rel")


    # Ensure all arrays have the same shape before proceeding
    if rad325.shape != rad295.shape or rad325.shape != dn325.shape or rad325.shape != dn295.shape:
        raise ValueError("Array shapes are not consistent. Cannot perform element-wise operations.")
        # Print the shapes of the arrays
        print(f"rad325 blackbody radiance shape: {rad325.shape}")
        print(f"rad295 blackbody radiance shape: {rad295.shape}")
        print(f"dn325 blackbody dn shape: {dn325.shape}")
        print(f"dn295 blackbody dn shape: {dn295.shape}")

    # Calculate the offset (a)
    offset = (rad325 * dn295 - rad295 * dn325) / (dn295 - dn325)

    # Calculate the gain (b)
    gain = (rad325 - rad295) / (dn325 - dn295)
    
    print(f"Shape of offset calculate: {offset.shape}")
    print(f"Shape of gain calculate: {gain.shape}")
    

    # Apply non-linearity correction if applicable
    if band in corrections:
        ival, sinc = corrections[band]
        correction = create_nonlinearity_correction(offset.shape, ival, sinc)
        offset += correction
        logging.info(f"Applied non-linearity correction for Band {band}")

    # Duplicate the gain/offset 5400 times to match the image size (11264x5400)
    offset_full = np.tile(offset[:, np.newaxis], (1, 5400))
    gain_full = np.tile(gain[:, np.newaxis], (1, 5400))

    # Saves the gain and offset to to outwat directory
    save_offset_gain(offset_full, gain_full, outwat, band, unique_id)

    logging.info(f"Finished calculating and saving Gain/Offset for Band {band}")

def create_nonlinearity_correction(shape, ival, sinc):
    """
    Creates the non-linearity correction wedge.

    :param shape: The shape of the offset array (e.g., (11264,))
    :param ival: The initial value for the non-linearity correction
    :param sinc: The increment value for the non-linearity correction
    :return: The non-linearity correction array
    """
    correction = ival + np.arange(shape[0]) * sinc
    return correction[:, np.newaxis]  # Expand to match the 11264x1 shape


