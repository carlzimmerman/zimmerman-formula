# VERIFY — MI linear cosmology first pass (adversarial re-run, 2026-07-17)

**Re-run:** `mi_growth.py` exit 0, `mi_spectra.py` exit 0. Every headline number
reproduced exactly (D-ratio 8.503/9.868, sigma8 6.896/8.003, V(35)=5508/6469,
V(100)=3337/3919, naive 4004/3112, floors 2.19→1.019 / 1108→439).

## Independent checks (all passed, exit 0)

1. **Is mu_eff genuinely self-consistent, or a smuggled fixed nu?** GENUINE.
   nu_eff varies along the trajectory (1.166 at z=200 → 3.434 at z=0 — a fixed
   nu would be constant), and re-computing nu(g_rms(D_final)/a0) from the stored
   converged D gives max|nu_re/nu_eff − 1| = 1.9e-6: a true fixed point of the
   D ↔ g_rms map, not the naive lane in disguise. The growth ODE checks out:
   mu(|a_pec|/a0)·a_pec = g_pec linearized ⇒ delta'' + (2 + dlnH/dN) delta' =
   (3/2)Ω_m(a)·nu_eff·delta, with dlnH/dN = −(3/2)Ω_m(a) for flat ΛCDM ⇒ the
   coefficient (2 − 1.5Ω_m) in the code is correct.

2. **Does self-consistency change the answer vs V_ΛCDM×nu?** YES — different
   mechanism, and it does NOT rescue the model. Naive multiplies the ΛCDM
   velocity by nu at the R-scale smoothed g_R (nu = 12.0 @35, 15.4 @100 — the
   double-count root cause, reproduced). SC instead evolves delta under the
   kernel and gets V kinematically from continuity (f₀ and the D-ratio; **no ×nu
   on V anywhere** — the double-count is genuinely removed, not re-multiplied).
   Result: SC/naive = 1.38 @35, 1.07 @100 — comparable-to-worse, because the
   double-count is replaced by the amplitude runaway.

3. **Is the overshoot manufactured?** NO — it is analytically forced by the
   kernel. Deep regime nu ≈ (g/a0)^(−1/2), g ∝ delta/a² ⇒ source ∝ delta^(1/2)·a;
   power-law consistency in EdS forces delta ∝ a² (p = p/2 + 1 ⇒ p = 2) — the
   Nusser 2002 runaway inside this framework's own kernel. Measured local
   exponent f(a=0.3) = 1.633 (between ΛCDM 1 and attractor 2, as it should be
   mid-transition); the enhancement saturates at the attractor (nu_eff(0)=3.43,
   g_rms locks at 0.09 a0), never at nu→1. Anchor is mild (nu = 1.166 at z=200),
   so the blow-up is not seeded by an inflated start. Independent LSODA
   re-integration at rtol=1e-10 reproduces D-ratio 8.5026.

4. **sigma8:** arithmetic exact (0.811×8.503 = 6.896; ×9.868 = 8.003). Linear
   sigma8 crosses 1 at z = 2.74 (canonical) / 3.02 (alt) — structure nonlinear
   far too early; z=0 values are linear-extrapolated diagnostics, correctly
   labeled as such. This IS the classic MOND-structure over-production
   (Nusser 2002), not a manufactured deficit: verified as hard as a win would be.

5. **Bulk flow, amplitude AND shape:** SC amplitude 14.5×/8.1× Qin (canonical),
   17.0×/9.6× (alt). Shape is honest: the enhancement is scale-independent
   (rms approximation), so all MI curves inherit the declining ΛCDM V(R) shape;
   Qin's banked points RISE (380@35 → 410@100), which no variant reproduces —
   floor_cH lands 439@35 (1.2×, ~2.4σ high) but 266@100 (0.65×, ~1.8σ low).
   "Roughly viable, above ΛCDM in the direction Qin wants" is fair at 35 Mpc/h;
   the shape mismatch at 100 is real and stated.

6. **Floors:** nu(y=1) = √2 = 1.414 and nu(Z=5.790) = 1.0829 confirmed;
   floor_cH is nearly MI-off by construction (f₀/f_Λ = 1.05) — the RESULT says
   exactly that. Both footings run end-to-end (~15% spread, alt slightly worse).
   Skordis–Złośnik 2021 (PRL 127:161302) and Nusser 2002 (astro-ph/0109016)
   credited in both scripts + RESULT.md; first-pass caveat (Newtonian
   quasi-linear on AeST background, NOT covariant MI perturbation theory;
   frame-field perturbations, condensate–baryon coupling, CMB/recombination
   re-check at nu(z=200)≈1.17, relativistic transfer, scale-dependence, and the
   peculiar-vs-total-acceleration fork all open) is prominent in docstrings,
   RESULT.md, and the figure title.

## VERDICT: **UPHELD — STILL-OVERSHOOTS (both footings), fork-hostage, needs the covariant treatment**

On the specified footing (kernel argument = the element's peculiar acceleration,
self-consistently iterated) MI over-produces large-scale structure: sigma8
8.5–9.9× Planck, bulk flows 8–17× Qin 2021. Self-consistency genuinely removes
the naive double-count but replaces it with the analytically-forced delta ∝ a²
attractor runaway — no manufactured taming AND no manufactured overshoot found.
The one taming lever is the dS-Unruh kernel-argument fork: total-proper-
acceleration floor (g ≥ cH_Λ = Z·a0) gives sigma8 = 1.02 (26% high — still a
real tension) and V(35) = 439 / V(100) = 266, but that variant nearly switches
MI off on linear scales by construction. The fork spans the entire verdict range
and is precisely the unwritten covariant-MI question.

**Honest one-liner:** the first tractable MI linear cosmology reproduces the
classic MOND-structure runaway inside the framework's own kernel — self-
consistency is a runaway-to-attractor, not a cure — and only the variant that
effectively turns MI off at linear scales survives the sigma8/bulk-flow
confrontation; which variant is right is exactly what the covariant completion
must decide.
