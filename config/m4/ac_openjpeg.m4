# SYNOPSIS
#
#   AC_OPENJPEG([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the openjpeg library. If we find them, we set the Makefile
# conditional HAVE_OPENJPEG. We as set OPENJPEG_CFLAGS and OPENJPEG_LIBS
# 
# To allow users to build there own copy of openjpeg, we also define
# BUILD_OPENJPEG

AC_DEFUN([AC_OPENJPEG],
[
# Guard against running twice
if test "x$done_openjpeg" = "x"; then
AC_HANDLE_WITH_ARG([openjpeg], [openjpeg], [openjpeg], $2, $3, $1)
if test "x$want_openjpeg" = "xyes"; then
        AC_MSG_CHECKING([for openjpeg library])
        succeeded=no
        if test "$ac_openjpeg_path" != ""; then
            OPENJPEG_LIBS="-L$ac_openjpeg_path/lib -lopenjp2"
            OPENJPEG_CFLAGS="-I$ac_openjpeg_path/include/openjeg-2.3"
	    OPENJPEG_PREFIX="$ac_openjpeg_path"
            succeeded=yes
        else
	    AC_SEARCH_LIB([OPENJPEG], [libopenjp2], [openjpeg-2.3/], 
	                  [openjpeg.h], ,[libopenjp2], [-openjp2])
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_openjpeg" == "xyes" ; then
            build_openjpeg="yes"
            ac_openjpeg_path="\${prefix}"
            OPENJPEG_LIBS="-L$ac_openjpeg_path/lib -lopenjp2"
            OPENJPEG_CFLAGS="-I$ac_openjpeg_path/include/openjeg-2.3"
	    OPENJPEG_PREFIX="$ac_openjpeg_path"
            succeeded=yes
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(OPENJPEG_CFLAGS)
                AC_SUBST(OPENJPEG_LIBS)
                AC_SUBST(OPENJPEG_PREFIX)
                AC_DEFINE(HAVE_OPENJPEG,,[Defined if we have Openjpeg])
                have_openjpeg="yes"
        fi
fi
AM_CONDITIONAL([HAVE_OPENJPEG], [test "$have_openjpeg" = "yes"])
AM_CONDITIONAL([BUILD_OPENJPEG], [test "$build_openjpeg" = "yes"])

AC_CHECK_FOUND([openjpeg], [openjpeg],[openjpeg],$1,$2)
done_openjpeg="yes"
fi
])
