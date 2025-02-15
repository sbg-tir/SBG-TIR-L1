import warnings
from loguru import logger
import pytest
import re

# ------------------------------------------
# Set up to warnings go to the logger
# ------------------------------------------
showwarning_ = warnings.showwarning


def showwarning(message, *args, **kwargs):
    # Swig has numerous warning messages that we can't do anything about.
    # There is a ticket for this (see https://github.com/swig/swig/issues/2881), and
    # this might get fixed in swig 4.4. But for now at least, these are present. Strip
    # these out, we can't do anything about these warnings and don't want to see them.
    if not re.search(r"has no __module__ attribute", str(message)):
        logger.warning(message)
    # showwarning_(message, *args, **kwargs)


warnings.showwarning = showwarning

# ------------------------------------------
# Various markers we use throughout the tests
# ------------------------------------------

# Short hand for marking as unconditional skipping. Good for tests we
# don't normally run, but might want to comment out for a specific debugging
# reason.
skip = pytest.mark.skip

# Marker for long tests. Only run with --run-long
long_test = pytest.mark.long_test

# ------------------------------------------
# Based on markers, we skip tests
# ------------------------------------------


def pytest_addoption(parser):
    parser.addoption("--run-long", action="store_true", help="run long tests")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-long"):
        skip_long_test = pytest.mark.skip(reason="need --run-long option to run")
        for item in items:
            if "long_test" in item.keywords:
                item.add_marker(skip_long_test)


# ------------------------------------------
# Includes fixtures, made available to all tests.
# ------------------------------------------

pytest_plugins = [
    "fixtures.dir_fixture",
    "fixtures.misc_fixture",
]
