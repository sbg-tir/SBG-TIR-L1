# SYNOPSIS
#
#   AC_MSPI_SHARED([required])
#
# DESCRIPTION
#
# This looks for the MSPI-Shared library. If we find it, then we set the
# Makefile conditional HAVE_MSPI_SHARED. We also set MSPI_SHARED_CPPFFLAGS and
# MSPI_SHARED_LIBS. 
#
# Not finding this library might or might not indicate an error. If you
# want an error to occur if we don't find the library, then specify
# "required". Otherwise, leave it as empty and we'll just silently
# return if we don't find the library.
# 

AC_DEFUN([AC_MSPI_SHARED],
[
# Guard against running twice
if test "x$done_mspi_shared" = "x"; then
AC_HANDLE_WITH_ARG([mspi_shared], [mspi-shared], [MSPI-Shared], [cannot_build], [default_search], $1)

if test "x$want_mspi_shared" = "xyes"; then
        AC_MSG_CHECKING([for MSPI-Shared library])
        succeeded=no
        if test "$ac_mspi_shared_path" != ""; then
            MSPI_SHARED_LIBS="-R$ac_mspi_shared_path/lib -L$ac_mspi_shared_path/lib -lMSPI-Shared"
            MSPI_SHARED_CFLAGS="-I$ac_mspi_shared_path/include"
            succeeded=yes
        else
	  PKG_CHECK_MODULES([MSPI_SHARED], [MSPI-Shared], [succeeded=yes], [succeeded=no])
          if test "$succeeded" = "no"; then

             for ac_path_tmp in $prefix $CONDA_PREFIX $THIRDPARTY /data/smyth/MSPI-Shared/install ; do
                if test -e "$ac_path_tmp/lib/libMSPI-Shared.la" && test -r "$ac_path_tmp/lib/libMSPI-Shared.la"; then
                   MSPI_SHARED_LIBS="-R$ac_path_tmp/lib -L$ac_path_tmp/lib -lMSPI-Shared"
                   MSPI_SHARED_CFLAGS="-I$ac_path_tmp/include"
                   succeeded=yes
                   break
                fi
              done
	  fi
        fi
# We can only use MSPI shared if we also have HDFEOS5
        if test "$have_hdfeos5" != "yes"; then
	   succeeded=no
	fi
        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
		MSPI_SHARED_CFLAGS=""
		MSPI_SHARED_LIBS=""
		have_mspi_shared="no"
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(MSPI_SHARED_CFLAGS)
                AC_SUBST(MSPI_SHARED_BUILD_DEPEND)
                AC_SUBST(MSPI_SHARED_LIBS)
                AC_DEFINE(HAVE_MSPI_SHARED,,[Defined if we have MSPI-Shared])
                have_mspi_shared="yes"
        fi
fi

AM_CONDITIONAL([HAVE_MSPI_SHARED], [test "$have_mspi_shared" = "yes"])
AM_CONDITIONAL([BUILD_MSPI_SHARED], [test "$build_mspi_shared" = "yes"])

AC_CHECK_FOUND([mspi_shared], [mspi-shared],[MSPI-Shared],$1,$2)
done_mspi_shared="yes"
fi
])
