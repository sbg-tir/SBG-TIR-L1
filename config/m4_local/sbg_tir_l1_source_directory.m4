# We have the top directory for geocal as a variable. This allows the
# full AFIDS system to include this in a subdirectory.

AC_DEFUN([SBG_TIR_L1_SOURCE_DIRECTORY],[
AC_SUBST([swigrules], [swig_rules])
AC_SUBST([srcsbg_tir_l1bin], [bin])
AC_SUBST([srcpython], [python])
AC_SUBST([srcscript], [script])
AC_SUBST([srclib], [lib])
AC_SUBST([unittestdata], [unit_test_data])
AC_SUBST([pythonswigsrc], [bindings/python])
AC_SUBST([swigsrc], [bindings/python/swig])
AC_SUBST([pythondocdir], [\${prefix}/share/doc/sbg_tir_l1/python])
AC_SUBST([sbg_tir_l1swigincdir], [\${prefix}/share/sbg_tir_l1/swig])
AC_SUBST([swigincdir], [\${prefix}/share/sbg_tir_l1/swig])
AC_SUBST([installsbg_tir_l1dir], [\${prefix}])
AC_SUBST([sbg_tir_l1pkgpythondir],[\${prefix}/\${pythondir}/sbg_tir_l1])
])
