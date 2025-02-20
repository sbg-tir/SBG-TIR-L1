import os
import numpy as np
from osgeo import gdal

def extract_blackbody_data(inph5b, bands_to_process, outbdn_dir, unique_id):
    """
    Extract blackbody data from the HDF5 file, average the data across samples,
    and save as VICAR file (note that it can be changed if preferd to GTiff).

    :param inph5b: Path to the blackbody HDF5 file
    :param bands_to_process: Configuration parameters indicating what bands to process
    :param unique_id: part of the input file name to ne ised in the output file name
    :param outbdn_dir: Directory to save the extracted blackbody data files
    :return: List of paths to the extracted blackbody data files
    """

    # Ensure the output directory exists
    if not os.path.exists(outbdn_dir):
        os.makedirs(outbdn_dir)

    # Define the bands to extract, assuming they are specified in the config or inferred from the data
    # bands_to_process = config.get('bands_to_process', range(1, 7))  # Assuming bands 1 to 6 by default

    # Loop through each band and extract the corresponding blackbody data
    extracted_files = []
    for band in bands_to_process:
        output_file_325 = os.path.join(outbdn_dir, f'dn325b{band}_{unique_id}.rel') # VICAR file
        output_file_295 = os.path.join(outbdn_dir, f'dn295b{band}_{unique_id}.rel') # VICAR file

        # Use GDAL to read the HDF5 datasets
        hdf5_dataset_path_325 = f'HDF5:"{inph5b}"://BlackBodyPixels/b{band}_blackbody_325'
        hdf5_dataset_path_295 = f'HDF5:"{inph5b}"://BlackBodyPixels/b{band}_blackbody_295'

        dataset_325 = gdal.Open(hdf5_dataset_path_325)
        dataset_295 = gdal.Open(hdf5_dataset_path_295)

        if dataset_325 is None or dataset_295 is None:
            raise RuntimeError(f"Failed to open HDF5 dataset for band {band}")

        # Read the data as numpy arrays
        data_325 = dataset_325.ReadAsArray()
        data_295 = dataset_295.ReadAsArray()

        print(f"Original shape of band {band} data (325K): {data_325.shape}")
        print(f"Original shape of band {band} data (295K): {data_295.shape}")

        # Average across the second axis (samples)
        avg_325 = np.mean(data_325, axis=1).reshape(-1, 1)
        avg_295 = np.mean(data_295, axis=1).reshape(-1, 1)

        print(f"Averaged shape of band {band} data (325K): {avg_325.shape}")
        print(f"Averaged shape of band {band} data (295K): {avg_295.shape}")

        # Save the averaged data as VICAR files
        driver = gdal.GetDriverByName("VICAR")
        out_325 = driver.Create(output_file_325, 1, avg_325.shape[0], 1, gdal.GDT_Float32)
        out_325.GetRasterBand(1).WriteArray(avg_325)

        out_295 = driver.Create(output_file_295, 1, avg_295.shape[0], 1, gdal.GDT_Float32)
        out_295.GetRasterBand(1).WriteArray(avg_295)

        if out_325 is None or out_295 is None:
            raise RuntimeError(f"Failed to save band {band} data")

        print(f"Extracted and averaged band {band} blackbody data (325K) to {output_file_325}")
        print(f"Extracted and averaged band {band} blackbody data (295K) to {output_file_295}")
        
        extracted_files.append(output_file_325)
        extracted_files.append(output_file_295)

    return extracted_files
