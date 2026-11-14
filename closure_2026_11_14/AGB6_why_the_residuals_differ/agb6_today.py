"""AGB6 closing arithmetic (written after the chain; no frozen word; fits nothing).

The chain shows that the published age slope is real in uncorrected residuals and that the releases' own host
corrections have already taken most of it out. A correction applied on top of PUBLISHED distances should then use
the slope still left in them, not the full published slope. Slope left in the published distances:
   Pantheon+ (this lane, set Pb, no mass step fitted):            read from agb6_chain.json
   DES Dovekie (AGB3, fit U on the published moduli, reading P):   read from agb3_D.json
   the same divided by the reliability of the star-formation ages inside that fit (AGB3 post hoc: 0.64 to 0.76)
Each is used as a Gaussian prior on the amplitude in AGB1's cosmology fit, with AGB1's cosmic-average template
(grids of agb2_J_diag.json) and with the sample's own drift (grids of agb3_S.json). AGB2's joint arithmetic.
Writes agb6_today.json; log to agb6_today.out."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(R, "AGB2_host_mass_step_redshift")); sys.argv = ["agb2_joint.py", "none"]
import numpy as np
import agb2_joint as J2

log = lambda s: print(s, flush=True); out = {}
ch = json.load(open(os.path.join(HERE, "agb6_chain.json")))["all"]["nostep"]["A"]["Pb"]
u = json.load(open(os.path.join(R, "AGB3_des_host_star_formation", "agb3_D.json")))["fits"]["fork_P"]["U"]
priors = {"Pantheon+ published (0.20)": (ch[0], ch[1]), "DES published (photometric ages)": (u["A"], u["sandwich_sd_A"]),
          "DES published, noise allowed (reliability 0.64)": (u["A"]/0.64, u["sandwich_sd_A"]/0.64), "published slope in full, for comparison": (1.0, 0.13)}
J = json.load(open(os.path.join(R, "AGB2_host_mass_step_redshift", "agb2_J_diag.json")))["samples"]; S = json.load(open(os.path.join(R, "AGB3_des_host_star_formation", "agb3_S.json")))["grids"]
Af, An = np.array(J2.GRID_F), np.array(J2.GRID_N)
grids = {"cosmic-average template, whole sample": J["full"], "cosmic-average template, DES alone": J["des_only"], "sample's own drift, whole sample": S["full_sfr"], "sample's own drift, DES alone": S["des_only_sfr"]}
def word(q0, d): return "ACCELERATING TODAY" if d >= 4 and q0 < 0 else "DECELERATING TODAY" if d >= 4 and q0 > 0 else "SIGN NOT SETTLED"
for pn, (a, s) in priors.items():
    log(f"slope left: {pn}: {a:+.3f} +- {s:.3f}")
    for gn, g in grids.items():
        r = J2.joint(Af, np.array(g["f"]), np.array(g["q0"]), An, np.array(g["n"]), np.array(g["t"]), a, s); out[f"{pn} | {gn}"] = r
        log(f"     {gn:42s} amplitude {r['A']:+.3f}  q0 {r['q0']:+.3f}  q0 = 0: dchi2 {r['D_today']:6.2f}  {word(r['q0'], r['D_today']):18s}  never accelerated: dchi2 {r['D_never']:6.1f}")
json.dump(out, open(os.path.join(HERE, "agb6_today.json"), "w"), indent=1, default=float); log("wrote agb6_today.json")
