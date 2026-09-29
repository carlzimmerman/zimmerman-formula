#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG171 S2 -- door 11A, gate G1 (the law) for every candidate flow law in FROZEN_QUESTION.md.

G1 line: max over x = r/r_M in [0.1, 30] (400 log points) of |g_model/g_target - 1| <= 0.10, for M_b = 1e9, 1e10, 1e11, 1e12 Msun,
point mass and exponential sphere (h = CFG118's HEXP, primary; h = 0.5 r_M, CFG124, secondary), the SAME constants at every mass.
Target: P2, g = sqrt(g_N^2 + a0 g_N) (primary); nu_mono reported.  Both footings.

Laws (steady, spherical, Newtonian; inward acceleration g = -d(v^2/2)/dr, verified in S1 1a'):
  L0   GR's river (PG-SdS):                  v^2/2 = Psi_N + H^2 r^2/2            ->  g = g_N - H^2 r
  L1   linear superposition, own frame:      v = -sqrt(2 Psi_N) + H r              ->  g = g_N + H[sqrt(2Psi_N) - r g_N/sqrt(2Psi_N)] - H^2 r
  L2a  conserved incompressible sink medium added in v^2:  v_m = beta M(<r)/r^2 (sink on the baryons, universal beta)
  L2b  the same medium added linearly in v
  L3b  negative-c_s^2 isothermal medium, supersonic branch (S1 1f): g = g_N + 2K/r, universal K
  L4   AQUAL/QUMOND for Psi = v^2/2 (the declared RESTATEMENT): spherical flux law mu(g/a0) g = g_N, solved by root-finding
For the free amplitudes (L2a beta, L2b beta, L3b K) the script reports the SMALLEST achievable max-residual over any single value shared by
the four masses (a bound, never adopted; a coarse log grid of 4001 values then a bounded refinement).

MUTATE --mutate a : L4 with mu = 1 (the GR river) against the P2 target -> L4's row must FAIL (exit 1 if it does).
MUTATE --mutate b : the target replaced by GR's g_N - H^2 r -> L0's row must PASS (exit 1 if it does).
Runs in < 1 min.
"""
import sys
sys.dont_write_bytecode = True
import math  # noqa: E402
import numpy as np  # noqa: E402
from scipy.optimize import brentq, minimize_scalar  # noqa: E402
import cfg171_common as C  # noqa: E402

MODE = C.parse_mode(sys.argv, ["a", "b"])
R = C.Report("cfg171_s2_g1_law", MODE)
P, check = R.P, R.check
P(f"CFG171 S2 -- G1 (law) for the door-11A flow laws (mode: {'MAIN' if MODE is None else 'MUTATE_' + MODE})")
XG = np.geomspace(0.1, 30.0, 400)
FOOTS = ("canonical", "alt")


def psi_N(prof, r):
    """Newtonian flow potential Psi_N = -Phi_N (Phi(inf) = 0) = G M(<r)/r + int_r^inf 4 pi G rho r' dr' = int_r^inf g_N dr'."""
    if prof.name == "point":
        return prof.u(r) / r
    if not hasattr(prof, "_psi_tab"):
        rr = np.geomspace(1e-5, 1e7, 60001)
        gN = prof.u(rr) / rr ** 2
        # cumulative from the outside: Psi(r) = int_r^R g dr + G M_tot / R
        seg = 0.5 * (gN[1:] + gN[:-1]) * np.diff(rr)
        prof._psi_tab = (np.log(rr), np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) + prof.ug[-1] / rr[-1])
    lr, tab = prof._psi_tab
    return np.interp(np.log(r), lr, tab)


_PROF = {}


def profs(Mb, foot):
    """cached profiles (point, exp_hCFG118, exp_h0.5rM)."""
    if (Mb, foot) not in _PROF:
        _PROF[(Mb, foot)] = C.profiles(Mb, foot)
    return _PROF[(Mb, foot)]


def g_target(prof, r, foot, kernel):
    if MODE == "b":
        return prof.u(r) / r ** 2 - C.H_kpc(foot) ** 2 * r
    gN = prof.u(r) / r ** 2
    return C.KERNELS[kernel](gN / C.a0_kpc(foot)) * gN


def g_L0(prof, r, foot):
    return prof.u(r) / r ** 2 - C.H_kpc(foot) ** 2 * r


def g_L1(prof, r, foot):
    H = C.H_kpc(foot)
    gN = prof.u(r) / r ** 2
    s2 = np.sqrt(2.0 * psi_N(prof, r))
    return gN + H * (s2 - r * gN / s2) - H * H * r


def _num_grad(fun, r, e=1e-5):
    return (fun(r * (1 + e)) - fun(r * (1 - e))) / (2 * r * e)


def g_L2a(prof, r, beta):
    """v^2 = 2 Psi_N + v_m^2, v_m = beta M_b(<r)/r^2 (conserved, incompressible, sink proportional to baryon mass)."""
    vm2h = lambda q: 0.5 * (beta * prof.u(q) / C.G / q ** 2) ** 2
    return prof.u(r) / r ** 2 - _num_grad(vm2h, r)


def g_L2b(prof, r, beta):
    """v = -sqrt(2 Psi_N) - v_m (both inflow, linear): v^2/2 = Psi_N + sqrt(2 Psi_N) v_m + v_m^2/2."""
    def half_extra(q):
        vm = beta * prof.u(q) / C.G / q ** 2
        return np.sqrt(2.0 * psi_N(prof, q)) * vm + 0.5 * vm * vm
    return prof.u(r) / r ** 2 - _num_grad(half_extra, r)


def g_L3b(prof, r, K):
    return prof.u(r) / r ** 2 + 2.0 * K / r


def mu_z_from_nu(kernel):
    """AQUAL form of a QUMOND kernel: z = y nu(y) is monotone in y; invert numerically (root-finding, independent of the algebraic law)."""
    nu = C.KERNELS[kernel]

    def y_of_z(z):
        f = lambda ly: math.log(10 ** ly * float(nu(10 ** ly))) - math.log(z)
        return 10 ** brentq(f, -14, 14, xtol=1e-14)
    return y_of_z


def g_L4(prof, r, foot, kernel):
    """spherical flux law of the AQUAL flow-potential equation: mu(g/a0) g = g_N.  Solved for g by root-finding on the monotone map
    z -> y(z) = mu(z) z; the P2 closed form (sqrt(1+4z^2) - 1)/2 is used for P2, the numerical inverse of y nu(y) for nu_mono."""
    a0 = C.a0_kpc(foot)
    gN = prof.u(r) / r ** 2
    if MODE == "a":
        return gN                                            # MUTATE a: mu = 1, the GR river
    out = np.empty_like(gN)
    for i, yv in enumerate(gN / a0):
        if kernel == "P2":
            # mu(z) z = (sqrt(1+4z^2) - 1)/2 = 2 z^2/(sqrt(1+4z^2) + 1)  (stable form)
            fz = lambda lz: math.log(2 * math.exp(2 * lz) / (math.sqrt(1 + 4 * math.exp(2 * lz)) + 1)) - math.log(yv)
            out[i] = a0 * math.exp(brentq(fz, -40, 40, xtol=1e-14, rtol=1e-15))
        else:
            # z = y nu(y): this IS the QUMOND map, so the AQUAL inverse reproduces it by construction (restatement)
            out[i] = a0 * yv * float(C.KERNELS[kernel](yv))
    return out


def maxres(gm, gt):
    return float(np.max(np.abs(gm / gt - 1.0)))


# ======================================================================================================== the scoring loop (fixed laws)
R.banner("G1 fixed-constant laws: L0 (GR river), L1 (linear superposition), L4 (AQUAL for v^2/2, restatement)")
FIXED = {}
for foot in FOOTS:
    for kernel in ("P2", "nu_mono"):
        for fam in ("point", "exp_hCFG118", "exp_h0.5rM"):
            row = {}
            for law in ("L0", "L1", "L4"):
                worst, wM = -1.0, None
                for Mb in C.MASSES:
                    prof = profs(Mb, foot)[fam]
                    r = XG * C.r_M(Mb, foot)
                    gt = g_target(prof, r, foot, kernel)
                    gm = {"L0": lambda: g_L0(prof, r, foot), "L1": lambda: g_L1(prof, r, foot), "L4": lambda: g_L4(prof, r, foot, kernel)}[law]()
                    m = maxres(gm, gt)
                    if m > worst:
                        worst, wM = m, Mb
                row[law] = dict(max_res=worst, worst_M=wM, pass_=worst <= 0.10)
            FIXED[(foot, kernel, fam)] = row
            P(f"    {foot:9s} {kernel:7s} {fam:12s}: " + ";  ".join(f"{k} max|g/g_t-1| = {v['max_res']:.3g} ({'PASS' if v['pass_'] else 'FAIL'}, worst M {v['worst_M']:.0e})"
                                                          for k, v in row.items()))
R.num("G1_fixed", {"|".join(k): v for k, v in FIXED.items()})

# amplitude of L1's cross term against the target's anomaly (P2, canonical, point mass)
R.banner("L1 amplitude: the cross term H sqrt(GM/2r) against the law's anomaly g_t - g_N (P2, point mass)")
L1AMP = {}
for foot in FOOTS:
    for Mb in C.MASSES:
        prof = C.B.point_mass(Mb)
        vals = {}
        for x in (1.0, 10.0, 30.0):
            r = x * C.r_M(Mb, foot)
            gN = C.G * Mb / r ** 2
            anom = float(C.nu_p2(gN / C.a0_kpc(foot))) * gN - gN
            crossg = C.H_kpc(foot) * math.sqrt(C.G * Mb / (2 * r))
            vals[x] = crossg / anom
        L1AMP[f"{foot}|{Mb:.0e}"] = vals
        P(f"    {foot:9s} M_b = {Mb:.0e}: cross/anomaly at x = 1, 10, 30: " + ", ".join(f"{v:.2e}" for v in vals.values()))
R.num("L1_cross_over_anomaly", L1AMP)

# ======================================================================================================== best-amplitude bounds
R.banner("G1 free-amplitude laws: the smallest max-residual that ANY single shared amplitude can reach (a bound, never adopted)")


def bound_over_amplitude(gfun, a_nat, foot, kernel, fam):
    def worst(la):
        amp = a_nat * 10 ** la
        w_ = 0.0
        for Mb in C.MASSES:
            prof = profs(Mb, foot)[fam]
            r = XG * C.r_M(Mb, foot)
            w_ = max(w_, maxres(gfun(prof, r, amp), g_target(prof, r, foot, kernel)))
        return w_
    grid = np.linspace(-8, 8, 321)
    vals = np.array([worst(q) for q in grid])
    i = int(np.argmin(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    res = minimize_scalar(worst, bounds=(lo, hi), method="bounded", options=dict(xatol=1e-6))
    best = min(float(res.fun), float(vals[i]))
    return best, a_nat * 10 ** (res.x if res.fun <= vals[i] else grid[i])


BOUNDS = {}
for foot in FOOTS:
    a0 = C.a0_kpc(foot)
    Mref = 1e11
    rM = C.r_M(Mref, foot)
    anom1 = (math.sqrt(2) - 1) * a0                               # P2 anomaly at x = 1
    # natural amplitudes: each law's extra force equals the P2 anomaly at x = 1 for M_b = 1e11
    beta_a = math.sqrt(anom1 * rM ** 5 / 2.0) / (Mref * 1.0)       # L2a: g_extra = 2 (beta M)^2 / r^5
    beta_b = anom1 * rM ** 3.5 / (2.5 * math.sqrt(2 * C.G * Mref) * Mref)   # L2b leading term (5/2) sqrt(2GM) beta M r^-7/2
    K_nat = math.sqrt(C.G * Mref * a0) / 2.0                     # L3b: 2K/r = deep-MOND at 1e11
    for kernel in ("P2",):
        for fam in ("point", "exp_hCFG118"):
            for law, gf, an in (("L2a", g_L2a, beta_a), ("L2b", g_L2b, beta_b), ("L3b", g_L3b, K_nat)):
                b, amp = bound_over_amplitude(gf, an, foot, kernel, fam)
                BOUNDS[f"{foot}|{kernel}|{fam}|{law}"] = dict(min_max_res=b, amp_at_min=amp, amp_nat=an, pass_=b <= 0.10)
                P(f"    {foot:9s} {kernel:4s} {fam:12s} {law}: best achievable max|g/g_t - 1| over any shared amplitude = {b:.3f} "
                  f"({'PASS' if b <= 0.10 else 'FAIL'}); at amplitude/natural = {amp / an:.3g}")
R.num("G1_free_amplitude_bounds", BOUNDS)

# ======================================================================================================== controls and reported rows
R.banner("controls: CFG44's point-mass identity, the simple-nu difference (reported), the law's slopes")
Mb = 1e11
prof = C.B.point_mass(Mb)
r = XG * C.r_M(Mb)
g4 = g_L4(prof, r, "canonical", "P2")
Mdyn = g4 * r ** 2 / C.G
ident = float(np.max(np.abs(Mdyn / (Mb * np.sqrt(1 + XG ** 2)) - 1)))
if MODE is None:
    check("C1 CONTROL: L4's root-found flux law reproduces CFG44's point-mass identity M_dyn = M_b sqrt(1 + x^2) to 1e-9 (it IS the law)",
          f"max deviation {ident:.2e}", ident < 1e-9)
gN = prof.u(r) / r ** 2
simp = C.nu_simple(gN / C.a0_kpc("canonical")) * gN
p2 = C.nu_p2(gN / C.a0_kpc("canonical")) * gN
d_simple = float(np.max(np.abs(simp / p2 - 1)))
R.num("simple_vs_P2_max_over_x", d_simple)
check("R1 (reported) the DOOR11 file's parenthetical 'simple' nu differs from the record's P2 by up to this much over x in [0.1, 30]: the kernel "
      "choice matters at the 10% line, so the record's P2 (sqrt(1+1/y)) is used", f"max |g_simple/g_P2 - 1| = {d_simple:.3f}", True, load_bearing=False)
sl_cross = float(np.polyfit(np.log(r), np.log(C.H_kpc("canonical") * np.sqrt(C.G * Mb / (2 * r))), 1)[0])
sl_deep = float(np.polyfit(np.log(r[XG > 10]), np.log(p2[XG > 10] - gN[XG > 10]), 1)[0])
check("R2 (reported) log-slopes: L1's cross term -0.5 against the target anomaly's -> -1 (x > 10)",
      f"cross {sl_cross:.3f}; target anomaly (x>10) {sl_deep:.3f}", True, load_bearing=False)
R.num("slopes", dict(L1_cross=sl_cross, target_anomaly_x_gt_10=sl_deep))

# ======================================================================================================== verdicts
R.banner("G1 verdicts (P2 primary; nu_mono reported)")
prim = [FIXED[(f, "P2", fam)] for f in FOOTS for fam in ("point", "exp_hCFG118")]
L0_pass = all(rw["L0"]["pass_"] for rw in prim)
L1_pass = all(rw["L1"]["pass_"] for rw in prim)
L4_pass = all(rw["L4"]["pass_"] for rw in prim)
L4_all = all(FIXED[k]["L4"]["pass_"] for k in FIXED)
free_pass = {law: all(BOUNDS[k]["pass_"] for k in BOUNDS if k.endswith(law)) for law in ("L2a", "L2b", "L3b")}
if MODE is None:
    check("G1-L0 GR's own river (Newton + the repulsive Lambda term) FAILS the law on every mass, both profiles, both footings",
          f"worst {max(rw['L0']['max_res'] for rw in prim):.3f}", not L0_pass)
    check("G1-L1 linear velocity superposition FAILS (the cross term is 0.2-3% of the law's anomaly at x = 1-30 and has the wrong slope)",
          f"worst {max(rw['L1']['max_res'] for rw in prim):.3f}; cross/anomaly max {max(max(v.values()) for v in L1AMP.values()):.3f}",
          not L1_pass and max(max(v.values()) for v in L1AMP.values()) < 0.05)
    check("G1-L2a/L2b/L3b no single shared amplitude brings the conserved-sink media or the negative-c_s^2 isothermal medium within 10%",
          f"best bounds {[round(BOUNDS[k]['min_max_res'], 3) for k in BOUNDS]}", not any(free_pass.values()))
    check("G1-L4 the AQUAL flow-potential law reproduces the target exactly (P2 and nu_mono, both profiles, both footings) -- as a RESTATEMENT (p*)",
          f"worst {max(FIXED[k]['L4']['max_res'] for k in FIXED):.2e}", L4_all)
nf = R.write()
if MODE == "a":
    flipped = not L4_pass
    P(f"  MUTATE a: L4 with mu = 1 {'FAILS' if flipped else 'still passes'} G1 -> {'exit 1 (control bites)' if flipped else 'control broken'}")
    sys.exit(1 if flipped else 0)
if MODE == "b":
    flipped = L0_pass
    P(f"  MUTATE b: with GR's law as the target L0 {'PASSES' if flipped else 'still fails'} G1 -> {'exit 1 (control bites)' if flipped else 'control broken'}")
    sys.exit(1 if flipped else 0)
sys.exit(1 if nf else 0)
