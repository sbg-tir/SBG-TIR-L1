from __future__ import annotations
from loguru import logger
from pathlib import Path
import shutil
import re

def l1b_geo_process(l1a_raw_att: Path, l1b_rad: list[Path]):
    '''Top level L1B GEO process'''
    l1b_att = Path(re.sub(r'L1A_RAW_ATT', 'L1B_ATT', l1a_raw_att.name))
    l1b_geo_qa = Path(re.sub(r'L1A_RAW_ATT', 'L1B_GEO_QA', l1a_raw_att.name))
    l1b_geo = [Path(re.sub(r'L1B_RAD', 'L1B_GEO', f.name)) for f in l1b_rad]
    shutil.copyfile(l1a_raw_att, l1b_att)
    shutil.copyfile(l1a_raw_att, l1b_geo_qa)
    for f1, f2 in zip(l1b_rad, l1b_geo):
        shutil.copyfile(f1, f2)
    
__all__ = ["l1b_geo_process",]
