from sbg_tir_l1 import L1OspDir
import geocal
import pickle

def test_l1_osp_dir(l1_osp_dir, isolated_dir):
    t = L1OspDir(l1_osp_dir)
    print(t.l1b_geo_config.pge_name)
    pickle.dump(t, open("test.pkl", "wb"))
    t2 = pickle.load(open("test.pkl", "rb"))
    print(t2.l1b_geo_config.pge_name)
    print(t.dem)
    print(t.lwm)
    # Skip for now, we want to move to geotiff 1x1 degree tiles rather than
    # VICAR 5x5. We'll update this later
    #print(t.ortho_base)
    
