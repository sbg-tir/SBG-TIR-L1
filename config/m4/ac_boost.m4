# SYNOPSIS
#
#   AC_BOOST([required], [can_build], [default_build], [MINIMUM-VERSION])
#
# DESCRIPTION
#
# This looks for the BOOST libraries. If we find them, we set the Makefile
# conditional HAVE_BOOST. We as set BOOST_CPPFLAGS, and BOOST_LIBDIR.
#
# Because the libraries can have different names on different systems,
# we also set BOOST_REGEX_LIB, BOOST_FILESYSTEM_LIB, BOOST_DATETIME_LIB, 
# BOOST_IOSTREAMS_LIB, and BOOST_SERIALIZATION_LIB that can be used on 
# a link line (e.g., it might be "-lboost_regex" on a number of linux
# systems). We can extend this with other boost libraries if needed, but
# right now this is all we use.
# 
# To allow users to build there own copy of BOOST, we also define
# BUILD_BOOST
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

AC_DEFUN([AC_BOOST],
[
# Guard against running twice
if test "x$done_boost" = "x"; then
AC_HANDLE_WITH_ARG([boost], [boost], [BOOST], $2, $3, $1)

# GCC has -isystem like -I. The advantage is is knows not to warn about
# things in the header files we can't change. Boost has a number of things like
# this
if test "x$GCC" = "xyes"; then
    boost_include="-isystem"
else
    boost_include="-I"
fi
if test "x$want_boost" = "xyes"; then
        boost_lib_version_req=ifelse([$4], ,1.20.0,$4)
        boost_lib_version_req_shorten=`expr $boost_lib_version_req : '\([[0-9]]*\.[[0-9]]*\)'`
        boost_lib_version_req_major=`expr $boost_lib_version_req : '\([[0-9]]*\)'`
        boost_lib_version_req_minor=`expr $boost_lib_version_req : '[[0-9]]*\.\([[0-9]]*\)'`
        boost_lib_version_req_sub_minor=`expr $boost_lib_version_req : '[[0-9]]*\.[[0-9]]*\.\([[0-9]]*\)'`
        if test "x$boost_lib_version_req_sub_minor" = "x" ; then
           boost_lib_version_req_sub_minor="0"
           fi
        WANT_BOOST_VERSION=`expr $boost_lib_version_req_major \* 100000 \+  $boost_lib_version_req_minor \* 100 \+ $boost_lib_version_req_sub_minor`

        AC_MSG_CHECKING(for BOOST library >= $boost_lib_version_req)
        succeeded=no
	boost_version_check_needed=yes
        if test "$ac_boost_path" != ""; then
            BOOST_CPPFLAGS="$boost_include$ac_boost_path/include"
            succeeded=yes
        else
            for ac_boost_path_tmp in $prefix $CONDA_PREFIX $THIRDPARTY /opt/afids_support /usr /usr/local /opt /opt/local /sw ; do
                  if test -e "$ac_boost_path_tmp/include/boost/smart_ptr.hpp" && test -r "$ac_boost_path_tmp/include/boost/smart_ptr.hpp"; then
                      ac_boost_path="$ac_boost_path_tmp"
                      BOOST_CPPFLAGS="$boost_include$ac_boost_path_tmp/include"
                      succeeded=yes
                      break;
                  fi
            done
        fi
	if test "$succeeded" != "yes" -a "x$build_needed_boost" == "xyes" ; then
            build_boost="yes"
            ac_boost_path="\${prefix}"
            BOOST_CPPFLAGS="$boost_include$ac_boost_path/include"
            succeeded=yes
        fi
        if test "$succeeded" = "yes" ; then
            boost_done=no
            if test "$build_boost" = "yes"; then
               BOOST_LIBDIR="$ac_boost_path/lib"
               BOOST_REGEX_LIB="-lboost_regex"
               BOOST_FILESYSTEM_LIB="-lboost_filesystem -lboost_system"
               BOOST_DATETIME_LIB="-lboost_date_time"
               BOOST_IOSTREAMS_LIB="-lboost_iostreams"
               BOOST_SERIALIZATION_LIB="-lboost_serialization"
               AC_DEFINE(HAVE_BOOST_SERIALIZATION_BOOST_ARRAY_HPP,,[Defined if we have boost/serialization/boost_array.hpp])
               boost_done=yes
            fi
            for ac_boost_lib_base in "$ac_boost_path/lib" "$ac_boost_path/lib64"; do
              if test "$boost_done" = "no"; then
                for ac_boost_lib in libboost_regex.la libboost_regex.so libboost_regex.dylib ; do
                   if test -e "$ac_boost_lib_base/$ac_boost_lib"; then
                       BOOST_LIBDIR="$ac_boost_lib_base"
                       BOOST_REGEX_LIB="-lboost_regex"
		       BOOST_FILESYSTEM_LIB="-lboost_filesystem -lboost_system"
                       BOOST_DATETIME_LIB="-lboost_date_time"
		       BOOST_IOSTREAMS_LIB="-lboost_iostreams"
                       BOOST_SERIALIZATION_LIB="-lboost_serialization"
                       boost_done=yes
                       break;
                   fi
                done
              fi
              if test "$boost_done" = "no"; then
                for ac_boost_lib in libboost_regex-mt.la libboost_regex-mt.so libboost_regex-mt.dylib ; do
                   if test -e "$ac_boost_lib_base/$ac_boost_lib"; then
                       BOOST_LIBDIR="$ac_boost_lib_base"
                       BOOST_REGEX_LIB="-lboost_regex-mt"
		       BOOST_FILESYSTEM_LIB="-lboost_filesystem-mt -lboost_system-mt"
                       BOOST_DATETIME_LIB="-lboost_date_time-mt"
                       BOOST_IOSTREAMS_LIB="-lboost_iostreams-mt"
                       BOOST_SERIALIZATION_LIB="-lboost_serialization-mt"
                       boost_done=yes
                       break;
                   fi
                done
              fi
            done
            if test "$boost_done" = "no"; then
	        boost_version_check_needed=no
                succeeded=no
            fi
        fi
        if test "x$build_boost" == "xyes" ; then
	   boost_version_check_needed=no
        fi
        if test "$boost_version_check_needed" = "yes"; then
	   CPPFLAGS_SAVED="$CPPFLAGS"
	   CPPFLAGS="$CPPFLAGS $BOOST_CPPFLAGS"
	   export CPPFLAGS

 	   LDFLAGS_SAVED="$LDFLAGS"
 	   LDFLAGS="$LDFLAGS $BOOST_LDFLAGS"
 	   export LDFLAGS

 	   AC_REQUIRE([AC_PROG_CXX])
 	   AC_LANG_PUSH(C++)
 	   AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[
 	   @%:@include <boost/version.hpp>
 	   ]], [[
 	   #if BOOST_VERSION >= $WANT_BOOST_VERSION
 	   // Everything is okay
 	   #else
 	   #  error Boost version is too old
 	   #endif
 	   ]])],[
 	   succeeded=yes
 	   ],[
 	   succeeded=no
	   AC_MSG_WARN([We found boost, but the version is too old])
 	   ])
 	   AC_LANG_POP([C++])
        fi
# We have a fix needed for specific versions of boost. Go ahead and
# check for these.
        if test "$succeeded" = "yes" ; then
	   CPPFLAGS_SAVED="$CPPFLAGS"
	   CPPFLAGS="$CPPFLAGS $BOOST_CPPFLAGS"
	   export CPPFLAGS

 	   LDFLAGS_SAVED="$LDFLAGS"
 	   LDFLAGS="$LDFLAGS $BOOST_LDFLAGS"
 	   export LDFLAGS

 	   AC_REQUIRE([AC_PROG_CXX])
 	   AC_LANG_PUSH(C++)

 	   AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[
 	   @%:@include <boost/version.hpp>
 	   ]], [[
 	   #if BOOST_VERSION / 100 == 1056
 	   // At 1.56
 	   #else
 	   #  error Boost version is not 1.56
 	   #endif
 	   ]])],[
	   BOOST_CPPFLAGS="$boost_include$srcdir/boost_fix/1.56 $BOOST_CPPFLAGS"
 	   ],[
 	   ])

 	   AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[
 	   @%:@include <boost/version.hpp>
 	   ]], [[
 	   #if BOOST_VERSION / 100 == 1057
 	   // At 1.57
 	   #else
 	   #  error Boost version is not 1.57
 	   #endif
 	   ]])],[
	   BOOST_CPPFLAGS="$boost_include$srcdir/boost_fix/1.57 $BOOST_CPPFLAGS"
 	   ],[
 	   ])

 	   AC_COMPILE_IFELSE([AC_LANG_PROGRAM([[
 	   @%:@include <boost/version.hpp>
 	   ]], [[
 	   #if BOOST_VERSION / 100 == 1058
 	   // At 1.58
 	   #else
 	   #  error Boost version is not 1.58
 	   #endif
 	   ]])],[
	   BOOST_CPPFLAGS="$boost_include$srcdir/boost_fix/1.58 $BOOST_CPPFLAGS"
 	   ],[
 	   ])

	   # Also, check for the header file 
           AC_CHECK_HEADERS([boost/serialization/boost_array.hpp])
 	   AC_LANG_POP([C++])
        fi

        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
        else
                AC_MSG_RESULT([yes])
	        BOOST_CPPFLAGS="$BOOST_CPPFLAGS -DBOOST_TEST_DYN_LINK"
                AC_SUBST(BOOST_CPPFLAGS)
                AC_SUBST(BOOST_LIBDIR)
		AC_SUBST(BOOST_REGEX_LIB)
		AC_SUBST(BOOST_FILESYSTEM_LIB)
		AC_SUBST(BOOST_DATETIME_LIB)
		AC_SUBST(BOOST_IOSTREAMS_LIB)
		AC_SUBST(BOOST_SERIALIZATION_LIB)
                AC_DEFINE(HAVE_BOOST,,[Defined if we have BOOST])
                have_boost="yes"
        fi
fi
AM_CONDITIONAL([HAVE_BOOST], [test "$have_boost" = "yes"])
AM_CONDITIONAL([BUILD_BOOST], [test "$build_boost" = "yes"])
AC_CHECK_FOUND([boost], [boost],[BOOST],$1,$2)
done_boost="yes"
fi
])
