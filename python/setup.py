from setuptools import setup

# Version moved so we have one place it is defined.
exec(open("sbg_tir_l1/version.py").read())

# Namespace packages are a bit on the new side. If you haven't seen
# this before, look at https://packaging.python.org/guides/packaging-namespace-packages/#pkgutil-style-namespace-packages for a description of
# this.
setup(
    name='sbg-tir-l1',
    version=__version__,
    description='SBG TIR L1',
    author='Mike Smyth, Veljko Jovanovic',
    author_email='mike.m.smyth@jpl.nasa.gov, veljko.m.jovanovic@jpl.nasa.gov',
    license='Apache 2.0',
    packages=['sbg_tir_l1'],
    package_data={"*" : ["py.typed", "*.pyi"]},
    install_requires=[
        'numpy', 'scipy', 
    ],
    scripts=["bin/l1a_cal", "bin/l1b_rad", "bin/l1b_geo",]
)
