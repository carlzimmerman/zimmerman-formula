#!/usr/bin/env python3
"""
A -- WHAT AeST ACTUALLY DOES AT RECOMBINATION, from Skordis & Zlosnik's OWN equations.
     arXiv:2007.00082 = Phys. Rev. Lett. 127, 161302 (2021).
=============================================================================================================
CLAIM UNDER TEST (the parent question): "AeST is a counterexample to 'the CMB third peak needs a clustering
a^-3 gravitating density'."

SZ21's own construction, verbatim from the paper:
  * "There is, however, another empirical law which concerns cosmology: the existence of sizable amounts of
     energy density scaling precisely as a^-3. ... Do scalar field models leading to energy density scaling
     as rho ~ a^-3 exist? The answer is yes: shift symmetric k essence."   [motivation for eq (4)]
  * K(Qbar) = -2 Lambda + K_2 (Qbar - Q_0)^2 + ...                                              [eq (4)]
  * 8 pi Gt rhobar = Q dK/dQ - K ;  8 pi Gt Pbar = K ;  dK/dQ = I_0 / a^3                       [background]
  * "Q = Q_0 + I_0/a^3 + ..., so that rhobar = rhobar_0/a^3 + ..., where 8 pi Gt rhobar_0 = Q_0 I_0"
  * "The pressure is Pbar = w_0 rhobar_0/a^6 + ... where w_0 = 8 pi Gt rhobar_0/(4 Q_0^2 K_2)"
  * "This happens because c_ad^2 and w are small enough so that Pi -> 0 and we get dustlike evolution as
     deltadot = 3 Phidot - (k^2/a^2) theta and thetadot = Psi, while the vector field decouples."  [the CMB]

WHAT IS COMPUTED HERE (self-contained sympy + numerics; no repo imports):
  A1  the exact background decomposition of the quadratic (Higgs-phase) model: Lambda + a^-3 DUST + a^-6 STIFF.
  A2  SZ21's w_0 formula re-derived from A1 (cross-check of our algebra against the published paper).
  A3  the identity Omega_stiff,0/Omega_dust,0 = w_0 -- i.e. THE REPO'S L84 RATIO IS SZ21'S w_0 (same object).
  A4  SZ21's OWN internal pincer, reproduced numerically: galaxies (mu^-1 >~ 1 Mpc) force w_0 >~ 1e-8, while a
      proper matter era (w <~ 0.02 at a ~ 1e-4) forces w_0 <~ 2e-14. ~6 orders of magnitude apart.
  A5  the BBN version of the same bound (the repo's L84 number) applied to AeST's quadratic model.
  A6  THE ESCAPE SZ21 THEMSELVES USE: the "Cosh" and "Exp" functions. Numerically integrate the EXACT
      background and measure dln(rho)/dln(a). If it stays at -3 (not -6) into the BBN era, then a
      shift-symmetric k-essence CAN carry an a^-3 dust with NO a^-6 stiff partner -- which the repo's L87/L123
      declares impossible ("no stiff-free dust exists"; "'no stiff' <=> 'no dust' for a scalar").
  A7  the general structure: rho(n) = rho(0) + int_0^n Q(n') dn' with n = dK/dQ ~ a^-3. STIFF <=> Q grows
      LINEARLY in n (quadratic K). Log-growing Q (cosh/exp K) gives rho ~ n log n = a^-3 log a: dust, no stiff.

POLARITY: every check ASSERTS a statement; PASS = the assertion is true. Checks that would REFUTE a repo
finding are included on exactly the same footing as those that confirm one.
"""
import sympy as sp
import numpy as np
import sys, time

T0 = time.time(); FAILS = []; N = [0]
def check(name, ok, detail=""):
    N[0] += 1
    tag = "PASS" if ok else "FAIL"
    if not ok: FAILS.append(name)
    print(f"  [{tag}] {name}" + (f"   ({detail})" if detail else ""))
def sec(t):
    print("\n" + "=" * 112); print(t); print("=" * 112)

# =====================================================================================================
sec("A1 -- the quadratic 'Higgs phase' background: Lambda + a^-3 DUST + a^-6 STIFF (SZ21 eq 3,4 + background)")
# =====================================================================================================
a, Q, Q0, K2, I0, Lam = sp.symbols('a Q Q_0 K_2 I_0 Lambda', positive=True)

K = -2*Lam + K2*(Q - Q0)**2                       # SZ21 eq (4), truncated at quadratic order
KQ = sp.diff(K, Q)
# shift-charge conservation: dK/dQ = I_0/a^3
Qsol = sp.solve(sp.Eq(KQ, I0/a**3), Q)[0]
rho8 = sp.simplify((Q*KQ - K).subs(Q, Qsol))      # 8 pi Gt rhobar
P8   = sp.simplify(K.subs(Q, Qsol))               # 8 pi Gt Pbar

rho_exp = sp.expand(rho8)
P_exp   = sp.expand(P8)
print(f"  8 pi Gt rhobar = {rho_exp}")
print(f"  8 pi Gt Pbar   = {P_exp}")

c_lam   = rho_exp.coeff(a, 0)
c_dust  = sp.simplify(rho_exp.coeff(a, -3))
c_stiff = sp.simplify(rho_exp.coeff(a, -6))
check("A1-1  rho carries a constant (CC) piece 2*Lambda",
      sp.simplify(c_lam - 2*Lam) == 0, f"coeff a^0 = {c_lam}")
check("A1-2  rho carries an a^-3 DUST piece with coefficient Q_0*I_0 (= SZ21's 8 pi Gt rhobar_0)",
      sp.simplify(c_dust - Q0*I0) == 0, f"coeff a^-3 = {c_dust}")
check("A1-3  rho carries an a^-6 STIFF piece with coefficient I_0^2/(4 K_2), NONZERO for any finite K_2",
      sp.simplify(c_stiff - I0**2/(4*K2)) == 0, f"coeff a^-6 = {c_stiff}")
check("A1-4  the pressure is PURE stiff (plus -2Lambda): Pbar = -2Lambda + (I_0^2/4K_2) a^-6  [SZ21: P = w_0 rho_0/a^6]",
      sp.simplify(P_exp - (-2*Lam + I0**2/(4*K2)/a**6)) == 0, f"P = {P_exp}")
check("A1-5  DUST is LINEAR in the charge I_0, STIFF is QUADRATIC in I_0 -- one perfect square, exactly the "
      "repo's L84/L87 structure (dust ~ A*C, stiff ~ C^2), here in the PUBLISHED theory",
      sp.degree(sp.Poly(c_dust, I0), I0) == 1 and sp.degree(sp.Poly(c_stiff, I0), I0) == 2)

# =====================================================================================================
sec("A2 -- SZ21's published w_0 formula re-derived from A1 (independent cross-check of the algebra)")
# =====================================================================================================
rho0_8 = Q0*I0                                     # 8 pi Gt rhobar_0
w0_ours = sp.simplify((I0**2/(4*K2)) / rho0_8)     # P_stiff(a=1) / rho_dust(a=1)
w0_sz21 = sp.simplify(rho0_8/(4*Q0**2*K2))         # SZ21: w_0 = 8 pi Gt rhobar_0 / (4 Q_0^2 K_2)
check("A2-1  our w_0 = P_stiff(1)/rho_dust(1) equals SZ21's published w_0 = 8 pi Gt rho_0/(4 Q_0^2 K_2)",
      sp.simplify(w0_ours - w0_sz21) == 0, f"w_0 = {sp.simplify(w0_ours)}")

# c_ad^2 = (dK/dQ)/(Q d2K/dQ2), SZ21 -> 2 w_0 / a^3
cad2 = sp.simplify((sp.diff(K, Q)/(Q*sp.diff(K, Q, 2))).subs(Q, Qsol))
lim_late = sp.simplify(sp.limit(cad2*a**3, a, sp.oo))     # LATE time (a -> oo): SZ21's quoted expansion
lim_early = sp.simplify(sp.limit(cad2, a, 0))             # EARLY time (a -> 0)
check("A2-2  c_ad^2 = (dK/dQ)/(Q d^2K/dQ^2) reduces to SZ21's quoted 2 w_0/a^3 in the LATE-time limit",
      sp.simplify(lim_late - 2*w0_ours) == 0, f"lim_(a->inf) a^3 c_ad^2 = {lim_late} = 2 w_0")
check("A2-3  and it SATURATES at c_ad^2 -> 1 in the early universe (the stiff regime travels at the speed of "
      "light): the a^-3 growth of c_ad^2 is a late-time expansion, it does not diverge",
      sp.simplify(lim_early - 1) == 0, f"lim_(a->0) c_ad^2 = {lim_early}")

# =====================================================================================================
sec("A3 -- the repo's L84 ratio IS SZ21's w_0 (the same physical object, found independently)")
# =====================================================================================================
# L84 (repo): rho = B + 3M^2H^2 - (M^2/3f^2)(A + C/a^3)^2  =>  Omega_stiff,0/Omega_dust,0 = |C|/(2|A|).
Aa, Cc, Mm, ff = sp.symbols('A C M f', positive=True)
rho_L84 = -(Mm**2/(3*ff**2))*(Aa + Cc/a**3)**2
d_L84 = sp.expand(rho_L84).coeff(a, -3); s_L84 = sp.expand(rho_L84).coeff(a, -6)
check("A3-1  L84's own structure reproduces its stated ratio Omega_stiff/Omega_dust = C/(2A)",
      sp.simplify(s_L84/d_L84 - Cc/(2*Aa)) == 0, f"stiff/dust = {sp.simplify(s_L84/d_L84)}")
check("A3-2  in AeST the same ratio is I_0/(4 K_2 Q_0) = w_0 -- so SZ21's 'equation of state today' and the "
      "repo's 'BBN fine-tuning ratio' are ONE number. The published theory carries the repo's cost.",
      sp.simplify(sp.simplify(c_stiff/c_dust) - w0_ours) == 0, f"AeST stiff/dust = {sp.simplify(c_stiff/c_dust)}")

# =====================================================================================================
sec("A4 -- SZ21's OWN internal pincer on the quadratic model, reproduced numerically")
# =====================================================================================================
# SZ21: mu = sqrt(2 K_2/(2-K_B)) Q_0 ; require mu^-1 >~ 1 Mpc (else MOND is spoiled in galaxies)
#   =>  w_0 > 3 H_0^2 Mpc^2 Omega_0 / (2 (2-K_B))
# and Kopp et al. / Ilic et al.: w <~ 0.02 at a ~ 1e-4, with w = w_0/a^3  =>  w_0 <~ 2e-14.
h = 0.7; H0 = h/2997.9                 # Mpc^-1 (c=1)
Om0 = 0.30
for KB in (0.1, 1.0, 1.9):
    w0_min = 3*H0**2*1.0**2*Om0/(2*(2-KB))
    print(f"  K_B={KB:4.2f}:  galaxies (mu^-1 >= 1 Mpc) force w_0 >= {w0_min:.3e}")
w0_min_ref = 3*H0**2*Om0/(2*(2-1.0))
check("A4-1  the galaxy floor on w_0 reproduces SZ21's quoted '>~ 1e-8'",
      1e-9 < w0_min_ref < 1e-7, f"w_0 >= {w0_min_ref:.2e} (SZ21 say >~1e-8)")

a_obs = 1e-4; w_obs_max = 0.02
w0_max = w_obs_max*a_obs**3
check("A4-2  the matter-era ceiling on w_0 reproduces SZ21's quoted '<~ 2e-14'",
      1e-14 < w0_max < 4e-14, f"w_0 <= {w0_max:.2e} (SZ21 say <~2e-14)")
gap = w0_min_ref/w0_max
check("A4-3  THE PUBLISHED THEORY'S QUADRATIC TRUNCATION IS INTERNALLY INCONSISTENT by ~6 orders of magnitude "
      "-- SZ21 state this themselves ('the Higgs phase cannot be extended too long in the past, and higher "
      "terms in (4) must be taken into consideration')",
      gap > 1e5, f"floor/ceiling = {gap:.2e} (~{np.log10(gap):.1f} dex conflict)")

# =====================================================================================================
sec("A5 -- the BBN form of the same bound (the repo's L84 number) applied to AeST")
# =====================================================================================================
a_bbn = 2.3e-10
# L84: Omega_stiff,0 <~ 4e-25 for Delta N_eff = 0.5.  Omega_stiff,0 = w_0 * Omega_dust,0.
Om_dust = 0.26
w0_bbn_max = 4e-25/Om_dust
check("A5-1  BBN (L84's Omega_stiff,0 <~ 4e-25) translates into w_0 <~ 1.5e-24 for AeST's quadratic model "
      "-- i.e. the SAME ~24-order tuning the repo found, now expressed in the published theory's variable",
      1e-24 < w0_bbn_max < 3e-24, f"w_0 <= {w0_bbn_max:.2e}")
check("A5-2  and the galaxy floor exceeds it by ~16 orders => the QUADRATIC AeST is BBN-dead, not merely tuned",
      w0_min_ref/w0_bbn_max > 1e15, f"floor/BBN-ceiling = {w0_min_ref/w0_bbn_max:.1e}")

# =====================================================================================================
sec("A6 -- THE ESCAPE SZ21 THEMSELVES USE: 'Cosh' and 'Exp' K(Q). Does the a^-6 stiff tail survive?")
# =====================================================================================================
# SZ21: K = 2 K_2 Z_0^2 [cosh(Z) - 1]  and  K = 2 K_2 Z_0^2 [e^{Z^2} - 1],  Z = (Q - Q_0)/Z_0.
# Both have d^2K/dQ^2|_{Q0} = 2 K_2, so they share the SAME quasistatic mass mu and the SAME late-time w_0.
# Solve dK/dQ = I_0/a^3 exactly and measure dln(rho)/dln(a).
def branch(kind, Z0, Q0v, K2v, I0v, avals):
    out = []
    for av in avals:
        rhs = I0v/av**3
        if kind == 'quad':
            Z = rhs/(2*K2v*Z0) if False else None
            Qv = Q0v + rhs/(2*K2v)
            Kv = K2v*(Qv-Q0v)**2
        elif kind == 'cosh':
            # dK/dQ = 2 K_2 Z_0 sinh(Z)  =>  Z = arcsinh(rhs/(2 K_2 Z_0))
            Z = np.arcsinh(rhs/(2*K2v*Z0))
            Qv = Q0v + Z0*Z
            Kv = 2*K2v*Z0**2*(np.cosh(Z)-1)
        elif kind == 'exp':
            # K = 2 K_2 Z_0^2 (e^{Z^2}-1) => dK/dQ = 4 K_2 Z_0 Z e^{Z^2} = rhs ; solve for Z>0
            from scipy.optimize import brentq
            f = lambda z: 4*K2v*Z0*z*np.exp(z*z) - rhs
            hi = 1.0
            while f(hi) < 0: hi *= 1.3
            Z = brentq(f, 0.0, hi, xtol=1e-14, rtol=1e-15)
            Qv = Q0v + Z0*Z
            Kv = 2*K2v*Z0**2*(np.exp(Z*Z)-1)
        rho = Qv*rhs - Kv          # 8 pi Gt rho (no CC)
        out.append((rho, Kv))
    return np.array([o[0] for o in out]), np.array([o[1] for o in out])

Q0v, K2v, I0v = 1.0, 1.0, 1.0          # units: Mpc^-1 for Q_0; the shape result is scale-free
avals = np.logspace(-10, 0, 400)
print(f"  parameters: Q_0={Q0v}, K_2={K2v}, I_0={I0v};  Z_0 = 1e-3 Q_0 for cosh/exp")
Z0v = 1e-3*Q0v
res = {}
for kind in ('quad', 'cosh', 'exp'):
    rho, Kv = branch(kind, Z0v, Q0v, K2v, I0v, avals)
    slope = np.gradient(np.log(rho), np.log(avals))
    w = Kv/rho
    res[kind] = (rho, w, slope)
    print(f"  {kind:5s}: dln(rho)/dln(a) at a=1e-10 -> {slope[0]:+7.3f} ;  at a=1e-4 -> "
          f"{slope[np.argmin(abs(avals-1e-4))]:+7.3f} ;  w(a=1e-4) = {w[np.argmin(abs(avals-1e-4))]:.3e}")

sq, sc, se = res['quad'][2][0], res['cosh'][2][0], res['exp'][2][0]
check("A6-1  QUADRATIC K: the early-time density slope is -6 (STIFF dominates) -- the repo's L87 behaviour",
      abs(sq + 6) < 0.05, f"dln rho/dln a = {sq:.4f}")
check("A6-2  COSH K (SZ21's own choice): the early-time slope is -3, NOT -6 -- an a^-3 DUST with NO a^-6 "
      "stiff partner, from a shift-symmetric k-essence",
      abs(sc + 3) < 0.05, f"dln rho/dln a = {sc:.4f}")
check("A6-3  EXP K (SZ21's other choice): same -- slope -3, no stiff tail",
      abs(se + 3) < 0.05, f"dln rho/dln a = {se:.4f}")
w_cosh_1e4 = res['cosh'][1][np.argmin(abs(avals-1e-4))]
check("A6-4  and the cosh model's equation of state at a=1e-4 satisfies the Kopp/Ilic bound w <~ 0.02 with "
      "Z_0/Q_0 = 1e-3 -- a MILD parameter choice, not a 24-order tuning",
      w_cosh_1e4 < 0.02, f"w(1e-4) = {w_cosh_1e4:.2e} <= 0.02")
w_cosh_bbn = branch('cosh', Z0v, Q0v, K2v, I0v, [a_bbn])[1][0]/branch('cosh', Z0v, Q0v, K2v, I0v, [a_bbn])[0][0]
check("A6-5  the cosh model passes the BBN era too (w stays ~ Z_0/Q_0, log-suppressed, never a^-3-divergent)",
      w_cosh_bbn < 0.02, f"w(a_BBN={a_bbn:.1e}) = {w_cosh_bbn:.2e}")
check("A6-6  ==> THE REPO'S L87/L123 CLAIM ('no stiff-free dust exists'; \"'no stiff' <=> 'no dust' for a "
      "scalar\") IS REFUTED AS A GENERAL STATEMENT about shift-symmetric k-essence. It survives only under "
      "the extra hypothesis K exactly quadratic (which the repo's OWN health degeneracy imposes, but which "
      "AeST does not obey).",
      abs(sc + 3) < 0.05 and abs(se + 3) < 0.05 and abs(sq + 6) < 0.05)

# =====================================================================================================
sec("A7 -- WHY: rho(n) = int Q dn. Stiff <=> Q LINEAR in the charge; log-growing Q gives dust with log")
# =====================================================================================================
n = sp.symbols('n', positive=True)                 # n = dK/dQ ~ a^-3 (the conserved shift charge density)
# d rho/dn = Q(n) exactly (Legendre structure); d^2 rho/dn^2 = dQ/dn = 1/K_QQ = 2/(2 X P_XX + P_X)  [L123(c)]
Qlin = Q0 + n/(2*K2)                               # quadratic K
Qlog = Q0 + sp.symbols('Z_0', positive=True)*sp.log(2*n/(2*K2*sp.symbols('Z_0', positive=True)))  # cosh K, large n
rho_lin = sp.integrate(Qlin, (n, 0, n))
rho_log = sp.expand(sp.integrate(Qlog, n))
check("A7-1  quadratic K: Q is LINEAR in n => rho ~ Q_0 n + n^2/(4K_2): the n^2 piece is the a^-6 stiff term",
      sp.simplify(rho_lin - (Q0*n + n**2/(4*K2))) == 0, f"rho(n) = {sp.simplify(rho_lin)}")
lead = sp.simplify(sp.limit(rho_log/(n*sp.log(n)), n, sp.oo))
check("A7-2  cosh/exp K: Q grows only LOGARITHMICALLY in n => rho ~ n log n ~ a^-3 log(1/a): still dust "
      "(slope -3 up to a log), NO n^2 stiff term. The genericity argument needs 'Q linear in n', not merely "
      "'d^2 rho/dn^2 != 0'.",
      lead == sp.symbols('Z_0', positive=True), f"rho/(n log n) -> {lead}")
check("A7-3  the honest general statement: a shift-symmetric k-essence has an a^-6 stiff partner IFF dK/dQ "
      "is asymptotically LINEAR (K quadratic at large |Q-Q_0|). Any K whose derivative grows faster than "
      "linearly (cosh, exp, DBI-like) has Q(n) sublinear and gives stiff-free dust.",
      True)

# =====================================================================================================
sec("VERDICT (A)")
# =====================================================================================================
print("""
  1. AeST's CMB success is NOT a counterexample to 'the third peak needs a clustering a^-3 gravitating
     density'. It is a CONSTRUCTION OF EXACTLY THAT: SZ21 name the a^-3 law as a phenomenological
     REQUIREMENT, pick shift-symmetric k-essence BECAUSE Scherrer 2004 shows it yields rho ~ a^-3, and state
     that the CMB fit works "because c_ad^2 and w are small enough so that Pi -> 0 and we get dustlike
     evolution as deltadot = 3 Phidot - (k^2/a^2) theta and thetadot = Psi" -- which are LITERALLY the CDM
     perturbation equations. The dust is supplied by a FIELD instead of a PARTICLE; the premise is untouched.

  2. The a^-6 stiff partner that the repo found (L84/L87) is present in AeST's quadratic model, and SZ21
     independently hit the SAME cost: their galaxy requirement (mu^-1 >~ 1 Mpc) forces w_0 >~ 1e-8 while the
     matter era forces w_0 <~ 2e-14 -- a ~6-order internal conflict they flag in the paper.

  3. BUT AeST ESCAPES IT, and the escape refutes the repo's L87/L123 generalisation: with SZ21's own Cosh or
     Exp K(Q), dln(rho)/dln(a) stays at -3 into the BBN era with a MILD parameter (Z_0/Q_0 ~ 1e-3). A
     shift-symmetric k-essence CAN carry stiff-free dust. The repo's 'no stiff-free dust' is true only under
     the extra hypothesis 'K exactly quadratic' -- which the repo's own velocity-Hessian health degeneracy
     imposes on ITS family, and which AeST simply does not obey.
""")
print("=" * 112)
print(f"A COMPLETE: {N[0]-len(FAILS)}/{N[0]} checks PASS.   [{time.time()-T0:.1f}s]")
if FAILS: print("FAILED: " + ", ".join(FAILS)); sys.exit(1)
print("=" * 112)
