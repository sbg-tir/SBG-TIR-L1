dnl Process this file with autoconf to produce a configure script.

AC_INIT(sbg-tir-l1, 0.01)
AC_CONFIG_AUX_DIR([config])
AC_CONFIG_MACRO_DIRS([config/m4])
AC_CONFIG_MACRO_DIRS([config/m4_local])
AC_CONFIG_FILES([script/setup_sbg_tir_l1.csh script/setup_sbg_tir_l1.sh])
AC_CONFIG_FILES([lib/global_fixture_default.cc])

SBG_TIR_L1_COMMON

#=================================================================
# Find h5diff
AC_PATH_PROG([H5DIFF], [h5diff], "", [$PATH$PATH_SEPARATOR${ac_afids_dir}/bin])
if test -z "$H5DIFF"; then
   AC_MSG_ERROR([Cannot find h5diff])
fi

#=================================================================
# Find parallel
AC_PATH_PROG([PARALLEL], [parallel], "", [$PATH$PATH_SEPARATOR${ac_afids_dir}/bin])
if test -z "$PARALLEL"; then
   AC_MSG_ERROR([Cannot find parallel])
fi

#=================================================================
# Find python. Note that the virtual environment has modules that
# depend on the afids build, so set LD_LIBRARY_PATH here for AFIDS
# before checking all the modules.

original_ld_library_path="${LD_LIBRARY_PATH}"
export LD_LIBRARY_PATH="${afidsdir}/lib64:${afidsdir}/lib:${LD_LIBRARY_PATH}"
AFIDS_PYTHON(required, cannot_build, default_search)
LD_LIBRARY_PATH="${original_ld_library_path}"

#=================================================================
# Various thirdparty libraries.
AC_DOXYGEN(optional, cannot_build, default_search)

#=================================================================
# Location of all the source code directories
SBG_TIR_L1_SOURCE_DIRECTORY

#=================================================================
# Location of dem and spice data

AC_ARG_WITH([srtm-l2],
AS_HELP_STRING([--with-srtm-l2@<:@=DIR@:>@], [give directory where SRTM L2 data can be found]), [ ac_srtml2_dir="$withval" ], [ ac_srtml2_dir="/home/smyth/sandbox/sbg_ancillary/srtm_v3_dem_L2"] )
AC_SUBST([srtml2dir], ["$ac_srtml2_dir"])

AC_ARG_WITH([spice-data],
AS_HELP_STRING([--with-spice-data@<:@=DIR@:>@], [give directory where SPICE data can be found]), [ ac_spicedata_dir="$withval" ], [ ac_spicedata_dir="/home/smyth/sandbox/sbg_ancillary/spice_data/cspice"] )
AC_SUBST([spicedatadir], ["$ac_spicedata_dir"])

#=================================================================
# Option to bypass running SWIG to update SWIG wrappers. The SWIG
# wrappers can take a bit of time to create and compile, so if you
# aren't working directly with them it can be useful to turn off during
# development.
AC_ARG_WITH([swig],
           [AS_HELP_STRING([--without-swig],
             [Bypass running SWIG to update SWIG wrappers. The SWIG wrappers can take a bit of time to create and compile, so if you aren't working directly with them it can be useful to turn off during development.])],
           [SWIG=/fake_so_fail],
           [])

AC_PROG_SWIG()
SWIG_ENABLE_CXX
SWIG_PYTHON

#=================================================================
# Option to bypass running doxygen to update documentation. This is useful
# for a build environment that is used for development, but you'll want all
# of your "real" build environments to also update the documentation.
AC_ARG_WITH([documentation],
           [AS_HELP_STRING([--without-documentation],
             [Bypass running doxygen to update documentation. This is useful for a build environment that is used for development, but you'll want all of your "real" build environments to also update the documentation.])],
           [],
           [with_documentation=yes])
if test "$have_doxygen" != "yes"; then
   with_documentation=no
fi
AM_CONDITIONAL([WITH_DOCUMENTATION], [test x$with_documentation = xyes])

if test "$have_swig" = "yes" -a "$USE_MAINTAINER_MODE" != "no"; then
  generate_swig="yes"
else
  generate_swig="no" 
fi

if test "$generate_swig" = "yes" -a "$have_doxygen" != "yes"; then
     AC_MSG_ERROR([
sbg_tir_l1 requires doxygen if you are also generating SWIG python bindings.
You can try specifying the location using --with-doxygen if configure
couldn't find this. Or you can turn off the use of swig using 
--without-swig.])
fi

AC_CONFIG_FILES([Makefile])
AC_OUTPUT

#======================================================================
# Give a nice log message describing what has been configured
#======================================================================

LOC_MSG()
LOC_MSG([SBG TIR L1 is now configured])
LOC_MSG()
LOC_MSG([  Installation directory:        ${prefix}])
LOC_MSG([  Build debug version:           ${enable_debug}])
LOC_MSG([  CXX compiler:                  ${CXX} ${CXXFLAGS}])
LOC_MSG()
LOC_MSG([  Generate SWIG wrappers:        ${generate_swig}])
LOC_MSG([  Install documentation:         ${with_documentation}])

