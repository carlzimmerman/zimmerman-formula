#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG232_A7_scalar_tensor_13c -- 13c: the conformally coupled AQUAL-type scalar chi on the Einstein metric g (the MOND-relevant sector kept: the relative time-time
potential).  A labelled REPRODUCTION control of the single-metric pincer N1; new legs G1-C (A3), G3, G4, Q2 as a law (A6).  Here: the static law by inversion,
legality (k-essence conditions), radial sound speed, lensing slip D2, G2 by the nonlinear quasi-static estimate (CFG172's declared reading).
Static reduction: div[mu_chi(|grad chi|/a0) grad chi] = 4 pi G rho_b ; baryon acceleration g_b = g_N + |grad chi| (additive, not QUMOND); light sees Psi_GR only.
MUTATE M9: GR-quadratic kinetic function (mu_chi -> 0 coupling, h = 0): G1-law flips to F and Q2 flips to PASS.
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG232_common as C

R = C.Run("CFG232_A7_scalar_tensor_13c")
MUT = R.mutate
P = R.P
bite = []
Bc = C.B

y = np.geomspace(1e-8, 1e8, 4001)
res = {}
for kn in ("P2", "nu_mono"):
    nu = C.KERNELS[kn]
    h = (1.0 / (np.sqrt(1.0 + 1.0 / y) + 1.0)) if kn == "P2" else (nu(y) - 1.0) * y     # |grad chi|/a0 the scalar must supply (P2 in the cancellation-free form (nu-1) y = 1/(sqrt(1+1/y)+1))
    if MUT == "M9":
        h = 0.0 * h
    mu = np.where(h > 0, y / np.maximum(h, 1e-300), np.inf)   # mu_chi(h) = y/h  (flux: mu_chi h = y)
    dy_dh = np.gradient(y, h) if not MUT else np.zeros_like(y)
    lnmu = np.log(mu)
    dlnmu_dlnh = np.gradient(lnmu, np.log(h)) if not MUT else np.zeros_like(y)
    cr2 = 1.0 / (1.0 + dlnmu_dlnh) if not MUT else np.ones_like(y)
    res[kn] = dict(h=h, mu=mu, dy_dh=dy_dh, cr2=cr2)
    if MUT:
        continue
    mono = bool(np.all(np.diff(h) > 0))
    P(f"  {kn}: h(y) increasing = {mono}; h(y->0) ~ sqrt(y): h(1e-8)/sqrt(1e-8) = {h[0]/1e-4:.4f}; h(y=1e8) = {h[-1]:.4f} (P2 wall: 1/2)")
    P(f"      mu_chi > 0: {bool(np.all(mu > 0))};  d(mu h)/dh = dy/dh > 0: {bool(np.all(dy_dh[1:-1] > 0))};  radial sound speed c_r^2 = 1/(1 + dln mu/dln h): min {cr2[2:-2].min():.3e}, max {cr2[2:-2].max():.3f}")
    ys = y[np.argmin(abs(y - 7e5))]
    P(f"      at the Solar-System acceleration y = {ys:.2e}: c_r^2 = {cr2[np.argmin(abs(y-7e5))]:.3e} (hand: 1/(4y) = {1/(4*ys):.2e} for P2)")
R.banner("13c static law by inversion (round trip), legality, sound speed")
if not MUT:
    d = res["P2"]
    # round trip: solve mu_chi(h) h = y_source, g_b = y + h
    max_dev = 0.0
    for yy in np.geomspace(1e-5, 1e5, 50):
        # invert h by interpolation on the designed table
        hh = np.interp(np.log(yy), np.log(y), d["h"])
        max_dev = max(max_dev, abs((yy + hh) / (yy * float(C.nu_p2(yy))) - 1))
    R.check("13c G1-law round trip: g_b = g_N + |grad chi| with the designed mu_chi reproduces nu g_N to the table accuracy (P2)", max_dev < 1e-3, f"max dev {max_dev:.1e}")
    # G1 at seven masses x two profiles (the law depends on g_N only, exactly as 13a)
    worst = 0.0
    for M in np.geomspace(1e9, 1e12, 7):
        for pn in ("point", "exp"):
            prof = Bc.point_mass(M) if pn == "point" else Bc.exp_sphere(M, 2.0)
            rM = math.sqrt(C.G * M / C.A0_KPC)
            rr = np.geomspace(0.1 * rM, 30 * rM, 41)
            yb = prof.gN(rr) / C.A0_KPC
            hh = np.interp(np.log(yb), np.log(y), d["h"])
            worst = max(worst, float(np.max(np.abs((yb + hh) / (yb * C.nu_p2(yb)) - 1))))
    R.check("G1-LAW 13c (P2, designed by inversion): max |g/g_target - 1| <= 0.10, 7 masses x point + exponential sphere", worst <= 0.10, f"max = {worst:.1e} (P-declared, M1-inv)", kind="result")
    R.verdict("G1-law 13c", "PASS (P-declared by inversion, M1-inv)", f"max deviation {worst:.1e}; against CFG44's C(r) target the exponential sphere fails at low mass exactly as in 13a (the law depends on g_N alone)")
    okleg = all(np.all(res[k]["mu"] > 0) and np.all(res[k]["dy_dh"][2:-2] > 0) and np.all((res[k]["cr2"][2:-2] > 0) & (res[k]["cr2"][2:-2] <= 1.0)) for k in res)
    R.check("13c legality: mu_chi > 0, d(mu h)/dh > 0 (F_X + 2X F_XX > 0), 0 < c_r^2 <= 1 (subluminal) on the whole designed branch, P2 and nu_mono", okleg, "result", kind="result")
    P(f"  the P2 kinetic function is a DBI-like wall: |grad chi| <= a0/2 for every source acceleration, mu_chi -> 2y -> infinity; radial sound speed c_r^2 = 1/(4y) -> {1/(4*7e5):.1e} at Saturn: subluminal but strongly coupled (very small sound speed) in the Solar System")
    R.verdict("G5a 13c (static branch)", ("PASS on the conditions checked (mu > 0, F_X + 2X F_XX > 0, 0 < c_r^2 <= 1)" if okleg else "FAIL (a legality condition is violated)"), "time-dependent stability beyond the radial/tangential sound-speed conditions, superluminality of nonlinear solutions and the strong-coupling scale c_r^2 ~ 1e-7 are not analysed")

    # D2 lensing: light sees Psi_GR only
    P("  D2 (13c): Psi' = g_N (no scalar in the lensing potential), Phi' = nu g_N: M_dyn/M_lens = nu (2 -> lensing sees Newtonian mass only): the Bekenstein-Sanders deficit, as the record's N1")
    R.num("D2_ratio_at_y", {str(v): float(C.nu_p2(v)) for v in (1e-2, 1.0, 1e2)})

    # G2 nonlinear quasi-static estimate
    R.banner("G2 (13c): nonlinear quasi-static estimate G_eff/G = nu(y_lin), y_lin = (3/2) Omega_m(z) H(z)^2 delta /(k_phys a0), delta = 1 (upper bound on y_lin)")
    H0, Om = 67.36, 0.3153
    a0m = C.A0_KPC * 1e3                                  # (km/s)^2/Mpc
    tab = {}
    worst_g = 0.0
    for z in (0, 0.5, 1, 2, 3, 10, 30):
        row = {}
        for k in (0.1, 0.3, 1, 3, 10, 30):
            g = 1.5 * Om * (1 + z) ** 3 * H0 ** 2 / (k * (1 + z))
            yl = g / a0m
            row[k] = float(C.nu_p2(yl)) - 1.0
            worst_g = max(worst_g, row[k])
        tab[z] = row
        P(f"  z={z:>4}: G_eff/G - 1 at k = 0.1..30 /Mpc: " + ", ".join(f"{row[k]:.3g}" for k in row))
    R.num("G2_13c", {str(z): r for z, r in tab.items()})
    R.check("G2 (13c, local law applied to linear structure, delta = 1): |G_eff/G - 1| <= 0.05 at every k and z tabulated", worst_g <= 0.05, f"max = {worst_g:.3g}", kind="result")
    R.verdict("G2 13c", "FAIL on the nonlinear quasi-static estimate", f"G_eff/G - 1 up to {worst_g:.1e}; the linear perturbation theory of chi is strongly coupled at chi' = 0 (mu_chi(0) = 0): UNDEFINED as a linear theory; CMB UNDEFINED")
else:
    R.banner("MUTATE M9: GR-quadratic kinetic function (h = 0)")
    rr = np.geomspace(0.1, 30, 30)
    g_b = 1.0 / rr ** 2                                    # point mass, g_N only
    tgt = np.sqrt(1 / rr ** 4 + 1 / rr ** 2)
    dev = float(np.max(np.abs(g_b / tgt - 1)))
    P(f"  G1-law with h = 0: max deviation {dev:.2f} (fails); phantom = 0 so Q2 = 0 (passes): pincer ends move oppositely")
    bite.append(dev > 0.10)
R.finish(bite if MUT else None)
