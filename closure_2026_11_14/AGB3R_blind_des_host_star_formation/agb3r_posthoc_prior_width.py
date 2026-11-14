"""AGB3R post hoc (not a frozen fork): J2 with D2's prior error replaced by its sandwich and shuffle errors."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
AGB2 = os.path.normpath(os.path.join(HERE, "..", "AGB2_host_mass_step_redshift"))
sys.argv = ["agb2_joint.py", "AGB3R"]; sys.path.insert(0, AGB2)
from agb2_joint import joint
import numpy as np
D = json.load(open(os.path.join(HERE, "agb3r_D.json"))); K4 = json.load(open(os.path.join(HERE, "agb3r_K2K4.json")))["K4"]["cfg"]["D2"]
S = json.load(open(os.path.join(HERE, "agb3r_S_full.json"))); p = D["D2"]["primary"]
out = {}
for name, sd in (("wls", p["sd_A"]), ("sandwich", p["sd_A_sandwich"]), ("shuffle", K4["scatter_shuffle"])):
    r = joint(np.array(S["grid_f"]), np.array(S["f"]), np.array(S["q0"]), np.array(S["grid_n"]), np.array(S["n"]), np.array(S["t"]), p["A"], sd)
    out[name] = dict(sd=sd, A=r["A"], q0=r["q0"], D_today=r["D_today"], D_never=r["D_never"])
    print(f"prior {p['A']:+.4f} +- {sd:.4f} ({name}): joint A_H {r['A']:+.3f}  q0 {r['q0']:+.4f}  dchi2_today {r['D_today']:.3f}  dchi2_never {r['D_never']:.3f}")
json.dump(out, open(os.path.join(HERE, "agb3r_posthoc_prior_width.json"), "w"), indent=1)
