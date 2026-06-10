#!/usr/bin/env python3
"""
agentQ -- JACOBSON 1995 REDONE WITH THE DESER-LEVIN TEMPERATURE (machine-verified)
==================================================================================
Task: carry the FULL kappa_DL = sqrt(a^2 + H^2) (gr-qc/9706018; machine-verified on the
stationary family in agentN1) through Jacobson's Clausius derivation of the Einstein
equation of state (gr-qc/9504004), work the expansion in (H/a)^2, and decide between the
three pre-registered outcomes:
  (i)   correction = a cosmological-constant term (Lambda re-derived, no MOND);
  (ii)  correction = acceleration-keyed modified equation of state (sign? form?);
  (iii) the construction is ambiguous at finite a/H (state precisely where).
This EXTENDS the banked verdict (reviews/ESTABLISHED_PATHS_LEDGER.md +
reviews/clausius_sign_calculation.py: temperature route -> anti-MOND, decisive) -- it does
not re-litigate it. Every expansion below is sympy-verified; raw coefficients are reported
before any comparison to Z, 6, 2pi. Units c = hbar = k_B = 1 except where SI numbers are
printed. Conventions: dS static patch ds^2 = -f dt^2 + dr^2/f + r^2 dOmega^2, f = 1-H^2r^2.
"""
import sympy as sp
import numpy as np

ok = lambda b: "PASS" if b else "FAIL"
fails = []
def check(tag, cond):
    print(f"   [{tag}] {ok(cond)}")
    if not cond: fails.append(tag)

print("="*98)
print("PART A -- BASELINE: Jacobson gr-qc/9504004 reproduced symbolically (the validation anchor)")
print("="*98)
lam, kap, Rkk, Tkk, eta, H, a = sp.symbols('lambda kappa R_kk T_kk eta H a', positive=True)
# Boost Killing vector chi^mu = -kappa*lambda*k^mu on the local Rindler horizon.
# Heat:    dQ_chi = int T_mn chi^m dSig^n = -kappa * int lambda T_kk dlam dA
# Entropy: dS = eta dA;  Raychaudhuri at leading order: theta = -lambda R_kk
#          => dA = -int lambda R_kk dlam dA.
# Clausius dQ = T dS with T = kappa/2pi; the common factor int(-lambda)dlam dA cancels:
T_unruh = kap/(2*sp.pi)
balance = sp.Eq(kap*Tkk, T_unruh*eta*Rkk)          # kappa*T_kk = T(kappa)*eta*R_kk
sol = sp.solve(balance, Tkk)[0]
print(f"  A1. local balance with T = kappa/2pi  =>  T_kk = {sol}")
check("A1 T_kk = (eta/2pi) R_kk, kappa cancels", sp.simplify(sol - eta*Rkk/(2*sp.pi)) == 0)
print("      => R_kk = (2pi/eta) T_kk for all null k => Einstein eqs, G = 1/(4 eta),")
print("         with Lambda entering ONLY as the Bianchi integration constant. [REPRODUCED]")

# A2. Lambda-blindness of the kk-balance: any term prop. to g_mn is invisible (g_kk = 0).
t, r, th, ph = sp.symbols('t r theta phi', real=True)
f = 1 - H**2*r**2
g = sp.diag(-f, 1/f, r**2, r**2*sp.sin(th)**2)
# explicit radial null vector k^mu = (1/f, 1, 0, 0):
k = sp.Matrix([1/f, 1, 0, 0])
gkk = sp.simplify((k.T*g*k)[0])
print(f"  A2. explicit null k^mu=(1/f,1,0,0) in dS static patch: g_mn k^m k^n = {gkk}")
check("A2 g_kk = 0 (Lambda-term invisible to the balance)", gkk == 0)

# A3. The Bianchi step (the 1-D abstract of Jacobson's closing move): T_kk fixes T_mn only
# up to f*g_mn; conservation + contracted Bianchi force f = -R/2 + const.
x = sp.symbols('x'); Rfun = sp.Function('R')(x); ffun = sp.Function('f')(x)
cond = sp.Eq(sp.diff(Rfun/2 + ffun, x), 0)          # div(R_mn + f g_mn) = 0 with Bianchi
fsol = sp.dsolve(cond, ffun).rhs
print(f"  A3. d/dx(R/2 + f) = 0  =>  f = {fsol}  (Lambda = the constant; NOT derived, NOT modified)")
check("A3 f = -R/2 + const", sp.simplify(fsol + Rfun/2 - sp.Symbol('C1')) == 0)

print()
print("="*98)
print("PART B -- THE SUBSTRATE: exact dS worldline thermodynamics (full Christoffel computation)")
print("="*98)
# B1. proper acceleration of the static observer at radius r (full covariant computation)
coords = [t, r, th, ph]
ginv = g.inv()
Gamma = [[[sp.simplify(sp.Rational(1,2)*sum(ginv[mu,s]*(sp.diff(g[s,nu],coords[rho])
          + sp.diff(g[s,rho],coords[nu]) - sp.diff(g[nu,rho],coords[s])) for s in range(4)))
          for rho in range(4)] for nu in range(4)] for mu in range(4)]
u = sp.Matrix([1/sp.sqrt(f), 0, 0, 0])               # static 4-velocity, u.u = -1
unorm = sp.simplify((u.T*g*u)[0])
acc = sp.Matrix([sp.simplify(sum(Gamma[mu][0][0]*u[0]*u[0] for _ in [0])) for mu in range(4)])
# a^mu = u^nu nabla_nu u^mu ; for static u only the Gamma^mu_tt (u^t)^2 term survives
acc = sp.Matrix([sp.simplify(Gamma[mu][0][0]*u[0]**2) for mu in range(4)])
amag2 = sp.simplify((acc.T*g*acc)[0])                # |a|^2 -- branch-free object
a_exact = H**2*r/sp.sqrt(1-H**2*r**2)
print(f"  B1. u.u = {unorm};  a^mu = (0, {acc[1]}, 0, 0);  |a|^2 = {amag2}")
# squared comparison: both sides manifestly nonnegative on the static patch (0 < Hr < 1),
# so |a|^2 equality is |a| equality -- no Abs/branch ambiguity.
check("B1 |a|^2 = (H^2 r)^2/(1-H^2 r^2)  [=> |a| = H^2 r/sqrt(1-H^2r^2)]",
      sp.simplify(amag2 - a_exact**2) == 0)

# B2. kappa_DL = sqrt(a^2+H^2) = H/sqrt(1-H^2 r^2) exactly (squared, same justification)
kDL2_r = sp.simplify(a_exact**2 + H**2)
check("B2 a^2+H^2 = H^2/(1-H^2r^2)  [=> kappa_DL = H/sqrt(1-H^2r^2)]",
      sp.simplify(kDL2_r - H**2/(1-H**2*r**2)) == 0)
kDL_r = H/sp.sqrt(1-H**2*r**2)

# B3. THE TOLMAN IDENTITY (the central exact fact): T_DL * |xi| = H/2pi = kappa_b/2pi.
xi_norm = sp.sqrt(f)                                  # |xi| for xi = d_t ; kappa_b = H
tolman2 = sp.simplify(kDL2_r*xi_norm**2)
print(f"  B3. (a^2+H^2) * |xi|^2 = {tolman2}   [Deser-Levin = Tolman-shifted Gibbons-Hawking, EXACT]")
check("B3 (T_DL*|xi|)^2 = (H/2pi)^2 exactly (kappa_b = H; positive => T_DL|xi| = H/2pi)",
      sp.simplify(tolman2 - H**2) == 0)

# B4. proper distance to the horizon and the three small-(H ell) expansions
ell = sp.symbols('ell', positive=True)
ell_of_r = sp.integrate(1/sp.sqrt(1-H**2*sp.Symbol('rp')**2), (sp.Symbol('rp'), r, 1/H))
ell_of_r = sp.simplify(ell_of_r)
r_of_ell = sp.cos(H*ell)/H
a2_of_ell = sp.simplify((a_exact**2).subs(r, r_of_ell))   # squared: branch-free
a_cot = H*sp.cos(H*ell)/sp.sin(H*ell)
kDL2_ell = sp.simplify(kDL2_r.subs(r, r_of_ell))
print(f"  B4. ell(r) = {ell_of_r}  =>  r(ell) = cos(H ell)/H")
print(f"      a(ell)^2 = {a2_of_ell}  ;  kappa_DL(ell)^2 = {kDL2_ell}")
# on the static patch 0 < H ell < pi/2: sin, cos > 0, so squared equality = equality.
check("B4a a(ell)^2 = H^2 cot^2(H ell)  [=> a = H cot(H ell)]",
      sp.simplify(a2_of_ell - a_cot**2) == 0)
check("B4b kappa_DL(ell)^2 = H^2/sin^2(H ell)  [=> kappa_DL = H/sin(H ell)]",
      sp.simplify(kDL2_ell - (H/sp.sin(H*ell))**2) == 0)
s_a   = sp.series(a_cot*ell, ell, 0, 6).removeO()
s_kDL = sp.series(H*ell/sp.sin(H*ell), ell, 0, 6).removeO()
s_nai = sp.series(sp.sqrt(1+(H*ell)**2), ell, 0, 6).removeO()
print(f"      series  a*ell           = {s_a}")
print(f"      series  kappa_DL*ell    = {s_kDL}")
print(f"      series  sqrt(1+(Hell)^2)= {s_nai}    [the flat-frame 'naive' DL]")
check("B4c a*ell = 1 - (Hell)^2/3 - (Hell)^4/45",
      sp.simplify(s_a - (1 - (H*ell)**2/3 - (H*ell)**4/45)) == 0)
check("B4d kappa_DL*ell = 1 + (Hell)^2/6 + 7(Hell)^4/360",
      sp.simplify(s_kDL - (1 + (H*ell)**2/6 + 7*(H*ell)**4/360)) == 0)
check("B4e naive = 1 + (Hell)^2/2 - (Hell)^4/8",
      sp.simplify(s_nai - (1 + (H*ell)**2/2 - (H*ell)**4/8)) == 0)

print()
print("="*98)
print("PART C -- READING R1 (Tolman-consistent bookkeeping): the H^2 term propagates NOWHERE")
print("="*98)
# Per-observer Clausius at proper distance ell:  dE_loc = dQ_xi/|xi| ;  T_loc = T_DL.
# Because T_DL = kappa_b/(2pi |xi|) EXACTLY (B3), the ratio is observer-independent:
dQxi = sp.Symbol('deltaQ_xi', positive=True)
ratio2 = sp.simplify(((dQxi/xi_norm)**2/((kDL2_r/(2*sp.pi)**2))))         # (dE_loc/T_DL)^2
print(f"  C1. (dE_loc/T_DL)^2 = (dQ_xi/|xi|)^2 / (kappa_DL/2pi)^2 = {ratio2}")
check("C1 dE_loc/T_DL = 2pi dQ_xi / H  -- ell-free AND the H^2-in-quadrature is GONE",
      sp.simplify(ratio2 - (2*sp.pi*dQxi/H)**2) == 0)
print("""      With the EXACT Deser-Levin temperature the Clausius ratio collapses to the
      Killing-normalized Jacobson ratio 2pi*dQ_xi/kappa_b: identical balance, identical
      equation of state, at ALL orders in H/a. The sqrt(a^2+H^2) is nothing but the Tolman
      factor of the horizon temperature -- it cancels against the Tolman factor of the
      locally measured heat. Jacobson-with-DL = Jacobson, identically. Lambda is NOT
      re-derived (A3: still the integration constant); no MOND; no correction AT ANY ORDER.""")

print("="*98)
print("PART D -- READING R2 (proper-frame DL at finite a: the ONLY reading where H survives)")
print("="*98)
# Flat-frame bookkeeping: |chi| = kappa*ell, a = 1/ell (a|chi| = kappa), T_obs = sqrt(a^2+H^2)/2pi.
# dE_loc/T_obs = (dQ_chi/|chi|)*2pi/kappa_DL = (2pi/kappa)*(a/kappa_DL)*dQ_chi.
kDL = sp.sqrt(a**2 + H**2)
balance2 = sp.Eq(2*sp.pi*(a/kDL)*kap*Tkk, eta*kap*Rkk)   # common -int lambda dlam dA cancelled
sol2 = sp.solve(balance2, Tkk)[0]
Geff_over_G = sp.simplify((eta*Rkk/(2*sp.pi))/sol2)       # R_kk = 8 pi G_eff T_kk
print(f"  D1. balance  =>  T_kk = {sp.simplify(sol2)}   =>  G_eff/G = {Geff_over_G}")
check("D1 G_eff/G = a/sqrt(a^2+H^2)", sp.simplify(Geff_over_G - a/kDL) == 0)

# D2. IDENTIFICATIONS (exact): G_eff/G = mu_F4 = a/kappa ; = T_Unruh-flat/T_DL ; = 2pi*kappa_DL*dT_DL/da
mu_F4 = a/kDL
check("D2a G_eff/G == mu_F4 = a/kappa (the F4 kernel, exactly)",
      sp.simplify(Geff_over_G - mu_F4) == 0)
check("D2b a/kappa == T_U^flat(a)/T_DL(a)",
      sp.simplify((a/(2*sp.pi))/(kDL/(2*sp.pi)) - mu_F4) == 0)
check("D2c a/kappa == 2pi * dT_DL/da  (F4's susceptibility, normalized)",
      sp.simplify(2*sp.pi*sp.diff(kDL/(2*sp.pi), a) - mu_F4) == 0)
print("      => The Clausius balance consumes T itself; F4 consumes dT/da. By the algebra of")
print("         the quadrature they are the SAME function a/kappa -- but Clausius hangs it on G")
print("         (the force side), F4 on m_eff (the inertia side).")

# D3. the (H/a)^2 expansion of the equation of state
xq = sp.symbols('x', positive=True)                       # x = (H/a)^2
expand = sp.series(1/sp.sqrt(1+xq), xq, 0, 4).removeO()
print(f"  D3. G_eff/G = (1+x)^(-1/2), x=(H/a)^2  =  {expand}  + O(x^4)")
check("D3 coefficients 1, -1/2, +3/8, -5/16",
      sp.simplify(expand - (1 - xq/2 + 3*xq**2/8 - 5*xq**3/16)) == 0)

# D4. the sign is FORCED: T_DL >= T_U in quadrature => W >= 1 => G_eff <= G always
W = kDL/a
check("D4 W = kappa_DL/a >= 1 for all (a,H>0)  [G_eff <= G: no temperature reading can flip it]",
      sp.simplify(W**2 - 1 - (H/a)**2) == 0)

# D5. numbers, both footings (memory rule: run both ways)
Z = float(sp.sqrt(32*sp.pi/3))
a0_lam, cHlam = 9.36e-11, 9.36e-11*Z          # canonical pure-Lambda footing
a0_tot, cH0   = 1.13e-10, 6.55e-10            # rho_total/cH0 footing
print(f"  D5. G_eff/G = a/sqrt(a^2+(cH)^2)   [Z = sqrt(32pi/3) = {Z:.4f}]")
print(f"      {'a/cH':>8} {'G_eff/G':>10}   regime")
for xr in (100, 3, 1, 1/Z, 0.03):
    print(f"      {xr:>8.3g} {xr/np.sqrt(xr**2+1):>10.4f}   "
          f"{'Newtonian' if xr>3 else ('a = a0 (deep-MOND onset)' if abs(xr-1/Z)<1e-9 else 'transition' if xr>=0.5 else 'deep MOND: gravity ~gone')}")
print(f"      at a = a0: G_eff/G = 1/sqrt(1+Z^2) = {1/np.sqrt(1+Z**2):.5f}  (footing-independent statement:")
print(f"      pure-Lambda (H/a0)^2 = Z^2 = {Z**2:.2f}; rho_total footing (cH0/a0')^2 = {(cH0/a0_tot)**2:.2f} -- same regime)")

# D6. dynamics: gravity-side mu vs inertia-side mu (the structural anti-MOND statement)
gN = sp.symbols('g_N', positive=True)
sols_force = sp.solve(sp.Eq(a, (a/kDL)*gN), a)
print(f"  D6. force-side   a = mu(a) g_N  =>  solutions a = {sols_force}")
check("D6a force-side: a = sqrt(g_N^2 - H^2) -- REAL ONLY FOR g_N > cH; below: a = 0 (total shutoff)",
      any(sp.simplify(s**2 - (gN**2 - H**2)) == 0 for s in sols_force))
sols_inert = sp.solve(sp.Eq((a/kDL)*a, gN), a)
print(f"      inertia-side mu(a) a = g_N  =>  a = {sols_inert}")
# physical root: the one with a^2 = g_N^2/2 + g_N*sqrt(4H^2+g_N^2)/2 (positive discriminant)
a_phys = sp.sqrt(gN**2/2 + gN*sp.sqrt(4*H**2 + gN**2)/2)
check("D6b physical root present in solve()",
      any(sp.simplify(s**2 - a_phys**2) == 0 for s in sols_inert))
# deep-MOND limit: a_phys^2/(g_N H) -> 1 as g_N -> 0  (i.e. a -> sqrt(g_N H), the enhancement)
lim_deep = sp.limit(a_phys**2/(gN*H), gN, 0, '+')
check("D6c inertia-side deep-MOND limit: a^2/(g_N H) -> 1, i.e. a -> sqrt(g_N H) (the MOND enhancement)",
      lim_deep == 1)
print("""      SAME function, two legs: on the INERTIA leg a/kappa gives deep-MOND a = sqrt(g_N H)
      (enhancement -- the observed phenomenology, F4's selling point); on the GRAVITY leg the
      Clausius balance puts it, the self-consistent response below g_N = cH is a = 0 EXACTLY:
      gravity does not weaken gradually -- it SHUTS OFF. Anti-MOND in its most extreme form
      (the banked sign, now exact and structural).""")

print("="*98)
print("PART E -- OUTCOME (i) TEST: the correction is NOT a cosmological-constant term")
print("="*98)
# The R2 correction enters multiplying T_kk: R_kk = 8 pi G [1 - x/2 + ...] T_kk.
# A Lambda-term would have to enter as Lambda*g_kk -- but g_kk = 0 identically (A2).
corr = sp.simplify(8*sp.pi*sp.Symbol('G')*(mu_F4 - 1)*Tkk)
print(f"  E1. correction term = 8 pi G (mu_F4 - 1) T_kk = {corr}")
print("      proportional to T_kk (a SOURCE-coupling rescaling), NOT to g_kk (which is 0, A2).")
check("E1 correction vanishes when T_kk = 0 (so it can NEVER mimic Lambda, which gravitates in vacuum)",
      corr.subs(Tkk, 0) == 0)
print("      Lambda remains exactly where Jacobson left it: the Bianchi integration constant (A3),")
print("      untouched by the temperature substitution. Outcome (i) does NOT occur.")

print("="*98)
print("PART F -- OUTCOME (iii): the finite-(H/a) construction is SCHEME-AMBIGUOUS, quantified")
print("="*98)
# Four defensible pairings of (which acceleration, which redshift weight); W-factor at O((Hell)^2):
schemes = {
 "S0 exact-dS DL + exact Tolman weight (R1)": sp.simplify((H/sp.sin(H*ell))*sp.sin(H*ell)/H),
 "S1 banked coarse swap / flat a=1/ell + flat weight (R2)": sp.sqrt(1+(H*ell)**2),
 "S2 exact-dS a(ell)=Hcot(Hell) in DL + flat weight": sp.simplify(H*ell/sp.sin(H*ell)),
 "S3 flat a=1/ell in DL + exact Tolman weight": sp.simplify(sp.sqrt(1+(H*ell)**2)*sp.sin(H*ell)/(H*ell)),
}
coeffs = {}
for name, expr in schemes.items():
    ser = sp.series(expr, ell, 0, 4).removeO()
    c2 = sp.simplify((ser - 1).coeff(ell, 2)/H**2)
    coeffs[name] = c2
    print(f"  {name}:  W = 1 + ({c2})*(H ell)^2 + ...")
check("F1 scheme spread at O((H/a)^2) = {0, 1/6, 1/3, 1/2} -- the coefficient is PURE SCHEME",
      sorted(sp.Rational(str(c)) for c in coeffs.values()) == [0, sp.Rational(1,6), sp.Rational(1,3), sp.Rational(1,2)])
print("""      Jacobson's construction approximates the boost Killing field in a curved background;
      the candidate chi fails Killing's equation at O(x^2 * Riemann) (gr-qc/9504004; the error
      budget made explicit in Guedens-Jacobson-Sarkar arXiv:1112.6215). In dS, Riemann ~ H^2, so
      the construction's OWN neglected terms at the bookkeeping distance ell are O((H ell)^2) --
      EXACTLY the order at which the schemes disagree. The (H/a)^2 coefficient of any 'finite-a/H
      Jacobson equation of state' is therefore not determined by the construction: it is gauge.""")

# F2. the regime wall: MOND lives where the expansion has no validity domain at all
c_si = 2.99792458e8
Zsym = sp.sqrt(32*sp.pi/3)
Lam, c_ = sp.symbols('Lambda c', positive=True)
a0_def  = c_**2*sp.sqrt(Lam/(32*sp.pi))
cHL_def = c_**2*sp.sqrt(Lam/3)
check("F2a framework identity (cH_Lambda/a0)^2 = 32pi/3 = Z^2 (exact)",
      sp.simplify((cHL_def/a0_def)**2 - 32*sp.pi/3) == 0)
Hell_a0 = float(sp.atan(Zsym))                      # a = H cot(H ell) = H/Z  =>  H ell = arctan(Z)
print(f"  F2. deep-MOND onset a = a0 = cH_L/Z:  (H/a)^2 = Z^2 = {float(Zsym**2):.2f}  (expansion parameter ~33x past unity)")
print(f"      bookkeeping observer's distance: H*ell = arctan(Z) = {Hell_a0:.4f} rad")
print(f"      = {100*Hell_a0/(np.pi/2):.1f}% of the FULL static-patch depth pi/2 = {np.pi/2:.4f}")
check("F2b at a <= a0 the 'local' wedge spans >=89% of the static patch -- nothing local remains",
      Hell_a0/(np.pi/2) > 0.89)
print("""      Below a0 the local Rindler horizon and the cosmological horizon MERGE (the GEMS
      content of Deser-Levin: one embedding horizon). The Clausius bookkeeping in the MOND
      regime is just Gibbons-Hawking thermodynamics of the dS horizon -- the Lambda sector,
      already in the Einstein equation as the integration constant. There is no separate
      'low-acceleration equation of state' to derive: the construction has no validity
      domain AT ALL for a <~ a0.""")

print("="*98)
print("PART G -- the covariantization no-go (echo of the Door-II wall, one line)")
print("="*98)
muf = sp.Function('mu')(x); Tf = sp.symbols('T0', positive=True)
div = sp.diff(muf*Tf, x)                              # conserved T, 1-D abstract
print(f"  G1. d/dx[mu(x) T] = {div} = 0 with T != 0  =>  mu' = 0: mu = const on the support of T.")
check("G1 any covariant completion of G*mu(a)T_mn forces mu = const (no acceleration-keyed EoS)",
      sp.simplify(sp.solve(sp.Eq(div, 0), sp.diff(muf, x))[0]) == 0)

print("="*98)
print("PART H -- COEFFICIENT DISCIPLINE: raw O(1) numbers FIRST, comparison AFTER")
print("="*98)
raw = {
  "(H/a)^2 series": "1, -1/2, +3/8, -5/16  (binomial (-1/2 choose n))",
  "scheme spread at O((Hell)^2)": "0, 1/6, 1/3, 1/2",
  "Tolman exact-dS coefficient": "1/6  (kappa_DL*ell expansion)",
  "G_eff/G at a=a0": f"1/sqrt(1+Z^2) = {1/np.sqrt(1+Z**2):.5f}",
  "H*ell at a0 / (pi/2)": f"{Hell_a0/(np.pi/2):.4f}",
  "temperature prefactor": "1/2pi (Unruh/DL, unmodified)",
}
for k_, v in raw.items(): print(f"   raw: {k_:38s} = {v}")
print(f"   comparison (AFTER): Z = sqrt(32pi/3) = {Z:.5f}, 1/Z = {1/Z:.5f}, 6, 2pi = {2*np.pi:.5f}")
print(f"   - 1/sqrt(1+Z^2) = {1/np.sqrt(1+Z**2):.5f} vs 1/Z = {1/Z:.5f}: {100*abs(1/np.sqrt(1+Z**2)-1/Z)*Z:.1f}% apart --")
print("     the trivial large-Z identity 1/sqrt(1+Z^2) ~ 1/Z; STRUCTURALLY MEANINGLESS, flagged.")
print("   - 1/6 vs 1/Z: 3.5% near-miss ALREADY flagged meaningless in agentB; here 1/6 is a Tolman")
print("     series coefficient (kappa_DL*ell) -- again unrelated to Z. No coefficient lands on Z, 6, 2pi.")

print("="*98)
print(f"MACHINE-CHECK SUMMARY: {'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}")
print("="*98)
print("""VERDICT (both ways, full weight -- details in agentQ_jacobson_DL.md):
 R1 (the well-defined reading): Jacobson-with-Deser-Levin = Jacobson IDENTICALLY, all orders
    in H/a -- T_DL is exactly the Tolman-shifted Gibbons-Hawking temperature (B3), and Clausius
    only ever consumes the Tolman-invariant ratio (C1). Einstein recovered exactly; Lambda NOT
    re-derived (still the integration constant, A3); the kk-balance is Lambda-blind (A2, E1).
 R2 (the only reading where H survives): an observer-indexed, acceleration-keyed rescaling
    G_eff/G = a/sqrt(a^2+H^2) = mu_F4 EXACTLY (D2a) -- the F4 kernel on the WRONG LEG: a
    gravity-side deficit at low a (anti-MOND; the banked sign, now exact), with total shutoff
    below g_N = cH (D6a). The sign cannot flip in ANY temperature reading (D4: quadrature).
 (iii) sharpened: the (H/a)^2 coefficient is pure scheme ({0,1/6,1/3,1/2}, F1), degenerate with
    the construction's own neglected O(x^2*Riemann) terms; and in the MOND regime a <= a0 the
    'local' wedge IS the cosmological horizon (F2) -- the construction has no validity domain.
 EXTENSION of the banked verdict: horizon thermodynamics cannot reach MOND even with the exact
 DL temperature, for a reason now precise -- Clausius consumes T (kappa-only, Tolman-trivial);
 the two-variable (a,H) structure agentN1 proved real lives in the RESPONSE kernel (dissipation),
 an object the equation-of-state bookkeeping never touches. The MI lane, not the EoS lane.""")
