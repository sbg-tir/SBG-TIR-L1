# SYNOPSIS
#
#   AC_EXPAT([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the expat library. If we find them, we set the Makefile
# conditional HAVE_EXPAT. We as set EXPAT_CFLAGS and EXPAT_LIBS
# 
# To allow users to build there own copy of expat, we also define
# BUILD_EXPAT

AC_DEFUN([AC_EXPAT],
[
# Guard against running twice
if test "x$done_expat" = "x"; then
AC_HANDLE_WITH_ARG([expat], [expat], [expat], $2, $3, $1)
if test "x$want_expat" = "xyes"; then
        AC_MSG_CHECKING([for expat library])
        succeeded=no
        if test "$ac_expat_path" != ""; then
            EXPAT_LIBS="-L$ac_expat_path/lib -lexpat"
            EXPAT_CFLAGS="-I$ac_expat_path/include"
	    EXPAT_PREFIX="$ac_expat_path"
            succeeded=yes
        else
	    AC_SEARCH_LIB([EXPAT], [expat], , [expat.h], ,
	                  [libexpat], [-lexpat])
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_expat" == "xyes" ; then
            build_expat="yes"
            ac_expat_path="\${prefix}"
            EXPAT_LIBS="-L$ac_expat_path/lib -lexpat"
            EXPAT_CFLAGS="-I$ac_expat_path/include"
	    EXPAT_PREFIX="$ac_expat_path"
            succeeded=yes
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(EXPAT_CFLAGS)
                AC_SUBST(EXPAT_LIBS)
                AC_SUBST(EXPAT_PREFIX)
                AC_DEFINE(HAVE_EXPAT,,[Defined if we have Expat])
                have_expat="yes"
        fi
fi
AM_CONDITIONAL([HAVE_EXPAT], [test "$have_expat" = "yes"])
AM_CONDITIONAL([BUILD_EXPAT], [test "$build_expat" = "yes"])

AC_CHECK_FOUND([expat], [expat],[expat],$1,$2)
done_expat="yes"
fi
])
