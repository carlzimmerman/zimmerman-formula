#!/usr/bin/env python3
"""
ANGLE 2 -- THE ARROW OF TIME FROM DECLINING a0.
================================================
Tests the SPECIFIC claim in the task brief: the framework's a0 ~ sqrt(rho_DE)
DECLINING gives a FIRST-PRINCIPLES arrow of time + a LOW-ENTROPY PAST, because
high-Lambda past => small horizon => low S_dS, and Lambda declining to today =>
S_dS increasing = the 2nd law.

Primary source verbatim (Volovik, "First law of de Sitter thermodynamics",
2504.05763, eqs 4-6): S_Hubble = A/4G = (Gibbons-Hawking), A = 4 pi r_H^2,
r_H = 1/H. Gibbons-Hawking 1977 PRD 15 2738: S = A/4 (Planck units).

EVERY load-bearing step in sympy. Honest BOTH ways: does declining-Lambda SOLVE
or merely RE-POSIT the low-entropy past? Is the decline REQUIRED or OPTIONAL?
"""
import sympy as sp

print("="*78)
print("STEP 0 -- the framework anchors, symbolic")
print("="*78)
# symbols
Lam, G, c, lP, hbar, kB, Hl, t, z = sp.symbols(
    'Lambda G c l_P hbar k_B H_Lambda t z', positive=True)
Om, OL = sp.symbols('Omega_m Omega_Lambda', positive=True)
H0 = sp.symbols('H_0', positive=True)

# de Sitter radius from Lambda: R_dS = sqrt(3/Lambda)  (Lambda in 1/m^2)
R_dS = sp.sqrt(3/Lam)
# de Sitter / Lambda Hubble rate: H_Lambda = c sqrt(Lambda/3)  => c/H_Lambda = R_dS
H_Lambda_expr = c*sp.sqrt(Lam/3)
print("R_dS = sqrt(3/Lambda) =", R_dS)
print("H_Lambda = c sqrt(Lambda/3); check c/H_Lambda = R_dS:",
      sp.simplify(c/H_Lambda_expr - R_dS) == 0)

# a0 = c^2 sqrt(Lambda/32pi)
a0 = c**2*sp.sqrt(Lam/(32*sp.pi))
# also a0 = c H_Lambda / Z, Z = sqrt(32pi/3)
Z = sp.sqrt(sp.Rational(32,1)*sp.pi/3)
a0_alt = c*H_Lambda_expr/Z
print("a0 = c^2 sqrt(Lambda/32pi); a0 = cH_Lambda/Z identical:",
      sp.simplify(a0 - a0_alt) == 0)
print("   => a0 ~ sqrt(Lambda).  a0 ~ Lambda^(1/2).")

print()
print("="*78)
print("STEP 1 -- de Sitter horizon entropy S_dS(Lambda) [Gibbons-Hawking, verbatim]")
print("="*78)
# A = 4 pi R_dS^2 ; S = A/(4 G hbar/c^3 units) -> in Planck units S = A/4 l_P^2
# Use S_dS = A/(4 l_P^2) with A = 4 pi R_dS^2, l_P^2 = G hbar / c^3
A_hor = 4*sp.pi*R_dS**2
lP2 = G*hbar/c**3
S_dS = A_hor/(4*lP2)
S_dS = sp.simplify(S_dS)
print("A_horizon = 4 pi R_dS^2 =", sp.simplify(A_hor))
print("S_dS = A/(4 l_P^2) =", S_dS)
# Show S_dS = 3 pi / (Lambda l_P^2) = 3 pi c^3 /(Lambda G hbar)
S_dS_canon = 3*sp.pi/(Lam*lP2)
print("canonical 3 pi/(Lambda l_P^2) match:", sp.simplify(S_dS - S_dS_canon)==0)
print("   => S_dS = 3 pi c^3 / (G hbar Lambda)  ~  1/Lambda.   S_dS ~ Lambda^(-1).")

# derivative wrt Lambda: dS/dLambda < 0
dS_dLam = sp.diff(S_dS, Lam)
print("dS_dS/dLambda =", sp.simplify(dS_dLam), " (negative => S grows as Lambda falls)")
print("   sign of dS/dLambda:", "NEGATIVE" if sp.simplify(dS_dLam).subs(
    {sp.pi:3.14159, c:3e8, G:6.67e-11, hbar:1e-34, Lam:1e-52}) < 0 else "positive")

print()
print("="*78)
print("STEP 2 -- the CHAIN claimed by the brief, made explicit and CHECKED")
print("="*78)
print(" high-Lambda PAST  => small R_dS=sqrt(3/Lambda) => small A => SMALL S_dS")
print(" Lambda declines   => R_dS grows             => A grows  => S_dS GROWS")
print(" Express a0 and S_dS in each other to see they move OPPOSITELY:")
# a0 ~ Lambda^1/2 ; S_dS ~ Lambda^-1 => S_dS ~ a0^-2
# solve Lambda from a0
Lam_of_a0 = sp.solve(sp.Eq(a0, sp.Symbol('a0_v', positive=True)), Lam)[0]
a0v = sp.Symbol('a0_v', positive=True)
S_of_a0 = sp.simplify(S_dS.subs(Lam, Lam_of_a0))
print(" Lambda(a0) =", Lam_of_a0)
print(" S_dS(a0)  =", S_of_a0, "   => S_dS ~ a0^(-2).")
print(" CONFIRMED: a0 DOWN  <=>  S_dS UP. Declining a0 == growing horizon entropy.")
print(" So IF a0 truly declines (Lambda truly declines), the 2nd law direction and")
print(" the a0-decline direction COINCIDE by construction.  [algebra OK]")

print()
print("="*78)
print("STEP 3 -- the HONESTY FORK: is Lambda actually declining in this framework?")
print("="*78)
print(" TWO distinct 'a0(z) declining' readings live in the corpus -- they are NOT")
print(" the same and only ONE makes Lambda (hence S_dS) time-dependent:")
print()
print(" READING A  (CANONICAL pure-Lambda):  a0 = c^2 sqrt(Lambda/32pi), Lambda = TRUE")
print("            cosmological CONSTANT.  Then a0 is CONSTANT in time, rho_DE const,")
print("            and S_dS = 3pi/(Lambda l_P^2) is a CONSTANT CEILING. NO arrow from a0.")
print()
print(" READING B  (total-density / horizon):  a0(z) = c H(z)/Z ~ sqrt(rho_total).")
print("            H(z) declines as matter dilutes => a0 declines. But here the thing")
print("            declining is rho_TOTAL (matter+rad+Lambda), NOT Lambda. The horizon")
print("            that grows is the APPARENT/Hubble horizon r=c/H(z), NOT the dS one.")
print()
print(" READING C  (DESI evolving-DE, the brief's literal words 'rho_DE higher in past'):")
print("            Lambda_eff(z) = 8piG rho_DE(z)/c^2 with rho_DE ITSELF declining")
print("            (thawing/w0wa). ONLY here is Lambda time-dependent => only here does")
print("            S_dS = 3pi/(Lambda(z) l_P^2) actually move.")
print()
print(" The brief conflates A and C. The arrow-from-S_dS argument REQUIRES reading C")
print(" (a genuinely time-dependent Lambda). Reading A (the framework's CANONICAL,")
print(" Z-corroborated footing) gives a CONSTANT S_dS and therefore NO arrow at all.")

print()
print("="*78)
print("STEP 4 -- numbers: S_dS today, and S_dS in each reading at z~ matter era")
print("="*78)
subs_num = {c:2.99792458e8, G:6.674e-11, hbar:1.054571817e-34,
            sp.pi:sp.pi}
Lam_today = 1.091e-52  # 1/m^2
S_today = float(S_dS_canon.subs(subs_num).subs(Lam, Lam_today))
print(f" Lambda_today = {Lam_today:.3e} 1/m^2")
print(f" S_dS(today)  = {S_today:.3e} k_B   (the ~10^122 number)")
print()
# Reading C: if rho_DE was, say, 2x higher at z~? (DESI thawing gives modest change)
for factor, label in [(1.0,'today'),(1.1,'rho_DE +10% (DESI-ish past)'),
                      (2.0,'rho_DE x2 past'),(10.0,'rho_DE x10 early')]:
    Lam_past = Lam_today*factor
    S_past = float(S_dS_canon.subs(subs_num).subs(Lam, Lam_past))
    print(f"   READING C: {label:28s} Lambda={Lam_past:.3e}  S_dS={S_past:.3e}"
          f"  (dS from today: {S_past-S_today:+.2e})")
print(" => In reading C a higher past rho_DE gives a LOWER past S_dS: a real low-entropy")
print("    past. But the MAGNITUDE of the dS-entropy change is tiny unless rho_DE was")
print("    HUGELY higher early on (which DESI thawing does NOT support -- only ~O(10%)).")

print()
print("="*78)
print("STEP 5 -- the BUDGET CHECK: is dS_dS even the dominant entropy? (Penrose's point)")
print("="*78)
print(" The cosmic ENTROPY BUDGET (Egan-Lineweaver 2010, arXiv:0909.3983):")
print("   S_dS (cosmic event horizon)  ~  2.6 x 10^122 k_B   (>99.99% of total)")
print("   S_SMBH (supermassive BHs)    ~  1.2 x 10^103 k_B")
print("   S_stellar BH ~10^97; S_photons,nu ~10^89; S_baryons ~10^81 ...")
print(" => S_dS DOMINATES the budget by ~19 orders. So 'S_dS rising = 2nd law' is, to")
print("    leading order, the WHOLE entropy story -- the horizon IS the universe's")
print("    entropy. This is a genuine point IN FAVOR of the arrow=horizon-growth idea.")
print(" BUT (the catch): in READING A, S_dS is a fixed CEILING (S_max), and the")
print("    realized horizon entropy approaches it MONOTONICALLY from below as matter")
print("    dilutes -- this monotone rise is the STANDARD generalised-2nd-law arrow,")
print("    and it needs NO declining Lambda. The framework's a0 plays NO role in it.")

print()
print("="*78)
print("STEP 6 -- SOLVE or RE-POSIT? the decisive test")
print("="*78)
print(" The Past Hypothesis must explain why S(t=0) was LOW. Reading C's claim:")
print("   'the universe BEGINS at high Lambda (low S_dS) -> the low-S initial condition")
print("    is GIVEN by the high-Lambda start, not POSITED.'")
print()
print(" TEST: does high-Lambda-start DERIVE low total entropy, or just relabel it?")
print("   (a) S_dS = 3pi/(Lambda l_P^2): a high STARTING Lambda does give low STARTING")
print("       S_dS. TRUE as far as the horizon term goes.")
print("   (b) BUT the Past Hypothesis is about the LOW WEYL/clumping entropy + low")
print("       matter entropy (smooth hot plasma), NOT the horizon term. A small horizon")
print("       at early times is a KINEMATIC fact of ANY FRW model (LCDM included:")
print("       H large early => small apparent horizon => small horizon entropy). It is")
print("       NOT special to declining Lambda and does NOT address why matter began")
print("       smooth/cold-gravitationally (Weyl ~ 0). ")
print("   (c) Worse: to make S_dS itself START low you must POSIT a high INITIAL")
print("       Lambda and POSIT its monotone decline -- you have traded the Past")
print("       Hypothesis on S for a Past Hypothesis on Lambda(t_0) and a monotonicity")
print("       postulate on Lambda(t). That is RE-POSITING, not deriving.")
print()
print(" VERDICT STEP 6: declining-Lambda RE-POSITS the low-entropy past (moves it from")
print(" S to Lambda) and addresses only the horizon term, which is low early in ANY")
print(" cosmology. It does NOT derive the Weyl/Past-Hypothesis content. SAME as the")
print(" PENROSE_CROSS_DOORS verdict: S_dS is pure-Lambda, independent of the Weyl")
print(" initial condition the Past Hypothesis is actually about.")

print()
print("="*78)
print("STEP 7 -- is the DECLINE required (DESI) or optional?")
print("="*78)
print(" - The framework's CANONICAL a0 (Reading A, the Z-corroborated one) needs")
print("   Lambda = CONSTANT. Under Reading A there is NO declining Lambda, NO declining")
print("   S_dS, and the arrow argument DOES NOT EVEN APPLY (S_dS is a constant ceiling).")
print(" - The arrow-from-declining-a0 story is OPTIONAL: it is only available in the")
print("   speculative Reading C (DESI evolving-DE w0wa). DESI DR2 (2024-26) hints at")
print("   thawing DE at ~2-4 sigma but it is NOT established, and even if real the")
print("   rho_DE change is O(10%), giving a NEGLIGIBLE S_dS change (Step 4).")
print(" - So: the framework does NOT REQUIRE a declining Lambda; its own best footing")
print("   FORBIDS it. The arrow story is a bolt-on that needs an EXTERNAL (DESI) input")
print("   the framework neither predicts nor derives.")
