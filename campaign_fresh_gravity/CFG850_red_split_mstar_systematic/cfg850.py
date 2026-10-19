"""CFG850 -- red/spheroidal low-g lensing excess vs the LePhare M* bias (CFG667).  Criteria: FROZEN_CRITERIA.md.
Reuses cfg829.py.  Run: python3 cfg850.py (CFG850_MUTATE=1).  kappa = 1/2 FITTED; not theory closed."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG850_MUTATE") == "1"; os.environ.pop("CFG829_MUTATE", None)
src = open(os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py")).read().split("P(\"CFG829  KiDS")[0]
M = {"__file__": os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py"), "__name__": "d"}; exec(compile(src, "cfg829.py", "exec"), M)
load, amp, nu_e, A0 = M["load"], M["amp"], M["nu_e"], M["A0"]; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
W = (10 ** -13.3, 10 ** -11.9)
F = {"blue": ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
     "red": ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5),
     "disc": ("Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0),
     "sph": ("Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0)}
def A(k, foot, sh):
    gb, go, C = load(*F[k]); gbs = gb * 10 ** sh; return amp(gbs, go, C, gbs * nu_e(gbs / A0[foot]), W)
VAR = [(0.0, 0.0), (0.123, 0.0), (0.20, 0.0), (0.123, 0.05), (0.20, 0.05)] if not MUT else [(0.8, 0.0)]
P("CFG850  red/spheroidal low-g excess vs the LePhare M* bias" + ("  [MUTATE red +0.8 dex]" if MUT else ""))
RES = dict(lane="CFG850", mutate=MUT, rows={})
for foot in ("canonical", "alt"):
    P(f"\n  [{foot}]  shift(red/sph, blue/disc)   A_red  A_blue  split(sigma)   |  A_sph  A_disc  split(sigma)")
    for sr, sb in VAR:
        r, b, s, d = A("red", foot, sr), A("blue", foot, sb), A("sph", foot, sr), A("disc", foot, sb)
        z1 = (r["A"] - b["A"]) / math.hypot(r["sA"], b["sA"]); z2 = (s["A"] - d["A"]) / math.hypot(s["sA"], d["sA"])
        RES["rows"][f"{foot}|{sr}|{sb}"] = dict(A_red=r["A"], A_blue=b["A"], z_colour=z1, A_sph=s["A"], A_disc=d["A"], z_sersic=z2)
        P(f"           (+{sr:.3f}, +{sb:.2f})          {r['A']:.3f}  {b['A']:.3f}  {z1:+5.1f}        |  {s['A']:.3f}  {d['A']:.3f}  {z2:+5.1f}")
c = RES["rows"]
if MUT: cls = "SPLIT IS M*" if c["canonical|0.8|0.0"]["z_colour"] < 2 else "SPLIT SURVIVES (mutate did not bite)"
else:
    z123, z20 = c["canonical|0.123|0.0"]["z_colour"], c["canonical|0.2|0.0"]["z_colour"]
    cls = "SPLIT SURVIVES" if (z123 >= 3 and z20 >= 2) else ("SPLIT IS M*" if z123 < 2 else "WEAKENED")
    P(f"\n  K1 zero shift: red {c['canonical|0.0|0.0']['A_red']:.3f} blue {c['canonical|0.0|0.0']['A_blue']:.3f} (CFG829 1.587 / 1.016)")
RES["cls"] = cls; P(f"\n  CLASS: {cls}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg850_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg850{sfx}.out"), "w").write("\n".join(OUT) + "\n")
