# BE1_baryon_energy_budget: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** X81 and CE1 show that cold collapse gives cusps, and that the converged native η at 10¹² sits above SPARC's
Υ-floor limit. The floor-physics doors are closed (X25, X47, X60, X65–X67, PS1/PS2). The one untested source of a
physical core scale is energy from the galaxy's own stars. Is the measured supernova energy enough to soften each
SPARC galaxy's converged-cusp core to what SPARC allows?

**This is a necessary condition only.** It tests energy, not a mechanism, and no coupling efficiency is fitted or
assumed: the required efficiency is the output.

**Halos.** X74's SPARC halos, read-only through the same exec loader as X76:
- canonical footing, background A_c2b_refit, f★ 0.034, slope 2.7774;
- M200 and R200 from the route E relation;
- smooth core ρ₀/(1+x²)^{3/2}, truncated at R200, holding M200.

**Two cores per galaxy:**
- **Σ_conv** = max(Σ_a0, η_conv(M200) Σ_coll(M200)). η_conv comes from CE1's medians (25.94 / 17.67 / 16.91 at
  10¹²/10¹³/10¹⁴), mapped through X74's own `cf_of` interpolation of the c_f-equivalent table, which is flat below 10¹².
- **Σ_target** = max(Σ_a0, η_t Σ_coll(M200)), with:
  - **primary η_t = 21.2**, the SPARC Υ-floor limit from the pre-read bracket (the minimal change);
  - **reported η_t = 10.82**, the passing c_f 4 rule.

**Energy.**
- W = −G ∫₀^R200 M(r) dM/r, by numerical integration.
- Required injection (virial): E_req = (W_target − W_conv)/2 ≥ 0. It is 0 when the collapse branch is inactive at both.
- Supernova energy: E_SN = (M★ / 100 M☉) × 10⁵¹ erg, with M★ = 0.5 L[3.6] (the Υ in route E's M_b).
  - One core-collapse SN per 100 M☉ formed, 10⁵¹ erg each. These are round IMF/explosion numbers quoted from memory,
    PROVISIONAL.
  - Taking M★ instead of the mass ever formed is conservative (it gives less energy).
- ε_req = E_req / E_SN.

**Grade** (on the galaxies where the collapse branch is active at Σ_conv; canonical headline):
- **SN ENERGETICALLY EXCLUDED:** median ε_req > 1.
- **SN ENERGY AMPLE:** median ε_req ≤ 0.01.
- **SN ENERGY SUFFICIENT IF COUPLED:** anything between. The necessary condition is met; the coupling mechanism is
  untested.
- Also reported:
  - the fraction of active galaxies with ε_req > 1;
  - ε_req against M200 (Spearman);
  - the alt footing, never pooled.

**Checks.**
- **K1:** W of an untruncated Plummer-like smooth core: numerical vs a closed form of the same integral via an
  independent quadrature, to 1e-6.
- **K2:** at η_t = η_conv, E_req = 0 exactly for every galaxy.
- **MUTATE:** E_SN × 0.01 must push the median ε_req up by exactly ×100.

**Not done here.** No feedback model, no ΛCDM simulation calibration, no fitted efficiency. If the class is SUFFICIENT IF
COUPLED, the next question is a mechanism that couples the energy to the cold dark energy core. That is a separate lane.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy
is a gravitating field component, never a particle.
