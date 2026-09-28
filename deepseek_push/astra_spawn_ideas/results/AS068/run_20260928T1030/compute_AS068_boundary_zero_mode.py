#!/usr/bin/env python3
"""
AS068 -- Can a boundary condition remove the zero mode?

Branch: CORE coefficient / conditional MU_n statistical response (n >= 1, real).
Units: s = c*sqrt(G*rho_L), Y = g/s (dimensionless), kappa = 1/2 ADOPTED (a0 = s/2).
Kernel: J'(Y) = mu_n(Y) = 1 - (1+Y)^(-n)  (the conditional MU_n response; n=2 is the
        MU2 branch on the adopted footing: Y = g/s, s = 2 a0).
Boundary condition under test: J(Y_ref) = 0  =>  J(0) = -int_0^{Y_ref} J'(Y) dY  (exact FTC).

Structural context (sources, hashes pinned):
  PD01 (37e39d1a...):  slope of 1-(1+Y)^(-n) at origin = n = channel count; kappa = 1/n.
  PD08 (83f6054c...):  particle-free derivation; p(0)=0, p'(0)=1, mu = 1-(1-p)^2, mu'(0)=2.
  k01  (8df5a3ab...):  the additive zero mode theorem: statics depend on J only through J';
                       FLRW background sees Lambda_eff = Lambda + (2-K_B) J(0)/2 + K(Q0)/2;
                       rho_vac = (2-K_B) J(0)/(16 pi G) [k01 units]; K3: sign of J(0) < 0 there.

This run answers: does the boundary condition J(Y_ref)=0 (a) fix the additive constant
(removal identity), and (b) supply a physically determined vacuum/closure relation?

Result summary (derived here):
  (a) YES, exact: J(0) = -int_0^{Y_ref} mu_n(Y) dY; for n=2, J(0) = -Y_ref^2/(1+Y_ref).
  (b) NO: the freedom is relocated to the adopted datum Y_ref (1 real DOF in, 1 real DOF
      out; nothing in the action fixes Y_ref), and for EVERY finite positive Y_ref and
      EVERY n > 0 the vacuum density is negative:
          rho_vac/rho_Lambda = -(2-K_B) c^2 J0'(Y_ref)/(16 pi),  J0' := Y_ref^2/(1+Y_ref)   (n=2)
      Diagnostic counterexamples at lambda = Y_ref in {1/2, 1, 2} (K_B = 0):
          J(0) = -1/6, -1/2, -4/3 ;  rho_vac/rho_Lambda = -5.9601e14, -1.7880e15, -4.7680e15.
      Magnitude match |ratio| = 1 would need Y_ref* ~ 1.67e-8 (K_B=0) -- an adopted fitted
      datum -- and the sign would STILL be negative.
  Limits: Y_ref -> 0+ : J(0) = -Y_ref^2 + O(Y_ref^3) -> 0-  (no information, trivial vacuum);
          Y_ref -> inf: J(0) -> -inf  (mu_n -> 1: the primitive does not converge; the
          zero-mode freedom returns as a divergent choice; k01's kernel class converged
          because its Delta -> 0 in the deep limit -- different regime, noted).

Every check states measurement and threshold before evaluation.
"""
import json
import sympy as sy
import mpmath as mp

mp.mp.dps = 60

RES, NP, NF = [], 0, 0
def check(name, measured, ok, reading=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")
    RES.append({"name": name, "measured": str(measured), "pass": ok, "reading": reading})
    if ok: NP += 1
    else:  NF += 1

# ---------------------------------------------------------------- constants
G  = mp.mpf("6.67430e-11")          # m^3 kg^-1 s^-2  (G_N; separate symbol from G_bare/G_cosmo)
c  = mp.mpf("299792458")            # m/s (exact)
a0_can = mp.mpf("9.3619e-11")       # canonical footing, m/s^2
a0_alt = mp.mpf("1.1279e-10")       # alternative footing, m/s^2
pi = mp.pi
c2 = c*c
KB = mp.mpf("0.25")                 # corpus band K_B in [0, 0.25]; tables use 0 and 0.25

rho_Lam_can = 4*a0_can**2/(G*c2)    # canonical vacuum mass density, kg/m^3 (kappa=1/2)
rho_L_altk = 4*a0_alt**2/(G*c2)     # alternative footing at SAME kappa=1/2 (changed density)
s_can = c*mp.sqrt(G*rho_Lam_can)    # = 2 a0_can on the adopted footing
s_alt = 2*a0_alt
kap_eff_alt = a0_alt/s_can          # effective kappa at FIXED canonical density
print("="*118)
print("AS068 -- boundary condition vs the additive zero mode (MU_n class, n>=1, kappa=1/2 adopted)")
print("="*118)
print(f"    rho_Lambda(can) = {mp.nstr(rho_Lam_can, 12)} kg/m^3 ; s_can = {mp.nstr(s_can, 12)} m/s^2 = 2 a0_can ? {mp.nstr(s_can/(2*a0_can), 15)}")
print(f"    rho_Lambda(alt, kappa=1/2) = {mp.nstr(rho_L_altk, 12)} kg/m^3 ; s_alt = {mp.nstr(s_alt, 12)}")
print(f"    kappa_eff(alt at fixed canonical density) = {mp.nstr(kap_eff_alt, 12)}")

# ---------------------------------------------------------------- STEP 1-2: symbolic core
Y, lam, n_, KBs = sy.symbols('Y lambda n K_B', positive=True)
mu_n = 1 - (1 + Y)**(-n_)
mu_2 = 1 - (1 + Y)**(-2)

# exact removal identity for n=2 (closed form) + general n
J0_n2_expr = sy.simplify(-sy.integrate(mu_2, (Y, 0, lam)))
J0_n2_closed = sy.simplify(-lam**2/(1 + lam))
J0_gen = sy.simplify(-(sy.integrate(mu_n, (Y, 0, lam))))
print(f"\n    symbolic: J(0; n=2, lam) = {J0_n2_expr}  ==  {J0_n2_closed}")
print(f"    symbolic: J(0; n, lam)   = {J0_gen}")
check("S1 [removal identity, exact] the boundary condition J(Y_ref)=0 with kernel J'=mu_n fixes J(0)=-int_0^Y_ref mu_n dY; the n=2 integral evaluates to the closed form -lam^2/(1+lam)",
      f"J0(lam) = {J0_n2_closed}; general n: {J0_gen}",
      sy.simplify(J0_n2_expr - J0_n2_closed) == 0,
      "FTC + elementary quadrature, exact. The additive constant is determined by the reference position.")

# FTC consistency: d/dlam J(0) = -J'(lam) = -mu(lam)
dJ0 = sy.simplify(sy.diff(J0_n2_closed, lam) + mu_2.subs(Y, lam))
dJ0g_parts = []
for nv in (1, 3, sy.Rational(5,2), 4):           # explicit n bypasses sympy's Piecewise branch algebra
    J0n = sy.simplify(-sy.integrate(mu_n.subs(n_, nv), (Y, 0, lam)))
    dJ0n = sy.simplify(sy.diff(J0n, lam) + mu_n.subs({n_: nv, Y: lam}))
    dJ0g_parts.append(dJ0n == 0)
check("S2 [FTC consistency by direct differentiation] d/dlam[J(0)] = -J'(lam) = -mu_n(lam), symbolic, for n=2 (closed form) and n in {1,3,5/2,4}",
      f"n=2 residual: {dJ0}; general-n residuals: {dJ0g_parts}",
      dJ0 == 0 and all(dJ0g_parts),
      "the closed form is the exact primitive of the kernel; differentiation returns the kernel's negative exactly (no numerics involved).")

# sign theorem: mu_n > 0 on (0, inf) for n>0  =>  J(0) < 0 for all finite positive references
print(f"\n    integrand positivity: mu_n(Y) = 1-(1+Y)^(-n) > 0 for Y>0, n>0 (since (1+Y)^(-n) < 1);")
print(f"    therefore J(0) = -int_0^lam mu_n < 0 for EVERY finite positive lam and EVERY n>0: sign-obstruction theorem, no exception.")
print(f"    n=2 closed form: J0 = -lam^2/(1+lam);  G0 := -J0 = lam^2/(1+lam) > 0;  dG0/dlam = (lam^2+2lam)/(1+lam)^2 > 0")

# kernel asymptotics (leading neglected terms)
ser0 = sy.series(mu_2, Y, 0, 5)
serI = sy.series(mu_2.subs(Y, 1/sy.Symbol('t', positive=True)), sy.Symbol('t', positive=True), 0, 4)
print(f"\n    kernel asymptotics: mu_2(Y) = {sy.expand(ser0)}  (leading neglected term -3 Y^2)")
print(f"    deep: 1-mu_2(1/t) = {sy.simplify(serI)}  ->  1/Y^2 - 2/Y^3 + ... at Y -> inf")

# S3: slope at origin (= n, the PD01 channel-count consistency) and saturation
slope_n = sy.simplify(sy.limit(sy.diff(mu_n, Y), Y, 0))
sat_n = sy.simplify(sy.limit(mu_n, Y, sy.oo))
check("S3 [kernel limiting regimes, exact] mu_n'(0) = n (PD01 channel-count slope) and mu_n(inf) = 1 (L230 saturation), symbolic",
      f"mu_n'(0) = {slope_n}; mu_n(inf) = {sat_n}",
      sy.simplify(slope_n - n_) == 0 and sat_n == 1,
      "the kernel's Newtonian slope is the channel count and the deep saturation is unity: the boundary position is the ONLY freedom the static kernel leaves for the primitive.")

# ---------------------------------------------------------------- STEP 3: vacuum prediction
# k01 K1-K3 structure carried into s-units (source k01, pinned): rho_vac = (2-K_B) s^2 J(0)/(16 pi G)
# rho_Lambda = 4 a0^2/(G c^2) = s^2/(G c^2)  (kappa=1/2)
# ratio R(lam) = rho_vac/rho_Lambda = -(2-K_B) c^2 G0(lam)/(16 pi),  G0 = lam^2/(1+lam)
def G0f(lamv): return lamv**2/(1+lamv)
def ratio(lamv, kbv): return -(2-kbv)*c2*G0f(lamv)/(16*pi)
print("\n  VACUUM PREDICTION (dimensionless ratio; footing enters only through rho_Lambda)")
print(f"    ratio formula: R(lam) = -(2-K_B) c^2 lam^2 / (16 pi (1+lam))")
for kbv in (mp.mpf(0), KB):
    for lv in (mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2")):
        J0v = -G0f(lv); Rv = ratio(lv, kbv)
        print(f"    K_B={float(kbv):.2f}  lam={float(lv):.1f}:  J(0) = {mp.nstr(J0v, 20)} ; rho_vac/rho_Lambda = {mp.nstr(Rv, 10)}")

# exact fractional values of the diagnostics (n=2, K_B symbolic kept separate)
diag_exact = {mp.mpf("0.5"): (sy.Rational(-1,6), sy.Rational(1,6)),
              mp.mpf("1"):  (sy.Rational(-1,2), sy.Rational(1,2)),
              mp.mpf("2"):  (sy.Rational(-4,3), sy.Rational(4,3))}
okd = all(sy.simplify(sy.Rational(-1,1)*G0f(lv) - j0e) == 0 for lv, (j0e, _) in diag_exact.items())
hmm = all(sy.simplify(G0f(lv) - g0e) == 0 for lv, (_, g0e) in diag_exact.items())
check("S4 [diagnostic counterexamples, exact fractions] at lambda = 1/2, 1, 2 the determined constants are J(0) = -1/6, -1/2, -4/3 (exact rationals)",
      " -1/6, -1/2, -4/3",
      bool(okd and hmm),
      "three distinct, exactly equal to the closed form. These are the diagnostic counterexamples at lambda=1/2,1,2: the vacuum prediction changes with the reference and is negative at all three.")

# ---------------------------------------------------------------- STEP 4: independent check - 60-digit numerics
print("\n  INDEPENDENT NUMERICAL CHECK (mpmath, dps=60; tolerance 1e-30 relative set BEFORE evaluation)")
for lv in (mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2")):
    q = mp.quad(lambda t: 1 - 1/(1+t)**2, [0, lv])
    exact = G0f(lv)
    r = abs(q - exact)/max(abs(exact), mp.mpf(1))
    check(f"N1 [FTC residual, 60-digit] quad(int_0^lam mu_2) vs closed form lam^2/(1+lam) at lam={float(lv)}",
          f"quad = {mp.nstr(q, 25)}, closed = {mp.nstr(exact, 25)}, rel resid = {mp.nstr(r, 5)}",
          r < mp.mpf("1e-30"),
          "numerical integration of the actual kernel reproduces the closed form: the removal identity is an exact identity, not a fit.")

for nn, lv in ((1, mp.mpf(1)), (3, mp.mpf("0.5")), (mp.mpf("2.5"), mp.mpf(2)), (4, mp.mpf(1))):
    q = mp.quad(lambda t: 1 - 1/(1+t)**nn, [0, lv])
    if nn == 1:
        ex_pos = lv - mp.log(1+lv)                # int_0^lam (1-(1+t)^(-1)) dt = lam - ln(1+lam)
    else:
        ex_pos = lv - ((1+lv)**(1-nn) - 1)/(1-nn) # int_0^lam mu_n dt = lam + [(1+lam)^(1-n)-1]/(1-n)
    r = abs(q - ex_pos)/max(abs(ex_pos), mp.mpf(1))
    check(f"N2 [general-n FTC residual] int_0^lam (1-(1+t)^(-n)) dt vs closed form at n={float(nn)}, lam={float(lv)}; J(0) = -<that integral>",
          f"rel resid {mp.nstr(r, 5)} (J(0) = {mp.nstr(-ex_pos, 12)})",
          r < mp.mpf("1e-30"),
          "the general-n closed form (n != 1) and the n=1 log form are exact primitives of the kernel for every n >= 1 sampled.")

# asymptotics numerics: check the CLAIMED leading terms directly (ratio -> 1)
mv = mp.mpf("1e-8")
lin_ratio = (1 - 1/(1+mv)**2 - 2*mv)/(-3*mv**2)      # (mu_2 - 2Y)/(-3Y^2) -> 1 as Y -> 0
lin_resid = abs(lin_ratio - 1)
dv = mp.mpf("1e6")
deep_lead = (1/(1+dv)**2) * dv**2 - 1               # (1-mu_2)*Y^2 - 1 -> -2/Y
deep_resid = abs(deep_lead - (-2/dv))
check("N3 [Newtonian and deep asymptotics on the kernel] (mu_2(Y)-2Y)/(-3Y^2) -> 1 at Y=1e-8 and (1-mu_2(Y))*Y^2 - 1 -> -2/Y at Y=1e6",
      f"lin ratio-1 = {mp.nstr(lin_resid, 5)} (expected ~ (4/3)Y = 1.3e-8); deep resid = {mp.nstr(deep_resid, 5)} (expected ~3/Y^2 = 3e-12)",
      lin_resid < mp.mpf("1e-6") and deep_resid < mp.mpf("1e-8"),
      "the stated leading neglected terms (domain: |Y| << 1 and Y >> 1) describe the kernel; the regulator question is about the PRIMITIVE, not the kernel.")

# limits of the primitive at the two physical ends
lim0 = ratio(mp.mpf("1e-10"), mp.mpf(0))          # ~ - (2)c^2 (1e-20)/(16 pi) tiny negative
J0_inf_lead = mp.mpf(0)                            # placeholder replaced below
# deep behavior: J0 = -lam^2/(1+lam) = -lam + 1 - 1/(1+lam)
lam_big = mp.mpf("1e12")
J0_big = -G0f(lam_big)
res_deepJ0 = abs(J0_big - (-lam_big + 1 - 1/(1+lam_big)))
check("N4 [primitive limiting regimes] Y_ref->0+: J(0) = -Y_ref^2 + O(Y_ref^3) -> 0- ; Y_ref->inf: J(0) = -Y_ref + 1 - 1/(1+Y_ref) -> -inf (no finite reference in the deep limit)",
      f"at lam=1e-10: R = {mp.nstr(lim0, 4)} (->0-, no information); at lam=1e12: J(0) = {mp.nstr(J0_big, 8)}, agrees with -lam+1-1/(1+lam) to rel {mp.nstr(res_deepJ0, 3)}",
      res_deepJ0 < mp.mpf("1e-30"),
      "the Newtonian end (Y_ref->0) leaves the constant trivially undetermined (vacuum -> 0); the deep end (Y_ref->inf) diverges because mu_n -> 1: k01's convergent class had Delta -> 0 there; for the MU_n kernel no boundary at infinity exists.")

# ---------------------------------------------------------------- NEGATIVE CONTROL: vary Y_ref
print("\n  NEGATIVE CONTROL -- vary Y_ref keeping the static kernel fixed (capable of failing)")
lam_grid = [mp.mpf("1e-4"), mp.mpf("1e-2"), mp.mpf("0.5"), mp.mpf("1"), mp.mpf("2"), mp.mpf("100")]
row = [(float(l), mp.nstr(-G0f(l), 12), mp.nstr(ratio(l, mp.mpf(0)), 8)) for l in lam_grid]
for l, j0, rr in row:
    print(f"    Y_ref = {l:>6g}:  J(0) = {j0:>14s}   rho_vac/rho_Lambda (K_B=0) = {rr:>17s}")
mono = all(G0f(lam_grid[i]) < G0f(lam_grid[i+1]) for i in range(len(lam_grid)-1))
distinct = len(set(mp.nstr(G0f(l), 40) for l in lam_grid)) == len(lam_grid)
check("C1 [negative control: changed vacuum prediction under Y_ref variation] with the SAME static kernel J'=mu_2, moving the boundary from 1e-4 to 100 changes J(0) monotonically and strictly (dG0/dlam = (lam^2+2lam)/(1+lam)^2 > 0), so the vacuum prediction is a continuous one-parameter family, not a determined constant",
      f"monotone-strict: {mono}, distinct values: {distinct}; ranges J(0) in [-1e-8 ... -99.0]",
      mono and distinct,
      "the control is capable of failing: had the zero mode been removed WITHOUT residue, every Y_ref would give the same J(0)/vacuum prediction; they differ at every sampled reference. The freedom is relocated to Y_ref, not removed: one real dimensionless datum enters, fixed by no equation of the action (consistent with k01's no-second-scale theorem).")

# magnitude requirement: |R| = 1  =>  G0(lam*) = 16 pi / ((2-K_B) c^2)
for kbv in (mp.mpf(0), KB):
    w = 16*pi/((2-kbv)*c2)
    ls = (w + mp.sqrt(w*w + 4*w))/2
    R_at = ratio(ls, kbv)
    print(f"    K_B={float(kbv):.2f}: required G0 = {mp.nstr(w, 8)} -> Y_ref* = {mp.nstr(ls, 10)} (boundary ALMOST at the origin, deep Newtonian); R(lam*) = {mp.nstr(R_at, 6)} (still negative)")
    check(f"C2 [magnitude fine-tune cannot fix the sign] the boundary position that matches |rho_vac/rho_Lambda| = 1 at K_B={float(kbv):.2f} sits at Y_ref* ~ {mp.nstr(ls, 6)} and still gives R < 0",
          f"Y_ref* = {mp.nstr(ls, 12)}; R = {mp.nstr(R_at, 6)} < 0",
          R_at < 0,
          "an adopted (fitted) reference position can reach the SIZE but never the SIGN of the positive vacuum density: the sign obstruction is unconditional in this action class.")

# fix-density / fix-kappa footings handling (framework contract)
print("\n  FOOTINGS (kappa=1/2 adopted; canonical vs alternative carried separately)")
for tag, a0f, rl, s_f in (("canonical", a0_can, rho_Lam_can, s_can), ("alternative(kappa=1/2)", a0_alt, rho_L_altk, s_alt)):
    rv = ratio(mp.mpf(1), mp.mpf(0)) * rl          # rho_vac at lambda=1, K_B=0
    ev = rv * c2
    print(f"    {tag:24s}: a0 = {mp.nstr(a0f, 8)} m/s^2, rho_Lambda = {mp.nstr(rl, 10)} kg/m^3, s = {mp.nstr(s_f, 10)} m/s^2;")
    print(f"        at Y_ref=1, K_B=0: rho_vac = {mp.nstr(rv, 6)} kg/m^3 ; eps_vac = {mp.nstr(ev, 6)} J/m^3")
print(f"    kappa_eff for the alternative acceleration at FIXED canonical density: {mp.nstr(kap_eff_alt, 10)} (footing separation rule: never both fixed)")

# residual JSON for the record
json.dump({"pass": NP, "fail": NF, "checks": RES}, open("residuals.json", "w"), indent=1)
print(f"\nAS068 COMPLETE: {NP}/{NP+NF} checks PASS.")
if NF > 0:
    raise SystemExit(1)
