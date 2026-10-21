"""CFG956 POST HOC (written after the MAIN result; no verdict weight): the galaxy-side shift G1 recomputed at each period's own
boundary wave (eps_95(P), phi_95(P)) instead of the frozen conservative 'any phi' maximum.  Reads cfg956.json and
cfg956_DAMPED.json only; no refit.  Also lists CFG689's own 68% band width (dex) at each point's z for context.
The oscillating-a0(z) hypothesis, including its damped form, is the owner's idea (2026-10-21).
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg956_posthoc_g1.py
"""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE)
M = json.load(open(os.path.join(HERE, "cfg956.json"))); D = json.load(open(os.path.join(HERE, "cfg956_DAMPED.json")))
J689 = json.load(open(os.path.join(CFG, "CFG689_native_ruler_bao", "cfg689.json")))
OUT = []
def P(s): print(s); OUT.append(s)
def ratio(z, e, Pp, ph, beta=0.0): return (1 + e*(1 + z)**beta*math.sin(2*math.pi*math.log1p(z)/Pp + ph))/(1 + e*math.sin(ph))
# CFG689 68% band width in dex at its nodes (z > 2.33 extrapolated as CFG689 P6 does)
bz = [1.0, 1.2, 1.5, 2.33]; bw = [math.log10(J689["BAO+SN"]["P1"][str(z)]["sqrtX_q"][3]/max(J689["BAO+SN"]["P1"][str(z)]["sqrtX_q"][1], 1e-3)) for z in bz]
def band_dex(z): return float(np.interp(z, bz, bw)) if z >= 1.0 else None
res = []
P("POST HOC G1 at each period's own boundary wave (eps_95, phi_95); no verdict weight")
P(f"{'point':58s} {'z':>6s} {'sig68':>6s} | {'G1_S':>6s} {'/sig':>5s} {'G1_C':>6s} {'/sig':>5s} | damped max {'G1':>6s} {'/sig':>5s} | CFG689 band68 dex")
for g in M["galaxy"]:
    if g["sigma_dex"] is None: continue
    row = dict(label=g["label"], z=g["z"], sigma_dex=g["sigma_dex"], conservative_G1_S=g["G1_S_dex"], conservative_G1_C=g["G1_C_dex"])
    for br in ("S", "C"):
        best, Pb = 0.0, None
        for r in M["rows"][br]:
            if r["phi95"] is None: continue
            v = abs(math.log10(max(ratio(g["z"], r["eps95"], r["P"], r["phi95"]), 1e-3)))
            if v > best: best, Pb = v, r["P"]
        row[f"G1b_{br}"], row[f"G1b_{br}_P"], row[f"G1b_{br}_over_sigma"] = best, Pb, best/g["sigma_dex"]
    bd, kb = 0.0, None
    for key, rr in D["rows"].items():
        for r in rr:
            if r["phi95"] is None: continue
            v = abs(math.log10(max(ratio(g["z"], r["eps95"], r["P"], r["phi95"], r["beta"]), 1e-3)))
            if v > bd: bd, kb = v, f"{key} P {r['P']}"
    row["G1b_damped"], row["G1b_damped_at"], row["G1b_damped_over_sigma"] = bd, kb, bd/g["sigma_dex"]
    row["CFG689_band68_dex"] = band_dex(g["z"]); res.append(row)
    bds = "-" if row["CFG689_band68_dex"] is None else f"{row['CFG689_band68_dex']:.2f}" + (" (extrap.)" if g["z"] > 2.33 else "")
    P(f"{g['label'][:58]:58s} {g['z']:6.3f} {g['sigma_dex']:6.3f} | {row['G1b_S']:6.3f} {row['G1b_S_over_sigma']:5.2f} {row['G1b_C']:6.3f} {row['G1b_C_over_sigma']:5.2f} | "
      f"{bd:6.3f} {row['G1b_damped_over_sigma']:5.2f} ({kb}) | {bds}")
n = sum(max(r["G1b_S_over_sigma"], r["G1b_C_over_sigma"]) > 1 for r in res); nd = sum(r["G1b_damped_over_sigma"] > 1 for r in res)
P(f"boundary-wave G1 exceeds the 68% statistical error for {n} of {len(res)} points (plain S/C) and {nd} (damped); frozen conservative G1: "
  f"{M['galaxy_summary']['n_G1_exceeds_sigma']}; distance effect G2 exceeds sigma for {M['galaxy_summary']['n_G2_exceeds_sigma']}")
# inner high-z window: the boundary waves themselves (eps_95, phi_95) at z 3-5 (the frozen window in cfg956_DAMPED.json is the
# outer one: eps0 up to eps0_95 at EVERY allowed phi); the true allowed window lies between the two
NODES = np.array(J689["cfg"]["nodes"]); WB = np.array(J689["BAO+SN"]["P2"]["pbest"][:6]); A233 = math.sqrt(WB[-1]/WB[0])
ZW = [3.0, 3.5, 4.0, 4.5, 5.0]; inner = {}
P("\nPOST HOC inner z 3-5 window: a0(z)/a0(0) of the boundary waves (eps_95, phi_95), min/max over P; clipped at 0")
for key, rr in list(D["rows"].items()) + [("plain_" + b, M["rows"][b]) for b in ("S", "C")]:
    A = A233 if key.endswith("S") else 1.0; lo, hi = {}, {}
    for z in ZW:
        v = [max(A*ratio(z, r["eps95"], r["P"], r["phi95"], r.get("beta", 0.0)), 0.0) for r in rr if r["phi95"] is not None]
        lo[str(z)], hi[str(z)] = min(v), max(v)
    inner[key] = dict(lo=lo, hi=hi)
    P(f"  {key:12s} " + ", ".join(f"z{z}: [{lo[str(z)]:.2f}, {hi[str(z)]:.2f}]" for z in ZW))
json.dump(dict(posthoc=True, note="after MAIN; no verdict weight", rows=res, n_exceed_plain=int(n), n_exceed_damped=int(nd), inner_window_z=ZW, inner_window=inner),
          open(os.path.join(HERE, "cfg956_POSTHOC_G1.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg956_POSTHOC_G1.out"), "w").write("\n".join(OUT) + "\n")
print("wrote cfg956_POSTHOC_G1.json / .out")
