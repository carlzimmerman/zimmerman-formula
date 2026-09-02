#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
cmc_filter_scalar_dof_gate_2026.py -- does the CMC / Hubble high-pass auxiliary propagate a scalar?  Quadratic ADM action around FLRW.
=====================================================================================================================================
The proposal (2026-09-02) adds to GR a spatial auxiliary chi with
    L_chi = lam * N sqrt(gamma) [ -1/2 gamma^{ij} d_i chi d_j chi - 1/2 (xi^2/9) K^2 chi^2 + gamma^{ij} d_i chi d_j ln N ],
K = trace of the extrinsic curvature (Theta = K: 3H on FLRW, 0 static), and claims zero propagating auxiliary DOF from a reduced
4x4 Dirac block.  That block does not contain the lapse.  The coupling d chi . d ln N makes the Lagrangian depend on spatial
gradients of the lapse, the structure that in spatially covariant gravity generically turns the lapse from a Lagrange multiplier
into a solved variable and frees one scalar mode.  This script decides it at the level that matters for cosmology: the full
quadratic action for scalar perturbations (alpha = dN, psi = shift potential, zeta = curvature, chi) around de Sitter, derived from
the ADM Lagrangian by sympy, auxiliaries integrated out exactly, and the residual zeta action inspected:
    A(k) zeta-dot^2 - B(k) zeta^2 :  A = 0  ->  no scalar DOF (GR)   ;   A != 0  ->  ONE propagating scalar (a dark field by another name).
Regression: lam -> 0 must give A = 0 identically.  Then the sign of A (ghost) and B/A at large k (gradient instability).
Units M_Pl^2 = 1 (so the GR Lagrangian is 1/2 N sqrt(gamma)(R3 + K_ij K^ij - K^2 - 2 Lambda)), c = 1.  Checks CAN fail.
"""
import sys
import sympy as sp
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
t, x, y, z = sp.symbols("t x y z", real=True)
k, H, lam, xi, eps = sp.symbols("k H lambda xi epsilon", positive=True)
a = sp.exp(H*t); Lam = 3*H**2                                   # de Sitter background: H^2 = Lambda/3
al, ps, ze, ch = [sp.Function(n)(t) for n in ("alpha", "psi", "zeta", "chi")]
cs = sp.cos(k*x)
alpha = eps*al*cs; psi = eps*ps*cs; zeta = eps*ze*cs; chi = eps*ch*cs
N = 1 + alpha; omega = sp.log(a) + zeta                            # gamma_ij = e^{2 omega} delta_ij
X = [x, y, z]
g = sp.diag(*[sp.exp(2*omega)]*3); ginv = sp.diag(*[sp.exp(-2*omega)]*3); sqrtg = sp.exp(3*omega)
Nlow = [sp.diff(psi, x), 0, 0]                                    # N_i = d_i psi
def Gam(kk, i, j):                                                # Christoffels of a conformally flat 3-metric
    d = lambda i_, j_: 1 if i_ == j_ else 0
    return d(kk, i)*sp.diff(omega, X[j]) + d(kk, j)*sp.diff(omega, X[i]) - d(i, j)*sp.diff(omega, X[kk])
def DN(i, j): return sp.diff(Nlow[j], X[i]) - sum(Gam(kk, i, j)*Nlow[kk] for kk in range(3))
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(g[i, j], t) - DN(i, j) - DN(j, i))/(2*N))
Kup = ginv*Kij*ginv
KK = sum(Kij[i, j]*Kup[i, j] for i in range(3) for j in range(3))
Ktr = sum(ginv[i, i]*Kij[i, i] for i in range(3))
R3 = -2*sp.exp(-2*omega)*(2*sum(sp.diff(omega, xx, 2) for xx in X) + sum(sp.diff(omega, xx)**2 for xx in X))
L_GR = sp.Rational(1, 2)*N*sqrtg*(R3 + KK - Ktr**2 - 2*Lam)
dchi2 = sum(ginv[i, i]*sp.diff(chi, X[i])**2 for i in range(3))
dchi_dlnN = sum(ginv[i, i]*sp.diff(chi, X[i])*sp.diff(sp.log(N), X[i]) for i in range(3))
L_chi = lam*N*sqrtg*(-sp.Rational(1, 2)*dchi2 - sp.Rational(1, 2)*(xi**2/9)*Ktr**2*chi**2 + dchi_dlnN)
ZD, ZE = sp.symbols("ZD ZE")
def coeffs(L):
    """polynomial extraction: replace zeta-dot and zeta by plain symbols first (simplify hides Derivative powers from .coeff)"""
    Lp = sp.expand(L.subs(sp.Derivative(ze, t), ZD).subs(ze, ZE))
    A_ = sp.simplify(Lp.coeff(ZD, 2)); B_ = sp.simplify(-Lp.coeff(ZE, 2).subs(ZD, 0)); C_ = sp.simplify(Lp.coeff(ZD, 1).coeff(ZE, 1))
    return A_, B_, C_
def quad(L):
    ser = sp.series(L, eps, 0, 3).removeO()
    L2 = ser.coeff(eps, 2); L1 = ser.coeff(eps, 1)
    avg = lambda e: sp.simplify(sp.integrate(sp.expand(e), (x, 0, 2*sp.pi/k))*k/(2*sp.pi))
    return avg(L2), avg(L1)
P("="*100); P("1. the quadratic scalar action around de Sitter (x-averaged), GR + lam * L_chi"); P("="*100)
L2_GR, L1_GR = quad(L_GR)
L2_chi, L1_chi = quad(L_chi)
check("1a first-order terms vanish on the de Sitter background (consistency of the ansatz)", sp.simplify(L1_GR) == 0 and sp.simplify(L1_chi) == 0)
L2 = sp.expand(L2_GR + L2_chi)
zd = sp.diff(ze, t)
AL = sp.symbols("AL")
info("GR part, coefficients: zeta-dot^2: " + str(coeffs(L2_GR)[0]) + " ; alpha^2: " + str(sp.simplify(sp.expand(L2_GR.subs(al, AL)).coeff(AL, 2))) + " ; psi appears as: " + str(sp.simplify(sp.diff(L2_GR, ps))))
info("chi part: " + str(sp.simplify(L2_chi)))
def reduce(L2x):
    """integrate out chi, alpha, psi (all algebraic in the quadratic Lagrangian); return the residual zeta Lagrangian."""
    Lr = L2x
    e_chi = sp.diff(Lr, ch)
    if e_chi.has(ch): Lr = sp.expand(Lr.subs(ch, sp.solve(e_chi, ch)[0]))
    e_ps = sp.diff(Lr, ps)                                           # psi is a Lagrange multiplier in GR: its equation constrains alpha
    if not e_ps.has(ps) and e_ps.has(al):
        Lr = sp.expand(Lr.subs(al, sp.solve(e_ps, al)[0]))
        e_al = sp.diff(Lr, ps) if Lr.has(ps) else sp.Integer(0)      # after substitution, psi may still appear linearly -> its coefficient must vanish
        # any remaining psi-dependence: solve the alpha-equation (now an equation for psi) if psi appears quadratically
        if Lr.has(ps):
            e2 = sp.diff(Lr, ps)
            if e2.has(ps): Lr = sp.expand(Lr.subs(ps, sp.solve(e2, ps)[0]))
            else: Lr = sp.expand(Lr.subs(ps, 0))                     # linear multiplier with vanishing coefficient on shell
    else:
        sol = sp.solve([sp.diff(Lr, al), sp.diff(Lr, ps)], [al, ps], dict=True)
        Lr = sp.expand(Lr.subs(sol[0]))
    return sp.simplify(Lr)
Lred_GR = reduce(L2_GR)
A_GR, B_GR, C_GR = coeffs(Lred_GR)
info("GR residual zeta Lagrangian: " + str(Lred_GR))
check("1b GR regression: with lam = 0 the residual zeta action has NO kinetic term (A = 0): vacuum de Sitter propagates no scalar", sp.simplify(A_GR) == 0, f"A_GR = {A_GR}")
P(""); P("="*100); P("2. with the CMC auxiliary: integrate out chi (its constraint), then alpha and psi"); P("="*100)
e_chi = sp.diff(L2, ch); chi_sol = sp.solve(e_chi, ch)[0]
W = sp.simplify(chi_sol/al)
info("chi = W alpha with W = " + str(sp.simplify(W)) + "   (the proposal's filter: k^2/(k^2 + a^2 xi^2 H^2), K-bar = 3H, m^2 = xi^2 H^2)")
check("2a integrating out chi reproduces the proposal's transfer function W = k^2 a^-2/(k^2 a^-2 + xi^2 H^2)", sp.simplify(W - (k**2/a**2)/(k**2/a**2 + xi**2*H**2)) == 0)
Lred = reduce(L2)
info("residual Lagrangian (raw): " + str(Lred))
A, B, C = coeffs(Lred)
A_hand = lam*a*k**2*W/(4*H**2)
info("hand derivation: L_chi,eff = (lam a k^2 W/4) alpha^2 with alpha = zeta-dot/H  =>  A_hand = " + str(sp.simplify(A_hand)))
check("2b' the sympy residual matches the hand derivation A = lam a k^2 W/(4 H^2)", sp.simplify(A - A_hand) == 0)
info("residual zeta Lagrangian: A zeta-dot^2 - B zeta^2 (+ C zeta zeta-dot):")
info("  A = " + str(A)); info("  B = " + str(B)); info("  C = " + str(C))
check("2b ONE PROPAGATING SCALAR: A != 0 for lam != 0 -- the lapse-gradient coupling d chi . d ln N frees a scalar mode; the reduced 4x4 block missed it because it did not contain the lapse",
      sp.simplify(A) != 0, f"A(lam->0) = {sp.simplify(sp.limit(A, lam, 0))}")
# large-k dispersion: c_s^2 = lim (B/A) / (k^2/a^2)
info(f"large-k: A -> {sp.simplify(sp.limit(A/a, k, sp.oo))} x a  (k-independent: a canonical dust-like mode) ; small-k: A -> {sp.simplify(sp.series(A, k, 0, 3).removeO())}")
tot = sp.simplify(sp.diff(C, t) + 2*B)
info(f"the zeta^2 and zeta zeta-dot terms are the GR ones; they form a total derivative iff C-dot + 2B = 0: C-dot + 2B = {tot}")
check("2c the extra scalar is DUST-LIKE: the (B, C) part is a pure total derivative (C-dot + 2B = 0, identical to GR), so the new mode's Lagrangian is A zeta-dot^2 alone -- zero gradient energy, c_s^2 = 0 (the mimetic class), positive kinetic term for lam > 0 (not a ghost): a cosmological dark-matter surrogate by construction",
      tot == 0 and sp.simplify(A.subs({lam: 1, xi: 1, H: 1, k: 1, t: 0})) > 0, f"C-dot + 2B = {tot}; A > 0")
info("its equation of motion is d/dt(A zeta-dot) = 0, and A ~ a k^2 W/H^2 -> k^4/(xi^2 H^4 a) as a -> oo: the kinetic coefficient vanishes in the infrared (strong coupling), and zeta-dot ~ 1/A grows like a")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  The reduced (Theta, chi) Dirac block was fine as far as it went; the lapse was not in it.  Once the coupling d chi . d ln N is")
P("  put into the ADM action, integrating out chi leaves a k-dependent lapse term, the lapse stops being a Lagrange multiplier, and")
P("  the curvature perturbation acquires a kinetic term A = lam a k^2 W/(4H^2) with NO gradient term: one extra scalar, dust-like")
P("  (c_s^2 = 0, the mimetic class), absent in GR (A_GR = 0).  By the proposal's own rule")
P("  ('if the full Hamiltonian analysis reveals a propagating mode, we kill it immediately') the branch-selective filter, as written,")
P("  is a dark field by another name.  The large-scale fix of the growth gate stands as a target for a construction that filters the")
P("  MOND enhancement without a lapse-gradient coupling -- that construction does not yet exist.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
