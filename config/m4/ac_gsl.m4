# SYNOPSIS
#
#   AC_GSL([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the GSL libraries. If we find them, we set the Makefile
# conditional HAVE_GSL. We as set GSL_CFLAGS and GSL_LIBS
# 
# To allow users to build there own copy of GSL, we also define
# BUILD_GSL
#
# A particular package might not have the library source code, so you
# can supply the "can_build" argument as "can_build". Empty string means we
# can't build this, and various help messages etc. are adjusted for this.
#
# Not finding this library might or might not indicate an error. If you
# want an error to occur if we don't find the library, then specify
# "required". Otherwise, leave it as empty and we'll just silently
# return if we don't find the library.
# 
# If the user doesn't otherwise specify the "with" argument for this
# library, we can either have a default behavior of searching for the
# library on the system or of building our own copy of it. You can
# specify "default_build" if this should build, otherwise we just look
# for this on the system.

AC_DEFUN([AC_GSL],
[
# Guard against running twice
if test "x$done_gsl" = "x"; then
AC_HANDLE_WITH_ARG([gsl], [gsl], [GSL], $2, $3, $1)
if test "x$want_gsl" = "xyes"; then
        AC_MSG_CHECKING([for GSL library])
        succeeded=no
        if test "$ac_gsl_path" != ""; then
            GSL_LIBS="-L$ac_gsl_path/lib -lgsl -lgslcblas"
            GSL_CFLAGS="-I$ac_gsl_path/include"
            succeeded=yes
        else
	    AC_SEARCH_LIB([GSL], [gsl], , [gsl/gsl_blas.h], ,
                          [libgsl], [-lgsl -lgslcblas])
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_gsl" == "xyes" ; then
            build_gsl="yes"
            ac_gsl_path="\${prefix}"
            GSL_LIBS="-L$ac_gsl_path/lib -lgsl -lgslcblas"
            GSL_CFLAGS="-I$ac_gsl_path/include"
            succeeded=yes
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(GSL_CFLAGS)
                AC_SUBST(GSL_LIBS)
                AC_DEFINE(HAVE_GSL,,[Defined if we have GSL])
                have_gsl="yes"
        fi
fi
AM_CONDITIONAL([HAVE_GSL], [test "$have_gsl" = "yes"])
AM_CONDITIONAL([BUILD_GSL], [test "$build_gsl" = "yes"])

AC_CHECK_FOUND([gsl], [gsl],[GSL],$1,$2)

done_gsl="yes"
fi
])
