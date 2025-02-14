# SYNOPSIS
#
#   AC_GDAL([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the GDAL libraries. If we find them, we set the Makefile
# conditional HAVE_GDAL. We as set GDAL_CFLAGS and GDAL_LIBS.
#
# The variable GDAL_EXTRA_ARG is set with anything extra to pass to the
# GDAL configure line when building (e.g., specify location of extra libraries
# to use such as Kakadu)
# 
# To allow users to build there own copy of GDAL, we also define
# BUILD_GDAL
#
# If the variable $V2OLB is defined (so we are in a MIPL environment) we
# initially look for GDAL at $GDALLIB directory

AC_DEFUN([AC_GDAL],
[
# Guard against running twice
if test "x$done_gdal" = "x"; then
AC_HANDLE_WITH_ARG([gdal], [gdal], [GDAL], $2, $3, $1)
AC_ARG_WITH([extra-gdal-arg],
            [AS_HELP_STRING([--with-extra-gdal-arg],
             [Extra argument to add when building gdal. Useful to specify local libraries that you might want to use, such as ECW or Kakadu. This string is passed directly to the GDAL configuration, so for example you might specify --with-extra-gdal-arg="--with-ecw=<directory> --with-kakadu=<directory2>"])],
            [GDAL_EXTRA_ARG="$withval"],
            [GDAL_EXTRA_ARG=""])
AC_ARG_WITH([ecw-plugin],
	    [AS_HELP_STRING([--with-ecw-plugin][@<:@=DIR@:>@],[Build the ECW library as a plugin, rather than building directly into GDAL. Can supply the directory with ECW library (default /opt/local/ecw/ERDAS-ECW_JPEG_2000_SDK-5.1.1/Desktop_Read-Only)])],
	    [
              if test "$withval" = "no"; then
                 build_ecw_plugin="no"
              elif test "$withval" = "yes"; then
                 build_ecw_plugin="yes"
		 ecw_dir="/opt/local/ecw/ERDAS-ECW_JPEG_2000_SDK-5.1.1/Desktop_Read-Only"
              else
                 build_ecw_plugin="yes"
		 ecw_dir="$withval"
               fi
	   ],
           [ build_ecw_plugin="no"
           ]
	   )

if test "x$want_gdal" = "xyes"; then
        AC_MSG_CHECKING([for GDAL library])
        succeeded=no
        if test "$ac_gdal_path" != ""; then
            GDAL_PREFIX="$ac_gdal_path"
            GDAL_LIBS="-L$ac_gdal_path/lib -lgdal"
            GDAL_CFLAGS="-I$ac_gdal_path/include"
            succeeded=yes
        else
	    if test "$V2OLB" != "" && test "$GDALLIB" != ""; then
		GDAL_PREFIX="$GDALLIB"
		GDAL_LIBS="-L$GDAL_PREFIX/lib -lgdal"
		GDAL_CFLAGS="-I$GDAL_PREFIX/include"
		succeeded=yes
	    else
	      AC_SEARCH_LIB([GDAL], [gdal], , [gdal.h], , [libgdal], [-lgdal])
	    fi
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_gdal" = "xyes" ; then
            build_gdal="yes"
            ac_gdal_path="\${prefix}"
            GDAL_PREFIX="$ac_gdal_path"
            GDAL_LIBS="-L$ac_gdal_path/lib -lgdal"
            GDAL_CFLAGS="-I$ac_gdal_path/include"
            succeeded=yes
        fi
        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
	fi
        if test "$succeeded" = "yes" -a "$build_gdal" = "no"; then
                GDAL_LIBS="`$GDAL_PREFIX/bin/gdal-config --libs`"
                GDAL_CFLAGS=`$GDAL_PREFIX/bin/gdal-config --cflags`
	        AC_MSG_CHECKING([version GDAL library is new enough])
		AC_REQUIRE([AC_PROG_CC])
		CPPFLAGS_SAVED="$CPPFLAGS"
		CPPFLAGS="$CPPFLAGS $GDAL_CFLAGS"
		export CPPFLAGS
		AC_LANG_PUSH([C++])
		AC_RUN_IFELSE([AC_LANG_PROGRAM([[@%:@include <gdal.h>
@%:@include <fstream>]],
		  [[std::ofstream t("conftest.out");
		   t << GDAL_RELEASE_NAME << "\n";]])],
		   [ gdal_version=`cat conftest.out` ],
		   [AC_MSG_FAILURE([gdal version program execution failed])])
		AC_LANG_POP([C++])
		CPPFLAGS="$CPPFLAGS_SAVED"
		AX_COMPARE_VERSION([${gdal_version}], [ge], [1.9.2],
		   [AC_MSG_RESULT([yes])],
		   [AC_MSG_RESULT([no])
		    AC_MSG_WARN([We require GDAL version to be >= 1.9.2. There are bugs in earlier versions that we have encountered, so we don't use earlier version of GDAL])
		    succeeded=no])
	fi
        if test "$succeeded" = "yes" ; then
	        # If we are building, then use AFIDSTOP here instead. prefix
		# is fine in the makefile, but GDAL_PREFIX is used in the
		# setup_env file.
 	        if test "$build_gdal" = "yes"; then
	            GDAL_PREFIX="\${AFIDSTOP}"
		fi
                AC_SUBST(GDAL_PREFIX)
                AC_SUBST(GDAL_CFLAGS)
                AC_SUBST(GDAL_LIBS)
		AC_SUBST(GDAL_EXTRA_ARG)
                AC_DEFINE(HAVE_GDAL,,[Defined if we have GDAL])
                have_gdal="yes"
        fi
fi
if test "$build_gdal" = "yes"; then
  AC_GEOS(required, $2, default_search)
  AC_OGDI(required, $2, default_search)
  AC_EXPAT(required, $2, default_search)
  AC_OPENJPEG(required, $2, default_search)
else # Not building GDAL
  AM_CONDITIONAL([HAVE_GEOS], [false])
  AM_CONDITIONAL([HAVE_OGDI], [false])
  AM_CONDITIONAL([HAVE_EXPAT], [false])
  AM_CONDITIONAL([HAVE_OPENJPEG], [false])
  AM_CONDITIONAL([BUILD_GEOS], [false])
  AM_CONDITIONAL([BUILD_OGDI], [false])
  AM_CONDITIONAL([BUILD_EXPAT], [false])
  AM_CONDITIONAL([BUILD_OPENJPEG], [false])
  build_geos="no"
  build_ogdi="no"
  build_expat="no"
  build_openjpeg="yes"
fi # End if/else building GDAL
AM_CONDITIONAL([HAVE_GDAL], [test "$have_gdal" = "yes"])
AM_CONDITIONAL([BUILD_GDAL], [test "$build_gdal" = "yes"])

AC_CHECK_FOUND([gdal], [gdal],[Gdal],$1,$2)

if test "$build_ecw_plugin" = "yes"; then
    ECW_CFLAGS="-I$ecw_dir/include"
    ECW_LIBS="-R$ecw_dir/lib/x64/release -L$ecw_dir/lib/x64/release -lNCSEcw"
    AC_SUBST(ECW_CFLAGS)
    AC_SUBST(ECW_LIBS)
fi

AM_CONDITIONAL([BUILD_ECW_PLUGIN], [test "$build_ecw_plugin" = "yes"])
done_gdal="yes"
fi
])
