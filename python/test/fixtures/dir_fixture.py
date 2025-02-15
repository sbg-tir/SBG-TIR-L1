# This defines fixtures that gives the paths to various directories with
# test data

import os
import pytest
from pathlib import Path


@pytest.fixture(scope="function")
def unit_test_data():
    """Return the unit test directory"""
    yield Path(os.path.dirname(__file__)).parent.parent.parent / "unit_test_data"


@pytest.fixture(scope="session")
def end_to_end_run_dir():
    res = Path(os.path.dirname(__file__)).parent.parent / "end_to_end_run"
    # Create directory if it isn't already there
    res.mkdir(parents=True, exist_ok=True)
    return res
