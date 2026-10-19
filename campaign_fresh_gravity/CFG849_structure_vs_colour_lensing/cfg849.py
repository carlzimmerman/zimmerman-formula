"""CFG849 -- structure (Sersic) vs colour carrying the low-g isolated-lens excess.  Criteria: FROZEN_CRITERIA.md.
Reuses cfg829.py's loader and amplitude.  Run: python3 cfg849.py (CFG849_MUTATE=1).  kappa = 1/2 FITTED; not theory closed."""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG849_MUTATE") == "1"; os.environ.pop("CFG829_MUTATE", None)
src = open(os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py")).read().split("P(\"CFG829  KiDS")[0]
M = {"__file__": os.path.join(LANES, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py"), "__name__": "d"}; exec(compile(src, "cfg829.py", "exec"), M)
load, amp, nu_e, A0 = M["load"], M["amp"], M["nu_e"], M["A0"]; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
W = (10 ** -13.3, 10 ** -11.9)
B = {"blue": ("Fig-8_RAR-KiDS-isolated_Colorbin_1.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 0.0),
     "red": ("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5),
     "disc n<2": ("Fig-8_RAR-KiDS-isolated_Sersicbin_1.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 0.0),
     "sph n>2": ("Fig-8_RAR-KiDS-isolated_Sersicbin_2.txt", "Fig-8_RAR-KiDS-isolated_Sersicbins_covmatrix.txt", 2.0)}
P("CFG849  structure vs colour at the dwarfs' g_bar" + ("  [MUTATE g_obs x1.5 for n>2]" if MUT else ""))
RES = dict(lane="CFG849", mutate=MUT)
for foot in ("canonical", "alt"):
    A = {}
    for k, (f, c, bm) in B.items():
        gb, go, C = load(f, c, bm)
        if MUT and k == "sph n>2": go = go * 1.5; C = C * 2.25
        gl = gb * nu_e(gb / A0[foot]); a = amp(gb, go, C, gl, W); A[k] = (a["A"], a["sA"])
    dc, sc = A["red"][0] - A["blue"][0], math.hypot(A["red"][1], A["blue"][1]); ds, ss = A["sph n>2"][0] - A["disc n<2"][0], math.hypot(A["sph n>2"][1], A["disc n<2"][1])
    s1 = math.hypot(sc, ss)
    if ds >= 3 * ss and dc >= 3 * sc and abs(ds - dc) < s1: cls = "BOTH / DEGENERATE"
    elif ds >= 3 * ss and ds >= dc: cls = "STRUCTURE CARRIES IT"
    elif dc >= 3 * sc and dc > ds + s1: cls = "COLOUR CARRIES IT"
    else: cls = "NO SPLIT"
    RES[foot] = dict(A={k: list(v) for k, v in A.items()}, d_colour=[dc, sc], d_sersic=[ds, ss], cls=cls)
    P(f"\n  [{foot}] " + "  ".join(f"{k} {v[0]:.3f}+-{v[1]:.3f}" for k, v in A.items()))
    P(f"     colour split red-blue {dc:+.3f} +- {sc:.3f} ({dc / sc:+.1f} sigma);  Sersic split sph-disc {ds:+.3f} +- {ss:.3f} ({ds / ss:+.1f} sigma)  -> {cls}")
if not MUT: P(f"\n  K1 blue {RES['canonical']['A']['blue'][0]:.3f} / red {RES['canonical']['A']['red'][0]:.3f} vs CFG829 1.016 / 1.587")
RES["cls"] = RES["canonical"]["cls"]; P(f"\n  CLASS (canonical): {RES['cls']}")
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg849_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg849{sfx}.out"), "w").write("\n".join(OUT) + "\n")
