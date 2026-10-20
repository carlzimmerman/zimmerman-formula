#!/usr/bin/env python3
"""AG4f: is the footing-law pairing (n=1 <-> canonical rho_Lambda, n=2 <-> alt rho_total) physics or a cross-fitting artefact?
SPARC cross-law ratio R = a0_best(n=2)/a0_best(n=1) (AG4b pipeline: per-galaxy MAP Upsilon under the population prior), galaxy
bootstrap, mock worlds W1 = (n=1, a0_canonical) and W2 = (n=2, a0_alt), and three mix splits.
Criteria: FROZEN_CRITERIA.md (committed alone, before this script).  Run: OMP_NUM_THREADS=1 nice -n 10 python3 ag4f.py
AG4F_MUTATE=1 replaces nu2 by nu1 everywhere: R must be exactly 1 (exit 1 = bites).
kappa = 1/2 fitted; footings never pooled in a verdict; not theory closed. T = a0_alt/a0_canonical = 1/sqrt(Omega_L) is an
identity of the footing definitions, not a result."""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity"); sys.path.insert(0, LANES)
import CFG4_common as C

MUT = os.environ.get("AG4F_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag4f{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n"); OUT.flush()
FAILS = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else "")); (None if ok else FAILS.append(name)); return ok

LN10 = math.log(10.0); KPC_S = 3.0857e19
LU0, SIG_U, S0 = math.log10(0.5), 0.10, 0.05
LU = LU0 + np.linspace(-0.5, 0.5, 201); UG = 10 ** LU; PRIOR = ((LU - LU0) / SIG_U) ** 2
LA = np.linspace(-10.30, -9.70, 301); AG = 10 ** LA
NU1 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / y))
NU2 = NU1 if MUT else (lambda y: np.sqrt(1 + 1 / y))
A0C, A0A = C.A0["canonical"], C.A0["alt"]; T = A0A / A0C
P("AG4f: footing-law pairing test" + ("   *** MUTATE: nu2 := nu1 ***" if MUT else ""))
P("kappa = 1/2 fitted; footings never pooled in a verdict; not theory closed.")
P(f"T = a0_alt/a0_canonical = {T:.5f} = 1/sqrt(Omega_L): an identity of the footing definitions (target only, not a result)")

# ------------------------------------------------------------------------------------------------ data (AG4b's cuts)
GAL = C.load_sparc(); D_ = []
for g in GAL:
    R, Vo, eV, Vg, Vd, Vb = (np.asarray(g[k], float) for k in ("R", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"))
    Rm = R * KPC_S
    gb_lo = (np.sign(Vg) * Vg ** 2 + UG[0] * Vd ** 2 + 1.4 * UG[0] * Vb ** 2) * 1e6 / Rm
    gb_hi = (np.sign(Vg) * Vg ** 2 + UG[-1] * Vd ** 2 + 1.4 * UG[-1] * Vb ** 2) * 1e6 / Rm
    go = (Vo * 1e3) ** 2 / Rm
    m = (Vo > 0) & (go > 0) & (gb_lo > 0) & (gb_hi > 0) & np.isfinite(go) & (R > 0)
    if m.sum() < 5:
        continue
    gas = np.sign(Vg[m]) * Vg[m] ** 2 * 1e6 / Rm[m]; star = (Vd[m] ** 2 + 1.4 * Vb[m] ** 2) * 1e6 / Rm[m]
    sv = 2.0 / LN10 * np.clip(eV[m], 1, None) / np.clip(Vo[m], 1, None)
    meta = g.get("meta") or {}
    gb5 = gas + 0.5 * star; j = int(np.argmax(R[m]))
    D_.append(dict(name=g["name"], go=go[m], gas=gas, star=star, sv=sv,
                   fdeep=float(np.mean(gb5 / A0C < 0.3)), SB=float(meta.get("SBdisk", np.nan)), fgas=float(gas[j] / gb5[j])))
NG = len(D_)
P(f"SPARC: {NG} galaxies (AG4b cuts), {sum(len(d['go']) for d in D_)} points")


def curves(data, nu):
    """(Ngal, 301): per-galaxy chi2_min over Upsilon (MAP with prior) at each a0 on the fine grid."""
    out = np.empty((len(data), len(AG)))
    for k, d in enumerate(data):
        gb = d["gas"][:, None] + d["star"][:, None] * UG[None, :]                    # (n, 201)
        lgo = np.log10(d["go"]); s2 = d["sv"] ** 2 + S0 ** 2
        for c0 in range(0, len(AG), 43):
            a = AG[c0:c0 + 43]
            r = lgo[:, None, None] - np.log10(nu(gb[:, :, None] / a[None, None, :]) * gb[:, :, None])   # (n, 201, na)
            c2 = (r ** 2 / s2[:, None, None]).sum(0) + PRIOR[:, None]
            out[k, c0:c0 + 43] = c2.min(0)
    return out


def best(cur, w=None):
    S = cur.sum(0) if w is None else w @ cur
    return AG[np.argmin(S, axis=-1)]


RNG = np.random.default_rng(20261020)
def boot_counts(n, nb=1000):
    idx = RNG.integers(0, n, (nb, n)); W = np.zeros((nb, n))
    for b in range(nb):
        W[b] = np.bincount(idx[b], minlength=n)
    return W


def ratio(c1, c2, W=None):
    a1, a2 = best(c1), best(c2); R0 = a2 / a1
    if W is None:
        return dict(a1=float(a1), a2=float(a2), R=float(R0))
    b1, b2 = best(c1, W), best(c2, W); Rb = b2 / b1
    return dict(a1=float(a1), a2=float(a2), R=float(R0), sR=float(np.std(Rb)), s_la1=float(np.std(np.log10(b1))), s_la2=float(np.std(np.log10(b2))))


def mock(truth_nu, a0, seed):
    rng = np.random.default_rng(seed); out = []
    for d in D_:
        lu = float(np.clip(LU0 + SIG_U * rng.standard_normal(), LU[0], LU[-1])); gb = d["gas"] + d["star"] * 10 ** lu
        noise = 0.05 * rng.standard_normal() + np.sqrt(d["sv"] ** 2 + 0.05 ** 2) * rng.standard_normal(len(gb))
        out.append(dict(d, go=truth_nu(gb / a0) * gb * 10 ** noise))
    return out


# ------------------------------------------------------------------------------------------------ data
c1, c2 = curves(D_, NU1), curves(D_, NU2)
W = boot_counts(NG); obs = ratio(c1, c2, W)
P(f"\nDATA: n=1 best a0 {obs['a1']:.4e} (+-{obs['s_la1']:.3f} dex), n=2 best a0 {obs['a2']:.4e} (+-{obs['s_la2']:.3f} dex); "
  f"R = {obs['R']:.4f} +- {obs['sR']:.4f};  (R - T)/sigma = {(obs['R'] - T) / obs['sR'] if obs['sR'] > 0 else 0:+.2f}")
p1 = abs(math.log10(obs["a1"] / A0C)) <= 2 * obs["s_la1"]; p2 = abs(math.log10(obs["a2"] / A0A)) <= 2 * obs["s_la2"]
P(f"  n=1 best a0 vs canonical footing: {math.log10(obs['a1'] / A0C):+.4f} dex ({'within' if p1 else 'outside'} 2 sigma); "
  f"n=2 best a0 vs alt footing: {math.log10(obs['a2'] / A0A):+.4f} dex ({'within' if p2 else 'outside'} 2 sigma)")

P("\nControls")
check("K1 AG4b S3 reproduced to 0.01 dex (n=1 9.333e-11, n=2 1.148e-10)",
      MUT or (abs(math.log10(obs["a1"] / 9.333e-11)) <= 0.01 and abs(math.log10(obs["a2"] / 1.148e-10)) <= 0.01), f"{obs['a1']:.4e} / {obs['a2']:.4e}")

# ------------------------------------------------------------------------------------------------ worlds
WORLDS = {"W1 (n=1, canonical)": (NU1, A0C, range(101, 121)), "W2 (n=2, alt)": (NU2, A0A, range(121, 141))}
WR = {}
for wn, (tnu, ta0, seeds) in WORLDS.items():
    rs, a1s, a2s = [], [], []
    for s in seeds:
        md = mock(tnu, ta0, s); r_ = ratio(curves(md, NU1), curves(md, NU2)); rs.append(r_["R"]); a1s.append(r_["a1"]); a2s.append(r_["a2"])
    mu, sd = float(np.mean(rs)), float(np.std(rs, ddof=1))
    cons = abs(obs["R"] - mu) <= 2 * math.sqrt(sd ** 2 + obs["sR"] ** 2)
    WR[wn] = dict(mu=mu, sd=sd, consistent=bool(cons), R=rs, a1_med=float(np.median(a1s)), a2_med=float(np.median(a2s)))
    P(f"  {wn}: mock R = {mu:.4f} +- {sd:.4f} (n=1 fits a0 {np.median(a1s):.4e}, n=2 fits {np.median(a2s):.4e}); R_obs {'CONSISTENT' if cons else 'INCONSISTENT'}")
k2md = mock(NU1, A0C, 101); k2a = best(curves(k2md, NU1))
check("K2 W1 mock (seed 101) fitted with n=1 recovers a0_canonical to 0.02 dex", abs(math.log10(k2a / A0C)) <= 0.02, f"{k2a:.4e}")

# ------------------------------------------------------------------------------------------------ mix splits
P("\nMix splits (median halves)")
SPL = {}
for sn, key in (("(a) deep fraction", "fdeep"), ("(b) SBdisk", "SB"), ("(c) gas fraction at last point", "fgas")):
    v = np.array([d[key] for d in D_]); ok = np.isfinite(v); med = float(np.median(v[ok])); res = {}
    for half, msk in (("hi", ok & (v > med)), ("lo", ok & (v <= med))):
        ii = np.where(msk)[0]; res[half] = ratio(c1[ii], c2[ii], boot_counts(len(ii)))
    dl = res["hi"]["R"] - res["lo"]["R"]; sdl = math.sqrt(res["hi"]["sR"] ** 2 + res["lo"]["sR"] ** 2)
    SPL[sn] = dict(median=med, hi=res["hi"], lo=res["lo"], delta=dl, s_delta=sdl, z=dl / sdl if sdl > 0 else 0.0)
    P(f"  {sn}: R(hi) {res['hi']['R']:.4f} +- {res['hi']['sR']:.4f}, R(lo) {res['lo']['R']:.4f} +- {res['lo']['sR']:.4f}; delta {dl:+.4f} +- {sdl:.4f} (z {SPL[sn]['z']:+.2f})")

# ------------------------------------------------------------------------------------------------ reading
nd = obs["sR"] > 0.04 or any(w["sd"] > 0.04 for w in WR.values())
cw = [k for k, w in WR.items() if w["consistent"]]
if nd:
    rd = "NOT DIAGNOSTIC"
elif len(cw) == 2:
    rd = "PAIRS DEGENERATE (by construction)"
elif len(cw) == 1:
    rd = ("W1 FAVOURED" if cw[0].startswith("W1") else "W2 FAVOURED")
else:
    rd = "NEITHER"
mixdep = any(abs(s["z"]) > 3 for s in SPL.values())
if mixdep and not nd:
    rd += " + MIX-DEPENDENT"
P(f"\nREADING: {rd}")
if MUT:
    allone = abs(obs["R"] - 1) < 1e-12 and all(abs(r - 1) < 1e-12 for w in WR.values() for r in w["R"])
    P(f"MUTATE (nu2 := nu1): R = 1 everywhere -> {'control BITES (exit 1, as designed)' if allone else 'control DID NOT BITE (recorded)'}")
P(f"controls failed: {FAILS or 'none'}")
json.dump(dict(lane="AG4f", mutate=MUT, T=T, data=obs, a1_within_canonical=p1, a2_within_alt=p2, worlds=WR, splits=SPL, reading=rd),
          open(os.path.join(HERE, f"ag4f_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(1 if (MUT and abs(obs["R"] - 1) < 1e-12) or FAILS else 0)
