# SYNOPSIS
#
#   AC_AFIDS_DATA([required], [can_build], [default_build])
#
# DESCRIPTION
#
# This looks for the AFIDS data. If we find this, then we set the
# variable AFIDS_DATA, and HAVE_AFIDS_DATA
#
# We also define BUILD_AFIDS_DATA
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

AC_DEFUN([AC_AFIDS_DATA],
[
# Guard against running twice
if test "x$done_afids_data" = "x"; then
AC_HANDLE_WITH_ARG([afids_data], [afids-data], [AFIDS data], $2, $3, $1)

if test "x$want_afids_data" = "xyes"; then
        AC_MSG_CHECKING([for AFIDS data])
        succeeded=no
        if test "$ac_afids_data_path" != ""; then
            AFIDS_DATA="$ac_afids_data_path/data"
	    succeeded=yes
        else
	   for ac_path_tmp in $prefix $CONDA_PREFIX $THIRDPARTY /opt/afids ; do
               if test -e "$ac_path_tmp/data/vdev"; then
                  AFIDS_DATA="$ac_path_tmp/data"
	          succeeded=yes
                  break;
               fi
           done
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_afids_data" == "xyes" ; then
            build_afids_data="yes"
            ac_afids_data_path="\${prefix}"
            AFIDS_DATA="$ac_afids_data_path/data"
            succeeded=yes
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
		AFIDS_DATA_ABS=`eval echo ${AFIDS_DATA}`
                AC_SUBST(AFIDS_DATA)
                AC_SUBST(AFIDS_DATA_ABS)
                have_afids_data="yes"
        fi
fi
AM_CONDITIONAL([HAVE_AFIDS_DATA], [test "$have_afids_data" = "yes"])
AM_CONDITIONAL([BUILD_AFIDS_DATA], [test "$build_afids_data" = "yes"])

AC_CHECK_FOUND([afids_data], [afids-data],[AFIDS Data],$1,$2)
done_afids_data=yes
fi
])
