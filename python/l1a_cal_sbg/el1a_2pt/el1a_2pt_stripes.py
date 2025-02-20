# el1a_2pt_stripes.py

import numpy as np

def create_bad_stripes_mask(shape, stripe_locations):
    """
    Creates a mask to identify bad stripes in the image.

    :param shape: Shape of the image (e.g., (11264, 5400))
    :param stripe_locations: List of stripe locations in the format [(start_line, num_lines), ...]
    :return: A binary mask with bad stripes marked as 0
    """
    mask = np.ones(shape)
    for start_line, num_lines in stripe_locations:
        mask[start_line:start_line+num_lines, :] = 0
    return mask

# Example stripe locations from the VICAR procedure
stripe_locations = [
    (33, 16), (289, 16), (545, 16), (801, 16), (1057, 16), (1313, 16), (1569, 16), (1825, 16),
    (2081, 16), (2337, 16), (2593, 16), (2849, 16), (3105, 16), (3361, 16), (3617, 16), (3873, 16),
    (4129, 16), (4385, 16), (4641, 16), (4897, 16), (5153, 16), (5409, 16), (5665, 16), (5921, 16),
    (6177, 16), (6433, 16), (6689, 16), (6945, 16), (7201, 16), (7457, 16), (7713, 16), (7969, 16),
    (8225, 16), (8481, 16), (8737, 16), (8993, 16), (9249, 16), (9505, 16), (9761, 16), (10017, 16),
    (10273, 16), (10529, 16), (10785, 16), (11041, 16)
]

# Example usage
image_shape = (11264, 5400)
bad_stripes_mask = create_bad_stripes_mask(image_shape, stripe_locations)
