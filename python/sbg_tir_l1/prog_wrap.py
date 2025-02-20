from __future__ import annotations
from loguru import logger
from contextlib import contextmanager
from pathlib import Path
import os
import sys


@contextmanager
def prog_wrap(prod_dir: Path, log_name: str, pge_name: str, debug=False):
    """Wrap around a program, handling the top level logger. We change into the
    output directory."""
    if not debug:
        # Debug is turned on by default, so only need to turn off if we don't want it
        logger.remove(0)
        logger.add(sys.stderr, level="INFO")
    opath = prod_dir.absolute()
    opath.mkdir(parents=True, exist_ok=True)
    logger.add(opath / log_name, level=("INFO" if not debug else "DEBUG"))
    curdir = os.getcwd()
    try:
        os.chdir(opath)
        with logger.catch(reraise=True):
            logger.info(f"{pge_name} processing started")
            yield
        logger.info(f"{pge_name} processing succeeded")
    except:
        logger.info(f"{pge_name} processing failed")
        sys.exit(1)
    finally:
        os.chdir(curdir)
