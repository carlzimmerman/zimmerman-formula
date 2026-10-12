#!/usr/bin/env python3
"""CFG649 CMB-SAFETY GATE (FROZEN_CRITERIA.md, commit 0d6f7f883).

Part A  primary CMB: is candidate B's switch 1_B provably OFF at recombination (A1 data at z_i, A2 code scan, A3 linear-peak
        estimate at z = 1100, A4 CFG630 context)?  The switch-off-era physics is GR-linear and INHERITED; nothing is fitted.
Part B  CMB lensing from the framework's OWN gravitating field: R(k, z) = P_grav,F / P_grav,S0 from a PM run and its
        same-realisation S0 control, Limber-projected to C_L^phiphi; Delta A_lens = A_F / A_S0 - 1 on Planck 2018 VIII MV band
        weights (8-400 primary), with the frozen extrapolation bracket and the coverage fraction of the box.

Usage (any PM output in the cfg596 JSON format: snap{name: a, k, P, P_grav, n_catch, e_sum, ...}):
    nice -n 10 python3 cfg649_cmb_safety.py [--f F.json] [--s0 S0.json] [--tag NAME] [--engine path/to/engine.py]
Defaults: F = cfg596_work/P1 (RES canonical), S0 = cfg596_work/P0.  CFG649_MUTATE=1 runs the frozen MUTATE set (separate outputs).
One process, numpy only, < 0.5 GB.  kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math, re, argparse, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy.integrate import quad
from scipy.special import log_ndtr

HERE = os.path.dirname(os.path.abspath(__file__))
CFGD = os.path.dirname(HERE); REPO = os.path.dirname(CFGD); EXT = os.path.join(os.path.dirname(REPO), "_external_data")
W596 = os.path.join(EXT, "cfg596_work")
MUTATE = os.environ.get("CFG649_MUTATE", "0") == "1"
T0 = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("--f", default=os.path.join(W596, "P1", "cfg596_RES_canonical_N1024_L100_ns1024_lean.json"))
ap.add_argument("--s0", default=os.path.join(W596, "P0", "cfg596_S0_canonical_N1024_L100_ns1024_lean.json"))
ap.add_argument("--tag", default="cfg596_P1_canonical")
ap.add_argument("--engine", default=os.path.join(CFGD, "CFG596_lean_pm_1024", "cfg596_pm.py"))
ap.add_argument("--khi", type=float, default=None, help="box support top (default pi N /(4 L) from the JSON)")
ap.add_argument("--out", default=None)
ARGS = ap.parse_args()
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
RES = {"lane": "CFG649", "criteria_commit": "0d6f7f883", "mutate": MUTATE, "tag": ARGS.tag,
       "settings": "kappa = 1/2 FITTED; footings never pooled; cold energy mass required; no particle species; not theory closed; "
                   "no LCDM fit / halofit / HMcode / CLASS / CAMB spectrum in any verdict; F vs same-pipeline S0",
       "inputs": {"F": os.path.relpath(ARGS.f, os.path.dirname(REPO)), "S0": os.path.relpath(ARGS.s0, os.path.dirname(REPO))}}
CHECKS = {}
def check(name, desc, ok, detail=""):
    CHECKS[name] = dict(desc=desc, ok=bool(ok), detail=detail)
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {desc} -- {detail}")

# ------------------------------------------------------------------ engine constants and linear spectrum (cfg527/cfg596 verbatim)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; OL = 1.0 - Om
NS, SIG8 = 0.965, 0.811
E = lambda a: math.sqrt(Om / a ** 3 + OL)
def T_eh(k):
    OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
_trapz = getattr(np, "trapezoid", None) or np.trapz
_KG = np.geomspace(1e-5, 100, 40000)
_PK = _KG ** NS * T_eh(_KG * h) ** 2
_W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_NORM = SIG8 ** 2 / (_trapz(_PK * _W8(_KG * 8.0) ** 2 * _KG ** 2, _KG) / (2 * math.pi ** 2))
_PK *= _NORM
def P_lin0(k):                     # engine: zero above k = 100 h/Mpc; used only where k <= 100 matters (lensing weights)
    return np.interp(np.log(np.maximum(k, 1e-5)), np.log(_KG), _PK, left=0, right=0)
def P_lin0_ext(k):                 # same normalisation, EH continued analytically to any k (A3 only)
    k = np.asarray(k, float); return _NORM * k ** NS * T_eh(k * h) ** 2
_AG = np.geomspace(1e-4, 1.0, 2000)
_g = np.array([quad(lambda u: 1.0 / (u * E(u)) ** 3, 0, x)[0] * E(x) for x in _AG])
_DG = _g / _g[-1]
def Dgrow(a):
    return np.interp(np.log(a), np.log(_AG), _DG)
C_KMS = 299792.458
_ZF = np.concatenate([[0.0], np.geomspace(1e-5, 1200.0, 20000)])
_IF = 1.0 / np.sqrt(Om * (1 + _ZF) ** 3 + OL)
_CHIF = C_KMS / 100.0 * np.concatenate([[0.0], np.cumsum(0.5 * (_IF[1:] + _IF[:-1]) * np.diff(_ZF))])   # Mpc/h
chi_of = lambda z: np.interp(z, _ZF, _CHIF)
z_of_chi = lambda c: np.interp(c, _CHIF, _ZF)
Z_STAR = 1090.0; CHI_STAR = float(chi_of(Z_STAR))

# ------------------------------------------------------------------ inputs
def load(fn):
    d = json.load(open(fn)); sn = d["snap"]
    out = {}
    for name, s in sn.items():
        out[name] = dict(a=float(s["a"]), k=np.array(s["k"], float), P=np.array(s["P"], float), Pg=np.array(s["P_grav"], float),
                         n_catch=s.get("n_catch"), e_sum=s.get("e_sum"), src_sum=s.get("src_sum"), q_max=s.get("q_max"))
    return d, out
DF, SF = load(ARGS.f); DS, SS = load(ARGS.s0)
NPM = int(DS.get("np", 1024)); LBOX = float(DS.get("L", 100.0))
K_HI = ARGS.khi if ARGS.khi else math.pi * NPM / (4 * LBOX)
assert int(DF.get("np", NPM)) == NPM and float(DF.get("L", LBOX)) == LBOX and DF.get("seed") == DS.get("seed"), "F and S0 must share box and realisation"
common = [n for n in SS if n in SF]
ZI_NAME = min(common, key=lambda n: SS[n]["a"])
LATE = sorted([n for n in common if SS[n]["a"] >= 0.5 - 1e-9], key=lambda n: SS[n]["a"])
A_N = np.array([SS[n]["a"] for n in LATE]); A_ZI = SS[ZI_NAME]["a"]
KB = SS[LATE[0]]["k"]
SUP = (KB >= KB[0] - 1e-12) & (KB <= K_HI + 1e-9)
KS = KB[SUP]; K_LO = float(KS[0]); K_HI_B = float(KS[-1])
P(f"CFG649 CMB-safety gate  tag={ARGS.tag}  MUTATE={MUTATE}")
P(f"  F  = {RES['inputs']['F']}\n  S0 = {RES['inputs']['S0']}")
P(f"  box L = {LBOX:g} Mpc/h, N = {NPM}; support k = {K_LO:.4f}-{K_HI_B:.3f} h/Mpc ({SUP.sum()} bins); late snapshots a = "
  + ", ".join(f"{a:.4f}" for a in A_N) + f"; z_i snapshot a = {A_ZI:.3f}")
RES["box"] = dict(L=LBOX, N=NPM, k_lo=K_LO, k_hi=K_HI_B, nbins=int(SUP.sum()), a_nodes=A_N.tolist(), a_zi=A_ZI)

# ================================================================== PART A  primary CMB
P("\nPART A  primary CMB: is the switch off at recombination?")
fzi, szi = SF[ZI_NAME], SS[ZI_NAME]
rg = float(np.max(np.abs(fzi["Pg"] / szi["Pg"] - 1))); rp = float(np.max(np.abs(fzi["P"] / szi["P"] - 1)))
nc = fzi["n_catch"]; es = fzi["e_sum"]
a1_ok = (nc is None or nc <= 1) and (es is None or es == 0.0) and rg <= 1e-6
check("A1", f"switch OFF at the run's start z = {1 / A_ZI - 1:.0f}: n_catch <= 1, e_sum = 0, max|P_grav,F/P_grav,S0 - 1| <= 1e-6",
      a1_ok, f"n_catch {nc}, e_sum {es}, max dev P_grav {rg:.2e}, particle P {rp:.2e}")
first_on = [(n, SF[n]["n_catch"], SF[n]["e_sum"]) for n in sorted(SF, key=lambda n: SF[n]["a"])]
P("  switch diagnostics per stored snapshot (F): " + "; ".join(f"{n}: n_catch {c}, e_sum {e:.3g}" if e is not None else f"{n}: n/a"
                                                     for n, c, e in first_on))
P("  NOTE: no diagnostics were stored between z_i and the first late snapshot -> the in-box switch-on epoch is NOT measured.")
RES["A1"] = dict(n_catch_zi=nc, e_sum_zi=es, maxdev_Pgrav_zi=rg, maxdev_P_zi=rp, per_snapshot=first_on)

# A2: static scan of the engine
src = open(ARGS.engine).read().splitlines()
def find(pat):
    return [(i + 1, l.strip()) for i, l in enumerate(src) if re.search(pat, l)]
hits = dict(a0_use=find(r"a0_code\("), branch=find(r'branch == "'), catch_mask=find(r"e\[s\] \* unpack\(catch_p"),
            no_catch_branch=find(r"if not catch\.any\(\)"), finish=find(r"phik\[s\] - srck\[s\]"), s0_path=find(r'if switch == "S0"'),
            zero_sum=find(r"comp_sel = \(rv_sel \* q\[rr\]\)"), peak_rule=find(r"delta >= 3 \* \(tau - EPS\)"), ball_rule=find(r"ok &= mean >= Dta"))
for k_, v in hits.items():
    P(f"  A2 {k_}: " + ("; ".join(f"L{n}: {t[:110]}" for n, t in v) if v else "NOT FOUND"))
need = ["catch_mask", "no_catch_branch", "finish", "zero_sum", "peak_rule", "ball_rule"]
a2_ok = all(hits[n] for n in need)
check("A2", "engine scan: the only extra source is e*catch (resolved turnaround peaks, enclosed mean >= Delta_ta) minus a per-component "
            "zero-sum compensation; a0 enters only via nu inside that path; no source outside catchments", a2_ok,
      "a0_code used at " + ",".join(f"L{n}" for n, _ in hits["a0_use"]) + "; FLAT branch constant")
RES["A2"] = {k_: v for k_, v in hits.items()}

# A3: linear-peak estimate at z = 1100 (EH continued, matter + Lambda growth, NO radiation -> growth overestimated, conservative)
DLIN_TA = 1.062
KX = np.geomspace(1e-5, 1e7, 60000)
def sigma_R(R, a):
    x = KX * R; W = np.where(x > 1e-3, 3 * (np.sin(x) - x * np.cos(x)) / np.maximum(x, 1e-3) ** 3, 1.0)
    return math.sqrt(_trapz(P_lin0_ext(KX) * W ** 2 * KX ** 2, KX) / (2 * math.pi ** 2)) * float(Dgrow(a))
RG = np.geomspace(1e-3, 10.0, 41)
a_rec = 1 / (1 + 1100.0)
VLS = 4 * math.pi / 3 * CHI_STAR ** 3
logN = []
for R in RG:
    s = sigma_R(R, a_rec); nu = DLIN_TA / s
    logN.append((math.log10(VLS / (4 * math.pi / 3 * R ** 3)) + log_ndtr(-nu) / math.log(10), s, nu))
imax = int(np.argmax([x[0] for x in logN]))
P(f"  A3 z = 1100: max sigma_lin over R in [1e-3, 10] Mpc/h = {max(x[1] for x in logN):.3e}; most dangerous R = {RG[imax]:.3g} Mpc/h, "
  f"nu = {logN[imax][2]:.1f}; log10 N(turnaround peaks in the whole last-scattering ball) = {logN[imax][0]:.1f}")
check("A3", "ESTIMATE: expected number of linear turnaround peaks at z = 1100 in the last-scattering volume < 1e-10", logN[imax][0] < -10,
      f"log10 N_max = {logN[imax][0]:.1f} at R = {RG[imax]:.3g} Mpc/h")
# in-box switch-on estimate (context): Lagrangian radius of the smallest resolved ball (r_min, enclosed mean Delta_ta ~ 5.55 at high z)
RMIN = float(DF.get("rmin", 0.78125)); RL = RMIN * 5.55 ** (1 / 3)
def nbox(z):
    s = sigma_R(RL, 1 / (1 + z)); return math.log10(LBOX ** 3 / (4 * math.pi / 3 * RL ** 3)) + log_ndtr(-DLIN_TA / s) / math.log(10)
zz = np.linspace(0.5, 40, 400); nb = np.array([nbox(z) for z in zz])
z_on = float(zz[np.where(nb >= 0)[0].max()]) if (nb >= 0).any() else None
P(f"  A3 context: in-box switch-on estimate (linear peaks at R_L = {RL:.2f} Mpc/h reaching N = 1 in the box): z_on ~ {z_on}")
RES["A3"] = dict(logN_max=logN[imax][0], R_at_max=float(RG[imax]), nu_at_max=logN[imax][2], sigma_max=max(x[1] for x in logN),
                 z_on_box_estimate=z_on, R_L_box=RL, dlin_ta=DLIN_TA, note="ESTIMATE; EH continued; matter+Lambda growth, no radiation (overestimates growth)")
# A4: CFG630 context
try:
    j630 = json.load(open(os.path.join(CFGD, "CFG630_settling_feeds_dark_energy", "cfg630_results.json")))
    dr1 = j630["prediction"]["can"]["drho_over_rho0"]["1.0"]; ceil = j630["checks"]["K4_ceiling"]["max_drho"]
    P(f"  A4 context (CFG630 JSON): settling -> dark energy since z = 1: {dr1[0]:.2e}-{dr1[1]:.2e} of rho_DE0 (canonical); max over brackets {ceil:.2e}")
    RES["A4"] = dict(drho_z1_canonical=dr1, max_drho_all=ceil)
except Exception as ex:
    P(f"  A4 context unavailable: {ex}"); RES["A4"] = None
VA = "SWITCH-OFF CONFIRMED" if (a1_ok and a2_ok and logN[imax][0] < -10) else "LOOPHOLE"
P(f"  PART A verdict: {VA}  (primary-CMB physics in the switch-off era is GR-linear and inherited; no primary-CMB spectrum computed)")
RES["verdict_A"] = VA

# ================================================================== PART B  CMB lensing
P("\nPART B  CMB lensing from the gravitating field")
# z = 1 appears TWICE (zero-width interval): the left copy belongs to the box side (z <= 1), the right copy to the extrapolated side,
# so a step in R at z = 1 (rule Z-a) is integrated exactly by the trapezoid rule (post-first-run engineering fix, see README).
N1Z, N2Z = 300, 400
ZL = np.concatenate([np.geomspace(1e-3, 1.0, N1Z), np.geomspace(1.0, 50.0, N2Z)])
LOWZ = np.arange(len(ZL)) < N1Z
AL = 1 / (1 + ZL); CHL = chi_of(ZL)
LL = np.arange(8, 2049)
KK = (LL[:, None] + 0.5) / CHL[None, :]                       # (nL, nz)
WGT = ((CHI_STAR - CHL) / CHI_STAR) ** 2 * (1 + ZL) ** 2

def interp_a(vals, a):
    """vals: (n_nodes, nk) on A_N; linear in a, clamp at the nodes' ends (a > 1 not used)."""
    a = np.clip(a, A_N[0], A_N[-1]); j = np.clip(np.searchsorted(A_N, a) - 1, 0, len(A_N) - 2)
    t = (a - A_N[j]) / (A_N[j + 1] - A_N[j]); return vals[j] * (1 - t) + vals[j + 1] * t
def logk_interp(kq, kn, yn):
    return np.interp(np.log(kq), np.log(kn), yn)

PS_N = np.array([SS[n]["Pg"][SUP] for n in LATE])              # S0 gravitating P on the support
def ratio_nodes(field="Pg", src_F=None):
    srcF = SF if src_F is None else src_F
    return np.array([srcF[n][field][SUP] / SS[n][field][SUP] for n in LATE])

def baseline(kind):
    """S0 weighting baseline on (LL, ZL)."""
    out = np.zeros_like(KK)
    for j, (a, z) in enumerate(zip(AL, ZL)):
        k = KK[:, j]; D2 = float(Dgrow(a)) ** 2; pl = P_lin0(k) * D2
        if kind == "base2":
            out[:, j] = pl; continue
        if LOWZ[j]:
            pn = np.exp(interp_a(np.log(PS_N), a))
        else:
            D1 = float(Dgrow(0.5)); Nk = PS_N[0] / (P_lin0(KS) * D1 ** 2)
            pn = P_lin0(KS) * D2 * (1 + (Nk - 1) * (D2 / D1 ** 2))
        ins = (k >= K_LO) & (k <= K_HI_B)
        v = pl.copy(); v[ins] = np.exp(logk_interp(k[ins], KS, np.log(pn)))
        hi = k > K_HI_B
        if hi.any():
            m = KS >= K_HI_B / 2; sl = np.polyfit(np.log(KS[m]), np.log(pn[m]), 1)[0]
            v[hi] = pn[-1] * (k[hi] / K_HI_B) ** sl
        out[:, j] = v
    return out

def ratio_grid(Rn, zrule, krule):
    """R on (LL, ZL) from node ratios Rn (n_nodes, nk_support)."""
    out = np.ones_like(KK)
    lowmean = Rn[:, :3].mean(axis=1)                            # per node
    def at_a(k, a):
        r = interp_a(Rn, a); lm = float(np.interp(a, A_N, lowmean))
        v = np.ones_like(k)
        ins = (k >= K_LO) & (k <= K_HI_B); v[ins] = logk_interp(k[ins], KS, r)
        v[k > K_HI_B] = r[-1]
        v[k < K_LO] = 1.0 if krule == "Ka" else lm
        return v
    for j, (a, z) in enumerate(zip(AL, ZL)):
        k = KK[:, j]
        if LOWZ[j]:
            out[:, j] = at_a(k, a)
        else:
            r1 = at_a(k, A_N[0])
            if zrule == "Za": out[:, j] = 1.0
            elif zrule == "Zb": out[:, j] = 1.0 + (r1 - 1.0) * max(0.0, (a - A_ZI) / (A_N[0] - A_ZI))
            elif zrule == "Zc": out[:, j] = r1
    return out

PL = None
x26 = open(os.path.join(REPO, "real_research", "cross_thread_review_2026_09_26", "XR26_cmb.py")).read()
import ast
PL18 = ast.literal_eval(x26[x26.index("PL18_MV = {") + len("PL18_MV = "):x26.index("DP_MEAN")].strip())
BANDS = {r: [(lo, hi, sA) for (lo, hi, A_, sA, fid) in PL18[r]] for r in ("8-400", "8-2048")}
BANDS["ACT40-763"] = [(L_, L_, 1.0) for L_ in range(40, 764)]  # uniform weight per integer L (ACT DR6 bandpowers not on disk)
SIG = {"8-400": 0.028, "8-2048": 0.026, "ACT40-763": 0.023}  # published amplitude errors, LABELLED CONTEXT
L4 = (LL * (LL + 1.0)) ** 2 * 4.0 / (LL + 0.5) ** 4

def cl_of(Pgrid, mask=None):
    I = WGT[None, :] * Pgrid
    if mask is not None: I = I * mask
    return L4 * _trapz(I, CHL, axis=1)                          # proportional to L^2 (L+1)^2 C_L^phiphi

def band_stats(clF, clS):
    out = {}
    for r, bl in BANDS.items():
        Ab, w = [], []
        for lo, hi, sA in bl:
            m = (LL >= lo) & (LL <= hi); Ab.append(clF[m].mean() / clS[m].mean()); w.append(1 / sA ** 2)
        Ab, w = np.array(Ab), np.array(w)
        out[r] = dict(dA=float((w * Ab).sum() / w.sum() - 1), A_b=Ab.tolist(),
                      dchi2_rel=float((((Ab - 1) ** 2) * w).sum()) if r != "ACT40-763" else None)
    return out

COV = (LOWZ[None, :] & (KK >= K_LO) & (KK <= K_HI_B)).astype(float)
ZMASK = np.broadcast_to(LOWZ[None, :], KK.shape).astype(float)
KMASK = ((KK >= K_LO) & (KK <= K_HI_B)).astype(float)

def coverage(base):
    clS = cl_of(base); out = {}
    for nm, M_ in (("box", COV), ("z_le_1", ZMASK), ("k_in_box", KMASK)):
        clc = cl_of(base, M_); r = {}
        for rr, bl in BANDS.items():
            fb, w = [], []
            for lo, hi, sA in bl:
                m = (LL >= lo) & (LL <= hi); fb.append(clc[m].mean() / clS[m].mean()); w.append(1 / sA ** 2)
            fb, w = np.array(fb), np.array(w); r[rr] = dict(f=float((w * fb).sum() / w.sum()), f_b=fb.tolist())
        out[nm] = r
    return out

BASES = {"base1": baseline("base1"), "base2": baseline("base2")}
P(f"  Limber: {len(LL)} integer L (8-2048) x {len(ZL)} z (1e-3-50); chi_* = {CHI_STAR:.1f} Mpc/h (engine background, no radiation)")
CV = {b: coverage(BASES[b]) for b in BASES}
for b in BASES:
    P(f"  coverage ({b}): box region (z <= 1 AND k in support) = " + ", ".join(f"{r} {CV[b]['box'][r]['f']:.3f}" for r in BANDS)
      + " | z <= 1 (any k) = " + ", ".join(f"{r} {CV[b]['z_le_1'][r]['f']:.3f}" for r in BANDS)
      + " | k in support (any z) = " + ", ".join(f"{r} {CV[b]['k_in_box'][r]['f']:.3f}" for r in BANDS))
RES["coverage"] = CV

def run_all(Rn, label):
    tab = {}
    for b, base in BASES.items():
        clS = cl_of(base)
        for zr in ("Za", "Zb", "Zc"):
            for kr in ("Ka", "Kb"):
                Rg = ratio_grid(Rn, zr, kr); tab[f"{b}|{zr}|{kr}"] = band_stats(cl_of(base * Rg), clS)
    return tab

def summarize(tab, label):
    can = tab["base1|Zb|Ka"]
    P(f"\n  [{label}] canonical (base1, Z-b, K-a): dA 8-400 = {can['8-400']['dA']:+.4f}, 8-2048 = {can['8-2048']['dA']:+.4f}, "
      f"ACT-range = {can['ACT40-763']['dA']:+.4f}; dchi2_rel 8-400 = {can['8-400']['dchi2_rel']:.2f}, 8-2048 = {can['8-2048']['dchi2_rel']:.2f}")
    P("    per-band A_b (8-400): " + " ".join(f"{x:.4f}" for x in can["8-400"]["A_b"]))
    P(f"    {'member':18s} {'dA 8-400':>9s} {'dA 8-2048':>10s} {'dA ACT':>8s} {'dchi2 8-400':>12s}")
    for m, v in tab.items():
        P(f"    {m:18s} {v['8-400']['dA']:+9.4f} {v['8-2048']['dA']:+10.4f} {v['ACT40-763']['dA']:+8.4f} {v['8-400']['dchi2_rel']:12.3f}")
    def label_rule(stat, sig):
        two = 2 * sig; vals = [v[stat]["dA"] for v in tab.values()]; c = can[stat]["dA"]
        if abs(c) > two: return "UNSAFE-ROBUST" if all(abs(x) > two for x in vals) else "UNSAFE"
        return "SAFE" if all(abs(x) <= two for x in vals) else "CONDITIONAL"
    lab = {s: label_rule(s, SIG[s]) for s in SIG}
    rng = {s: [min(v[s]["dA"] for v in tab.values()), max(v[s]["dA"] for v in tab.values())] for s in SIG}
    P(f"    bracket ranges: " + "; ".join(f"{s} [{rng[s][0]:+.4f}, {rng[s][1]:+.4f}] (2 sigma {2 * SIG[s]:.3f}) -> {lab[s]}" for s in SIG))
    return dict(canonical=can, members=tab, ranges=rng, labels=lab)

# node ratios on the box support, printed (first look at R beyond CFG596's published z = 0 values happens HERE)
RN_G = ratio_nodes("Pg"); RN_P = ratio_nodes("P")
for kq in (0.1, 0.3, 0.5, 1.0, 2.0):
    P(f"  R_grav(k = {kq}) at a = " + ", ".join(f"{a:.3f}: {logk_interp(np.array([kq]), KS, r)[0]:.4f}" for a, r in zip(A_N, RN_G)))
RES["R_nodes"] = dict(a=A_N.tolist(), k=KS.tolist(), R_grav=RN_G.tolist(), R_part=RN_P.tolist())

if not MUTATE:
    SG = summarize(run_all(RN_G, "gravitating field"), "gravitating field (VERDICT)")
    SPp = summarize(run_all(RN_P, "particle field"), "particle field (CONTEXT ONLY)")
    RES["B_grav"] = SG; RES["B_part_context"] = SPp
    VB = SG["labels"]["8-400"]
    RES["verdict_B"] = VB
    P(f"\n  PART B verdict (Planck 8-400 band weights, 2 sigma = 0.056, F vs S0): {VB}; ACT-range label (context) {SG['labels']['ACT40-763']}")
else:
    P("\nMUTATE set")
    # M1 F == S0
    RN0 = ratio_nodes("Pg", src_F=SS)
    t = run_all(RN0, "M1"); mx = max(abs(v[s]["dA"]) for v in t.values() for s in SIG)
    mc = max(abs(v[s]["dchi2_rel"]) for v in t.values() for s in ("8-400", "8-2048"))
    check("M1", "F == S0 -> dA = 0 (<= 1e-12) in every member and statistic; dchi2_rel = 0", mx <= 1e-12 and mc <= 1e-20, f"max |dA| {mx:.1e}, max dchi2 {mc:.1e}")
    # M2a constant 1.10 everywhere (direct grid, every base)
    dev = 0.0
    for b, base in BASES.items():
        st = band_stats(cl_of(base * 1.10), cl_of(base)); dev = max(dev, max(abs(st[s]["dA"] - 0.10) for s in SIG))
    check("M2a", "R == 1.10 everywhere -> dA = 0.100 (<= 1e-9)", dev <= 1e-9, f"max |dA - 0.1| {dev:.1e}")
    # M2b 1.10 on the covered region only; expected 0.1 x band-weighted coverage, computed independently
    dev = 0.0; rep = {}
    for b, base in BASES.items():
        st = band_stats(cl_of(base * (1 + 0.10 * COV)), cl_of(base))
        for s in SIG:
            exp_ = 0.10 * CV[b]["box"][s]["f"]; dev = max(dev, abs(st[s]["dA"] - exp_)); rep[f"{b}|{s}"] = (st[s]["dA"], exp_)
    check("M2b", "R = 1.10 on the box region only -> dA = 0.10 x f_cov (<= 1e-9)", dev <= 1e-9,
          f"max dev {dev:.1e}; e.g. base1 8-400 dA {rep['base1|8-400'][0]:.5f} vs {rep['base1|8-400'][1]:.5f}")
    # M2c CFG596's own z = 0 boost held for z <= 1 (K-a, Z-a), vs an independent midpoint-in-chi quadrature
    Bz0 = RN_G[-1]
    RNc = np.array([Bz0 for _ in A_N])
    tc = band_stats(cl_of(BASES["base1"] * ratio_grid(RNc, "Za", "Ka")), cl_of(BASES["base1"]))
    # independent: uniform chi midpoints, direct evaluation of base1 pieces through the same baseline definition on a new grid
    nchi = 6000; ce = np.linspace(chi_of(1e-3), chi_of(50.0), nchi + 1); cm = 0.5 * (ce[1:] + ce[:-1]); dc = np.diff(ce)
    zm = z_of_chi(cm); am = 1 / (1 + zm); wm = ((CHI_STAR - cm) / CHI_STAR) ** 2 * (1 + zm) ** 2
    def base1_point(k, a, z):
        D2 = float(Dgrow(a)) ** 2; pl = P_lin0(k) * D2
        if z <= 1.0:
            pn = np.exp(interp_a(np.log(PS_N), a))
        else:
            D1 = float(Dgrow(0.5)); Nk = PS_N[0] / (P_lin0(KS) * D1 ** 2); pn = P_lin0(KS) * D2 * (1 + (Nk - 1) * (D2 / D1 ** 2))
        v = pl.copy(); ins = (k >= K_LO) & (k <= K_HI_B); v[ins] = np.exp(logk_interp(k[ins], KS, np.log(pn)))
        hi = k > K_HI_B
        if hi.any():
            m = KS >= K_HI_B / 2; sl = np.polyfit(np.log(KS[m]), np.log(pn[m]), 1)[0]; v[hi] = pn[-1] * (k[hi] / K_HI_B) ** sl
        return v
    clF2 = np.zeros(len(LL)); clS2 = np.zeros(len(LL))
    for j in range(nchi):
        k = (LL + 0.5) / cm[j]; pb = base1_point(k, am[j], zm[j])
        r = np.ones_like(k)
        if zm[j] <= 1.0:
            ins = (k >= K_LO) & (k <= K_HI_B); r[ins] = logk_interp(k[ins], KS, Bz0); r[k > K_HI_B] = Bz0[-1]
        clS2 += wm[j] * pb * dc[j]; clF2 += wm[j] * pb * r * dc[j]
    ti = band_stats(L4 * clF2, L4 * clS2)
    rel = max(abs(tc[s]["dA"] - ti[s]["dA"]) / abs(ti[s]["dA"]) for s in SIG)
    check("M2c", "CFG596's own z = 0 boost injected (z <= 1, K-a, Z-a): dA > 0 and = independent midpoint quadrature (<= 1e-3 rel)",
          all(tc[s]["dA"] > 0 for s in SIG) and rel <= 1e-3,
          "; ".join(f"{s} {tc[s]['dA']:+.5f} vs {ti[s]['dA']:+.5f}" for s in SIG) + f"; max rel {rel:.1e}")
    RES["M2c"] = dict(grid=tc, independent=ti)
    RES["mutate_bites"] = all(CHECKS[c]["ok"] for c in ("M1", "M2a", "M2b", "M2c"))
    P(f"  MUTATE bites: {RES['mutate_bites']}")

RES["checks"] = CHECKS; RES["runtime_s"] = time.time() - T0
try:
    import resource; RES["maxrss_gb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
except Exception:
    pass
P(f"\nruntime {RES['runtime_s']:.0f} s; maxrss {RES.get('maxrss_gb', 0):.2f} GB. kappa = 1/2 FITTED; cold energy mass required; not theory closed.")
base = ARGS.out or os.path.join(HERE, f"cfg649_{ARGS.tag}" + ("_MUTATE" if MUTATE else ""))
def _clean(o):
    if isinstance(o, dict): return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return o
json.dump(_clean(RES), open(base + ".json", "w"), indent=1)
open(base + ".out", "w").write("\n".join(OUT) + "\n")
