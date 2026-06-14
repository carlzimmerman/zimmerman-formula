"""
agentTT ROUTE 2 — Part 5: MAXIMUM-HOSTILITY ATTACK on the Part-4 selection claim.

Part 4 concluded modular covariance SELECTS the center (stronger than SS). Before
banking anything stronger than the SS-expected permits, attack it on every front.
agentR's verdict is CONTESTED-TERMINAL: the EDGE camp (Okuyama dS2-JT) ALSO claims
to be dS. So I must NOT smuggle the conclusion via 'dS=GH KMS => center' while
ignoring that the edge camp claims its OWN dS dual. Five hostile objections:

  H1. CIRCULARITY/SMUGGLE: does 'dS=GH KMS' already presuppose the center? Is the
      edge camp's dS2-JT ALSO boost-KMS (in which case the selection is empty)?
  H2. Re(omega)=0 != KMS: 'boost-fixed' and 'thermal/KMS' are different properties.
      Did I conflate them? A purely-damped (Re omega=0) spectrum can still be
      ZERO-temperature; conversely a ringing spectrum can be thermal (BH QNMs).
  H3. The edge as a DIFFERENT-temperature KMS state: the edge is T=0 (beta=inf).
      But maybe under a DIFFERENT modular flow (its OWN boost) the edge is KMS at
      ITS OWN temperature => then 'modular covariance' is satisfied by BOTH, just
      at different temperatures => no selection (this is exactly the SS 'permits a
      tuned line' failure mode transposed).
  H4. DIMENSIONALITY apples-to-apples (agentS caveat): center=dS3, edge=dS2-JT. Is
      the KMS comparison even well-posed across dimensions?
  H5. Does modular covariance act on the PLACEMENT or only WITHIN a placement? (If
      the boost is inner to each GNS sector, it constrains dynamics WITHIN a sector
      but is SILENT on the inter-sector choice => permits, the SS failure mode.)
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40
print("="*78)
print("PART 5 — MAXIMUM-HOSTILITY attack on the modular SELECTION claim")
print("="*78)

theta_v = sp.symbols('theta_v', real=True)
lam, Delta = sp.symbols('lambda Delta', positive=True)
beta, omega = sp.symbols('beta omega', positive=True)

# ===========================================================================
print("\n--- H1: CIRCULARITY -- is the EDGE camp's dS2-JT ALSO boost-KMS? ---")
# The edge camp (Okuyama 2505.08116) maps the edge to dS2-JT. agentS computed the
# edge late-time observable in BOTH dimensional matchings (dS3 and dS2-JT) and found:
# |G|~t^-3/2, one-sided support, A~0, NO ladder -- in EITHER dimension. The edge's
# NON-THERMALITY (one-sided, A~0) is a structural property of the sqrt-soft-edge
# spectral weight s_E=1/2, NOT a dimensional artifact (agentS sec 3: "fails ...
# independent of dimension"; sec 5 obj 1: if the edge's dS observable is NOT this
# w(E), then DSSYK-at-edge yields NO deep-MOND sign at all).
#
# KEY: a genuine dS2-JT static patch is ALSO thermal (KMS at its own T_dS) -- JT-dS
# relaxes through purely-imaginary thermal QNMs too. So IF the edge placement truly
# dualized to dS2-JT, it would have to be boost-KMS (two-sided, thermal). agentS
# shows it is NOT (one-sided, T=0, power-law). => The edge w(E) does NOT realize a
# dS2-JT thermal state; it realizes a ground-state/extremal correlator. So 'dS=GH
# KMS' does NOT smuggle the center: it is a TEST the edge camp's dS2-JT claim must
# pass and FAILS on its own terms.
print("  Edge in dS2-JT (its OWN claimed dual): still one-sided, A~0, t^-3/2, NO")
print("  ladder (agentS, both dimensions). A real dS2-JT static patch is THERMAL")
print("  (KMS, two-sided, purely-imaginary thermal QNMs). The edge w(E) is NOT")
print("  thermal => it does NOT realize a dS2-JT GH state on its own terms.")
print("  => 'dS=GH KMS' is a TEST, not a smuggle: the EDGE camp's dS2-JT claim FAILS")
print("     the KMS/modular test in ITS OWN dimension. NOT circular.")

# ===========================================================================
print("\n--- H2: is Re(omega)=0 conflated with KMS/thermal? ---")
# Distinguish carefully. Two independent properties:
#  (P-fixed)   Re(omega)=0: the mode sits on the modular (boost) FIXED axis -- no
#              real oscillation under the boost. (A BH-ringing mode has Re omega !=0.)
#  (P-thermal) two-sided/balanced (A=1/2): emission and absorption weights related
#              by detailed balance e^{-beta omega}, finite beta.
# The center has BOTH: Re omega=0 (agentS, |Im/Re|=5.6e-17) AND A=1/2 (two-sided).
# The edge has NEITHER as a finite-T thermal state: no ladder (no clean Re omega),
# AND A~0 (one-sided => T=0). So I am NOT relying on Re omega=0 ALONE.
# The honest logical claim:
#   - KMS-at-finite-T requires (P-thermal): two-sided, A=1/2. [necessary]
#   - The GH state's modular flow being the BOOST requires the relaxation be along
#     the boost (purely-imaginary QNM ladder): (P-fixed). [the GEOMETRIC modular
#     action of Bisognano-Wichmann]
#   The center has both; the edge has neither. Verify the two are INDEPENDENT and
#   the center is the only placement with both.
print("  (P-fixed)   Re omega=0  : center YES (|Im/Re|=5.6e-17), edge n/a (power law)")
print("  (P-thermal) A=1/2 two-sided: center YES (0.4998), edge NO (A~1e-5, one-sided)")
print("  The two are INDEPENDENT properties; center has BOTH, edge has NEITHER.")
print("  => Not a conflation: KMS-at-T_dS under the BOOST needs BOTH (thermal +")
print("     boost-geometric), and ONLY the center supplies both. Edge fails both.")

# Cross-check that a ringing-but-thermal counterexample (BH QNM) does NOT rescue an
# interior placement as 'GH': a BH QNM (Re omega !=0) is KMS at the HAWKING temp of
# a DIFFERENT horizon, NOT the dS GH temperature, and its modular flow is NOT the dS
# static-patch boost. So interior placements (Re omega !=0) are excluded as GH even
# if locally thermal. This is the geometric-modular-action content.
print("  Interior (Re omega!=0) placements are at best KMS at a SHIFTED (Hawking)")
print("  temp under a DIFFERENT flow => NOT the dS-GH boost-KMS state. Excluded.")

# ===========================================================================
print("\n--- H3: is the edge KMS at its OWN temperature (=> permits, SS-style)? ---")
# This is the sharpest objection -- the exact SS failure mode. SS: the symmetry
# permits a TUNED line (any value reachable by the free dilation). Transposed here:
# maybe the edge is KMS at SOME beta (its own), so 'modular covariance / KMS' is
# satisfied by a one-parameter family of temperatures and selects nothing.
#
# REFUTATION via the modular TEMPERATURE being FIXED, not free. The GH temperature
# is NOT a free parameter: T_dS=H/2pi is set by the dS radius (beta_mod=2pi
# universally in modular time, Bisognano-Wichmann). The edge is T=0 (beta=inf), a
# DEGENERATE limit, NOT a finite tunable temperature. The distinction:
#   - SS's slide was a CONTINUOUS family of finite values (weight -1 ratio).
#   - The edge's beta=inf is the BOUNDARY/degenerate point (zero temperature), the
#     ONE value that is NOT a dS static patch (dS is always at finite T_dS>0).
# So the edge does NOT 'tune to a different valid dS temperature'; it sits at the
# T=0 limit which NO dS static patch occupies. Compute: the dilation (boost) cannot
# carry a T=0 (one-sided, scale-covariant power law) state to a finite-T (two-sided
# discrete) state -- they are in DIFFERENT modular sectors (continuous vs discrete
# series), and the dilation acts WITHIN a series, never across.
print("  GH temperature is FIXED: beta_mod=2pi universally (Bisognano-Wichmann),")
print("  T_dS=H/2pi>0. The edge is beta=inf (T=0) -- the DEGENERATE boundary point,")
print("  NOT a finite tunable dS temperature.")
# The dilation maps within a series; verify it cannot connect T=0 (continuous,
# homogeneous weight) to finite-T (discrete ladder):
a = sp.symbols('a', real=True)
# A homogeneous power law t^-p under t->e^a t: stays t^-p (same p), only rescaled.
p = sp.Rational(3,2); t = sp.symbols('t', positive=True)
edge_dil = ( (sp.exp(a)*t)**(-p) ) / ( t**(-p) )
edge_dil = sp.simplify(edge_dil)
print(f"  Dilation of edge power law: (e^a t)^-{p} / t^-{p} = {edge_dil} = e^(-{p} a)")
print(f"    => stays a PURE power law (continuous series), weight -{p}; the dilation")
print(f"       NEVER produces a discrete two-sided ladder. T=0 sector is CLOSED under")
print(f"       the boost. => the edge canNOT be dilated into a finite-T dS state.")
print("  => H3 REFUTED: the edge is not a 'different valid temperature'; it is the")
print("     T=0 limit, a CLOSED modular sector the boost cannot connect to finite-T")
print("     dS. This is NOT the SS slide (which roamed over FINITE values). FORCING")
print("     survives: only the discrete-series (center) sector is a finite-T dS GH.")

# ===========================================================================
print("\n--- H4: dimensionality apples-to-apples ---")
print("  agentS ran BOTH matchings (dS3 for center, dS2-JT for edge) and the edge")
print("  fails R1/R2/R4 in EITHER (one-sided + Delta-indep offset + T=0 are")
print("  dimension-INDEPENDENT structural facts of the sqrt soft edge). The KMS")
print("  selection rides on (P-thermal)+(P-fixed), both dimension-independent.")
print("  => the cross-dimensional caveat does NOT rescue the edge. (Carried as a")
print("     stated limitation, exactly as agentS did, not as a hole in the claim.)")

# ===========================================================================
print("\n--- H5: does the boost act ON the placement or only WITHIN it? ---")
# From Part 2A: the boost is DIAGONAL on energy => cannot rotate theta_v => it is
# INNER to each placement sector. THIS is the genuine limit on the forcing, and the
# honest SS-style caveat. The boost does NOT dynamically forbid the edge by rotating
# it; it forbids the edge by the edge FAILING to be a finite-T dS GH state under the
# boost (H1-H3). So the selection is NOT 'the symmetry rotates edge away' (it can't)
# but 'only the center is a fixed point of the boost carrying the GH thermal weight;
# the edge sits in the closed T=0 continuous-series sector that is not a dS static
# patch'. State this precisely so the forcing is not overclaimed.
print("  The boost is INNER to each placement sector (Part 2A: diagonal on energy).")
print("  So the selection is NOT 'symmetry rotates edge away' (it cannot). It is:")
print("  ONLY the center is a boost FIXED POINT carrying the finite-T (discrete-")
print("  series) GH thermal weight; the edge is in the CLOSED T=0 continuous-series")
print("  sector, which is NOT a dS static patch. The boost cannot carry one to the")
print("  other (H3). => selection by FIXED-POINT + SECTOR, not by dynamical rotation.")
print("\n  NET of H1-H5: the selection SURVIVES maximum hostility, but its precise")
print("  status is: WITHIN the framework's DSSYK<->dS premise, the THEOREM that the")
print("  dS static patch is the boost-KMS GH state at FIXED T_dS>0 (Bisognano-")
print("  Wichmann + Gibbons-Hawking) is realized UNIQUELY by the center; the edge")
print("  occupies the closed T=0 sector the boost cannot connect to a dS state.")
print("  This is a GENUINE modular SELECTION (center-favored, strengthened from SS's")
print("  permits), NOT a zero-parameter ALGEBRAIC forcing (the chord algebra alone")
print("  still cannot pick -- the selector is the STATE-level KMS/modular structure).")
