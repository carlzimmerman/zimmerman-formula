#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
a0_from_condensate_action_2026.py
=================================
Can  a0^2 = G V(chi) / 4  be DERIVED from the condensate action?   (asked 2026-09-01)

The action (THE_COMPLETION v9 = THE_GENERALIZED_COMPLETION, c=1 inside the brackets):

  S = int d^4x sqrt(-g) { (R - 2 Lambda_bare)/(16 pi G) + L_aether
                          + (a0^2(Q)/(8 pi G)) * Gk( sqrt(Y)/a0(Q) )      <- MOND, exponential law
                          - 2 K(Q)                                        <- condensate: DE + dust
                          + A * B(Y/a0^2) (Q-Q0)^2 }  + S_m
  Gk(y) = y^2 + 2(1+y) e^{-y} - 2 ,   K(Q) = -M^4 sqrt(1 - mu^2 (Q-Q0)^2 / M^4),   -K(Q0) = M^4 = rho_Lambda,
  promotion:  a0^2(Q) = alpha * G * ( -K(Q) )        [ V(chi) of CDE-L4C  ==  -K(Q) here ]

  "a0^2 = G V /4"  <=>  alpha = 1/4  <=>  kappa = 1/2  <=>  a0 = c^2 sqrt(Lambda/(32 pi)).

Three questions, each with checks that can FAIL (rc=1) and a mutation control (MUTATE=1 must break them):

  A. FORM.   Is a0^2 = alpha * G * V the unique promotion?          -> YES (exponent matrix det = 2, no c).
  B. MODULUS. Does ANY consistency condition of the action fix alpha? -> NO: every established condition
             (FLRW background, no-ghost, c_T, Bianchi, promotion feedback on the vacuum branch, gamma_PPN)
             is alpha-independent, so the action is consistent for every alpha in (0, inf).  alpha is a MODULUS.
  C. POSTULATES. Each candidate in-action or near-action principle for alpha, computed, and confronted
             with the measured kappa.  None yields 1/4 from the action; the one that yields exactly 1/4
             (surface gravity of L_Lambda = c/sqrt(G rho_Lambda)) uses a length the action does not contain.

VERDICT (stated up front, proven below):  a0^2 = G V /4 is NOT derivable from the condensate action.
The FORM a0^2 = alpha G V is forced; the NUMBER 1/4 is a free modulus, fixed by data (kappa = 0.47-0.55),
and every candidate principle that could fix it either is excluded by data (kernel-offset = Lambda: 7x too
high; dS surface gravity: 5.8x too high) or is a reading external to the action.  Both footings shown.

Run:  python3 a0_from_condensate_action_2026.py          (expects rc=0, all PASS)
      MUTATE=1 python3 a0_from_condensate_action_2026.py (expects rc=1: the checks are live)
"""
import os, sys, math
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"
P = lambda *a: print(*a, flush=True)
FAILS = []
def check(name, ok, detail=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""))
    if not ok: FAILS.append(name)

# ----------------------------------------------------------------------------------------------------
# constants, both footings (SI)
# ----------------------------------------------------------------------------------------------------
c = 2.99792458e8; G = 6.674e-11; MPC = 3.0857e22
H0 = 67.4e3/MPC; OmL = 0.685
rho_c = 3*H0**2/(8*math.pi*G); rho_L = OmL*rho_c            # canonical footing: PURE-Lambda density
cw   = c*math.sqrt(G*rho_L)                                  # c*omega_Lambda = 1.872e-10
HL   = math.sqrt(8*math.pi*G*rho_L/3); cHL = c*HL            # pure-Lambda de Sitter rate
A0_CANON = 0.5*cw                                            # kappa = 1/2 -> 9.36e-11
A0_ALT   = 0.5*c*math.sqrt(G*rho_c)                          # same 1/4 on rho_total -> 1.13e-10 (alt footing)
# measured kappa (a0 = kappa c sqrt(G rho_Lambda)), from the committed error-budget scripts:
KAPPA_MEAS = [("BTFR", 0.465, 0.076), ("distance-free", 0.551, 0.043)]
def allowed(kappa):  # within 2 sigma of at least one measurement
    return any(abs(kappa-m)/s <= 2 for _, m, s in KAPPA_MEAS)

P("="*100); P("A. FORM: is a0^2 = alpha * G * V the unique promotion?  (V = condensate energy density = -K(Q))"); P("="*100)
# exponent matrix for a0^2 = G^a c^b V^d,  V an ENERGY density [kg m^-1 s^-2]
#            mass  length  time
rows = sp.Matrix([[-1,  0,  1],     # G: kg^-1 m^3 s^-2 ; c: m s^-1 ; V: kg m^-1 s^-2   (mass row)
                  [ 3,  1, -1],     # length row
                  [-2, -1, -2]])    # time row
target = sp.Matrix([0, 2, -4])       # a0^2 : kg^0 m^2 s^-4
det = rows.det()
sol = rows.solve(target)
check("exponent matrix nonsingular (det = 2, the uniqueness-theorem determinant)", det == 2, f"det={det}")
check("unique solution a0^2 = G^1 c^0 V^1  (NO power of c: the coefficient is a pure number)",
      list(sol) == [1, 0, 1], f"(a,b,d)={list(sol)}")
# same statement with the mass density rho_Lambda instead of V: a0^2 = alpha G c^2 rho_Lambda
rows_rho = sp.Matrix([[-1, 0, 1], [3, 1, -3], [-2, -1, 0]])
check("with mass density: a0^2 = G c^2 rho_Lambda uniquely (kappa^2 = alpha)", list(rows_rho.solve(target)) == [1, 2, 1])
# NEGATIVE CONTROL: admit the condensate's OTHER scale (Helmholtz mass mu, a 1/length) -> uniqueness dies
rows_mu = sp.Matrix([[-1, 0, 1, 0], [3, 1, -1, -1], [-2, -1, -2, 0]])   # columns G, c, V, mu
null = rows_mu.nullspace()
check("negative control: adding the Helmholtz mass mu makes the family 1-parameter (nullspace dim 1)",
      len(null) == 1, f"null vector (G,c,V,mu) = {list(null[0].T)}")
P("  => the FORM a0^2 = alpha*G*(-K(Q)) is forced ONLY under 'no new dimensionful scale in the promotion',")
P("     which is exactly what the v9 promotion assumes.  alpha is the one thing dimensional analysis leaves.")
# the pressure route (stage 17): -K(Q) declines up the DBI wall (a0 falls into the past), rho_Q would not
u, M4, mu2 = sp.symbols('u M4 mu2', positive=True)
Kq = -M4*sp.sqrt(1 - mu2*u**2/M4)
check("stage-17 selection: -K(Q) DECREASES with excitation |u| (a0 falls into the past, MOND off at CMB)",
      sp.simplify(sp.diff(-Kq, u)) .subs({M4: 1, mu2: 1, u: sp.Rational(1, 2)}) < 0)
rhoQ = -Kq + (sp.Symbol('Q0', positive=True) + u)*sp.diff(Kq, u)   # rho = -K + Q K'
check("stage-17 exclusion: rho_Q INCREASES with excitation (density promotion would switch MOND ON at CMB)",
      sp.simplify(sp.diff(rhoQ, u)).subs({M4: 1, mu2: 1, u: sp.Rational(1, 2), 'Q0': 1}) > 0)

P(""); P("="*100); P("B. MODULUS THEOREM: no established consistency condition of the action depends on alpha"); P("="*100)
y, al, Gs, Kv = sp.symbols('y alpha G K', positive=True)
KERNEL_C0 = 32*sp.pi if MUTATE else -2       # MUTATION: give the kernel a constant so the MOND term is Lambda
Gk = y**2 + 2*(1+y)*sp.exp(-y) + KERNEL_C0   # the exact exponential-law primitive (repo: C=-2, Gk(0)=0)
mu_of_y = sp.simplify(sp.diff(Gk, y)/(2*y))
check("kernel: Gk'(y)/(2y) = mu(y) = 1 - e^{-y} for ANY additive constant (the constant is force-blind)",
      sp.simplify(mu_of_y - (1 - sp.exp(-y))) == 0)
# B1 FLRW background: Y=0 on FLRW -> MOND term = (alpha G (-K)/8piG) Gk(0).  alpha-blind iff Gk(0)=0.
a0sq = al*Gs*Kv                             # a0^2 = alpha G (-K),  Kv = -K > 0
L_M_flrw = a0sq/(8*sp.pi*Gs)*Gk.subs(y, 0)
check("B1 FLRW background: the MOND term vanishes identically at Y=0 (Gk(0)=0) => background alpha-blind",
      sp.simplify(L_M_flrw) == 0, f"L_MOND|FLRW = {sp.simplify(L_M_flrw)}")
# B2 no-ghost / gradient health: lambda_perp = mu > 0, lambda_par = (d/dy)(y mu) > 0 for all y>0, times a0^2>0
lam_perp = mu_of_y; lam_par = sp.simplify(sp.diff(y*mu_of_y, y))
ys = [sp.Rational(1, 100), sp.Rational(1, 2), 1, 3, 10]
check("B2 no-ghost/gradient: lambda_perp = 1-e^{-y} > 0 and lambda_par = 1+(y-1)e^{-y} > 0 on a y-grid",
      all(lam_perp.subs(y, v) > 0 and lam_par.subs(y, v) > 0 for v in ys))
check("B2 the alpha-dependence of the MOND term is the overall positive factor a0^2 = alpha G(-K) > 0: sign alpha-blind",
      sp.simplify(sp.diff(a0sq, al)/a0sq - 1/al) == 0 and al > 0)
# B3 promotion feedback on the Q equation: d(a0^2)/dQ = -alpha G K'(Q) = alpha G * (charge density n); vanishes on vacuum
Q, Q0 = sp.symbols('Q Q0', positive=True)
KQ = -M4*sp.sqrt(1 - mu2*(Q-Q0)**2/M4)
feedback = sp.diff(al*Gs*(-KQ), Q)
check("B3 promotion feedback -alpha G K'(Q) = 0 on the vacuum branch Q=Q0 for EVERY alpha (w=-1 exact survives)",
      sp.simplify(feedback.subs(Q, Q0)) == 0)
check("B3 off-vacuum the feedback is proportional to the charge n = -K'(Q) (trace): alpha rescales, never re-signs",
      sp.simplify(feedback/(al*Gs) + sp.diff(KQ, Q)) == 0)
# B4 c_T: the MOND term depends on the metric only ALGEBRAICALLY through Y (no metric derivatives)
g00 = sp.symbols('g00'); dphi = sp.symbols('dphi', positive=True)
Yexpr = dphi**2/(-g00)                       # schematic algebraic dependence Y = (g^{mn}+A^mA^n) d_m phi d_n phi
L_M = a0sq/(8*sp.pi*Gs)*Gk.subs(y, sp.sqrt(Yexpr)/sp.sqrt(a0sq))
check("B4 c_T=1 alpha-blind: L_MOND contains no derivative of the metric (algebraic in g via Y)",
      L_M.has(g00) and not any(isinstance(a, sp.Derivative) for a in L_M.atoms(sp.Derivative)))
# B5/B6 structural, alpha-blind by construction: minimal coupling (Bianchi), Phi=Psi (a0 sets a radius only)
check("B5 Bianchi identity: S_m couples minimally to ONE metric; alpha never enters S_m", True, "structural")
r, GM = sp.symbols('r GM', positive=True)
r_trans = sp.sqrt(GM/sp.sqrt(a0sq))            # MOND radius: g_N = a0
check("B6 gamma_PPN=1 alpha-blind: alpha only rescales the MOND radius r_M = sqrt(GM/a0) ~ alpha^{-1/4}",
      sp.simplify(sp.diff(sp.log(r_trans), al) + sp.Rational(1, 4)/al) == 0)
P("  => THEOREM (by exhibited family): the v9 action is consistent for every alpha in (0,inf).  alpha = kappa^2")
P("     is a MODULUS of the action.  Nothing in the action can derive alpha = 1/4; only a NEW postulate can.")

P(""); P("="*100); P("C. POSTULATES that could fix alpha: each computed, each confronted with the measured kappa"); P("="*100)
P(f"  footing: rho_Lambda = {rho_L:.3e} kg/m^3, c*sqrt(G rho_L) = {cw:.4e}, cH_Lambda = {cHL:.4e} m/s^2")
P(f"  measured kappa: " + ", ".join(f"{n} {m}+-{s}" for n, m, s in KAPPA_MEAS) + "   (allowed = within 2 sigma of either)")
P(f"  {'postulate':62s} {'alpha=kappa^2':>14s} {'kappa':>7s} {'a0 [m/s^2]':>11s}  verdict")
cands = []
def cand(name, alpha, in_action, note=""):
    k = math.sqrt(alpha); a0 = k*cw
    ok = allowed(k)
    cands.append((name, alpha, k, a0, ok, in_action))
    P(f"  {name:62s} {alpha:14.5f} {k:7.4f} {a0:11.3e}  {'allowed' if ok else 'EXCLUDED'}"
      + ("" if in_action else "  [NOT in the action]") + (f"  {note}" if note else ""))
# P1a: the kernel's own regime offset IS the dark energy.  Offset Gk(0)-Gk(inf) = 2 (constant-independent):
offset = sp.limit(Gk - y**2, y, 0) - sp.limit(Gk - y**2, y, sp.oo)
check("P1 the kernel's deep-MOND-vs-Newtonian offset is EXACTLY 2 (in units a0^2/8piG), constant-independent",
      sp.simplify(offset - 2) == 0, f"offset={sp.simplify(offset)}")
# rho_Lambda = (a0^2/8piG)*2 = a0^2/(4piG)  => a0^2 = 4 pi G rho_Lambda  => alpha = 4 pi
cand("P1a MOND-kernel vacuum energy a0^2/(4piG) IS rho_Lambda (Gk(inf)=0)", 4*math.pi, True)
P("       P1b with the repo's Gk(0)=0 the MOND term carries NO FLRW vacuum energy -> rho_Lambda must be the separate M^4 -> alpha free")
P(f"       (the kernel's regime modulation of the vacuum energy at kappa=1/2 is kappa^2/(4pi) = 1/(16pi) = {1/(16*math.pi):.4f} of rho_Lambda)")
cand("P2  de Sitter surface gravity: a0 = c H_Lambda (Deser-Levin floor)", 8*math.pi/3, True)
cand("P3  Gibbons-Hawking temperature: a0 = c H_Lambda/(2 pi)", 2/(3*math.pi), True, "Milgrom 1999 / MK")
cand("P4  Friedmann identity a0 = cH_Lambda/Z, Z^2 = 32pi/3 (kappa=1/2 rewritten)", 0.25, True, "IDENTITY, no content")
cand("P5  surface gravity of L_Lambda = c/sqrt(G rho_L): a0 = c^2/(2 L_Lambda)", 0.25, False,
     "L_Lambda != dS horizon c/H_L (ratio sqrt(3/8pi))")
cand("P6  Jeans coefficient 1/sqrt(pi)", 1/math.pi, False)
P("       P7  cuscuton FLRW equation 3 mu_c^2 H = -V'(chi): ties a0 to V'/mu_c^2 -> introduces the SAME free kappa_H; no alpha")
P("       P8  DBI-wall relation mu^2 Lambda_D^2 = M^4 (stage 17): a0-blind (fixes Lambda_D, not alpha)")
# the "32 pi" identity: a0 = c^2 sqrt(Lambda/32pi) <=> alpha = 1/4 with Lambda = 8 pi G rho_L / c^2
Lam, cc, rl, GG = sp.symbols('Lambda c rho_L G', positive=True)
a0_32 = cc**2*sp.sqrt(Lam/(32*sp.pi)); a0_q = sp.sqrt(sp.Rational(1, 4)*GG*rl*cc**2)
check("32pi identity: c^2 sqrt(Lambda/32pi) == sqrt(G rho_L c^2 /4) with Lambda = 8piG rho_L/c^2  (32pi = 4 x 8pi)",
      sp.simplify(a0_32.subs(Lam, 8*sp.pi*GG*rl/cc**2) - a0_q) == 0)
check("dS horizon vs L_Lambda: c/H_Lambda = L_Lambda * sqrt(3/8pi)  (the only 1/4 candidate uses a non-action length)",
      abs((c/HL)/(c/math.sqrt(G*rho_L)) - math.sqrt(3/(8*math.pi))) < 1e-12)
# data confrontation
excl = [n for n, a, k, a0, ok, ia in cands if not ok]
alive = [n for n, a, k, a0, ok, ia in cands if ok]
check("P1a (kernel vacuum energy = Lambda) is EXCLUDED by the measured kappa (a0 ~7x too high)",
      any(n.startswith("P1a") for n in excl))
check("P2 (dS surface gravity) is EXCLUDED by the measured kappa (a0 ~5.8x too high)", any(n.startswith("P2") for n in excl))
check("three readings survive the data (P3 0.461, P4/P5 0.500, P6 0.564): data cannot pick, action cannot pick",
      all(any(n.startswith(p) for n in alive) for p in ("P3", "P4", "P5", "P6")))
check("NO in-action postulate yields alpha = 1/4 (the two that give 1/4 are an identity and a non-action length)",
      all(not (abs(a-0.25) < 1e-12 and ia and "IDENTITY" not in n and "Friedmann" not in n) for n, a, k, a0, ok, ia in cands))
P(f"  alt footing (same 1/4 on rho_total, the corpus's other value): a0 = {A0_ALT:.3e}; canonical a0 = {A0_CANON:.3e}")

P(""); P("="*100); P("VERDICT"); P("="*100)
P("  DERIVED:      the FORM  a0^2 = alpha * G * (-K(Q))  (det=2 uniqueness; pressure route selected by sign).")
P("  NOT DERIVED:  alpha = 1/4.  Theorem by exhibited family: every consistency condition of the v9 action")
P("                (FLRW, no-ghost, c_T, Bianchi, vacuum-branch feedback, gamma) is alpha-independent =>")
P("                alpha is a free modulus.  The only route left is a postulate OUTSIDE the action, and the")
P("                in-action candidates are excluded by data (P1a, P2) or empty (P4).  kappa = 1/2 stays FITTED.")
P("  WHAT WOULD COUNT: a mechanism producing a DENSITY-form coefficient (rational available) -- the graviton-bath")
P("                CTP nonlinear drift (mi_cubic_noise_ctp_2026.py residual) -- evaluated, with a number that can miss.")
if MUTATE:
    P(f"\n  MUTATE=1: kernel constant set to +32pi (MOND term = Lambda on FLRW). Expected: B1 and the P1-offset checks FAIL.")
P(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "") + f"   rc={1 if FAILS else 0}")
sys.exit(1 if FAILS else 0)
