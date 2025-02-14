# SYNOPSIS
#
#   AC_PERL_MODULE(modname)
#
# Checks to see if the the given perl modules are available.

AC_DEFUN([AC_PERL_MODULE],[
    if test -z $PERL;
    then
        PERL="perl"
    fi
    PERL_NAME=`basename $PERL`
    AC_MSG_CHECKING($PERL_NAME module: $1)
    $PERL "-M$1" -e exit > /dev/null 2>&1
	if test $? -eq 0;
	then
		AC_MSG_RESULT(yes)
	else
		AC_MSG_RESULT(no)
		AC_MSG_ERROR(failed to find required module $1)
		exit 1
	fi
])
