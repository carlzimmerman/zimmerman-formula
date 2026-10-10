#!/usr/bin/env python3
"""CFG548 -- weighing the Local Group from its fringe: the zero-velocity radius R0 and the local Hubble flow, per FROZEN_CRITERIA.md
(committed alone first, 9eeab46c4).
Model: radial Lynden-Bell--Sandage shells about the LG barycentre from the Big Bang to t0 under r'' = -G M/r^2 + DE push (w = -1
primary; DESI w0wa variants), first branch.  Under candidate B the law is off outside bound systems, so the fringe feels Newtonian
gravity of the LG's total (baryons + settled cold energy).  Masses under test from CFG522's JSON (F-M1 shared catchment, F-CI
census-individual); LCDM comparator = timing-argument mass with the same constants.  Data: the committed UNGC (Karachentsev+13).
kappa = 1/2 FITTED; footings never pooled; cold energy mass still required.  Published numbers are PROVISIONAL recalls; nothing
is downloaded.
MUTATE (CFG548_MUTATE=1): T1 Lambda = 0 vs the closed form, T2 F-M1 x 0.3 must be TOO LIGHT, T3 shuffled distances.
Run: nice -n 10 python3 campaign_fresh_gravity/CFG548_local_group_zero_velocity_surface/cfg548_lg_zvs.py   (CFG548_MUTATE=1 too)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "2"
import io, math, json, time, contextlib, hashlib
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
ROOT = os.path.dirname(LANES)
try:
    os.nice(10)
except OSError:
    pass
MUTATE = os.environ.get("CFG548_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
LOG, CHK, RES = [], {}, {"lane": "CFG548", "mutate": MUTATE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}]{'' if lb else ' (reported)'} {name}: {msg}")


P(__doc__.split("Run:")[0].strip())
P(f"  FROZEN_CRITERIA.md sha256 {hashlib.sha256(open(os.path.join(HERE, 'FROZEN_CRITERIA.md'), 'rb').read()).hexdigest()}")

# ------------------------------------------------------------------ constants (CFG513/515: kpc, km/s, Msun)
G = 4.30091727e-6
KPC_M = 3.0856775814913673e19
GYR = 3.15576e16 / (KPC_M / 1e3)
h = 0.674; H0 = 0.1 * h; OM_M = 0.3153; OM_L = 1 - OM_M
T0_GYR = 13.80; T0 = T0_GYR * GYR
A0 = {"canonical": 9.36e-11 * KPC_M / 1e6, "alt": 1.13e-10 * KPC_M / 1e6}
FOOTS = ("canonical", "alt")
nu_mono = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(np.maximum(y, 1e-300))))
D_TIM, VR_TIM, VT_SAL = 770.0, -109.3, 82.4
MB_LG = 1.8e11
SIG_D = 0.05
R0_K09, ER0_K09 = 960.0, 30.0                         # Karachentsev+09, PROVISIONAL
PUB_M = {"K09 (1.9+-0.2)e12": (1.9e12, 0.2e12, 0.2e12), "P14 (2.3+-0.7)e12": (2.3e12, 0.7e12, 0.7e12),
         "P16 incl. LMC 2.64(+0.42/-0.38)e12": (2.64e12, 0.38e12, 0.42e12)}                    # PROVISIONAL recalls
DESI = {"DESI DR2+CMB+Pantheon+ (w0 -0.838, wa -0.62)": (-0.838, -0.62), "DESI DR2+CMB+DESY5 (w0 -0.752, wa -0.86) [reported]": (-0.752, -0.86)}

# ------------------------------------------------------------------ masses from CFG522 JSON
J522 = json.load(open(os.path.join(LANES, "CFG522_local_group_timing", "cfg522_results.json")))
sys.path.insert(0, os.path.join(LANES, "CFG515_census_edge_resolution"))
import cfg515_lib as L                                                       # noqa: E402
COLD = L.COLD_PER_B
MASS = {}
for f in FOOTS:
    MASS[f] = {"F-M1 shared catchment": J522["M1"][f]["full"]["M_tot"], "F-CI census-individual": J522["census_individual"][f]["M_tot"]}
fMb73 = J522["D6"]["MW7.3e10+M31"]["f_ret"]; fM33 = J522["D6"]["MW+M31+M33+LMC"]["f_ret"]
MVAR = {"F-M1 M_b,MW 7.3e10": 1.93e11 * (1 + COLD / fMb73), "F-M1 +M33/LMC baryons": 1.91e11 * (1 + COLD / fM33)}
F_LG = J522["census"]["f_LG"]
P(f"\n  masses (CFG522 JSON): " + "; ".join(f"{k} {v:.4e}" for k, v in MASS['canonical'].items()) + f" (alt identical: "
  f"{MASS['alt']['F-M1 shared catchment']:.4e}); variants " + "; ".join(f"{k} {v:.4e}" for k, v in MVAR.items()) + f"; f_LG {F_LG:.4f}")


# ------------------------------------------------------------------ background (only needed for w != -1)
def background(w0, wa):
    fde = lambda a: a ** (-3 * (1 + w0 + wa)) * math.exp(-3 * wa * (1 - a))
    la = np.linspace(math.log(1e-8), 0.0, 20001); ag = np.exp(la)
    E = np.sqrt(OM_M / ag ** 3 + OM_L * np.array([fde(a) for a in ag]))
    integ = 1.0 / (H0 * E)
    t = np.concatenate([[0.0], np.cumsum(0.5 * (integ[1:] + integ[:-1]) * np.diff(la))])
    t += (2.0 / 3.0) / (H0 * math.sqrt(OM_M)) * ag[0] ** 1.5
    aoft = lambda tt: float(np.interp(tt, t, ag))
    push = lambda tt: -0.5 * (1 + 3 * (w0 + wa * (1 - aoft(tt)))) * OM_L * H0 ** 2 * fde(aoft(tt))
    return float(t[-1]), push


T_LCDM_OWN, _ = background(-1.0, 0.0)
P(f"  background check: LCDM age with these constants (no radiation) {T_LCDM_OWN / GYR:.3f} Gyr (t0 used for w = -1: {T0_GYR})")


# ------------------------------------------------------------------ the shell family
def shells(Mfun, Mi, t0=T0, push=None, lam=True, ne=300, law=None, Mscale=None):
    """first-branch v(R) at t0.  Mfun(r, t) enclosed gravitating mass; Mi the mass used for the t_i start.  push(t) -> coefficient of r
    (default Omega_L H0^2 if lam).  law: optional callable g(r, t) replacing G M/r^2.  Returns sorted (R, v)."""
    Ms = Mscale or Mi
    Rs = (G * Ms * t0 ** 2) ** (1 / 3); eu = G * Ms / Rs
    ti = 1e-4 * t0
    ri = (4.5 * G * Mi * ti ** 2) ** (1 / 3)
    emax = 0.5 * (0.15 * 6000.0) ** 2 / eu * 1.5
    if law is not None:
        emax *= 1.0
    es = -2.5 + (emax + 2.5) * np.linspace(0, 1, ne) ** 3
    kL = OM_L * H0 ** 2 if lam else 0.0

    def rhs(t, y):
        r = max(y[0], 1e-6)
        g = law(r, t) if law is not None else G * Mfun(r, t) / r ** 2
        k = push(t) if push is not None else kL
        return [y[1], -g + k * r]

    ev = lambda t, y: y[0] - 1.0
    ev.terminal = True; ev.direction = -1
    out = []
    for e in es:
        v2 = 2 * (e * eu + G * Mi / ri + 0.5 * kL * ri ** 2)
        if v2 <= 0:
            continue
        s = solve_ivp(rhs, (ti, t0), [ri, math.sqrt(v2)], method="DOP853", rtol=1e-9, atol=1e-9, events=ev)
        if s.t_events[0].size or s.status != 0:
            continue
        out.append((s.y[0, -1], s.y[1, -1]))
    out = np.array(sorted(out))
    return out[:, 0], out[:, 1]


def R0_of(R, v):
    i = np.where((v[:-1] < 0) & (v[1:] >= 0))[0]
    if not i.size:
        return float("nan")
    j = i[-1]
    return float(R[j] - v[j] * (R[j + 1] - R[j]) / (v[j + 1] - v[j]))


def pm(M):
    return lambda r, t: M


# ------------------------------------------------------------------ data: the committed UNGC
def vizier_tsv(path):
    rows = [l.rstrip("\n").split("\t") for l in open(path, encoding="latin-1") if l.strip() and not l.startswith("#")]
    hdr = [x.strip() for x in rows[0]]
    return [{hdr[i]: (r[i].strip() if i < len(r) else "") for i in range(len(hdr))} for r in rows[3:]]


def _f(x):
    try:
        return float(x)
    except Exception:
        return float("nan")


UNGC = vizier_tsv(os.path.join(ROOT, "real_research", "data", "ungc_karachentsev2013.tsv"))
ACC = ("TRGB", "Cep", "RR", "HB", "SBF", "BS", "CMD", "geom")


def frame(f31):
    nm = np.array([r["Name"].strip() for r in UNGC]); MD = np.array([r["MD"].strip() for r in UNGC])
    ra = np.array([_f(r["_RAJ2000"]) for r in UNGC]); de = np.array([_f(r["_DEJ2000"]) for r in UNGC])
    D = np.array([_f(r["Dist"]) for r in UNGC]) * 1e3; V = np.array([_f(r["Vlg"]) for r in UNGC])
    fD = np.array([r["f_Dist"].strip() for r in UNGC]); Ti = np.array([_f(r["Ti1"]) for r in UNGC])
    un = np.nan_to_num(np.stack([np.cos(np.radians(de)) * np.cos(np.radians(ra)), np.cos(np.radians(de)) * np.sin(np.radians(ra)),
                                 np.sin(np.radians(de))], axis=1))
    i31 = int(np.where(nm == "MESSIER031")[0][0])
    xc = f31 * D[i31] * un[i31]; Dc = float(np.linalg.norm(xc)); nc = xc / Dc
    with np.errstate(all="ignore"):                       # Accelerate matmul raises spurious FP flags on the zero rows (no coordinates)
        cth = un @ nc
        d31 = np.linalg.norm(D[:, None] * un - (D[i31] * un[i31])[None, :], axis=1)
    R = np.sqrt(np.clip(D ** 2 + Dc ** 2 - 2 * D * Dc * cth, 0, None)); Vr = V * (D - Dc * cth) / np.maximum(R, 1e-9)
    Rn = dict(zip(nm, R))
    return dict(name=nm, MD=MD, D=D, V=V, fD=fD, Ti=Ti, R=R, Vr=Vr, Rn=Rn, dMW=D, d31=d31)


def select(fr, win, groups=True):
    ok = np.isfinite(fr["R"]) & np.isfinite(fr["Vr"]) & np.isin(fr["fD"], ACC) & (fr["R"] >= win[0]) & (fr["R"] <= win[1])
    if groups:
        keep = np.array([(md in ("Milky Way", "MESSIER031", "MESSIER033")) or (np.isfinite(ti) and ti <= 0)
                         or (fr["Rn"].get(md, np.inf) < 1500.0) for md, ti in zip(fr["MD"], fr["Ti"])])
        ok &= keep
    return ok


# ------------------------------------------------------------------ fitting machinery (tables over a mass grid)
MGRID = np.geomspace(3e11, 3e13, 33)
SGRID = np.geomspace(5.0, 200.0, 70)


def table(push=None, t0=T0, lam=True):
    tab = []
    for M in MGRID:
        R, v = shells(pm(M), M, t0=t0, push=push, lam=lam)
        tab.append((R, v, R0_of(R, v)))
    return tab


def model_at(tab, Rq):
    V = np.empty((len(tab), len(Rq))); S = np.empty_like(V)
    for k, (R, v, _) in enumerate(tab):
        V[k] = np.interp(Rq, R, v)
        dv = np.gradient(v, R)
        S[k] = np.interp(Rq, R, dv)
    return V, S


def fit(tab, R, Vr, sig_d=SIG_D):
    """profile likelihood over sigma_int; returns (M_fit, R0_fit, sig_int, lnL_max, lnL(M) array)."""
    Vm, Sm = model_at(tab, R)
    res2 = (Vr[None, :] - Vm) ** 2                                         # (K, N)
    ed2 = (Sm * sig_d * R[None, :]) ** 2
    var = SGRID[None, :, None] ** 2 + ed2[:, None, :]                       # (K, S, N)
    lnl = -0.5 * np.sum(res2[:, None, :] / var + np.log(2 * np.pi * var), axis=2)
    js = np.argmax(lnl, axis=1); prof = lnl[np.arange(len(tab)), js]
    k = int(np.argmax(prof))
    lm = np.log(MGRID)
    if 0 < k < len(MGRID) - 1:
        y0, y1, y2 = prof[k - 1], prof[k], prof[k + 1]; den = y0 - 2 * y1 + y2
        dx = 0.5 * (y0 - y2) / den if den < 0 else 0.0
        lmf = lm[k] + dx * (lm[1] - lm[0])
    else:
        lmf = lm[k]
    r0s = np.array([t[2] for t in tab])
    R0f = float(np.exp(np.interp(lmf, lm, np.log(r0s))))
    return float(np.exp(lmf)), R0f, float(SGRID[js[k]]), float(prof.max()), prof


def R0_pred_from_tab(tab, M):
    r0s = np.array([t[2] for t in tab])
    return float(np.exp(np.interp(math.log(M), np.log(MGRID), np.log(r0s))))


def linfit_R0(R, Vr):
    A = np.vstack([R, np.ones_like(R)]).T
    (s, b), *_ = np.linalg.lstsq(A, Vr, rcond=None)
    return -b / s, s * 1e3, float(np.std(Vr - (s * R + b)))


# ------------------------------------------------------------------ LCDM timing mass (point-mass two-body, Lambda, first approach)
def age_of(M, d, vr, vt=0.0):
    Lm = d * vt

    def rhs(t, y):
        r = max(y[0], 1e-3)
        return [-y[1], -(-G * M / r ** 2 + Lm ** 2 / r ** 3 + OM_L * H0 ** 2 * r)]
    if vt == 0.0:
        ev = lambda t, y: y[0] - 0.05
        ev.terminal = True; ev.direction = -1
    else:
        ev = lambda t, y: y[1]
        ev.terminal = True; ev.direction = -1
    s = solve_ivp(rhs, (0, 60 * GYR), [d, vr], events=ev, rtol=1e-11, atol=1e-11, max_step=0.05 * GYR)
    if s.t_events[0].size:
        te = s.t_events[0][0]
        if vt == 0.0:
            ye = s.y_events[0][0]; te += ye[0] / max(abs(ye[1]), 1e-9) * 0.5
        return te
    return 60 * GYR


def timing_mass(d, vr, vt=0.0):
    return brentq(lambda lm: age_of(10 ** lm, d, vr, vt) - T0, 11.5, 14.0, xtol=1e-10)


def vr_given(M, d, vt=0.0):
    return brentq(lambda v: age_of(M, d, v, vt) - T0, -600.0, -1.0, xtol=1e-9)


# ====================================================================================================================================
P("\n== CONTROLS (part 1) ==")
# K1: Lambda = 0 vs the Lynden-Bell closed form
MK = MASS["canonical"]["F-M1 shared catchment"]
R_, v_ = shells(pm(MK), MK, lam=False)
R0_l0 = R0_of(R_, v_); R0_cf = (8 * G * MK * T0 ** 2 / math.pi ** 2) ** (1 / 3)
check("K1", abs(R0_l0 / R0_cf - 1) < 0.005, f"Lambda = 0 R0 {R0_l0:.1f} kpc vs closed form {R0_cf:.1f} ({100 * (R0_l0 / R0_cf - 1):+.3f}%)")
RES["K1"] = dict(R0_lam0=R0_l0, R0_closed=R0_cf)

# K2: LCDM timing mass
M_tr = 10 ** timing_mass(D_TIM, VR_TIM); M_tt = 10 ** timing_mass(D_TIM, VR_TIM, VT_SAL)
vback = vr_given(M_tr, D_TIM)
check("K2", abs(vback - VR_TIM) < 0.1, f"LCDM radial timing mass {M_tr:.4e} re-integrated -> v_r {vback:.3f} km/s (target {VR_TIM})")
M_tr_d = {d: 10 ** timing_mass(d, VR_TIM) for d in (730.0, 810.0)}
vpm522 = vr_given(MASS["canonical"]["F-M1 shared catchment"], 780.0)
P(f"    LCDM timing masses: radial {M_tr:.4e} (D 730: {M_tr_d[730.0]:.3e}, 810: {M_tr_d[810.0]:.3e}); v_tan 82.4: {M_tt:.4e}")
P(f"    reported: F-M1 total as a point mass at 780 kpc -> radial v_r {vpm522:.1f} km/s vs CFG522 extended profile "
  f"{J522['M1']['canonical']['full']['v_radial']:.1f}")
RES["LCDM_timing"] = dict(radial=M_tr, radial_D730=M_tr_d[730.0], radial_D810=M_tr_d[810.0], vtan82=M_tt, K2_vback=vback,
                          F_M1_pointmass_vr780=vpm522)
MODELS = {"F-M1 shared catchment": MASS["canonical"]["F-M1 shared catchment"], "F-CI census-individual": MASS["canonical"]["F-CI census-individual"],
          **MVAR, "LCDM timing (radial)": M_tr, "LCDM timing (v_tan 82.4)": M_tt}

# ------------------------------------------------------------------ tables
P("\n== MODEL TABLES ==")
t1 = time.time()
TAB = table()
P(f"  w = -1 table over {len(MGRID)} masses ({time.time() - t1:.0f} s); R0(M): " + ", ".join(f"{m:.1e}->{t[2]:.0f}" for m, t in zip(MGRID[::8], TAB[::8])))
TABD, T0D = {}, {}
for lab, (w0, wa) in DESI.items():
    t0d, push = background(w0, wa)
    T0D[lab] = t0d
    TABD[lab] = table(push=push, t0=t0d)
    P(f"  {lab}: own age {t0d / GYR:.3f} Gyr; table done")

# ------------------------------------------------------------------ data
P("\n== DATA (committed UNGC, Karachentsev+13) ==")
WINS = ((600.0, 2500.0), (500.0, 2000.0), (700.0, 3000.0))
F31S = (2 / 3, 0.5, 0.6)
FR = {f: frame(f) for f in F31S}
fr0 = FR[2 / 3]; sel0 = select(fr0, WINS[0])
Rd, Vd = fr0["R"][sel0], fr0["Vr"][sel0]
P(f"  primary sample (f31 2/3, 0.6-2.5 Mpc, accurate distances, group rule): N = {sel0.sum()}")
for n, r, v in sorted(zip(fr0["name"][sel0], Rd, Vd), key=lambda x: x[1]):
    P(f"    {n:18s} R {r:7.0f} kpc  V_r {v:+6.0f} km/s")
RES["sample"] = [dict(name=str(n), R_kpc=float(r), Vr=float(v)) for n, r, v in zip(fr0["name"][sel0], Rd, Vd)]

# K4 (reported): FP11-style linear fit
fr63 = frame(0.63)
s_all = np.isfinite(fr63["R"]) & np.isfinite(fr63["Vr"]) & np.isin(fr63["fD"], ACC) & (fr63["R"] >= 700) & (fr63["R"] <= 3000)
s_grp = select(fr63, (700.0, 3000.0))
l_all = linfit_R0(fr63["R"][s_all], fr63["Vr"][s_all]); l_grp = linfit_R0(fr63["R"][s_grp], fr63["Vr"][s_grp])
check("K4", True, f"f31 0.63, 0.7-3 Mpc linear fit: accurate distances, no group cut (N {s_all.sum()}) R0 {l_all[0]:.0f} kpc, "
      f"H {l_all[1]:.0f}, rms {l_all[2]:.0f}; with the frozen group rule (N {s_grp.sum()}) R0 {l_grp[0]:.0f}, H {l_grp[1]:.0f}, "
      f"rms {l_grp[2]:.0f} [FP11 committed: 1.050 all / 1.048 accurate, groups excluded]", lb=False)
RES["K4"] = dict(all=dict(N=int(s_all.sum()), R0=l_all[0], H=l_all[1], rms=l_all[2]), grp=dict(N=int(s_grp.sum()), R0=l_grp[0], H=l_grp[1], rms=l_grp[2]))

# ------------------------------------------------------------------ the weighing
P("\n== THE WEIGHING (point mass + Lambda fit) ==")
Mf, R0m, sint, lnL0, prof0 = fit(TAB, Rd, Vd)
P(f"  primary: M_flow {Mf:.3e} Msun, R0_meas {R0m:.0f} kpc, sigma_int {sint:.0f} km/s, N {len(Rd)}")
rng = np.random.default_rng(548)
bo = []
for _ in range(400):
    ii = rng.integers(0, len(Rd), len(Rd))
    bo.append(fit(TAB, Rd[ii], Vd[ii])[1])
sig_boot = float(np.std(bo))
vari = {}
for f31 in F31S:
    for w in WINS:
        s_ = select(FR[f31], w)
        m_, r_, si_, _, _ = fit(TAB, FR[f31]["R"][s_], FR[f31]["Vr"][s_])
        vari[f"f31 {f31:.3f} win {w[0]:.0f}-{w[1]:.0f}"] = dict(N=int(s_.sum()), M=m_, R0=r_, sig_int=si_)
        P(f"    variant f31 {f31:.3f}, window {w[0]:.0f}-{w[1]:.0f}: N {s_.sum()}, M {m_:.3e}, R0 {r_:.0f}, sigma_int {si_:.0f}")
r0v = np.array([v["R0"] for v in vari.values()])
sig_sys = 0.5 * float(r0v.max() - r0v.min())
sig_tot = math.hypot(sig_boot, sig_sys)
sig_lnM = 3 * sig_tot / R0m
P(f"  sigma_boot {sig_boot:.0f} kpc, sigma_sys (half range of {len(r0v)} variants) {sig_sys:.0f}, sigma_tot {sig_tot:.0f} "
  f"({100 * sig_tot / R0m:.1f}% of R0; diagnostic line 11.6%); sigma_lnM {sig_lnM:.3f}")
RES["weighing"] = dict(M_flow=Mf, R0_meas=R0m, sig_int=sint, N=int(len(Rd)), sig_boot=sig_boot, sig_sys=sig_sys, sig_tot=sig_tot,
                       sig_lnM=sig_lnM, variants=vari)
fret_post = COLD * MB_LG / (Mf - MB_LG)
P(f"  post-hoc common f_ret implied by the flow mass (M_b 1.8e11): {fret_post:.3f}  (CFG522 shared catchment 0.170; timing allowed ~0.12-0.30)")
RES["weighing"]["fret_post_hoc"] = fret_post

# DESI fits
desi_fit = {}
for lab in DESI:
    m_, r_, si_, _, _ = fit(TABD[lab], Rd, Vd)
    desi_fit[lab] = dict(M=m_, R0=r_, sig_int=si_)
    P(f"  {lab}: M_flow {m_:.3e}, R0_meas {r_:.0f}")
RES["desi_fit"] = desi_fit

# K3: injection-recovery
P("\n== CONTROLS (part 2) ==")
Minj = MASS["canonical"]["F-M1 shared catchment"]; R0inj = R0_pred_from_tab(TAB, Minj)
Rt_, vt_ = shells(pm(Minj), Minj)
rr, zz = [], []
for _ in range(50):
    vm = np.interp(Rd, Rt_, vt_) + rng.normal(0, 35.0, len(Rd))
    Ro = Rd * (1 + SIG_D * rng.normal(size=len(Rd)))
    mm, r0r, *_ = fit(TAB, Ro, vm)
    rr.append(r0r); zz.append((R0inj - r0r) / sig_tot)
check("K3", abs(np.median(rr) / R0inj - 1) < 0.03 and abs(np.mean(zz)) < 1,
      f"injected F-M1 (R0 {R0inj:.0f}): median recovered R0 {np.median(rr):.0f} ({100 * (np.median(rr) / R0inj - 1):+.1f}%), mean Z {np.mean(zz):+.2f}")
RES["K3"] = dict(R0_inj=R0inj, R0_rec_median=float(np.median(rr)), meanZ=float(np.mean(zz)))

# ------------------------------------------------------------------ predictions and Z
P("\n== PREDICTIONS (point mass, w = -1) and Z against R0_meas ==")
PRED = {}
for foot in FOOTS:
    PRED[foot] = {}
    mods = dict(MODELS); mods["F-M1 shared catchment"] = MASS[foot]["F-M1 shared catchment"]; mods["F-CI census-individual"] = MASS[foot]["F-CI census-individual"]
    if MUTATE:
        mods = {"T2: F-M1 x 0.3": 0.3 * MASS[foot]["F-M1 shared catchment"], **mods}
    for k, M in mods.items():
        r0p = R0_pred_from_tab(TAB, M)
        Z = (r0p - R0m) / sig_tot
        Zk = (r0p - R0_K09) / math.hypot(ER0_K09, sig_sys)
        lnr = math.log(Mf / M)
        PRED[foot][k] = dict(M=M, R0_pred=r0p, Z=Z, Z_vs_K09=Zk, ln_Mflow_over_M=lnr, agree_timing=abs(lnr) <= 2 * sig_lnM)
        P(f"  [{foot}] {k:30s} M {M:.3e}: R0_pred {r0p:6.0f} kpc  Z {Z:+6.2f}  (vs K09 0.96+-0.03: {Zk:+6.2f})  "
          f"M_flow/M {Mf / M:.3f}  ({'AGREES' if abs(lnr) <= 2 * sig_lnM else 'DISAGREES'})")
RES["pred"] = PRED

# variants
P("\n== VARIANTS ==")
VAR = {}
# DESI
for lab in DESI:
    for foot in FOOTS:
        M = MASS[foot]["F-M1 shared catchment"]
        r0p = R0_pred_from_tab(TABD[lab], M)
        VAR[f"{lab} [{foot}]"] = dict(R0_pred=r0p, R0_meas=desi_fit[lab]["R0"], Z=(r0p - desi_fit[lab]["R0"]) / sig_tot,
                                       R0_pred_LCDM_radial=R0_pred_from_tab(TABD[lab], M_tr))
        P(f"  {lab} [{foot}]: F-M1 R0_pred {r0p:.0f} vs R0_meas(same model) {desi_fit[lab]['R0']:.0f}: Z {VAR[f'{lab} [{foot}]']['Z']:+.2f}"
          f"; LCDM-timing(radial) R0_pred {VAR[f'{lab} [{foot}]']['R0_pred_LCDM_radial']:.0f}")
# rigid profile (CFG522 M1 settings), per footing
p515 = os.path.join(LANES, "CFG515_census_edge_resolution", "cfg515_mw.py")
src = open(p515).read(); mk = "J513 = json.load("
assert src.count(mk) == 1
NS = {"__file__": p515, "__name__": "cfg515_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index(mk)], "cfg515_ro", "exec"), NS)
Prof = NS["Prof"]
for foot in FOOTS:
    mw = Prof("mw", Mb=6.0e10, foot=foot, fret=F_LG); m31 = Prof("m31", Mb=1.2e11, foot=foot, fret=F_LG, point=True)
    lr = np.linspace(-1.0, 4.0, 900); rr_ = 10 ** lr
    Mr = mw.Mb_enc(rr_) + mw.Mdark(rr_) + m31.Mb_enc(rr_) + m31.Mdark(rr_)
    Mtot = mw.Mb_tot() + mw.Mcold + m31.Mb_tot() + m31.Mcold
    Mfun = lambda r, t, Mr=Mr: float(np.interp(math.log10(max(r, 0.1)), lr, Mr))
    Rp, vp = shells(Mfun, Mtot)
    r0p = R0_of(Rp, vp)
    VAR[f"rigid profile [{foot}]"] = dict(M_tot=float(Mtot), edges=[float(mw.redge), float(m31.redge)], M_at_edge_m31=float(Mfun(m31.redge, 0)),
                                         R0_pred=r0p, Z=(r0p - R0m) / sig_tot)
    P(f"  rigid profile [{foot}] (edges {mw.redge:.0f}/{m31.redge:.0f} kpc, M_tot {Mtot:.4e}): R0_pred {r0p:.0f}, Z {(r0p - R0m) / sig_tot:+.2f}")
# growth bracket (reported)
Mb_, Mc_ = MB_LG, MASS["canonical"]["F-M1 shared catchment"] - MB_LG
Rg, vg = shells(lambda r, t: Mb_ + Mc_ * t / T0, Mb_, Mscale=Mb_ + Mc_)
r0g = R0_of(Rg, vg)
VAR["growth: cold mass ~ t [reported]"] = dict(R0_pred=r0g, Z=(r0g - R0m) / sig_tot)
P(f"  growth bracket (cold mass ~ t, reported): R0_pred {r0g:.0f}, Z {(r0g - R0m) / sig_tot:+.2f}")
# plain law outside (reference, not candidate B)
for foot in FOOTS:
    a0 = A0[foot]
    law = lambda r, t, a0=a0: float(nu_mono(G * MB_LG / r ** 2 / a0)) * G * MB_LG / r ** 2
    Rm, vm_ = shells(None, MB_LG, law=law, ne=320, Mscale=3e12)
    r0p = R0_of(Rm, vm_)
    VAR[f"reference: law on outside, baryons 1.8e11 [{foot}]"] = dict(R0_pred=r0p, Z=(r0p - R0m) / sig_tot)
    P(f"  reference (NOT candidate B) law on outside, baryons only [{foot}]: R0_pred {r0p:.0f}, Z {(r0p - R0m) / sig_tot:+.2f}")
RES["variants"] = VAR

# Hubble slope just outside (reported)
so = Rd >= R0m
if so.sum() >= 3:
    s_d = np.polyfit(Rd[so], Vd[so], 1)[0] * 1e3
else:
    s_d = float("nan")
Rg_ = np.linspace(R0m, 2500.0, 60)
slopes = {}
for k in ("F-M1 shared catchment", "LCDM timing (radial)"):
    M = MODELS[k]; Rt2, vt2 = shells(pm(M), M)
    slopes[k] = float(np.polyfit(Rg_, np.interp(Rg_, Rt2, vt2), 1)[0] * 1e3)
slopes["best-fit flow mass"] = float(np.polyfit(Rg_, np.interp(Rg_, *shells(pm(Mf), Mf)), 1)[0] * 1e3)
P(f"\n  Hubble slope over [R0_meas, 2.5 Mpc]: data {s_d:.0f} km/s/Mpc (N {so.sum()}); models: " + ", ".join(f"{k} {v:.0f}" for k, v in slopes.items()))
RES["hubble_slope"] = dict(data=s_d, N=int(so.sum()), models=slopes)

# published masses as ratios (reported; the LMC systematic via P16)
P("  published flow masses (PROVISIONAL) vs F-M1 and this lane's flow mass:")
RES["published"] = {}
for k, (m, lo, hi) in PUB_M.items():
    zM = (MODELS["F-M1 shared catchment"] - m) / hi
    RES["published"][k] = dict(M=m, F_M1_over=MODELS["F-M1 shared catchment"] / m, Mflow_over=Mf / m, Z_mass=zM,
                               R0_of_M=R0_pred_from_tab(TAB, m))
    P(f"    {k}: F-M1/M {MODELS['F-M1 shared catchment'] / m:.2f} (Z_mass {zM:+.1f}); this lane's M_flow/M {Mf / m:.2f}; "
      f"R0 at that mass in this model {R0_pred_from_tab(TAB, m):.0f} kpc")

# ------------------------------------------------------------------ POST HOC (dated 2026-10-09; reported, NOT part of the verdict)
P("\n== POST HOC (dated 2026-10-09; reported only, not part of the verdict) ==")
PH = {}
# (a) satellites: the frozen window's inner edge lets bound MW satellites (Leo I/II, CVn I, ...) in at R ~ 0.6-0.7 Mpc
for cut in (300.0, 400.0):
    for f31 in F31S:
        for w in WINS:
            s_ = select(FR[f31], w) & (FR[f31]["dMW"] > cut) & (FR[f31]["d31"] > cut)
            m_, r_, si_, _, _ = fit(TAB, FR[f31]["R"][s_], FR[f31]["Vr"][s_])
            PH[f"sat-cut {cut:.0f} f31 {f31:.3f} win {w[0]:.0f}-{w[1]:.0f}"] = dict(N=int(s_.sum()), M=m_, R0=r_, sig_int=si_)
    r0c = np.array([v["R0"] for k, v in PH.items() if k.startswith(f"sat-cut {cut:.0f}")])
    k0 = f"sat-cut {cut:.0f} f31 0.667 win 600-2500"
    s0 = select(FR[2 / 3], WINS[0]) & (FR[2 / 3]["dMW"] > cut) & (FR[2 / 3]["d31"] > cut)
    bo_ = [fit(TAB, FR[2 / 3]["R"][s0][ii], FR[2 / 3]["Vr"][s0][ii])[1] for ii in (rng.integers(0, s0.sum(), s0.sum()) for _ in range(200))]
    sb_, ss_ = float(np.std(bo_)), 0.5 * float(r0c.max() - r0c.min()); st_ = math.hypot(sb_, ss_)
    zz_ = {k: (R0_pred_from_tab(TAB, MODELS[k]) - PH[k0]["R0"]) / st_ for k in ("F-M1 shared catchment", "F-CI census-individual", "LCDM timing (radial)", "LCDM timing (v_tan 82.4)")}
    PH[f"summary cut {cut:.0f}"] = dict(R0=PH[k0]["R0"], M=PH[k0]["M"], N=PH[k0]["N"], sig_boot=sb_, sig_sys=ss_, sig_tot=st_, frac=st_ / PH[k0]["R0"], Z=zz_)
    P(f"  satellites within {cut:.0f} kpc of the MW or M31 removed: primary N {PH[k0]['N']}, M_flow {PH[k0]['M']:.3e}, R0 {PH[k0]['R0']:.0f}; "
      f"variants R0 {r0c.min():.0f}-{r0c.max():.0f}; sigma_boot {sb_:.0f}, sigma_sys {ss_:.0f}, sigma_tot/R0 {st_ / PH[k0]['R0']:.3f}; Z: "
      + ", ".join(f"{k} {z:+.2f}" for k, z in zz_.items()))
# (b) the rigid-profile variant as frozen is ill-posed: shells started on the point-mass-total family at r_i ~ 0.6 kpc feel only
#     the inner ~1e11 Msun and all escape (no zero crossing).  Reported alternative: start each shell self-consistently on the
#     enclosed mass, r_i = (4.5 G M(r_i) t_i^2)^(1/3).
for foot in FOOTS:
    mw = Prof("mw", Mb=6.0e10, foot=foot, fret=F_LG); m31 = Prof("m31", Mb=1.2e11, foot=foot, fret=F_LG, point=True)
    lr = np.linspace(-1.0, 4.0, 900); rr_ = 10 ** lr
    Mr = mw.Mb_enc(rr_) + mw.Mdark(rr_) + m31.Mb_enc(rr_) + m31.Mdark(rr_)
    Mfun = lambda r, t, Mr=Mr: float(np.interp(math.log10(max(r, 0.1)), lr, Mr))
    ti = 1e-4 * T0; ri = 1.0
    for _ in range(200):
        ri = (4.5 * G * Mfun(ri, 0) * ti ** 2) ** (1 / 3)
    Mi = Mfun(ri, 0)
    Rp, vp = shells(Mfun, Mi, Mscale=float(Mr[-1]))
    r0p = R0_of(Rp, vp)
    PH[f"rigid profile self-consistent start [{foot}]"] = dict(r_i=ri, M_i=Mi, R0_pred=r0p, Z=(r0p - R0m) / sig_tot)
    P(f"  rigid profile, self-consistent start [{foot}]: r_i {ri:.2f} kpc, M(r_i) {Mi:.3e}; R0_pred {r0p:.0f} kpc, Z(frozen sigma) {(r0p - R0m) / sig_tot:+.2f}")
RES["post_hoc"] = PH

# ------------------------------------------------------------------ MUTATE teeth
if MUTATE:
    P("\n== MUTATE ==")
    r0lam = R0_pred_from_tab(TAB, MK)
    check("T1", abs(R0_l0 / R0_cf - 1) < 0.005 and r0lam < R0_l0,
          f"Lambda = 0 R0 {R0_l0:.0f} = closed form {R0_cf:.0f}; with Lambda {r0lam:.0f} (ratio {r0lam / R0_l0:.3f}): Lambda moves R0 inward at fixed M")
    zT2 = [PRED[f]["T2: F-M1 x 0.3"]["Z"] for f in FOOTS]
    check("T2", all(z <= -2 for z in zT2), f"F-M1 x 0.3: Z {zT2[0]:+.2f} / {zT2[1]:+.2f} (must be <= -2, TOO LIGHT)")
    rr0 = abs(np.corrcoef(Rd, Vd)[0, 1]); rs, dl = [], []
    for _ in range(200):
        Rp_ = rng.permutation(Rd)
        rs.append(abs(np.corrcoef(Rp_, Vd)[0, 1]))
        Vm, Sm = model_at(TAB, Rp_)
        lm = np.log(MGRID); k = int(np.argmin(abs(lm - math.log(Mf))))
        var = SGRID[:, None] ** 2 + (Sm[k] * SIG_D * Rp_)[None, :] ** 2
        l_ = np.max(-0.5 * np.sum((Vd - Vm[k]) ** 2 / var + np.log(2 * np.pi * var), axis=1))
        dl.append(lnL0 - l_)
    frac = float(np.mean(np.array(dl) >= 10))
    check("T3", np.median(rs) < 0.2 and frac >= 0.95, f"real |r| {rr0:.2f}; shuffled median |r| {np.median(rs):.2f}; "
          f"Delta lnL >= 10 in {100 * frac:.0f}% of 200 permutations (median {np.median(dl):.1f})")
    RES["MUTATE"] = dict(T1=dict(R0_lam0=R0_l0, R0_lam=r0lam), T2=zT2, T3=dict(r_real=rr0, r_shuf_med=float(np.median(rs)), frac=frac))

# ------------------------------------------------------------------ verdict
P("\n== VERDICT (frozen rules) ==")
lb_ok = all(c["ok"] for c in CHK.values() if c["load_bearing"])
diag = sig_tot / R0m <= 0.116
Zs = {f: PRED[f]["F-M1 shared catchment"]["Z"] for f in FOOTS}


def lab(Z):
    if abs(Z) < 2:
        return "CONSISTENT"
    if Z >= 2:
        return "TOO MASSIVE" + (" (marginal)" if Z < 3 else "")
    return "TOO LIGHT" + (" (marginal)" if Z > -3 else "")


if not diag:
    verdict = "NOT DIAGNOSTIC"
else:
    labs = {f: lab(z) for f, z in Zs.items()}
    if len(set(labs.values())) == 1:
        verdict = labs["canonical"]
    else:
        verdict = min(labs.values(), key=lambda s: ("CONSISTENT" in s, "marginal" in s))
agree = {f: PRED[f]["F-M1 shared catchment"]["agree_timing"] for f in FOOTS}
P(f"  controls (load-bearing) {'all pass' if lb_ok else 'SOME FAIL'}; diagnostic: {diag} (sigma_tot/R0 {sig_tot / R0m:.3f})")
P(f"  F-M1 Z: canonical {Zs['canonical']:+.2f}, alt {Zs['alt']:+.2f} -> {verdict}")
P(f"  R0 weighing vs CFG522 timing mass (F-M1): {'AGREES' if all(agree.values()) else 'DISAGREES'} (M_flow/M = {Mf / MODELS['F-M1 shared catchment']:.3f}, "
  f"2 sigma_lnM band = x{math.exp(-2 * sig_lnM):.2f}-{math.exp(2 * sig_lnM):.2f}); LCDM radial timing mass: "
  f"{'AGREES' if PRED['canonical']['LCDM timing (radial)']['agree_timing'] else 'DISAGREES'} (M_flow/M = {Mf / M_tr:.3f})")
RES["verdict"] = dict(verdict=verdict, Z=Zs, controls_ok=lb_ok, diagnostic=diag, timing_agree=agree)
RES["checks"] = CHK
RES["elapsed_s"] = time.time() - T_START
P(f"\n  elapsed {RES['elapsed_s']:.0f} s")


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


json.dump(clean(RES), open(os.path.join(HERE, f"cfg548_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg548_lg_zvs{SUF}.out"), "w").write("\n".join(LOG) + "\n")
