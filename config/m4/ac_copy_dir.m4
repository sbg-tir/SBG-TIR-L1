# SYNOPSIS
#
# AC_COPY_DIR
#
# DESCRIPTION
#
# On linux systems, you can efficiently install a directory by doing a
# "cp -ur". However not all systems support this. So we have a basic test
# in place to determine how we can do this cp.
#
# This sets the variable COPY_DIRECTORY for use in the Makefile.

AC_DEFUN([AC_COPY_DIR],
[ AC_MSG_CHECKING([for copy directory])
 rm -fr conftestdata
 mkdir conftestdata
 touch conftestdata/test.data
 if cp -ur conftestdata conftestdatacopy 2>/dev/null; then
    cp_prog="cp -ur"
    rm -rf conftestdatacopy conftestdata
 else
    if rsync -r conftestdata conftestdatacopy 2>/dev/null; then
      cp_prog="rsync -r"
      rm -rf conftestdatacopy conftestdata
    else
      AC_MSG_RESULT([no])
      AC_MSG_ERROR([Cannot find way to copy directory (tried cp -ur and rsync)])
    fi
 fi
 AC_MSG_RESULT([yes])
 COPY_DIRECTORY="$cp_prog"
 AC_SUBST(COPY_DIRECTORY)
])

