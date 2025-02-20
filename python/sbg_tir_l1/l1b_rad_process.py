from __future__ import annotations
from loguru import logger
from pathlib import Path
import shutil
import re

def l1b_rad_process(l1a_pix: Path, l1a_gain: Path, l1a_raw_att: Path):
    '''Top level L1B RAD process'''
    l1b_rad = Path(re.sub(r'L1A_PIX', 'L1B_RAD', l1a_pix.name))
    shutil.copyfile(l1a_pix, l1b_rad)
    
__all__ = ["l1b_rad_process",]
