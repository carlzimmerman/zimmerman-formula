import resource
import numpy as np
import as204_curved_heat_force as m


def rss_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


print("import rss MB", round(rss_mb(), 1))
leaf8 = m.S3.load_cache("leaf_L8.npz")
print("after L8 load rss MB", round(rss_mb(), 1))
leaf10 = m.S3.load_cache("leaf_L10.npz")
print("after L10 load rss MB", round(rss_mb(), 1))
rngs = np.random.default_rng(204)
runs = {}
m.run_s3(8, 0.05, 0.0, 2.3374, "x", runs, rngs, leaf=leaf8)
print("after run_s3 L8 rss MB", round(rss_mb(), 1))
import gc; gc.collect()
print("after gc rss MB", round(rss_mb(), 1))