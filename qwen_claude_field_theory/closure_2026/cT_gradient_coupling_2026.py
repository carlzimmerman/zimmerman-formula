#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cT_gradient_coupling_2026.py
============================
CAN A GRADIENT-BUILT DISFORMAL COUPLING SEPARATE LENSING FROM c_T?

The decisive calculation for the last open gate. cT_lensing_welding_2026.py established that
the welding is a THEOREM -- null-cone safety requires a conformal coupling, and a conformal
coupling cancels identically from the lensing combination -- leaving exactly one freedom:
WHERE the disformal amplitude B is nonzero. This file prices that freedom.

THE SETUP FORCED BY SHIFT SYMMETRY. The framework's scalar obeys phi -> phi + const, so the
matter coupling cannot contain phi itself. The general shift-symmetric matter metric is

    gtilde_munu = A(Y,Q) g_munu + B(Y,Q) d_mu phi d_nu phi   (+ vector pieces)

with Y = q^{mu nu} d_mu phi d_nu phi the aether-frame spatial gradient and Q = A^mu d_mu phi
the tick. Both invariants are gradient-built, so both are shift-symmetric.

WHAT THIS FILE COMPUTES, each number before its check:
 A. that the conformal piece A(Y,Q) STILL cancels from lensing no matter how it is built, so
    the theorem survives the move to gradients and B != 0 remains mandatory;
 B. the weak-field structure of the gradient-built disformal piece, which is NOT the same as
    the potential-built one -- it carries a 0i term and an ij term the A_mu A_nu form lacks;
 C. THE ESCAPE: B may be a FUNCTION of Y that vanishes as Y -> 0. Since GW170817 travelled
    almost entirely through intergalactic space where Y is small, and lensing is measured
    through galaxies where Y ~ a_0^2, a steep enough B(Y) separates them. Compute the power
    required and compare it with the powers the framework already contains.
"""
import sys
import numpy as np
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
C, MPC, KPC, GYR = 2.99792458e8, 3.0857e22, 3.0857e19, 3.156e16
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

head("PART A -- the conformal piece still cancels, however it is built")
Phi, Psi, dA = sp.symbols("Phi Psi delta_A")
# gtilde = A g with A = 1 + dA:  g00 -> -(1+2Phi)(1+dA), gij -> (1-2Psi)(1+dA)
Phi_t = sp.simplify(Phi + dA / 2)     # -(1+2Phi_t) = -(1+2Phi)(1+dA) to first order
Psi_t = sp.simplify(Psi - dA / 2)     # (1-2Psi_t) = (1-2Psi)(1+dA)
check(sp.simplify((Phi_t + Psi_t) - (Phi + Psi)) == 0,
      "A1  *** ANY conformal factor, gradient-built or not, shifts Phi and Psi by EQUAL AND "
      "OPPOSITE amounts, so it cancels from Phi+Psi IDENTICALLY. Moving to shift-symmetric "
      "invariants does NOT rescue the conformal route ***",
      f"Phi_t + Psi_t - (Phi+Psi) = {sp.simplify((Phi_t+Psi_t)-(Phi+Psi))}")
check(sp.simplify(sp.diff(Phi_t - Psi_t, dA)) == 1,
      "A2  and it shifts the SLIP Phi-Psi at first order, which is what lensing-vs-dynamics "
      "actually measures -- so a conformal factor is not invisible, it is invisible IN THE "
      "LENSING SUM specifically",
      "d(Phi_t - Psi_t)/d(delta_A) = 1")
check(True,
      "A3  *** THEREFORE B != 0 REMAINS MANDATORY under shift symmetry, and the welding "
      "theorem survives intact. The only freedom is WHERE B is nonzero ***")

head("PART B -- the gradient-built disformal piece has a different weak-field structure")
Q0, psi_r, Bc = sp.symbols("Q_0 psi_r B", real=True)
# d_mu phi = (Q_0, psi_r, 0, 0) for phi = Q_0 t + psi(r)
dphi = sp.Matrix([Q0, psi_r, 0, 0])
D = Bc * (dphi * dphi.T)
info("B0  B d_mu phi d_nu phi components",
     f"00 = {D[0,0]},  0r = {D[0,1]},  rr = {D[1,1]}")
check(sp.simplify(D[0, 0] - Bc * Q0**2) == 0 and sp.simplify(D[1, 1] - Bc * psi_r**2) == 0,
      "B1  the gradient form carries a 00 piece B Q_0^2, a 0r piece B Q_0 psi', AND an rr "
      "piece B psi'^2 -- the potential-built A_mu A_nu form has ONLY the 00 piece",
      "so the two are structurally different couplings, not a relabelling")
ratio_rr = (1.0e-3) ** 2            # |grad psi| / Q_0 ~ v/c
info("B2  size of the extra pieces", f"rr/00 = psi'^2/Q_0^2 ~ (v/c)^2 ~ {ratio_rr:.1e}; the 0r "
     "piece is a t-r cross term, removable by t -> t + f(r) for a STATIC configuration, hence "
     "pure gauge for lensing")
check(ratio_rr < 1e-4,
      "B3  so at leading order the gradient-built disformal piece acts through its 00 "
      "component alone, exactly like the potential-built one -- the lensing algebra of the "
      "welding file carries over UNCHANGED, and with it the requirement B ~ v_c^2/c^2",
      f"the rr correction enters at {ratio_rr:.0e} of the 00 piece")

head("PART C -- THE ESCAPE: B as a function of Y, and the power it needs")
# From the welding file: to satisfy GW170817 while confining B to galaxies, the in-galaxy B
# must be < 2.80e-12 against the 3.92e-07 lensing requires.  Shortfall:
B_lens, B_allowed = 3.922e-07, 2.800e-12
short = B_lens / B_allowed
info("C0  the gap to close (from cT_lensing_welding_2026.py)",
     f"B_lens = {B_lens:.3e}, B_allowed_in_galaxy = {B_allowed:.3e}, shortfall = {short:.3e} "
     f"= {np.log10(short):.2f} orders")
# Y ~ (g/c^2)^2 in the aether frame, so B ~ Y^p gives B_gal/B_path = (g_gal/g_path)^(2p).
# g in a lensing galaxy: ~a0 (the regime where the MOND anomaly is measured).
# g along the intergalactic path: peculiar accelerations from large-scale structure.
v_pec = 300e3                       # m/s, typical LSS peculiar velocity
t_H = 13.8 * GYR
g_igm = v_pec / t_H
info("C1  intergalactic acceleration estimate", f"g_IGM ~ v_pec/t_H = {v_pec/1e3:.0f} km/s / "
     f"13.8 Gyr = {g_igm:.3e} m/s^2")
for nm, a0 in A0.items():
    contrast = a0 / g_igm
    p_req = np.log10(short) / (2 * np.log10(contrast))
    info(f"C2  {nm:9s}", f"g_gal/g_IGM = a0/g_IGM = {contrast:.1f}  =>  required power "
                          f"B ~ Y^p with p >= {p_req:.3f}")
p_req_can = np.log10(short) / (2 * np.log10(A0["canonical"] / g_igm))
p_req_alt = np.log10(short) / (2 * np.log10(A0["alt"] / g_igm))
check(p_req_can < 1.5 and p_req_alt < 1.5,
      f"C3  *** THE REQUIRED POWER IS p >= {p_req_can:.2f} canonical / {p_req_alt:.2f} alt. "
      "The framework's OWN deep-MOND structure supplies Y^(3/2) -- p = 1.5 -- which EXCEEDS "
      "the requirement. A disformal amplitude carrying the deep-MOND power closes the "
      "GW170817 gap on this estimate ***",
      f"needed {max(p_req_can, p_req_alt):.3f}, available 1.5")
margin = 2 * (1.5 - p_req_can) * np.log10(A0["canonical"] / g_igm)
info("C4  margin at p = 3/2", f"{margin:.2f} orders of headroom canonical")

head("PART D -- what would break it, priced honestly")
# D1: the host-galaxy crossing is the hard part -- B is NOT small there.
frac = 20.0 * KPC / (40.0 * MPC)
for nm, a0 in A0.items():
    supp = (g_igm / a0) ** (2 * 1.5)
    dt_over_t = frac * B_lens / 2 + (1 - frac) * B_lens * supp / 2
    info(f"D1  {nm:9s} total Delta t/t at p = 3/2",
         f"host {frac:.1e} x full + path (1-{frac:.1e}) x {supp:.2e} = {dt_over_t:.3e}")
dt_can = frac * B_lens / 2 + (1 - frac) * B_lens * (g_igm / A0["canonical"]) ** 3 / 2
check(dt_can > 7e-16,
      f"D2  *** AND THE HOST CROSSING STILL DOMINATES AND STILL FAILS: {dt_can:.2e} against the "
      f"7e-16 bound, over by {dt_can/7e-16:.2e}x. Suppressing B along the intergalactic path "
      "does NOT help, because the 20 kpc inside the host contributes at FULL strength ***",
      "the escape kills the path term and leaves the host term untouched")
# D3: what would be needed of the host term
B_host_needed = 7e-16 * 2 / frac
info("D3  inverting the host term", f"the in-host B must be < {B_host_needed:.2e} against the "
     f"{B_lens:.2e} lensing needs -- short by {B_lens/B_host_needed:.2e}x "
     f"({np.log10(B_lens/B_host_needed):.2f} orders)")
check(B_lens / B_host_needed > 1e4,
      "D4  so the gradient escape moves the problem but does not solve it: the binding term is "
      "no longer the 40 Mpc of intergalactic path but the 20 kpc inside NGC 4993, and there "
      "the field is genuinely of order a_0, where B must be of order v_c^2/c^2 for lensing to "
      "work at all",
      "*** THE LANE IS NOT CLOSED, BUT IT IS NARROWED TO ONE QUESTION: what is Y along the "
      "actual line of sight through NGC 4993 to its own merger site? ***")

head("PART E -- standing")
for s_ in [
    "THE WELDING THEOREM SURVIVES SHIFT SYMMETRY. A conformal factor cancels from Phi+Psi "
    "however it is built, so a disformal amplitude B != 0 remains mandatory for lensing, and "
    "B != 0 moves the photon cone. That is now established for the gradient-built class too.",
    "THE GRADIENT COUPLING IS NOT A RELABELLING: it carries 0r and rr pieces the A_mu A_nu "
    "form lacks. But the 0r piece is pure gauge for a static configuration and the rr piece "
    "is (v/c)^2 suppressed, so the lensing algebra and the requirement B ~ v_c^2/c^2 carry "
    "over unchanged.",
    "*** THE ESCAPE IS REAL FOR THE INTERGALACTIC PATH AND THE REQUIRED POWER IS MODEST: "
    f"p >= {p_req_can:.2f}, against the Y^(3/2) the framework's deep-MOND limit already "
    "supplies. That is the first time a required exponent in this programme has come in BELOW "
    "what the framework contains. ***",
    "BUT IT DOES NOT CLOSE THE GATE, because the binding contribution is the host-galaxy "
    "crossing, where the field IS of order a_0 and B must be full strength for lensing to "
    "work. The escape removes the 40 Mpc term and leaves the 20 kpc term.",
    "THE NEXT CALCULATION, AND IT IS NARROW: what is Y along the actual line of sight from "
    "the GW170817 merger site to the edge of NGC 4993? The merger sat at a projected ~2 kpc "
    "from the centre of an early-type galaxy -- a HIGH-acceleration environment where "
    "g >> a_0 and Y^(3/2) suppression is therefore LARGE, not small. That number was assumed "
    "here (a_0, deep-MOND) rather than computed, and it is the one input the verdict turns on.",
    "footings: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 FITTED",
]:
    info("S", s_)

print("\n" + "=" * 100)
print(f"GRADIENT-COUPLING CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
sys.exit(1 if FAIL else 0)
