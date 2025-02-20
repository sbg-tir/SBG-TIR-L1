import os
from osgeo import gdal
import logging
from common.log_utils import log_message

def extract_uncalibrated_dn(inph5i, bands_to_process, outimg_dir, unique_id, nl, ns):
    """
    Extract Uncalibrated DN values from the raw image HDF5 file and save them as VICAR or TIFF files.

    :param inph5i: Path to the raw image HDF5 file
    :param bands_to_process: Configuration parameters indicating what bands to process
    :param outimg_dir: Directory to save the extracted DN files
    :param unique_id: part of the input file name to ne ised in the output file name
    ;param nl,ns: expected size of the image file
    :return: Path to the directory containing the extracted DN files
     """

    # Confirm output directory exists
    if not os.path.exists(outimg_dir):
        os.makedirs(outimg_dir)    
  

    # Loop through each band and extract the corresponding DN data
    extracted_files = []
    for band in bands_to_process:
        output_file = os.path.join(outimg_dir, f'b{band}_image_{unique_id}.hlf')  # VICAR format

        # Use GDAL to translate the HDF5 dataset to VICAR or TIFF format
        # The HDF5 path adapted based on the on the structure of input HDF5 file
        hdf5_dataset_path = f'HDF5:"{inph5i}"://UncalibratedPixels/pixel_data_{band}'

        # Open the HDF5 dataset
        dataset = gdal.Open(hdf5_dataset_path)
        if dataset is None:
            raise RuntimeError(f"Failed to open HDF5 dataset for band {band}")

        # Translate the dataset to the desired output format
        driver = gdal.GetDriverByName("VICAR")  # Can be changed to GTiff if preferred
        out_dataset = driver.CreateCopy(output_file, dataset)

        number_l, number_s = dataset.RasterYSize, dataset.RasterXSize
        log_message(f"Input Image Size is: {nl} Lines x {ns} Samples")

        if number_l != nl or number_s != ns:
            logging.error(f"ERROR: {output_file} has Incorrect Image Size")
            raise ValueError(f"Incorrect image size: {number_l}x{number_s} (expected {nl}x{ns})")

        if out_dataset is None:
            raise RuntimeError(f"Failed to save band {band} to {output_file}")
        
        log_message(f"Extracted band {band} DN to {output_file}")
        extracted_files.append(output_file)

    return extracted_files
