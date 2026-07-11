# LANE 1 -- Pure-MI Lensing Impossibility Theorem (notes)

Script: `lane1_theorem.py` (exit 0, all three teeth PASS). Framework-first; verified the
"impossible" verdict as hard as a "works" one (memory rule). This is a THEOREM, not a
failed-search-dressed-as-proof: it turns on the framework's OWN proven property `||K||<=1`.

## The claim tested
Can `[GR host S_EH[g] UNMODIFIED] + [MOND confined to the matter INERTIA sector] +
[ONE metric g -> photons & gravitons share the null cone (GW170817)] + [the verified galaxy
RAR g_obs = sqrt(g_bar^2 + g_bar a0)]` bend light by the FULL nu-enhancement with NO extra
source (medium/DM) and NO second cone / gravity modification? Answer: **NO -- impossible.**

## The theorem (statement)
Under (H1) unmodified GR host + one Levi-Civita connection of one metric g; (H2) photons and
gravitons on the same cone; (H3) MOND only in the matter/inertia sector via a bounded form
factor (`||K||<=1`) with a genuinely modified worldline response; (H4) the framework RAR:
**the lensing is Newtonian (sourced by the BARYONIC T_00 = rho_bar); light is under-deflected
by exactly nu relative to the observed dynamics.** Correct nu-enhanced lensing is impossible
under (H1)-(H4).

## Proof -- three independent teeth
- **T1 (geometry).** One metric + no gravitational slip (the MI stress tensor is fluid-like,
  `A u u + B g`, isotropic in the rest frame -> anisotropic stress = 0 -> Psi = Phi). Then the
  lensing potential (Phi+Psi)/2 = Phi = the dynamical potential; light and massive bodies feel
  ONE potential sourced by ONE T_00. Any nu-enhancement must therefore live in T_00 itself.
  (Decoupling light from dynamics needs a second cone = the dead disformal route, excluded by H2.)
- **T2 (double-count, RAR-forced).** The RAR is reproduced by EXACTLY ONE of
  `{baryonic metric + modified inertia}` XOR `{enhanced metric + standard inertia}`. Inverting
  the framework inertia law `A(a)=(sqrt(a0^2+4a^2)-a0)/2`, the "put the enhancement in BOTH"
  branch solves `A(a_both)=g_obs` and gives `a_both = nu(g_obs)*g_obs > g_obs` -- it
  OVER-predicts the RAR by the factor nu(g_obs) at every radius (numerically 1.14->2.35 over
  5->40 kpc). So genuine MI (H3, modified worldline) forces the BARYONIC-metric branch ->
  T_00 = rho_bar -> Newtonian lensing. Restoring correct lensing forces mu->1 (worldline
  trivializes) = MODIFIED GRAVITY, not modified inertia.
- **T3 (magnitude/boundedness).** `Q = <u|K(Box_u)|u>`, and `||K||<=1` (Herglotz-Nevanlinna /
  Loewner, proven in `operator_definition.py`) gives `|Q| <= 1`, so `|L_matter| <= (1/2)rho_m`:
  the MI matter Lagrangian -- hence T_00 -- is BOUNDED by the baryonic rest-mass scale. A bounded
  form factor on the baryons cannot manufacture `T_00 = nu*rho_bar > rho_bar`. The actual MI
  internal-energy correction is `O(a0 r/c^2) ~ |Phi| ~ 1e-6`, while correct lensing needs the
  O(1) fraction `(nu-1)`; the shortfall is ~1e6 (matches the banked source-side fork "MI
  stress-energy ~1e7 too weak").

## The exhaustive escape fork (contrapositive)
To lens by the full nu without dark matter you must break exactly one hypothesis, and each
break is a KNOWN route -- there is no fourth door inside "matter-sector-only, one cone, GR host":
- **(a) break H3 upward** = add gravitating stress-energy `T_00 -> nu*rho_bar` tracking the
  baryons = a MEDIUM / dark component. This is the framework's OWN **Branch B (elastic
  dark-ENERGY, not dark matter)**, or a ghost condensate. Sources lensing; costs a Cassini bill.
- **(b) break H1** = enhance the metric via a modified-GRAVITY source (nonlocal-metric MOND,
  Deffayet-Esposito-Farese-Woodard; or TeVeS/AeST vector). But then mu->1: modified GRAVITY.
- **(c) break H2** = a second cone / disformal photon metric `g~ = g + B u u` -- DEAD by
  GW170817 (photon-vs-graviton speed, ~6-7 orders; banked `mi_disformal_gw170817_TENSION.py`).

## Why the flagged loopholes are closed (not hand-waved)
- **"nonlocal mechanism threads it":** K(Box_u) is a BOUNDED operator (`||K||<=1`). Nonlocality
  cannot AMPLIFY the bounded matter energy into an O(nu) enhancement -- boundedness IS the wall.
  (Derivative-of-K terms in T_munu carry `delta(Box_u) ~ grad Phi`, i.e. O(Phi), not O(1); a0 is
  the only new scale and `a0 r << c^2`, so no O(1) fractional energy correction can appear.)
- **"connection-level mechanism":** photons follow null geodesics of the Levi-Civita connection
  of the SAME g. A different connection (Palatini/torsion) = modifying gravity (horn b); a
  different cone = a second metric (horn c). Neither is matter-sector-only MI.
- **passive-frame stress `T_munu[u]`:** tied to H_Lambda (cosmological), not local baryons; it
  cannot scale with `rho_bar(r)` to build a galaxy-shaped nu-halo (banked "bath ~127 orders short").
- **full nonlinearity (the literature's caveat):** nonlinearity changes how T_00 depends on
  rho_bar but cannot break `T_00 <= O(rho_bar)`; nonlinear structure that DOES enhance lensing
  lives in a field equation / extra field's stress = horn (a) or (b).

## Literature grounding (all consistent with the theorem)
- Milgrom, "MOND -- particularly as modified inertia" (arXiv:1111.1611) and Scholarpedia:
  modified inertia MUST be nonlocal; the modification lives in the massive-body equation of
  motion; the gravity sector is standard.
- Wikipedia/MOND reviews: relativistic MOND "struggles to explain gravitational lensing";
  viable lensing suggests "modification should be in the gravitational sector rather than the
  dynamical one" -- i.e. horn (b), exactly the theorem's fork.
- Bekenstein-Sanders / TeVeS / AeST: correct MOND lensing is delivered by EXTRA fields
  (scalar/vector) whose stress-energy sources the deflection = horn (a)/(b), never pure
  matter-sector MI. Deffayet-Esposito-Farese-Woodard nonlocal-METRIC MOND (arXiv:1405.0393) is
  a pure modified-GRAVITY construction = horn (b).

## Bottom line
Pure single-cone matter-sector modified inertia lenses **Newtonian** (under-lenses by nu). This
is a real obstruction forced by `||K||<=1` + the RAR + one cone + an unmodified GR host -- NOT a
manufactured deficit. It does NOT say "the framework needs dark matter": it says dark-matter-free
correct lensing REQUIRES a MEDIUM, and the framework's own **Branch B (elastic dark energy)** is
precisely that forced medium (horn a). "No dark matter" survives; "pure MI, no medium" does not.
