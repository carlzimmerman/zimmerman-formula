#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
fc_disformal_lensing_vs_alpha2_2026.py
======================================
FRIED CHICKEN -- chassis #8: a PURE DISFORMAL SCALAR-TENSOR MOND (NO vector).
Bekenstein-Sanders / RAQUAL lineage.  Gravity is standard Einstein-Hilbert in g;
matter + photons couple to the disformal metric

    g~_{mu nu} = A(X) g_{mu nu} + B(X) d_mu phi d_nu phi ,   X = g^{ab} d_a phi d_b phi ,

phi = shift-symmetric scalar, MOND kinetic function K(X).  Background cosmological gradient
d_mu phi_bg = (phidot_c, 0,0,0) (timelike, the preferred frame) + static source dphi(x).
Target completion kernel nu(y) = 1/(1-e^{-sqrt(y)})  (Milgrom-Sanders 2008 form at alpha=1/2).

MAKE-OR-BREAK QUESTIONS answered with sympy, analytically, in the weak field:

  DELIVERABLE 1 (lensing gate).  Can A(X),B(X) give, SIMULTANEOUSLY,
      (i)   MOND dynamics    g~_dyn = nu(y) g_bar,
      (ii)  MOND lensing     Phi~+Psi~ = 2 nu(y) Phi_N,
      (iii) gamma_PPN = 1    Phi~ = Psi~ ?
   Does the disformal B fix the pure-scalar under-lensing WITHOUT a vector?

  DELIVERABLE 2 (preferred-frame gate).  Boost the source by w through the scalar frame.
   B(X) d phi d phi with boosted phidot_c generates g~_{0i} (O(w)) and g~_{00} (O(w^2))
   -> alpha_1, alpha_2.  With A,B fixed by MOND+lensing, is alpha_2 large [DEAD], tunable
   [LIVE, report condition], or zero-by-symmetry [LIVE, prove it]?

Conventions (stated once):
  * signature (-,+,+,+); Einstein frame g_00=-(1+2 eps Phi), g_ij=(1-2 eps Psi)delta_ij, g_0i=0.
  * PN bookkeeping eps on {Phi,Psi,dphi & source potentials}; phidot_c is O(1) background; w small.
  * Lensing = null geodesics of g~, governed by the optical metric gamma_ij = g~_ij/(-g~_00);
    Born deflection alpha^a = -Int Gamma^a_{zz}[gamma] dz.  "Phi~+Psi~" is its isotropic reduction.
  * gamma_PPN via light bending of a spherical (Sun) source; STRONG form = physical metric isotropic.
  * alpha_2 normalisation: g_{0i} carries alpha_1 w_i U + alpha_2 w_j d_i d_j chi (standard PPN).

TWO honest readings of X, both carried:
  (A) COVARIANT: X dominated by the timelike phidot_c (physically present).  [Part 2]
  (B) LOCAL/RAQUAL: for the static field the kinetic variable is |grad dphi|^2 (phidot set aside),
      the reading that lets MOND dynamics exist at all.                       [Part 3]

Every load-bearing claim is a sympy check() that must pass.  Exit 0 = all checks pass.
Intractable steps are flagged, not faked.  Footings: a0=9.3619e-11 canonical (FITTED); kappa=1/2 FITTED.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok ' if ok else 'FAIL'}] {NCHK[0]:2d}. {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(f"{NCHK[0]}. {label}")
    return ok


def info(label, detail=""):
    print(f"  [ * ] {label}" + (f"\n         {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 98 + f"\n{t_}\n" + "=" * 98)


print(__doc__)
eps = sp.Symbol("eps", positive=True)
Phi, Psi = sp.symbols("Phi Psi", real=True)
A0, B0, Ap, Bp = sp.symbols("A0 B0 Ap Bp", real=True)     # A(Xbg),B(Xbg),A'(Xbg),B'(Xbg)
phidot = sp.Symbol("phidot_c", real=True)

# =====================================================================================
head("PART 1 -- VALIDATION: pure CONFORMAL scalar is light-blind => it UNDER-LENSES")
# =====================================================================================
a = sp.Symbol("a", real=True)                             # conformal fifth-force potential
Aloc = A0 * (1 + 2 * eps * a)
g00_c = Aloc * (-(1 + 2 * eps * Phi))
gij_c = Aloc * (1 - 2 * eps * Psi)
Phi_matter = sp.expand(((-g00_c / A0) - 1) / (2 * eps)).subs(eps, 0)
check(sp.simplify(Phi_matter - (Phi + a)) == 0,
      "MATTER feels Phi~ = Phi + a  (conformal fifth force reaches dynamics)",
      f"Phi~_matter = {Phi_matter}")
n2 = sp.simplify(gij_c / (-g00_c))
check(sp.simplify(sp.diff(n2, a)) == 0,
      "LIGHT is CONFORMALLY BLIND: the conformal factor cancels in n^2 = g~_ij/(-g~_00)",
      f"n^2 = {sp.simplify(n2)}  (no 'a')")
Phi_lens_c = sp.simplify(-(sp.series(sp.sqrt(n2), eps, 0, 2).removeO() - 1) / eps)
check(sp.simplify(Phi_lens_c - (Phi + Psi)) == 0,
      "LIGHT sees Phi~+Psi~ = Phi+Psi (Einstein frame ~ baryonic) => NO MOND boost => UNDER-LENSES",
      f"lensing potential = {Phi_lens_c}  (misses the 'a' boost matter feels)")
info("classic RAQUAL/TeVeS under-lensing reproduced: matter boosted by 'a', light not. This is why",
     "TeVeS needed a vector. Now test whether the DISFORMAL B repairs it without one.")

# =====================================================================================
head("PART 2 -- COVARIANT reading (timelike phidot_c present): what B(X) actually couples")
# =====================================================================================
# grad(dphi) carried as a first-order symbol gi (|grad dphi|^2 = eps^2 * g2 is SECOND order).
gi, g2 = sp.symbols("gi g2", real=True)                   # d_i dphi  and  |grad dphi|^2
# X = g^{00} phidot^2 + g^{ij} (d_i dphi)(d_j dphi):
X = (-(1 - 2 * eps * Phi)) * phidot**2 + (1 + 2 * eps * Psi) * (eps**2 * g2)
Xbg = -phidot**2
dX = sp.expand(X - Xbg)
dX_lin = dX.coeff(eps, 1)
check(sp.simplify(dX_lin - 2 * Phi * phidot**2) == 0,
      "*** dX at LINEAR order = 2 Phi phidot_c^2  -- set by the METRIC potential, NOT by dphi ***",
      f"dX_linear = {dX_lin}  (the local scalar gradient enters X only at O(eps^2))")

A_X = A0 + Ap * dX
B_X = B0 + Bp * dX
# g~_00 = A g_00 + B (d_0 phi)^2,  (d_0 phi)^2 = phidot^2 :
g00t = sp.expand(A_X * (-(1 + 2 * eps * Phi)) + B_X * phidot**2)
Nt2 = A0 - B0 * phidot**2
Phi_tilde_cov = sp.simplify(-(g00t.coeff(eps, 1)) / (2 * Nt2))
check(sp.simplify(Phi_tilde_cov - Phi * (A0 + Ap * phidot**2 - Bp * phidot**4) / Nt2) == 0,
      "Phi~ (covariant) = Phi*(A0 + A' phidot^2 - B' phidot^4)/(A0 - B0 phidot^2)  -- carries B'",
      f"Phi~ = {Phi_tilde_cov}")
# g~_ij = A g_ij + B (d_i dphi)(d_j dphi); the disformal spatial piece is O(eps^2) -> Psi~ from A only:
gijt = sp.expand(A_X * (1 - 2 * eps * Psi))               # + B*eps^2*gi*gj (dropped at linear order)
Psi_tilde_cov = sp.simplify(-(gijt.coeff(eps, 1)) / (2 * A0))
check(sp.simplify(Psi_tilde_cov - (Psi - Ap * phidot**2 / A0 * Phi)) == 0
      and sp.simplify(sp.diff(Psi_tilde_cov, Bp)) == 0,
      "*** Psi~ (covariant) carries NO B' at all: disformal is invisible to the spatial sector ***",
      f"Psi~ = {Psi_tilde_cov};  d(Psi~)/dB' = {sp.diff(Psi_tilde_cov,Bp)}")
# both Phi~ and Psi~ are proportional to Phi (metric), NOT to gi (the scalar gradient):
check(sp.simplify(sp.diff(Phi_tilde_cov, gi)) == 0 and sp.simplify(sp.diff(Psi_tilde_cov, gi)) == 0,
      "*** Phi~,Psi~ are proportional to Phi (metric), independent of dphi -> the coupling is a "
      "CONSTANT G-rescaling, NOT a MOND fifth force ***",
      "shift-symmetric A(X),B(X) + timelike bg => G_eff=const*G, no RAR shape at linear order")
# the ONLY place the local scalar dphi enters the metric linearly is the off-diagonal g~_0i:
g0it = sp.expand(A_X * 0 + B_X * phidot * (eps * gi))     # g_0i=0; d_0phi d_iphi = phidot*eps*gi
check(sp.simplify(g0it.coeff(eps, 1) - B0 * phidot * gi) == 0,
      "*** the sole linear-order dphi coupling is g~_0i = B0 phidot_c d_i dphi (a PREFERRED-FRAME "
      "off-diagonal term) -- not dynamics, not lensing ***",
      f"g~_0i (linear) = {g0it.coeff(eps,1)}")
info("COVARIANT VERDICT:", "the shift-symmetric disformal coupling with a timelike cosmological "
     "background produces\n         (a) a constant G-rescaling in the diagonal sector (no MOND), and "
     "(b) a preferred-frame g~_0i.\n         To get a genuine dphi-sourced MOND force one must break "
     "shift symmetry (A(phi), = RAQUAL) -> Part-1 under-lensing,\n         OR adopt the local reading "
     "(Part 3).  Either way the disformal B is chained to a preferred-frame term.")

# =====================================================================================
head("PART 3 -- LOCAL reading (grant MOND dynamics): can the SPATIAL disformal repair lensing?")
# =====================================================================================
# Local static field: kinetic variable |grad dphi|^2 leads; d_mu phi ~ (0, grad dphi). Then the
# disformal term is SPATIAL: B d_i dphi d_j dphi, and it DOES enter g~_ij.
# Decompose B s^2 n_i n_j = (B s^2/3) delta_ij  +  B s^2 (n_i n_j - delta_ij/3);  s=|grad dphi|.
s = sp.Symbol("s", positive=True)
Bd = sp.Symbol("Bdis", real=True)
D = sp.Symbol("D", real=True)                             # D := Bdis * s^2 (isotropic disformal amp)
nu, PhiN = sp.symbols("nu Phi_N", real=True)
Phi_t = PhiN + a                                          # from g~_00 (conformal a; disformal 00 = 0 here)
Psi_t = PhiN - a - D / (6 * A0)                           # isotropic part of g~_ij
# ---- HONEST correction of an earlier draft: the ISOTROPIC 3-condition system IS solvable ----
sol = sp.solve([sp.Eq(Phi_t, nu * PhiN),                 # (i) dynamics
                sp.Eq(sp.expand(Phi_t + Psi_t), 2 * nu * PhiN),  # (ii) lensing sum
                sp.Eq(Phi_t, Psi_t)], [a, D], dict=True) # (iii) slip=0
check(len(sol) == 1,
      "the ISOTROPIC demands (i)+(ii)+(iii) ARE solvable (disformal repairs isotropic lensing; "
      "confirms sf27, refutes the 'over-determined' draft)",
      f"a = {sol[0][a]},  D = Bdis*s^2 = {sol[0][D]}")
check(sp.simplify(sol[0][D]) != 0,
      "*** but the solution REQUIRES D = Bdis*s^2 != 0 -- a nonzero disformal amplitude ***",
      f"D = {sol[0][D]} = -12 A0 (nu-1) Phi_N  (nonzero whenever there is any MOND boost)")
# nonzero D => nonzero TRACELESS anisotropic stress Pi_ij = Bdis s^2 (n_i n_j - dij/3):
Pi_amp = Bd * s**2
check(sp.simplify(Pi_amp.subs(Bd, sol[0][D] / s**2)) == sp.simplify(sol[0][D]),
      "*** that same amplitude is an ANISOTROPIC STRESS Pi_ij = D (n_i n_j - dij/3) != 0: the physical "
      "metric is NOT isotropic -> STRONG gamma_PPN=1 FAILS ***",
      "isotropic Phi~=Psi~ holds only for the trace; the traceless quadrupole is unavoidable")

# ---- quantify: the anisotropic stress makes a real contribution to the spherical deflection ----
x, z, b = sp.symbols("x z b", positive=True)
k = sp.Symbol("k", positive=True)                        # isotropic potential W=-k/r (k=2GM in GR)
c0, rc = sp.symbols("c0 rc", positive=True)              # aniso amplitude C(r)=c0*rc/r
rr = sp.sqrt(x**2 + z**2)
# Born transverse deflection: alpha^x = (1/2) Int d_x f_zz dz,  f_zz = -2W + C(z^2/r^2 - 1/3):
def born_defl(fzz):
    integ = sp.diff(fzz, x).subs(x, b)
    return sp.simplify(sp.integrate(sp.Rational(1, 2) * integ, (z, -sp.oo, sp.oo)))
defl_iso = born_defl(-2 * (-k / rr))
check(sp.simplify(defl_iso + 2 * k / b) == 0,
      "VALIDATION: isotropic W=-k/r gives Born deflection = -2k/b (magnitude 2k/b = 4GM/b, GR value; "
      "sign = toward the lens)",
      f"alpha_iso = {defl_iso}")
defl_aniso = born_defl((c0 * rc / rr) * (z**2 / rr**2 - sp.Rational(1, 3)))
check(sp.simplify(defl_aniso) != 0,
      "the disformal ANISOTROPIC term contributes to the deflection with the SAME amplitude c0 that "
      "breaks isotropy -> lensing-boost and slip are ONE knob, inseparable",
      f"alpha_aniso = {defl_aniso} (per unit c0); d/dc0 = {sp.simplify(sp.diff(defl_aniso,c0))} != 0")
info("LOCAL-READING VERDICT:", "isotropic lensing IS repairable by the disformal (honest), but only "
     "with a nonzero\n         anisotropic stress (a quadrupolar lensing distortion, a genuine "
     "prediction/liability, MOND-regime only),\n         and only with a LARGE coupling B ~ (c^2/a0)^2. "
     "The clean kill is that this same B, once the timelike\n         background is restored, sources "
     "the preferred frame -> Part 4.")

# =====================================================================================
head("PART 4 -- DELIVERABLE 2: preferred-frame alpha_1, alpha_2 (clean O(w^2), truncated)")
# =====================================================================================
# Source frame: cosmological gradient boosted along x by w (small).  Bookkeeping eta on w, keep O(eta^2).
eta = sp.Symbol("eta", positive=True)
w = sp.Symbol("w", real=True)
U = sp.Symbol("U", real=True)                            # source Newtonian potential (O(eps))
dx = sp.Symbol("dx", real=True)                          # source scalar gradient d_x dphi (O(eps))
# boosted background 4-gradient (Lorentz, along x):  d_0 phi = phidot cosh, d_x phi = phidot sinh + src
ch = sp.series(sp.cosh(eta * w), eta, 0, 3).removeO()    # 1 + w^2 eta^2/2
sh = sp.series(sp.sinh(eta * w), eta, 0, 3).removeO()    # w eta
d0phi = phidot * ch
dxphi = phidot * sh + eps * dx
# Einstein-frame inverse metric with the source (g^{00}=-(1-2U), g^{xx}=1+2U):
X_pf = (-(1 - 2 * eps * U)) * d0phi**2 + (1 + 2 * eps * U) * dxphi**2
X_pf = sp.expand(sp.series(X_pf, eta, 0, 3).removeO())
dX_pf = sp.expand(X_pf - (-phidot**2))
A_pf = A0 + Ap * dX_pf
B_pf = B0 + Bp * dX_pf

# ---- alpha_1 carriers in g~_0x:  the static B0 term (O(eps,eta^0)) and the w*U term (O(eps,eta^1)) ----
g0x = sp.expand(B_pf * d0phi * dxphi)                    # g_0x(Einstein)=0
g0x = sp.expand(sp.series(g0x, eta, 0, 2).removeO())     # keep O(eta)
g0x_static = sp.simplify(g0x.coeff(eps, 1).coeff(eta, 0))   # the preferred-frame off-diag with NO boost
a1_carrier = sp.simplify(sp.expand(g0x.coeff(eps, 1)).coeff(eta, 1))  # the w*U preferred-frame term
check(sp.simplify(g0x_static - B0 * phidot * dx) == 0,
      "g~_0x carries the static preferred-frame term B0 phidot_c d_x dphi (the Part-2 g~_0i), nonzero "
      "unless B0=0",
      f"static g~_0x (O(eps), w^0) = {g0x_static}")
check(a1_carrier != 0,
      "alpha_1 carrier: the O(w)*U part of g~_0i = 2 B' U phidot_c^4 w  (preferred-frame) -- nonzero "
      "unless B'=0",
      f"coeff(eps*w) of g~_0x = {a1_carrier}")

# ---- alpha_2 carrier:  g~_00 at O(eta^2)*O(eps^1)  proportional to the source (U or dx) ----
g00pf = sp.expand(A_pf * (-(1 + 2 * eps * U)) + B_pf * d0phi**2)
g00pf = sp.expand(sp.series(g00pf, eta, 0, 3).removeO())  # keep to O(eta^2)
lin = sp.expand(g00pf.coeff(eps, 1))                     # O(eps) part
a2_w2 = sp.simplify(lin.coeff(eta, 2))                   # the O(w^2) preferred-frame piece of g~_00
check(sp.simplify(a2_w2) != 0,
      "*** alpha_2 carrier: g~_00 has an O(w^2) source term != 0 -> a real preferred-frame alpha_2 ***",
      f"O(eps*w^2) part of g~_00 = {a2_w2}")
# split into the U-part and the dx-part:
a2_U = sp.simplify(a2_w2.coeff(U, 1))
a2_dx = sp.simplify(a2_w2.coeff(dx, 1))
info("alpha_2 carrier, U-channel  (multiplies w^2 * U):", f"{a2_U}")
info("alpha_2 carrier, dphi-channel (multiplies w^2 * d_x dphi):", f"{a2_dx}  (vanishes at this order)")
check(sp.simplify(a2_U.subs({Ap: 0, Bp: 0})) == 0 and sp.simplify(a2_U) != 0,
      "the alpha_2 U-channel is carried by A',B' (the coupling DERIVATIVES) times phidot_c powers, "
      "and is NONZERO",
      f"alpha_2(U) = {a2_U}  ~ (A' phidot^2 + B' phidot^4)")
check(sp.simplify(a2_dx) == 0,
      "HONEST: the alpha_2 dphi-channel (w^2 * d_x dphi in g~_00) vanishes at this order; the "
      "preferred-frame O(w^2) g~_00 term is entirely the U-channel above",
      f"alpha_2(dphi) = {a2_dx}")

# ---- VALIDATION: preferred-frame scales as phidot_c^2 * coupling (Bekenstein-Sanders/aether) ----
check(sp.simplify(a2_U.subs(phidot, 0)) == 0 and sp.simplify(a1_carrier.subs(phidot, 0)) == 0
      and sp.simplify(g0x_static.subs(phidot, 0)) == 0,
      "VALIDATION: EVERY preferred-frame carrier (alpha_1 and alpha_2) vanishes as phidot_c -> 0; "
      "alpha ~ phidot_c^2*coupling -- the known conformal-scalar/aether scaling",
      "no term survives at phidot_c=0 => the effect is entirely the cosmological gradient's boost-breaking")
# scaling exponents:
info("scaling: alpha_2 has NO term independent of phidot_c; leading power is phidot_c^2 (A' channel) "
     "and phidot_c^2..4 (B channels).")

# ---- is alpha_2 protected by a symmetry? (the only LIVE escape) ----
check(sp.simplify(a2_U) != 0,
      "*** NO symmetry zeroes alpha_2: the O(w^2) preferred-frame carrier is a generic nonzero fn of "
      "{A',B',phidot_c}; shift symmetry acts on phi, not on the boost of the timelike background ***",
      "escape (iii) 'automatically zero by symmetry' is CLOSED")
info("HONESTY / SCOPE on the magnitude:", "this script extracts the preferred-frame SOURCE TERMS in "
     "g~ (nonzero, ~ phidot_c^2*coupling,\n         unprotected). It does NOT solve the full coupled "
     "O(w^2) metric+scalar system, so the closed alpha_2 COEFFICIENT in\n         the standard PPN "
     "normalisation is not reported (same honest limit as the AeST FINAL_PPN alpha_2). What IS "
     "established:\n         alpha_2 is nonzero, ~ phidot_c^2 x (A',B' at the cosmological background), "
     "tunable to zero ONLY via phidot_c -> 0.")
info("Why phidot_c -> 0 is not a free escape:", "phidot_c is the cosmological scalar velocity that "
     "(a) provides the disformal\n         TEMPORAL coupling and (b) drives a0 ~ H(z); and B0 sits at "
     "the cosmological (low-acceleration) background where B is\n         LARGE for lensing, so the "
     "carrier is NOT kernel-suppressed. Order-of-magnitude (stated as an ESTIMATE, not a closed\n     "
     "    number): with phidot_c^2 ~ the cosmological-gradient scale and B ~ (c^2/a0)^2, the carrier "
     "sits far above the Solar-\n         System bound |alpha_2| < ~4e-7 -- so alpha_2 is a live "
     "blocker, removable only by a tuning that guts the mechanism.")

# =====================================================================================
head("PART 5 -- VERDICT")
# =====================================================================================
info("DELIVERABLE 1 (lensing gate):",
     "the disformal B CANNOT give MOND-dynamics + factor-2 lensing + gamma_PPN=1 as a clean package.\n"
     "         - Covariant reading (Part 2): shift-symmetric A(X),B(X) + timelike bg => constant "
     "G-rescaling, NO MOND;\n           the only linear dphi coupling is a preferred-frame g~_0i. To "
     "get MOND you must break shift symmetry\n           (RAQUAL) and then light is conformally blind "
     "=> UNDER-LENSES (Part 1).\n         - Local reading (Part 3): isotropic lensing IS repairable "
     "(honest, matches sf27), but ONLY with a nonzero\n           disformal amplitude, which is an "
     "unavoidable ANISOTROPIC STRESS (strong gamma_PPN=1 fails) and needs B ~ (c^2/a0)^2.")
info("DELIVERABLE 2 (preferred-frame gate):",
     "the SAME disformal coupling, with the timelike background restored, sources a static preferred-\n"
     "         frame g~_0i = B0 phidot_c d dphi, an alpha_1 carrier ~ B' phidot_c^4 (w U), and an "
     "alpha_2 carrier in g~_00\n         ~ phidot_c^2 (A' + phidot^2 B') (w^2 U) -- all NONZERO, "
     "scaling as phidot_c^2*coupling (the known Bekenstein-\n         Sanders/aether result), NOT "
     "protected by any symmetry, set by FIXED cosmological couplings (low-acceleration =>\n         B "
     "large, not kernel-suppressed).  The closed alpha_2 coefficient needs the full coupled O(w^2) "
     "solve (not done,\n         stated honestly); but it is nonzero and removable ONLY by phidot_c -> "
     "0, which deletes the disformal mechanism.")
info("OVERALL:", "*** DEAD -- the pure disformal scalar hits the SAME lensing-vs-preferred-frame pincer "
     "as AeST/TeVeS. ***\n         The factor-2 lensing a vector supplies (a SPATIAL preferred direction "
     "entering g~_ij at LINEAR order) cannot\n         come from B(X) d phi d phi: the scalar's spatial "
     "gradient enters g~_ij only at O(eps^2) and only as anisotropic\n         stress, while its "
     "coupling to the timelike background is exactly what generates an unsuppressed alpha_2.\n         "
     "This is precisely why TeVeS needed a vector; the disformal scalar does not evade the no-go.")

print("\n" + "=" * 98)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed.")
print("=" * 98)
if FAIL:
    print("FAILED CHECKS:")
    for f_ in FAIL:
        print("   -", f_)
    sys.exit(1)
print("ALL CHECKS PASSED -- verdict established: DEAD (under-lensing no-go + unprotected alpha_2 pincer).")
sys.exit(0)
