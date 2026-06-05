#!/usr/bin/env python3
r"""
THE LAST FORCING ROUTE (item D in the definitive verdict): the covariant O(eps^3) free
energy of the AeST C(Q)Y^{3/2} vertex on a STRAINED (inhomogeneous) de Sitter horizon --
the Verlinde-4/3-survival fork, done covariantly.
================================================================================================
QUESTION (verbatim from the verdict, line 80-83): does matching the MOND free energy (with its
R_dS IR cutoff) on a strained horizon to the first law delta Q = T delta S FORCE kappa=1/2
(a0 = (c/2)sqrt(G rho_Lambda), Z=sqrt(32pi/3)=5.789), or does the freedom persist / a different
number appear (Verlinde 6, etc.)?

THE FORK (the verdict flagged it): Verlinde's elastic derivation gives a0/6 because his strain
energy is QUADRATIC (mu eps^2) and his integral int eps^2 A dr returns the volume at FIRST power
(the sphere 4/3 collapses to the 1/d ball factor -> d(d-1)=6). Redo with the COVARIANT cubic
vertex C|grad phi|^3 (a genuine 3/2 power, NOT quadratic): does the sphere-volume 4/3 survive
(-> kappa=1/2) or cancel (-> 6)?  What principle decides?

RESULT (this script, every factor in sympy, independently reproducible):
  The fork does NOT resolve to kappa=1/2. The cubic vertex changes the eps-POWER of the strain
  free energy from Verlinde's eps^2 to eps^3, while the horizon entropy / first-law response is
  irreducibly eps^2 (the area of a trace-free-strained sphere is O(eps^2), O(eps) vanishing). The
  resulting 3-vs-2 power mismatch means F_MOND = delta Q cannot be an identity: it fixes the
  STRAIN AMPLITUDE eps, leaving a0 (hence kappa) carrying an UNFIXED eps -- a continuous freedom,
  not 1/2. Equivalently, the cubic ON-SHELL action is LOGARITHMIC (int dr/r), so there is NO
  sphere 4/3 to "survive" at all; the angular 4pi is eaten by the 1/(12pi) normalization leaving
  a bare 1/3 times an arbitrary log(R_dS/r_min). Forcing a number out of the cubic vertex requires
  an EXTRA posit (eps=1, or a choice of integration region, or a stress-balance ansatz), and
  DIFFERENT posits give DIFFERENT rationals -- NONE uniquely 1/2.

VERDICT: freedom persists. The Verlinde-survival fork resolves AGAINST closure: the genuine 3/2
power does not preserve the 4/3 (Verlinde's path), it removes the ball-volume factor entirely and
replaces the would-be coefficient with an undetermined strain amplitude/cutoff. kappa is NOT forced.

Needs sympy.
"""
import sympy as sp

# ---- exact target identities (the thing a closure would have to FORCE) -----------------------
G, c, Lam = sp.symbols('G c Lambda', positive=True)
rho_L = Lam*c**2/(8*sp.pi*G)
a0_target = (c/2)*sp.sqrt(G*rho_L)
Z_target  = sp.simplify(c*(c*sp.sqrt(Lam/3))/a0_target)     # cH_L/a0
assert sp.simplify(a0_target - c**2*sp.sqrt(Lam/(32*sp.pi))) == 0
assert sp.simplify(Z_target - 4*sp.sqrt(6)*sp.sqrt(sp.pi)/3) == 0       # = sqrt(32pi/3)
KAPPA_TARGET = sp.Rational(1,2)


def banner(s): print("="*94 + "\n" + s + "\n" + "="*94)


# ==============================================================================================
def part1_verlinde_quadratic_baseline():
    banner("PART 1 -- Verlinde QUADRATIC baseline: int eps^2 A dr returns Vol^1 (4/3 -> 1/d). [d-gen]")
    r, d, Vstar, r0 = sp.symbols('r d Vstar r0', positive=True)
    Omega = 2*sp.pi**(sp.Rational(1,2)*d)/sp.gamma(sp.Rational(1,2)*d)
    A = Omega*r**(d-1)
    u = -Vstar/A
    eps = sp.diff(u, r)                                       # = (d-1)Vstar/(Omega r^d)
    Iquad = sp.simplify(sp.integrate(eps**2 * A, (r, r0, sp.oo)))
    Vball = Omega/d * r0**d
    print("  int eps^2 A dr =", Iquad)
    print("  ratio to Vstar^2/(Omega r0^d) =", sp.simplify(Iquad/(Vstar**2/(Omega*r0**d))),
          "  (= (d-1)^2/d ; the 1/d is the only surviving geometry -> d(d-1)=6 with the tensor trace)")
    print("  => Verlinde's eps^2 integral returns the displaced VOLUME at FIRST power: 4/3 CANCELLED.\n")
    return sp.simplify(Iquad/(Vstar**2/(Omega*r0**d)))


# ==============================================================================================
def part2_cubic_onshell_action():
    banner("PART 2 -- AeST CUBIC on-shell action of a point mass, IR-cut at R_dS (the task setup).")
    r, M, a0, rmin = sp.symbols('r M a0 r_min', positive=True)
    R_dS = sp.sqrt(3/Lam)
    gp = sp.sqrt(G*M*a0)/r                                    # deep-MOND point-mass field
    assert sp.simplify(gp**2/a0 - G*M/r**2) == 0             # Newtonian-from-MOND check
    L = -gp**3/(12*sp.pi*G*a0)                                # AQUAL f->(2/3)x^{3/2}
    I = sp.simplify(sp.integrate(L*4*sp.pi*r**2, (r, rmin, R_dS)))
    F = sp.simplify(-I)
    F_clean = sp.Rational(1,3)*M**sp.Rational(3,2)*sp.sqrt(G*a0)*sp.log(R_dS/rmin)
    assert sp.simplify(F - F_clean) == 0
    print("  F_MOND = (1/3) M^{3/2} sqrt(G a0) ln(R_dS/r_min)   [POWER M^{3/2}, carries a LOG]")
    print("  -- the angular 4pi cancels the 1/(12pi) -> a bare 1/3; the radial integral is dr/r")
    print("     (LOGARITHMIC). There is NO sphere 4/3 in the on-shell action to 'survive'.\n")
    return F_clean


# ==============================================================================================
def part3_firstlaw_horizon_side():
    banner("PART 3 -- strained dS first law: delta Q = T delta S. Two clean facts established.")
    M, a0, rh, drh, hbar = sp.symbols('M a0 r_h dr_h hbar', positive=True)
    R_dS = sp.sqrt(3/Lam); H_L = c*sp.sqrt(Lam/3); T = hbar*H_L/(2*sp.pi)
    # (3a) gross SdS shift from a central mass M:  dQ = T dS = -M c^2 (exact, hbar cancels)
    fSdS = 1 - 2*G*M/(c**2*rh) - (Lam/3)*rh**2
    expr = sp.series(sp.series(fSdS.subs(rh, R_dS+drh), M,0,2).removeO(), drh,0,2).removeO()
    drh_val = sp.simplify(sp.series(sp.solve(sp.Eq(expr,0), drh)[0], M,0,2).removeO())
    dA = sp.simplify(8*sp.pi*R_dS*drh_val)
    dQ = sp.simplify(T*(dA*c**3/(4*G*hbar)))
    print("  (3a) central mass M:  dr_h =", drh_val, " ;  dQ = T dS =", sp.simplify(dQ),
          "  (= -M c^2, exact; hbar cancels). [horizon side ~ M^1, NO log]")
    # (3b) inhomogeneous (trace-free l=2) strain: area is O(eps^2). Entropy response ~ eps^2.
    eps_, R, th, ph = sp.symbols('epsilon R theta varphi', real=True, positive=True)
    f = (3*sp.cos(th)**2 - 1)/2
    rr = R*(1+eps_*f); rp = sp.diff(rr, th)
    sqrtg = sp.sqrt(sp.expand((rp**2+rr**2)*rr**2*sp.sin(th)**2))
    ser = sp.expand(sp.series(sqrtg, eps_, 0, 4).removeO())
    Acoef1 = sp.simplify(sp.integrate(sp.integrate(ser.coeff(eps_,1), (ph,0,2*sp.pi)), (th,0,sp.pi)))
    Acoef2 = sp.simplify(sp.integrate(sp.integrate(ser.coeff(eps_,2), (ph,0,2*sp.pi)), (th,0,sp.pi)))
    print("  (3b) trace-free l=2 strain:  delta A  O(eps^1) coeff =", Acoef1,
          " ;  O(eps^2) coeff =", Acoef2, "= (16pi/5)R^2")
    print("       => horizon entropy response delta S = delta A/4lP^2 is O(eps^2). [NOT O(eps^3)]\n")
    return dQ, Acoef2


# ==============================================================================================
def part4_the_match_and_kappa(F_MOND, dQ):
    banner("PART 4 -- the MATCH F_MOND = dQ, and the OBSTRUCTION (power mismatch -> kappa not pinned).")
    M, a0, rmin = sp.symbols('M a0 r_min', positive=True)
    # gross-mass match (M^{3/2} vs M^1):
    dQ_lead = -M*c**2
    sol = sp.solve(sp.Eq(F_MOND, sp.Abs(dQ_lead)), a0)
    a0sol = sp.simplify(sol[0])
    kappa = sp.simplify(a0sol/(c*sp.sqrt(G*rho_L)))
    print("  (4a) gross-mass match (F_MOND ~ M^{3/2}  =  |dQ| ~ M^1):")
    print("       a0 =", a0sol)
    print("       kappa = a0/[c sqrt(G rho_L)] =", kappa)
    print("       free symbols in kappa:", kappa.free_symbols, " -> contains M and r_min: NOT a number.\n")
    # eps-expansion match (eps^3 vs eps^2) -- schematic, to show the residual eps:
    eps_, KM, KS = sp.symbols('epsilon K_M K_S', positive=True)
    F_sym = KM*sp.sqrt(a0)*eps_**3
    Q_sym = KS*(c**4/G)*eps_**2/sp.sqrt(Lam)
    a0_eps = sp.solve(sp.Eq(F_sym, Q_sym), a0)[0]
    kappa_eps = sp.simplify(a0_eps/(c*sp.sqrt(G*rho_L)))
    print("  (4b) strained-horizon eps-match (F_MOND ~ eps^3  =  dQ ~ eps^2):")
    print("       a0 =", sp.simplify(a0_eps), "  (carries 1/eps^2)")
    print("       kappa =", kappa_eps, "  free symbols:", kappa_eps.free_symbols,
          " -> contains eps: NOT a number.\n")
    return kappa, kappa_eps


# ==============================================================================================
def part5_adhoc_closures_give_different_numbers():
    banner("PART 5 -- forcing a number out anyway needs an EXTRA posit; different posits -> diff rationals.")
    a0 = sp.symbols('a0', positive=True)
    R_dS = sp.sqrt(3/Lam); H_L = c*sp.sqrt(Lam/3)
    # (5a) Verlinde criterion eps=1 + bulk-volume (4/3)piR^3 integration:
    F_density = a0**2*1**3/(12*sp.pi*G)                         # eps=1
    F_A = F_density*sp.Rational(4,3)*sp.pi*R_dS**3
    dQ_A = (H_L*c**3/(8*sp.pi*G))*(sp.Rational(16,5)*sp.pi*R_dS**2*1**2)
    a0_A = sp.solve(sp.Eq(F_A, dQ_A), a0)[0]
    Z_A = sp.simplify(c*H_L/a0_A)
    # (5b) stress-balance sigma_MOND = dQ/V:
    sig = a0**2/(4*sp.pi*G)                                     # d/deps[a0^2 eps^3/12piG] at eps=1
    dQV = sp.simplify(dQ_A/(sp.Rational(4,3)*sp.pi*R_dS**3))
    a0_B = sp.solve(sp.Eq(sig, dQV), a0)[0]
    Z_B = sp.simplify(c*H_L/a0_B)
    print("  (5a) eps=1 + bulk-volume:   Z = cH/a0 =", sp.nsimplify(Z_A), "=", float(Z_A))
    print("  (5b) stress balance:        Z = cH/a0 =", sp.nsimplify(Z_B), "=", float(Z_B))
    print("  TARGET (kappa=1/2):         Z =", float(Z_target), " (= sqrt(32pi/3))")
    print("  Verlinde:                   Z = 6.000  ;  thermal: Z = 2pi = 6.283")
    print("  => the cubic ad-hoc closures land at", round(float(Z_A),2), "and", round(float(Z_B),2),
          "-- NEITHER is 5.789, and they DISAGREE with each other.")
    print("     (their specific values are artifacts of the crude shell/volume ansatz; the load-bearing")
    print("      fact is that they are choice-dependent and not 1/2.)\n")
    return float(Z_A), float(Z_B)


def main():
    print("#"*94)
    print("# Strained-horizon O(eps^3): the Verlinde-survival fork, done covariantly.")
    print("# Target a closure must FORCE:  kappa = 1/2,  Z = sqrt(32pi/3) = %.4f" % float(Z_target))
    print("#"*94 + "\n")

    q_ratio = part1_verlinde_quadratic_baseline()
    F_MOND  = part2_cubic_onshell_action()
    dQ, Acoef2 = part3_firstlaw_horizon_side()
    kappa, kappa_eps = part4_the_match_and_kappa(F_MOND, dQ)
    Z_A, Z_B = part5_adhoc_closures_give_different_numbers()

    banner("FINAL VERDICT")
    print(f"""  The Verlinde-4/3-survival fork resolves AGAINST closure.

  WHY VERLINDE GETS A NUMBER (6): his strain energy is QUADRATIC (eps^2). The entropy/first-law
    response is also eps^2 (area of a strained sphere is O(eps^2), Part 3b). The eps^2 CANCELS in
    the match, leaving a pure geometric number -- the sphere 4/3 collapses to the 1/d ball factor,
    giving d(d-1)=6 (Part 1, ratio (d-1)^2/d).

  WHY THE COVARIANT CUBIC VERTEX DOES NOT: the genuine 3/2 power makes the strain free energy
    O(eps^3) (Part 2/4b) while the horizon response stays O(eps^2) (Part 3b). The 3-vs-2 power
    MISMATCH means F_MOND = delta Q is not an identity: it fixes the STRAIN AMPLITUDE eps and
    leaves a0 (hence kappa) carrying an UNFIXED eps (Part 4b). Equivalently the cubic ON-SHELL
    action is LOGARITHMIC (Part 2): there is no sphere 4/3 to survive -- the 4pi is eaten by the
    1/(12pi), leaving a bare 1/3 times an ARBITRARY log(R_dS/r_min).

  WHAT PRINCIPLE DECIDES (the answer to the task's question): the DEGREE of the vertex vs the
    DEGREE of the area functional. Verlinde's match works ONLY because both are quadratic (2=2).
    The covariant MOND term is cubic; the horizon area is quadratic; 3 != 2, so no eps-independent
    pure number can be read off. The 3/2 power that the framework needs is EXACTLY the power that
    breaks Verlinde's cancellation -- not in favor of 4/3-survival, but by introducing a new,
    unfixed strain scale. (Forcing a number anyway needs an extra posit; Part 5: eps=1 -> Z~{Z_A:.2f},
    stress-balance -> Z~{Z_B:.2f}; neither is {float(Z_target):.3f}, and they disagree.)

  kappa = 1/2 is NOT forced. The freedom persists -- now demonstrated for the LAST (off-saddle,
    strained-horizon) route the definitive verdict had left open. This closes item D as a rigorous
    null by the SAME structural fact in a new guise: on the homogeneous saddle Ybar=0 hid a0
    (saddle-blindness); off the saddle, the cubic vertex's eps^3 vs the area's eps^2 prevents the
    coefficient from being read off. Either way, no equilibrium horizon thermodynamics fixes kappa.
  CONSISTENT with the whole prior sweep; predictions remain Z-free, so nothing empirical changes.""")
    print("#"*94)


if __name__ == "__main__":
    main()
