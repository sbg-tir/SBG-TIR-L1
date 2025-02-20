from __future__ import annotations
from pathlib import Path
import shutil
import re


def l1a_cal_process(l1a_bb: Path, l1a_raw_pix: Path):
    """Top level L1A CAL process"""
    l1a_pix = Path(re.sub(r"L1A_RAW_PIX", "L1A_PIX", l1a_raw_pix.name))
    l1a_rad_gain = Path(re.sub(r"L1A_RAW_PIX", "L1A_RAD_GAIN", l1a_raw_pix.name))
    shutil.copyfile(l1a_raw_pix, l1a_pix)
    shutil.copyfile(l1a_raw_pix, l1a_rad_gain)


__all__ = [
    "l1a_cal_process",
]
