# This sets IS_MAC and IS_MAC64 if we are on a mac, with 64 bits

AC_DEFUN([AC_IS_MAC],
[
  AM_CONDITIONAL([IS_MAC], [test ! -z "`uname | grep Darwin`"])
  mac64="no"
  if test "$GCC" = yes; then
    if(test ! -z "`uname | grep Darwin`"); then
       if(test ! -z "`${CC} -v 2>&1 | grep x86_64`"); then
          mac64="yes"
       fi
    fi
  fi
  AM_CONDITIONAL([IS_MAC64], [test "$mac64" = yes])
]
)
