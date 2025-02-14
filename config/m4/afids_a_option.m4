AC_DEFUN([AFIDS_A_OPTION],[
#=================================================================
# Option to include "AFIDS configuration A" stuff.
AC_ARG_WITH([afids-a],
            [AS_HELP_STRING([--with-afids-a],
              [Include "AFIDS configuration A" code.  If this isn't selected, portions of AFIDS code are excluding from the install.])],
            [with_afids_a=yes],
            [with_afids_a=no])
AM_CONDITIONAL([WITH_AFIDS_A], [test x$with_afids_a = xyes])

])
