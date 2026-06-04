#!/usr/bin/env python3
"""
DOOR F -- is a0 a de Sitter stretched-horizon COMPLEXITY / emergence rate, or slogan?
=====================================================================================
The repo already established two things (desitter_complexity_sign.py, complexity_mond_source_hypothesis.py):
  - a0 ~ cH is Buckingham-pi FORCED for any de Sitter-scale mechanism (only the O(1) differs);
  - at leading order de Sitter complexity TRACKS entropy: dC/dt prop S_dS.
What was NEVER done there, and is the actual Door-F question (item 2), is the DECISIVE NUMBER:
  take the 2025 literature complexity growth rate dC/dtau ~ (O(1)) S_dS T_dS, convert it to an
  acceleration, and ask QUANTITATIVELY:
    (Q1) does the complexity RATE land anywhere near a0, or near cH, or somewhere else entirely?
    (Q2) does any complexity-rate quantity reproduce the sqrt(S_dS) SUPPRESSION in
         a0 = a_Planck * (sqrt(pi)/Z) / sqrt(S_dS)  -- i.e. the UV/IR bridge -- or not?
    (Q3) is "geometry unfolding = complexity growth" CALCULABLE/falsifiable, or thematic only?

Literature anchors (verified June 2026):
  * Narovlansky-Verlinde, "Double-scaled SYK and de Sitter Holography", arXiv:2310.16994
        R_dS^2/G = 4 pi N / p^2 ; DSSYK is the candidate microscopic dual of the dS static patch.
  * "De Sitter Complexity Grows Linearly in the Static Patch", arXiv:2508.10093 (2025), eq.(19):
        dC/dtau = [ 8 pi ((d-1)/d)^((d-1)/2) / ( sqrt(d) * arccos(sqrt((d-1)/d)) ) ] * S * T
        i.e. LINEAR growth, rate = (pure number depending on dim) x (entropy x temperature).
        This CORRECTS Susskind's original 'hyperfast' (divergent) growth.
  * "dS holographic complexity from Krylov complexity in DSSYK", arXiv:2510.13986 (2025):
        late-time Krylov-complexity growth rate prop temperature x entropy of dS (independent confirmation).
  * Lloyd / Brown-Susskind bound context: dC/dt <= 2E/(pi hbar); for a thermal system the late-time
        rate is ~ T S (this is the AdS-BH statement these dS papers port over).

Everything below is arithmetic on those formulae + the framework's own a0. numpy only.
Labels: [ESTABLISHED]=textbook/lit; [DERIVED]=arithmetic here; [HYPOTHESIS-TEST]=the Door-F claim under test.
"""
import numpy as np

# ---- constants (SI) ----
c     = 2.99792458e8
G     = 6.674e-11
hbar  = 1.054571817e-34
kB    = 1.380649e-23
Mpc   = 3.0856775815e22
H0    = 67.4e3 / Mpc                      # Planck 2018, s^-1
lP    = np.sqrt(G*hbar/c**3)              # Planck length
tP    = lP / c                            # Planck time
aP    = c**2 / lP                         # Planck acceleration = c^2/lP
Z     = 2*np.sqrt(8*np.pi/3)              # framework coefficient 5.789
a0_obs= 1.2e-10                           # observed MOND scale
a0_fw = c*H0/Z                            # framework a0 = cH/Z


def banner(s): print("="*94); print(s); print("="*94)


# ---------------------------------------------------------------------------------------------
def part0_de_sitter_scales():
    banner("PART 0 [ESTABLISHED] -- the de Sitter static-patch numbers everything is built from")
    R   = c/H0                                  # de Sitter (Hubble) radius
    A   = 4*np.pi*R**2
    S   = A/(4*lP**2)                           # Gibbons-Hawking entropy (dimensionless, nats)
    T   = hbar*H0/(2*np.pi*kB)                  # Gibbons-Hawking temperature (K)
    kT  = kB*T                                  # thermal energy (J)
    print(f"  R_dS = c/H0              = {R:.4e} m")
    print(f"  S_dS = A/4lP^2           = {S:.4e}   (~10^122, dimensionless)")
    print(f"  T_GH = hbar H0 / 2pi kB  = {T:.4e} K   (kB T = {kT:.4e} J)")
    print(f"  a_Planck = c^2/lP        = {aP:.4e} m/s^2")
    print(f"  cH0 (horizon surf grav)  = {c*H0:.4e} m/s^2")
    print(f"  a0 (framework cH/Z)      = {a0_fw:.4e} m/s^2 ; observed {a0_obs:.2e}")
    # cross-check the boxed identity a0 = aP*(sqrt(pi)/Z)/sqrt(S)
    a0_from_S = aP*(np.sqrt(np.pi)/Z)/np.sqrt(S)
    print(f"\n  [DERIVED] cross-check  a0 = a_Planck*(sqrt(pi)/Z)/sqrt(S_dS) = {a0_from_S:.4e} m/s^2")
    print(f"           vs cH/Z = {a0_fw:.4e}  -> ratio {a0_from_S/a0_fw:.6f}  (identity holds)")
    print("""
  KEY STRUCTURE to keep in mind for Door F: a0 carries a sqrt(S_dS) ~ 10^61 SUPPRESSION below the
  Planck acceleration. ANY claim that 'a0 = a complexity rate' must reproduce a 10^61 suppression,
  not just land in the right ballpark by dimensional luck. That is the quantitative test below.\n""")
    return R, S, T, kT


# ---------------------------------------------------------------------------------------------
def part1_complexity_rate_number(R, S, T, kT):
    banner("PART 1 [DERIVED] -- the ACTUAL de Sitter complexity growth rate, as a number")
    # 2508.10093 eq.(19) prefactor for d spatial-ish index. dS_{d+1}; our universe dS_4 => d=3.
    def kappa(d):
        return 8*np.pi*((d-1)/d)**((d-1)/2) / (np.sqrt(d)*np.arccos(np.sqrt((d-1)/d)))
    d = 3
    k = kappa(d)
    print(f"  Lit formula (2508.10093 eq.19):  dC/dtau = kappa(d) * S * T ,  kappa(3) = {k:.4f}")
    print(f"  (sanity: kappa(2)={kappa(2):.3f}, kappa(3)={kappa(3):.3f}, kappa(4)={kappa(4):.3f}; all O(1)-O(10))")

    # dC/dtau is computational rate. Two honest normalizations of 'rate':
    #  (a) DIMENSIONLESS-GATES form: C is a pure number, tau a TIME, so dC/dtau has units 1/s.
    #      Lloyd/thermal:  (dC/dt)  ~  S * (kB T / hbar)  = S * (k_B T)/hbar    [gates per second]
    #  (b) if instead one (as some authors) measures complexity-time in units where the rate has the
    #      'energy' reading 2E/(pi hbar) with E ~ S kB T (thermal energy of the horizon dof).
    rate_gates_per_s = S * (kT/hbar)                 # using kappa~O(1) dropped to expose the SCALE
    rate_with_kappa  = k * S * (kT/hbar)
    print(f"\n  [DERIVED] de Sitter complexity rate (gates/sec):")
    print(f"     dC/dt ~ S * kB T / hbar            = {rate_gates_per_s:.4e}  s^-1")
    print(f"     dC/dt = kappa(3) * S * kB T / hbar = {rate_with_kappa:.4e}  s^-1")
    # Compare to the bare Hubble rate and to a 'naive S * H'
    print(f"     for comparison:  H0 = {H0:.4e} s^-1 ;   S*H0 = {S*H0:.4e} s^-1")
    print(f"     note  kB T_GH/hbar = {kT/hbar:.4e} s^-1  ~  H0/2pi = {H0/(2*np.pi):.4e} s^-1 (GH temp IS ~H)")
    print("""
  [DERIVED -- the first decisive fact] The de Sitter Gibbons-Hawking temperature gives
  kB T_GH/hbar = H0/2pi.  So the 'thermal clock' of the horizon ticks at the HUBBLE rate, and the
  complexity rate is  dC/dt ~ S_dS * H0  (up to 2pi and kappa). The complexity grows at  ~ S * H,
  NOT at H. This is the central number for Door F.\n""")
    return k, rate_with_kappa, S*H0


# ---------------------------------------------------------------------------------------------
def part2_turn_the_rate_into_an_acceleration(k, S, T, kT, R):
    banner("PART 2 [HYPOTHESIS-TEST] -- can the complexity RATE be read as a0 (or cH)? the numbers")
    H = H0
    # A 'rate' (1/s) is not an acceleration (m/s^2). To compare to a0 you must multiply by a velocity
    # or divide a length appropriately. Enumerate the *only* dimensionally-allowed bridges and show
    # WHERE each lands. This is the honest 'does any complexity quantity = a0' scan.
    print("  A complexity RATE has units 1/s; a0 has units m/s^2. The dimensionally allowed bridges,")
    print("  built ONLY from {c, H, R=c/H, S}, and where each one lands (target: a0=%.2e):\n"%a0_obs)

    candidates = {
        "c * H                         (surface gravity; the KNOWN a0 scale)": c*H,
        "c * (dC/dt)/S    = c*H/2pi    (rate per dof x c)":                    c*(k*S*(kT/hbar))/S,  # ~ c*kT/hbar
        "c * (dC/dt)      = c*S*H*k    (full rate x c)":                       c*(k*S*(kT/hbar)),
        "(dC/dt)/S * c    again-per-dof":                                      c*(kT/hbar),
        "c^2/R * 1        = cH         (curvature x c^2)":                     c**2/R,
        "a_Planck/sqrt(S) = c^2/(lP sqrt(S))   (UV/IR bridge, NO complexity)": (c**2/lP)/np.sqrt(S),
        "a_Planck/S       = c^2/(lP S)         (full entropy suppression)":    (c**2/lP)/S,
    }
    for name, val in candidates.items():
        ratio = val/a0_obs
        flag = "  <-- ~ a0" if 0.05 < ratio < 20 else ("  (off by %+.0f dex)"%np.log10(ratio) if ratio>0 else "")
        print(f"    {name:<58} = {val:.3e} m/s^2{flag}")
    print(f"""
  [DERIVED -- the decisive result for Q1/Q2]
   * The ONLY combinations that land on a0 are 'c*H'-type (surface gravity) and the UV/IR bridge
     a_Planck/sqrt(S_dS). BOTH are ENTROPY/geometry quantities -- a0=cH/Z and a0=aP/sqrt(S) are the
     SAME statement (S=pi R^2/lP^2). NEITHER contains the complexity RATE dC/dt.
   * The complexity RATE itself, c*(dC/dt) ~ c S H, is ~10^122 LARGER than a0 (it carries the FULL
     factor S_dS, not sqrt(S_dS)). Per-degree-of-freedom, c*(dC/dt)/S = c*kB T/hbar ~ c*H/2pi -- which
     is again just the cH surface-gravity scale, with the complexity content (the factor S) DIVIDED
     BACK OUT. So 'rate per dof' = cH is a restatement of Gibbons-Hawking, not a complexity result.
   * CRUCIAL MISMATCH OF EXPONENTS: a0 = aP * sqrt(pi)/Z / S_dS^(1/2)  (suppression power 1/2).
     The complexity rate scales as S_dS^(+1)  (rate ~ S H). There is NO power of the complexity rate
     equal to S^(-1/2): you cannot get S^(-1/2) by taking c-and-R powers of a quantity ~ S^(+1)
     without re-inserting the Planck length by hand. So the sqrt(S_dS) suppression in a0 is NOT
     reproduced by any complexity-rate quantity. It comes from the AREA/entropy (a0 ~ c^2/R, and
     R ~ lP sqrt(S)), i.e. from holographic GEOMETRY, with complexity playing no role in the power.\n""")


# ---------------------------------------------------------------------------------------------
def part3_what_complexity_does_and_does_not_fix(S, T):
    banner("PART 3 [ESTABLISHED] -- what the complexity program genuinely gives, vs what it doesn't")
    print("""  GENUINELY ESTABLISHED (real research, not slogan):
   * dS static patch  ==  finite-dim quantum system on the stretched horizon, dim ~ e^{S_dS}
     (Banks-Fischler; CLPW Type II_1 algebra 2023).  [the framework's true home -- Door A]
   * DSSYK reproduces dS_3 correlators with R_dS^2/G = 4 pi N/p^2 (Narovlansky-Verlinde 2023):
     the FIRST solvable, calculable 'gravity from the dS horizon'. This is a real ally.
   * dS complexity grows LINEARLY at late times, rate = (O(1)) x S x T  (2508.10093, 2510.13986),
     CORRECTING Susskind's original 'hyperfast' growth. The rate is fixed by entropy x temperature.

  CONJECTURAL / SLOGAN (must be flagged):
   * 'time = complexity' : the bulk time of the static patch = boundary complexity. Evocative; the
     ONE solid instance is black-hole interior VOLUME growing linearly = complexity (AdS, well-tested).
     For dS it is a 2023-2026 conjecture, not a theorem.
   * 'Complexity = Anything' (Belin-Myers-Ruan-Sarosi-Speranza; Aguilar-Gutierrez et al for dS):
     the complexity DUAL IS NON-UNIQUE -- an infinite class of bulk observables all 'grow linearly &
     show the switchback effect', so no single C is privileged. Hence any number you extract from
     'the' complexity is convention-dependent at the O(1) level -- exactly the level a0=cH/Z lives at.
   * dS holography itself is contested (Rahman-Susskind dispute Narovlansky-Verlinde's reading).

  CONSEQUENCE for 'a0 = complexity rate':
   * The SCALE a0~cH is forced by de Sitter dimensional analysis (Part 2) -- complexity, entropy, and
     surface gravity ALL give it; complexity adds nothing to the scale.
   * The COEFFICIENT Z=5.789 sits exactly at the 'Complexity=Anything' convention-ambiguity level, so
     complexity cannot pin it (consistent with the repo's number-field no-go for Z).
   * The sqrt(S_dS) SUPPRESSION -- the one genuinely striking thing in a0 -- is a GEOMETRY (area-law)
     fact, scaling as S^(-1/2); the complexity rate scales as S^(+1). Opposite role of S. No match.\n""")


# ---------------------------------------------------------------------------------------------
def part4_is_there_anything_calculable(S):
    banner("PART 4 [HYPOTHESIS-TEST] -- does 'geometry unfolding = complexity' give anything FALSIFIABLE?")
    print("""  Three honest buckets:

  (A) CALCULABLE & already a real program (NOT 'a0=rate', but adjacent and on-mission):
      In DSSYK the static-patch spectrum IS the horizon spectrum (q-Hermite chord DOS, flat at E=0).
      The repo's own DSSYK_DEEPMOND_PROBLEM.md reduced the deep-MOND SIGN to two literature-defined
      chord calculations. That is calculable and falsifiable IN PRINCIPLE -- but it is the
      ENTROPY/DOS route (which dof freeze), NOT the complexity-RATE route. Complexity growth (dC/dt)
      does not enter those calculations.

  (B) NOT calculable as stated ('a0 = complexity emergence rate'): there is no equation in the
      literature, and none constructible here, that outputs a0 FROM a complexity rate. Every attempt
      (Part 2) either reproduces cH (surface gravity, no complexity) or overshoots by S_dS. The
      'emergence rate' framing yields a number ~10^122 too large unless you divide by S -- which just
      returns you to the surface-gravity scale. So as a DERIVATION of a0 it is empty.

  (C) THEMATIC ONLY (the honest home of Carl's intuition): 'geometry unfolds' <-> 'complexity grows'
      is a genuine, beautiful correspondence for the EMERGENCE OF TIME / the static-patch geometry from
      a boundary quantum system. It tells you the dS interior is a chaotic finite quantum computer whose
      'clock' ticks at ~ S*H (Part 1). It does NOT tell you a0. It is inspiration + a real research
      neighborhood (DSSYK), not a calculation of the MOND scale.

  FALSIFIABILITY CHECK: a claim is falsifiable if it forbids something. 'a0 = complexity rate' forbids
  nothing a0=cH/Z doesn't already (same scale). It makes no NEW numerical prediction (no new power of
  S, no fixed coefficient). The DSSYK deep-MOND-sign program (bucket A) IS falsifiable (the chord
  overlap w(0) is either nonzero -> MOND, or zero -> not), but that is the ENTROPY route, not 'a0=rate'.\n""")


# ---------------------------------------------------------------------------------------------
def verdict():
    banner("DOOR F -- BRUTALLY HONEST VERDICT")
    print("""  REAL RESEARCH DIRECTION (the neighborhood): YES.
     dS-static-patch = finite quantum system, and DSSYK<->dS, is where 'gravity from the de Sitter
     horizon' is genuinely being made quantitative right now (Narovlansky-Verlinde 2023; CLPW II_1).
     The framework LIVES in this neighborhood. That is a true ally for the PROGRAM (Door A).

  'a0 = de Sitter complexity / emergence rate' SPECIFICALLY: NO -- it is a slogan, not a calculation.
     1. The complexity growth rate is now KNOWN (2025): dC/dt = O(1) x S_dS x T_GH ~ S_dS x H. It
        scales as S^(+1) and, as an acceleration (c x dC/dt), overshoots a0 by ~10^122. Divide out S
        to 'fix' it and you are back at cH -- pure Gibbons-Hawking surface gravity, no complexity left.
     2. a0's signature feature, the sqrt(S_dS) ~ 10^61 SUPPRESSION below a_Planck, scales as S^(-1/2)
        and is an AREA-LAW/holographic-GEOMETRY fact (a0 ~ c^2/R, R ~ lP sqrt(S)). Complexity (S^+1)
        has the WRONG, opposite power of S. No complexity-rate quantity reproduces it.
     3. The dual is non-unique ('Complexity = Anything'), so even the O(1) is convention-ambiguous --
        exactly where Z=5.789 sits; complexity cannot pin Z.
     => 'geometry unfolding = complexity growth' is EVOCATIVE ANALOGY for emergent time, with one solid
        instance (BH interior volume) and a lot of dS conjecture. It gives the framework NOTHING new
        that is calculable or falsifiable about a0. The calculable, on-mission DSSYK work is the
        ENTROPY/DOS (deep-MOND-sign) route, where the complexity RATE does not appear.

  ONE-LINE: real research NEIGHBORHOOD (DSSYK<->dS), but 'a0 = complexity rate' is a slogan -- the
  measured complexity rate is ~S_dS x H (overshoots a0 by ~10^122, wrong power of S), and a0's
  sqrt(S_dS) suppression is holographic GEOMETRY, not complexity dynamics.""")
    print("="*94)


def main():
    print("#"*94)
    print("# DOOR F: is a0 a de Sitter complexity/emergence RATE, or is 'geometry unfolding' a slogan?")
    print("#"*94 + "\n")
    R, S, T, kT = part0_de_sitter_scales()
    k, rate, SH = part1_complexity_rate_number(R, S, T, kT)
    part2_turn_the_rate_into_an_acceleration(k, S, T, kT, R)
    part3_what_complexity_does_and_does_not_fix(S, T)
    part4_is_there_anything_calculable(S)
    verdict()


if __name__ == "__main__":
    main()
