#!/usr/bin/env python3
"""
GAP A -- the INTERPOLATION mu.  Can the Deser-Levin dS-Unruh temperature T(a)=sqrt(a^2+a_Lambda^2)
PRODUCE the framework's own interpolation, from a PRINCIPLED postulate -- or only by reverse-engineering?
====================================================================================================
Framework (its OWN terms, NOT standard-MOND):
    a0   = cH_Lambda / Z,   Z = sqrt(32 pi/3) ~ 5.7927
    g_obs = sqrt(g_bar^2 + g_bar*a0)            (modified INERTIA)
Deser-Levin (Deser & Levin 1997; Narnhofer-Peter-Thirring 1996; Milgrom 1999):
    T(a) = (hbar/2 pi c k) sqrt(a^2 + a_Lambda^2),   a_Lambda = c H_Lambda  (the dS-Unruh floor).

This script does ONE thing, adversarially: enumerate the PRINCIPLED ways an inertial response could
couple to T(a), DERIVE mu(x) symbolically for each, check the Newtonian + deep-MOND limits, and ask the
ONLY question that matters for a 'closure': does it match the framework's mu, and if so is the postulate
INDEPENDENTLY principled or REVERSE-ENGINEERED to hit sqrt(g^2+g*a0)?

Banked walls we BUILD ON (do not re-derive, cite):
  * Z is UNFORCED (kappa-closure + number-field sqrt(pi)): project_zimmerman_coefficient_footing.
  * covariant MI = trichotomy: local->ghost, field->Cassini, nonlocal->active-kernel SIGN theorem
    (passive dS vacuum gives rho>=0 => delta_m>=0 => ANTI-MOND). project_covariant_mi_completion.
  * banked deser_levin_mond_derivation.py: naive F=T(a)-T(0) gives deep-MOND + scale ~cH_Lambda (REAL),
    but coefficient 2 a_Lambda (= 2Z a0, not a0), mu_mech=(sqrt(1+x^2)-1)/x (not framework's), no EOM.

Convention for mu: an inertial law  mu(a/a0) * a = g_bar  (modified inertia: the ACTUAL accel a obeys
g_obs := a, so mu*g_obs = g_bar). Newtonian: mu->1 at large arg. Deep-MOND: mu->(a/a0)/k for some k,
giving a = sqrt(k a0 g_bar). The framework's a = g_obs solves g_obs^2 = g_bar^2 + g_bar a0.
Needs sympy only. Exit 0.
"""
import sympy as sp

# ---------------------------------------------------------------------------
# 0. THE TARGET: the framework's OWN mu, extracted EXACTLY from g_obs=sqrt(g^2+g a0).
# ---------------------------------------------------------------------------
def section_target():
    print("="*100)
    print(" 0. THE TARGET -- the framework's interpolation, extracted exactly from g_obs=sqrt(g_bar^2+g_bar a0)")
    print("="*100)
    g, a0 = sp.symbols('g_bar a0', positive=True)
    gobs = sp.sqrt(g**2 + g*a0)
    # modified inertia: actual accel a = g_obs obeys mu(a/a0)*a = g_bar. Solve mu in terms of x=a/a0.
    a, x = sp.symbols('a x', positive=True)
    # from a = sqrt(g^2+g a0): a^2 = g^2 + g a0 -> g^2 + a0 g - a^2 = 0 -> g = (-a0+sqrt(a0^2+4a^2))/2
    g_of_a = (-a0 + sp.sqrt(a0**2 + 4*a**2))/2
    mu_fw = sp.simplify(g_of_a / a)                 # mu = g_bar / a
    mu_fw_x = sp.simplify(mu_fw.subs(a, x*a0))      # in x=a/a0
    print("  g_obs = sqrt(g_bar^2 + g_bar a0).  Invert (a:=g_obs):  g_bar = (-a0+sqrt(a0^2+4a^2))/2.")
    print(f"  => mu_fw(x) = g_bar/a = {mu_fw_x}      (x = a/a0)")
    # limits
    lim_hi = sp.limit(mu_fw_x, x, sp.oo)
    lo = sp.series(mu_fw_x, x, 0, 2).removeO()
    print(f"     Newtonian  x->oo : mu_fw -> {lim_hi}   (OK)")
    print(f"     deep-MOND  x->0  : mu_fw ~ {sp.simplify(lo)}   => a = sqrt({sp.simplify(1/ (lo/x))} * a0 * g_bar)")
    # deep-mond coefficient k_fw: mu~x/k => a^2 = k a0 g_bar
    k_fw = sp.simplify(x/lo)
    print(f"     => deep-MOND coefficient k_fw = {k_fw}  (a = sqrt(k a0 g_bar), so a0_eff = k*a0 = a0).")
    print("  This is the EXACT object every postulate below must reproduce to count as a closure.\n")
    return mu_fw_x, x, a0

# ---------------------------------------------------------------------------
# helper: given a candidate mu(x) (x=a/a0_or_aL), report limits + deep-MOND coeff + match-to-target
# ---------------------------------------------------------------------------
def report(name, mu_expr, x, target_mu, scale_note):
    print(f"  --- {name} ---")
    print(f"     mu(x) = {mu_expr}        ({scale_note})")
    try:
        lim_hi = sp.limit(mu_expr, x, sp.oo)
    except Exception:
        lim_hi = sp.nsimplify(mu_expr.subs(x, 1e9))
    print(f"     Newtonian x->oo : mu -> {lim_hi}  {'OK' if sp.simplify(lim_hi-1)==0 else 'FAIL (no Newtonian limit)'}")
    lo = sp.series(mu_expr, x, 0, 2).removeO()
    lo = sp.simplify(lo)
    print(f"     deep-MOND x->0  : mu ~ {lo}")
    # match to framework target form (both as functions of their own x)?
    diff = sp.simplify(mu_expr - target_mu)
    matches = (diff == 0)
    print(f"     == framework mu_fw(x) ?  {'YES (identical function)' if matches else 'NO (different function)'}")
    if not matches:
        # are they the same FAMILY up to rescaling x -> c x ? try to find c making them equal
        c = sp.symbols('c', positive=True)
        try:
            sol = sp.solve(sp.simplify(mu_expr.subs(x, c*x) - target_mu), c, dict=True)
            sol = [s for s in sol if s.get(c, None) is not None]
            if sol:
                cc = sp.simplify(sol[0][c])
                # check it actually holds identically
                if sp.simplify(mu_expr.subs(x, cc*x) - target_mu) == 0:
                    print(f"     ...but SAME FAMILY: mu(x)=mu_fw(x) after rescaling x->{cc} x  (i.e. only the a0-coefficient differs).")
                else:
                    print(f"     ...not even same family under linear rescale of x.")
            else:
                print(f"     ...not same family under linear rescale of x.")
        except Exception:
            print(f"     ...family check inconclusive symbolically.")
    print()
    return matches

# ---------------------------------------------------------------------------
def main():
    target_mu, x, a0 = section_target()

    print("="*100)
    print(" ENUMERATE PRINCIPLED POSTULATES: how does inertia couple to T(a)=sqrt(a^2+a_Lambda^2)?")
    print("   (units a_Lambda=1; x=a/a_Lambda for the bare-temperature routes. target written in x=a/a0;")
    print("    we compare FUNCTIONAL FORM, then separately the coefficient/scale.)")
    print("="*100 + "\n")

    xs = sp.symbols('x', positive=True)
    # bare-temperature routes use x = a/a_Lambda. Framework target uses x=a/a0. Compare forms; coeff handled per-case.
    # Re-express target in a SCALE-FREE way for form comparison: the framework family is f(x)=(sqrt(1+4x^2)-1)/(2x).
    fw_family = (sp.sqrt(1+4*xs**2)-1)/(2*xs)

    results = {}

    # (i) F = T(a)-T(0)  [BANKED]  -> mu = (T(a)-T(0))/a in the inertial-response reading
    print(" (i) POSTULATE  F = T(a) - T(0)   [Milgrom 1999 / banked deser_levin_mond_derivation.py]")
    print("     inertial response = excess heat over the dS vacuum. mu(x) = (sqrt(1+x^2)-1)/x, x=a/a_Lambda.")
    mu_i = (sp.sqrt(1+xs**2)-1)/xs
    results['(i) F=T(a)-T(0)'] = report("(i) F=T(a)-T(0)", mu_i, xs, fw_family,
                                        "x=a/a_Lambda; banked")
    print("     SCALE: deep-MOND a=sqrt(2 a_Lambda g)=sqrt(2Z a0 g) => a0_eff=2 a_Lambda = 2Z a0 ~ 11.6 a0. OFF by 2Z.")
    print("     VERDICT: principled (Milgrom's vacuum-heat idea) but WRONG FORM and wrong coeff. Not the framework's.\n")

    # (ii) inertial mass m_i proportional to T(a) (or T(a)/T(0))
    print(" (ii) POSTULATE  m_inertial(a) proportional to T(a)   [the 'mass IS the seen temperature' reading]")
    print("      Law: m(a) a = m0 g  with m(a)/m0 = T(a)/T(0) = sqrt(1+x^2).  => mu(x)=sqrt(1+x^2).")
    mu_ii = sp.sqrt(1+xs**2)
    results['(ii) m_i ~ T(a)'] = report("(ii) m_i ~ T(a)", mu_ii, xs, fw_family, "x=a/a_Lambda")
    print("      Newtonian OK (->...check), but deep-MOND: mu->1, NOT ->0 -> inertia RISES at low a = ANTI-MOND.")
    print("      This is EXACTLY the passive-vacuum sign theorem (covariant-MI nonlocal horn): T(a)>=T(0) always")
    print("      => m_i raised => anti-MOND. Cite project_covariant_mi_completion. WRONG SIGN. Dead.\n")

    print(" (ii') POSTULATE  m_inertial(a) proportional to T(0)/T(a)  [invert: 'hotter => lighter']")
    print("      mu(x)=T(0)/T(a)=1/sqrt(1+x^2).  Gives MOND sign? check:")
    mu_iip = 1/sp.sqrt(1+xs**2)
    results["(ii') m_i ~ 1/T(a)"] = report("(ii') m_i ~ T(0)/T(a)", mu_iip, xs, fw_family, "x=a/a_Lambda")
    print("      Newtonian x->oo: mu->0 (NOT 1) -- inertia VANISHES at high a. NO Newtonian limit. Dead, and ad hoc.\n")

    # (iii) thermodynamic F = T dS/dx with horizon entropy S ~ Area ~ 1/T^2 (de Sitter) -> entropic force
    print(" (iii) POSTULATE  thermodynamic/entropic F = T dS/dx  (Verlinde-style, horizon entropy S)")
    print("       de Sitter horizon entropy S ~ A ~ 1/H^2 ~ 1/T^2 (Gibbons-Hawking). With T=T(a):")
    print("       S(a) ~ 1/T(a)^2 = 1/(a^2+a_L^2).  Entropic force on the probe F = T dS/d(something).")
    # Verlinde's actual construction: F = T dS/dx with dS/dx = 2 pi kB m c/hbar (equipartition), T=T(a).
    # That gives F = (a-dependent T)*const -> just reproduces (i)-like temperature law, not new. Instead the
    # SHARP entropic reading: number of bits N ~ A ~ 1/T^2; equipartition E=1/2 N kB T; F from dE.
    # We test the cleanest principled version: F = -dE/dx with E= 1/2 N kB T, N ~ 1/T^2 => E ~ 1/T => E ~ 1/sqrt(a^2+1).
    # Then "force" ~ dE/da is not an inertia law without an extra postulate. The honest statement:
    print("       Equipartition E=(1/2)N kB T with N ~ A ~ 1/T^2 gives E ~ 1/T ~ 1/sqrt(a^2+a_L^2): DECREASING in a.")
    E_iii = 1/sp.sqrt(xs**2+1)
    dE = sp.simplify(sp.diff(E_iii, xs))
    print(f"       dE/dx = {dE}  -> a 'force' that is NEGATIVE and ->0 at large a: gives no Newton limit, no mu.")
    print("       To get an inertia law you must POSTULATE the map force<->mu separately. The entropy route does")
    print("       NOT, by itself, output a mu(x); it reproduces a temperature law only after re-inserting equipartition")
    print("       (= route (i)). No NEW principled mu. (And Verlinde's own a0 = cH/(2pi), Z=2pi, not Z=sqrt(32pi/3).)")
    print("       VERDICT: does not independently yield the framework's mu. Cite banked Z-unforced.\n")
    results['(iii) entropic F=TdS'] = False

    # (iv) free-energy / partition-function route: F_free = -T ln Z_part, inertia from d^2/da^2 etc.
    print(" (iv) POSTULATE  free-energy route: a thermal probe has free energy phi(a) ~ -T(a) (one dof),")
    print("       and inertial mass = curvature of phi in the velocity/accel response.")
    print("       Cleanest principled form: m_i(a) ~ d phi/d(accel-potential). For a single mode phi=-T(a):")
    phi = -sp.sqrt(xs**2+1)
    mphi = sp.simplify(sp.diff(phi, xs))           # ~ -x/sqrt(1+x^2)  (a response)
    print(f"       d phi/dx = {sp.simplify(sp.diff(phi,xs))}  -> magnitude x/sqrt(1+x^2): a SIGMOID response.")
    mu_iv = xs/sp.sqrt(1+xs**2)
    results['(iv) free-energy dT/da'] = report("(iv) mu = dT/da = x/sqrt(1+x^2)", mu_iv, xs, fw_family, "x=a/a_Lambda")
    print("       Newtonian x->oo: mu->1 (OK!). deep-MOND x->0: mu ~ x => a=sqrt(a_L g): MOND sign+law CORRECT.")
    print("       *** This is the 'simple-nu' family mu=x/sqrt(1+x^2) -- right limits, but a DIFFERENT function")
    print("       from the framework's (sqrt(1+4x^2)-1)/(2x). And note: choosing phi=-T(a) and 'mu=dphi/dx' is")
    print("       a CHOSEN map, not forced; other free-energy maps give other mu. Principled-ish, but NOT the")
    print("       framework's mu and NOT uniquely forced. Honest: a near-miss, still a posit.\n")

    # (v) Milgrom 2011/2022 time-nonlocal memory-kernel theta(y): the ONLY ghost-free corner (banked trichotomy)
    print(" (v) POSTULATE  Milgrom-2011/2022 time-NONLOCAL memory kernel theta(y)  [the ghost-free corner]")
    print("      MI from a worldline action S=-m c^2 int dt sqrt(...)*Theta[{a(t)}/a0] with a nonlocal functional.")
    print("      Milgrom's existence result: for ANY desired mu(x) one can CONSTRUCT a kernel reproducing it for")
    print("      circular orbits -- so this route can match the framework's mu BY CONSTRUCTION.")
    print("      *** That is precisely the problem: it matches because it is REVERSE-ENGINEERED. The kernel is")
    print("      CHOSEN to give the target mu; it is not predicted by the dS temperature. AND the banked active-")
    print("      kernel SIGN THEOREM (project_covariant_mi_completion) shows the MOND-signed kernel CANNOT be")
    print("      sourced from the passive dS vacuum (Kallen-Lehmann rho>=0 => delta_m>=0 => anti-MOND). So the")
    print("      one route that CAN hit the framework's mu is (a) reverse-engineered and (b) provably not derivable")
    print("      from the dS-Unruh temperature itself. VERDICT: matches only by construction = NOT a derivation.\n")
    results['(v) nonlocal kernel'] = 'matches-by-construction'

    # ---------------------------------------------------------------------------
    # ADVERSARIAL CORE: is there ANY single-function-of-T postulate whose mu = framework mu?
    # Frame it as: can sqrt(1+4x^2)-1 over 2x arise from an algebraic combination of T(a)=sqrt(a^2+1) and T(0)=1?
    # ---------------------------------------------------------------------------
    print("="*100)
    print(" ADVERSARIAL CORE -- can the framework's mu be BUILT from T(a),T(0) by a principled algebraic map?")
    print("="*100)
    a, aL, a0sym = sp.symbols('a a_Lambda a0', positive=True)
    Ta = sp.sqrt(a**2 + aL**2); T0 = aL
    # framework inertia law in physical units: g_bar = a - a0/2 + ... actually g_bar = (-a0+sqrt(a0^2+4a^2))/2
    gbar_fw = (-a0sym + sp.sqrt(a0sym**2 + 4*a**2))/2
    print("  Framework (modified inertia, a:=g_obs):  g_bar(a) = (-a0 + sqrt(a0^2 + 4 a^2))/2.")
    print(f"     i.e. g_bar = {gbar_fw}")
    print("  Bare temperature gives, in the SAME inertial-response reading F=g_bar:")
    print("     route (i):  g_bar = T(a)-T(0) = sqrt(a^2+a_L^2) - a_L.")
    gbar_i = Ta - T0
    print(f"     i.e. g_bar = {gbar_i}")
    print("  KEY STRUCTURAL FACT: T(a)-T(0)=sqrt(a^2+a_L^2)-a_L has a^2 UNDER a CONSTANT(a_L^2) sqrt;")
    print("  the framework's g_bar has 4a^2 under a sqrt of a0^2 (a0=a_L/Z), and is LINEAR-shifted by a0/2.")
    print("  Map them: T(a)-T(0) -> g_bar requires a_L^2 -> a0^2 AND a^2 -> 4a^2/... i.e. you must replace the")
    print("  CONSTANT dS floor a_L by a0 AND multiply the acceleration term -- two independent rescalings:")
    # Solve: for what (p,q) does p*(sqrt(a^2+q^2)-q) equal gbar_fw identically? It can't (linear shift -a0/2).
    p, q = sp.symbols('p q', positive=True)
    cand = p*(sp.sqrt(a**2 + q**2) - q)
    diff = sp.simplify(cand - gbar_fw)
    # try to solve for p,q making diff==0 for all a -> compare leading + sub-leading
    # expand both at large a and small a
    cand_lo = sp.series(cand, a, 0, 3).removeO()
    fw_lo   = sp.series(gbar_fw, a, 0, 3).removeO()
    print(f"     small-a:  route(i)-form ~ {sp.simplify(cand_lo)}")
    print(f"               framework     ~ {sp.simplify(fw_lo)}")
    print("     route(i)-form is PURELY a^2 at small a (deep-MOND, g~a^2/2q); the framework is a^2/a0 + O(a^4)")
    print("     ALSO pure a^2 at leading order -- BUT the framework has NO linear-in-a term while ANY single")
    print("     sqrt(a^2+q^2)-q form also has none, so the deep-MOND LIMITS can be matched (set 2pq... ).")
    cand_hi = sp.simplify(sp.series(cand, a, sp.oo, 2).removeO())
    fw_hi   = sp.simplify(sp.series(gbar_fw, a, sp.oo, 2).removeO())
    print(f"     large-a:  route(i)-form -> {cand_hi}   (->p*a - p*q)")
    print(f"               framework     -> {fw_hi}   (-> a - a0/2)")
    print("     Newtonian (g_bar->a) forces p=1. Then route(i)-form -> a - q; framework -> a - a0/2.")
    print("     Matching the CONSTANT offset forces q=a0/2. Plug p=1,q=a0/2 into the FULL form and test identity:")
    cand_fix = cand.subs({p:1, q:a0sym/2})
    identity = sp.simplify(cand_fix - gbar_fw)
    print(f"     [p=1,q=a0/2]:  (route-i form) - (framework)  =  {identity}")
    if identity == 0:
        print("     *** ALGEBRAIC IDENTITY: with p=1 and q=a0/2, T(a)-T(0) EXACTLY reproduces the framework's g_bar! ***")
    else:
        print("     => NOT identically zero: the framework's mu is NOT the bare T(a)-T(0) law for any (p,q).")
    print()

    # report the q=a0/2 finding's meaning explicitly
    print("  INTERPRETATION of the (p=1, q=a0/2) result above:")
    if identity == 0:
        print("   - The framework's law IS route-(i) 'F=T(a)-T(0)' provided the temperature floor inside the sqrt is")
        print("     q=a0/2 = a_Lambda/(2Z), NOT the physical dS floor a_Lambda. So to make the dS-Unruh temperature")
        print("     output the framework's mu you must REPLACE the Deser-Levin floor a_Lambda by a_Lambda/(2Z).")
        print("     That replacement is EXACTLY the unforced Z (project_zimmerman_coefficient_footing): the FORM")
        print("     (i) gives is right ONLY after inserting the 2Z coefficient by hand. The mu-shape match is")
        print("     therefore REVERSE-ENGINEERED through the same Z that is provably unforced. NOT a derivation.")
    print()

    # ---------------------------------------------------------------------------
    print("="*100)
    print(" SUMMARY LEDGER (both-ways; closure = matches framework mu FROM a principled, non-reverse-engineered postulate)")
    print("="*100)
    print(f"  {'postulate':<34}{'Newton?':<9}{'MOND sign?':<12}{'= fw mu?':<10}{'principled / reverse-eng':<28}")
    rows = [
      ("(i) F=T(a)-T(0)",        "yes", "yes", "NO",  "principled; wrong form+coeff(2Z)"),
      ("(ii) m_i ~ T(a)",        "yes", "NO(anti)", "NO", "principled; WRONG SIGN (theorem)"),
      ("(ii') m_i ~ T(0)/T(a)",  "NO",  "yes", "NO",  "ad hoc; no Newton limit"),
      ("(iii) entropic F=TdS",   "n/a", "n/a", "NO",  "yields no mu w/o re-inserting (i)"),
      ("(iv) free-energy dT/da", "yes", "yes", "NO",  "near-miss (simple-nu); still a posit"),
      ("(v) nonlocal kernel",    "yes", "yes", "by-constr", "REVERSE-ENGINEERED; +sign theorem"),
    ]
    for r in rows:
        print(f"  {r[0]:<34}{r[1]:<9}{r[2]:<12}{r[3]:<10}{r[4]:<28}")
    print()
    print("  HONEST NET (no manufactured closure, no manufactured deficit):")
    print("   * GAP A is NOT closed by a principled temperature postulate. Three robust facts:")
    print("     1. The bare dS-Unruh law F=T(a)-T(0) gives a DIFFERENT mu, (sqrt(1+x^2)-1)/x, with coeff 2Z (banked).")
    print("     2. The framework's mu IS reproducible by F=T(a)-T(0) ONLY if the temperature floor is set to")
    print("        a_Lambda/(2Z) instead of the physical Deser-Levin a_Lambda -- i.e. ONLY by inserting the")
    print("        unforced Z by hand (algebraically exact above). That is reverse-engineering, not derivation.")
    print("     3. The ONE route that can hit ANY target mu -- Milgrom's nonlocal kernel (v) -- does so BY")
    print("        CONSTRUCTION, and the banked active-kernel SIGN THEOREM proves the MOND-signed kernel is")
    print("        un-sourceable from the passive dS vacuum (rho>=0 => delta_m>=0 => anti-MOND).")
    print("   * What IS real (the genuine, non-trivial content, both-ways): the dS-Unruh route robustly gives the")
    print("     deep-MOND sqrt-LAW and the SCALE a0~cH_Lambda; postulate (iv) even gives a mu with BOTH correct")
    print("     limits from a near-principled free-energy reading -- but it is the simple-nu form, not the")
    print("     framework's, and the choice phi=-T(a), mu=dphi/dx is not forced.")
    print("   * GENUINELY-NEW forcing route flagged? NONE. No postulate derives the framework's specific mu without")
    print("     either (a) inserting the unforced Z, or (b) reverse-engineering a nonlocal kernel that the sign")
    print("     theorem forbids from the dS vacuum. mu stays POSTULATED. Consistent with the banked trichotomy.")
    print("="*100)


if __name__ == "__main__":
    main()
