# el1a_2pt_masking.py

import numpy as np
import logging
from osgeo import gdal
from el1a_2pt_stripes import create_bad_stripes_mask
import matplotlib.pyplot as plt

def create_masks(outimg, band, unique_id):
    """
    Creates binary masks to identify good data, bad data, and stripes in the image.
    Also generates histograms for the data and the masks.

    :param outimg: Directory where extracted DN images are stored
    :param band: Band number being processed
    :param unique_id: Unique identifier for this run
    :return: The created mask
    """
    logging.info(f"***Creating Masks and Histograms for Band {band}")
  
    # Load the processed image data
    image_path = f"{outimg}/b{band}_image_{unique_id}.hlf"
    image_data = load_vicar_image(image_path)
    
    # Create initial mask based on image data
    mask = np.where((image_data > 0) & (image_data <= 32000), 1, 0)

    # Apply bad stripes mask if applicable
    if band in [1, 2, 6]:  # Bands that have stripes
        stripe_locations = [
            (33, 16), (289, 16), (545, 16), (801, 16), (1057, 16), (1313, 16), (1569, 16), (1825, 16),
            (2081, 16), (2337, 16), (2593, 16), (2849, 16), (3105, 16), (3361, 16), (3617, 16), (3873, 16),
            (4129, 16), (4385, 16), (4641, 16), (4897, 16), (5153, 16), (5409, 16), (5665, 16), (5921, 16),
            (6177, 16), (6433, 16), (6689, 16), (6945, 16), (7201, 16), (7457, 16), (7713, 16), (7969, 16),
            (8225, 16), (8481, 16), (8737, 16), (8993, 16), (9249, 16), (9505, 16), (9761, 16), (10017, 16),
            (10273, 16), (10529, 16), (10785, 16), (11041, 16)
        ]
        stripe_mask = create_bad_stripes_mask(image_data.shape, stripe_locations)
        mask[stripe_mask == 0] = -1  # Mark stripes as -1 in the mask

    # Apply bad lines mask for Band 5
    if band == 5:
        badlines_mask = create_badlines_mask(image_data.shape)
        mask[badlines_mask == 0] = 0  # Mark bad lines as 0 (bad data)

    # Save mask to a file
    save_mask(mask, f"{outimg}/mask_{unique_id}.npy")

    # Generate and log histogram for the image data
    generate_and_save_histogram(image_data, f"{outimg}/histogram_image_band{band}_{unique_id}.png", "Image Data Histogram")

    # Generate and log histogram for the mask
    generate_and_save_histogram(mask, f"{outimg}/histogram_mask_band{band}_{unique_id}.png", "Mask Histogram")

    # Log the result
    mean = np.mean(mask)
    std_dev = np.std(mask)
    logging.info(f"Band {band} Mask Mean={mean} SD={std_dev}")

    return mask

def load_vicar_image(image_path):
    """
    Loads a VICAR image file using GDAL.

    :param image_path: Path to the VICAR image file
    :return: The image data as a numpy array
    """
    dataset = gdal.Open(image_path, gdal.GA_ReadOnly)
    if dataset is None:
        raise IOError(f"Unable to open HERE {image_path} using GDAL")
    
    band = dataset.GetRasterBand(1)
    image_data = band.ReadAsArray()
    
    return image_data


def create_badlines_mask(shape):
    """
    Creates a mask to identify bad lines for band 5.
    
    :param shape: Shape of the image (e.g., (11264, 5400))
    :return: A binary mask with bad lines marked as 0
    """
    mask = np.ones(shape)
    bad_lines = [219, 220, 475, 476, 731, 732, 987, 988, 1243, 1244, 1499, 1500, 1755, 1756, 2011, 2012,
                 2267, 2268, 2523, 2524, 2779, 2780, 3035, 3036, 3291, 3292, 3547, 3548, 3803, 3804,
                 4059, 4060, 4315, 4316, 4571, 4572, 4827, 4828, 5083, 5084, 5339, 5340, 5595, 5596,
                 5851, 5852, 6107, 6108, 6363, 6364, 6619, 6620, 6875, 6876, 7131, 7132, 7387, 7388,
                 7643, 7644, 7899, 7900, 8155, 8156, 8411, 8412, 8667, 8668, 8923, 8924, 9179, 9180,
                 9435, 9436, 9691, 9692, 9947, 9948, 10203, 10204, 10459, 10460, 10715, 10716, 10971, 10972, 11227, 11228]
    for line in bad_lines:
        mask[line, :] = 0
    return mask

def save_mask(mask, path):
    """
    Saves the mask to a file.
    
    :param mask: The mask array to save
    :param path: The file path where the mask will be saved
    """
    np.save(path, mask)
    logging.info(f"Saved mask to {path}")

def generate_and_save_histogram(data, output_path, title):
    """
    Generates and saves a histogram of the given data.

    :param data: The data for which to generate the histogram
    :param output_path: The file path where the histogram will be saved
    :param title: The title of the histogram
    """
    plt.figure()
    plt.hist(data.flatten(), bins=100, color='blue', alpha=0.7)
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    logging.info(f"Saved histogram to {output_path}")
