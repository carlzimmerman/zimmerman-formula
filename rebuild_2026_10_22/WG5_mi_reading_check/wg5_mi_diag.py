#!/usr/bin/env python3
"""WG5 DIAGNOSTIC (no frozen criteria; not a graded lane): the CMB lensing a modified-inertia reading of the law would show.
In pure modified inertia (the framework's original de Sitter-Unruh arm, a0kit) the metric carries no phantom: light sees only the
Newtonian potential of the baryons. Here the existing law-on runs (WG2 R1 a0 flat, WG4 a0 tracking rho_DE) stand in for MI's dynamics
(QUMOND's curl projection is the only difference at the mesh scale), and their stored baryon spectra are turned into the Newtonian
potential, Psi_N,k = -1.5 Omega_b delta_k / (a k^2), with the mode-weighted <1/k^4> of each bin, then projected and graded exactly as WG2. Check: on WG2's law-off runs the same
formula must reproduce the stored potential spectra (they are Newtonian by construction).
Run: python3 wg5_mi_diag.py. kappa = 1/2 FITTED; pure MI is closed by galaxy lensing at 21 sigma (RETRACTIONS.md); not theory closed."""
import os, sys, json, math, glob, copy
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.stats import chi2 as CHI2
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity", "CFG917_cmb_lensing_gate")); import cfg917_lib as LB   # read only
sys.path.insert(0, os.path.join(REB, "WG4_a0_tracks_de_web")); import wg4_pm; PM = wg4_pm.B                         # WG2 engine + WG4 backgrounds, read only
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(s)

# ---------------------------------------------------------------- copied unchanged from WG2's wg2_grade.py (lines 21-83)
H = PM.H; CH = 2997.92458 / H                      # c / H0 in Mpc
ZS = 1090.0
LS = np.arange(8, LB.LMAX + 1); L4 = (LS * (LS + 1.0)) ** 2 / (2 * math.pi)
D = LB.load_pr4()

# ------------------------------------------------------------------ geometry and Limber (WG1's engine, same E(a) as the runs)
def geom(bg):
    E, _ = PM.background(bg)
    z = np.concatenate([np.linspace(0.0, 10.0, 8001), np.geomspace(10.0, ZS, 4001)[1:]])
    f = CH / np.array([E(1 / (1 + zz)) for zz in z])
    chi = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(z))]); chis = float(chi[-1])
    cg = np.concatenate([np.geomspace(1e-3, 100.0, 160), np.linspace(100.0, chis, 700)[1:]])
    w = np.zeros_like(cg); w[1:] += 0.5 * np.diff(cg); w[:-1] += 0.5 * np.diff(cg)
    q = 2.0 * (chis - cg) / (cg * chis)
    return dict(cg=cg, zg=np.interp(cg, chi, z), ker=w * q ** 2 / cg ** 2, chis=chis)
GEO = {bg: geom(bg) for bg in ("B1", "B2", "B1D", "B2D")}   # B1D, B2D as WG4

def snap_tables(run):
    """per snapshot: z, log k (1/Mpc), log Delta^2_Psi on bins up to k_cut = 0.5 k_Ny, and the high-k slope."""
    kny = math.pi * run["N"] / run["L"] * H; kcut = 0.5 * kny; tabs = []
    for s in sorted(run["snaps"], key=lambda s: s["z"]):
        k = np.array(s["k"]) * H; Pp = np.array(s["P_psi"]) / H ** 3
        d2 = k ** 3 * Pp / (2 * math.pi ** 2); m = (k <= kcut) & (d2 > 0)
        lk, ld = np.log(k[m]), np.log(d2[m])
        hi = (k[m] >= kcut / 2)
        slope = float(np.polyfit(lk[hi], ld[hi], 1)[0]) if hi.sum() >= 3 else -4.0
        tabs.append(dict(z=s["z"], lk=lk, ld=ld, slope=slope))
    return tabs, kcut

def logd2(t, lkq, zero_beyond):
    lk, ld = t["lk"], t["ld"]
    out = np.interp(lkq, lk, ld)                                           # flat below the first bin (np.interp clamps)
    hi = lkq > lk[-1]
    out = np.where(hi, ld[-1] + t["slope"] * (lkq - lk[-1]), out)
    return out, (hi if zero_beyond else np.zeros_like(hi)), (lkq >= lk[0]) & (lkq <= lk[-1])

def project(run, zero_beyond=False):
    g = GEO[run["bg"]]; tabs, kcut = snap_tables(run)
    zs = np.array([t["z"] for t in tabs]); lz = np.log1p(zs)
    C = np.zeros(len(LS)); Cin = np.zeros(len(LS))
    for chi, z, kw in zip(g["cg"], g["zg"], g["ker"]):
        k = (LS + 0.5) / chi; lkq = np.log(k)
        if z >= zs[-1]:
            i0 = i1 = len(tabs) - 1; t = 0.0
        else:
            i1 = int(np.searchsorted(zs, z)); i0 = max(i1 - 1, 0); t = 0.0 if i1 == i0 else (math.log1p(z) - lz[i0]) / (lz[i1] - lz[i0])
        a0_, z0_, in0 = logd2(tabs[i0], lkq, zero_beyond); a1_, z1_, in1 = logd2(tabs[i1], lkq, zero_beyond)
        ld = (1 - t) * a0_ + t * a1_
        Pk = 2 * math.pi ** 2 * np.exp(ld) / k ** 3
        Pk = np.where(z0_ | z1_, 0.0, Pk)
        C += kw * Pk; Cin += kw * Pk * (in0 & in1)
    X = np.zeros(LB.LMAX + 1); X[LS] = L4 * C
    Xin = np.zeros(LB.LMAX + 1); Xin[LS] = L4 * Cin
    return X, Xin

def grade_X(X):
    A, sA = LB.pr4_amp(D, X); c2 = LB.pr4_chi2(D, X)
    u = LB.wsum(D["W"], X); b = LB.qform(u, D["Cinv"]); Ap = LB.qform(u, D["Cinv"], D["d"]) / b
    return dict(r=1 / A, A_fit=A, sA=sA, chi2_unscaled=c2, p_unscaled=float(CHI2.sf(c2, D["n"])), r_plain=1 / Ap)

def run_label(r):
    return "FAILS LOW" if r < 0.5 else ("FAILS HIGH" if r > 2 else "WITHIN x2")


# ---------------------------------------------------------------- WG5 diagnostic
_K4 = {}
def kinv4(N):
    """mode-weighted <1/k^4> per bin on the run's own mesh and binning (the stored potential spectra average 1/k^4 over each bin)."""
    if N not in _K4:
        m = PM.Mesh(N); M = m.M; kk = m.kk; wt = np.full(kk.shape, 2.0); wt[..., 0] = 1.0
        if M % 2 == 0: wt[..., -1] = 1.0
        wt[0, 0, 0] = 0.0; kf = 2 * np.pi / PM.L; edges = np.arange(0.5, M // 2 + 1, 1.0) * kf
        ib = np.digitize(kk.ravel(), edges); wv = wt.ravel(); inside = (kk.ravel() <= np.pi / m.dx)   # DEC zeroes modes outside the sphere
        x = np.where(kk.ravel() > 0, kk.ravel(), 1.0) ** -4.0
        nb = np.bincount(ib, weights=wv, minlength=len(edges) + 1); s4 = np.bincount(ib, weights=wv * x * inside, minlength=len(edges) + 1)
        ok = nb[1:len(edges)] > 0; _K4[N] = (s4[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]
    return _K4[N]
def newtonian(run):
    r = copy.deepcopy(run); w4 = kinv4(run["N"])
    for s in r["snaps"]:
        pd = np.array(s["P_delta"])
        s["P_psi"] = ((1.5 * PM.OMB / s["a"]) ** 2 * w4[:len(pd)] * pd * PM.PSI_UNIT ** 2).tolist()
    return r
P("WG5 DIAGNOSTIC: lensing of a pure modified-inertia reading (Newtonian potential of the law-grown baryons), graded as WG2 on Planck PR4 8-400.")
CHK = []
for f in sorted(glob.glob(os.path.join(REB, "WG2_bare_law_web_lensing", "runs", "R0_*.json"))):
    run = json.load(open(f)); X, _ = project(run); Xn, _ = project(newtonian(run))
    q = grade_X(Xn)["r"] / grade_X(X)["r"]; CHK.append(q)
    P(f"  check on law-off run {os.path.basename(f)[:-5]}: r(Newtonian formula) / r(stored) = {q:.5f}")
ok = all(abs(q - 1) < 0.02 for q in CHK); P(f"  check (within 2 %): {'PASS' if ok else 'FAIL'}")
RES = {}
P(""); P("Law-on runs, MI-style lensing (Newtonian potential only) vs the same run with the law's phantom in the metric:")
files = sorted(glob.glob(os.path.join(REB, "WG2_bare_law_web_lensing", "runs", "R1_TIE_B*_As*e-09_N128_s200_zon50_canonical.json"))) + \
        sorted(glob.glob(os.path.join(REB, "WG4_a0_tracks_de_web", "runs", "R1_DE_B*_As*e-09_N128_s200_zon50_canonical.json")))
for f in files:
    run = json.load(open(f)); t = os.path.basename(f)[:-5]
    gm = grade_X(project(run)[0]); gn = grade_X(project(newtonian(run))[0])
    RES[t] = dict(r_with_phantom=gm["r"], r_MI_newtonian_only=gn["r"], label_MI=run_label(gn["r"]))
    P(f"  {t:<48} with phantom r {gm['r']:9.4g} | MI (Newtonian only) r {gn['r']:9.4g} -> {run_label(gn['r'])}")
dev = max(abs(q - 1) for q in CHK); marg = min(max(0.5 / v["r_MI_newtonian_only"], v["r_MI_newtonian_only"] / 2) for v in RES.values())
P(f"  largest check deviation {100 * dev:.1f} % against the smallest label margin x{marg:.1f}: the labels can't move")
P(""); P("Reading: pure MI is already closed by galaxy lensing at 21 sigma (RETRACTIONS.md, STANDING.md line 284). This diagnostic adds its CMB-lensing side.")
P("kappa = 1/2 FITTED; not theory closed; nothing here says the data favour the framework.")
json.dump(dict(lane="WG5_mi_reading_check", kind="DIAGNOSTIC, no frozen criteria", check_pass_2pct=ok, check_ratios=CHK, check_max_dev=dev, smallest_label_margin=marg, runs=RES),
          open(os.path.join(HERE, "wg5_mi_diag_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "wg5_mi_diag.out"), "w").write("\n".join(OUT) + "\n")
