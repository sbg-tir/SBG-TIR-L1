# SYNOPSIS
#
#   AC_FFTW([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the fftw library. If we find them, we set the Makefile
# conditional HAVE_FFTW. We as set FFTW_CFLAGS and FFTW_LIBS
# 
# To allow users to build there own copy of fftw, we also define
# BUILD_FFTW
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

AC_DEFUN([AC_FFTW],
[
# Guard against running twice
if test "x$done_fftw" = "x"; then
AC_HANDLE_WITH_ARG([fftw], [fftw], [fftw], $2, $3, $1)
if test "x$want_fftw" = "xyes"; then
        AC_MSG_CHECKING([for Fftw library])
        succeeded=no
        if test "$ac_fftw_path" != ""; then
            FFTW_LIBS="-L$ac_fftw_path/lib -lfftw3"
            FFTW_CFLAGS="-I$ac_fftw_path/include"
            succeeded=yes
        else
	    AC_SEARCH_LIB([FFTW], [fftw3], , [fftw3.h], , [libfftw3], [-lfftw3])
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_fftw" == "xyes" ; then
            build_fftw="yes"
            ac_fftw_path="\${prefix}"
            FFTW_LIBS="-L$ac_fftw_path/lib -lfftw3"
            FFTW_CFLAGS="-I$ac_fftw_path/include"
            succeeded=yes
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(FFTW_CFLAGS)
                AC_SUBST(FFTW_LIBS)
                AC_DEFINE(HAVE_FFTW,,[Defined if we have FFTW])
                have_fftw="yes"
        fi
fi
AM_CONDITIONAL([HAVE_FFTW], [test "$have_fftw" = "yes"])
AM_CONDITIONAL([BUILD_FFTW], [test "$build_fftw" = "yes"])

AC_CHECK_FOUND([fftw], [fftw],[fftw],$1,$2)

done_fftw="yes"
fi
])
