
import sys
import os


# Add the parent directory of 'common' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from el1a_bbcal import el1a_bbcal


if __name__ == "__main__":
    # Specify the input files original
#    inph5i = "/ops/store16/PRODUCTS/L1A_RAW_PIX/2024/02/26/L1A_RAW_PIX_31986_008_20240226T085402_0601_01.h5"
#    inph5b = "/ops/store16/PRODUCTS/L1A_BB/2024/02/26/ECOSTRESS_L1A_BB_31986_008_20240226T085402_0601_01.h5"

    # Input file for Kerry noice case 
     inph5i = "/ops/store18/PRODUCTS/L1A_RAW_PIX/2023/07/20/L1A_RAW_PIX_28557_007_20230720T064330_0712_01.h5"
     inph5b = "/ops/store18/PRODUCTS/L1A_BB/2023/07/20/ECOv002_L1A_BB_28557_007_20230720T064330_0712_01.h5"

     inpupf = "../L1A_PCF_UPF.txt"
    
    # Call el1a_bbcal with the specified files
     el1a_bbcal(inph5i, inph5b, inpupf)
