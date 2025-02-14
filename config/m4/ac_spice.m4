# SYNOPSIS
#
#   AC_SPICE([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the SPICE library. If we find it, then we set the
# Makefile conditional HAVE_SPICE. We also set SPICE_CFLAGS and
# SPICE_LIBS
#
# To allow users to build there own copy of SPICE, we also define
# BUILD_SPICE.
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

AC_DEFUN([AC_SPICE],
[
# Guard against running twice
if test "x$done_spice" = "x"; then
AC_HANDLE_WITH_ARG([spice], [spice], [SPICE], $2, $3, $1)

if test "x$want_spice" = "xyes"; then
        AC_MSG_CHECKING([for SPICE library])
        succeeded=no
        if test "$build_spice" == "yes"; then
            SPICE_LIBS="-R$ac_spice_path/lib -L$ac_spice_path/lib -lcspice"
            SPICE_CFLAGS="-I$srcdir/spice/cspice/incude"
            succeeded=yes
        elif test "$ac_spice_path" != ""; then
            SPICE_LIBS="-R$ac_spice_path/lib -L$ac_spice_path/lib -lcspice"
            SPICE_CFLAGS="-I$ac_spice_path/include"
            succeeded=yes
        else
  	    if test "x$CONDA_PREFIX" != x; then
	       if test -e "$CONDA_PREFIX/include/SpiceCK.h"; then
                  SPICE_LIBS="-R$CONDA_PREFIX/lib -L$CONDA_PREFIX/lib -lcspice"
                  SPICE_CFLAGS="-I$CONDA_PREFIX/include"
                  succeeded=yes
	       elif test -e "$prefix/include/SpiceCK.h"; then
                  SPICE_LIBS="-R$prefix/lib -L$prefix/lib -lcspice"
                  SPICE_CFLAGS="-I$prefix/include"
                  succeeded=yes
	       fi
            fi
            if test "$succeeded" != "yes" ; then
	        AC_SEARCH_LIB([SPICE], [spice], , [SpiceCK.h], ,
                            [libcspice], [-lcspice])
            fi
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_spice" == "xyes" ; then
            build_spice="yes"
            ac_spice_path="\${prefix}"
            SPICE_LIBS="-R$ac_spice_path/lib -L$ac_spice_path/lib -lcspice"
            SPICE_CFLAGS="-I$srcdir/spice/cspice/incude"
            succeeded=yes
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(SPICE_CFLAGS)
                AC_SUBST(SPICE_LIBS)
                have_spice="yes"
                AC_DEFINE(HAVE_SPICE,,[Defined if we have SPICE])
        fi
fi
AM_CONDITIONAL([HAVE_SPICE], [test "$have_spice" = "yes"])
AM_CONDITIONAL([BUILD_SPICE], [test "$build_spice" = "yes"])

AC_CHECK_FOUND([spice], [spice],[SPICE],$1,$2)
done_spice="yes"
fi
])
