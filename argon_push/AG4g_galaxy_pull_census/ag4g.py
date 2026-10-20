#!/usr/bin/env python3
"""AG4g: per-galaxy pull census on SPARC. MAP Upsilon under the stellar-population prior (n=1, canonical a0) with the coherent
distance/inclination term profiled analytically; stage 1 counts |pull| >= 3 galaxies against 200 law-true mocks from the fit's
own error model; stage 2 scans 11 pre-declared master-table properties (Spearman, permutation p, Holm-Bonferroni).
Criteria: FROZEN_CRITERIA.md (committed alone, before this script).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 ag4g.py      AG4G_MUTATE=1: injected Hubble-type-dependent Upsilon must be flagged.
kappa = 1/2 fitted; not theory closed. A LEAD is a pointer, not a detection."""
import json, math, os, sys
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity"); sys.path.insert(0, LANES)
import CFG4_common as C

MUT = os.environ.get("AG4G_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag4g{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n"); OUT.flush()
FAILS = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else "")); (None if ok else FAILS.append(name)); return ok

LN10 = math.log(10.0); KPC_S = 3.0857e19
LU0, SIG_U, S0 = math.log10(0.5), 0.10, 0.05
LU = LU0 + np.linspace(-0.5, 0.5, 201); UG = 10 ** LU; PRIOR = ((LU - LU0) / SIG_U) ** 2
NU1 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / y)); NU2 = lambda y: np.sqrt(1 + 1 / y)
A0C, A0A = C.A0["canonical"], C.A0["alt"]
P("AG4g: per-galaxy pull census (n=1, canonical a0; coherent distance/inclination term profiled)" + ("   *** MUTATE ***" if MUT else ""))
P("kappa = 1/2 fitted; not theory closed. A LEAD is a pointer, not a detection.")

# ------------------------------------------------------------------------------------------------ data (AG4b cuts)
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
    meta = g.get("meta") or {}
    cg = math.sqrt((meta["eD"] / meta["D"] / LN10) ** 2 + (2.0 / math.tan(max(math.radians(meta["Inc"]), 0.05)) * math.radians(meta["eInc"]) / LN10) ** 2) if meta else 0.0
    D_.append(dict(name=g["name"], go=go[m], gas=np.sign(Vg[m]) * Vg[m] ** 2 * 1e6 / Rm[m], star=(Vd[m] ** 2 + 1.4 * Vb[m] ** 2) * 1e6 / Rm[m],
                   sv=2.0 / LN10 * np.clip(eV[m], 1, None) / np.clip(Vo[m], 1, None), cg=cg, meta=meta))
NG = len(D_)
P(f"SPARC: {NG} galaxies (AG4b cuts); median coherent distance/inclination error c_g = {np.median([d['cg'] for d in D_]):.3f} dex")


def fit(data, nu, a0, use_cg=True):
    lus = np.empty(len(data))
    for k, d in enumerate(data):
        gb = d["gas"][:, None] + d["star"][:, None] * UG[None, :]
        r = np.log10(d["go"])[:, None] - np.log10(nu(gb / a0) * gb)
        w = 1.0 / (d["sv"] ** 2 + S0 ** 2); Sw = w.sum(); Swr = (w[:, None] * r).sum(0); Swr2 = (w[:, None] * r ** 2).sum(0)
        chi = Swr2 - (Swr ** 2 / (Sw + 1.0 / d["cg"] ** 2) if (use_cg and d["cg"] > 0) else 0.0) + PRIOR
        lus[k] = LU[int(np.argmin(chi))]
    return (lus - LU0) / SIG_U


def mock(nu, a0, seed, lu_true=None):
    rng = np.random.default_rng(seed); out = []
    for k, d in enumerate(D_):
        lu = float(np.clip(LU0 + SIG_U * rng.standard_normal(), LU[0], LU[-1])) if lu_true is None else float(np.clip(lu_true[k], LU[0], LU[-1]))
        gb = d["gas"] + d["star"] * 10 ** lu
        lgo = np.log10(nu(gb / a0) * gb) + d["cg"] * rng.standard_normal() + np.sqrt(d["sv"] ** 2 + S0 ** 2) * rng.standard_normal(len(gb))
        out.append(dict(d, go=10 ** lgo))
    return out


nlarge = lambda p: int(np.sum(np.abs(p) >= 3 - 1e-9))

# ------------------------------------------------------------------------------------------------ properties
def props(data):
    def m_(d, k):
        v = d["meta"].get(k) if d["meta"] else None
        return np.nan if v is None else float(v)
    L = np.array([m_(d, "L36") for d in data]); MHI = np.array([m_(d, "MHI") for d in data])
    V = np.array([m_(d, "Vflat") for d in data]); V[V <= 0] = np.nan
    lg = lambda x: np.log10(np.where(x > 0, x, np.nan))
    return {"T": np.array([m_(d, "T") for d in data]), "HubbleFlow(fD=1)": np.array([1.0 if m_(d, "fD") == 1 else 0.0 for d in data]),
            "Inc": np.array([m_(d, "Inc") for d in data]), "Q": np.array([m_(d, "Q") for d in data]), "logL36": lg(L),
            "logSBdisk": lg(np.array([m_(d, "SBdisk") for d in data])), "logRdisk": lg(np.array([m_(d, "Rdisk") for d in data])),
            "logMHI": lg(MHI), "Vflat": V, "eD/D": np.array([m_(d, "eD") / m_(d, "D") for d in data]),
            "gas_fraction": 1.33 * MHI / (1.33 * MHI + 0.5 * L)}


def spearman_perm(x, y, B, seed):
    ok = np.isfinite(x) & np.isfinite(y); x, y = x[ok], y[ok]; n = len(x)
    rx = rankdata(x); ry = rankdata(y); rx = (rx - rx.mean()) / rx.std(); ry = (ry - ry.mean()) / ry.std()
    rho = float(np.mean(rx * ry))
    rng = np.random.default_rng(seed); Pm = rng.permuted(np.tile(ry, (B, 1)), axis=1)
    rb = Pm @ rx / n
    return rho, float((1 + np.sum(np.abs(rb) >= abs(rho) - 1e-12)) / (B + 1)), n


def scan(pulls, PR, B, seed=20261020):
    rows = []
    for kname, x in PR.items():
        for sn, y in (("signed", pulls), ("|pull|", np.abs(pulls))):
            rho, pv, n = spearman_perm(x, y, B, seed); rows.append(dict(prop=kname, stat=sn, rho=rho, p=pv, n=n))
    order = np.argsort([r["p"] for r in rows]); m = len(rows); run = 0.0
    for i, j in enumerate(order):                                     # Holm step-down adjusted p
        run = max(run, min(1.0, (m - i) * rows[j]["p"])); rows[j]["p_holm"] = run
    for r in rows:
        r["lead"] = r["p_holm"] < 0.05
    return rows


PR = props(D_)
if MUT:
    zT = (PR["T"] - np.nanmean(PR["T"])) / np.nanstd(PR["T"])
    md = mock(NU1, A0C, 777, lu_true=LU0 + 0.10 * zT); pm = fit(md, NU1, A0C); rows = scan(pm, PR, 10000)
    rT = [r for r in rows if r["prop"] == "T" and r["stat"] == "signed"][0]
    P(f"MUTATE: injected log U = log 0.5 + 0.10 z_T; scan on T (signed): rho {rT['rho']:+.3f}, p {rT['p']:.4f}, Holm {rT['p_holm']:.4f}")
    bites = rT["lead"]
    P(f"MUTATE: {'control BITES (T flagged; exit 1, as designed)' if bites else 'control DID NOT BITE (recorded)'}")
    json.dump(dict(lane="AG4g", mutate=True, T_signed=rT, rows=rows), open(os.path.join(HERE, f"ag4g_results{TAG}.json"), "w"), indent=1, default=float)
    OUT.close(); sys.exit(1 if bites else 0)

# ------------------------------------------------------------------------------------------------ stage 1
P("\nControls")
p_nocg = fit(D_, NU1, A0C, use_cg=False)
check("K1 without the D/inc term, the large-pull fraction reproduces AG4b's 22.4% to +-1 galaxy", abs(nlarge(p_nocg) - 0.224 * NG) <= 1.0,
      f"{nlarge(p_nocg)} of {NG} = {nlarge(p_nocg) / NG:.1%}")
S1 = {}
for wn, nu, a0, s0 in (("n=1 canonical (PRIMARY)", NU1, A0C, 0), ("n=1 alt", NU1, A0A, 1000), ("n=2 alt", NU2, A0A, 2000)):
    p_obs = fit(D_, nu, a0); Nobs = nlarge(p_obs)
    Nm, mmean = [], []
    for s in range(1, 201):
        pm = fit(mock(nu, a0, s0 + s), nu, a0); Nm.append(nlarge(pm)); mmean.append(float(np.mean(pm)))
    Nm = np.array(Nm); p1 = float(np.mean(Nm >= Nobs))
    S1[wn] = dict(N_obs=Nobs, frac_obs=Nobs / NG, N_mock_mean=float(Nm.mean()), N_mock_p99=float(np.percentile(Nm, 99)), N_mock_max=int(Nm.max()),
                  p1=p1, reading="EXCESS" if p1 < 0.01 else "NO EXCESS", mock_mean_pull=float(np.mean(mmean)), pulls=p_obs.tolist())
    P(f"  {wn}: large pulls {Nobs} of {NG} ({Nobs / NG:.1%}); law-true mocks {Nm.mean():.1f} on average (99th pct {np.percentile(Nm, 99):.0f}, max {Nm.max()}); "
      f"p = {p1:.3f} -> {S1[wn]['reading']}; signed pulls: median {np.median(p_obs):+.2f}, >=+3: {int(np.sum(p_obs >= 3 - 1e-9))}, <=-3: {int(np.sum(p_obs <= -3 + 1e-9))}")
    if wn.endswith("(PRIMARY)"):
        check("K2 mock mean pull within +-0.1 of 0", abs(np.mean(mmean)) <= 0.1, f"{np.mean(mmean):+.3f}")
prim = S1["n=1 canonical (PRIMARY)"]; pulls = np.array(prim["pulls"])
P(f"\nSTAGE 1 (primary): {prim['reading']}")
top = np.argsort(-np.abs(pulls))[:15]
P("  largest pulls (name, pull, T, fD, Inc, Q, c_g):")
for k in top:
    m = D_[k]["meta"] or {}
    P(f"    {D_[k]['name']:12s} {pulls[k]:+5.2f}  T {m.get('T')}  fD {m.get('fD')}  Inc {m.get('Inc')}  Q {m.get('Q')}  c_g {D_[k]['cg']:.3f}")

# ------------------------------------------------------------------------------------------------ stage 2
P(f"\nSTAGE 2 property scan ({'GRADED' if prim['reading'] == 'EXCESS' else 'EXPLORATORY: stage 1 found no excess'}); Spearman, 10,000 permutations, Holm")
rows = scan(pulls, PR, 10000)
for r in sorted(rows, key=lambda r: r["p"]):
    P(f"  {r['prop']:18s} {r['stat']:7s} rho {r['rho']:+.3f}  n {r['n']:3d}  p {r['p']:.4f}  Holm {r['p_holm']:.4f}{'  <- LEAD' if r['lead'] else ''}")
leads = [f"{r['prop']} ({r['stat']})" for r in rows if r["lead"]]
P(f"  leads: {leads or 'none'}")
# K3: the scan's family-wise false-positive rate on law-true mocks
fw = 0
for s in range(1001, 1051):
    pm = fit(mock(NU1, A0C, s), NU1, A0C); fw += any(r["lead"] for r in scan(pm, PR, 1000, seed=s))
check("K3 scan family-wise false-positive rate on 50 law-true mocks <= 0.10", fw / 50 <= 0.10, f"{fw}/50")

P(f"\nAG4g: stage 1 {prim['reading']} (primary); stage 2 leads: {leads or 'none'}" + ("" if prim["reading"] == "EXCESS" else " (exploratory)"))
P(f"controls failed: {FAILS or 'none'}")
json.dump(dict(lane="AG4g", mutate=False, stage1={k: {kk: vv for kk, vv in v.items()} for k, v in S1.items()}, stage2=rows, leads=leads,
               K3_fw=fw / 50, names=[d["name"] for d in D_]), open(os.path.join(HERE, "ag4g_results.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(1 if FAILS else 0)
