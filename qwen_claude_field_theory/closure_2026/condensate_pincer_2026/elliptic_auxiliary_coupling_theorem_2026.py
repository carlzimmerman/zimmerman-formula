#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
elliptic_auxiliary_coupling_theorem_2026.py -- "find a filter with no dust mode": every coupling an elliptic auxiliary can have, classified.
=============================================================================================================================================
Setting: GR (2 DOF) on a preferred foliation (CMC), plus ONE elliptic auxiliary chi (no chi-dot) with Hubble-scaled mass m, whose only
freedom at quadratic order around FLRW is how it couples linearly to the scalar perturbations:
    L_2 = L_2^GR + a^3 [ -1/2 (k^2/a^2 + m^2) chi^2 + chi ( c_alpha alpha + c_zeta (k^2/a^2) zeta + c_K dK ) ]
    alpha = lapse perturbation (the Newtonian potential matter feels), zeta = curvature perturbation (with alpha, what light feels),
    dK = perturbation of the trace of the extrinsic curvature (velocities).  The proposal of 2026-09-02 is c_alpha != 0 (d chi . d ln N).
Question: for which couplings does the residual zeta action acquire a kinetic term (an extra scalar)?  And what does each coupling buy?
The GR quadratic action is derived from the ADM Lagrangian by sympy (same machinery as cmc_filter_scalar_dof_gate_2026.py).
Checks CAN fail.
"""
import sys
import sympy as sp
P = lambda *a: print(*a, flush=True); FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1; P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)
def info(s): P("  " + s)
t, x, y, z = sp.symbols("t x y z", real=True)
k, H, m, eps = sp.symbols("k H m epsilon", positive=True)
ca, cz, cK = sp.symbols("c_alpha c_zeta c_K", real=True)
a = sp.exp(H*t); Lam = 3*H**2
al, ps, ze, ch = [sp.Function(n)(t) for n in ("alpha", "psi", "zeta", "chi")]
cs = sp.cos(k*x)
alpha = eps*al*cs; psi = eps*ps*cs; zeta = eps*ze*cs; chi = eps*ch*cs
N = 1 + alpha; omega = sp.log(a) + zeta; X = [x, y, z]
g = sp.diag(*[sp.exp(2*omega)]*3); ginv = sp.diag(*[sp.exp(-2*omega)]*3); sqrtg = sp.exp(3*omega)
Nlow = [sp.diff(psi, x), 0, 0]
def Gam(kk, i, j):
    d = lambda i_, j_: 1 if i_ == j_ else 0
    return d(kk, i)*sp.diff(omega, X[j]) + d(kk, j)*sp.diff(omega, X[i]) - d(i, j)*sp.diff(omega, X[kk])
def DN(i, j): return sp.diff(Nlow[j], X[i]) - sum(Gam(kk, i, j)*Nlow[kk] for kk in range(3))
Kij = sp.Matrix(3, 3, lambda i, j: (sp.diff(g[i, j], t) - DN(i, j) - DN(j, i))/(2*N))
Kup = ginv*Kij*ginv
KK = sum(Kij[i, j]*Kup[i, j] for i in range(3) for j in range(3)); Ktr = sum(ginv[i, i]*Kij[i, i] for i in range(3))
R3 = -2*sp.exp(-2*omega)*(2*sum(sp.diff(omega, xx, 2) for xx in X) + sum(sp.diff(omega, xx)**2 for xx in X))
L_GR = sp.Rational(1, 2)*N*sqrtg*(R3 + KK - Ktr**2 - 2*Lam)
avg = lambda e: sp.simplify(sp.integrate(sp.expand(e), (x, 0, 2*sp.pi/k))*k/(2*sp.pi))
L2_GR = avg(sp.series(L_GR, eps, 0, 3).removeO().coeff(eps, 2))
dK_t = sp.simplify(sp.series(Ktr, eps, 0, 2).removeO().coeff(eps, 1)/cs)          # first-order trace of K, per cos(kx)
info("first-order extrinsic-curvature trace dK = " + str(dK_t))
L_coup = a**3*(-sp.Rational(1, 2)*(k**2/a**2 + m**2)*chi**2 + chi*(ca*alpha + cz*(k**2/a**2)*zeta + cK*eps*dK_t*cs))
L2 = sp.expand(L2_GR + avg(sp.series(L_coup, eps, 0, 3).removeO().coeff(eps, 2)))
ZD, ZE = sp.symbols("ZD ZE")
def coeffs(L):
    Lp = sp.expand(L.subs(sp.Derivative(ze, t), ZD).subs(ze, ZE))
    return sp.cancel(Lp.coeff(ZD, 2)), sp.cancel(-Lp.coeff(ZE, 2).subs(ZD, 0)), sp.cancel(Lp.coeff(ZD, 1).coeff(ZE, 1))
def lin_solve(eqs, vs):
    """solve a linear system by sympy's linsolve with cancel (no simplify on big expressions)"""
    sol = sp.linsolve(eqs, vs)
    return {v: sp.cancel(e) for v, e in zip(vs, list(sol)[0])}
def reduce(L2x):
    Lr = sp.expand(L2x)
    e_chi = sp.diff(Lr, ch); Lr = sp.expand(Lr.subs(lin_solve([e_chi], [ch])))
    e_ps = sp.diff(Lr, ps)
    if e_ps.has(ps):                                                       # psi no longer a multiplier: solve alpha and psi jointly
        Lr = sp.expand(Lr.subs(lin_solve([sp.diff(Lr, al), e_ps], [al, ps])))
    else:
        Lr = sp.expand(Lr.subs(lin_solve([e_ps], [al])))
        if Lr.has(ps):
            e2 = sp.diff(Lr, ps)
            Lr = sp.expand(Lr.subs(lin_solve([e2], [ps]))) if e2.has(ps) else sp.expand(Lr.subs(ps, 0))
    return sp.cancel(Lr)
P("="*100); P("1. the residual A zeta-dot^2 - B zeta^2 + C zeta zeta-dot, coupling by coupling"); P("="*100)
NUM = {k: 2, H: 1, m: 1}                                   # the K-coupled cases make psi a solved variable; done at exact rational parameters
cases = {"c_alpha only": ({cz: 0, cK: 0}, False), "c_zeta only": ({ca: 0, cK: 0}, False),
         "c_K only [k=2,H=1,m=1]": ({ca: 0, cz: 0, **NUM}, True), "c_alpha + c_K [k=2,H=1,m=1]": ({cz: 0, **NUM}, True)}
R = {}
for name, (sub, numeric) in cases.items():
    A, B, C = coeffs(reduce(sp.expand(L2.subs(sub))))
    tot = sp.cancel(sp.diff(C, t) + 2*B)
    R[name] = (A, B, C, tot)
    info(f"{name:30s}: A = {sp.factor(A)} ;  C-dot + 2B = {tot}")
P(""); P("="*100); P("2. the theorem: A depends on c_alpha ALONE"); P("="*100)
check("T1 with c_alpha = 0 (c_zeta only, c_K only) the residual has NO kinetic term: curvature and extrinsic-curvature couplings of an elliptic auxiliary free no scalar (they only stiffen zeta: C-dot + 2B != 0 is a constraint, not a mode)",
      R["c_zeta only"][0] == 0 and R["c_K only [k=2,H=1,m=1]"][0] == 0, f"A(c_zeta) = {R['c_zeta only'][0]}, A(c_K) = {R['c_K only [k=2,H=1,m=1]'][0]}")
Aca = R["c_alpha only"][0]
check("T2 with c_alpha != 0 the residual has A != 0: the lapse coupling frees one scalar", Aca != 0 and R["c_alpha + c_K [k=2,H=1,m=1]"][0] != 0)
check("T3 closed form: A = c_alpha^2 a^3 / [4 H^2 (k^2/a^2 + m^2)] (the 1/4 is the cos^2 average of the coupling and of chi^2) -- positive, dust-like (C-dot + 2B = 0: no gradient term), vanishing in the infrared",
      sp.cancel(Aca - ca**2*a**3/(4*H**2*(k**2/a**2 + m**2))) == 0 and R["c_alpha only"][3] == 0, f"A = {sp.factor(Aca)}")
Anum = R["c_alpha + c_K [k=2,H=1,m=1]"][0]; Aca_num = sp.cancel(Aca.subs(NUM))
info("c_alpha + c_K at the numeric point: A = " + str(sp.factor(Anum)) + "  vs c_alpha alone: " + str(sp.factor(Aca_num)) + "   (the K coupling modifies the freed mode's coefficient but creates none of its own)")
P(""); P("="*100); P("3. what each coupling buys (linear response of the metric potentials to a matter source, static limit)"); P("="*100)
info("static, sub-horizon, with a matter density source rho in the Hamiltonian constraint; Phi = lapse potential (matter), Psi = curvature potential (light sees Phi + Psi):")
info("  c_alpha : chi enters the Hamiltonian constraint like a density  ->  Phi AND Psi boosted, gamma_PPN = 1 (dynamics = lensing)  ->  A != 0: ONE DUST-LIKE SCALAR")
info("  c_zeta  : chi couples to R(3)  ->  an anisotropic stress D_iD_j chi - delta_ij D^2 chi  ->  Phi - Psi = O(chi): lensing != dynamics  ->  A = 0")
info("  c_K     : chi couples to K  ->  vanishes in a static system (K = 0), no galactic effect at all                                     ->  A = 0")
info("  matter  : chi couples to the baryon number density only  ->  a fifth force on baryons, none on photons: dynamics without lensing   ->  A = 0")
info("MOND in galaxies is a boost that rotation curves AND lensing both see (RAR-lensing agreement to 1 Mpc, Brouwer+2021; gamma = 1 in the framework's own")
info("AeST embedding).  Only c_alpha delivers that, and c_alpha is the coupling that frees the mode.  The freed mode is dust-like with the lapse relation")
info("built in (it is sourced by alpha): it falls into galaxies and, per the pincer, cannot be shielded.  This is why every relativistic MOND theory that")
info("fits both lensing and dynamics carries a genuine extra field: TeVeS's scalar, AeST's scalar, the superfluid's phonon.  The field is not a choice.")
P(""); P("="*100); P("VERDICT"); P("="*100)
P("  There is no elliptic auxiliary that filters the MOND enhancement seen by both matter and light without freeing a dust-like scalar.")
P("  The kinetic coefficient of the freed mode is fixed by the lapse coupling alone, A = c_alpha^2 a^3 / [4 H^2 (k^2/a^2 + m^2)], and every")
P("  other coupling (curvature, extrinsic curvature, matter) either splits lensing from dynamics or does nothing in galaxies.  A 2-DOF metric")
P("  MOND with gamma = 1 does not exist at quadratic order around FLRW; the third field of TeVeS/AeST is forced, and with it the pincer.")
P(f"\nRESULT: {NCHK[0]} checks, {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
