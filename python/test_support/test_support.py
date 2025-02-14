# This contains support routines for doing unit tests.
import pytest
import os
try:
    from sbg import *
    have_swig = True
except ImportError:
    have_swig = False
    
@pytest.yield_fixture(scope="function")
def isolated_dir(tmpdir):
    '''This is a fixture that creates a temporary directory, and uses this
    while running a unit tests. Useful for tests that write out a test file
    and then try to read it.

    This fixture changes into the temporary directory, and at the end of
    the test it changes back to the current directory.

    Note that this uses the fixture tmpdir, which keeps around the last few
    temporary directories (cleaning up after a fixed number are generated).
    So if a test fails, you can look at the output at the location of tmpdir, 
    e.g. /tmp/pytest-of-smyth
    '''
    curdir = os.getcwd()
    try:
        tmpdir.chdir()
        yield curdir
    finally:
        os.chdir(curdir)

@pytest.yield_fixture(scope="function")
def unit_test_data():
    '''Return the unit test directory'''
    yield os.path.abspath(os.path.dirname(__file__) + "/../../unit_test_data") + "/"

slow = pytest.mark.slow

# Short hand for marking as unconditional skipping. Good for tests we
# don't normally run, but might want to comment out for a specific debugging
# reason.
skip = pytest.mark.skip


# Can add lots of other fixtures as needed for testing.        
