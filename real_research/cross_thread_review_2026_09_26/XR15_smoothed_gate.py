#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR15 -- DOOR (c): THE GATE READS A SMOOTHED VARIABLE, (1 - l^2 lap) chi = U, IMPOSED AS A LINEAR CONSTRAINT.  Does it
repair the action-level obstruction of V0's MOND-sector gate (DE12, 7f84b3546; DE13, 6daea932c + a7abb4d4f), and at
what cost?

WHY.  Varied as an action term, the converged model's gate f = W(U), U = C[lap(u - v) + div((nu - 1) grad S w)] (CV3's
reading A+), has a second variation that is a k^0 NEGATIVE bulk modulus on the edge-layer gas, amplified by the phantom's
response A^2 (DE12): Gamma = c_gate k with c_gate 1500-3700 km/s against 37-117 km/s gas, 2-5e4 H at k = 1/kpc.  No
gradient energy of any strength repairs it (DE13 + completion).  DE13 left three doors; this lane opens door (c): the
gate reads chi, with (1 - l^2 lap) chi = U enforced by a multiplier zeta that enters linearly (CV3's rule), f = W(chi).

THE CONSTRUCTION AND ITS EXACT VARIATIONS (sympy, part A).  L -> L_V0(f = W(chi)) + zeta [(chi - l^2 chi'') - U]/(8 pi G).
  zeta-equation: (1 - l^2 lap) chi = U;   chi-equation: (1 - l^2 lap) zeta = -8 pi G B W'(chi),  B = dL/df (CV3's);
  so zeta = -8 pi G Xi with Xi = G_l(B W'(chi)) the SMOOTHED gate force; the gate's u-part is -C zeta'', its v-part the
  opposite (the carrier stays blind), no slip.  First variation on the baryons: DE12's -4 pi G C B W' t smoothed by G_l.
  Second variation, per the reduced gate functional -int B(y) W(t(chi)) with chi = G_l U (DE12's reduction, exact):
    T1 = int B W'' t^2 (G_l dU)^2              the main term; the smoothing suppresses it as (1 + l^2 k^2)^-2
    T2 = int Xi d2U                             the ANALOGUE of DE13's background term: the smoothed gate force times U's
                                                own second-order response (the phantom's curvature h''); NOT suppressed
    T3 = 2 int B' W' t (G_l dU)                 the cross term: the kernel coefficient's response B' = a0 h(y)/(4 pi G) dg_N
                                                times the gate's; suppressed only once
    T4 = int B'' W                              the gated kernel's own second variation = the MOND-enhanced self-gravity of
                                                the gas (no W', W''): not a gate term; neglected with Newtonian self-gravity
                                                and buoyancy (DE13's scope), its size reported as the gas's MOND Jeans growth
  The smoothing is linear, so it has no gradient-of-background term of its own (unlike DE13's form (ii)); T2 and T3 are the
  terms it exposes.  C3 checks T1 + T2 + T3 + T4 against finite differences of the discretised functional.

THE LAYERS (part C).  DE12's transitions, loaded unedited (its definitions only; its checks never run, its JSON never
written): 24 galaxy layers (z = 0.25, 1, 2.5, 4; M_b = 1e10, 1e11, 1e12; canonical 9.36e-11 and alt 1.13e-10) and DE13's
eight uncapped 1e14 clusters; the kappa-capped 1e14 cluster of DE12's G6 separately.  Gas at 1e6 K (117 km/s).
  * THE EXACT l = 0 SECTOR ('par').  Spherical perturbations are exact in a spherical background: radial displacement xi,
    delta rho = -div(rho xi), dg_N = -4 pi G rho xi, dU = C div(A_par dg_N), A_par = d(y nu)/dy, d2U = C div(h'' dg_N^2/a0);
    chi's perturbation G_l dU solved on the radial Yukawa operator.  A negative mode here is a real instability.
  * DE13's CONVENTION ('perp'): radial modes carrying the transverse response A_perp = nu (dU = C 4 pi G nu delta rho),
    DE13's conservative choice; with it, the WKB gate term bounds every direction.
  Growth: M xi'' = -K xi (kinetic weight rho r^2), Gamma = sqrt(-lambda_min).  Where l is below 5 grid cells the WKB rate
  Gamma = max_r max_k k sqrt(c_gate^2/(1 + l^2 k^2)^2 - c_s^2) is used and labelled.
  The layer's own evolution rate: the edge's motion across its own width, (1 + z) H |dr_e/dz| / L.

PRE-DECLARED (written into this file before the main run; single-layer exploratory runs on z = 0.25/1e11 and 1e12,
z = 2.5/1e11 and z = 4/1e10, canonical, were used to build and debug the machinery and are disclosed in the README):
  H1 [the review's example, per layer; load-bearing]: on EVERY galaxy layer some l <= 0.3 r_e (that layer's own edge
     radius) brings the gate-driven growth of the exact l = 0 sector to Gamma <= H(z), and at that l the layer's own
     edges (t = 1, 1/2, 0) move by less than 10%.
  H2 [the construction, one constant l; load-bearing]: a single l brings all 24 galaxy layers to Gamma <= H(z) (exact
     l = 0 sector) while (i) the KiDS lenses' edges (1e11 at z = 0.25, both footings; t = 1/2 and t = 0) move < 10%,
     (ii) MOND stays fully on (t_chi >= 1) at r_F for 1e10, 1e10.5, 1e11 at z = 2.5, both footings, and (iii) at the Sun
     (z = 0, 6e10, 8 kpc).
  The writer's expectation before the run: H1 fails at z = 0.25 (a residual Gamma ~ 1-3 H seen in exploration), H2 fails
  (the z = 0.25 layers need l of hundreds of kpc; the z >= 2.5 regions are ~30-270 kpc).

CHECKS
  A1 [sympy] the chi-extended V0's Euler-Lagrange equations: zeta's constraint, (1 - l^2 d^2) zeta = -8 pi G B W'(chi),
     the gate's u-part -C zeta'' cancelling its v-part (no leak), no slip.
  A2 [sympy + counting] the constraint Jacobian (multipliers Phi, lam, Psi, zeta against u, v, w, chi): the new pair's
     entries are (Psi, chi) = [m^2 w - lap(u - v)] W'(chi) and (zeta, w) = -C (phantom operator); det K's symbol is
     2 k^4 [G_loop k^2 - (1 + l^2 k^2)(k^2 + M^2)] -- GATE-DEPENDENT.  At l = 0 (CV3's A+ as written) the (Psi, w)
     entry itself carries 1 - G_loop, G_loop = U_b W' t (A - 1): CV3's G3 matrix omits it.  With U reading an UNGATED
     phantom (a further pair, lap w~ = lap(u - v)) det K = 2 k^6 (k^2 + M^2)(1 + l^2 k^2): gate-independent.
  L1 [numbers, load-bearing] G_loop > 1 inside every one of the 24 galaxy layers (both directions): in V0 as written the
     constraint symbol vanishes inside every layer -- at l = 0 on surfaces, for l > 0 at k* = sqrt(G_loop - 1)/l (no
     screening) -- so door (c) cannot remove it; DE12's reduction (A with f -> 1) is exact only for the ungated reading.
  C1 CONTROL: l = 0 reproduces DE12's committed c_gate and Gamma(k = 1/kpc)/H on all 24 galaxy layers (1e-12) and its
     capped cluster.
  C2 CONTROL: the radial smoothing solver against the exact spherical Yukawa integral (test profile) and the point mass's
     field e^{-r/l}/(l^2 r).
  C3 CONTROL: T1 + T2 + T3 + T4 equal finite differences of the discretised l = 0 functional (with the nonlinear phantom
     and B) to 1e-5 at l = 0 and l > 0; without T2 + T3 they miss by >= 1e-3 at l > 0 (the exposed terms are real).
  C4 CONTROL: at l = 0 the discrete l = 0 sector is unstable on every galaxy layer, gas alone stable (DE12 reproduced in
     this lane's form); the discrete growth matches the WKB rate at small l.
  C5 CONTROL: Gamma/H converged in grid points (800 vs 1600, 5%) and in the domain margin (6 l vs 9 l, 3%), and a stability
     threshold to 3%.  The first development run used a 2 l margin, which truncated the fastest mode (it sits just outside
     the layer and reaches ~4 l beyond it); its values are printed beside the converged ones.
  S1 [load-bearing; MUTATE's target] the smoothing is effective: on every galaxy layer the gate-driven growth falls from
     DE12's 1e3-1e5 H to <= 10 H at some l <= r_e.
  H1, H2 as pre-declared.
  R1-R5 (reported) R1 growth vs l per layer, vs H and vs the layer's own evolution rate, and per-layer thresholds; R2 the
     residual mode's driver (T1/T2/T3) against the gas's own MOND Jeans growth (T4); R3 one constant l: growth, edges, the
     KiDS lenses, the flagship r_F (with the smoothed gate's own force there) and the Sun; R4 the kappa cap with chi (MS5):
     chi = G_l(U_cap), and the capped branch's k^0 term Xi U_rhorho, which the smoothing only dilutes; R5 (NOT
     pre-declared) a smoothing length depending on cosmic time only, l(z), still linear on each leaf.
MUTATE=1 drops the smoothing inside the second variation only (dchi = dU, Xi = B W' t) and keeps the smoothed background:
S1 must FAIL (rc = 1).  C5 fails with it (the unsmoothed growth is grid-limited, DE12's UV catastrophe, so it cannot
converge).

SCOPE.  DE12's frozen background and reduction (U's response A at f = 1; B = a0^2 q(y^2)/(8 pi G) of the ungated field);
isothermal fluid gas; self-gravity (Newtonian and T4) and buoyancy neglected at the gate's scales, T4's growth reported;
spherical isolated systems; the transverse (l > 0 multipole) sector bounded by the 'perp' convention, not solved.  V0 as
written (U reading the gated w) is not in DE12's reduction: L1 prices its constraint structure only.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR15_smoothed_gate.py
"""
import os, sys, json, math, time, io, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np
from scipy.linalg import solve_banded, eigh
import sympy as sp
warnings.filterwarnings("ignore", message=".*overflow encountered.*")
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR15_smoothed_gate"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR15", "mutate": MUTATE, "checks": {}, "numbers": {}}
H1_LMAX_OVER_RE, EDGE_TOL = 0.3, 0.10                                   # pre-declared (H1, H2)


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
if MUTATE: P("\n  *** MUTATE=1: the smoothing is dropped inside the second variation (background kept smoothed); S1 must FAIL ***")

# ---------------------------------------------------------------------------------- DE12's machinery, loaded unedited
# (the same extraction DE13 uses: the constants/kernel head and the transition() definitions; C1/C2/G1-G6 never run,
#  DE12's JSON never written; transition_on = transition with the radial grid as an argument)
P12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
D12 = {"__name__": "de12", "__file__": P12}
_src = open(P12).read()
_head = _src.split("# ============================================================================================ C1 the amplification")[0]
_trans = _src.split("# ============================================================================================ the transitions")[1].split(
    "# ============================================================================================ G1 G2 the budget")[0]
_trans = _trans.split('banner("C2')[0]
_GRID_LINE = "r = np.geomspace(1.0, 2e4, 20000) * KPC"
assert _trans.count(_GRID_LINE) == 1
_trans_on = "def transition_on(rgrid, " + _trans.split("def transition(")[1].replace(_GRID_LINE, "r = rgrid")
with contextlib.redirect_stdout(io.StringIO()):
    exec((_head + _trans + "\n" + _trans_on).replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D12)
G, MS, KPC, A0, FB, Hz, E2f = [D12[k] for k in ("G", "MS", "KPC", "A0", "FB", "Hz", "E2")]
nu_of, ynup_of, h_of, dh_of, q_of, Wd, host = [D12[k] for k in ("nu_of", "ynup_of", "h_of", "dh_of", "q_of", "Wd", "host")]
transition, transition_on, CS = D12["transition"], D12["transition_on"], D12["CS"]
C_LIGHT = D12["L52"]["c"]; V_CAP = D12["V_CAP"]
R12 = json.load(open(os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness_results.json")))["numbers"]
P(f"  DE12 machinery loaded (definitions only)   [{time.time() - T0:.0f}s]")
W_M = 0.25; TU = 1 / (2 * W_M)
CS2 = CS["1e6K"] ** 2
GAL = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in ("canonical", "alt")]
CLU = [(z, 1e14, f) for z in (0.25, 1.0, 2.5, 4.0) for f in ("canonical", "alt")]
KEY = lambda z, Mb, f: f"{z}/{Mb:.0e}/{f}"


# the kernel in closed form: h(y) = y/(e^sqrt(y) - 1) (nu_RAR; DE12's table equals it below y* = 2.34, checked in C2)
def h_an(y):
    y = np.asarray(y, float); return y / np.expm1(np.sqrt(np.minimum(y, 1e4)))


def h1_an(y, e=1e-5):
    y = np.asarray(y, float); return (h_an(y * (1 + e)) - h_an(y * (1 - e))) / (2 * y * e)


def h2_an(y, e=1e-4):
    y = np.asarray(y, float); return (h_an(y * (1 + e)) - 2 * h_an(y) + h_an(y * (1 - e))) / (y * e) ** 2


# ---------------------------------------------------------------------------------- the radial smoothing operator
def lap_parts(r):
    """conservative radial Laplacian (1/r^2)(r^2 f')' on nodes r: couplings rh^2/dr, diagonal, node weights r^2 w."""
    dr = np.diff(r); rh = 0.5 * (r[1:] + r[:-1])
    wi = np.zeros(len(r)); wi[1:-1] = 0.5 * (r[2:] - r[:-2]); wi[0] = 0.5 * dr[0]; wi[-1] = 0.5 * dr[-1]
    cpl = rh ** 2 / dr
    dia = np.zeros(len(r)); dia[:-1] -= cpl; dia[1:] -= cpl
    return cpl, dia, r ** 2 * wi, wi


def smooth_solve(r, l, rhs, bc0=0.0, bc1=0.0, inner="neumann"):
    """solve (1 - l^2 L) chi = rhs: zero flux at r[0] ('neumann', the regular centre as r[0] -> 0) or Dirichlet bc0;
    Dirichlet bc1 at r[-1].  rhs may be a matrix (one column per right-hand side)."""
    b = np.array(rhs, float, copy=True)
    if l == 0:
        return b
    cpl, dia, den, wi = lap_parts(r)
    ab = np.zeros((3, len(r)))
    ab[1] = 1 - l ** 2 * dia / den
    ab[0, 1:] = -l ** 2 * cpl / den[:-1]
    ab[2, :-1] = -l ** 2 * cpl / den[1:]
    if inner == "dirichlet":
        ab[1, 0] = 1; ab[0, 1] = 0.0; b[0] = bc0
    ab[1, -1] = 1; ab[2, -2] = 0.0; b[-1] = bc1
    return solve_banded((1, 1), ab, b)


def yukawa_exact(r, U, l, idx):
    """spherical Yukawa smoothing by quadrature: chi(r) = (1/(2 l r)) int U r' [e^{-|r-r'|/l} - e^{-(r+r')/l}] dr'."""
    trap = getattr(np, "trapezoid", None) or np.trapz
    return np.array([trap(U * r * (np.exp(-np.abs(r[i] - r) / l) - np.exp(-(r[i] + r) / l)), r) / (2 * l * r[i]) for i in idx])


# ---------------------------------------------------------------------------------- backgrounds
RG = np.geomspace(0.05, 2e5, 12000) * KPC                               # the global radial grid (0.05 kpc - 200 Mpc)


def background(z, Mb, foot, l_kpc, cap=False, rg=RG):
    """U (DE12's), chi = G_l U + the galaxy's point mass (C G M_b e^{-r/l}/(l^2 r), the exact Yukawa field of the
    baryons DE12 keeps at r = 0), and Xi = G_l(B W'(t_chi) t) on the global grid."""
    tr = transition_on(rg, z, Mb, foot, W_M, amp=True, cap=cap)
    U = (tr["t"] - 0.5) * 2 * W_M + 1
    C = 1 / (tr["H"] ** 2 * tr["xce"])
    l = l_kpc * KPC
    if l > 0:
        chi = smooth_solve(rg, l, U, bc1=U[-1]) + C * G * Mb * MS * np.exp(-rg / l) / (l ** 2 * rg)
    else:
        chi = U.copy()
    t = (chi - 1) / (2 * W_M) + 0.5
    _, W1, _ = Wd(t)
    BWt = tr["B"] * W1 * TU
    Xi = smooth_solve(rg, l, BWt, bc1=0.0) if l > 0 else BWt
    return dict(r=rg, U=U, chi=chi, t=t, C=C, tr=tr, Xi=Xi, H=tr["H"], l=l)


def edges(bg):
    """outermost radii (kpc) where t_chi crosses 1, 1/2 and 0 (t falls outward); None if the region is gone."""
    r, t = bg["r"], bg["t"]
    out = {}
    for lev in (1.0, 0.5, 0.0):
        idx = np.where((t[:-1] >= lev) & (t[1:] < lev))[0]
        out[lev] = (float(r[idx[-1]] + (lev - t[idx[-1]]) * (r[idx[-1] + 1] - r[idx[-1]]) / (t[idx[-1] + 1] - t[idx[-1]])) / KPC
                    if len(idx) else None)
    return out


# ---------------------------------------------------------------------------------- the l = 0 sector on one layer
def ext_grid(ra, rb, Np, l, rmin):
    rp = np.linspace(ra, rb, Np)
    if l == 0:
        return rp, 0
    d0 = rp[1] - rp[0]; dmax = max(l / 4, d0)
    left, x, d = [], ra, d0
    while x - d > max(ra - 8 * l, rmin):
        d = min(d * 1.08, dmax); x -= d; left.append(x)
    right, x, d = [], rb, d0
    while x < rb + 8 * l:
        d = min(d * 1.08, dmax); x += d; right.append(x)
    return np.concatenate([np.array(left[::-1]), rp, np.array(right)]), len(left)


def layer_problem(z, Mb, foot, l_kpc, bg, Np=800, variant="par", smooth_pert=True, cs2=CS2, margin_l=6.0):
    """quadratic forms of the exact l = 0 sector (variant 'par') or DE13's radial/transverse-A convention ('perp') on the
    outermost chi-layer.  xi on half points of a uniform grid over [r_in - 6l, r_out + 6l] (zero flux at its ends; the
    fastest mode sits just outside the layer and reaches ~4 l beyond it, C5);
    chi's perturbation on an extended grid (to 8 l beyond, Dirichlet zero)."""
    l = l_kpc * KPC
    rg, tg = bg["r"], bg["t"]
    on = (tg > 0) & (tg < 1)
    if not on.any():
        return None
    idx = np.where(on)[0]
    brk = np.where(np.diff(idx) > 1)[0]
    idx = idx[brk[-1] + 1:] if len(brk) else idx                     # the outermost contiguous layer
    r_in, r_out = rg[idx.min()], rg[idx.max()]
    Lc = r_out - r_in
    m = max(margin_l * l, 0.1 * Lc)
    ra, rb = max(r_in - m, rg[1]), r_out + m
    r, i0 = ext_grid(ra, rb, Np, l, rg[1])
    ip = np.arange(i0, i0 + Np)
    C, a0 = bg["C"], A0[foot]
    tr = transition_on(r, z, Mb, foot, W_M)
    B = tr["B"]
    U0 = (tr["t"] - 0.5) * 2 * W_M + 1
    if l > 0:
        chi_e = np.interp(r, rg, bg["chi"])
        chi0 = smooth_solve(r, l, U0, bc0=chi_e[0], bc1=chi_e[-1], inner="dirichlet")
    else:
        chi0 = U0.copy()
    t0 = (chi0 - 1) / (2 * W_M) + 0.5
    W0, W1, W2 = Wd(t0)
    cpl, dia, wts, wi = lap_parts(r)
    rpn = r[ip]; rh = 0.5 * (rpn[1:] + rpn[:-1]); dh = np.diff(rpn); nx = Np - 1
    trh = transition_on(rh, z, Mb, foot, W_M)
    rho_h, y_h = trh["rho_b"], trh["y"]
    wp = np.zeros(Np); wp[1:-1] = 0.5 * (rpn[2:] - rpn[:-2]); wp[0] = 0.5 * dh[0]; wp[-1] = 0.5 * dh[-1]
    Dv = np.zeros((Np, nx))                                            # div of a half-point field, zero flux outside
    jj = np.arange(nx)
    Dv[jj, jj] = rh ** 2 / (rpn[:-1] ** 2 * wp[:-1]); Dv[jj + 1, jj] = -rh ** 2 / (rpn[1:] ** 2 * wp[1:])
    Dm = -Dv * rho_h[None, :]                                          # delta rho = -div(rho xi)
    dg = -4 * math.pi * G * rho_h                                      # dg_N per xi (exact for l = 0)
    if variant == "par":
        dU = C * Dv * ((1 + h1_an(y_h)) * dg)[None, :]                   # C div(A_par dg_N)
    else:
        dU = (C * 4 * math.pi * G * nu_of(tr["y"][ip]))[:, None] * Dm    # DE13's convention: C 4 pi G A_perp delta rho
    dUe = np.zeros((len(r), nx)); dUe[ip] = dU
    X = smooth_solve(r, l, dUe, inner="dirichlet") if (l > 0 and smooth_pert) else dUe
    BWt = B * W1 * TU
    Xi = smooth_solve(r, l, BWt, inner="dirichlet") if (l > 0 and smooth_pert) else BWt
    T1 = X.T @ ((B * W2 * TU ** 2 * wts)[:, None] * X)
    Xip = Xi[ip]
    T2 = np.diag(-C * (Xip[1:] - Xip[:-1]) * h2_an(y_h) / a0 * rh ** 2 * dg ** 2)
    Pn = np.zeros((Np, nx)); Pn[jj, jj] = 0.5 * dg; Pn[jj + 1, jj] += 0.5 * dg          # dg_N at the nodes
    yn = tr["y"][ip]
    T3a = Pn.T @ ((a0 * h_an(yn) / (4 * math.pi * G) * W1[ip] * TU * wts[ip])[:, None] * X[ip])
    T3 = T3a + T3a.T
    T4 = Pn.T @ ((h1_an(yn) / (4 * math.pi * G) * W0[ip] * wts[ip])[:, None] * Pn)
    Kgas = Dm.T @ ((cs2 / tr["rho_b"][ip] * wts[ip])[:, None] * Dm)
    Mk = rho_h * rh ** 2 * dh
    return dict(K=Kgas - (T1 + T2 + T3), Kgas=Kgas, T1=T1, T2=T2, T3=T3, T4=T4, M=Mk, H=bg["H"], r=r, ip=ip, rh=rh,
                chi0=chi0, t0=t0, X=X, C=C, a0=a0, r_in=r_in, r_out=r_out, Lc=Lc, B=B, W2=W2, rho=tr["rho_b"], y=tr["y"],
                Np=Np, dx=(rb - ra) / (Np - 1))


def lowest(K, M, k=1, vec=False):
    s = 1 / np.sqrt(M)
    Ks = (s[:, None] * K) * s[None, :]; Ks = 0.5 * (Ks + Ks.T)
    if vec:
        w, V = eigh(Ks, subset_by_index=[0, k - 1]); return w, V * s[:, None]
    return eigh(Ks, eigvals_only=True, subset_by_index=[0, k - 1])


def wkb_gamma(bg, z, Mb, foot, l_kpc, variant):
    """max over the chi-layer of max_k k sqrt(c_gate^2/(1 + l^2 k^2)^2 - c_s^2), c_gate^2 = rho B W'' t^2 (C 4 pi G A)^2."""
    tr = bg["tr"]; t = bg["t"]; m = (t > 0) & (t < 1)
    if not m.any():
        return 0.0
    _, _, W2 = Wd(t[m])
    y = tr["y"][m]
    A = (1 + h1_an(y)) if variant == "par" else nu_of(y)
    cg2 = np.maximum(tr["rho_b"][m] * tr["B"][m] * W2 * TU ** 2 * (bg["C"] * 4 * math.pi * G * A) ** 2, 0.0)
    l = l_kpc * KPC
    if l == 0:
        return float("inf") if np.max(cg2) > CS2 else 0.0
    xs = np.geomspace(1e-2, 1e2, 400)
    g2 = (xs[None, :] / l) ** 2 * (cg2[:, None] / (1 + xs[None, :] ** 2) ** 2 - CS2)
    return float(np.sqrt(max(np.max(g2), 0.0)))


def gamma_at(z, Mb, foot, l_kpc, variant, bg=None, Np=800, smooth_pert=None, parts=False, margin_l=6.0):
    """the fastest gate-driven growth rate / H on the layer at smoothing length l; ('wkb' when l < 5 cells)."""
    smooth_pert = (not MUTATE) if smooth_pert is None else smooth_pert
    bg = background(z, Mb, foot, l_kpc) if bg is None else bg
    Pp = layer_problem(z, Mb, foot, l_kpc, bg, Np=Np, variant=variant, smooth_pert=smooth_pert, margin_l=margin_l)
    if Pp is None:
        return dict(G=None, n=None, how="no layer")
    if l_kpc > 0 and l_kpc * KPC < 5 * Pp["dx"]:
        return dict(G=wkb_gamma(bg, z, Mb, foot, l_kpc if smooth_pert else 0.0, variant) / bg["H"], n=None, how="wkb")
    ev = lowest(Pp["K"], Pp["M"], k=3)
    out = dict(G=(math.sqrt(-ev[0]) / Pp["H"] if ev[0] < 0 else 0.0), n=int(np.sum(ev < 0)), how="eig")
    if parts:
        combos = {"T1": Pp["Kgas"] - Pp["T1"], "T2": Pp["Kgas"] - Pp["T2"], "T3": Pp["Kgas"] - Pp["T3"],
                  "T4_MOND_Jeans": Pp["Kgas"] - Pp["T4"]}
        for k_, K_ in combos.items():
            e_ = lowest(K_, Pp["M"])[0]
            out["gas+" + k_] = math.sqrt(-e_) / Pp["H"] if e_ < 0 else 0.0
        w_, V_ = lowest(Pp["K"], Pp["M"], vec=True)
        v_ = V_[:, 0]
        out["mode_r_kpc"] = float(Pp["rh"][np.argmax(np.abs(v_) * np.sqrt(Pp["M"]))] / KPC)
        out["layer_kpc"] = (float(Pp["r_in"] / KPC), float(Pp["r_out"] / KPC))
    return out


# ============================================================================================ A the variations (sympy)
banner("A1 A2  THE chi-EXTENDED V0: its Euler-Lagrange equations and its constraint Jacobian (sympy, CV3's chassis)")
x = sp.symbols("x", real=True)
G_, a0_, c1, d1, m2_, Cg, l_ = sp.symbols("G a0 c1 d1 m2 C l", positive=True)
sig = sp.symbols("sigma", real=True)
Phi, u, v, lam, w, Psi, psiM, chi, zeta, wt = [sp.Function(n)(x) for n in
                                               ("Phi", "u", "v", "lam", "w", "Psi", "psim", "chi", "zeta", "wt")]
rb, rd = sp.Function("rho_b")(x), sp.Function("rho_d")(x)
Wf = sp.Function("W")
qc = lambda s: c1 * s ** sp.Rational(3, 2) + d1 * sp.log(1 + s)          # CV3's concrete kernel (q = Q - Z, S = 1)
qcp = lambda s: sp.Rational(3, 2) * c1 * sp.sqrt(s) + d1 / (1 + s)       # q'(Z) = nu - 1
d_ = lambda F, n=1: sp.diff(F, x, n)
EPG = 8 * sp.pi * G_


def V0(f):
    """CV1/CV3's static Lagrangian (term for term) with gate expression f, M^2 = m^2 (1 - f)."""
    M2 = m2_ * (1 - f)
    return (-(rb + rd) * Phi + (2 * d_(psiM) ** 2 - 4 * d_(Phi) * d_(psiM)) / (2 * EPG) + (d_(u) - d_(Phi)) ** 2 / EPG
            + a0_ ** 2 * f * qc(d_(w) ** 2 / a0_ ** 2) / EPG
            + Psi * (d_(w, 2) - M2 * w - f * (d_(u, 2) - d_(v, 2))) / EPG
            + lam * (d_(v, 2) - 4 * sp.pi * G_ * rd) / EPG - sig * M2 * w ** 2 / EPG)


phant = lambda W_: d_(qcp(d_(W_) ** 2 / a0_ ** 2) * d_(W_))
U_Ap = Cg * ((d_(u, 2) - d_(v, 2)) + phant(w))                             # CV3's reading A+ (the phantom of the gated w)
L_c = V0(Wf(chi)) + zeta * (chi - l_ ** 2 * d_(chi, 2) - U_Ap) / EPG        # door (c): f = W(chi), zeta's linear constraint
ELc = {str(F_.func): sp.euler_equations(L_c, [F_], x)[0].lhs * EPG for F_ in (Phi, psiM, u, v, lam, w, Psi, chi, zeta)}
s_t, eps_ = sp.Symbol("s_t"), sp.Symbol("eps")
TEST = {Phi: sp.sin(sp.Rational(7, 10) * x + sp.Rational(3, 10)), u: sp.cos(sp.Rational(11, 10) * x) / 2 + x ** 2 / 5,
        v: sp.sin(sp.Rational(13, 10) * x + sp.Rational(1, 2)) * sp.Rational(3, 10), lam: sp.cos(sp.Rational(9, 10) * x),
        w: sp.sin(sp.Rational(4, 5) * x) * sp.Rational(2, 5) + sp.Rational(1, 10), Psi: sp.cos(x / 2 + sp.Rational(1, 5)) * sp.Rational(3, 5),
        psiM: sp.sin(sp.Rational(7, 10) * x + sp.Rational(3, 10)), rb: 1 + sp.sin(x) / 5, rd: sp.Rational(1, 2) + sp.cos(2 * x) / 10,
        chi: sp.Rational(1, 2) + sp.sin(sp.Rational(3, 5) * x) / 3, zeta: sp.cos(sp.Rational(6, 5) * x + sp.Rational(1, 7)) / 4,
        wt: sp.cos(sp.Rational(3, 4) * x) / 3}
TESTSYM = {G_: sp.Rational(3, 7), a0_: sp.Rational(6, 5), c1: sp.Rational(1, 3), d1: sp.Rational(1, 4), m2_: sp.Rational(5, 3),
           Cg: sp.Rational(2, 9), sig: 1, l_: sp.Rational(4, 7)}
W_TEST = sp.Lambda(s_t, 1 / (1 + sp.exp(-3 * s_t)))                       # a concrete smooth gate (CV3's)
XPTS = (sp.Rational(3, 10), sp.Rational(11, 10), sp.Rational(27, 10))


def num(expr):
    """|expr| at three points after substituting concrete fields, constants and gate shape (an identity valid for arbitrary
    functions must vanish there to ~40 digits)."""
    e = expr.replace(Wf, W_TEST).subs(TESTSYM).subs(TEST).doit()
    return float(max(abs(sp.N(e.subs(x, xp), 40)) for xp in XPTS))


B_expr = (a0_ ** 2 * qc(d_(w) ** 2 / a0_ ** 2) + Psi * (m2_ * w - (d_(u, 2) - d_(v, 2))) + sig * m2_ * w ** 2) / EPG
Wpc = sp.diff(Wf(chi), chi)
rA = {"zeta-eq is the constraint": num(ELc["zeta"] - (chi - l_ ** 2 * d_(chi, 2) - U_Ap)),
      "chi-eq: (1 - l^2 d^2) zeta = -8 pi G B W'(chi)": num(ELc["chi"] - (zeta - l_ ** 2 * d_(zeta, 2) + EPG * B_expr * Wpc))}
Eu_g = ELc["u"] - (-2 * d_(u, 2) + 2 * d_(Phi, 2) - d_(Psi * Wf(chi), 2))
Ev_g = ELc["v"] - d_(Psi * Wf(chi) + lam, 2)
rA["gate's u-part = -C zeta''"] = num(Eu_g - (-Cg * d_(zeta, 2)))
rA["no leak: u-part + v-part"] = num(Eu_g + Ev_g)
rA["no slip (psi = Phi)"] = num(ELc["psim"].subs(psiM, Phi))
gate_part = num(Eu_g)
for k_, v_ in rA.items():
    P(f"    {k_:48s} residual {v_:.1e}")
P(f"    (the gate's u-part itself, not vacuous: {gate_part:.2e})")
check("A1 [sympy] the chi-extended V0: zeta's equation is the linear constraint, chi's is (1 - l^2 d^2) zeta = -8 pi G B W'(chi) "
      "(zeta = -8 pi G x the smoothed gate force), the gate's u-part -C zeta'' cancels its v-part (no leak), no slip",
      "; ".join(f"{k_}: {v_:.0e}" for k_, v_ in rA.items()), max(rA.values()) < 1e-30 and gate_part > 1e-6,
      "door (c) keeps V0's leak-free, slip-free structure; the baryons feel DE12's gate potential smoothed by G_l")
OUT["numbers"]["A1"] = rA


def frechet(E, F_, direction):
    return sp.diff(E.subs(F_, F_ + eps_ * direction).doit(), eps_).subs(eps_, 0)


eta = sp.cos(sp.Rational(5, 3) * x + sp.Rational(2, 7)) / 5
Zw = d_(w) ** 2 / a0_ ** 2
Zs = sp.Symbol("Zs", positive=True)
Aeff = (qcp(Zs) + 2 * Zs * sp.diff(qcp(Zs), Zs)).subs(Zs, Zw)            # A_par - 1 in one dimension
E_Psi = d_(w, 2) - m2_ * (1 - Wf(chi)) * w - Wf(chi) * (d_(u, 2) - d_(v, 2))
E_zeta = chi - l_ ** 2 * d_(chi, 2) - U_Ap
r_pc = num(frechet(E_Psi, chi, eta) - (m2_ * w - (d_(u, 2) - d_(v, 2))) * Wpc * eta)
v_pc = num(frechet(E_Psi, chi, eta))
r_zw = num(frechet(E_zeta, w, eta) - (-Cg * d_(Aeff * d_(eta))))
E_Psi_l0 = d_(w, 2) - m2_ * (1 - Wf(U_Ap)) * w - Wf(U_Ap) * (d_(u, 2) - d_(v, 2))     # CV3's A+ as written (l = 0)
WpU = sp.diff(Wf(s_t), s_t).subs(s_t, U_Ap)
r_l0 = num(frechet(E_Psi_l0, w, eta) - (d_(eta, 2) - m2_ * (1 - Wf(U_Ap)) * eta
                                          + (m2_ * w - (d_(u, 2) - d_(v, 2))) * WpU * Cg * d_(Aeff * d_(eta))))
coef = 1 + (m2_ * w - (d_(u, 2) - d_(v, 2))) * WpU * Cg * Aeff                       # eta'' coefficient = 1 - G_loop
coefv = [float(sp.N(coef.replace(Wf, W_TEST).subs(TESTSYM).subs(TEST).doit().subs(x, xp), 12)) for xp in XPTS]
P(f"    (Psi, chi) entry = [m^2 w - (u'' - v'')] W'(chi): residual {r_pc:.1e} (the entry itself {v_pc:.2e})")
P(f"    (zeta, w) entry = -C d/dx[(A_par - 1) d/dx]: residual {r_zw:.1e}")
P(f"    CV3's A+ as written (l = 0): (Psi, w) entry = d^2 - M^2 + [m^2 w - (u'' - v'')] W'(U) C d/dx[(A_par - 1) d/dx]: "
  f"residual {r_l0:.1e}; its d^2 coefficient 1 - G_loop at the test points: {', '.join(f'{c_:.6f}' for c_ in coefv)}")
kk, M2s, gam, Gl, Ab, fs = sp.symbols("k M2 gamma G_loop A f", real=True)
a_ = -kk ** 2
Kmats = {
    "V0 as written, l = 0 (rows Phi, lam, Psi; cols u, v, w)":
        sp.Matrix([[2 * a_, 0, 0], [0, a_, 0], [-fs * a_, fs * a_, a_ - M2s + Gl * kk ** 2]]),
    "V0 + chi (rows Phi, lam, Psi, zeta; cols u, v, w, chi)":
        sp.Matrix([[2 * a_, 0, 0, 0], [0, a_, 0, 0], [-fs * a_, fs * a_, a_ - M2s, gam],
                   [-Cg * a_, Cg * a_, Cg * (Ab - 1) * kk ** 2, 1 + l_ ** 2 * kk ** 2]]),
    "U reads an ungated phantom + chi (adds Psi~, w~; lap w~ = lap(u - v))":
        sp.Matrix([[2 * a_, 0, 0, 0, 0], [0, a_, 0, 0, 0], [-fs * a_, fs * a_, a_ - M2s, gam, 0],
                   [-Cg * a_, Cg * a_, 0, 1 + l_ ** 2 * kk ** 2, Cg * (Ab - 1) * kk ** 2], [-a_, a_, 0, 0, a_]])}
dets = {}
for k_, Km in Kmats.items():
    dets[k_] = sp.factor(Km.det())
    P(f"    det K [{k_}] = {dets[k_]}")
d_chi = dets["V0 + chi (rows Phi, lam, Psi, zeta; cols u, v, w, chi)"]
d_ung = dets["U reads an ungated phantom + chi (adds Psi~, w~; lap w~ = lap(u - v))"]
# with gamma C = -G_loop/(A - 1) (gamma = -lap(u - v) W' t for m^2 w -> 0): det = 2 k^4 [G_loop k^2 - (1 + l^2 k^2)(k^2 + M^2)]
d_chi_G = sp.factor(d_chi.subs(gam, -Gl / (Cg * (Ab - 1))))
gate_dep = sp.diff(d_chi, gam) != 0 and sp.diff(dets["V0 as written, l = 0 (rows Phi, lam, Psi; cols u, v, w)"], Gl) != 0
gate_free = sp.diff(d_ung, gam) == 0 and sp.diff(d_ung, Ab) == 0
P(f"    V0 + chi with gamma C = -G_loop/(A - 1):  det K = {d_chi_G}")
P("    COUNT: the new pair (zeta, chi) adds two fields and two constraints (zeta's and chi's equations); neither carries a time\n"
  "    derivative (the smoothing acts on the leaves), so chi adds no propagating mode WHERE det K != 0.  The ungated variant\n"
  "    adds one more pair (Psi~, w~), again 0 degrees of freedom.")
check("A2 [sympy] the constraint Jacobian with the new multiplier pair: (Psi, chi) = [m^2 w - lap(u - v)] W'(chi), (zeta, w) = "
      "-C x the phantom operator; det K = 2 k^4 [G_loop k^2 - (1 + l^2 k^2)(k^2 + M^2)] is GATE-DEPENDENT (so is CV3's A+ at "
      "l = 0, whose (Psi, w) entry carries 1 - G_loop); with U reading an ungated phantom det K = 2 k^6 (k^2 + M^2)(1 + l^2 k^2)",
      f"entry residuals {r_pc:.0e}, {r_zw:.0e}, {r_l0:.0e}; det(V0 + chi) = {d_chi_G}; det(ungated) = {d_ung}",
      max(r_pc, r_zw, r_l0) < 1e-30 and v_pc > 1e-6 and gate_dep and gate_free and any(abs(c_ - 1) > 1e-4 for c_ in coefv),
      "CV3's rule (the determinant is gate-free when the gate reads constrained fields) needs one more condition: the fields "
      "the gate reads must not be determined by a constraint the gate itself enters.  V0's w is (its source is f lap(u - v)).")
OUT["numbers"]["A2"] = {k_: str(v_) for k_, v_ in dets.items()}
OUT["numbers"]["A2"]["V0+chi in G_loop"] = str(d_chi_G)
OUT["numbers"]["A2"]["CV3_Aplus_eta2_coefficient_at_test_points"] = coefv
P(f"  [{time.time() - T0:.0f}s]")


# ============================================================================================ B controls
banner("C1  CONTROL: at l = 0 this lane's code path returns DE12's committed c_gate and Gamma(k = 1/kpc)/H")
c1dev, c1rows = [], {}
for (z, Mb, foot) in GAL:
    bg0 = background(z, Mb, foot, 0.0, rg=np.geomspace(1.0, 2e4, 20000) * KPC)       # DE12's own grid
    tr = bg0["tr"]; t = bg0["t"]; m = (t > 0) & (t < 1)
    _, _, W2 = Wd(t)
    Aperp, Apar = nu_of(tr["y"]), nu_of(tr["y"]) + ynup_of(tr["y"])
    cg2 = np.maximum(np.maximum(tr["rho_b"] * tr["B"] * W2 * TU ** 2 * (bg0["C"] * 4 * math.pi * G * Aperp) ** 2,
                                tr["rho_b"] * tr["B"] * W2 * TU ** 2 * (bg0["C"] * 4 * math.pi * G * Apar) ** 2), 0.0)
    cmax = float(np.sqrt(np.max(cg2[m])))
    gH = (1 / KPC) * math.sqrt(max(cmax ** 2 - CS2, 0.0)) / tr["H"]
    ref = R12["budget"][KEY(z, Mb, foot)]
    c1dev += [abs(cmax / ref["c_gate_max"] - 1), abs(gH / ref["Gamma_over_H"] - 1)]
    c1rows[KEY(z, Mb, foot)] = dict(c_gate_kms=cmax / 1e3, Gamma_over_H_1kpc=gH)
bgc = background(0.25, 1e14, "canonical", 0.0, cap=True, rg=np.geomspace(1.0, 2e4, 20000) * KPC)
mc = (bgc["t"] > 0) & (bgc["t"] < 1)
cclu = float(np.sqrt(np.max(np.maximum(bgc["tr"]["c_gate2"]["perp"], bgc["tr"]["c_gate2"]["par"])[mc])))
c1dev.append(abs(cclu / R12["cluster_kappa"]["c_gate_max"] - 1))
P("    " + "; ".join(f"{k_}: {v_['c_gate_kms']:.0f} km/s, {v_['Gamma_over_H_1kpc']:.2e} H" for k_, v_ in list(c1rows.items())[:6]) + " ...")
check("C1 CONTROL: at l = 0 the smoothed-gate code path gives DE12's committed c_gate and Gamma(k = 1/kpc)/H on all 24 galaxy "
      "layers and its kappa-capped cluster's c_gate",
      f"max rel dev {max(c1dev):.1e} over {len(c1dev)} numbers (Gamma/H {min(v_['Gamma_over_H_1kpc'] for v_ in c1rows.values()):.1e}-"
      f"{max(v_['Gamma_over_H_1kpc'] for v_ in c1rows.values()):.1e}; capped cluster {cclu / 1e3:.0f} km/s)", max(c1dev) < 1e-12)
OUT["numbers"]["C1"] = c1rows

banner("C2  CONTROL: the radial smoothing solver, the point mass's Yukawa field, and the closed-form kernel")
rt = np.geomspace(1e-3, 50, 6000)
Ut = (1 / rt) ** 2 * np.exp(-(rt / 5) ** 2) / (1 + (0.01 / rt) ** 2)
c2 = {}
for lt in (0.05, 0.3, 1.0):
    ch = smooth_solve(rt, lt, Ut, bc1=Ut[-1])
    idx = np.where((rt > 0.3) & (rt < 5))[0][::100]
    c2[f"l={lt}"] = float(np.max(np.abs(ch[idx] / yukawa_exact(rt, Ut, lt, idx) - 1)))
# the point mass's field solves the homogeneous equation on the grid: residual of (1 - l^2 L) e^{-r/l}/r relative to its size
lt = 0.3; fpm = np.exp(-rt / lt) / rt
cpl, dia, den, wi = lap_parts(rt)
Lf = (dia * fpm + np.concatenate([cpl * fpm[1:], [0]]) + np.concatenate([[0], cpl * fpm[:-1]])) / den
res_pm = np.abs(fpm - lt ** 2 * Lf)[(rt > 0.05) & (rt < 3)] / fpm[(rt > 0.05) & (rt < 3)]
c2["point_mass_homogeneous_resid"] = float(np.max(res_pm))
yy = np.geomspace(1e-7, 0.5, 400)
c2["h_closed_form_vs_DE12_table"] = float(np.max(np.abs(h_an(yy) / h_of(yy) - 1)))
c2["A_par_closed_form_vs_DE12_table"] = float(np.max(np.abs((1 + h1_an(yy)) / (nu_of(yy) + ynup_of(yy)) - 1)))
P("    " + "; ".join(f"{k_}: {v_:.1e}" for k_, v_ in c2.items()))
check("C2 CONTROL: the FD Yukawa smoothing matches the exact spherical integral (<= 3e-3 at l/dr >= 5, <= 1e-4 for l >= 0.3); "
      "e^{-r/l}/r solves the homogeneous equation to the grid's accuracy; the closed-form kernel equals DE12's table below y = 0.5",
      c2, c2["l=0.05"] < 3e-3 and c2["l=0.3"] < 1e-4 and c2["l=1.0"] < 1e-4 and c2["point_mass_homogeneous_resid"] < 1e-3
      and c2["h_closed_form_vs_DE12_table"] < 1e-6 and c2["A_par_closed_form_vs_DE12_table"] < 1e-5)
OUT["numbers"]["C2"] = c2

banner("C3  CONTROL: T1 + T2 + T3 + T4 against finite differences of the discretised l = 0 functional")
GLx, GLw = np.polynomial.legendre.leggauss(8)


def dq(y, dy):
    """q(y + dy) - q(y) = 2 int_y^{y+dy} h(s) ds (8-point Gauss-Legendre)."""
    mid, half = y + 0.5 * dy, 0.5 * dy
    return 2 * half * np.sum(GLw * h_an(mid[..., None] + half[..., None] * GLx), axis=-1)


def functional_check(z, Mb, foot, l_kpc, Np=300, seed=3):
    """E(xi) = -sum w B(y) W(t(chi)) + sum w c_s^2 rho ln rho with the nonlinear phantom flux a0 h(g/a0), B from q, and
    chi = G_l U solved on the same grid; its second difference in eps against xi^T K xi."""
    bg = background(z, Mb, foot, l_kpc)
    Pp = layer_problem(z, Mb, foot, l_kpc, bg, Np=Np, variant="par", smooth_pert=True)
    r, ip, C, a0, rh = Pp["r"], Pp["ip"], Pp["C"], Pp["a0"], Pp["rh"]; l = l_kpc * KPC
    tr = transition_on(r, z, Mb, foot, W_M); trh = transition_on(rh, z, Mb, foot, W_M)
    rpn = r[ip]; dh = np.diff(rpn)
    wp = np.zeros(len(rpn)); wp[1:-1] = 0.5 * (rpn[2:] - rpn[:-2]); wp[0] = 0.5 * dh[0]; wp[-1] = 0.5 * dh[-1]
    g0n, g0h, rho_h = tr["y"] * a0, trh["y"] * a0, trh["rho_b"]
    _, _, wts, _ = lap_parts(r)
    U0 = (tr["t"] - 0.5) * 2 * W_M + 1
    bc0, bc1 = Pp["chi0"][0], Pp["chi0"][-1]
    qb = q_of(g0n / a0)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(3):
        c0, wd, kw = rng.uniform(0.2, 0.8), rng.uniform(0.05, 0.2), rng.uniform(3, 25)
        xs = (rh - rh[0]) / (rh[-1] - rh[0])
        xi = np.exp(-((xs - c0) / wd) ** 2) * np.cos(kw * xs)

        def E(e):
            dg = -4 * math.pi * G * rho_h * xi * e
            Fh = rh ** 2 * rho_h * xi * e
            drho = np.zeros(len(rpn)); drho[:-1] -= Fh; drho[1:] += Fh; drho /= rpn ** 2 * wp
            tot = rh ** 2 * (dg + a0 * (h_an((g0h + dg) / a0) - h_an(g0h / a0)))
            div = np.zeros(len(rpn)); div[:-1] += tot; div[1:] -= tot; div /= rpn ** 2 * wp
            U = U0.copy(); U[ip] += C * div
            ch = smooth_solve(r, l, U, bc0=bc0, bc1=bc1, inner="dirichlet") if l > 0 else U
            Wv = Wd((ch - 1) / (2 * W_M) + 0.5)[0]
            dgn = np.zeros(len(r)); dgp = np.zeros(len(rpn)); dgp[:-1] += 0.5 * dg; dgp[1:] += 0.5 * dg; dgn[ip] = dgp
            Bv = (a0 ** 2 / (8 * math.pi * G)) * (qb + dq(g0n / a0, dgn / a0))
            rho = tr["rho_b"][ip]
            return -np.sum(wts * Bv * Wv), np.sum(wts[ip] * CS2 * (rho + drho) * np.log((rho + drho) / rho))
        e1 = 1e-4 / max(float(np.max(np.abs(Pp["X"] @ xi))), 1e-300)
        (Ep, Gp), (Em, Gm), (E0_, G0_) = E(e1), E(-e1), E(0.0)
        fdg, fdgas = (Ep + Em - 2 * E0_) / e1 ** 2, (Gp + Gm - 2 * G0_) / e1 ** 2
        pt = {k_: -float(xi @ Pp[k_] @ xi) for k_ in ("T1", "T2", "T3", "T4")}
        scale = sum(abs(v_) for v_ in pt.values())                      # normalise by the terms' size (they can cancel)
        full, noexp = sum(pt.values()), pt["T1"] + pt["T4"]
        out.append((abs(fdg - full) / scale, abs(fdg - noexp) / scale, abs(fdgas / float(xi @ Pp["Kgas"] @ xi) - 1)))
    return out


c3 = {}
for (z, Mb, foot, fr) in ((0.25, 1e11, "canonical", 0.0), (0.25, 1e11, "canonical", 0.1), (2.5, 1e11, "alt", 0.1)):
    re_ = R12["budget"][KEY(z, Mb, foot)]["r_edge_kpc"]
    c3[f"{KEY(z, Mb, foot)} l={fr} r_e"] = functional_check(z, Mb, foot, fr * re_)
for k_, v_ in c3.items():
    P(f"    {k_}: with T2+T3 {', '.join(f'{a:.1e}' for a, _, _ in v_)}; without {', '.join(f'{b:.1e}' for _, b, _ in v_)}; "
      f"gas {', '.join(f'{c:.1e}' for _, _, c in v_)}")
c3ok = all(a < 1e-5 and c < 1e-6 for v_ in c3.values() for a, _, c in v_) and \
    all(max(b for _, b, _ in v_) >= 1e-3 for k_, v_ in c3.items() if "l=0.0" not in k_)
check("C3 CONTROL: T1 + T2 + T3 + T4 is the exact second variation of the discretised l = 0 functional (to 1e-5 of the terms' "
      "summed size, three random directions, l = 0 and l = 0.1 r_e); without the exposed terms T2 + T3 it misses by >= 1e-3 at l > 0",
      {k_: [f"{a:.1e}/{b:.1e}" for a, b, _ in v_] for k_, v_ in c3.items()}, c3ok,
      "the smoothing's own analogue of DE13's background term is T2 (the smoothed gate force times the phantom's curvature) "
      "together with the cross term T3; both are in every stability number below")
OUT["numbers"]["C3"] = {k_: v_ for k_, v_ in c3.items()}
P(f"  [{time.time() - T0:.0f}s]")

banner("C4  CONTROL: DE12's instability in this lane's discrete form at l = 0, and the discrete growth against WKB at small l")
c4_un, c4_gas, c4_wkb = [], [], {}
for (z, Mb, foot) in GAL:
    bg0 = background(z, Mb, foot, 0.0)
    Pp = layer_problem(z, Mb, foot, 0.0, bg0, Np=600, variant="par", smooth_pert=True)
    c4_un.append(lowest(Pp["K"], Pp["M"])[0] < 0)
    c4_gas.append(lowest(Pp["Kgas"], Pp["M"])[0] >= 0)
for (z, Mb, foot) in ((0.25, 1e11, "canonical"), (1.0, 1e12, "alt"), (2.5, 1e10, "canonical"), (4.0, 1e11, "alt")):
    re_ = R12["budget"][KEY(z, Mb, foot)]["r_edge_kpc"]
    lk = 0.02 * re_
    bgs = background(z, Mb, foot, lk)
    Pp = layer_problem(z, Mb, foot, lk, bgs, Np=900, variant="par", smooth_pert=True)
    ev = lowest(Pp["K"], Pp["M"])[0]
    gd = math.sqrt(-ev) / bgs["H"] if ev < 0 else 0.0
    gw = wkb_gamma(bgs, z, Mb, foot, lk, "par") / bgs["H"]
    c4_wkb[KEY(z, Mb, foot)] = (gd, gw)
P("    discrete vs WKB growth at l = 0.02 r_e (Gamma/H): " + "; ".join(f"{k_}: {a:.0f} vs {b:.0f}" for k_, (a, b) in c4_wkb.items()))
c4ok = all(c4_un) and all(c4_gas) and all(0.5 < a / b < 1.5 for a, b in c4_wkb.values())
check("C4 CONTROL: at l = 0 the discrete l = 0 sector has negative modes on every galaxy layer and gas alone none (DE12 in this "
      "lane's form); at l = 0.02 r_e the discrete growth is within 50% of the WKB rate max_k k sqrt(c^2/(1+l^2k^2)^2 - c_s^2)",
      f"unstable {sum(c4_un)}/{len(c4_un)}; gas stable {sum(c4_gas)}/{len(c4_gas)}; discrete/WKB "
      f"{', '.join(f'{a / b:.2f}' for a, b in c4_wkb.values())}", c4ok)
OUT["numbers"]["C4"] = {"discrete_vs_wkb_at_0.02re": c4_wkb}

# ============================================================================================ L1 the loop in V0 as written
banner("L1  V0 AS WRITTEN: U reads the phantom of the GATED w, so the gate sits inside the constraint that fixes what it reads")
L1rows = {}
MSCR = {"1/m = 0.2 Mpc": 1 / (200 * KPC), "1/m = 0.5 Mpc": 1 / (500 * KPC)}
for (z, Mb, foot) in GAL:
    bg0 = background(z, Mb, foot, 0.0)
    tr = bg0["tr"]; t = bg0["t"]; m = (t > 0) & (t < 1)
    hs = host(Mb, z)
    rr = bg0["r"]
    rho_nfw = hs["rho_s"] / ((rr / hs["rs"]) * (1 + rr / hs["rs"]) ** 2)
    Ub = bg0["C"] * 4 * math.pi * G * FB * rho_nfw                       # the baryon contrast lap(u - v) read by w's source
    W0, W1, _ = Wd(t)
    row = {}
    for lab, A in (("par", 1 + h1_an(tr["y"])), ("perp", nu_of(tr["y"]))):
        Gl_ = Ub * W1 * TU * (A - 1)
        row[f"Gmax_{lab}"] = float(np.max(Gl_[m]))
        row[f"frac_layer_above1_{lab}"] = float(np.mean(Gl_[m] > 1))
        for ml, mm in MSCR.items():                                     # invertible for all k iff (1 + M l)^2 > G_loop
            M_ = mm * np.sqrt(np.maximum(1 - W0, 1e-12))
            need = np.where(Gl_ > 1, (np.sqrt(np.maximum(Gl_, 1)) - 1) / M_, 0.0)
            row[f"l_invertible_{lab}_{ml}_kpc"] = float(np.max(need[m]) / KPC)
    L1rows[KEY(z, Mb, foot)] = row
g_min = min(min(v_["Gmax_par"], v_["Gmax_perp"]) for v_ in L1rows.values())
for k_, v_ in L1rows.items():
    if k_.endswith("canonical"):
        P(f"    {k_:22s}: max G_loop {v_['Gmax_par']:.2f} (radial A) / {v_['Gmax_perp']:.2f} (transverse A); share of the layer "
          f"above 1: {v_['frac_layer_above1_par']:.2f}/{v_['frac_layer_above1_perp']:.2f}; l needed for invertibility with "
          f"L361's screening: {v_['l_invertible_perp_1/m = 0.2 Mpc_kpc']:.0f} kpc (1/m 0.2 Mpc), "
          f"{v_['l_invertible_perp_1/m = 0.5 Mpc_kpc']:.0f} kpc (0.5 Mpc)")
check("L1 in V0 as written the loop gain G_loop = U_b W' t (A - 1) exceeds 1 inside every galaxy layer, for radial and "
      "transverse directions (baryon contrast, no screening credit): the constraint symbol vanishes inside every layer -- at "
      "l = 0 on surfaces, and for any l > 0 at k* = sqrt(G_loop - 1)/l unless (1 + M l)^2 > G_loop",
      f"min over the 24 layers of max G_loop = {g_min:.2f}; max {max(max(v_['Gmax_par'], v_['Gmax_perp']) for v_ in L1rows.values()):.1f}",
      g_min > 1.0,
      "a finding about V0, beyond DE12's reduction: DE12 (and the stability numbers below) price the gate reading an UNGATED "
      "phantom; with U reading w (gated) the static constraints are singular in every layer and smoothing cannot remove it")
OUT["numbers"]["L1_loop_gain"] = L1rows
P(f"  [{time.time() - T0:.0f}s]")


# ============================================================================================ C the main scans
def evo_rate(z, Mb, foot):
    """the layer's own evolution rate: the edge's motion across its own width, (1 + z) H |dr_e/dz| / L (the U-edge)."""
    dz = 0.02
    rs = []
    for zz in (z - dz, z + dz):
        e = edges(background(zz, Mb, foot, 0.0))
        rs.append(e[0.5])
    e0 = edges(background(z, Mb, foot, 0.0))
    L = e0[0.0] - e0[1.0]
    return (1 + z) * abs(rs[1] - rs[0]) / (2 * dz) / L, e0


def shifts(e, e0):
    """fractional shift of each edge radius; 1.0 (100%) if the region is gone."""
    return {lev: (abs(e[lev] / e0[lev] - 1) if (e[lev] is not None and e0[lev] is not None) else 1.0) for lev in (1.0, 0.5, 0.0)}


banner("R1  GROWTH vs l ON EVERY LAYER (per-layer l in units of its own edge radius r_e; 'par' = the exact l = 0 sector)")
FL = [0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0]
ROWS = {}
fmt = lambda g: ("gone" if g["G"] is None else (f"{g['G']:.1e}" + ("w" if g["how"] == "wkb" else "")))


def scan_layer(z, Mb, foot):
    rate, e0 = evo_rate(z, Mb, foot)
    re_ = e0[0.5]
    row = dict(r_e_kpc=re_, L_kpc=e0[0.0] - e0[1.0], evo_rate_over_H=rate, edges0=e0, grid={})
    for fr in FL:
        bg = background(z, Mb, foot, fr * re_)
        gp = gamma_at(z, Mb, foot, fr * re_, "par", bg=bg)
        gq = gamma_at(z, Mb, foot, fr * re_, "perp", bg=bg)
        row["grid"][fr] = dict(par=gp, perp=gq, shifts=shifts(edges(bg), e0))
    return row


for (z, Mb, foot) in GAL + CLU:
    key = KEY(z, Mb, foot)
    ROWS[key] = row = scan_layer(z, Mb, foot)
    P(f"    {key:22s} r_e {row['r_e_kpc']:6.0f} kpc, layer evolves at {row['evo_rate_over_H']:4.1f} H | Gamma/H par: " +
      " ".join(fmt(row["grid"][f]["par"]) for f in FL) + f"   [{time.time() - T0:.0f}s]")
P("    (columns: l/r_e = " + ", ".join(str(f) for f in FL) + "; 'w' = WKB where l < 5 cells)")


def refine(z, Mb, foot, re_, variant, crit, lo, hi, n=7):
    """bisection in log l between lo (fails crit) and hi (meets crit)."""
    for _ in range(n):
        mid = math.sqrt(lo * hi)
        g = gamma_at(z, Mb, foot, mid * re_, variant)
        if g["G"] is not None and crit(g):
            hi = mid
        else:
            lo = mid
    return hi


TH = {}


def thresholds(key, row):
    z, Mb, foot = float(key.split("/")[0]), float(key.split("/")[1]), key.split("/")[2]
    re_ = row["r_e_kpc"]
    th = {}
    for variant in ("par", "perp"):
        for cname, crit in (("H", lambda g: g["G"] <= 1.0), ("stable", lambda g: g["G"] == 0.0),
                            ("evo", lambda g, rr=row["evo_rate_over_H"]: g["G"] <= rr)):
            fr_hit = next((f for f in FL if row["grid"][f][variant]["G"] is not None and crit(row["grid"][f][variant])), None)
            if fr_hit is None:
                th[f"{cname}_{variant}"] = None
                continue
            i = FL.index(fr_hit)
            fr_ref = refine(z, Mb, foot, re_, variant, crit, FL[i - 1], fr_hit) if (i > 0 and Mb < 1e13) else fr_hit
            th[f"{cname}_{variant}"] = fr_ref
        gvals = [(f, row["grid"][f][variant]["G"]) for f in FL if row["grid"][f][variant]["G"] is not None]
        fmin, gmin = min(gvals, key=lambda p: p[1])
        th[f"Gmin_{variant}"] = (fmin, gmin)
    row["thresholds"] = th
    return th


for key, row in ROWS.items():
    TH[key] = thresholds(key, row)


def fmt_th(v):
    return "never (l <= r_e)" if v is None else f"{v:.3f}"


for key, th in TH.items():
    r_ = ROWS[key]
    P(f"    {key:22s} l/r_e for Gamma <= H: par {fmt_th(th['H_par'])}, perp {fmt_th(th['H_perp'])}; stable: par "
      f"{fmt_th(th['stable_par'])}, perp {fmt_th(th['stable_perp'])}; Gamma <= evolution rate ({r_['evo_rate_over_H']:.1f} H): par "
      f"{fmt_th(th['evo_par'])}; min Gamma/H par {th['Gmin_par'][1]:.2f} at {th['Gmin_par'][0]} r_e, perp {th['Gmin_perp'][1]:.2f}")
OUT["numbers"]["R1_per_layer"] = {k_: dict(r_e_kpc=v_["r_e_kpc"], L_kpc=v_["L_kpc"], evo_rate_over_H=v_["evo_rate_over_H"],
                                           thresholds=v_["thresholds"],
                                           grid={str(f): dict(par=v_["grid"][f]["par"], perp=v_["grid"][f]["perp"],
                                                              shifts=v_["grid"][f]["shifts"]) for f in FL})
                                  for k_, v_ in ROWS.items()}

banner("C5  CONTROL: the growth rates and thresholds are converged (grid points, domain margin)")
c5 = {}
for (key, fr) in ((KEY(0.25, 1e11, "canonical"), 0.1), (KEY(0.25, 1e11, "canonical"), 0.3), (KEY(2.5, 1e11, "canonical"), 0.1),
                  (KEY(1.0, 1e12, "alt"), 0.3)):
    z, Mb, foot = float(key.split("/")[0]), float(key.split("/")[1]), key.split("/")[2]
    lk = fr * ROWS[key]["r_e_kpc"]
    g6 = ROWS[key]["grid"][fr]["par"]["G"]
    g12 = gamma_at(z, Mb, foot, lk, "par", Np=1600)["G"]
    gm3 = gamma_at(z, Mb, foot, lk, "par", margin_l=9.0)["G"]
    gm2 = gamma_at(z, Mb, foot, lk, "par", margin_l=2.0)["G"]
    c5[f"{key} l={fr}r_e"] = dict(Np800=g6, Np1600=g12, margin9l=gm3, margin2l_first_run=gm2)
key = KEY(2.5, 1e11, "canonical"); z, Mb, foot = 2.5, 1e11, "canonical"
if TH[key]["stable_par"] is not None:
    hi = next(f for f in FL if f >= TH[key]["stable_par"]); lo = FL[FL.index(hi) - 1]
    for _ in range(7):
        mid = math.sqrt(lo * hi)
        if gamma_at(z, Mb, foot, mid * ROWS[key]["r_e_kpc"], "par", Np=1600)["G"] == 0.0:
            hi = mid
        else:
            lo = mid
    c5["stable threshold 2.5/1e11/canonical, Np 800 vs 1600"] = (TH[key]["stable_par"], hi)
else:
    c5["stable threshold 2.5/1e11/canonical, Np 800 vs 1600"] = None
for k_, v_ in c5.items():
    P(f"    {k_}: {v_}")
rel = lambda a, b: 0.0 if (a == 0 and b == 0) else abs(a - b) / max(abs(a), abs(b), 1e-300)
c5ok = all(rel(v_["Np800"], v_["Np1600"]) < 0.05 and rel(v_["Np800"], v_["margin9l"]) < 0.03 for k_, v_ in c5.items() if isinstance(v_, dict)) \
    and c5["stable threshold 2.5/1e11/canonical, Np 800 vs 1600"] is not None \
    and rel(*c5["stable threshold 2.5/1e11/canonical, Np 800 vs 1600"]) < 0.03
check("C5 CONTROL: Gamma/H with 1600 grid points is within 5% of 800, a 9 l domain margin within 3% of the 6 l used, and "
      "the stability threshold within 3% (the first development run's 2 l margin, reported, truncated the fastest mode)",
      {k_: (v_ if not isinstance(v_, dict) else {a: round(b, 3) for a, b in v_.items()}) for k_, v_ in c5.items()}, c5ok)
OUT["numbers"]["C5"] = c5

banner("R2  THE RESIDUAL MODE: which term drives it, against the gas's own MOND Jeans growth (T4, not a gate term)")
R2 = {}
for key in [KEY(0.25, 1e10, "canonical"), KEY(0.25, 1e11, "canonical"), KEY(0.25, 1e12, "alt"), KEY(1.0, 1e11, "canonical"),
            KEY(2.5, 1e11, "canonical"), KEY(4.0, 1e10, "alt")]:
    z, Mb, foot = float(key.split("/")[0]), float(key.split("/")[1]), key.split("/")[2]
    re_ = ROWS[key]["r_e_kpc"]
    for fr in (0.1, 0.3, 0.5):
        g = gamma_at(z, Mb, foot, fr * re_, "par", parts=True)
        R2[f"{key} l={fr}r_e"] = g
        if g["G"] is None:
            continue
        P(f"    {key:22s} l = {fr} r_e: Gamma/H all {g['G']:.2f} | gas + T1 alone {g.get('gas+T1', float('nan')):.2f}, + T2 "
          f"{g.get('gas+T2', float('nan')):.2f}, + T3 {g.get('gas+T3', float('nan')):.2f} | gas + T4 (MOND Jeans) "
          f"{g.get('gas+T4_MOND_Jeans', float('nan')):.2f}; mode at {g.get('mode_r_kpc', float('nan')):.0f} kpc, layer "
          f"{g.get('layer_kpc', (0, 0))[0]:.0f}-{g.get('layer_kpc', (0, 0))[1]:.0f} kpc")
OUT["numbers"]["R2_drivers"] = R2
P(f"  [{time.time() - T0:.0f}s]")

banner("R3  ONE CONSTANT l FOR EVERY LAYER: growth, edges, the KiDS lenses, the flagship radius and the Sun")
LU = [1.0, 3.0, 10.0, 20.0, 30.0, 50.0, 100.0, 150.0, 200.0, 300.0, 500.0, 700.0, 1000.0, 1500.0]
E0 = {KEY(*k_): ROWS[KEY(*k_)]["edges0"] for k_ in GAL}
UNI = {}
FLAG = [(1e10, f) for f in ("canonical", "alt")] + [(10 ** 10.5, f) for f in ("canonical", "alt")] + [(1e11, f) for f in ("canonical", "alt")]
for lk in LU:
    rowu = dict(layers={}, flagship={}, sun={})
    for (z, Mb, foot) in GAL:
        bg = background(z, Mb, foot, lk)
        g = gamma_at(z, Mb, foot, lk, "par", bg=bg)
        gq = gamma_at(z, Mb, foot, lk, "perp", bg=bg)
        rowu["layers"][KEY(z, Mb, foot)] = dict(par=g, perp=gq, shifts=shifts(edges(bg), E0[KEY(z, Mb, foot)]))
    for (Mb, foot) in FLAG:
        bg = background(2.5, Mb, foot, lk)
        a0 = A0[foot]; rF = math.sqrt(G * Mb * MS / (0.1 * a0))
        tF = float(np.interp(rF, bg["r"], bg["t"]))
        dXi = np.gradient(bg["Xi"], bg["r"])
        yF = 0.1
        aU = 4 * math.pi * G * bg["C"] * float(np.interp(rF, bg["r"], dXi))
        aA = aU * float(1 + h1_an(np.array([yF]))[0])
        gM = float(nu_of(yF)) * yF * a0
        Wf_ = float(Wd(np.array([tF]))[0][0])
        g_in = (1 + Wf_ * (float(nu_of(yF)) - 1)) * yF * a0 - aA
        rowu["flagship"][f"{Mb:.2e}/{foot}"] = dict(t_rF=tF, on=bool(tF >= 1), gate_force_over_g=aA / gM, u_channel_over_g=aU / gM,
                                                   shift_dex=2 * math.log10(max(g_in / gM, 1e-300)))
    bg = background(0.0, 6e10, "canonical", lk)
    rS = 8 * KPC; tS = float(np.interp(rS, bg["r"], bg["t"]))
    yS = G * 6e10 * MS / (rS ** 2 * A0["canonical"])
    aS = 4 * math.pi * G * bg["C"] * float(np.interp(rS, bg["r"], np.gradient(bg["Xi"], bg["r"]))) * float(1 + h1_an(np.array([yS]))[0])
    rowu["sun"] = dict(t=tS, on=bool(tS >= 1), gate_force_over_g=aS / (float(nu_of(yS)) * yS * A0["canonical"]))
    UNI[lk] = rowu
    gz = lambda zz: max(((v_["par"]["G"] if v_["par"]["G"] is not None else 0.0) for k_, v_ in rowu["layers"].items()
                        if k_.startswith(f"{zz}/")), default=float("nan"))
    kids = max(max(rowu["layers"][KEY(0.25, 1e11, f)]["shifts"][0.5], rowu["layers"][KEY(0.25, 1e11, f)]["shifts"][0.0])
               for f in ("canonical", "alt"))
    z4 = max(max(v_["shifts"].values()) for k_, v_ in rowu["layers"].items() if k_.startswith("4.0/"))
    fl_on = all(v_["on"] for v_ in rowu["flagship"].values())
    fl_sh = max(abs(v_["shift_dex"]) for v_ in rowu["flagship"].values())
    gone = [k_ for k_, v_ in rowu["layers"].items() if v_["par"]["G"] is None]
    gE = max((v_["par"]["G"] or 0.0) / ROWS[k_]["evo_rate_over_H"] for k_, v_ in rowu["layers"].items())
    P(f"    l = {lk:6.0f} kpc: max Gamma/H par  z=0.25 {gz(0.25):9.2e}  z=1 {gz(1.0):9.2e}  z=2.5 {gz(2.5):9.2e}  z=4 {gz(4.0):9.2e} "
      f"(max Gamma/evolution rate {gE:8.2e}; regions gone: {len(gone)}) | "
      f"KiDS edge shift {kids:6.1%} | z = 4 edges {z4:6.1%} | flagship on at r_F: {fl_on} (|shift| <= {fl_sh:.3f} dex) | "
      f"Sun on: {rowu['sun']['on']} (gate force {rowu['sun']['gate_force_over_g']:.1e} g)   [{time.time() - T0:.0f}s]")
    rowu["summary"] = dict(maxG_par={str(zz): gz(zz) for zz in (0.25, 1.0, 2.5, 4.0)}, max_G_over_evo=gE, regions_gone=gone,
                           kids_shift=kids, z4_shift=z4,
                           flagship_on=fl_on, flagship_max_shift_dex=fl_sh)
OUT["numbers"]["R3_one_constant_l"] = {str(k_): v_ for k_, v_ in UNI.items()}

banner("R4  THE KAPPA CAP WITH chi (MS5): chi = G_l(U_cap); the capped branch's k^0 term Xi U_rhorho is not smoothed away")
R4 = {}
for (z, lab) in ((0.25, "DE12 G6 cluster, z = 0.25"), (0.5, "MS3's shear cap epoch, z = 0.5")):
    e_cap0 = None
    for lk in (0.0, 10.0, 30.0, 100.0, 300.0, 1000.0):
        bg = background(z, 1e14, "canonical", lk, cap=True)
        tr = bg["tr"]; t = bg["t"]; m = (t > 0) & (t < 1)
        e = edges(bg)
        if lk == 0.0:
            e_cap0 = e
            lcap = V_CAP / (tr["H"] * math.sqrt(tr["xce"])) / KPC
        Aperp = nu_of(tr["y"])
        Urr = V_CAP ** 2 * (4 * math.pi * G * Aperp) ** 2 / (2 * tr["g"] ** 2 * tr["H"] ** 2 * tr["xce"])
        crr = float(np.sqrt(np.max((tr["rho_b"] * bg["Xi"] * Urr)[m]))) if m.any() else 0.0
        R4[f"{lab} l={lk}"] = dict(edge_half_kpc=e[0.5], l_cap_kpc=lcap, shift=shifts(e, e_cap0)[0.5],
                                   cap_active=float(np.mean(tr["use_kap"][m])) if m.any() else None, c_rhorho_kms=crr / 1e3)
        P(f"    {lab}, l = {lk:6.0f} kpc: edge {e[0.5]:.0f} kpc (l_cap {lcap:.0f} kpc; shift {shifts(e, e_cap0)[0.5]:.1%}); cap active on "
          f"{R4[f'{lab} l={lk}']['cap_active']:.2f} of the layer; k^0 term c_rhorho = sqrt(rho Xi U_rhorho) = {crr / 1e3:.0f} km/s "
          f"(1e6 K gas 117, ICM ~1000)")
OUT["numbers"]["R4_kappa_cap"] = R4
P(f"  [{time.time() - T0:.0f}s]")

banner("R5  (not pre-declared) A SMOOTHING LENGTH THAT DEPENDS ON COSMIC TIME ONLY, l(z): still linear on each leaf")
R5 = {}
EXTRA = [(0.0, Mb, f) for Mb in (1e10, 1e11, 1e12) for f in ("canonical", "alt")]
for (z, Mb, foot) in EXTRA:
    key = KEY(z, Mb, foot)
    ROWS[key] = scan_layer(z, Mb, foot)
    TH[key] = thresholds(key, ROWS[key])
for zz in (0.0, 0.25, 1.0, 2.5, 4.0):
    keys = [k_ for k_ in ROWS if k_.startswith(f"{zz}/") and "1e+14" not in k_]
    lev = [TH[k_]["evo_par"] * ROWS[k_]["r_e_kpc"] if TH[k_]["evo_par"] is not None else float("inf") for k_ in keys]
    lH = [TH[k_]["H_par"] * ROWS[k_]["r_e_kpc"] if TH[k_]["H_par"] is not None else float("inf") for k_ in keys]
    l_evo = max(lev)
    trz = transition(zz if zz > 0 else 1e-6, 1e11, "canonical", W_M)
    lcap = V_CAP / (trz["H"] * math.sqrt(trz["xce"])) / KPC
    row = dict(l_evo_kpc=l_evo, l_H_kpc=max(lH), l_cap_kpc=lcap, l_evo_over_lcap=l_evo / lcap, layers={})
    if not math.isfinite(l_evo):
        R5[str(zz)] = row
        P(f"    z = {zz}: no l <= r_e brings every layer to Gamma <= its evolution rate")
        continue
    for k_ in keys:
        z_, Mb_, f_ = float(k_.split("/")[0]), float(k_.split("/")[1]), k_.split("/")[2]
        bg = background(z_, Mb_, f_, l_evo)
        g = gamma_at(z_, Mb_, f_, l_evo, "par", bg=bg)
        row["layers"][k_] = dict(G_over_H=g["G"], G_over_evo=(g["G"] or 0.0) / ROWS[k_]["evo_rate_over_H"],
                                 edge_shift=max(shifts(edges(bg), ROWS[k_]["edges0"]).values()))
    for Mb_, f_ in ((1e9, "canonical"), (1e9, "alt")):                    # a dwarf's region under the same l(z)
        e0 = edges(background(zz, Mb_, f_, 0.0)); e1 = edges(background(zz, Mb_, f_, l_evo))
        row["layers"][f"dwarf {KEY(zz, Mb_, f_)} (edges only)"] = dict(edge_shift=max(shifts(e1, e0).values()), r_e0_kpc=e0[0.5])
    if zz == 2.5:
        fl = {}
        for (Mb_, f_) in FLAG:
            bg = background(2.5, Mb_, f_, l_evo)
            rF = math.sqrt(G * Mb_ * MS / (0.1 * A0[f_]))
            fl[f"{Mb_:.2e}/{f_}"] = float(np.interp(rF, bg["r"], bg["t"]))
        row["flagship_t_rF"] = fl
    if zz == 0.0:
        bg = background(0.0, 6e10, "canonical", l_evo)
        row["sun_t"] = float(np.interp(8 * KPC, bg["r"], bg["t"]))
    R5[str(zz)] = row
    worst = max(v_["edge_shift"] for k_, v_ in row["layers"].items() if not k_.startswith("dwarf"))
    kid = max((row["layers"][KEY(zz, 1e11, f_)]["edge_shift"] for f_ in ("canonical", "alt")), default=None) if zz == 0.25 else None
    dw = max(v_["edge_shift"] for k_, v_ in row["layers"].items() if k_.startswith("dwarf"))
    gmax = max((v_["G_over_H"] or 0.0) for k_, v_ in row["layers"].items() if not k_.startswith("dwarf"))
    P(f"    z = {zz}: l(z) = {l_evo:6.0f} kpc (= {l_evo / lcap:.3f} of MS5's l_cap {lcap:.0f} kpc; Gamma <= H would need "
      f"{max(lH):.0f} kpc): max Gamma/H {gmax:.2f}; worst edge shift 1e10-1e12 {worst:.1%}; 1e9 dwarfs {dw:.1%}" +
      (f"; the KiDS lenses (1e11) {kid:.1%}" if kid is not None else "") +
      (f"; flagship t(r_F) min {min(row['flagship_t_rF'].values()):.2f}" if zz == 2.5 else "") +
      (f"; the Sun t = {row['sun_t']:.3g}" if zz == 0.0 else ""))
OUT["numbers"]["R5_l_of_z"] = R5
P(f"  [{time.time() - T0:.0f}s]")

# ============================================================================================ S H verdicts
banner("S1 H1 H2  VERDICTS")
s1 = {k_: min((ROWS[k_]["grid"][f]["par"]["G"] for f in FL if ROWS[k_]["grid"][f]["par"]["G"] is not None), default=float("inf"))
      for k_ in (KEY(*g_) for g_ in GAL)}
check("S1 [MUTATE's target] the smoothing is effective: on every galaxy layer the gate-driven growth of the exact l = 0 sector "
      "falls from DE12's 1e3-1e5 H to <= 10 H at some l <= r_e",
      f"min over l of Gamma/H per layer: {min(s1.values()):.2f}-{max(s1.values()):.2f}", max(s1.values()) <= 10.0,
      "the UV catastrophe is gone: what remains lives at the layer's own scale")
h1rows, h1ok = {}, True
for (z, Mb, foot) in GAL:
    key = KEY(z, Mb, foot); th = TH[key]["H_par"]
    if th is None or th > H1_LMAX_OVER_RE:
        h1rows[key] = dict(l_over_re=th, edge_shift=None, ok=False); h1ok = False; continue
    sh = shifts(edges(background(z, Mb, foot, th * ROWS[key]["r_e_kpc"])), ROWS[key]["edges0"])
    ok_ = max(sh.values()) < EDGE_TOL
    h1rows[key] = dict(l_over_re=th, edge_shift=max(sh.values()), ok=ok_); h1ok &= ok_
nfail = [k_ for k_, v_ in h1rows.items() if not v_["ok"]]
check("H1 [pre-declared] on every galaxy layer some l <= 0.3 r_e brings Gamma <= H(z) (exact l = 0 sector) with that layer's "
      "own edges moved < 10%", f"{len(GAL) - len(nfail)}/{len(GAL)} layers; failing: {', '.join(nfail) if nfail else 'none'}",
      h1ok, "per layer only: l is one constant of the action, so H1 is necessary, not sufficient (H2)")
OUT["numbers"]["H1"] = h1rows
h2 = {}
for lk, rowu in UNI.items():
    allH = all((v_["par"]["G"] or 0.0) <= 1.0 for v_ in rowu["layers"].values())
    h2[lk] = dict(all_layers_Gamma_le_H=allH, kids_ok=rowu["summary"]["kids_shift"] < EDGE_TOL,
                  flagship_on=rowu["summary"]["flagship_on"], sun_on=rowu["sun"]["on"])
h2ok = any(all(v_.values()) for v_ in h2.values())
lowG = next((lk for lk in LU if all((v_["par"]["G"] or 0.0) <= 10 for v_ in UNI[lk]["layers"].values())), None)
lowE = next((lk for lk in LU if UNI[lk]["summary"]["max_G_over_evo"] <= 1.0), None)
highF = max((lk for lk in LU if UNI[lk]["summary"]["flagship_on"] and UNI[lk]["summary"]["flagship_max_shift_dex"] <= 0.10
             and UNI[lk]["summary"]["kids_shift"] < EDGE_TOL and UNI[lk]["sun"]["on"]), default=None)
highZ4 = max((lk for lk in LU if UNI[lk]["summary"]["z4_shift"] < EDGE_TOL), default=None)
check("H2 [pre-declared] one constant l brings all 24 galaxy layers to Gamma <= H while the KiDS edges move < 10% and MOND stays "
      "on at r_F (z = 2.5) and at the Sun",
      f"no l in {LU[0]:.0f}-{LU[-1]:.0f} kpc has all four (all layers <= H at: "
      f"{[lk for lk, v_ in h2.items() if v_['all_layers_Gamma_le_H']] or 'none'}); the pincer: every layer <= 10 H needs "
      f"l >= {lowG} kpc (<= its own evolution rate: l >= {lowE} kpc), while the flagship (with KiDS and the Sun) holds only to "
      f"l = {highF} kpc and the z = 4 regions' edges stay within 10% only to l = {highZ4} kpc" if not h2ok else
      f"passing l: {[lk for lk, v_ in h2.items() if all(v_.values())]}", h2ok)
OUT["numbers"]["H2"] = {str(k_): v_ for k_, v_ in h2.items()}
OUT["numbers"]["pincer"] = dict(l_all_layers_le_10H_kpc=lowG, l_all_layers_le_evo_rate_kpc=lowE,
                                l_max_flagship_kids_sun_kpc=highF, l_max_z4_edges_10pc_kpc=highZ4)

nlb = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
json.dump(OUT, open(fn, "w"), indent=1, default=str)
P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb} "
  f"({', '.join(n_.split()[0] for n_, ok, lb in CH if lb and not ok) or 'none'}); wrote {os.path.basename(fn)}   [{time.time() - T0:.0f}s]")
sys.exit(1 if nlb else 0)
