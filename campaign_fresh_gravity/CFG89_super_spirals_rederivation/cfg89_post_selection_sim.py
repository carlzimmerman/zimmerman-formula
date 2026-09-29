# POST-HOC (declared as such, run after the frozen main): null of no trend -- offset iid N(mean, sd), v_pred as observed; select the 9 with the largest v_obs = v_pred*10^off.
import numpy as np, warnings; warnings.filterwarnings("ignore")
from cfg89_lib import *
D = load(); s = summary(D, {"model": "bulge", "Rd_src": "simard"}, "mono", "canonical", "bulge")
lvp = np.log10(s["vp"]); mu = s["off"].mean(); sd = s["off"].std(ddof=1)
rng = np.random.default_rng(1); ex = []
for _ in range(100000):
    o = rng.normal(mu, sd, 23); lvo = lvp + o; i = np.argsort(-lvo)[:9]; ex.append(o[i].mean() - o.mean())
ex = np.array(ex)
obs = s["m9"] - s["mean"]
print(f"selection-induced excess of the v_obs-selected nine over the sample mean under NO trend: mean {ex.mean():+.3f} (sd {ex.std():.3f}); observed excess {obs:+.3f}; P(excess>=obs) = {np.mean(ex>=obs):.3f}")
print(f"nine-fastest mean corrected for selection: {s['m9']-ex.mean():+.3f}; sd of log v_pred {lvp.std(ddof=1):.3f}")
