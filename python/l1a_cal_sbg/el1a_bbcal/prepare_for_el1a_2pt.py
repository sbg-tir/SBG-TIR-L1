
def prepare_for_el1a_2pt(config, band, suffix, debug, uncalibrated_dn_files, blackbody_data_files):
    """
    Prepare the necessary data and parameters for calling el1a_2pt.

    :param config: Configuration parameters from the L1A_PCF_UPF.txt file
    :param band: The spectral band being processed
    :param suffix: Suffix for identifying the processing run (e.g., date or unique ID)
    :param debug: Debug level (0 = No, 1 = Yes, 2 = Yes + delete temp files)
    :param uncalibrated_dn_files: List of paths to the uncalibrated DN files
    :param blackbody_data_files: List of paths to the blackbody data files
    # :param pcf_file_path: Path to the Processing Control File
    :return: Dictionary of prepared parameters to pass to el1a_2pt
    """

    # Ensure the pcf_file_path is passed correctly
    #if not pcf_file_path:
        #raise RuntimeError("PCF file path is empty!")

    # Identify the correct DN and blackbody files for the specified band
    dn_file = next((f for f in uncalibrated_dn_files if f'b{band}_image' in f), None)
    bb325_file = next((f for f in blackbody_data_files if f'dn325b{band}' in f), None)
    bb295_file = next((f for f in blackbody_data_files if f'dn295b{band}' in f), None)

    if not dn_file or not bb325_file or not bb295_file:
        raise RuntimeError(f"Missing data files for band {band}. DN: {dn_file}, BB325: {bb325_file}, BB295: {bb295_file}")

    # Define the output directories
    outimg_dir = config.get('IMAGE_RAW_DN')
    outbdn_dir = config.get('FPA_BB_DN')
    outwat_dir = config.get('CALC_IMAGE_RADIANCE')

    # Prepare the dictionary of parameters to pass to el1a_2pt
    el1a_2pt_params = {
        'config': config,
        'outimg': outimg_dir,
        'outbdn': outbdn_dir,
        'outwat': outwat_dir,
        'inprad': config.get('FPA_RADIANCE', './BlackbodyRadiance'),
        'band': band,
        'suffix': suffix,
        'debug': debug,
    }

    return el1a_2pt_params
