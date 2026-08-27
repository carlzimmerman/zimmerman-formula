#!/usr/bin/env python3
r"""CMYG decisive test: matter couples to composite g~ = e^{2 alpha q} g (alpha=beta conformal case).
Q: does the q-sector (which supplies MOND dynamics) also bend light?
"""
import sympy as sp
print("="*78); print("CMYG (alpha=beta): the conformal-invariance dichotomy"); print("="*78)
print(r"""
SETUP: g~_munu = e^{2 alpha q} g_munu.  Matter (massive + photons) follows g~ geodesics.
  Massive particles: timelike geodesics of g~ are NOT those of g.
     Weak field: extra acceleration a_extra = -c^2 alpha D_i q  => MOND dynamics from q.  GOOD.
  Photons: null geodesics are CONFORMALLY INVARIANT (as paths).
     ds~^2 = 0  <=>  ds^2 = 0, and the null geodesic EQUATION is invariant up to reparametrization.
     => photons follow the null geodesics of the GRAVITATIONAL metric g, blind to q.""")

print("\n"+"="*78); print("CONSEQUENCE"); print("="*78)
print(r"""  The GR sector is unmodified (H_TT = H_TT^GR, standard Einstein constraints), so g is sourced
  by BARYONS ONLY. Therefore:
        DYNAMICS  (massive):  MOND    (feels q)      <- rotation curves fit
        LENSING   (photons):  NEWTONIAN/baryonic     <- q is invisible to light
  CMYG predicts galaxies lens like their BARYONS ALONE while rotating like MOND.""")

print("\n"+"="*78); print("OBSERVATIONAL TEST"); print("="*78)
# deep-MOND: dynamical mass exceeds baryonic by factor sqrt(g_N a0)/g_N = sqrt(a0/g_N)
gN, a0 = sp.symbols('g_N a0', positive=True)
boost = sp.sqrt(a0/gN)   # ratio g_MOND/g_N in deep-MOND
print("  Deep-MOND boost g/g_N = sqrt(a0/g_N).  At g_N = a0/10:", sp.sqrt(10).evalf(4), "x")
print(r"""  Weak-lensing measurements (Brouwer+2021 KiDS; Mistele+2024 KiDS out to ~2 Mpc) find the
  LENSING radial-acceleration relation AGREES with the dynamical RAR -- light sees the same
  excess acceleration that rotation curves do, to ~Mpc scales.
  CMYG (alpha=beta) predicts lensing excess = 0 while dynamical excess = sqrt(a0/g_N) ~ 3x.
  => EXCLUDED by weak lensing. This is the classic 'conformal coupling cannot lens' result.""")

print("\n"+"="*78); print("THE ESCAPE, AND ITS COST"); print("="*78)
print(r"""  alpha != beta (DISFORMAL rather than conformal): then g~ is not conformal to g, null
  geodesics ARE modified, and light can see q. But then the photon and graviton cones split:
        c_gamma^2 / c_GW^2 - 1 ~ O(exp(2(alpha-beta)q)) - 1
  Lensing-sized q requires (alpha-beta)q = O(1) at galactic scales, while GW170817 bounds
  |c_gamma/c_GW - 1| <= 2e-15. This is EXACTLY the Gate-2 disformal no-go already committed
  (theory_2026/york/gate2_cone_gw170817_2026.py, gate2_lensing_2026.py): the gap-closing
  disformal is non-local AND cone-splitting, {2+0} n {lensing} n {luminal} = empty.

  So CMYG faces a strict dichotomy:
        alpha =  beta  -> conformal -> MOND dynamics but NO lensing  -> excluded by KiDS
        alpha != beta  -> disformal -> lensing possible but cone split -> excluded by GW170817
""")
print("="*78)
print("CMYG VERDICT: FAIL (dichotomy). Both branches already have committed kills.")
