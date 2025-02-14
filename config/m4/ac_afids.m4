# SYNOPSIS
#
#   AC_AFIDS([required])
#
# DESCRIPTION
#
# This looks for the AFIDS programs. If we find it, then we set the
# Makefile conditional HAVE_AFIDS. We also set AFIDS_PREFIX to the 
# base directory.
#
# Not finding this library might or might not indicate an error. If you
# want an error to occur if we don't find the library, then specify
# "required". Otherwise, leave it as empty and we'll just silently
# return if we don't find the library.

AC_DEFUN([AC_AFIDS],
[
# Guard against running twice
if test "x$done_afids" = "x"; then
AC_HANDLE_WITH_ARG([afids], [afids], [AFIDS], [cannot_build], [default_search], $1)
if test "x$want_afids" = "xyes"; then
        AC_MSG_CHECKING([for AFIDS programs])
        succeeded=no
        if test "$build_afids" == "yes"; then
	    AFIDS_PREFIX="\${prefix}"
            succeeded=yes
        elif test "$ac_afids_path" != ""; then
	    AFIDS_PREFIX="$ac_afids_path"
            succeeded=yes
        else
	    # Check for taetm instead of vicarb because we may install our
	    # own verion of vicarb, but want to still point to the other
	    # afids
            for ac_afids_path_tmp in $prefix $CONDA_PREFIX $THIRDPARTY /opt/afids ; do
                  if test -e "$ac_afids_path_tmp/bin/taetm" && test -r "$ac_afids_path_tmp/bin/taetm"; then
                      AFIDS_PREFIX="$ac_afids_path_tmp"
                      succeeded=yes
                      break;
                  fi
            done
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_afids" == "xyes" ; then
            build_afids="yes"
            ac_afids_path="\${prefix}"
	    AFIDS_PREFIX="\${prefix}"
            succeeded=yes
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
                AC_SUBST([AFIDS_PREFIX])
                have_afids="yes"
        fi
fi

AM_CONDITIONAL([HAVE_AFIDS], [test "$have_afids" = "yes"])
AC_CHECK_FOUND([afids], [afids],[AFIDS],$1,[cannot_build])
done_afids="yes"
fi
])
