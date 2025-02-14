# SYNOPSIS
#
#   AC_CARTO([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the Carto library. If we find it, then we set the
# Makefile conditional HAVE_CARTO. We also set CARTO_CFLAGS and
# CARTO_LIBS
#
# To allow users to build there own copy of Carto, we also define
# BUILD_CARTO.
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

AC_DEFUN([AC_CARTO],
[
# Guard against running twice
if test "x$done_carto" = "x"; then
AC_HANDLE_WITH_ARG([carto], [carto], [Carto], $2, $3, $1)

if test "x$want_carto" = "xyes"; then
        AC_MSG_CHECKING([for Carto library])
        succeeded=no
	CARTO_BUILD_DEPEND=""
        if test "$build_carto" == "yes"; then
            CARTO_LIBS="libcarto.la"
	    CARTO_BUILD_DEPEND="libcarto.la"
            CARTO_CFLAGS="-I$srcdir/carto/inc \$(VICAR_RTL_CFLAGS) \$(GSL_CFLAGS)"
            succeeded=yes
        elif test "$ac_carto_path" != ""; then
            CARTO_LIBS="-R$ac_carto_path/lib -L$ac_carto_path/lib -lcarto \$(VICAR_RTL_LIBS) \$(GSL_LIBS)"
            CARTO_CFLAGS="-I$ac_carto_path/include/carto -I$ac_carto_path/include \$(VICAR_RTL_CFLAGS) \$(GSL_CFLAGS)"
            succeeded=yes
        else
	    AC_SEARCH_LIB([CARTO], [carto], [carto/], [burl.h], ,
                          [libcarto], [-lcarto])
	    CARTO_LIBS="$CARTO_LIBS \$(VICAR_RTL_LIBS) \$(GSL_LIBS)"
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_carto" == "xyes" ; then
            build_carto="yes"
            ac_carto_path="\${prefix}"
            CARTO_LIBS="libcarto.la"
	    CARTO_BUILD_DEPEND="libcarto.la"
            CARTO_CFLAGS="-I$srcdir/carto/inc \$(VICAR_RTL_CFLAGS) \$(GSL_CFLAGS)"
            succeeded=yes
        fi

# We can only use the carto library if we also have vicar and gsl
        if test "$have_gsl" != "yes"; then
	   succeeded=no
	fi
        if test "$have_vicar_rtl" != "yes"; then
	   succeeded=no
	fi

        if test "$succeeded" != "yes" ; then
                CARTO_CFLAGS=""
		CARTO_LIBS=""
                AC_MSG_RESULT([no])
		have_carto="no"
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(CARTO_CFLAGS)
                AC_SUBST(CARTO_BUILD_DEPEND)
                AC_SUBST(CARTO_LIBS)
                AC_DEFINE(HAVE_CARTO,,[Defined if we have Carto library])
                have_carto="yes"
        fi
fi
AM_CONDITIONAL([HAVE_CARTO], [test "$have_carto" = "yes"])
AM_CONDITIONAL([BUILD_CARTO], [test "$build_carto" = "yes"])

AC_CHECK_FOUND([carto], [carto],[Carto],$1,$2)
done_carto="yes"
fi
])
