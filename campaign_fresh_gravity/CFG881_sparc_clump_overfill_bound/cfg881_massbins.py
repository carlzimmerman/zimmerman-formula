"""CFG881 POST-HOC DESCRIPTIVE breakdown (written after the frozen run; does not change the class).
Reads cfg881_results.json and prints the primary F_max by baryonic-mass bin and its trend with M_b.  Run: python3 cfg881_massbins.py"""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(HERE, "cfg881_results.json"))); OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
BINS = ((1e9, 1e10), (1e10, 5e10), (5e10, 1e13)); RES = {}
P("CFG881 post-hoc descriptive: primary F_max (floor 0.10, convention A, M_block = M_cl) by M_b bin")
for foot in ("canonical", "alt"):
    rows = R[foot]["rows"]; RES[foot] = {}
    P(f"\n  [{foot}]   shape    " + "   ".join(f"M_b {lo:.0e}-{hi:.0e}: N, median F [16-84%]" if hi < 1e13 else f"M_b >= {lo:.0e}: N, median F [16-84%]" for lo, hi in BINS))
    for sh in ("CORE1", "CORE3", "BARYON", "FLAT"):
        cells = []; RES[foot][sh] = {}
        for lo, hi in BINS:
            F = np.array([r["shapes"][sh]["primary"]["F_max"] for r in rows.values() if lo <= r["Mb"] < hi and sh in r["shapes"]])
            c = dict(N=len(F), med=float(np.median(F)) if len(F) else float("nan"),
                     p16=float(np.percentile(F, 16)) if len(F) else float("nan"), p84=float(np.percentile(F, 84)) if len(F) else float("nan"))
            RES[foot][sh][f"{lo:.0e}-{hi:.0e}"] = c; cells.append(f"{c['N']:3d}, {c['med']:.3f} [{c['p16']:.3f}-{c['p84']:.3f}]")
        xs = [(np.log10(r["Mb"]), np.log10(r["shapes"][sh]["primary"]["F_max"])) for r in rows.values() if r["Mb"] >= 1e9 and sh in r["shapes"]]
        x, y = np.array(xs).T; b = float(np.polyfit(x, y, 1)[0]); RES[foot][sh]["slope_logF_logMb"] = b
        P(f"     {sh:7s}  " + "      ".join(cells) + f"     slope dlogF/dlogM_b {b:+.2f}")
json.dump(RES, open(os.path.join(HERE, "cfg881_massbins.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg881_massbins.out"), "w").write("\n".join(OUT) + "\n")
