# SYNOPSIS
#
#   AC_GEOS([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the GEOS libraries. If we find them, we set the Makefile
# conditional HAVE_GEOS. 
# 
# To allow users to build there own copy of GEOS, we also define
# BUILD_GEOS

AC_DEFUN([AC_GEOS],
[
# Guard against running twice
if test "x$done_geos" = "x"; then
AC_HANDLE_WITH_ARG([geos], [geos], [Geos], $2, $3, $1)
if test "x$want_geos" = "xyes"; then
        AC_MSG_CHECKING([for GEOS library])
        succeeded=no
        if test "$ac_geos_path" != ""; then
            GEOS_CFLAGS="-I$ac_geos_path/include"
            GEOS_LIBS="-R$ac_geos_path/lib -L$ac_geos_path/lib -lgeos"
            succeeded=yes
        else
	    AC_SEARCH_LIB([GEOS], [geos], , [geos.h], ,
                          [libgeos], [-lgeos])
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_geos" == "xyes" ; then
            build_geos="yes"
            ac_geos_path="\${prefix}"
            GEOS_CFLAGS="-I$ac_geos_path/include"
            GEOS_LIBS="-R$ac_geos_path/lib -L$ac_geos_path/lib -lgeos"
            succeeded=yes
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(GEOS_CFLAGS)
                AC_SUBST(GEOS_LIBS)
                AC_DEFINE(HAVE_GEOS,,[Defined if we have GEOS])
                have_geos="yes"
        fi
fi
AM_CONDITIONAL([HAVE_GEOS], [test "$have_geos" = "yes"])
AM_CONDITIONAL([BUILD_GEOS], [test "$build_geos" = "yes"])

AC_CHECK_FOUND([geos], [geos],[Geos],$1,$2)
done_geos="yes"
fi
])
