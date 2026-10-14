"""CFG782 -- the untether-on-unbinding selector (photo-evaporation at reionization), derived and scored before the fossil test.
Criteria: FROZEN_CRITERIA.md (82c20ae1b) + ERRATUM_PRE_SCRIPT (f8e581283: K1/K2 against the correct analytic values).
SUDDEN iff V_init = (G R_ind M_b,now a0)^(1/4) < V_th = sqrt(2) c_s(T_IGM), c_s = sqrt(k T/(mu m_p)), mu = 0.59.
Run: python3 cfg782.py   (CFG782_MUTATE=1: R_ind = 1).  Seconds, tiny.
kappa = 1/2 FITTED; not theory closed.  A postulate's selector, not a derivation of the two populations.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402

MUT = os.environ.get("CFG782_MUTATE") == "1"
OUT = []


def P(s=""):
    print(s, flush=True)
    OUT.append(str(s))


G, MSUN, KB, MP = 6.674e-11, 1.989e30, 1.380649e-23, 1.6726e-27
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
cs = lambda T: math.sqrt(KB * T / (0.59 * MP)) / 1e3
Vth = {T: math.sqrt(2) * cs(T) for T in (1e4, 1.5e4, 2e4)}
Vinit = lambda M, a0: (G * M * MSUN * a0) ** 0.25 / 1e3
FAILS = []


def check(n, ok, d):
    P(f"  [{'PASS' if ok else 'FAIL'}] {n}: {d}")
    if not ok:
        FAILS.append(n)


P("CFG782  untether-on-unbinding selector" + ("  [MUTATE R_ind = 1]" if MUT else ""))
check("K1 c_s(1.5e4 K) analytic", abs(cs(1.5e4) - 14.49) < 0.01, f"{cs(1.5e4):.3f} km/s (frozen hand value 14.6 was wrong; erratum)")
check("K2 V_init(1e6 Msun, canonical)", abs(Vinit(1e6, A0['canonical']) - 10.56) < 0.01, f"{Vinit(1e6, A0['canonical']):.3f} km/s (frozen hand 10.4; erratum)")
P("  V_th at T_IGM 1 / 1.5 / 2 e4 K: " + " / ".join(f"{v:.2f}" for v in Vth.values()) + " km/s")

j = json.load(open(os.path.join(LANES, "CFG317_baryon_loss_cold_mass", "cfg317_baryon_loss_results.json")))["numbers"]
EST, NAMES = j["EST"], j["NAMES"]
groups = {"MW UFDs": "ufd", "MW classicals": "cls", "M31 (Collins)": "col", "M31 (LVD)": "m31", "LV field": "fld"}
objs = {}
allpts = []
for lab, key in groups.items():
    lst = []
    for nm, e in zip(NAMES[key], EST[f"-0.2|{key}"]):
        if e is None:
            continue
        Mb = float(e["Ms"]) + float(e.get("Mg") or 0.0)
        lR = e.get("lR")
        lst.append(dict(name=nm, Mb=Mb, lR=(None if lR is None else float(lR))))
        if lR is not None:
            allpts.append((math.log10(Mb), float(lR)))
    objs[lab] = lst
X = np.array(allpts)
slope, icpt = np.polyfit(X[:, 0], X[:, 1], 1)
P(f"  CFG317 relation (OLS on {len(X)} per-object values): log R_ind = {icpt:+.3f} {slope:+.3f} log M_b,now   (used where no per-object R_ind)")
lRrel = lambda Mb: icpt + slope * math.log10(Mb)
# SPARC: M_b = V_bar^2 R / G at the last point (Upsilon_disk 0.5, Upsilon_bul 0.7)
sp = []
_sp = C4.load_sparc()
for g in (_sp[0] if isinstance(_sp, tuple) else _sp):
    vb2 = g["Vgas"][-1] * abs(g["Vgas"][-1]) + 0.5 * g["Vdisk"][-1] ** 2 + 0.7 * g["Vbul"][-1] ** 2
    Mb = max(vb2, 1e-6) * 1e6 * g["R"][-1] * 3.0857e19 / G / MSUN
    sp.append(dict(name=g["name"], Mb=float(Mb), lR=None))
objs["SPARC"] = sp

RES = {"lane": "CFG782", "mutate": MUT, "relation": dict(slope=float(slope), icpt=float(icpt)), "groups": {}}
for foot, a0 in A0.items():
    for T, vt in Vth.items():
        tag = f"{foot}|T{T:.1e}"
        row = {}
        for lab, lst in objs.items():
            flags, details = [], []
            for o in lst:
                lR = 0.0 if MUT else (o["lR"] if o["lR"] is not None else lRrel(o["Mb"]))
                lR = max(lR, 0.0)                                     # R_ind >= 1 (no baryon gain)
                v = Vinit(o["Mb"] * 10 ** lR, a0)
                flags.append(v < vt)
                details.append((o["name"], round(v, 1)))
            frac = float(np.mean(flags)) if flags else float("nan")
            row[lab] = dict(N=len(flags), frac_sudden=frac, flagged=[d for d, f in zip(details, flags) if f] if lab != "MW UFDs" else None)
        RES["groups"][tag] = row
        if foot == "canonical" or T == 1.5e4:
            P(f"\n  {tag}: V_th {vt:.2f} km/s")
            for lab, r in row.items():
                extra = "" if lab == "MW UFDs" else f"; flagged: {r['flagged'][:8]}{' ...' if r['flagged'] and len(r['flagged']) > 8 else ''}"
                P(f"    {lab:15s} N {r['N']:3d}: SUDDEN fraction {r['frac_sudden']:.2f}{extra}")

prim = RES["groups"]["canonical|T1.5e+04"]
s1 = prim["MW UFDs"]["frac_sudden"] >= 0.90
s2 = {lab: prim[lab]["frac_sudden"] <= 0.10 for lab in prim if lab != "MW UFDs"}
s2_ends = all(RES["groups"][f"canonical|T{T:.1e}"][lab]["frac_sudden"] <= 0.10 for T in (1e4, 2e4) for lab in s2)
P(f"\n  S1 (>= 90% of UFDs SUDDEN): {prim['MW UFDs']['frac_sudden']:.2f} -> {'PASS' if s1 else 'FAIL'}")
P("  S2 (<= 10% of each passing group SUDDEN, primary): " + "; ".join(f"{k} {prim[k]['frac_sudden']:.2f} {'PASS' if v else 'FAIL'}" for k, v in s2.items()))
if not MUT:
    if s1 and all(s2.values()):
        verdict = "SELECTOR VIABLE" if s2_ends else "BORDERLINE (S2 fails only at a bracket end)"
    else:
        verdict = "DEAD"
    P(f"  VERDICT: {verdict}")
    RES["verdict"] = verdict
else:
    P("  MUTATE: flag set with R_ind = 1 (current baryons only) - must differ from the main run")
RES["S1"] = bool(s1); RES["S2"] = {k: bool(v) for k, v in s2.items()}; RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"cfg782_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg782{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if (FAILS or MUT) else 0)
