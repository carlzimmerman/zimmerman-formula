#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE8 -- KiDS-1000 WITH THE REGION KERNEL'S WEB SELF-TERM sigma AS A LABELLED AXIS, ON BOTH SWITCH BRANCHES.

WHY.  V0 (CV1/CV2, real_research/chk_v0_2026/) takes L361's region operator with the web self-term sigma = 1.  CV1's A5
showed that sigma moves the baryon force inside a region's edge layer by ~1 g_N.  Every committed KiDS score so far
(L352, L360, AT3's hard edge, L361 R3 edgeless) and L370's Harvey runs used sigma = 0.  The sigma = 1 edge layer's
lensing has never been scored.  A 3-d sigma = 1 Harvey operator lane is waiting on this verdict.  The user's
"all doors" asks for every branch and reading to be scored and labelled separately, never pooled.

THE MODEL (L361/CV1's operator, solved exactly as radial ODEs on L352's own grid; SI units)
  (lap - M^2) w = 4 pi G f rho_b,                  M^2 = m^2 (1 - f)          the gated, screened baryon field
  (lap - M^2) P = div[f (nu_mono(|w'|/a0) - 1) grad w] + sigma M^2 w           the gated phantom
  lensing = dynamics on Phi = u + f P,  lap u = 4 pi G rho_all               (CV1: baryons and light feel Phi)
  so M_lens(<r) = M_all(<r) + r^2 (f P)'/G.  The edge-layer term f' P is included.  sigma enters only where 0 < f < 1
  and M > 0.  Baryons: L352's point mass M_b = 10^lm (the kernel's source and the lensing mass), with Hernquist
  (a = 3 kpc (M_b/1e11)^0.3) for the matter density a switch reads.  The carrier: L360's post-decay template for each
  L357 cell ((1 - f_b) NFW of the bin's Moster host, cleared or capped at the trigger density), amplitude 1 (L360's
  criterion).  It is kernel-invisible (Newtonian only) but gravitates and is read by the switch.  Its OUTER PROFILE is an
  axis, labelled per cell: 'r200' = L360's template, cut at r200; 'nfw' = the host NFW continued (the gate reads, and
  the lens carries, the same density).  With a cut carrier the matter-only edge sits AT r200 and the gate is a hard
  step there -- a convention, flagged by the merger lane (L392), not physics.
  The gate: f = W(t) (Mathlib's smoothTransition), t = (x/x_c,eff - 1)/(2w) + 1/2, x = 4 pi G (rho - rho_bar)/H(z)^2 at
  z_l = 0.25, x_c,eff = x_c0 E(0.25)^(2p); f = 0 beyond the first radius where t <= 0 (the region connected to the centre):
    UPPER (curvature) branch: rho = the ungated dynamical density (stars' QUMOND phantom + carrier), L352's on-branch
                              convention;
    LOWER (matter-only) branch, contrast reading: rho = Hernquist stars + carrier;
    LOWER, absolute reading: x = (3/2) Omega_m(z) rho/rho_bar (L342's).
  The fit: L352's KiDS machinery, loaded unedited: the four Brouwer+21 bins with full covariance, M_b profiled per bin,
  the linear 2-halo term free per bin, exact annulus averages.  The pass criterion is L352's/L360's:
  Delta chi^2 <= +4 against the unswitched model, both footings.

CHECKS
  C0 CONTROL: this lane's projection matrix reproduces L352's project_M2 exactly (1e-10).
  C1 CONTROL: with f = 1 (no gate, no screening) the ODE solve reproduces L352's isolated QUMOND ESD (0.5% per point,
     every bin) and its KiDS score (|Delta chi^2| < 0.5).
  C2 CONTROL: a hard upper-branch edge (L352's on-branch convention, no carrier) with sigma = 0 in the Dirichlet limit
     (1/m = 1 kpc) reproduces L352's compensated ESD (2% of the peak): L352's compensated profile IS the operator's
     sigma = 0 hard-edge limit.
  C3 CONTROL: with C2's settings plus L360's carrier template, L360's committed score for the pair (p = 1, x_c0 = 2.5) +
     (p = 1, cap, x_v0 = 700) is reproduced (|dDelta chi^2| <= 1.5 per footing).
  C3b CONTROL: L352's own compensated ESD plus this lane's carrier template reproduces L360's committed score exactly
     (1e-6): the carrier template is L360's.
  S1 [load-bearing] sigma is exercised: at 1/m = 0.1 Mpc, w = 1, the sigma = 1 and sigma = 0 ESDs differ somewhere by
     more than 1e-3 Msun/pc^2.
  H1 [pre-declared hypothesis, load-bearing] sigma is a sub-dominant axis for KiDS: |Delta chi^2(sigma = 1) -
     Delta chi^2(sigma = 0)| <= 4 in every cell (branch, switch cell, carrier, 1/m, w, footing).  [The first trial run
     scored only the r200 convention and FAILED this (max 93, on the matter-only branches, whose r200 edges are hard);
     the outer-profile axis was added after it, so H1 is kept exactly as declared and scored over every cell.]
  V1 [reported] the verdict per branch: which cells pass at sigma = 0 and at sigma = 1, and whether sigma = 1 passes
     wherever sigma = 0 does.
MUTATE=1 sets sigma = 0 in the sigma = 1 cells: S1 must FAIL (rc = 1).

SCOPE.  Spherical, isolated lenses, static.  Point-mass baryons with no CGM (L360's convention).  The upper branch reads
the ungated phantom (the on-branch convention; the smooth gate's self-consistent profile is not iterated).  The heat
filter is omitted: it acts below 0.05 pc.  The gate is L359's switch form at z_l = 0.25 only; the carrier's amplitude is
fixed at 1.

Run from the repository root:  python3 real_research/dark_energy_2026/DE8_kids_sigma_axis_both_branches.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from scipy.linalg import solve_banded
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE8_kids_sigma_axis_both_branches"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE8", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("CHECKS")[0].strip())
if MUTATE: P("\n  *** MUTATE=1: sigma is set to 0 in the sigma = 1 cells; S1 must FAIL ***")

# ---------------------------------------------------------------------------------- L352's KiDS machinery, unedited
P52 = os.path.join(REPO, "real_research", "g03_audit_2026", "L352_switch_gauss_compensation.py")
L52 = {"__name__": "l352", "__file__": P52}
_src = open(P52).read().split("real_mode = ")[0].replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False")
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, L52)
(fit_model, esd_bin, twoh_cache, LM, Ed, Sd, Ci, A0, project_M2, annulus_esd, rr, Rp, MS, Om, OL, rho_crit0, Rd, nu_vec,
 Hz, G, MPCm, KPC_, _trap) = [L52[k] for k in ("fit_model", "esd_bin", "twoh_cache", "LM", "Ed", "Sd", "Ci", "A0", "project_M2",
                                              "annulus_esd", "rr", "Rp", "MS", "Om", "OL", "rho_crit0", "Rd", "nu_vec",
                                              "Hz", "G", "MPCm", "KPC", "_trap")]
h = 0.6736; FB = 0.02237 / (0.02237 + 0.1200)
ZL = 0.25
M200_BINS = [4.17e11, 8.97e11, 1.91e12, 5.55e12]                     # L360's Moster+13 hosts of the four bins
rhoc_zl = rho_crit0 * (Om * (1 + ZL) ** 3 + OL)
rho_bar = Om * rho_crit0 * (1 + ZL) ** 3
c200 = lambda M: 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h)))
mfn = lambda x: np.log(1 + x) - x / (1 + x)
E2L = lambda z: Om * (1 + z) ** 3 + OL                                # L360's E(z)^2 (its carrier trigger)
E2G = lambda z: 0.3138 * (1 + z) ** 3 + 0.6862                        # L359's gate background (DE1-DE7)
H_L = Hz(ZL)
P(f"  L352 KiDS machinery loaded (grid {len(rr)} radii, {len(Rp)} projected radii)   [{time.time() - T0:.0f}s]")
R59 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L359_vacuum_gated_switch_results.json")))
XE59 = {(float(k_.split("/")[0]), float(k_.split("/")[1])): v_["x_eff"] for k_, v_ in R59["numbers"]["K1"].items()}
R60 = json.load(open(os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids_results.json")))

# ------------------------------------------------------------------------------------------------ the radial mesh
N = len(rr)
rf = np.sqrt(rr[1:] * rr[:-1])                                        # interior faces i+1/2, i = 0..N-2
rlo = rr[0] ** 2 / rf[0]                                              # the first cell's inner face
faces = np.concatenate([[rlo], rf, [rr[-1] ** 2 / rf[-1]]])           # N + 1 faces
V = (faces[1:] ** 3 - faces[:-1] ** 3) / 3.0                          # cell volume per steradian
dRf = rr[1:] - rr[:-1]                                                # centre spacing across each interior face
AF = rf ** 2 / dRf                                                    # face conductance r^2/dr


def Wg(t):
    t = np.asarray(t, float)
    inside = (t > 0) & (t < 1)
    tt = np.where(inside, t, 0.5)
    ell = np.clip(1 / tt - 1 / (1 - tt), -700, 700)
    W = 1 / (1 + np.exp(ell))
    return np.where(t >= 1, 1.0, np.where(t <= 0, 0.0, W))


def solve_region(Mb, a0, f, m_inv, sigma, rho_bar_cells=None):
    """w, P on the mesh for point-mass baryons Mb [kg] (+ optional extended baryons), gate f on cells, screening length
    m_inv [m] (None -> no screening), web self-term sigma.  Returns M_lens(<face) - M_all(<face) = r^2 (f P)'/G."""
    M2 = np.zeros(N) if m_inv is None else (1.0 - f) / m_inv ** 2
    src = np.zeros(N) if rho_bar_cells is None else 4 * math.pi * G * f * rho_bar_cells * V
    # w: a+(w_{i+1} - w_i) - a-(w_i - w_{i-1}) - V M^2 w = src (+ G Mb at the inner face);  w_{N-1} = 0
    ab = np.zeros((3, N)); rhs = np.zeros(N)
    up = np.zeros(N); lo = np.zeros(N); di = np.zeros(N)
    up[:-1] = AF; lo[1:] = AF
    di[:] = -(up + lo) - V * M2
    rhs[:] = src; rhs[0] += G * Mb
    di[-1], lo[-1], rhs[-1] = 1.0, 0.0, 0.0
    ab[0, 1:] = up[:-1]; ab[1] = di; ab[2, :-1] = lo[1:]
    w = solve_banded((1, 1), ab, rhs)
    wp = np.diff(w) / dRf                                             # w' on interior faces
    ff = 0.5 * (f[1:] + f[:-1])
    y = np.maximum(np.abs(wp) / a0, 1e-14)
    J = rf ** 2 * ff * (nu_vec(y) - 1.0) * wp                         # r^2 f (nu - 1) w' on interior faces
    # P: a+(P_{i+1} - P_i) - J_{i+1/2} - a-(P_i - P_{i-1}) + J_{i-1/2} = V M^2 (P_i + sigma w_i);  P_{N-1} = 0
    Jf = np.concatenate([[0.0], J, [0.0]])                            # inner face: r^2 P' = J (regular centre)
    rhs2 = Jf[1:] - Jf[:-1] + V * M2 * sigma * w
    ab2 = np.zeros((3, N)); di2 = -(up + lo) - V * M2
    di2[-1] = 1.0; rhs2[-1] = 0.0
    ab2[0, 1:] = up[:-1]; ab2[1] = di2; ab2[2, :-1] = np.concatenate([lo[1:-1], [0.0]])
    Pn = solve_banded((1, 1), ab2, rhs2)
    fP = f * Pn
    return rf ** 2 * np.diff(fP) / dRf / G                            # extra lensing mass inside each interior face


# projection: L352's project_M2 as a matrix (same trapezoid on the same masked sub-grid)
KP = np.zeros((len(Rp), N))
for i, Rv in enumerate(Rp):
    msk = np.where(rr > Rv * 1.0000001)[0]
    r2 = rr[msk]
    if len(msk) < 2:
        continue
    tw = np.zeros(len(r2)); d = np.diff(r2)
    tw[:-1] += d / 2; tw[1:] += d / 2
    KP[i, msk] = 2 * tw * r2 / np.sqrt(r2 ** 2 - Rv ** 2)


def m2_of_rho(rho):
    Sig = KP @ rho
    return np.concatenate([[0], np.cumsum(0.5 * (Sig[1:] * Rp[1:] + Sig[:-1] * Rp[:-1]) * np.diff(Rp))]) * 2 * math.pi \
        + 2 * math.pi * Rp[0] ** 2 * Sig[0]


def esd_from_mlens(Mb, Mext_face, b):
    """annulus ESD for a point mass Mb plus an extended lensing mass given inside the interior faces."""
    Mf = np.concatenate([[0.0], Mext_face, [Mext_face[-1]]])          # extended mass inside faces 0..N (0 at the centre)
    rho = np.diff(Mf) / (4 * math.pi * V)
    M2 = m2_of_rho(rho)
    return annulus_esd(lambda R, M2=M2: np.interp(np.log(R), np.log(Rp), M2) + Mb, Rd[b])


banner("C0  CONTROL: the projection matrix is L352's project_M2")
_test = np.exp(-rr / (0.3 * MPCm)) / (rr / MPCm + 0.01) ** 2 * 1e-20
c0 = float(np.max(np.abs(m2_of_rho(_test) - project_M2(_test)) / np.max(np.abs(project_M2(_test)))))
check("C0 CONTROL: this lane's projection matrix reproduces L352's project_M2", f"max rel diff {c0:.1e}", c0 < 1e-10)

# ------------------------------------------------------------------------------------------------ carrier templates
def carrier_rho(b, xv_eff, pic, outer="r200"):
    """L360's post-decay carrier; outer = 'r200' (L360's template, cut at r200) or 'nfw' (the host NFW continued)."""
    M = M200_BINS[b]
    c = c200(M); r200 = (3 * M * MS / (4 * math.pi * 200 * rhoc_zl)) ** (1 / 3); rs = r200 / c
    rho_s = M * MS / (4 * math.pi * rs ** 3 * mfn(c))
    nfw = rho_s / ((rr / rs) * (1 + rr / rs) ** 2)
    rho = np.where(rr < r200, nfw, 0.0) if outer == "r200" else nfw
    rv = (Om * (1 + ZL) ** 3 / E2L(ZL) + 2 / 3 * xv_eff) * rhoc_zl
    rc = (1 - FB) * rho
    if not np.isfinite(xv_eff): return rc
    return np.where(rho >= rv, 0.0, rc) if pic == "cleared" else np.minimum(rc, rv)


def cum_mass_faces(rho_cells):
    return np.cumsum(4 * math.pi * rho_cells * V)[:-1]                # mass inside interior faces


CARRIERS = [(1.0, "cap", 700.0), (1.0, "cleared", 1000.0), (2.0, "cap", 1000.0)]
OUTERS = ("r200", "nfw")
TC, RHOC = {}, {}
for outer in OUTERS:
    for cc in CARRIERS:
        pc, pic, xv0 = cc
        xve = xv0 * E2L(ZL) ** pc
        for b in range(4):
            rc = carrier_rho(b, xve, pic, outer)
            RHOC[(cc, outer, b)] = rc
            TC[(cc, outer, b)] = annulus_esd(lambda R, M2=m2_of_rho(rc): np.interp(np.log(R), np.log(Rp), M2), Rd[b])
P(f"  carrier templates built for {CARRIERS} x outer {OUTERS}   [{time.time() - T0:.0f}s]")


# ------------------------------------------------------------------------------------------------ the gate on a branch
def stars_rho(Mb):
    a = 3.0 * (Mb / MS / 1e11) ** 0.3 * KPC_
    return Mb * a / (2 * math.pi * rr * (rr + a) ** 3)


def gate_f(branch, Mb, a0, xc_eff, w, rho_car):
    if branch == "upper":
        Mdyn = Mb * nu_vec(G * Mb / rr ** 2 / a0)
        rho = np.gradient(Mdyn, rr) / (4 * math.pi * rr ** 2) + rho_car
        x = 4 * math.pi * G * (rho - rho_bar) / H_L ** 2
    else:
        rho = stars_rho(Mb) + rho_car
        x = 4 * math.pi * G * (rho - (0.0 if branch == "lower_abs" else rho_bar)) / H_L ** 2
    if w is None:                                                      # hard edge at the outermost 'on' cell (L352)
        on = x >= xc_eff
        it = int(np.where(on)[0].max()) if on.any() else -1
        return np.where(np.arange(N) <= it, 1.0, 0.0)
    t = (x / xc_eff - 1) / (2 * w) + 0.5
    off = np.where(t <= 0)[0]
    f = Wg(t)
    if off.size:                                                       # the region connected to the centre (L392's rule)
        f[off[0]:] = 0.0
    return f


_ESD = {}


def model_esd(b, lm, foot, branch, xc_eff, w, m_inv, sigma, cc, outer="r200"):
    key = (b, round(lm, 3), foot, branch, round(xc_eff, 6), w, m_inv, sigma, cc, outer)
    if key in _ESD: return _ESD[key]
    Mb = 10 ** lm * MS; a0 = A0[foot]
    rho_car = RHOC[(cc, outer, b)] if cc is not None else np.zeros(N)
    f = np.ones(N) if branch == "none" else gate_f(branch, Mb, a0, xc_eff, w, rho_car)
    sig = 0.0 if (MUTATE and sigma == 1.0) else sigma
    extra = solve_region(Mb, a0, f, m_inv, sig)
    out = esd_from_mlens(Mb, extra, b)                                 # carrier added separately (as L360)
    _ESD[key] = out
    return out


def fit_cell(foot, branch, xc_eff, w, m_inv, sigma, cc, fs=1.0, outer="r200"):
    mods = []
    for b in range(4):
        best = None
        for lm in LM:
            mk0 = model_esd(b, lm, foot, branch, xc_eff, w, m_inv, sigma, cc, outer)
            if cc is not None: mk0 = mk0 + fs * TC[(cc, outer, b)]
            t2 = twoh_cache[b]; wt = 1 / Sd[b] ** 2
            A = float(np.clip(np.sum(wt * t2 * (Ed[b] - mk0)) / np.sum(wt * t2 * t2), 0.0, 20.0)); mk = mk0 + A * t2
            c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
            if best is None or c_ < best[0]: best = (c_, mk)
        mods.append(best[1])
    dv = np.concatenate(Ed) - np.concatenate(mods)
    return float(dv @ Ci @ dv)


BASE = {f_: fit_model(A0[f_], 0.0, "none", True)[0] for f_ in ("canonical", "alt")}
P(f"  L352's unswitched baseline chi^2: canonical {BASE['canonical']:.2f}, alt {BASE['alt']:.2f}   [{time.time() - T0:.0f}s]")

# ============================================================================================ C1 C2 C3 controls
banner("C1-C3  CONTROLS: isolated QUMOND, the hard compensated edge, and L360's committed pair")
dev1 = 0.0
for b in range(4):
    for lm in (10.0, 10.6, 11.2):
        mine = model_esd(b, lm, "canonical", "none", 1.0, 1.0, None, 0.0, None)
        ref = esd_bin(b, lm, A0["canonical"], 0.0, "none", False)[0]
        dev1 = max(dev1, float(np.max(np.abs(mine / ref - 1))))
d1 = {f_: fit_cell(f_, "none", 1.0, 1.0, None, 0.0, None) - BASE[f_] for f_ in ("canonical", "alt")}
check("C1 CONTROL: with f = 1 the ODE solve reproduces L352's isolated QUMOND ESD and its KiDS score",
      f"max rel ESD diff {dev1:.1e}; Delta chi^2 {d1['canonical']:+.2f}/{d1['alt']:+.2f}",
      dev1 < 5e-3 and max(abs(v) for v in d1.values()) < 0.5)
XC_LIN = XE59[(1.0, 2.5)]
dev2 = 0.0
for b in range(4):
    for lm in (10.2, 10.8, 11.4):
        mine = model_esd(b, lm, "canonical", "upper", XC_LIN, None, 1 * KPC_, 0.0, None)
        ref = esd_bin(b, lm, A0["canonical"], round(XC_LIN, 4), "compensated", False)[0]
        dev2 = max(dev2, float(np.max(np.abs(mine - ref)) / np.max(np.abs(ref))))
check("C2 CONTROL: a hard upper-branch edge with sigma = 0 in the Dirichlet limit (1/m = 1 kpc, below the 2.6 kpc cells at "
      "1 Mpc) reproduces L352's compensated ESD (the operator's sigma = 0 hard-edge limit)",
      f"max |diff| / max |ESD| = {dev2:.1e} (x_c,eff = {XC_LIN:.4f})", dev2 < 0.02)
ref60 = R60["numbers"]["M2"]["1.0/2.5/1.0/cap/700.0"]["dchi2"]
d3 = {f_: fit_cell(f_, "upper", round(XC_LIN, 4), None, 1 * KPC_, 0.0, (1.0, "cap", 700.0)) - BASE[f_] for f_ in ("canonical", "alt")}
dd3 = max(abs(d3[f_] - ref60[f_]) for f_ in d3)
check("C3 CONTROL: with C2's settings and L360's carrier template, L360's committed score for (1, 2.5) + (1, cap, 700) "
      "is reproduced", f"this lane {d3['canonical']:+.1f}/{d3['alt']:+.1f} vs L360 {ref60['canonical']:+.1f}/{ref60['alt']:+.1f} "
      f"(max |diff| {dd3:.2f})", dd3 <= 1.5)
# C3b: L352's own compensated ESD + this lane's carrier template -> L360's score exactly (isolates the template copy)
def fit_l352_plus_tc(foot, xc, cc, outer="r200"):
    mods = []
    for b in range(4):
        best = None
        for lm in LM:
            mk0 = esd_bin(b, lm, A0[foot], xc, "compensated", False)[0] + TC[(cc, outer, b)]
            t2 = twoh_cache[b]; wt = 1 / Sd[b] ** 2
            A = float(np.clip(np.sum(wt * t2 * (Ed[b] - mk0)) / np.sum(wt * t2 * t2), 0.0, 20.0)); mk = mk0 + A * t2
            c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
            if best is None or c_ < best[0]: best = (c_, mk)
        mods.append(best[1])
    dv = np.concatenate(Ed) - np.concatenate(mods)
    return float(dv @ Ci @ dv)
d3b = {f_: fit_l352_plus_tc(f_, round(XC_LIN, 4), (1.0, "cap", 700.0)) - BASE[f_] for f_ in ("canonical", "alt")}
dd3b = max(abs(d3b[f_] - ref60[f_]) for f_ in d3b)
check("C3b CONTROL: L352's own compensated ESD plus this lane's carrier template reproduces L360's committed score exactly "
      "(the template is L360's)", f"{d3b['canonical']:+.3f}/{d3b['alt']:+.3f} vs L360 {ref60['canonical']:+.3f}/{ref60['alt']:+.3f} "
      f"(max |diff| {dd3b:.1e})", dd3b < 1e-6,
      "so C3's residual is the ODE profile's 1.5e-3 difference (C2) moving one bin's best M_b on the discrete 0.1-dex grid: "
      "a KiDS score here carries ~2 of grid noise, which bounds how small a sigma shift can be read")
P(f"  controls done   [{time.time() - T0:.0f}s]")

# ============================================================================================ S1 sigma is exercised
banner("S1  sigma IS EXERCISED: the sigma = 1 and sigma = 0 ESDs at 1/m = 0.1 Mpc, w = 1")
s1 = 0.0
for branch in ("upper", "lower"):
    for b in range(4):
        e1 = model_esd(b, 10.8, "canonical", branch, XC_LIN, 1.0, 100 * KPC_, 1.0, (1.0, "cap", 700.0), "nfw")
        e0 = model_esd(b, 10.8, "canonical", branch, XC_LIN, 1.0, 100 * KPC_, 0.0, (1.0, "cap", 700.0), "nfw")
        s1 = max(s1, float(np.max(np.abs(e1 - e0))))
check("S1 sigma = 1 changes the lensing ESD (max |ESD(sigma=1) - ESD(sigma=0)| > 1e-3 Msun/pc^2 somewhere)",
      f"{s1:.3e} Msun/pc^2", s1 > 1e-3, "the edge layer's f' P term and the M^2 w source move the lensing mass near the edge")

# ============================================================================================ the scan
banner("THE SCAN: branch x switch cell x carrier x 1/m x w x sigma x footing (amplitude 1, L352's criterion)")
CELLS = [(1.0, 2.5), (0.5, 2.65), (0.5, 3.39)]
BRANCHES = ["upper", "lower", "lower_abs"]
MINV = [100 * KPC_, 500 * KPC_]
WS = [1.0, 0.25]
SC = {}
for outer in OUTERS:
    for branch in BRANCHES:
        for (p, xc0) in CELLS:
            xce = xc0 * E2G(ZL) ** p
            for cc in CARRIERS:
                for mi in MINV:
                    for w in WS:
                        row = {}
                        for sg in (0.0, 1.0):
                            for f_ in ("canonical", "alt"):
                                row[(sg, f_)] = fit_cell(f_, branch, xce, w, mi, sg, cc, 1.0, outer) - BASE[f_]
                        SC[(outer, branch, p, xc0, cc, mi, w)] = row
                        P(f"    {outer:4s} {branch:9s} cell ({p:g}, {xc0:g}) carrier {cc} 1/m = {mi / KPC_:.0f} kpc w = {w:g}: "
                          f"Delta chi^2 sigma=0 {row[(0.0, 'canonical')]:+7.1f}/{row[(0.0, 'alt')]:+7.1f}   sigma=1 "
                          f"{row[(1.0, 'canonical')]:+7.1f}/{row[(1.0, 'alt')]:+7.1f}   [{time.time() - T0:.0f}s]")
OUT["numbers"]["scan"] = {"/".join(str(x) for x in (k[0], k[1], k[2], k[3], "_".join(map(str, k[4])), round(k[5] / KPC_), k[6])):
                          {f"{sg}/{f_}": v for (sg, f_), v in row.items()} for k, row in SC.items()}

dmax = max(abs(row[(1.0, f_)] - row[(0.0, f_)]) for row in SC.values() for f_ in ("canonical", "alt"))
dmax_b = {(o, br): max(abs(row[(1.0, f_)] - row[(0.0, f_)]) for k, row in SC.items() if k[0] == o and k[1] == br
                       for f_ in ("canonical", "alt")) for o in OUTERS for br in BRANCHES}
P("    max |Delta chi^2(sigma=1) - Delta chi^2(sigma=0)| per outer convention and branch: "
  + "; ".join(f"{o}/{br}: {v:.2f}" for (o, br), v in dmax_b.items()))
OUT["numbers"]["sigma_shift_by_branch"] = {f"{o}/{br}": v for (o, br), v in dmax_b.items()}
check("H1 [pre-declared] sigma is a sub-dominant axis for KiDS: |Delta chi^2(sigma=1) - Delta chi^2(sigma=0)| <= 4 in every "
      "cell", f"max |difference| = {dmax:.2f}", dmax <= 4.0,
      "the edge layer is thin against KiDS's log-spaced radial bins, or the 2-halo term absorbs it")

banner("V1  THE VERDICT PER BRANCH")
passes = lambda row, sg: all(row[(sg, f_)] <= 4.0 for f_ in ("canonical", "alt"))
V = {}
for outer, branch in [(o, br) for o in OUTERS for br in BRANCHES]:
    keys = [k for k in SC if k[0] == outer and k[1] == branch]
    p0 = [k for k in keys if passes(SC[k], 0.0)]
    p1 = [k for k in keys if passes(SC[k], 1.0)]
    both = [k for k in p0 if k in p1]
    V[f"{outer}/{branch}"] = {"cells": len(keys), "pass_sigma0": len(p0), "pass_sigma1": len(p1), "sigma1_where_sigma0": len(both),
                             "best_sigma1": min(max(SC[k][(1.0, f_)] for f_ in ("canonical", "alt")) for k in keys)}
    P(f"    {outer:4s} {branch:9s}: {len(keys)} cells; pass at sigma = 0: {len(p0)}; at sigma = 1: {len(p1)}; sigma = 1 passes in "
      f"{len(both)} of the {len(p0)} sigma = 0 passes; best sigma = 1 score (worse footing) {V[f'{outer}/{branch}']['best_sigma1']:+.1f}")
    for k in p0:
        if k not in p1:
            P(f"      sigma = 1 LOSES: cell ({k[2]:g}, {k[3]:g}) carrier {k[4]} 1/m = {k[5] / KPC_:.0f} kpc w = {k[6]:g}")
    for k in p1:
        if k not in p0:
            P(f"      sigma = 1 GAINS: cell ({k[2]:g}, {k[3]:g}) carrier {k[4]} 1/m = {k[5] / KPC_:.0f} kpc w = {k[6]:g}")
OUT["numbers"]["verdict"] = V
check("V1 (reported) KiDS verdict per branch at sigma = 0 and sigma = 1", V, True, load_bearing=False)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
  f"[{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
