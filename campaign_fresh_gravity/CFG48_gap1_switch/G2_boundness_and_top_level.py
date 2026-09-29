#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
G2 -- OWNERSHIP AS A NONLOCAL FUNCTIONAL: energy boundness, monotone boundness functionals, the top-level (maximal-ball) functional, and
     what none of them can carry (history).   Tasks (1) and (2) of GATES_FROZEN.md; gates GC, GD, GA, GF, GG(i), GG(ii).

D1  Energy boundness on the BARYON potential.  A baryon element on the circular orbit of the law, E_b = (1/2) V_c^2 + Phi_N (Phi_N = -G M_b/r),
    is bound iff M_dyn(<r)/M_b < 2.  For the point-mass P2 law M_dyn = M_b sqrt(1 + (r/r_M)^2), so the edge is r_0 = sqrt(3) r_M exactly; for
    nu_mono it is solved.  Compared with the declared edge r_e = 0.4 r_ta (GE window 0.31-0.48).  The phantom-inclusive potential is bound
    everywhere inside whatever reference shell is chosen (log potential): its edge is the reference itself (r_ta), which is not a baryon-state
    function (computed as the second reading; it is also the MUTATE).
D2  The three MONOTONE boundness functionals (energy E_b < 0, enclosed mean baryon overdensity U above the edge threshold, expansion theta <= 0)
    evaluated at the Sun's own centre (1 AU) and at the Sun's Galactic position (8 kpc): all three are ON at the Sun with margins of ~17-25
    orders of magnitude, so a monotone functional gives the Sun its own phantom (CFG7 H1: the strict law is 4.0-5.7x over the Cassini ceiling).
    Top-level status is therefore not monotone: it needs an outward-looking maximum.
D3  The maximal-ball functional (the candidate that can detect top-level): M_top(x) = largest baryon mass in a ball containing x whose mean
    baryon overdensity is >= Delta_edge = Delta_ta/x_e^3 (x_e = 0.4, B's declared value), balls of any centre and radius (sup over centres:
    origin-free).  Point-mass tests: (a) the Sun-like clump and its host give the same M_top (one top-level system; the clump owns no phantom of
    its own); (b) the ball boundary of an isolated system with all its baryons retained is r_e = 0.4 r_ta exactly (Delta_edge = Delta_ta/x_e^3
    and M_col = M_b/f_b), so the source-confined edge costs no constant beyond B's declared x_e; (c) translation invariance of M_top; (d) MERGER JUMP:
    two equal systems at separation d: M_top jumps from M to 2M at d_c = 2^(4/3) R_1 (a fold), so the functional has a jump discontinuity at
    every merger and needs a smoothing width (a new constant) to be varied; (e) the functional gives the SAME value to an accreted satellite and to a
    formed-embedded tidal dwarf with the same baryon state: it cannot carry ownership by history.
D4  The size of what (e) must distinguish: M_dyn/M_b for a dwarf of M_b = 1e6, 1e7, 1e8 at r = 1 kpc: isolated law (accreted, keeps its infall halo)
    against Newtonian (formed embedded).
MUTATE=1 uses the phantom-inclusive potential with the r_ta reference in D1: the "edge at sqrt(3) r_M" claim must FAIL.
SCOPE.  Point masses / circular orbits in the law's field, P2 and nu_mono kernels; balls in flat 3-space (the leaf geometry); z = 0.
"""
import os, sys, math, itertools
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Gcommon import *   # noqa

MUTATE = os.environ.get("MUTATE", "0") == "1"
R = Report("G2_boundness_and_top_level", MUTATE)
P = R.P
P(__doc__.strip())
if MUTATE:
    P("\n  *** MUTATE=1: D1 uses the phantom-inclusive potential (reference r_ta); 'edge at sqrt(3) r_M' must FAIL ***")

XE = 0.4
DELTA_EDGE = DELTA_TA / XE ** 3                  # mean overdensity (in the cosmic mean) at the declared edge
RHO_B_BAR = FB_COSMIC * OM * RHOC0_MPC / 1e9     # cosmic baryon density, Msun / kpc^3

# =================================================================================================== D1
R.banner("D1  energy boundness on the baryon potential: the edge sits at sqrt(3) r_M, far inside r_e = 0.4 r_ta")
D1 = {}
ok_exact = True
for kname, kern in (("P2", nu_p2), ("nu_mono", nu_mono)):
    # E_b = 0  <=>  M_dyn/M_b = nu(y) = 2 with y = g_N/a0 = (r_M/r)^2
    y0 = brentq(lambda ly: float(kern(math.exp(ly))) - 2.0, math.log(1e-4), math.log(1e3), xtol=1e-14)
    x0 = 1.0 / math.sqrt(math.exp(y0))
    D1[kname] = dict(x0=x0)
    P(f"    {kname:8s}: nu(y) = 2 at y = {math.exp(y0):.5f}  =>  r_0 = {x0:.5f} r_M" + ("   (sqrt(3) = 1.73205)" if kname == "P2" else ""))
ok_exact = abs(D1["P2"]["x0"] - math.sqrt(3.0)) < 1e-9
rows = []
for Mb in (1e10, 1e11, 1e12):
    rM = r_M_kpc(Mb); rta = r_ta_kpc(Mb); re = XE * rta
    r0 = D1["P2"]["x0"] * rM
    # reading 2 (the MUTATE): phantom-inclusive potential, reference shell r_ta; circular orbit of the P2 point-mass law; E(r) = V^2/2 + Phi(r) - Phi(r_ta)
    rr = np.geomspace(1e-3 * rM, rta, 200001)
    g = np.sqrt((G * Mb / rr ** 2) ** 2 + A0 * G * Mb / rr ** 2)
    Phi = np.concatenate([[0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(rr))])
    E = 0.5 * g * rr + (Phi - Phi[-1])
    idx = np.where(E < 0)[0]
    r0_ph = float(rr[idx[-1]]) if len(idx) else float("nan")            # outermost radius with E<0 is r_ta side; find zero crossing from outside
    zc = np.where(np.diff(np.sign(E)) != 0)[0]
    r0_ph = float(rr[zc[-1]]) if len(zc) else float("nan")
    rows.append(dict(Mb=Mb, r_M=rM, r_ta=rta, r_e=re, r0_baryon=r0, r0_over_re=r0 / re, r0_phantom_ref_rta_over_rta=r0_ph / rta))
    P(f"    M_b = {Mb:.0e}: r_M = {rM:5.1f} kpc, r_ta = {rta:7.1f}, r_e = {re:6.1f} kpc;  E_b<0 edge {r0:6.1f} kpc = {r0 / re:.3f} r_e;"
      f"   phantom-inclusive potential, E = 0 at {r0_ph / rta:.3f} r_ta (reference-dependent; needs r_ta)")
R.num("D1", dict(kernels=D1, rows=rows))
if MUTATE:
    claim = all(abs(r["r0_phantom_ref_rta_over_rta"] * r["r_ta"] / r["r_M"] - math.sqrt(3.0)) < 1e-3 for r in rows)
else:
    claim = ok_exact and all(r["r0_over_re"] < 0.15 for r in rows)
R.check("D1 the baryon-potential boundness edge is r_0 = sqrt(3) r_M (P2, exact) and sits below 0.15 r_e for M_b = 1e10, 1e11, 1e12 (the law is verified far beyond it)",
        f"r_0/r_e = {[round(r['r0_over_re'], 3) for r in rows]}; nu_mono r_0 = {D1['nu_mono']['x0']:.3f} r_M" + ("  [MUTATE: phantom-inclusive potential]" if MUTATE else ""), claim)
R.verdict("GE / energy boundness (baryon potential)", "FAIL", f"edge at {min(r['r0_over_re'] for r in rows):.2f}-{max(r['r0_over_re'] for r in rows):.2f} of r_e; the phantom-inclusive potential has no edge without the reference r_ta (history / cosmology, not a state function)")

# =================================================================================================== D2
R.banner("D2  monotone boundness functionals are ON at the Sun (ownership inversion)")
AU_KPC = 1.495978707e11 / KPC_M
rho_m_kpc = OM * RHOC0_MPC / 1e9
M_sun_ = 1.0
r_au = 1.0 * AU_KPC
E_sun = -0.5 * G * M_sun_ / r_au                          # (km/s)^2, circular Keplerian orbit at 1 AU, E = -GM/2r  (Newtonian, y >> 1)
U_sun = (3 * M_sun_ / (4 * math.pi * r_au ** 3)) / (FB_COSMIC * rho_m_kpc)
Mb_mw, r_mw = 5.0e10, 8.0
yMW = G * Mb_mw / r_mw ** 2 / A0
E_mw = 0.5 * float(nu_p2(yMW)) * G * Mb_mw / r_mw - G * Mb_mw / r_mw
U_mw = (3 * Mb_mw / (4 * math.pi * r_mw ** 3)) / (FB_COSMIC * rho_m_kpc)
P(f"    Sun at 1 AU:        E_b = {E_sun:.3e} (km/s)^2 (<0: bound);  U = {U_sun:.2e} x cosmic baryon density  (edge threshold {DELTA_EDGE:.1f});  theta_b <= 0 by definition of bound (not computed)")
P(f"    Sun at 8 kpc (MW):  E_b = {E_mw:.3e} (km/s)^2 (<0: bound);  U(<8 kpc) = {U_mw:.2e} x cosmic;  y = g_N/a0 = {yMW:.2f}")
P(f"    U_sun / U_threshold = {U_sun / DELTA_EDGE:.1e};   U_sun / U_MW = {U_sun / U_mw:.1e}")
d2_ok = (E_sun < 0) and (E_mw < 0) and (U_sun > DELTA_EDGE) and (U_mw > DELTA_EDGE) and (U_sun / U_mw > 1e10)
R.check("D2 the energy and overdensity functionals are ON at the Sun's own centre (the turnaround functional theta_b <= 0 holds by definition for a bound virialised clump; not computed), with the overdensity margin over the MW's ~1e17",
        f"E_sun<0 {E_sun < 0}; U_sun/U_threshold = {U_sun / DELTA_EDGE:.1e}; U_sun/U_MW = {U_sun / U_mw:.1e}", d2_ok)
R.verdict("GG(ii) / monotone functionals", "FAIL", "every monotone-in-overdensity gate is ON at the Sun; the embedded system gets its own phantom (strict law 4.0-5.7x over the Cassini ceiling, CFG7 H1)")

# =================================================================================================== D3 maximal-ball functional
R.banner("D3  the maximal-ball (top-level) functional on point-mass configurations")


def min_enclosing_ball(pts):
    pts = [np.asarray(p, float) for p in pts]
    if len(pts) == 1:
        return pts[0], 0.0
    best = None
    for a, b in itertools.combinations(range(len(pts)), 2):
        c = 0.5 * (pts[a] + pts[b]); rad = 0.5 * np.linalg.norm(pts[a] - pts[b])
        if all(np.linalg.norm(p - c) <= rad * (1 + 1e-12) for p in pts) and (best is None or rad < best[1]):
            best = (c, rad)
    if len(pts) >= 3:
        for a, b, cc in itertools.combinations(range(len(pts)), 3):
            A_, B_, C_ = pts[a], pts[b], pts[cc]
            ab, ac = B_ - A_, C_ - A_
            n = np.cross(ab, ac); n2 = float(np.dot(n, n))
            if n2 < 1e-30:
                continue
            c = A_ + (np.dot(ac, ac) * np.cross(n, ab) + np.dot(ab, ab) * np.cross(ac, n)) / (2 * n2)
            rad = np.linalg.norm(c - A_)
            if all(np.linalg.norm(p - c) <= rad * (1 + 1e-12) for p in pts) and (best is None or rad < best[1]):
                best = (c, rad)
    return best


def M_top(idx, masses, pos, delta=DELTA_EDGE, rho_b=RHO_B_BAR):
    """largest baryon mass in a subset S (containing mass idx) whose minimal enclosing ball can be enlarged to the threshold Ubar = delta:
    exists iff R_S <= R_max(S) = (3 M_S/(4 pi rho_b delta))^(1/3).  Point masses; exact for these configurations (Ubar decreases with R)."""
    n = len(masses); best = 0.0; who = None
    for k in range(1, n + 1):
        for S in itertools.combinations(range(n), k):
            if idx not in S:
                continue
            MS = sum(masses[i] for i in S)
            c, rad = min_enclosing_ball([pos[i] for i in S])
            Rmax = (3 * MS / (4 * math.pi * rho_b * delta)) ** (1 / 3)
            if rad <= Rmax and MS > best:
                best, who = MS, S
    return best, who


# (a) host + Sun-like clump + a separate isolated dwarf
M_H, m_cl, M_dw = 5.0e10, 1.0, 1.0e8
pos = [np.array([0.0, 0, 0]), np.array([8.0, 0, 0]), np.array([1500.0, 0, 0])]
masses = [M_H, m_cl, M_dw]
Mt_host, s_host = M_top(0, masses, pos)
Mt_clump, s_clump = M_top(1, masses, pos)
Mt_dw, s_dw = M_top(2, masses, pos)
P(f"    (a) host {M_H:.0e}, clump (1 Msun) at 8 kpc, isolated dwarf {M_dw:.0e} at 1.5 Mpc:  M_top(host) = {Mt_host:.6e} {s_host}, M_top(clump) = {Mt_clump:.6e} {s_clump}, M_top(dwarf) = {Mt_dw:.3e} {s_dw}")
a_ok = abs(Mt_host - Mt_clump) / Mt_host < 1e-12 and Mt_dw == M_dw and abs(Mt_host - (M_H + m_cl)) < 1e-6
R.check("D3a the clump inside the host shares the host's M_top (it owns no phantom of its own); an isolated dwarf is its own top level", f"M_top host/clump/dwarf = {Mt_host:.6e} / {Mt_clump:.6e} / {Mt_dw:.3e}", a_ok)
# (b) the ball boundary = r_e for an isolated system with all baryons retained
b_rows = []
for Mb in (1e10, 1e11, 1e12):
    Rthr = (3 * Mb / (4 * math.pi * RHO_B_BAR * DELTA_EDGE)) ** (1 / 3)
    re = XE * r_ta_kpc(Mb)
    b_rows.append((Mb, Rthr, re, Rthr / re))
    P(f"    (b) M_b = {Mb:.0e}: ball boundary R_thr = {Rthr:8.3f} kpc vs r_e = 0.4 r_ta = {re:8.3f} kpc: ratio {Rthr / re:.6f}")
b_ok = all(abs(r[3] - 1) < 2e-3 for r in b_rows)
R.check("D3b the top-level ball boundary of an isolated, fully baryon-retaining system is r_e = 0.4 r_ta (Delta_edge = Delta_ta/x_e^3): no constant beyond B's declared x_e", f"ratios {[round(r[3], 6) for r in b_rows]}", b_ok)
# (c) translation invariance
sh = np.array([123.4, -55.0, 7.0])
Mt2, _ = M_top(1, masses, [p + sh for p in pos])
c_ok = abs(Mt2 - Mt_clump) / Mt_clump < 1e-12
R.check("D3c M_top is translation invariant (sup over all centres: no origin, no system-centre coordinate)", f"{Mt2:.6e} vs {Mt_clump:.6e}", c_ok)
# (d) merger jump
M1 = 1e10
R1 = (3 * M1 / (4 * math.pi * RHO_B_BAR * DELTA_EDGE)) ** (1 / 3)
ds = np.linspace(1.5 * R1, 3.5 * R1, 4001)
vals = []
for d in ds:
    v, _ = M_top(0, [M1, M1], [np.array([0.0, 0, 0]), np.array([d, 0, 0])])
    vals.append(v)
vals = np.array(vals)
jump_idx = np.where(np.diff(vals) != 0)[0]
dc = float(ds[jump_idx[0]]) if len(jump_idx) else float("nan")
P(f"    (d) two equal systems (1e10): M_top(1) jumps from {vals[0]:.2e} to {vals[-1]:.2e} at d_c = {dc / R1:.4f} R_1  (analytic 2^(4/3) = {2 ** (4 / 3):.4f});  jump ratio {vals[0] / vals[-1]:.3f}")
d_ok = len(jump_idx) == 1 and abs(dc / R1 - 2 ** (4 / 3)) < 2e-3 * 2 and abs(vals[0] / vals[-1] - 2.0) < 1e-9
R.check("D3d M_top has a jump (fold) of a factor 2 at d_c = 2^(4/3) R_1: a Lagrangian term built from it has a delta-function variation at every merger unless a smoothing width is introduced",
        f"one jump at d_c/R_1 = {dc / R1:.4f}; ratio {vals[0] / vals[-1]:.3f}", d_ok)
# (e) same state -> same value: an accreted satellite and a formed-embedded tidal dwarf with the same baryon state and position
Ms = 1e7
pos_s = [np.array([0.0, 0, 0]), np.array([60.0, 0, 0])]
Mt_acc, _ = M_top(1, [M_H, Ms], pos_s)
Mt_tdg, _ = M_top(1, [M_H, Ms], pos_s)
e_ok = Mt_acc == Mt_tdg
R.check("D3e the functional assigns identical values to an accreted satellite and a formed-embedded tidal dwarf with the same baryon state (it reads no history)", f"{Mt_acc:.6e} == {Mt_tdg:.6e}", e_ok)

# =================================================================================================== D4
R.banner("D4  what (e) must distinguish: isolated law (accreted) vs Newtonian (formed embedded) for the same baryons")
D4 = {}
for Mb in (1e6, 1e7, 1e8):
    r1 = 1.0
    y = G * Mb / r1 ** 2 / A0
    D4[f"{Mb:.0e}"] = dict(y=y, Mdyn_over_Mb_P2=float(nu_p2(y)), Mdyn_over_Mb_numono=float(nu_mono(y)))
    P(f"    M_b = {Mb:.0e} at 1 kpc: y = {y:.4f}; M_dyn/M_b isolated law {float(nu_p2(y)):.2f} (P2) / {float(nu_mono(y)):.2f} (nu_mono); Newtonian 1.00")
R.num("D4", D4)
d4_ok = all(v["Mdyn_over_Mb_P2"] > 2.0 for v in D4.values())
R.check("D4 (reported) the accreted/embedded distinction is a factor 2.8-26 in dynamical mass for the same baryon state", f"P2 ratios {[round(v['Mdyn_over_Mb_P2'], 1) for v in D4.values()]}", d4_ok, load_bearing=False)

R.verdict("GC / maximal-ball functional", "PASS", "reads only baryon masses and positions")
R.verdict("GD / maximal-ball functional", "PARTIAL", "origin-free (D3c) and defined on the leaf geometry; leaf-covariance needs the foliation (CV-type preferred frame); no covariant field-theoretic definition written")
R.verdict("GE / maximal-ball edge", "PARTIAL", "the ball boundary reproduces r_e without a new constant (D3b) -- but as a FIELD gate the Gauss lemma of G1 still gives M_dyn = M_b beyond it")
R.verdict("GA / maximal-ball functional", "FAIL", "supremum over centres and radii: jump discontinuities at mergers (D3d); variation needs a smoothing width (new constant) and is defined only almost everywhere")
R.verdict("GF / maximal-ball functional", "FAIL", "one new constant at least (the merger-smoothing width); x_e is B's own declared item")
R.verdict("GG(i) / any baryon-state functional", "FAIL", "identical baryon state, identical gate value (D3e), different ownership (D4): a history variable that is not a function of the baryon state is required")
R.verdict("GG(ii) / maximal-ball functional", "PARTIAL", "nesting removes the Sun's own phantom (D3a) -- but it also makes every ACCRETED satellite Newtonian, contradicting CFG7's rule (accreted keep their infall halo)")
nf = R.write()
sys.exit(1 if nf else 0)
