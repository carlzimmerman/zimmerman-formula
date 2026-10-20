#!/usr/bin/env python3
"""AG4b: SPARC law-form comparison, n=1 (canonical, nu1 = (1 + sqrt(1 + 4/y))/2) vs n=2 (quadratic a0-line, nu2 = sqrt(1 + 1/y)),
each galaxy's Upsilon_disk fitted (MAP) under a stellar-population prior N(log 0.50, 0.10 dex), bulge 1.4x, both footings.
Criteria: FROZEN_CRITERIA.md (committed alone, before this script).  Run: OMP_NUM_THREADS=1 nice -n 10 python3 ag4b.py
AG4B_MUTATE=1 runs the pipeline on the n=1-truth mock (seed 1) in place of the data; it must FLIP on both footings (exit 1 = bites).
kappa = 1/2 fitted; footings never pooled; cold-energy mass required; not theory closed."""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
LANES = os.path.join(REPO, "campaign_fresh_gravity"); sys.path.insert(0, LANES)
import CFG4_common as C                                                # the record's SPARC loader, footings and constants

MUT = os.environ.get("AG4B_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"ag4b{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n"); OUT.flush()
FAILS = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f": {detail}" if detail else "")); (None if ok else FAILS.append(name)); return ok

LN10 = math.log(10.0); KPC_S = 3.0857e19                              # the record's kpc (CFG4/CFG695)
LU0, SIG_U, S0 = math.log10(0.5), 0.10, 0.05
LU = LU0 + np.linspace(-0.5, 0.5, 201); UG = 10 ** LU
NU1 = lambda y: 0.5 * (1 + np.sqrt(1 + 4 / y))
NU2 = lambda y: np.sqrt(1 + 1 / y)
LAWS = {"n1": NU1, "n2": NU2}
A0 = {f: C.A0[f] for f in C.FOOTS}
P("AG4b: n=1 vs n=2 on SPARC with stellar-population Upsilon (MAP per galaxy)" + ("   *** MUTATE: n=1-truth mock in place of data ***" if MUT else ""))
P("kappa = 1/2 fitted; footings never pooled; cold-energy mass required; not theory closed.")
P(f"a0 canonical {A0['canonical']:.4e}, alt {A0['alt']:.4e} m/s^2; prior log10 U ~ N(log10 0.50, {SIG_U}); s0 = {S0} dex; bulge = 1.4 U")

# ------------------------------------------------------------------------------------------------ data
GAL = C.load_sparc(); RES = {"lane": "AG4b", "mutate": MUT, "criteria": "FROZEN_CRITERIA.md", "footings": {}}
D_ = []
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
    cg = math.sqrt((meta["eD"] / meta["D"] / LN10) ** 2 + (2.0 / math.tan(max(math.radians(meta["Inc"]), 0.05)) * math.radians(meta["eInc"]) / LN10) ** 2) if meta else 0.0
    D_.append(dict(name=g["name"], go=go[m], gas=gas, star=star, sv=sv, cg=cg, Q=meta.get("Q", 3)))
NGAL = len(D_)
P(f"SPARC: {len(GAL)} rotmod files, {NGAL} galaxies with >= 5 usable points, {sum(len(d['go']) for d in D_)} points")


def gbar(d, U):                                                        # (npts, nU)
    return d["gas"][:, None] + d["star"][:, None] * np.atleast_1d(U)[None, :]


def fit_all(data, nu, a0, s0=S0, sig_u=SIG_U, extra=False, keep=None):
    """per-galaxy MAP Upsilon; returns rms (velocity space, dex), chi2_min, MAP log U, and (if extra) transition-regime rms."""
    rms, chi, lus, rt = [], [], [], []
    for k, d in enumerate(data):
        if keep is not None and not keep[k]:
            continue
        gb = gbar(d, UG); r = np.log10(d["go"])[:, None] - np.log10(nu(gb / a0) * gb)
        s2 = d["sv"][:, None] ** 2 + s0 ** 2 + (d["cg"] ** 2 if extra == "V2" else 0.0)
        c2 = (r ** 2 / s2).sum(0) + ((LU - LU0) / sig_u) ** 2
        i = int(np.argmin(c2)); ri = r[:, i]
        rms.append(math.sqrt(np.mean((ri / 2) ** 2))); chi.append(float(c2[i])); lus.append(float(LU[i]))
        y = gb[:, i] / a0; t = (y >= 0.3) & (y <= 3.0)
        rt.append(math.sqrt(np.mean((ri[t] / 2) ** 2)) if t.sum() >= 3 else np.nan)
    return np.array(rms), np.array(chi), np.array(lus), np.array(rt)


RNG_BOOT = 20261020
def paired_z(d1, d2):
    d = d2 - d1; d = d[np.isfinite(d)]; n = len(d)
    rng = np.random.default_rng(RNG_BOOT); idx = rng.integers(0, n, (10000, n))
    med = float(np.median(d)); sd = float(np.std(np.median(d[idx], axis=1)))
    return med, sd, (-med / sd if sd > 0 else 0.0), n


def compare(data, a0, **kw):
    r1, c1, l1, t1 = fit_all(data, NU1, a0, **kw); r2, c2, l2, t2 = fit_all(data, NU2, a0, **kw)
    D, sD, z, n = paired_z(r1, r2)
    dc = c2 - c1; zc = float(-dc.sum() / (np.std(dc) * math.sqrt(len(dc)))) if np.std(dc) > 0 else 0.0
    Dt, sDt, zt, nt = paired_z(t1, t2)
    return dict(D=D, sD=sD, z=z, n=n, rms1_med=float(np.median(r1)), rms2_med=float(np.median(r2)), sum_dchi2=float(dc.sum()), z_chi2=zc,
                U1_med=float(10 ** np.median(l1)), U2_med=float(10 ** np.median(l2)),
                f1_edge=float(np.mean(np.abs(l1 - LU0) >= 3 * kw.get("sig_u", SIG_U))), f2_edge=float(np.mean(np.abs(l2 - LU0) >= 3 * kw.get("sig_u", SIG_U))),
                D_trans=Dt, z_trans=zt, n_trans=nt)


def reading(z):
    return "n=2 PREFERRED" if z >= 3 else "LEAN n=2" if z >= 2 else "NOT SIGNIFICANT" if z > -2 else "FLIPS (n=1 preferred)"


def mock(truth_nu, a0, seed):
    rng = np.random.default_rng(seed); out = []
    for d in D_:
        lu = float(np.clip(LU0 + SIG_U * rng.standard_normal(), LU[0], LU[-1])); gb = gbar(d, 10 ** lu)[:, 0]
        noise = 0.05 * rng.standard_normal() + np.sqrt(d["sv"] ** 2 + 0.05 ** 2) * rng.standard_normal(len(gb))
        out.append(dict(d, go=truth_nu(gb / a0) * gb * 10 ** noise))
    return out


# ------------------------------------------------------------------------------------------------ controls
P("\nControls")
y = np.logspace(-6, 4, 401)
g1 = NU1(y) * y; g2 = NU2(y) * y
check("K2 nu1(1e-4) = 100.50125, nu2(1e-4) = 100.00500", abs(NU1(np.array(1e-4)) - 100.50125) < 1e-5 and abs(NU2(np.array(1e-4)) - 100.005) < 1e-5,
      f"{float(NU1(np.array(1e-4))):.5f} / {float(NU2(np.array(1e-4))):.5f}")
check("K2 algebraic forms to 1e-12 (n=1: y = g^2/(g+1); n=2: g^2 - y^2 = y)",
      max(np.max(np.abs(g1 ** 2 / (g1 + 1) - y) / y), np.max(np.abs(g2 ** 2 - y ** 2 - y) / (y + y ** 2))) < 1e-12)
check("K3 deep limits agree at y = 1e-6", abs(float(NU1(np.array(1e-6)) / NU2(np.array(1e-6))) - 1) <= 1e-3)
# K1: CFG695's own global-Upsilon scan (its code path) on the same loader
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
Rm = np.concatenate([q["R"] for q in GAL]) * KPC_S; Vo = np.concatenate([q["Vobs"] for q in GAL]); eV = np.concatenate([q["eV"] for q in GAL])
Vg = np.concatenate([q["Vgas"] for q in GAL]); Vd = np.concatenate([q["Vdisk"] for q in GAL]); Vb = np.concatenate([q["Vbul"] for q in GAL])
VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
GB = VB2 * 1e6 / Rm[:, None]; GO = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GB)
OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (Vo > 0)[:, None]
WW = np.where(OK, (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)[:, None], 0.0)
def scan(nuf, a0v):
    with np.errstate(all="ignore"):
        gb = np.where(OK, GB, 1.0); r_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, nuf(gb / a0v) * gb, 1.0))
    mse = (WW * r_ ** 2).sum(0) / WW.sum(0); i = int(np.argmin(mse)); return math.sqrt(mse[i]), float(UPS[i])
c695 = json.load(open(os.path.join(LANES, "CFG695_saturating_vacuum", "cfg695_results.json")))["numbers"]["S2"]
k1 = {f: scan(NU1, A0[f]) for f in C.FOOTS}
check("K1 CFG695 n=1 global-Upsilon scan reproduced (1e-5)", all(abs(k1[f][0] - c695[f]["rms"]) <= 1e-5 and k1[f][1] == c695[f]["U"] for f in C.FOOTS),
      "; ".join(f"{f} {k1[f][0]:.5f}@{k1[f][1]:.2f}" for f in C.FOOTS))
k1n2 = {f: scan(NU2, A0[f]) for f in C.FOOTS}
P("  (reported) n=2 on the same global scan: " + "; ".join(f"{f} {k1n2[f][0]:.5f}@{k1n2[f][1]:.2f}" for f in C.FOOTS))
RES["controls"] = dict(K1_n1=k1, K1_n2_reported=k1n2)

# ------------------------------------------------------------------------------------------------ per footing
for f in C.FOOTS:
    a0 = A0[f]; P(f"\n=== footing: {f} (a0 = {a0:.4e}) ===")
    data = mock(NU1, a0, 1) if MUT else D_
    prim = compare(data, a0)
    P(f"  PRIMARY paired rms: median d (n2 - n1) = {prim['D']:+.4f} dex, sigma {prim['sD']:.4f}, z = {prim['z']:+.2f} (n = {prim['n']}); "
      f"median rms n1 {prim['rms1_med']:.4f} / n2 {prim['rms2_med']:.4f}")
    # power from injected mocks (always on the real error/baryon structure)
    zs1 = [compare(mock(NU1, a0, s), a0)["z"] for s in range(1, 21)]
    zs2 = [compare(mock(NU2, a0, s), a0)["z"] for s in range(21, 41)]
    p1 = float(np.mean(np.array(zs1) <= -2)); p2 = float(np.mean(np.array(zs2) >= 2))
    diag = p1 >= 0.8 and p2 >= 0.8
    P(f"  POWER: n=1-truth mocks z <= -2 in {p1:.0%} (median z {np.median(zs1):+.2f}); n=2-truth mocks z >= +2 in {p2:.0%} "
      f"(median z {np.median(zs2):+.2f}) -> {'DIAGNOSTIC' if diag else 'NOT DIAGNOSTIC'}")
    rd = reading(prim["z"]) if diag else "NOT DIAGNOSTIC"
    surv = (not diag) or prim["z"] > -2
    P(f"  READING ({f}): {rd}" + ("" if diag else f"   (real-data z {prim['z']:+.2f} reported, no verdict)"))
    P(f"  S1 sum dchi2_min (n2 - n1) = {prim['sum_dchi2']:+.1f}, z {prim['z_chi2']:+.2f};  S2 MAP Upsilon median n1 {prim['U1_med']:.3f} / n2 {prim['U2_med']:.3f}, "
      f">=3 sigma from prior n1 {prim['f1_edge']:.1%} / n2 {prim['f2_edge']:.1%};  S4 transition-regime d {prim['D_trans']:+.4f}, z {prim['z_trans']:+.2f} (n {prim['n_trans']})")
    # S3 best global a0 per law at per-galaxy MAP Upsilon
    lg = np.linspace(-10.4, -9.6, 81); s3 = {}
    for kn, nu in LAWS.items():
        tot = [fit_all(data, nu, 10 ** l)[1].sum() for l in lg]; i = int(np.argmin(tot))
        s3[kn] = dict(a0=float(10 ** lg[i]), kappa_canonical_units=float(0.5 * 10 ** lg[i] / A0["canonical"]), at_edge=bool(i in (0, len(lg) - 1)))
    P("  S3 best global a0 (per-galaxy MAP Upsilon): " + "; ".join(f"{k} {v['a0']:.3e} (kappa {v['kappa_canonical_units']:.3f}{', grid edge' if v['at_edge'] else ''})" for k, v in s3.items()))
    var = {}
    for vn, kw in (("V1 sigma_U 0.15", dict(sig_u=0.15)), ("V2 D/inc coherent term", dict(extra="V2")), ("V4 s0 0.03", dict(s0=0.03)), ("V4 s0 0.08", dict(s0=0.08))):
        v = compare(data, a0, **kw); var[vn] = dict(z=v["z"], D=v["D"], reading=reading(v["z"]))
    keep = np.array([d["Q"] <= 2 for d in data]); v = compare([d for d, k in zip(data, keep) if k], a0); var["V3 Q <= 2"] = dict(z=v["z"], D=v["D"], reading=reading(v["z"]))
    P("  VARIANTS: " + "; ".join(f"{k}: z {v['z']:+.2f} ({v['reading']})" for k, v in var.items()))
    RES["footings"][f] = dict(primary=prim, power=dict(p_n1=p1, p_n2=p2, z_n1=zs1, z_n2=zs2, diagnostic=diag), reading=rd,
                              n2_survives_AG4b=bool(surv), S3=s3, variants=var)

surv_all = all(RES["footings"][f]["n2_survives_AG4b"] for f in C.FOOTS)
RES["n2_survives_AG4b"] = surv_all
P(f"\nAG4b: " + "; ".join(f"{f} {RES['footings'][f]['reading']}" for f in C.FOOTS) + f".  n=2 survives AG4b: {surv_all}")
if MUT:
    bites = all(RES["footings"][f]["primary"]["z"] <= -2 for f in C.FOOTS)
    P(f"MUTATE (n=1-truth mock as data): FLIPS on both footings -> {'control BITES (exit 1, as designed)' if bites else 'control DID NOT BITE (recorded)'}")
P(f"controls failed: {FAILS or 'none'}")
json.dump(RES, open(os.path.join(HERE, f"ag4b_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(1 if (MUT and all(RES["footings"][f]["primary"]["z"] <= -2 for f in C.FOOTS)) or FAILS else 0)
