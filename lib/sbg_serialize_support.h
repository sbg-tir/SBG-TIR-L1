#define SWIG_MAPPER_NAMESPACE GeoCal
#include "geocal/geocal_serialize_support.h"

#define SBG_IMPLEMENT(NAME) \
BOOST_CLASS_EXPORT_IMPLEMENT(Sbg::NAME); \
template void NAME::serialize(boost::archive::polymorphic_oarchive& ar, \
				    const unsigned int version); \
template void NAME::serialize(boost::archive::polymorphic_iarchive& ar, \
				    const unsigned int version);
#define SBG_SPLIT_IMPLEMENT(NAME) \
BOOST_CLASS_EXPORT_IMPLEMENT(Sbg::NAME); \
template void NAME::save(boost::archive::polymorphic_oarchive& ar, \
				    const unsigned int version) const; \
template void NAME::load(boost::archive::polymorphic_iarchive& ar, \
				    const unsigned int version);

#define SBG_BASE(NAME,BASE) boost::serialization::void_cast_register<Sbg::NAME, Sbg::BASE>();
#define SBG_GENERIC_BASE(NAME) boost::serialization::void_cast_register<Sbg::NAME, GeoCal::GenericObject>();
