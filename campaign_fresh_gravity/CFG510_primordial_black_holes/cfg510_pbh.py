#!/usr/bin/env python3
"""CFG510: can the cold energy be primordial black holes? (FROZEN_CRITERIA.md, committed alone first.)
Run: python3 cfg510_pbh.py            -> cfg510_pbh.out, cfg510_pbh_results.json   (exit 0 iff controls K1, K2 pass)
     CFG510_MUTATE=1 python3 cfg510_pbh.py -> *_MUTATE.out / *_MUTATE_results.json (exit 1 iff both teeth detected)
Offline. Every literature bound is RECALLED and UNVERIFIED (no constraint curves on disk). kappa = 1/2 FITTED."""
import os, re, sys, json, math, csv
import numpy as np
TRAPZ = getattr(np, "trapezoid", None) or np.trapz
from math import erfc, sqrt, pi, log10

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG510_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))

G, C, HBAR, KB = 6.674e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23
MSUN, PC = 1.989e30, 3.0857e16; KPC, MPC = 1e3 * PC, 1e6 * PC
GYR = 3.15576e16; TH = 13.8 * GYR; GRAM = 1e-3
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
S_RATIO = 5.364; FB = 1 / (1 + S_RATIO)
h = 0.674; H0 = 100 * h * 1e3 / MPC; RHOC0 = 3 * H0 ** 2 / (8 * pi * G)
OMC = 0.1200 / h ** 2; OMR_H2 = 4.18e-5; OMR = OMR_H2 / h ** 2; A_S = 2.1e-9
def nu(y): y = np.maximum(y, 1e-300); return 1 / (-np.expm1(-np.sqrt(y)))
RES = {}

# =============================== PART A ===============================
P("=" * 100); P("PART A: L49 D1 re-examined in the settled-phantom picture"); P("=" * 100)
l49 = open(os.path.join(REPO, "fable_independent_2026", "L49_minimum_addition.out")).read()
m = re.search(r"\n\s*1\.00\s+([0-9.]+)\s+(-[0-9.]+)\s+\|", l49)
k1_med = float(m.group(2)); k1_fac = 10 ** (-k1_med)
K1 = abs(k1_med + 0.259) < 1e-9 and abs(k1_fac - 1.82) < 0.01
P(f"K1 L49 f=1 row: rms {m.group(1)}, median {k1_med:+.3f} dex -> overshoot x{k1_fac:.3f} (record x1.82): {'PASS' if K1 else 'FAIL'}")
P("   Cause on the record: the MOND kernel is sourced by the TOTAL potential AND the cold mass is placed as an abundance-matched")
P("   NFW halo at f=1, so the kernel amplifies the added mass (double counting). L49 never scored PBH mass windows.")

def host(a, rmin=1e-5, rmax=1e5, n=24001, trunc=None):
    """Dimensionless host: G = M_b = r_M = a0 = 1 (r_M = sqrt(G M_b/a0)). Hernquist baryons, scale a (units r_M)."""
    r = np.logspace(np.log10(rmin), np.log10(rmax), n)
    gb = 1 / (r + a) ** 2; Mb = r ** 2 / (r + a) ** 2
    Mph = r ** 2 * (nu(gb) - 1) * gb
    if trunc is not None:
        Mph = np.where(r <= trunc, Mph, np.interp(trunc, r, Mph))
    return r, Mb, Mph

# A1: accounting identity
r, Mb, Mph = host(0.3)
gobs = (Mb + Mph) / r ** 2; glaw = nu(1 / (r + 0.3) ** 2) / (r + 0.3) ** 2
a1_dev = float(np.max(np.abs(gobs / glaw - 1)))
r_edge = 1 / math.log(1 / (1 - FB))
Mph_edge = float(np.interp(r_edge, r, Mph))
P(f"A1 accounting: max|g(baryons+settled cold)/law(g_b) - 1| = {a1_dev:.1e} (overshoot factor 1 BY CONSTRUCTION, for ANY settled cold matter)")
P(f"   r_edge = r_M/ln(1/(1-f_b)) = {r_edge:.4f} r_M; settled cold inside r_edge = {Mph_edge:.4f} M_b (S = {S_RATIO}; a=0.3 r_M Hernquist)")
P("   -> this is the settling POSTULATE doing the work, not a test (CFG461/462/488/490/494/497: no mechanism supplied).")

def eddington(r, Mtot, rho, eps_eval):
    """Isotropic f(eps) by Eddington, with psi = Phi(r_out) - Phi(r) >= 0 and the boundary term at psi = 0."""
    dPhi = Mtot / r ** 2
    lr = np.log(r)
    Phi = np.concatenate([[0.0], np.cumsum(0.5 * (dPhi[1:] * r[1:] + dPhi[:-1] * r[:-1]) * np.diff(lr))])
    psi = Phi[-1] - Phi
    # derivatives w.r.t. psi (psi decreasing in r)
    drho = np.gradient(rho, r); dpsi = -dPhi
    d1 = drho / dpsi
    d2 = np.gradient(d1, r) / dpsi
    ps = psi[::-1]; d1s = d1[::-1]; d2s = d2[::-1]
    fe = []
    for e in eps_eval:
        t = np.linspace(0, math.sqrt(e), 4001)
        val = TRAPZ(2 * np.interp(e - t ** 2, ps, d2s), t)
        bnd = d1s[0] / math.sqrt(e)
        fe.append((val + bnd) / (math.sqrt(8) * pi ** 2))
    return np.array(fe), psi

# K2: Plummer control (G = M = b = 1)
rp = np.logspace(-4, 5, 24001)
Mp = rp ** 3 / (1 + rp ** 2) ** 1.5; rhop = 3 / (4 * pi) * (1 + rp ** 2) ** -2.5
sel = np.logspace(-1, 1, 15)
psi_ex = 1 / np.sqrt(1 + sel ** 2)
dPhi = Mp / rp ** 2
Phi = np.concatenate([[0.0], np.cumsum(0.5 * (dPhi[1:] * rp[1:] + dPhi[:-1] * rp[:-1]) * np.diff(np.log(rp)))])
psi_num = np.interp(sel, rp, Phi[-1] - Phi)
fp, _ = eddington(rp, Mp, rhop, psi_num)
fan = 24 * math.sqrt(2) / (7 * pi ** 3) * psi_ex ** 3.5
k2_dev = float(np.max(np.abs(fp / fan - 1)))
K2 = k2_dev < 0.02
P(f"K2 Eddington control (Plummer, f ~ eps^3.5): max relative deviation {k2_dev:.2e} over r in [0.1,10] b: {'PASS' if K2 else 'FAIL'}")

P("A2 isotropic collisionless population (PBHs) in the phantom, Eddington inversion. NOTE: in units of r_M the problem is")
P("   independent of M_b and of the footing (g_b/a0 depends only on r/r_M, a/r_M): the 3 masses x 2 footings share one profile per a.")
A2 = {}
for a in (0.3, 1.0):
    for trunc in (None, r_edge):
        r, Mb, Mph = host(a, trunc=trunc)
        rho = np.gradient(Mph, r) / (4 * pi * r ** 2)
        rho = np.maximum(rho, 0.0)
        Mt = Mb + Mph
        dPhi = Mt / r ** 2
        Phi = np.concatenate([[0.0], np.cumsum(0.5 * (dPhi[1:] * r[1:] + dPhi[:-1] * r[:-1]) * np.diff(np.log(r)))])
        psi = Phi[-1] - Phi
        rs = np.logspace(-2, 2, 81)
        eps = np.interp(rs, r, psi)
        fe, _ = eddington(r, Mt, rho, eps)
        ratio = float(fe.min() / np.abs(fe).max())
        ok = ratio >= -1e-3
        neg = rs[fe < -1e-3 * np.abs(fe).max()]
        key = f"a={a}|{'trunc' if trunc else 'untrunc'}"
        A2[key] = dict(min_over_max=ratio, pass_=bool(ok), neg_r_range=[float(neg.min()), float(neg.max())] if len(neg) else None)
        P(f"   a = {a:.1f} r_M, {'truncated at r_edge (reported)' if trunc else 'untruncated (scored)':32s}: min f / max|f| = {ratio:+.3e} -> "
          f"{('f >= 0 everywhere' if ratio >= 0 else 'small negative f WITHIN the -1e-3 tolerance (sharp edge)') + ': an isotropic collisionless population CAN sit in the phantom' if ok else 'NEGATIVE f at r/r_M in ' + str([round(x, 3) for x in A2[key]['neg_r_range']])}")
a2_scored = A2["a=0.3|untrunc"]["pass_"]
# resolution check (reported): half and double radial resolution, a = 0.3 untruncated
for nn in (12001, 48001):
    r_, Mb_, Mph_ = host(0.3, n=nn); rho_ = np.maximum(np.gradient(Mph_, r_) / (4 * pi * r_ ** 2), 0.0); Mt_ = Mb_ + Mph_
    dP_ = Mt_ / r_ ** 2; Ph_ = np.concatenate([[0.0], np.cumsum(0.5 * (dP_[1:] * r_[1:] + dP_[:-1] * r_[:-1]) * np.diff(np.log(r_)))])
    e_ = np.interp(np.logspace(-2, 2, 81), r_, Ph_[-1] - Ph_); f_, _ = eddington(r_, Mt_, rho_, e_)
    A2[f"res_n{nn}"] = float(f_.min() / np.abs(f_).max())
    P(f"   resolution check n = {nn}: min f / max|f| = {A2[f'res_n{nn}']:+.3e}")
P(f"A2 scored cells (a = 0.3 r_M, 3 masses x 2 footings, identical in r_M units): {'PASS (6/6)' if a2_scored else 'FAIL (0/6): needs anisotropy'}")
RES["A"] = dict(K1=dict(median=k1_med, factor=k1_fac, pass_=K1), A1_max_dev=a1_dev, r_edge=r_edge, Mph_edge=Mph_edge,
                K2_dev=k2_dev, K2=K2, A2=A2, A2_scored_pass=a2_scored)

# A3: granularity
P("A3 PBH granularity: mass at which two-body relaxation (t_rlx = 0.1 N/lnN t_cross) or dynamical friction from r equals 13.8 Gyr")
def fnum(v):
    try: x = float(v); return x if np.isfinite(x) else None
    except (TypeError, ValueError): return None
rows = list(csv.DictReader(open(os.path.join(REPO, "real_research/data/dsph/lvd_dwarf_mw.csv"))))
UFD = []
for rw in rows:
    MV = fnum(rw["M_V"]); sig = fnum(rw["vlos_sigma"]); ul = fnum(rw["vlos_sigma_ul"])
    rh = fnum(rw["rhalf_sph_physical"]) or fnum(rw["rhalf_physical"]); Dh = fnum(rw["distance_host"]) or fnum(rw["distance_gc"])
    if MV is None or rh is None or MV <= -7.7 or Dh is None: continue
    if sig is not None and ul is None and sig > 0:
        mhi = 10 ** fnum(rw["mass_HI"]) if fnum(rw["mass_HI"]) is not None else 0.0
        UFD.append(dict(name=rw["name"], LV=10 ** (0.4 * (4.83 - MV)), rh=rh, sig=sig, MHI=mhi))
def solveN(target):  # 0.1 N/lnN = target
    lo, hi = 2.0, 1e80
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if 0.1 * mid / math.log(mid) < target: lo = mid
        else: hi = mid
    return mid
ufd_rows = []
for d in UFD:
    Mb = 2 * d["LV"] + 1.33 * d["MHI"]; rr = 4 / 3 * d["rh"] * PC; s = d["sig"] * 1e3
    Mdyn = 3 * s ** 2 * rr / G / MSUN; Mc = Mdyn - 0.5 * Mb; fc = Mc / Mdyn
    if fc < 0.5: continue
    tcr = rr / (math.sqrt(3) * s); N = solveN(TH / tcr); m_rlx = Mc / N
    Vc = math.sqrt(2) * s; m_df = 1.17 * rr ** 2 * Vc / (G * 10 * TH) / MSUN
    rho = Mc * MSUN / (4 / 3 * pi * rr ** 3)
    m_heat = (math.sqrt(3) * s) ** 3 / (4 * math.sqrt(2) * pi * G ** 2 * rho * 10 * 10 * GYR) / MSUN   # D3 (3-D sigma, see README)
    m_heat1 = s ** 3 / (4 * math.sqrt(2) * pi * G ** 2 * rho * 10 * 10 * GYR) / MSUN                    # 1-D sigma variant
    ufd_rows.append(dict(name=d["name"], Mc=Mc, fc=fc, r_pc=rr / PC, sig=d["sig"], m_rlx=m_rlx, m_df=m_df, m_heat=m_heat, m_heat_1d=m_heat1,
                         rho_Msun_pc3=rho / MSUN * PC ** 3))
mr = np.array([u["m_rlx"] for u in ufd_rows]); md = np.array([u["m_df"] for u in ufd_rows])
P(f"   {len(ufd_rows)} MW UFDs, resolved and cold-dominated (f_cold >= 0.5, settled ontology: M_dyn - M_b is real cold mass)")
P(f"   UFD m_rlx: min {mr.min():.2e}, median {np.median(mr):.2e} Msun | m_df: min {md.min():.2e}, median {np.median(md):.2e} Msun")
disc = []
for lM in (9.0, 10.5, 11.5):
    for foot, a0 in A0.items():
        Mb = 10 ** lM * MSUN; rM = math.sqrt(G * Mb / a0); a = 0.3 * rM
        gb = G * Mb / (rM + a) ** 2; V = math.sqrt(float(nu(gb / a0)) * gb * rM)
        Mc = rM ** 2 * (float(nu(gb / a0)) - 1) * gb / G / MSUN
        tcr = rM / V; N = solveN(TH / tcr); m_rlx = Mc / N
        m_df = 1.17 * rM ** 2 * V / (G * 10 * TH) / MSUN
        disc.append(dict(logMb=lM, footing=foot, r_M_kpc=rM / KPC, V_kms=V / 1e3, Mc_rM=Mc, m_rlx=m_rlx, m_df=m_df))
        P(f"   disc host logM_b {lM:4.1f} {foot:9s}: r_M {rM/KPC:6.2f} kpc, V {V/1e3:6.1f} km/s, settled cold <r_M {Mc:.2e} Msun -> m_rlx {m_rlx:.2e}, m_df {m_df:.2e} Msun")
m_gran = float(min(mr.min(), md.min(), min(x["m_rlx"] for x in disc), min(x["m_df"] for x in disc)))
WIN_TOP_G = 1e22
gap_dex = log10(m_gran * MSUN / (WIN_TOP_G * GRAM))
A3 = gap_dex >= 3
P(f"A3 smallest granularity mass {m_gran:.2e} Msun = {m_gran*MSUN/GRAM:.2e} g; above the window top (1e22 g) by {gap_dex:.1f} dex -> "
  f"{'granularity IRRELEVANT in the window (PBHs there are a smooth collisionless fluid on every galactic scale)' if A3 else 'granularity MATTERS'}")
P("   Relaxation as the settling MECHANISM would need m >= m_rlx, i.e. masses Part B excludes (UFD heating, dynamics): not available.")
P("A4 settling routes open to PBHs: FL1 superfluid pressure NO (no pressure); CFG490 direct phonon coupling NO (a black hole")
P("   carries no baryon/phonon charge; G9 holds automatically); CFG381 khronon +1 coupling ONLY via black-hole 'sensitivities' in")
P("   khronometric gravity (recalled, NOT computed); two-body relaxation ONLY above m_rlx (excluded). PBHs have FEWER routes than a field.")
partA = "DISAPPEARS CONDITIONALLY (settling postulate)" if (K1 and A3) else "SURVIVES"
if K1 and A3 and not a2_scored: partA += " + needs anisotropy"
P(f"PART A VERDICT: x1.82 -> {partA}. Not RESOLVED: no settling mechanism is supplied on the record, and PBHs close two of its routes.")
RES["A"].update(UFD=ufd_rows, discs=disc, m_gran_Msun=m_gran, gap_dex=gap_dex, A3=A3, verdict=partA)

# =============================== PART B ===============================
P(); P("=" * 100); P("PART B: f_PBH = 1 mass window (bands RECALLED, UNVERIFIED; no constraint curves on disk)"); P("=" * 100)
Ms_g = MSUN / GRAM
ROBUST = [("E1 evaporation (CMB anis., EG gamma, Voyager e+-, 511 keV)", 1e5, 1e17),
          ("E2 HSC/M31 microlensing", 1e22, 1e-6 * Ms_g),
          ("E3 EROS/MACHO", 1e-7 * Ms_g, 30 * Ms_g),
          ("E4 OGLE", 1e-6 * Ms_g, 1e-2 * Ms_g),
          ("E5 UFD / star-cluster heating", 5 * Ms_g, 1e60),
          ("E6 wide binaries", 30 * Ms_g, 1e60),
          ("E7 CMB accretion (spherical)", 100 * Ms_g, 1e60),
          ("E8 LVK merger rate", 0.5 * Ms_g, 300 * Ms_g),
          ("E9 Lyman-alpha Poisson", 60 * Ms_g, 1e60),
          ("E10 disc heating / dyn. friction", 1e6 * Ms_g, 1e60),
          ("E11 incredulity / one per volume", 1e21 * Ms_g, 1e80)]
MAXIMAL = [(n, lo, hi) for n, lo, hi in ROBUST]
MAXIMAL[0] = ("E1' evaporation (claimed extension)", 1e5, 4e17)
MAXIMAL[1] = ("E2' HSC (claimed lower edge)", 3e21, 1e-6 * Ms_g)
MAXIMAL[6] = ("E7' CMB accretion (disc)", 1 * Ms_g, 1e60)
def score(mg, bands):
    hit = [n for n, lo, hi in bands if lo <= mg <= hi]
    return ("EXCLUDED", hit) if hit else ("OPEN", [])
def windows(bands):
    grid = 10 ** np.arange(10, 55.0001, 0.01)
    op = np.array([score(x, bands)[0] == "OPEN" for x in grid])
    out = []; i = 0
    while i < len(grid):
        if op[i]:
            j = i
            while j + 1 < len(grid) and op[j + 1]: j += 1
            out.append((float(grid[i]), float(grid[j]), float(log10(grid[j] / grid[i])))); i = j + 1
        else: i += 1
    return out
WR = windows(ROBUST); WM = windows(MAXIMAL)
for nm, W in (("robust", WR), ("maximal", WM)):
    P(f"   open windows ({nm}): " + "; ".join(f"{lo:.2e} - {hi:.2e} g ({w:.2f} dex)" for lo, hi, w in W))
winR = [w for w in WR if w[2] >= 1]; winM = [w for w in WM if w[2] >= 1]
P(f"   >= 1 dex window on BOTH sets: {'YES' if winR and winM else 'NO'}")

P("D-checks (derived; a > 1 dex disagreement flags the band UNSUPPORTED BY DERIVATION, nothing is moved):")
# D1 Hawking
Mevap = (TH * HBAR * C ** 4 / (5120 * pi * G ** 2)) ** (1 / 3)
TH_17 = HBAR * C ** 3 / (8 * pi * G * 1e17 * GRAM * KB) * KB / 1.602e-16   # keV
P(f"   D1 naive (photon-only 5120 pi) lifetime = 13.8 Gyr at M = {Mevap/GRAM:.2e} g (recalled full-species value ~5e14 g);")
P(f"      T_H(1e17 g) = {TH_17:.1f} keV: emission today in hard X / soft gamma (511 keV, MeV), consistent with E1's edge being an")
P(f"      EMISSION bound >> the lifetime mass. E1 edge not derivable without data: NO D-CHECK (stays recalled).")
# D2 microlensing lower edge
lam = 6.2e-7
Mw = C ** 2 * lam / (8 * pi * G)
def Mfs(Rs, Ds, Dl):
    Dls = Ds - Dl; return Rs ** 2 * C ** 2 * Dl / (4 * G * Ds * Dls)
Rsun = 6.957e8
fs_m31 = Mfs(Rsun, 770 * KPC, 720 * KPC); fs_mw = Mfs(Rsun, 770 * KPC, 20 * KPC)
d2_dex = log10(min(fs_m31, fs_mw) / GRAM / 1e22)
d2_flag = abs(log10(Mw / GRAM / 1e22)) > 1 and d2_dex > 1
P(f"   D2 wave-optics edge (w = 8 pi G M/(c^2 lambda) = 1, r-band): {Mw/GRAM:.2e} g ({log10(Mw/GRAM/1e22):+.2f} dex from E2's 1e22 g) -> supports E2's edge")
P(f"      finite-source edge (R_E in source plane = R_sun): M31-halo lens {fs_m31/GRAM:.2e} g, MW-halo lens {fs_mw/GRAM:.2e} g")
P(f"      ({d2_dex:+.1f} dex above 1e22 g for Sun-size sources: the recalled edge needs sources smaller than the Sun or")
P(f"      small-magnification detections; the derivation, if anything, WIDENS the window upward). E2 lower edge: SUPPORTED by wave")
P(f"      optics, QUESTIONED by finite source -> flagged 'finite-source caveat'; scoring keeps the narrower recalled edge.")
# D3 UFD heating
mh = np.array([u["m_heat"] for u in ufd_rows]); mh1 = np.array([u["m_heat_1d"] for u in ufd_rows])
d3_med = float(np.median(mh)); d3_dex = log10(d3_med / 5)
P(f"   D3 UFD star heating (record UFDs, real cold mass, lnL 10, 10 Gyr): median m_max {d3_med:.2f} Msun (1-D sigma variant "
  f"{np.median(mh1):.2f}); most constraining {np.sort(mh)[:3].round(2).tolist()} Msun; vs E5's 5 Msun: {d3_dex:+.2f} dex -> "
  f"{'SUPPORTED' if abs(d3_dex) <= 1 else 'UNSUPPORTED BY DERIVATION'}")
# D4 LVK
R_obs = (17, 45)
d4 = {}
for mm in (1, 10, 30, 100, 300):
    d4[mm] = 1.6e6 * mm ** (-32 / 37) * 1e-3
m_eq = (1.6e6 * 1e-3 / R_obs[1]) ** (37 / 32)
d4_dex = log10(300 / m_eq)
P("   D4 LVK rate at f = 1 (recalled Sasaki-type 1.6e6 Gpc^-3/yr m^-32/37, x1e-3 suppression, also recalled): " +
  ", ".join(f"{k} Msun {v:.1e}" for k, v in d4.items()) + f" vs observed {R_obs[0]}-{R_obs[1]} (recalled)")
P(f"      derived f=1 exclusion reaches only m <= {m_eq:.0f} Msun (rate = 45); E8's 300 Msun edge is {d4_dex:+.2f} dex beyond -> "
  f"{'SUPPORTED within the 1-dex rule' if abs(d4_dex) <= 1 else 'UNSUPPORTED BY DERIVATION'}; the 1e-3 suppression factor dominates (rates")
P("      at 30-300 Msun are within ~0.5 dex of observed). Above ~60 Msun E5/E6/E7/E9 cover the band anyway.")
# D5 isocurvature on CMB scales
k05 = 0.05 / MPC
iso = {}
for mg in (1e17, 1e20, 1e22):
    n = OMC * RHOC0 / (mg * GRAM)                # comoving number density (per m^3)
    iso[mg] = k05 ** 3 / (2 * pi ** 2 * n) / A_S
P("   D5 Poisson isocurvature at k = 0.05/Mpc, Delta^2_S / A_s: " + ", ".join(f"{k:.0e} g {v:.1e}" for k, v in iso.items()) +
  " -> utterly negligible (adiabatic on CMB scales)")
flags = {"E2": "finite-source caveat (derivation would widen the window)", "E5": "SUPPORTED" if abs(d3_dex) <= 1 else "UNSUPPORTED",
         "E8": "SUPPORTED" if abs(d4_dex) <= 1 else "UNSUPPORTED"}

P("FM1 dynamical bounds in the settled ontology: the phantom is REAL cold mass (CFG447 excludes the force reading), so")
P("    UFD heating, wide binaries and disc heating apply at FULL strength (D3 used real M_dyn - M_b). No relief, no tightening.")
# FM2 optical depth
def los(l, b, L, R0=8.2, n=4000):
    D = np.linspace(1e-3, L, n); lr, br = math.radians(l), math.radians(b)
    x = R0 - D * math.cos(br) * math.cos(lr); y = D * math.cos(br) * math.sin(lr); z = D * math.sin(br)
    return D, np.sqrt(x ** 2 + y ** 2 + z ** 2)
def rho_settled(rkpc, Mb, a0, frac_a=0.3):
    rM = math.sqrt(G * Mb * MSUN / a0) / KPC; a = frac_a * rM; re = rM * r_edge
    rr = np.maximum(rkpc, 1e-4)
    def Mph(x):
        gb = G * Mb * MSUN / ((x + a) * KPC) ** 2
        return (x * KPC) ** 2 * (nu(gb / a0) - 1) * gb / G / MSUN
    dr = 1e-4 * rr
    rho = (Mph(rr + dr) - Mph(rr - dr)) / (2 * dr) / (4 * pi * rr ** 2)     # Msun/kpc^3
    rho = np.where(rr <= re, rho, 0.0)
    return rho + OMC * RHOC0 / MSUN * KPC ** 3                 # + smooth unsettled reservoir at the cosmic mean
def rho_nfw(rkpc, M200, c=10.0):
    r200 = (3 * M200 * MSUN / (4 * pi * 200 * RHOC0)) ** (1 / 3) / KPC; rs = r200 / c
    dc = 200 / 3 * c ** 3 / (math.log(1 + c) - c / (1 + c)); x = np.maximum(rkpc, 1e-4) / rs
    return dc * RHOC0 / MSUN * KPC ** 3 / (x * (1 + x) ** 2)
def tau(D, rho, L):  # rho Msun/kpc^3, D kpc
    return 4 * pi * G / C ** 2 * TRAPZ(rho * MSUN / KPC ** 3 * (D * KPC) * ((L - D) * KPC) / (L * KPC), D * KPC)
FM2 = {}
for foot, a0 in A0.items():
    D, rg = los(280.5, -32.9, 50.0)
    tS = tau(D, rho_settled(rg, 6e10, a0), 50.0); tN = tau(D, rho_nfw(rg, 1e12), 50.0)
    D2, rg2 = los(121.2, -21.6, 770.0)
    tSm = tau(D2, rho_settled(rg2, 6e10, a0), 770.0); tNm = tau(D2, rho_nfw(rg2, 1e12), 770.0)
    s = np.linspace(-400, 0, 4000); bimp = 5.0; r31 = np.sqrt(bimp ** 2 + s ** 2)
    def tau31(rho):
        Dls = -s * KPC; Dl = (770 + s) * KPC
        return 4 * pi * G / C ** 2 * TRAPZ(rho * MSUN / KPC ** 3 * Dl * Dls / (770 * KPC), s * KPC)
    t31S = tau31(rho_settled(r31, 1.5e11, a0)); t31N = tau31(rho_nfw(r31, 1.5e12))
    rloc_S = float(rho_settled(np.array([8.2]), 6e10, a0)[0]) / 1e9; rloc_N = float(rho_nfw(np.array([8.2]), 1e12)[0]) / 1e9
    FM2[foot] = dict(LMC_settled=tS, LMC_nfw=tN, LMC_ratio=tS / tN, M31_settled=tSm + t31S, M31_nfw=tNm + t31N,
                     M31_ratio=(tSm + t31S) / (tNm + t31N), rho_local_settled=rloc_S, rho_local_nfw=rloc_N)
    P(f"FM2 {foot:9s}: tau(LMC) settled {tS:.2e} / NFW {tN:.2e} = {tS/tN:.2f}; tau(M31, b=5 kpc) settled {tSm+t31S:.2e} / NFW {tNm+t31N:.2e}"
      f" = {(tSm+t31S)/(tNm+t31N):.2f}; local cold density settled {rloc_S:.4f} vs NFW {rloc_N:.4f} Msun/pc^3")
fm2_ok = all(0.5 <= FM2[f][k] <= 2 for f in A0 for k in ("LMC_ratio", "M31_ratio"))
P(f"FM2 verdict: {'ratios in [0.5, 2] -> microlensing bands UNCHANGED' if fm2_ok else 'a ratio outside [0.5, 2] -> microlensing band edges FLAGGED (amplitude changes; edges in mass move little)'}")
P("    (MW baryons 6e10, M31 1.5e11 Msun Hernquist; NFW 1e12 / 1.5e12, c = 10: recalled inputs; phantom disc NOT computed)")
RES["B"] = dict(robust=ROBUST, maximal=MAXIMAL, windows_robust=WR, windows_maximal=WM, D1_Mevap_naive_g=Mevap / GRAM,
                D1_TH_1e17_keV=TH_17, D2_Mwave_g=Mw / GRAM, D2_Mfs_M31_g=fs_m31 / GRAM, D2_Mfs_MW_g=fs_mw / GRAM,
                D3_median_Msun=d3_med, D3_dex=d3_dex, D4=d4, D5=iso, flags=flags, FM2=FM2, FM2_ok=fm2_ok)

# =============================== PART C ===============================
P(); P("=" * 100); P("PART C: formation (power-spectrum spike) and the amount"); P("=" * 100)
GS, GS0, GSS0 = 106.75, 3.36, 3.91
Gf = (GS / GS0) * (GSS0 / GS) ** (4 / 3)
gam = 0.2
def form(Mpbh_g):
    MH = Mpbh_g * GRAM / gam
    H = C ** 3 / (2 * G * MH)
    af = math.sqrt(H0 * math.sqrt(OMR * Gf) / H)
    k = af * H / C
    rho = 3 * H ** 2 / (8 * pi * G)
    T = (rho * C ** 2 * 30 / (pi ** 2 * GS) * (HBAR * C) ** 3) ** 0.25 / 1.602e-10   # GeV
    beta = (OMC / OMR) * af / Gf
    return dict(MH_g=MH / GRAM, k_Mpc=k * MPC, f_Hz=C * k / (2 * pi), T_GeV=T, t_s=1 / (2 * H), beta=beta)
def sig_for(beta, dc):
    lo, hi = 1e-4, 10.0
    for _ in range(200):
        s = math.sqrt(lo * hi)
        if gam * erfc(dc / (math.sqrt(2) * s)) < beta: lo = s
        else: hi = s
    return s
FORM = {}
for mg in (1e17, 1e18, 1e19, 1e20, 1e21, 1e22):
    fm = form(mg)
    for dc in (0.41, 0.45, 0.55):
        s = sig_for(fm["beta"], dc); Pz = 81 / 16 * s ** 2
        x = dc / (math.sqrt(2) * s); dlnf = 2 * x * math.exp(-x * x) / (math.sqrt(pi) * erfc(x)) * 0.5   # d ln f / d ln sigma^2 ... /2 -> per ln P
        fm[f"dc{dc}"] = dict(sigma=s, Pzeta=Pz, ratio_As=Pz / A_S, dlnf_dlnP=dlnf, dP_for_1pct=0.01 / dlnf)
    FORM[mg] = fm
    d = fm["dc0.45"]
    P(f"   M {mg:.0e} g: k {fm['k_Mpc']:.2e}/Mpc, T_form {fm['T_GeV']:.2e} GeV, t {fm['t_s']:.1e} s, beta {fm['beta']:.2e}; "
      f"dc 0.45 -> P_zeta {d['Pzeta']:.3f} ({d['ratio_As']:.1e} x A_s), d ln f/d ln P {d['dlnf_dlnP']:.1f}, "
      f"1% amount needs P_zeta to {100*d['dP_for_1pct']:.2f}%")
kmin = min(FORM[m]["k_Mpc"] for m in FORM)
compat = kmin > 1e5 and max(iso.values()) < 1e-3
P(f"   spike scale k >= {kmin:.1e}/Mpc (CMB/LSS k <~ 1, mu-distortion 1-1e4/Mpc: recalled) and isocurvature negligible -> "
  f"{'COMPATIBLE with the CMB adiabatic, near scale-invariant spectrum (needs a feature ~7 orders up at k >~ 1e12/Mpc)' if compat else 'INCOMPATIBLE'}")
Tmin = min(FORM[m]["T_GeV"] for m in FORM)
P(f"   formation T >= {Tmin:.1e} GeV >> electroweak 1e2 GeV: the PBH amount is set before (and independently of) baryogenesis;")
P("   Omega_c/Omega_b = 5.364 would then be a coincidence of the spike amplitude and eta_b. AMOUNT: RESTATEMENT (moved into P_zeta,")
P("   which must be tuned to ~0.03% and placed by hand in k). With critical-collapse/non-Gaussian corrections the numbers move, the verdict does not.")
amount = "RESTATEMENT"
RES["C"] = dict(form={str(k): v for k, v in FORM.items()}, compatible=compat, amount=amount, gamma=gam, gstar=GS)

# =============================== PART D ===============================
P(); P("=" * 100); P("PART D: distinctive predictions if PBHs = cold energy in the window"); P("=" * 100)
SIGW = {}
for mg in (1e17, 1e19, 1e20, 1e22):
    fm = FORM[mg]; Pz = fm["dc0.45"]["Pzeta"]
    Om = 0.39 * (GS / 106.75) ** (-1 / 3) * OMR_H2 * Pz ** 2
    SIGW[mg] = dict(f_Hz=fm["f_Hz"], OmGWh2=Om)
    P(f"   SIGW: M {mg:.0e} g -> peak f ~ {fm['f_Hz']:.1e} Hz, Omega_GW h^2 ~ {Om:.1e} (LISA ~1e-12 at mHz, recalled; band 1e-4-1e-1 Hz)")
P("   -> LISA/TianQin/Taiji (and DECIGO/BBO toward 1 Hz) see a stochastic background ~1e3-1e4 above sensitivity, or rule out")
P("      Gaussian-adiabatic PBH formation over most of the window (non-Gaussian spikes lower Omega_GW; recalled caveat).")
def crit_frac(Mf, cut):
    lm = np.linspace(np.log(Mf) - 40, np.log(Mf) + 5, 20000); M = np.exp(lm); gc = 0.36
    psi = (M / Mf) ** (1 + 1 / gc) * np.exp(-(M / Mf) ** (1 / gc))   # mass function per ln M (recalled form)
    return float(TRAPZ(psi * (M < cut), lm) / TRAPZ(psi, lm))
TAIL = {}
for Mf in (2e17, 1e18, 1e19, 1e20):
    TAIL[Mf] = dict(below_1e17=crit_frac(Mf, 1e17), below_1e16=crit_frac(Mf, 1e16))
    P(f"   Hawking tail (critical collapse, gamma_c 0.36): M_f {Mf:.0e} g -> mass fraction < 1e17 g {TAIL[Mf]['below_1e17']:.1e}, < 1e16 g {TAIL[Mf]['below_1e16']:.1e}")
P("   -> near the low edge, the tail glows in 511 keV / MeV gamma rays (T_H ~ 100 keV at 1e17 g): COSI-class MeV data tests it.")
rho_loc = FM2["canonical"]["rho_local_settled"] * MSUN / PC ** 3
v = 250e3; b = 1.496e11; FLY = {}
for mg in (1e17, 1e20, 1e22):
    n = rho_loc / (mg * GRAM); rate = n * pi * b ** 2 * v * 3.156e7 * (1 + (42.1e3 / v) ** 2)
    dv = 2 * G * mg * GRAM / (b * v); dx = dv * 10 * 3.156e7
    FLY[mg] = dict(rate_per_yr_1AU=rate, dv_ms=dv, dx_10yr_m=dx)
    P(f"   flybys: M {mg:.0e} g -> {rate:.1e} per yr within 1 AU; impulse at 1 AU {dv:.1e} m/s; displacement after 10 yr {dx:.1e} m")
P("   -> 1e21-1e22 g PBHs perturb inner-planet ranging at the cm-m level per decade (a recalled proposal; ephemeris data needs a go).")
P(f"   microlensing: the wave-optics edge ({Mw/GRAM:.1e} g) predicts chromatic, sub-geometric magnification for M31/HSC-type events at")
P("      1e22-1e23 g; deeper/faster cadence or smaller (main-sequence) sources push into the window.")
RES["D"] = dict(SIGW={str(k): v for k, v in SIGW.items()}, tail={str(k): v for k, v in TAIL.items()}, flybys={str(k): v for k, v in FLY.items()})

# =============================== VERDICT ===============================
P(); P("=" * 100)
window = bool(winR and winM)
if not window: overall = "EXCLUDED (no >= 1 dex open window)"
elif partA.startswith("RESOLVED"): overall = "VIABLE"
else: overall = "VIABLE-CONDITIONAL"
P(f"OVERALL: {overall}; AMOUNT: {amount}")
P(f"  window (robust) {winR[0][0]:.1e}-{winR[0][1]:.1e} g, (maximal) {winM[0][0]:.1e}-{winM[0][1]:.1e} g; conditions: (1) the settling postulate (no mechanism; PBHs close FL1 and the phonon arm);")
P("  (2) the recalled band edges (curves need the owner's go); (3) a spike P_zeta ~ 0.015-0.02 (tuned to ~0.03%) at k ~ 1e12-1e14/Mpc;")
P(f"  (4) A2: {'isotropic equilibrium exists (no anisotropy condition)' if a2_scored else 'needs anisotropy'}.")
P("  kappa = 1/2 FITTED; the cold energy's mass is still required (PBHs supply it without a new particle); not theory closed.")
RES["overall"] = dict(verdict=overall, amount=amount, window=window)

# =============================== MUTATE ===============================
if MUT:
    P(); P("MUTATE teeth:")
    q = {"1 Msun": 1 * Ms_g, "1e-9 Msun": 1e-9 * Ms_g, "1e15 g": 1e15, "1e4 Msun": 1e4 * Ms_g}
    t1 = all(score(x, ROBUST)[0] == "EXCLUDED" and score(x, MAXIMAL)[0] == "EXCLUDED" for x in q.values())
    for k_, x in q.items(): P(f"   {k_:10s}: {score(x, ROBUST)[0]} by {score(x, ROBUST)[1]}")
    MB = [(n, lo, hi) for n, lo, hi in ROBUST]; MB[1] = ("E2 HSC moved to 1e17 g (MUTATE)", 1e17, 1e-6 * Ms_g)
    Wm = windows(MB); t2 = not any(w[2] >= 1 for w in Wm)
    P(f"   HSC lower edge -> 1e17 g: windows {[(f'{a:.1e}', f'{b_:.1e}', round(w, 2)) for a, b_, w in Wm]} -> "
      f"{'no >= 1 dex window -> OVERALL EXCLUDED (by E1 evaporation meeting the moved E2 HSC band)' if t2 else 'window still open'}")
    RES["MUTATE"] = dict(t1=t1, t2=t2)
    P(f"MUTATE: {'both teeth detected (exit 1)' if (t1 and t2) else 'NOT detected'}")
json.dump(RES, open(os.path.join(HERE, f"cfg510_pbh{TAG}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg510_pbh{TAG}.out"), "w").write("\n".join(OUT) + "\n")
if MUT: sys.exit(1 if (RES["MUTATE"]["t1"] and RES["MUTATE"]["t2"]) else 0)
sys.exit(0 if (K1 and K2) else 1)
