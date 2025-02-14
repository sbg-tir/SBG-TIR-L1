# SYNOPSIS
#
#   AC_MSP([required])
#
# DESCRIPTION
#
# This looks for the MSP libraries. If we find them, we set the Makefile
# conditional HAVE_MSP. We as set MSP_CFLAGS and MSP_LIBS
# 
# Not finding this library might or might not indicate an error. If you
# want an error to occur if we don't find the library, then specify
# "required". Otherwise, leave it as empty and we'll just silently
# return if we don't find the library.

AC_DEFUN([AC_MSP],
[
# Guard against running twice
if test "x$done_msp" = "x"; then
AC_HANDLE_WITH_ARG_DEFAULT_NO([msp], [msp], [MSP], [cannot_build], [default_search], $1)
have_msp="no"
if test "x$want_msp" = "xyes"; then
        AC_MSG_CHECKING([for MSP library])
        succeeded=no
        if test "$ac_msp_path" != ""; then
            MSP_LIBS="-R$ac_msp_path/lib -L$ac_msp_path/lib  -ldl -R$ac_msp_path/lib -L$ac_msp_path/lib -lMSPCoordinateConversionService -lMSPCovarianceService -lMSPImagingGeometryService -lMSPMensurationService -lMSPMensurationSessionRecordService -lMSPPointExtractionService -lMSPOutputMethodService -lMSPSensorModelService -lMSPSensorSpecificService -lMSPSupportDataService -lMSPTerrainService -lMSPlunar -lMSPasdetre -lMSPCCSUtils -lMSPcoordconverter -lMSPcsisd -lMSPcsm -lMSPcsmutil -lMSPDEIUtil -lMSPgeometry -lMSPjson -lMSPlas -lMSPmath -lMSPnitf -lMSPntmtre -lMSPRsmGeneratorService -lMSPRageServiceUtils -lMSPrsmg -lMSPrsme -lMSPdei -lMSPmens -lMSPrutil -lMSPrage -lMSPRageServiceUtils -lMSPrageutilities -lMSPSScovmodel -lMSPSSrutil -lMSPutilities -lMSPmiisd"
            MSP_CFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0 -I$ac_msp_path/include -I$ac_msp_path/include/CCSUtils -I$ac_msp_path/include/CoordinateConversion -I$ac_msp_path/include/Covariance -I$ac_msp_path/include/PointExtraction -I$ac_msp_path/include/ImagingGeometry -I$ac_msp_path/include/Mensuration -I$ac_msp_path/include/MensurationSessionRecord -I$ac_msp_path/include/OutputMethod -I$ac_msp_path/include/SensorModel -I$ac_msp_path/include/SupportData -I$ac_msp_path/include/Terrain -I$ac_msp_path/include/common -I$ac_msp_path/include/common/csm -I$ac_msp_path/include/common/csmutil -I$ac_msp_path/include/common/dtcc -I$ac_msp_path/include/common/geometry -I$ac_msp_path/include/common/math -I$ac_msp_path/include/common/ntmtre -I$ac_msp_path/include/common/miisd -I$ac_msp_path/include/common/nitf -I$ac_msp_path/include/common/utilities -I$ac_msp_path/include/RsmGenerator"
	    MSP_PREFIX=$ac_msp_path
            succeeded=yes
        else
          for ac_path_tmp in $prefix $CONDA_PREFIX $THIRDPARTY /data/smyth/MSP/install ; do
             if test -e "$ac_path_tmp/lib/libMSPnitf.so" && test -r "$ac_path_tmp/lib/libMSPnitf.so"; then
 	     	MSP_LIBS="-R$ac_path_tmp/lib -L$ac_path_tmp/lib -ldl -lMSPCoordinateConversionService -lMSPCovarianceService -lMSPImagingGeometryService -lMSPMensurationService -lMSPMensurationSessionRecordService -lMSPPointExtractionService -lMSPOutputMethodService -lMSPSensorModelService -lMSPSensorSpecificService -lMSPSupportDataService -lMSPTerrainService -lMSPlunar -lMSPasdetre -lMSPCCSUtils -lMSPcoordconverter -lMSPcsisd -lMSPcsm -lMSPcsmutil -lMSPDEIUtil -lMSPgeometry -lMSPjson -lMSPlas -lMSPmath -lMSPnitf -lMSPntmtre -lMSPRsmGeneratorService -lMSPRageServiceUtils -lMSPrsmg -lMSPrsme -lMSPdei -lMSPmens -lMSPrutil -lMSPrage -lMSPRageServiceUtils -lMSPrageutilities -lMSPSScovmodel -lMSPSSrutil -lMSPutilities -lMSPmiisd "
		MSP_CFLAGS="-D_GLIBCXX_USE_CXX11_ABI=0 -I$ac_path_tmp/include -I$ac_path_tmp/include/CCSUtils -I$ac_path_tmp/include/CoordinateConversion -I$ac_path_tmp/include/Covariance -I$ac_path_tmp/include/PointExtraction -I$ac_path_tmp/include/ImagingGeometry -I$ac_path_tmp/include/Mensuration -I$ac_path_tmp/include/MensurationSessionRecord -I$ac_path_tmp/include/OutputMethod -I$ac_path_tmp/include/SensorModel -I$ac_path_tmp/include/SupportData -I$ac_path_tmp/include/Terrain -I$ac_path_tmp/include/common -I$ac_path_tmp/include/common/csm -I$ac_path_tmp/include/common/csmutil -I$ac_path_tmp/include/common/dtcc -I$ac_path_tmp/include/common/geometry -I$ac_path_tmp/include/common/math -I$ac_path_tmp/include/common/ntmtre -I$ac_path_tmp/include/common/miisd -I$ac_path_tmp/include/common/nitf -I$ac_path_tmp/include/common/utilities -I$ac_path_tmp/include/RsmGenerator"
		MSP_PREFIX=$ac_path_tmp
                succeeded=yes
                break
             fi
           done
        fi
        if test "$succeeded" != "yes" ; then
                AC_MSG_RESULT([no])
		MSP_CFLAGS=""
		MSP_LIBS=""
		have_msp="no"
        else
                AC_MSG_RESULT([yes])
                AC_SUBST(MSP_CFLAGS)
                AC_SUBST(MSP_LIBS)
                AC_SUBST(MSP_PREFIX)
                AC_DEFINE(HAVE_MSP,,[Defined if we have MSP])
                have_msp="yes"
        fi
fi
AC_SUBST(have_msp)
AM_CONDITIONAL([HAVE_MSP], [test "$have_msp" = "yes"])
AM_CONDITIONAL([BUILD_MSP], [test "$build_msp" = "yes"])

AC_CHECK_FOUND([msp], [msp],[MSP],$1,[cannot_build])

done_msp="yes"
fi
])
