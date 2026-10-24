#!/usr/bin/env python3
"""X25_dwarf_pericentre_tides: does the hosted-dwarf extra over B_iso follow tidal stress AT PERICENTRE?

Frozen criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (d4827bece5). Reads, read-only:
X1's per-system CSV (E, r12, g_iso, x_e), Z2's per-system CSV (PM-based pericentres/apocentres in S1's MW field),
LVD distance_gc (check K6 only). One process, one thread, minutes.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x25_dwarf_pericentre_tides.py               -> .out, _results.json
    X25_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x25_dwarf_pericentre_tides.py  -> peri/apo swapped, K6 must fail
"""
import csv, json, math, os, resource, sys, time
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.stats import kendalltau, norm, rankdata
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

T0 = time.time()
MUTATE = os.environ.get("X25_MUTATE", "") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
TAG = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# X20's constants (step 0 and r12 / g_iso, kept identical so step 0 is exact)
G, PC, KPC, MSUN = 6.674e-11, 3.0857e16, 3.0857e19, 1.989e30
# X1 / Z2 / S1 host-field constants (the record's MW model)
G1, MSUN1, PC1 = 6.67430e-11, 1.989e30, 3.0856775814913673e16
KPC1 = 1e3 * PC1
A_H = 3.0 * KPC1
MHOST = {"MW": 6.0e10, "M31": 1.0e11, "field": 6.0e10}
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ("canonical", "alt")
HCLS = ("MW ultra-faint", "bright M31", "M31 others")
TAU_STAR, TAU_REP = 0.1, 0.03
NPERM, NBOOT, SEED = 20000, 10000, 20261024
P3S = 1.35e-3 / 2          # 3 sigma one-sided, Bonferroni over two proxies (frozen)
T_CLOCK = 10.0 * 3.15576e16  # 10 Gyr in s
RA_CAP = 4999.0             # Z2's cap (kpc): unbound / first approach
ECOL, SCOL = "Delta[iso AQUAL L*0]", "sdMC[iso AQUAL L*0]"
STEP0 = {"canonical": dict(med_tau=0.012146528924996767, rho=0.0026441036488630354, p=0.11269436528173592,
                           N=54, med=0.4804948186291816, sd=0.08276539816933023, Z=5.805503619352308, label="EXTRA"),
         "alt": dict(med_tau=0.012059279336816076, rho=0.012321523003701745, p=0.10329483525823709,
                     N=54, med=0.44510104586666516, sd=0.08205433574967709, Z=5.424467114383005, label="EXTRA")}

def fl(x):
    try:
        v = float(x); return v if math.isfinite(v) else None
    except Exception:
        return None

# ------------------------------------------------------------------ data
X1 = list(csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "X1_hosted_recount", "x1_per_system.csv"))))
Z2 = {(r["footing"], r["name"]): r for r in
      csv.DictReader(open(os.path.join(REPO, "rebuild_2026_10_22", "Z2_satellite_systematics", "z2_per_system.csv")))}
DGC = {r["name"]: fl(r.get("distance_gc")) for r in
       csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", "lvd_dwarf_mw.csv")))}

def rows(foot):
    out = []
    for r in X1:
        if r["footing"] != foot or r["cls"] not in HCLS:
            continue
        ms = 10 ** float(r["logMstar"]); rh = float(r["rh_pc"]) * PC; r12 = 4.0 / 3.0 * rh
        gN = G * (ms / 2) * MSUN / r12 ** 2
        dN, di = float(r["Delta[Newton]"]), float(r["Delta[iso AQUAL L*0]"])
        giso = gN * 10 ** (dN - di)
        q = dict(name=r["name"], host=r["host"], cls=r["cls"], E=float(r[ECOL]), s=float(r[SCOL]), giso=giso, r12=r12,
                 d=float(r["d_host_kpc"]) * KPC, dk=float(r["d_host_kpc"]), xe=float(r["x_e_mid"]),
                 logms=float(r["logMstar"]), logrh=math.log10(float(r["rh_pc"])))
        z = Z2.get((foot, r["name"]))
        if z is not None and fl(z.get("r_peri_kpc")) is not None:
            rp, ra = float(z["r_peri_kpc"]), float(z["r_apo_kpc"])
            if MUTATE:
                rp, ra = ra, rp
            q.update(rp=rp, ra=ra, rp16=fl(z.get("r_peri_p16")), rp84=fl(z.get("r_peri_p84")))
        out.append(q)
    return out

# ------------------------------------------------------------------ X20 machinery (verbatim logic, for step 0)
def tau_of(R, a0, xe, d, fac=2.0):
    return fac * xe * a0 * np.array([q["r12"] for q in R]) / d / np.array([q["giso"] for q in R])
def rankd(a):
    return np.argsort(np.argsort(a, axis=-1), axis=-1).astype(float)
def spearman(x, y):
    rx, ry = rankd(x), rankd(y)
    rx = rx - rx.mean(axis=-1, keepdims=True); ry = ry - ry.mean(axis=-1, keepdims=True)
    return (rx * ry).sum(axis=-1) / np.sqrt((rx ** 2).sum(axis=-1) * (ry ** 2).sum(axis=-1))
def perm_test_x20(R, E, a0, rng, nperm=NPERM):
    xe = np.array([q["xe"] for q in R]); d = np.array([q["d"] for q in R])
    lt = np.log10(tau_of(R, a0, xe, d)); rho = float(spearman(lt, E))
    host = np.array([q["host"] for q in R])
    idx = np.tile(np.arange(len(R)), (nperm, 1))
    for h in np.unique(host):
        m = np.where(host == h)[0]
        idx[:, m] = m[np.argsort(rng.random((nperm, len(m))), axis=1)]
    ltp = np.log10(tau_of(R, a0, xe[idx], d[idx]))
    rp = spearman(ltp, np.broadcast_to(E, ltp.shape))
    return rho, float((np.sum(rp >= rho) + 1) / (nperm + 1))
def boot_median(E, s, rng, n=NBOOT):
    N = len(E)
    if N == 0:
        return float("nan"), float("nan")
    ix = rng.integers(0, N, (n, N))
    draws = E[ix] + s[ix] * rng.standard_normal((n, N))
    return float(np.median(E)), float(np.std(np.median(draws, axis=1)))
def label(z):
    return "EXTRA" if z >= 2 else ("NONE" if z < 1 else "AMBIGUOUS")

# ------------------------------------------------------------------ S1's host field and orbit integrals
def g_host(R_m, Mb, a0):
    R_m = np.asarray(R_m, float)
    gN = G1 * Mb * MSUN1 / (R_m + A_H) ** 2
    return 0.5 * gN * (1 + np.sqrt(1 + 4 * a0 / gN))
class Potential:
    """Phi(r) - Phi(r_ref) from Phi' = g on a dense log grid (S1's field or any g(r))."""
    def __init__(self, gfun, rmin=0.05 * KPC1, rmax=8000 * KPC1, n=200001):
        lr = np.linspace(math.log(rmin), math.log(rmax), n); r = np.exp(lr)
        phi = cumulative_trapezoid(gfun(r) * r, lr, initial=0.0)
        self.cs = CubicSpline(lr, phi)
    def __call__(self, r):
        return self.cs(np.log(np.asarray(r, float)))
def orbit_quants(pot, rp, ra, nth=4000):
    """Pericentre speed V_p and radial period T_r for turning points rp < ra (SI)."""
    dphi = float(pot(ra) - pot(rp))
    vp2 = 2 * dphi / (1 - (rp / ra) ** 2)
    Vp = math.sqrt(vp2); L = rp * Vp; En = 0.5 * vp2 + float(pot(rp))
    th = (np.arange(nth) + 0.5) * math.pi / nth
    r = 0.5 * (ra + rp) - 0.5 * (ra - rp) * np.cos(th)
    vr2 = 2 * (En - pot(r)) - L ** 2 / r ** 2
    vr = np.sqrt(np.maximum(vr2, 1e-300))
    Tr = 2 * np.sum(0.5 * (ra - rp) * np.sin(th) / vr) * math.pi / nth
    return Vp, Tr

# ------------------------------------------------------------------ helpers for the new tests
def boot_spearman(x, E, s, rng, n=NBOOT):
    N = len(E); ix = rng.integers(0, N, (n, N))
    Ed = E[ix] + s[ix] * rng.standard_normal((n, N))
    rx = rankdata(x[ix], axis=1); ry = rankdata(Ed, axis=1)
    rx = rx - rx.mean(1, keepdims=True); ry = ry - ry.mean(1, keepdims=True)
    rr = (rx * ry).sum(1) / np.sqrt((rx ** 2).sum(1) * (ry ** 2).sum(1))
    return float(np.nanstd(rr))
def partial_rank(E, X, Z):
    """Rank partial correlation of E and X at fixed Z (rows = draws allowed)."""
    rE, rX, rZ = (rankdata(np.atleast_2d(v), axis=1) for v in (E, X, Z))
    def resid(a, z):
        zc = z - z.mean(1, keepdims=True); ac = a - a.mean(1, keepdims=True)
        b = (zc * ac).sum(1, keepdims=True) / (zc ** 2).sum(1, keepdims=True)
        return ac - b * zc
    a, b = resid(rE, rZ), resid(rX, rZ)
    out = (a * b).sum(1) / np.sqrt((a ** 2).sum(1) * (b ** 2).sum(1))
    return out if out.size > 1 else float(out[0])

# ------------------------------------------------------------------ run
P(f"X25_dwarf_pericentre_tides  {'MUTATE run (r_peri <-> r_apo swapped)' if MUTATE else 'normal run'}")
P("kappa = 1/2 FITTED; footings canonical 9.3603e-11 / alt 1.1312e-10 never pooled; not theory closed")
P(f"E column: {ECOL} (B_iso). Pericentres: Z2's PM orbits in S1's MW field (static, no LMC).")
RES = dict(frozen="d4827bece5", mutate=MUTATE, footings={}, checks={})
checks = []

# K2: orbit routine vs Kepler (point mass, Newtonian)
Mk = 1e11 * MSUN1
potk = Potential(lambda r: G1 * Mk / r ** 2)
rpk, rak = 30 * KPC1, 150 * KPC1
Vpk, Trk = orbit_quants(potk, rpk, rak)
ak = 0.5 * (rpk + rak)
Vp_ref = math.sqrt(G1 * Mk * (2 / rpk - 1 / ak)); Tr_ref = 2 * math.pi * math.sqrt(ak ** 3 / (G1 * Mk))
k2e = max(abs(Vpk / Vp_ref - 1), abs(Trk / Tr_ref - 1))
P(f"K2 orbit routine vs Kepler: V_p rel {abs(Vpk / Vp_ref - 1):.2e}, T_r rel {abs(Trk / Tr_ref - 1):.2e}: {'PASS' if k2e <= 1e-3 else 'FAIL'}")
checks.append(("K2", k2e <= 1e-3))

stop = False
for f in FOOTS:
    a0 = A0[f]; FR = RES["footings"][f] = {}
    R = rows(f); E = np.array([q["E"] for q in R]); S = np.array([q["s"] for q in R])
    xe = np.array([q["xe"] for q in R]); d = np.array([q["d"] for q in R])
    P(f"\n=== [{f}] set H: {len(R)} systems")

    # ---------------- Step 0 (X20 exact)
    rng = np.random.default_rng(SEED)
    tau = tau_of(R, a0, xe, d)
    for q, t in zip(R, tau):
        q["tau_now"] = float(t)
    rho0, p0 = perm_test_x20(R, E, a0, rng)
    m = tau <= TAU_STAR
    med0, sd0 = boot_median(E[m], S[m], rng)
    z0 = med0 / sd0
    ref = STEP0[f]
    got = dict(med_tau=float(np.median(tau)), rho=rho0, p=p0, N=int(m.sum()), med=med0, sd=sd0, Z=z0, label=label(z0))
    ok0 = all(abs(got[k] - ref[k]) <= 1e-6 for k in ("med_tau", "rho", "p", "med", "sd", "Z")) and got["N"] == ref["N"] and got["label"] == ref["label"]
    P(f"  STEP 0 (X20 reproduction): median tau {got['med_tau']:.6f} (X20 {ref['med_tau']:.6f}); rho {rho0:+.6f} ({ref['rho']:+.6f}); "
      f"p {p0:.6f} ({ref['p']:.6f}); tau<=0.1 N {got['N']} median {med0:+.6f} ({ref['med']:+.6f}) sd {sd0:.6f} ({ref['sd']:.6f}) "
      f"Z {z0:.4f} ({ref['Z']:.4f}) {got['label']}: {'PASS' if ok0 else 'FAIL'}")
    FR["step0"] = dict(got=got, ref=ref, ok=ok0)
    checks.append((f"K0[{f}]", ok0))
    if not ok0:
        stop = True
        P("  STOP RULE: step 0 failed; no pericentre number is computed.")
        continue

    # ---------------- K1: S1's field reproduces x_e_mid
    Mb = MHOST["MW"]
    k1 = max(abs(float(g_host(q["dk"] * KPC1, MHOST[q["host"]], a0)) / a0 / q["xe"] - 1) for q in R)
    P(f"  K1 S1 host field reproduces X1 x_e_mid (all {len(R)} H systems): max rel {k1:.2e}: {'PASS' if k1 <= 1e-6 else 'FAIL'}")
    checks.append((f"K1[{f}]", k1 <= 1e-6))

    # ---------------- set P
    Pset = [q for q in R if "rp" in q]
    noP = [q for q in R if "rp" not in q]
    P(f"  set P (H with a pericentre on disk): N {len(Pset)}  "
      f"({', '.join(f'{c} {sum(q[chr(99)+chr(108)+chr(115)] == c for q in Pset)}/{sum(q[chr(99)+chr(108)+chr(115)] == c for q in R)}' for c in HCLS)})")
    P(f"  no pericentre on disk ({len(noP)}): " + ", ".join(q["name"] for q in noP))
    FR["N_P"] = len(Pset); FR["no_pericentre"] = [q["name"] for q in noP]
    FR["N_P_by_class"] = {c: sum(q["cls"] == c for q in Pset) for c in HCLS}

    # K6 orbit sanity
    bad = [q["name"] for q in Pset if not (q["rp"] <= 1.02 * (DGC.get(q["name"]) or float("inf")) + 0.5 and q["rp"] <= q["ra"])]
    nodgc = [q["name"] for q in Pset if DGC.get(q["name"]) is None]
    k6 = not bad and not nodgc
    P(f"  K6 orbit sanity r_p <= 1.02 d_gc + 0.5 kpc and r_p <= r_a: violations {len(bad)} {bad[:8]} (no d_gc: {nodgc}): {'PASS' if k6 else 'FAIL'}")
    checks.append((f"K6[{f}]", k6))

    # ---------------- pericentre stress and shock proxy
    pot = Potential(lambda r: g_host(r, Mb, a0))
    for q in Pset:
        rp = q["rp"] * KPC1; ra = min(q["ra"], RA_CAP + 1.0) * KPC1
        ge = float(g_host(rp, Mb, a0))
        q["A"] = 2 * ge / rp                                        # orbit factor of tau (s^-2)
        q["tau_peri"] = q["A"] * q["r12"] / q["giso"]
        q["tau_peri3"] = 1.5 * q["tau_peri"]
        dg = abs(float(g_host(rp * 1.001, Mb, a0) - g_host(rp * 0.999, Mb, a0))) / (0.002 * rp)
        q["tau_grad"] = dg * q["r12"] / q["giso"]
        q["tau_max"] = max(q["tau_peri"], q["tau_now"])
        if q["rp"] < q["ra"]:
            Vp, Tr = orbit_quants(pot, rp, ra)
        else:   # MUTATE only (r_p > r_a): read the orbit with the turning points ordered
            Vp, Tr = orbit_quants(pot, ra, rp); Vp = Vp * ra / rp
        q["Vp"] = Vp; q["tp"] = rp / Vp; q["Tr_Gyr"] = Tr / 3.15576e16
        q["unbound"] = q["ra"] >= RA_CAP
        q["Np"] = 1.0 if q["unbound"] else max(1.0, T_CLOCK / Tr)
        q["sig_iso"] = math.sqrt(q["giso"] * q["r12"] / 3)
        dv = q["A"] * q["r12"] * q["tp"]
        x = q["sig_iso"] / q["r12"] * q["tp"]
        q["S1"] = (dv / q["sig_iso"]) ** 2 * (1 + x * x) ** -1.5
        q["H"] = q["S1"] * q["Np"]
        if q["rp16"] is not None and not MUTATE:
            r16 = q["rp16"] * KPC1
            q["tau_p16"] = 2 * float(g_host(r16, Mb, a0)) / r16 * q["r12"] / q["giso"]
    EP = np.array([q["E"] for q in Pset]); SP = np.array([q["s"] for q in Pset])
    tp_ = np.array([q["tau_peri"] for q in Pset]); Hp = np.array([q["H"] for q in Pset])
    tn_ = np.array([q["tau_now"] for q in Pset])
    P(f"  tau on P: current-distance (X20) median {np.median(tn_):.4g}; pericentre median {np.median(tp_):.4g} "
      f"(min {tp_.min():.3g}, max {tp_.max():.3g}); median ratio tau_peri/tau_now {np.median(tp_ / tn_):.3g}")
    P(f"  heating proxy H: median {np.median(Hp):.3g} (min {Hp.min():.3g}, max {Hp.max():.3g}); "
      f"N_p median {np.median([q['Np'] for q in Pset]):.2f}; unbound/capped {sum(q['unbound'] for q in Pset)}")
    FR["tau_summary"] = dict(median_tau_now_P=float(np.median(tn_)), median_tau_peri=float(np.median(tp_)),
                             min_tau_peri=float(tp_.min()), max_tau_peri=float(tp_.max()),
                             median_ratio=float(np.median(tp_ / tn_)), median_H=float(np.median(Hp)),
                             N_tau_peri_le_0p1=int((tp_ <= 0.1).sum()), N_tau_peri_le_0p03=int((tp_ <= 0.03).sum()))

    # ---------------- C1 / C2 with same-host permutation of orbits
    rng = np.random.default_rng(SEED)
    host = np.array([q["host"] for q in Pset])
    Aarr = np.array([q["A"] for q in Pset]); tparr = np.array([q["tp"] for q in Pset]); Nparr = np.array([q["Np"] for q in Pset])
    r12 = np.array([q["r12"] for q in Pset]); giso = np.array([q["giso"] for q in Pset]); sig = np.array([q["sig_iso"] for q in Pset])
    def stress(idx):
        A, tpp, Np = Aarr[idx], tparr[idx], Nparr[idx]
        t = A * r12 / giso
        dv = A * r12 * tpp; x = sig / r12 * tpp
        H = (dv / sig) ** 2 * (1 + x * x) ** -1.5 * Np
        return t, H
    def perm_idx(rng, n):
        idx = np.tile(np.arange(len(Pset)), (n, 1))
        for h in np.unique(host):
            mm = np.where(host == h)[0]
            idx[:, mm] = mm[np.argsort(rng.random((n, len(mm))), axis=1)]
        return idx
    def corr_test(Ev, rng, nperm=NPERM):
        t0, H0 = stress(np.arange(len(Pset)))
        r1 = float(spearman(np.log10(t0), Ev)); r2 = float(spearman(np.log10(H0), Ev))
        idx = perm_idx(rng, nperm); tP, HP = stress(idx)
        rp1 = spearman(np.log10(tP), np.broadcast_to(Ev, tP.shape)); rp2 = spearman(np.log10(HP), np.broadcast_to(Ev, HP.shape))
        return r1, float((np.sum(rp1 >= r1) + 1) / (nperm + 1)), r2, float((np.sum(rp2 >= r2) + 1) / (nperm + 1))
    r1, p1, r2, p2 = corr_test(EP, rng)
    sd1 = boot_spearman(np.log10(tp_), EP, SP, rng); sd2 = boot_spearman(np.log10(Hp), EP, SP, rng)
    kt1 = kendalltau(np.log10(tp_), EP); kt2 = kendalltau(np.log10(Hp), EP)
    zp1, zp2 = float(norm.isf(p1)), float(norm.isf(p2))
    P(f"  C1 Spearman(E, log tau_peri) {r1:+.3f} +- {sd1:.3f} (boot); Kendall {kt1.statistic:+.3f}; "
      f"same-host permutation p {p1:.4g} (Z_p {zp1:+.2f})")
    P(f"  C2 Spearman(E, log H)        {r2:+.3f} +- {sd2:.3f} (boot); Kendall {kt2.statistic:+.3f}; "
      f"same-host permutation p {p2:.4g} (Z_p {zp2:+.2f})")
    FR["C1"] = dict(rho=r1, sd_boot=sd1, kendall=float(kt1.statistic), kendall_p_scipy=float(kt1.pvalue), p_perm=p1, Z_p=zp1)
    FR["C2"] = dict(rho=r2, sd_boot=sd2, kendall=float(kt2.statistic), kendall_p_scipy=float(kt2.pvalue), p_perm=p2, Z_p=zp2)

    # ---------------- W: weak-stress subsets
    FR["W"] = {}
    for ts in (TAU_STAR, TAU_REP):
        mm = tp_ <= ts
        med, sd = boot_median(EP[mm], SP[mm], rng)
        z = med / sd if mm.sum() and sd > 0 else float("nan")
        lab = label(z) if mm.sum() else "N/A"
        above = float(np.median(EP[~mm])) if (~mm).sum() else float("nan")
        byc = {}
        for c in HCLS:
            mc = mm & np.array([q["cls"] == c for q in Pset])
            if mc.sum():
                a_, b_ = boot_median(EP[mc], SP[mc], rng)
                byc[c] = dict(N=int(mc.sum()), median=a_, sd=b_, Z=a_ / b_ if b_ > 0 else float("nan"))
        P(f"  W tau_peri <= {ts:<4}: N {int(mm.sum()):2d}  median E {med:+.3f} +- {sd:.3f}  Z {z:+.2f}  {lab:9s}  "
          f"(tau_peri > {ts}: N {int((~mm).sum())}, median {above:+.3f})  [{'PRIMARY' if ts == TAU_STAR else 'decision-side'}]")
        FR["W"][str(ts)] = dict(N=int(mm.sum()), median=med, sd=sd, Z=z, label=lab, N_above=int((~mm).sum()),
                                median_above=above, by_class=byc)
    medall, sdall = boot_median(EP, SP, rng)
    P(f"  all of P: median E {medall:+.3f} +- {sdall:.3f} (N {len(EP)})")
    FR["all_P"] = dict(median=medall, sd=sdall, N=len(EP))

    # fraction f_tid (paired bootstrap)
    mw = tp_ <= TAU_STAR
    ix = rng.integers(0, len(EP), (NBOOT, len(EP)))
    Ed = EP[ix] + SP[ix] * rng.standard_normal(ix.shape); wd = mw[ix]
    fr = []
    for k in range(NBOOT):
        if wd[k].sum() and np.median(Ed[k]) != 0:
            fr.append(1 - np.median(Ed[k][wd[k]]) / np.median(Ed[k]))
    fr = np.array(fr)
    ftid = 1 - float(np.median(EP[mw])) / float(np.median(EP)) if mw.sum() else float("nan")
    f16, f84 = (float(np.percentile(fr, 16)), float(np.percentile(fr, 84))) if fr.size else (float("nan"),) * 2
    P(f"  f_tid = 1 - E(tau_peri<=0.1)/E(P) = {ftid:+.3f}  68% [{f16:+.3f}, {f84:+.3f}]")
    FR["f_tid"] = dict(value=ftid, p16=f16, p84=f84)

    # ---------------- PC: partial correlations
    lms = np.array([q["logms"] for q in Pset]); lrh = np.array([q["logrh"] for q in Pset]); lt = np.log10(tp_)
    FR["PC"] = {}
    for nm, X in (("logMstar", lms), ("log_rhalf", lrh)):
        raw = float(spearman(X, EP)); pr = float(partial_rank(EP, X, lt))
        ixb = rng.integers(0, len(EP), (NBOOT, len(EP)))
        Eb = EP[ixb] + SP[ixb] * rng.standard_normal(ixb.shape)
        prb = partial_rank(Eb, X[ixb], lt[ixb]); sdp = float(np.nanstd(prb))
        Eperm = np.array([EP[rng.permutation(len(EP))] for _ in range(NPERM)])
        pp = partial_rank(Eperm, np.broadcast_to(X, Eperm.shape), np.broadcast_to(lt, Eperm.shape))
        p2s = float((np.sum(np.abs(pp) >= abs(pr)) + 1) / (NPERM + 1))
        if np.sign(pr) != np.sign(raw) or abs(pr) < 0.1:
            lab = "GONE"
        elif p2s < 0.05:
            lab = "SURVIVES"
        else:
            lab = "WEAKENED"
        P(f"  PC E vs {nm:9s}: raw Spearman {raw:+.3f}; partial at fixed log tau_peri {pr:+.3f} +- {sdp:.3f}; "
          f"two-sided permutation p {p2s:.4g} -> {lab}")
        FR["PC"][nm] = dict(raw=raw, partial=pr, sd_boot=sdp, p_two_sided=p2s, label=lab)
    prH = float(partial_rank(EP, np.log10(Hp), lms))
    P(f"  PC reported: partial Spearman(E, log H | log M*) {prH:+.3f}; raw Spearman(log tau_peri, log M*) {float(spearman(lt, lms)):+.3f}")
    FR["PC"]["E_H_given_logMstar"] = prH
    FR["PC"]["rho_tau_logMstar"] = float(spearman(lt, lms))

    # ---------------- reported sensitivities
    rep = {}
    for nm, key in (("tau_grad", "tau_grad"), ("tau_max", "tau_max"), ("tau_p16", "tau_p16")):
        vals = [q.get(key) for q in Pset]
        if any(v is None for v in vals):
            continue
        v = np.array(vals); mm = v <= TAU_STAR
        med, sd = boot_median(EP[mm], SP[mm], rng)
        rep[nm] = dict(rho=float(spearman(np.log10(v), EP)), N_le_0p1=int(mm.sum()), median_E_le_0p1=med, sd=sd,
                       Z=med / sd if sd > 0 else float("nan"), median_tau=float(np.median(v)))
        P(f"  reported {nm:8s}: median {np.median(v):.3g}; Spearman(E, log) {rep[nm]['rho']:+.3f}; "
          f"<= 0.1: N {int(mm.sum())}, median E {med:+.3f} +- {sd:.3f} (Z {rep[nm]['Z']:+.2f})")
    S1v = np.array([q["S1"] for q in Pset])
    rep["S1_rho"] = float(spearman(np.log10(S1v), EP))
    P(f"  reported S1 (per passage) Spearman(E, log S1) {rep['S1_rho']:+.3f}; factor-3 tau has the same ranks as tau_peri")
    # M31 / no-pericentre systems: r_p/d needed for tau = 0.1 (in their own host's field)
    need = {}
    for q in noP:
        Mh = MHOST[q["host"]]
        fn = lambda r: 2 * float(g_host(r, Mh, a0)) / r * q["r12"] / q["giso"] - 0.1
        dd = q["dk"] * KPC1
        need[q["name"]] = 1.0 if fn(dd) >= 0 else brentq(fn, 0.01 * KPC1, dd) / dd
    if need:
        nv = np.array(list(need.values()))
        P(f"  reported no-pericentre systems: r_p/d needed for tau = 0.1: median {np.median(nv):.3f} "
          f"(16% {np.percentile(nv, 16):.3f}, 84% {np.percentile(nv, 84):.3f}); fraction needing r_p/d < 0.3: {np.mean(nv < 0.3):.2f}")
        rep["no_peri_rp_over_d_needed"] = dict(median=float(np.median(nv)), p16=float(np.percentile(nv, 16)),
                                               p84=float(np.percentile(nv, 84)), frac_below_0p3=float(np.mean(nv < 0.3)), per_system=need)
    FR["reported"] = rep

    # ---------------- verdict
    w1 = FR["W"][str(TAU_STAR)]; w3 = FR["W"][str(TAU_REP)]
    if len(Pset) < 15 or w1["N"] < 8:
        v = "UNDECIDED"
    elif w1["label"] == "NONE" and min(p1, p2) <= P3S and not (w3["N"] >= 8 and w3["label"] == "EXTRA"):
        v = "TIDES EXPLAIN IT"
    elif w1["label"] == "EXTRA" and p1 >= 0.05 and p2 >= 0.05:
        v = "TIDES RULED OUT AT PERICENTRE"
    else:
        v = "TIDES PARTIAL"
    FR["verdict"] = v
    P(f"  VERDICT [{f}] (set P, N {len(Pset)}): {v}")

    # per-system table
    FR["per_system"] = [dict(name=q["name"], cls=q["cls"], E=q["E"], s=q["s"], r_peri_kpc=q["rp"], r_apo_kpc=q["ra"],
                             tau_now=q["tau_now"], tau_peri=q["tau_peri"], tau_grad=q["tau_grad"], H=q["H"], S1=q["S1"],
                             Np=q["Np"], Vp_kms=q["Vp"] / 1e3) for q in Pset]
    P("  per system (sorted by tau_peri) name r_p tau_now tau_peri H E:")
    for q in sorted(Pset, key=lambda q: q["tau_peri"]):
        P(f"     {q['name']:18s} r_p {q['rp']:7.1f}  tau_now {q['tau_now']:.3g}  tau_peri {q['tau_peri']:.3g}  H {q['H']:.3g}  E {q['E']:+.2f}")

    # ---------------- K3 / K4 controls
    rngc = np.random.default_rng(SEED + 1)
    Esyn = 0.5 * np.log10(tp_) + SP * rngc.standard_normal(len(EP))
    _, pk3, _, _ = corr_test(Esyn, rngc)
    k3 = pk3 < 0.01
    P(f"  K3 positive control (E = 0.5 log tau_peri + noise): C1 p = {pk3:.4g}: {'PASS' if k3 else 'FAIL'}")
    checks.append((f"K3[{f}]", k3))
    ps = []
    for _ in range(200):
        Es = EP[rngc.permutation(len(EP))]
        ps.append(corr_test(Es, rngc, nperm=2000)[1])
    frac = float(np.mean(np.array(ps) > 0.01)); k4 = frac >= 0.9
    P(f"  K4 negative control (E shuffled, 200 x 2000 perms): fraction C1 p > 0.01 = {frac:.3f}: {'PASS' if k4 else 'FAIL'}")
    checks.append((f"K4[{f}]", k4))

if stop:
    RES["verdict"] = "NOT RUN (step 0 failed)"
else:
    V = {f: RES["footings"][f]["verdict"] for f in FOOTS}
    RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else "UNDECIDED (footings disagree)"
P(f"\n=== VERDICT (both footings must agree; scope = set P): {RES['verdict']}")

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
checks.append(("K5", rss < 1.0))
P("\n=== CHECKS")
for k, ok in checks:
    P(f"  [{'PASS' if ok else 'FAIL'}] {k}")
RES["checks"] = {k: bool(ok) for k, ok in checks}
RES["peak_rss_GB"] = rss
npass = sum(ok for _, ok in checks)
P(f"\nchecks {npass}/{len(checks)}; runtime {time.time() - T0:.1f} s; peak RSS {rss:.3f} GB")
open(os.path.join(HERE, f"x25_dwarf_pericentre_tides{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"x25_dwarf_pericentre_tides_results{TAG}.json"), "w"), indent=1, default=float)
sys.exit(0 if npass == len(checks) else 1)
