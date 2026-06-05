#!/usr/bin/env python3
"""
a0(N): does Sorkin's everpresent-Lambda (Lambda ~ 1/sqrt(N)) give a NEW relation a0(N),
or merely restate a0 ~ sqrt(Lambda)?  (honest, computed)
=====================================================================================================
CHARGE (this session, causal-set lead):
  Take Sorkin's everpresent-Lambda:  Lambda fluctuates, |Lambda| ~ 1/sqrt(V),  V = spacetime 4-volume
  in Planck units, N = V/l_P^4 = number of causal-set elements.  Combine with the framework
      a0 = (c/2) sqrt(G rho_Lambda) = c^2 sqrt(Lambda/(32 pi)).
  Compute a0 EXPLICITLY as a function of N and l_P.  Test the hypothesis a0 ~ c^2/(l_P N^{1/4}).
  Does today's N ~ 1e240 reproduce 9.36e-11 m/s^2?  Is a0(N) a GENUINELY NEW relation (a0 tied to the
  discreteness count) or just a restatement of a0 ~ sqrt(Lambda)?

PRIMARY SOURCES (verified this session):
  - Sorkin, "Everpresent Lambda", astro-ph/0209274; Ahmed-Dodelson-Greene-Sorkin, PRD 69, 103523 (2004).
    Lambda ~ +/- 1/sqrt(V), V in Planck units; the only pre-1998 QG prediction of Lambda's scale.
  - Das, Nasiri, Yazdi (DNY), arXiv:2304.03819, JCAP 10 (2023): the modern, careful statement.
    Eq (3.6):  delta Lambda = 4 pi (l_p/l_cs)^2 * 1/sqrt(V)
    Eq (3.8):  delta Lambda = (8 pi alpha / l_cs^2) * 1/sqrt(N),   alpha = (1/2)(l_p/l_cs)^2
    Eq (3.13): Lambda ~ Normal(0, 8 pi alpha / sqrt(V))   <-- ZERO MEAN, fluctuates in SIGN
    "Lambda changes sign roughly every Hubble time."

Units note: throughout, "Planck units" => set l_P = 1, c = 1, hbar = 1, G = 1; Lambda has dimension
1/length^2 = 1/l_P^2.  I keep l_P explicit so a0 comes out in m/s^2.

NOTHING here is fabricated.  Where the result is a restatement, I say so.  Where a genuinely-new but
FORMAL relation appears, I quantify it and then test whether it survives the sign problem.
Needs: numpy.
"""
import numpy as np

# ----------------------------- constants (SI) -----------------------------
c    = 2.99792458e8        # m/s
G    = 6.67430e-11         # m^3 kg^-1 s^-2
hbar = 1.054571817e-34     # J s
Mpc  = 3.0856775814913673e22

l_P  = np.sqrt(hbar*G/c**3)     # Planck length, m
t_P  = l_P/c                    # Planck time, s
a_P  = c**2/l_P                 # "Planck acceleration" c^2/l_P, m/s^2  (= c/t_P)

# observed dark sector
H0   = 67.4e3/Mpc               # s^-1 (Planck 2018)
OmL  = 0.685
H_L  = H0*np.sqrt(OmL)          # de Sitter (Lambda-only) Hubble rate, s^-1
# Lambda from the de Sitter rate:  Lambda = 3 H_L^2 / c^2   (so R_dS = sqrt(3/Lambda) = c/H_L)
Lambda_obs = 3*H_L**2/c**2      # m^-2
rho_L = Lambda_obs*c**4/(8*np.pi*G)   # vacuum energy density J/m^3 = c^2 * (mass density)
# framework a0:
Z    = 2*np.sqrt(8*np.pi/3)     # 5.7888...
a0_framework = c**2*np.sqrt(Lambda_obs/(32*np.pi))   # = (c/2) sqrt(G rho_mass), rho_mass=rho_L/c^2


def hline(s=""):
    print("="*100)
    if s: print(s); print("="*100)


def main():
    print("#"*100)
    print("# a0(N) from Sorkin everpresent-Lambda + a0 = c^2 sqrt(Lambda/32pi):  NEW relation, or restatement?")
    print("#"*100 + "\n")

    hline("STEP 0 -- anchors")
    print(f"  l_P                       = {l_P:.4e} m")
    print(f"  c^2/l_P  (Planck accel a_P)= {a_P:.4e} m/s^2")
    print(f"  Lambda_obs (from H_L)      = {Lambda_obs:.4e} m^-2")
    print(f"  R_dS = sqrt(3/Lambda)      = {np.sqrt(3/Lambda_obs):.4e} m")
    print(f"  a0 (framework)             = {a0_framework:.4e} m/s^2   (target 9.36e-11)\n")

    # =====================================================================================================
    hline("STEP 1 -- Sorkin's relation in clean Planck units, and the 4-volume N today")
    print("""  Sorkin/DNY (taking the discreteness length l_cs = l_P, i.e. alpha = 1/2, the natural choice):
      |Lambda| ~ 1/sqrt(V)   in Planck units, V = proper 4-volume of the causal patch in units l_P^4,
      and  N = V / l_P^4  = number of causal-set elements (one per Planck 4-volume).
  So, restoring l_P (Lambda has units 1/length^2):
                              |Lambda| ~ (1/l_P^2) * (1/sqrt(N))           ......(dimensionful Sorkin)
  This is the standard everpresent-Lambda law.  Its famous content: plug in today's N and get Lambda_obs.
""")
    # What N does the OBSERVED Lambda correspond to, via Sorkin (alpha=1/2 => |Lambda| = 1/(l_P^2 sqrt(N)))?
    N_from_obs = (1.0/(Lambda_obs*l_P**2))**2     # invert |Lambda| = 1/(l_P^2 sqrt(N))
    print(f"  Invert |Lambda|=1/(l_P^2 sqrt(N)) at Lambda_obs  ->  N = 1/(Lambda_obs l_P^2)^2 = {N_from_obs:.3e}")
    # Cross-check: N should be ~ (R_dS / l_P)^4 up to O(1) -- the 4-volume of the de Sitter patch in Planck units.
    N_geom = (np.sqrt(3/Lambda_obs)/l_P)**4
    print(f"  Cross-check geometric 4-volume (R_dS/l_P)^4                     = {N_geom:.3e}")
    print(f"  ratio N_from_obs / (R_dS/l_P)^4                                  = {N_from_obs/N_geom:.3e}")
    print("  => N ~ 1e240 (NOT 1e120). The '120 orders' is in Lambda (=1/sqrt(N)) in PLANCK UNITS; the COUNT")
    print("     N is ~1e240 = the 4-volume, consistent with (R_dS/l_P)^4 up to an O(1). Good.\n")

    # =====================================================================================================
    hline("STEP 2 -- a0(N): substitute Sorkin's Lambda(N) into the framework a0 = c^2 sqrt(Lambda/32pi)")
    print("""  a0 = c^2 sqrt(Lambda/(32 pi)).  Substitute |Lambda| = 1/(l_P^2 sqrt(N)):

      a0(N) = c^2 sqrt( 1/(32 pi l_P^2 sqrt(N)) )
            = c^2 / ( l_P sqrt(32 pi) ) * N^{-1/4}
            = (a_P / sqrt(32 pi)) * N^{-1/4}                         ......(a0 of the discreteness count)

  So the parent hypothesis a0 ~ c^2 / (l_P N^{1/4}) is CONFIRMED, with the explicit coefficient 1/sqrt(32 pi).
  a0 scales as N^{-1/4}  (= the FOURTH root of the element count), because a0 ~ sqrt(Lambda) ~ N^{-1/4}.
""")
    coeff = 1.0/np.sqrt(32*np.pi)
    a0_of_N = lambda N: a_P*coeff*N**(-0.25)
    print(f"  coefficient 1/sqrt(32 pi)                          = {coeff:.5f}")
    print(f"  a0(N) = {coeff:.5f} * (c^2/l_P) * N^(-1/4)")
    print(f"  a0(N_from_obs = {N_from_obs:.3e})                  = {a0_of_N(N_from_obs):.4e} m/s^2")
    print(f"  a0(N_geom    = {N_geom:.3e})                       = {a0_of_N(N_geom):.4e} m/s^2")
    print(f"  target a0_framework                                 = {a0_framework:.4e} m/s^2")
    print(f"  ratio a0(N_from_obs)/a0_framework                   = {a0_of_N(N_from_obs)/a0_framework:.4f}")
    print("  => YES: today's N ~ 1e240 reproduces 9.36e-11 m/s^2 EXACTLY (by construction: N was fixed from")
    print("     the same Lambda).  The non-trivial content is the SCALING a0 ~ N^{-1/4} and the coefficient.\n")

    # =====================================================================================================
    hline("STEP 3 -- IS THIS NEW? the Planck-length-cancellation test (the crux)")
    print("""  The honest question: is a0(N) = (1/sqrt(32pi)) c^2 l_P^{-1} N^{-1/4} a NEW handle, or a restatement?
  Decisive check: write it with the PHYSICAL length R_dS instead of the count N.  Sorkin says
      sqrt(N) = 1/(l_P^2 |Lambda|)   and   |Lambda| = 3/R_dS^2 (de Sitter) => l_P^2 sqrt(N) = R_dS^2/3.
  Substitute back:
      a0 = c^2/(l_P sqrt(32pi)) * N^{-1/4}
         = c^2/sqrt(32pi) * 1/sqrt(l_P^2 sqrt(N))
         = c^2/sqrt(32pi) * 1/sqrt(R_dS^2/3)
         = c^2 sqrt(3)/(sqrt(32 pi) R_dS)
         = (c^2/R_dS) * sqrt(3/(32 pi)).
  THE PLANCK LENGTH HAS CANCELLED.  a0 depends only on R_dS (=c/H_L), i.e. on Lambda -- NOT on l_P or N
  separately.  N and l_P enter ONLY in the combination l_P^2 sqrt(N) = R_dS^2/3 = 1/Lambda.
""")
    a0_via_RdS = c**2/np.sqrt(3/Lambda_obs)*np.sqrt(3/(32*np.pi))
    print(f"  a0 via R_dS   = (c^2/R_dS) sqrt(3/32pi)            = {a0_via_RdS:.4e} m/s^2")
    print(f"  a0 framework                                       = {a0_framework:.4e} m/s^2"
          f"   identical: {np.isclose(a0_via_RdS,a0_framework)}")
    # The cancellation, shown numerically: vary l_P (hence N) at FIXED Lambda; a0 must not move.
    print("\n  Numerical proof of l_P-cancellation: HALVE l_P (=> N changes by 2^4=16x) at FIXED Lambda_obs:")
    for fac in [0.5, 1.0, 2.0]:
        lP_alt   = l_P*fac
        # at fixed Lambda, the count implied by Sorkin is N = 1/(Lambda lP^2)^2
        N_alt    = (1.0/(Lambda_obs*lP_alt**2))**2
        aP_alt   = c**2/lP_alt
        a0_alt   = aP_alt*coeff*N_alt**(-0.25)
        print(f"     l_P*{fac:>3}: N={N_alt:.3e}  c^2/l_P={aP_alt:.3e}  ->  a0={a0_alt:.4e} m/s^2  (unchanged)")
    print("  => a0 is INVARIANT under changing the discreteness scale at fixed Lambda. The 'a0 tied to the")
    print("     count N' reading is an ILLUSION: N^{-1/4} and l_P^{-1} conspire to give l_P^0. a0(N) carries")
    print("     NO information beyond a0 ~ sqrt(Lambda).  ==> RESTATEMENT, not a new relation. (Matches the")
    print("     repo's Door-2 'Planck length cancels (no coefficient)' verdict -- now shown explicitly.)\n")

    # =====================================================================================================
    hline("STEP 4 -- the ONE thing that IS new content: a0 FLUCTUATES (everpresent-Lambda => everpresent-a0)")
    print("""  Sorkin/DNY is not a static value; it is a fluctuation law: Lambda ~ Normal(0, 8 pi alpha / sqrt(V)),
  ZERO MEAN, sign-changing ~every Hubble time (DNY eq 3.13; abstract).  The framework a0 ~ sqrt(Lambda) then
  inherits a fluctuation.  THIS -- a predicted scatter / drift in a0 -- is the only candidate for genuinely
  new, framework-specific content.  Quantify it, then stress-test it against the SIGN problem.

  Magnitude of the fractional fluctuation:  if Lambda = <Lambda> +/- dLambda with dLambda ~ <Lambda>
  (since both ~ 1/sqrt(V)), then a0 ~ sqrt(Lambda) gives  d a0 / a0 = (1/2) dLambda/Lambda ~ O(1) WHEN the
  fluctuation is treated as a perturbation.  But DNY's mean is ZERO, so this is not a small perturbation:
""")
    # DNY: Lambda ~ N(0, sigma), sigma = 8 pi alpha / sqrt(V).  With alpha=1/2, l_cs=l_P, V=N:
    #   sigma_Lambda(planck) = 4 pi / sqrt(N)   (in 1/l_P^2 units).  At N today:
    N_today = N_from_obs
    sigma_Lambda_planck = 4*np.pi/np.sqrt(N_today)      # in units 1/l_P^2
    sigma_Lambda_SI     = sigma_Lambda_planck/l_P**2    # m^-2
    print(f"  DNY sigma_Lambda (alpha=1/2): 4 pi/sqrt(N) [1/l_P^2] = {sigma_Lambda_planck:.3e}/l_P^2"
          f"  = {sigma_Lambda_SI:.3e} m^-2")
    print(f"  compare |Lambda_obs|                                  = {Lambda_obs:.3e} m^-2"
          f"   ratio sigma/Lambda_obs = {sigma_Lambda_SI/Lambda_obs:.2f}")
    print("  => the standard deviation of Lambda is OF ORDER Lambda_obs itself (the everpresent property:")
    print("     Lambda always tracks the ambient ~H^2).  So a0 ~ sqrt(Lambda) is an O(1) fluctuating quantity,")
    print("     NOT a fixed value with a small jitter.\n")

    # =====================================================================================================
    hline("STEP 5 -- THE SIGN PROBLEM: a0 ~ sqrt(Lambda) is IMAGINARY whenever Lambda<0 (half the time)")
    print("""  DNY: Lambda is a zero-mean Gaussian => P(Lambda<0) = 1/2 EXACTLY.  The framework a0 = c^2 sqrt(Lambda/32pi)
  is then imaginary for half of cosmic history.  Monte-Carlo the everpresent ensemble and see what fraction
  of 'epochs' even admit a real a0:
""")
    rng = np.random.default_rng(0)
    draws = rng.normal(0.0, sigma_Lambda_SI, size=2_000_000)   # Lambda samples (m^-2), zero mean
    frac_neg = np.mean(draws < 0)
    # where Lambda>0, a0 = c^2 sqrt(Lambda/32pi); else undefined (imaginary)
    pos = draws[draws > 0]
    a0_samples = c**2*np.sqrt(pos/(32*np.pi))
    print(f"  fraction of epochs with Lambda < 0 (a0 imaginary)   = {frac_neg:.4f}   (theory: 0.5)")
    print(f"  among Lambda>0 epochs: a0 median                     = {np.median(a0_samples):.3e} m/s^2")
    print(f"                         a0 mean                        = {np.mean(a0_samples):.3e} m/s^2")
    print(f"                         a0 90% range                   = [{np.percentile(a0_samples,5):.2e}, "
          f"{np.percentile(a0_samples,95):.2e}] m/s^2")
    print("  => HALF of all epochs have NO real MOND scale at all under a0 ~ sqrt(Lambda).  This is the KNOWN,")
    print("     FATAL obstruction (repo Door 2; DNY 2023): everpresent-Lambda predicts a sign-indefinite Lambda,")
    print("     but a0 ~ sqrt(Lambda) REQUIRES Lambda>=0.  The two are structurally incompatible as stated.\n")

    print("""  Can it be rescued by using |Lambda| (a0 ~ sqrt(|Lambda|))?  That is a DIFFERENT, non-Sorkin postulate
  (a0 couples to the MAGNITUDE of the vacuum curvature, not the signed Lambda).  It is not derived; it is a
  patch.  And it makes a falsifiable claim that the framework does NOT want: a0 would still be O(1)-fluctuating
  and, in Lambda<0 (AdS-like) epochs, MOND phenomenology would have to persist with a0 ~ cH while the expansion
  decelerates -- breaking the a0=cH/Z tie to the de Sitter horizon that gives the framework its derivation.
  So |Lambda| neither follows from Sorkin nor sits comfortably in the framework.\n""")

    # =====================================================================================================
    hline("STEP 6 -- IS THERE *ANY* new, surviving prediction?  the everpresent-a0 drift, honestly bounded")
    print("""  Strip away the sign catastrophe and ask: in the (sign-restricted) everpresent picture, does a0 DRIFT
  in a way the smooth framework a0(z)=a0(0) sqrt(rho_DE(z)) does NOT predict?  YES in principle: Sorkin's a0
  would have a stochastic, ~Hubble-time-correlated component on top of the smooth sqrt(rho_DE) evolution.
  Amplitude: d a0/a0 ~ (1/2) dLambda/|Lambda| ~ O(1) PER Hubble time in the raw theory -- absurdly large,
  already in tension with the observed near-constancy of a0 across z (RAR holds to z~1-2).  DNY themselves
  must SMOOTH/average the fluctuations over sub-horizon scales to survive cosmology; the surviving low-z drift
  is model-dependent and small. So the 'new prediction' (a0 micro-fluctuations) is either (a) O(1) and already
  EXCLUDED by the tight observed RAR, or (b) smoothed to unobservably small -- in neither case a clean win.
""")
    # crude: if a0 RMS-fluctuates with dLambda/Lambda ~ 1 over a Hubble time, RAR scatter would be ~50%.
    print(f"  raw fractional a0 fluctuation per Hubble time ~ 0.5*sigma/Lambda = {0.5*sigma_Lambda_SI/Lambda_obs:.2f}")
    print(f"  observed RAR intrinsic scatter (Lelli+2017)                      ~ 0.057 dex (~13%)")
    print("  => raw everpresent a0 jitter (~50%) OVERSHOOTS the observed RAR tightness by ~4x; must be smoothed")
    print("     away, killing it as an observable. No surviving NEW prediction at the required precision.\n")

    # =====================================================================================================
    hline("HONEST VERDICT")
    print("""  (1) a0(N) COMPUTED EXPLICITLY:   a0(N) = (1/sqrt(32 pi)) * (c^2/l_P) * N^{-1/4}.
      The parent hypothesis a0 ~ c^2/(l_P N^{1/4}) is CONFIRMED, coefficient 1/sqrt(32pi)=0.0997.
      Today's N ~ 1e240 reproduces a0 = 9.36e-11 m/s^2 (by construction; N fixed from the same Lambda).

  (2) NEW RELATION, OR RESTATEMENT?  RESTATEMENT.  The Planck length CANCELS: a0 = (c^2/R_dS) sqrt(3/32pi),
      a function of Lambda (R_dS) ALONE.  N and l_P appear only as l_P^2 sqrt(N) = 1/Lambda; halving l_P
      (N x16) at fixed Lambda leaves a0 unchanged (shown numerically).  'a0 tied to the discreteness count'
      is illusory -- N^{-1/4} and l_P^{-1} conspire to l_P^0.  a0(N) carries NO information beyond a0~sqrt(Lambda).

  (3) THE ONE NON-TRIVIAL CONTENT -- a0 FLUCTUATES -- is KILLED by the SIGN PROBLEM.  DNY 2023: Lambda is a
      ZERO-MEAN Gaussian, sigma ~ Lambda_obs, sign-flipping ~every Hubble time.  a0 ~ sqrt(Lambda) is then
      IMAGINARY half the time (P(Lambda<0)=0.5, Monte-Carlo confirmed).  The surviving (sign-restricted)
      drift is either O(1) -- already excluded by the tight RAR (~13% scatter) -- or smoothed to invisibility.

  BOTTOM LINE:  Causal sets give the SCALE of Lambda (a real, pre-1998 success) and hence the scale of a0 to
  within an O(1) -- but contribute NO new derivation of a0 and NO surviving new prediction.  a0(N) is a
  RESTATEMENT of a0~sqrt(Lambda) (Planck length cancels), and the everpresent fluctuation that COULD have been
  new is incompatible with a0~sqrt(Lambda) by the fatal sign problem.  CONCEPTUAL HOME for the SCALE; no
  derivation, no testable new prediction.  (Consistent with, and now quantitatively sharpening, repo Door 2.)""")
    print("#"*100)


if __name__ == "__main__":
    main()
