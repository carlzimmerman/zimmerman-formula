#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG231_A5_reaction_energy -- G3: reaction on the baryons (potential-force statement) and the canonical energy of the vector sector inside
r_e = 0.4 r_ta, in BOTH r_ta conventions (CFG48's cosmic-share collapse mass; the committed law-enclosed-mass convention), vs (1/2) M_b V_f^2.
Frozen: CFG231_FROZEN_CRITERIA.md sections 2 (G3), 5 (item 6), 6.  Conventions imported read-only from CFG48's Gcommon (convention A) and re-derived
here (convention B, from the CFG48 referee's description).   Exit 0 if the reproduction checks pass.   No MUTATE modes.
"""
import sys, os, math
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import CFG231_common as C

sys.path.insert(0, os.path.join(C.REPO, "campaign_fresh_gravity", "CFG48_gap1_switch"))
import Gcommon as GC  # noqa: E402  (read-only import: r_ta convention A)

R = C.Report("CFG231_A5_reaction_energy")
C.header(R, "CFG231 A5 -- G3: reaction and energy")
G = C.G
a0k = C.AKPC(C.A0_SI["canonical"])
OM, HH, DTA = GC.OM, GC.HH, GC.DELTA_TA
RHO_M = OM * GC.RHOC0_MPC * 1e-9            # Msun/kpc^3 (mean matter density)


def rta_A(M):
    return GC.r_ta_kpc(M)                      # CFG48's convention (imported)


def rta_B(M):
    """committed convention: the law's own enclosed mass (P2, point mass: M sqrt(1+x^2), phantom included) falls to Delta_ta rho_m."""
    rM = C.r_M_kpc(M, a0k)
    f = lambda lr: M * math.sqrt(1 + (math.exp(lr) / rM) ** 2) - (4 * math.pi / 3) * DTA * RHO_M * math.exp(3 * lr)
    return math.exp(brentq(f, math.log(rM), math.log(1e5 * rM)))


R.banner("C-rta  reproduce the CFG48 referee's R7 table (P2, z = 0): r_ta convention A -> B (kpc)")
ref = {1e10: (319, 1151), 1e11: (688, 2047), 1e12: (1482, 3639)}
ok_r = True
for M, (a_, b_) in ref.items():
    ra, rb = rta_A(M), rta_B(M)
    R.P(f"  M_b = {M:.0e}: A = {ra:.0f} (referee {a_}), B = {rb:.0f} (referee {b_})")
    ok_r = ok_r and abs(ra / a_ - 1) < 0.01 and abs(rb / b_ - 1) < 0.01
R.check("C-rta both r_ta conventions reproduce the CFG48 referee's R7 table to 1% at 1e10, 1e11, 1e12 (A imported from Gcommon, B re-derived)", "see the rows above", ok_r)

Vf2 = lambda M: math.sqrt(G * M * a0k)


def energy(prof_kind, M, law, a_kpc, r_e, r_in_over_rM=1e-3, sign_mag=True, h=C.H_SPHERE):
    """canonical energy of the vector sector in r_in < r < r_e: int 4 pi r^2 |u| dr, u = (1/4 pi G)(E D - int_0^E D dE') (magnitude), D(E) = g_N."""
    prof = C.PointMass(M) if prof_kind == "point" else C.ExpSphere(M, h)
    rM = C.r_M_kpc(M, a0k)
    r = np.geomspace(r_in_over_rM * rM if prof_kind == "point" else 1e-4 * rM, r_e, 200001)
    gN = C.gN_of(prof, r)
    if law == "V0":
        E = gN                                        # D(E) = E, Lam = E^2/2
        u = (E * gN - 0.5 * E ** 2) / (4 * math.pi * G)
    else:
        E = C.PSI[law](gN, a_kpc)
        u = (E * gN - C.int_D(law, E, a_kpc)) / (4 * math.pi * G)
    return float(np.trapz(4 * math.pi * r ** 2 * np.abs(u), r))


R.banner("A5.1  the energy of the vector sector inside r_e = 0.4 r_ta, in units of (1/2) M_b V_f^2   (pass line <= 1; a = a_V(H_Lambda), V_f^2 = sqrt(G M a0_canonical))")
a_kpc = C.AKPC(C.a_V_si("HL"))
rows = {}
for kind in ("point", "sphere"):
    for law in ("K1", "K2", "K3", "V0"):
        for M in (1e10, 1e11, 1e12):
            rowc = {}
            for conv, rta in (("A", rta_A), ("B", rta_B)):
                r_e = 0.4 * rta(M)
                Ee = energy(kind, M, law, a_kpc, r_e)
                rowc[conv] = dict(r_e=r_e, ratio=Ee / (0.5 * M * Vf2(M)), x_e=r_e / C.r_M_kpc(M, a0k))
            rows[f"{kind}|{law}|{M:.0e}"] = rowc
for kind in ("point", "sphere"):
    for law in ("K1", "K2", "K3", "V0"):
        R.P(f"  {kind:6s} {law}: ratio E_field/((1/2) M V_f^2) at M = 1e10, 1e11, 1e12: " + "; ".join(
            f"conv A {rows[f'{kind}|{law}|{M:.0e}']['A']['ratio']:.3g} / conv B {rows[f'{kind}|{law}|{M:.0e}']['B']['ratio']:.3g}" for M in (1e10, 1e11, 1e12)))
R.num("energy_rows", rows)

R.banner("A5.2  closed-form control: deep-limit K2 energy ratio = (4/3) sqrt(a/a0) ln(r_e/r_in) (point mass); the frozen hand estimate said O(1) r_e/r_M (WRONG)")
ok2 = True
for M in (1e10, 1e12):
    r_e = 0.4 * rta_A(M); rM = C.r_M_kpc(M, a0k); rin = 1e-3 * rM
    num = energy("point", M, "K2", a_kpc, r_e) / (0.5 * M * Vf2(M))
    cf = (4.0 / 3.0) * math.sqrt(a_kpc / a0k) * math.log(r_e / rin)
    ok2 = ok2 and abs(num / cf - 1) < 1e-3
    R.P(f"  M = {M:.0e}: numeric {num:.4f}, closed form {cf:.4f}; r_e/r_M = {r_e / rM:.1f} (the frozen hand estimate 'O(1) x r_e/r_M' would give ~{r_e / rM:.0f}: an overestimate, kept)")
R.check("A5.2 numeric energy equals the closed form (4/3) sqrt(a/a0) ln(r_e/r_in) for K2 to 0.1%", "see rows above", ok2)

R.banner("A5.3  sensitivity to the inner cutoff of the point-mass energy (K2 diverges logarithmically): r_in = 1e-2, 1e-3, 1e-4 r_M at 1e10, convention A")
for rin in (1e-2, 1e-3, 1e-4):
    M = 1e10
    e = energy("point", M, "K2", a_kpc, 0.4 * rta_A(M), r_in_over_rM=rin) / (0.5 * M * Vf2(M))
    R.P(f"  r_in = {rin:g} r_M: K2 ratio {e:.3f}")
R.P("  K1 and K3 are finite as r_in -> 0 (E saturates); V0's point mass diverges as 1/r_in (shown by the sphere rows instead).")

R.banner("A5.4  reaction on the baryons")
R.P("  For a spherical E(r) the drag force f = eps E(r) r-hat is the gradient of phi(r) = -int E dr, i.e. a POTENTIAL force: the part of the force on the baryons beyond the gradient of a potential is identically zero,")
R.P("  so the reaction (frozen definition: force beyond -grad Phi from the vector's own field equations, over g_law) is 0 <= 0.10 g_law at every x in [0.3, 30]: recorded p* (by construction), NOT a pass of substance.")
R.P("  The Noether momentum balance of the full action would show the field carries the momentum the baryons lose; that is not scored (no time-dependent solution is computed here).")
R.check("A5.4 reaction = 0 by construction for a spherical potential force (curl-free)", "statement; p*", True, load_bearing=False)

R.banner("G3 verdicts")
worst = {}
for law in ("K1", "K2", "K3", "V0"):
    for kind in ("point", "sphere"):
        vals = [rows[f"{kind}|{law}|{M:.0e}"][c]["ratio"] for M in (1e10, 1e11, 1e12) for c in ("A", "B")]
        worst[(law, kind)] = (min(vals), max(vals))
        R.P(f"  {law} {kind}: energy ratio over M in {{1e10, 1e11, 1e12}} and both conventions in [{min(vals):.3g}, {max(vals):.3g}]  -> {'FAIL (> 1)' if min(vals) > 1 else ('mixed' if max(vals) > 1 else 'within the orbital energy')}")
R.num("energy_range", {f"{k[0]}|{k[1]}": v for k, v in worst.items()})
R.P("  the vector sector's energy inside r_e is a few times to ~10 times the baryons' orbital energy for K1/K2/K3 (logarithmic in r_e/r_M, not linear as the frozen hand estimate assumed).")
nf = R.write()
sys.exit(0 if nf == 0 else 1)
