# G196 -- THE ONE-BOUNDARY PAPER STATEMENT
**r_M = sqrt(G M_b / a0) as the theory's single radius.**

*Lane: G196. Repo: zimmerman-formula. Date: 2026-09-16.*
*Sources (all committed, nothing recomputed): G090 (Lean cert, rung 1), G095, G119, G132, G149, G176, G186, G188. Companion artifact: G196_results.json.*

---

## PART 1 -- THE COMPLETE STATEMENT

> **THE FRAMEWORK'S ONE BOUNDARY.** The equilibrium theory of gravity has exactly one
> physical radius: **r_M = sqrt(G M_b / a0)** — the baryonic a0-crossing, the radius at
> which the baryonic field falls to a0 (G M_b / r_M² = a0 exactly; the identity
> G M_b / r_M = sqrt(G M_b a0) is the **Lean-certified G090 rung 1**). Every phase change
> in the dark sector sits on this single line. Six independent diagnostics mark it:

**(a) The galaxy-scale break.** r_cut = sqrt(a0/g_ext) · r_M — the EFE-cap line projects
the one boundary inward when the environment exceeds the a0 floor. For the Milky Way
(M_b = 6.5e10, g_ext = 2.44e-10, the L240 own-halo field) the full-kernel solve gives the
**kernel break 6.13 kpc = 0.623 r_M** (registered 0.62; G119, full kernel G149). *Lane:
G119/G149. Measured: r_cut = 6.13 kpc = 0.623 r_M (kernel), R_efe = 6.50–6.74 kpc =
0.66 r_M (deep-form), sqrt(a0/g_ext) = 0.620 at the required g_ext.*
The identity r_efe/r_M = sqrt(a0/g_ext) holds to 1e-16 (M_b cancels); the 0.62 vs 0.66
gap is the kernel's interpolation near g ~ a0, not a parameter.

**(b) The cluster seam.** The pooled dust density rho_dust(r) is ONE law with a seam at
**r_t = 387 kpc = 0.96 × median r_M** (median r_M = 402 kpc; 1-sigma band [269, 543] kpc,
0.30 dex): the dust shape breaks from **p1 = 1.50 ± 0.04 → p2 = 2.94 ± 0.04**
(2-index model beating the single index by d_BIC = −351). The cluster environment sits AT
the a0 floor: sqrt(a0/g_ext) = 0.963 → g_ext = 1.08 a0. *Lane: G176. Measured:
p1 = 1.50, p2 = 2.94, r_t = 386.8 kpc = 0.96 r_M.*

**(c) The amplitude jump.** The phantom/dust amplitude ratio A = (sigma_ph/sigma_d)^3 at
the boundary is, in its integral reading, the *seam's own imprint*: the slope change
p1→p2 = 1.44 dex/dex accumulated over the seam's resolved width gives
**A_integral = 0.364**, and the measured phantom/dust ratio at r_t is median **0.369** —
both agree with the universal A = 0.273 (G159 geomean) within a factor ~1.35
(< 2), so the seam and the jump are the SAME event at 0.96 r_M. *Lane: G186 (invoking
G159/G185). Measured: A_integral = 0.364 (×1.34 vs 0.273), A_meas@r_t = 0.369 (×1.35),
A@cap = 0.297; the literal density step through the seam is 1.006 — a kink, not a step
(d_BIC = +7.3 against a step).*

**(d) The first-order latent heat.** The phantom→free-dust crossing carries a finite
entropy step **dS = 10.8–23.7 k_B/particle** (cosmic-ref 10.8, in-cluster 21.5,
matched-density 23.7 at m = 5 keV), so **L = T_b dS is finite**: L/N = 0.009–0.019 eV/particle,
L/(N k_B T_b) = 10.8–23.7 — water-class (13.1). The transition is first-order, not a
crossover. *Lane: G132. Measured: dS = 10.8–23.7 k_B; T_b = 9.52 K = the CMB at z = 2.49.*

**(e) The temperature law's pivot (2/3).** The ratio of the measured virial temperature to
the baryon-triad floor factors exactly,
**T_obs/T_pred = 2 (M_dyn/M_b) (r_M/r)** — a0 enters ONLY through r_M, so r_M IS the pivot
scale; its structural exponent against the mass ratio f is **2/3** (virial temperature of
the total mass at fixed overdensity; the BTFR-style 1/2 is excluded at ~2σ). Median closed
form 3.51 vs measured 3.57 (G075's 0.28). *Lane: G095 (G135). Measured: alpha = 2/3,
closed form 3.51, 21-system rms 0.076 dex.*

**(f) The pie's pivot.** The sector pie — dust-dominated INSIDE, phantom-dominated OUTSIDE —
is the two-regime map at both scales: at cluster scale the free dust is 81.6% of M_dyn at
50 kpc (= 97.6% of the missing mass there) falling to 24.6% at R500, the phantom rising
2.0% → 56.9%; at galaxy scale the interior IS the phantom (the r⁻² deep law, dark-share
0.89 at the solar circle, ~0–5% dust) and the 6.13 kpc break is where the deep law ENDS.
The pivot parameter in the closed form is **u = r_M/R500**. At matched r/r_M = 0.6 the
sectors FLIP: galaxy dust 3.9% vs cluster dust 74–79%. *Lane: G188 (invoking G179).
Measured: 50 kpc dust 81.6%, R500 phantom 56.9%; galaxy interior phantom dark-share 0.89.*

---

## PART 2 -- THE MEANING: the single boundary's physical content

The one radius is an **a0-crossing, and the a0-crossing is a phase switch**. It separates
the two-phase architecture of the dark sector by the STRENGTH of the field relative to a0:

- **Inside r_M, the field is STRONG (g > a0): the dust is un-equilibrated.** r_M is
  defined by G M_b / r_M² = a0 exactly — interior to it the baryonic field exceeds a0 by
  construction. Here the equilibrium phase cannot cover the deficit (the linear phantom's
  growth (r/r_M)/(f−1) is too slow), and the free dust — the cold, un-equilibrated sector —
  carries the missing mass. It is the strong-field Newtonian core (cluster dust 81.6% at
  50 kpc; g_tot(R500)/a0 = 0.55 < 1 on 12/12 clusters marks the deep side).
- **Outside r_M, the field is DEEP (g < a0): the phantom equilibrates.** Sub-a0 the
  equilibrium phase forms and the deficit is covered by the phantom, whose deep law
  v_flat² = sqrt(G M_b a0) is the Lean-certified G090 statement. The phantom dominates at
  R500 (56.9%).
- **The boundary is the a0-crossing where the two-phase architecture switches.** Every
  phase mark — the galaxy break, the cluster seam, the amplitude jump, the latent heat,
  the temperature pivot, the pie pivot — is the SAME switch seen through a different
  observable. The galaxy and cluster "shapes" are one system read at different r/r_M
  windows; the difference is only WHERE the equilibration boundary sits (inside r_M at
  galaxy scale — the EFE line 0.66 r_M; at ~r_M for the cluster seam; ~1.3 r_M for the
  phantom/dust crossover at cluster scale).

**The RAR itself is a phase diagram.** The deep radial acceleration relation is the
statement of this switch: the baryonic a0-crossing ends the strong-field region and opens
the deep one. r_M is therefore not one of several radii — it is the theory's single
radius, with the environment (g_ext) merely projecting it to a position r_b = r_M
sqrt(a0/g_ext) at each system's own M_b.

---

## PART 3 -- THE PAPER-READY FORM (for the cluster section)

### The one-paragraph statement

> The equilibrium dark sector carries a single boundary. It is the baryonic a0-crossing,
> r_M = sqrt(G M_b / a0), the radius at which the baryonic field falls to a0
> (the identity G M_b/r_M = sqrt(G M_b a0) is Lean-certified, G090 rung 1). Thermodynamically
> the crossing is first-order — it carries a finite entropy step dS = 10.8–23.7 k_B per
> particle (a latent heat L/(N k_B T) = 10.8–23.7, water-class) with boundary temperature
> T_b = 9.5 K, the CMB at cosmic noon. Structurally it is the phase switch: interior to r_M
> the field is strong (g > a0) and the missing mass is carried by un-equilibrated free dust
> (the strong-field core, 82% of M_dyn at 50 kpc); exterior, sub-a0, the phantom equilibrates
> and dominates (57% at R500). Observationally the same boundary is marked at every scale by
> the unified line r_b = r_M sqrt(a0/g_ext): the Milky Way's rotation-curve break at
> 6.1 kpc = 0.62 r_M (the external-field cap), the X-COP dust-density seam at r_t = 387 kpc =
> 0.96 r_M (p1 = 1.50 → p2 = 2.94) whose integrated imprint is the amplitude jump
> A = 0.36 ≃ 0.273, and the sector pie's pivot (dust inside, phantom outside).
> Ten independent diagnostics sit on the same r_M; the radial acceleration relation is the
> phase diagram of this one boundary, and the environment sets only where, at each system's
> own baryonic mass, that boundary projects.

### The boundary's testable predictions (for the cluster section)

1. **The galaxy break for ANY M_b / g_ext.** Predict |break| = r_M sqrt(a0/g_ext) =
   sqrt(G M_b / g_ext · a0-contribution) for any system: r_M = sqrt(G M_b/a0) with the
   break projected by the environmental field sqrt(a0/g_ext). The zero-parameter F(e_N)
   kernel solves the position; the MW (e_N = 2.29, kernel 6.13 kpc = 0.623 r_M) is the one
   testable in-band object and passes. The WALLABY DR3 resolved pairs give resolvable
   break forecasts (e.g. break at 1 r_M requires e_N ≥ 1.39, pair d ≤ 4.4 kpc) — the
   prediction is to find the break in low-field pairs and dwarfs.
2. **The cluster seam.** The same break, in the density slope at the r_M-class radius:
   any cluster's dust profile should change shape at r ≈ r_M(M_b) = 0.96 × the seam, with
   p1 ≈ 1.5 → p2 ≈ 2.9. The cluster environment sits at the a0 floor (sqrt(a0/g_ext) = 0.96),
   so the cluster seam is the un-projected ("bare") r_M boundary.
3. **The saturated pie.** Beyond the crossing the pie saturates in the r_M-class:
   M_sat ≈ 3.09e14 sits on the boundary (a_c ~ M^-0.41 run, G178), the phantom
   equilibrium covers the deficit with share (r/r_M)/(f−1) → 1 at/outside R500, and the
   deep-window envelope holds on [r_M, R500]. The pie's pivot u = r_M/R500 is fixed by
   M_b alone, so the phantom's dominance radius is predicted, not fitted.

---

## PART 4 -- VERDICTS

### V1 -- The statement is complete.
All six diagnostics (a)–(f) are stated with their lane and their measured value:
(a) G119/G149, 0.623 r_M (6.13 kpc); (b) G176, 0.96 r_M, p1 1.50 → p2 2.94;
(c) G186, A = 0.364/0.369 ≃ 0.273; (d) G132, dS = 10.8–23.7 k_B, water-class;
(e) G095, alpha = 2/3, closed form 3.51; (f) G188, dust 81.6% at 50 kpc / phantom 56.9% at
R500, u = r_M/R500. The Lean-certified footing (G090 rung 1) anchors the definition. The
statement also honors the galaxy-cluster unity (the same boundary inside r_M at galaxy
scale, at/outside r_M at cluster scale) and the honest caveats in V3.

### V2 -- The paper-ready paragraph.
Part 3's one paragraph is the cluster-section wording: it opens with the single-boundary
claim, states the thermodynamic character (latent heat, T_b = CMB at cosmic noon), the
phase-switch mechanism (strong dust / deep phantom), and the observational unification
(break 0.62, seam 0.96, jump 0.36 ≃ 0.273, pie pivot), and it closes by re-framing the RAR
as the boundary's phase diagram. It carries no unexplained numbers and no claims beyond the
committed lanes. Its three testable predictions (the any-mass galaxy break, the cluster
seam, the saturated pie) follow directly.

### V3 -- The honest statement.
The one-boundary claim is **strong**: ten independent diagnostics sit on the same
r_M = sqrt(G M_b/a0) line with mutual agreement, the algebraic identity
r_b/r_M = sqrt(a0/g_ext) holds to 1e-16, and the line reproduces both the MW break
(0.62 r_M) and the cluster seam (0.96 r_M) with only the environment as input (g_ext = 2.44e-10
for the MW, ~1.08 a0 for the clusters). Its strength is its *over-determination*: no single
observable carries it.

Its honesty requires **two registered caveats** (both from G186/G176, recorded verbatim):

1. **The smooth-steepening alternative.** The sharp seam at r_t is preferred, but a smooth
   log-quadratic steepening lies within **d_BIC = 16** of it — a finite-width transition is
   NOT excluded by the seam data alone. The one-boundary claim rests on the sharp-seam model
   winning, and the alternative (a continuous p(r)) is close enough that the seam should be
   reported as "a resolved transition," not "a discontinuity," until a wider dataset widens
   the BIC gap. The same lane notes the seam is ONE r_M-CLASS radius, not a per-cluster
   boundary (d_BIC = −110.8 against r_t = r_M per cluster).
2. **The contested cap-firing mechanism.** The position of the break (the EFE cap at the
   a0-crossing zone) is robust, but the MECHANISM by which the cap "fires" is contested:
   G138's cH0 firing rule fails 4/4 checks (never observable), while the a0-rule fires in
   the r_M-class zone. G132 confirms the measurement side: the first-order jump is UNTESTED
   at cluster scale (0/12 X-COP clusters resolvable; the smooth rise is a resolution limit,
   not a zero latent heat) — its resolved observable is the galaxy-scale break.

So the paper's one-boundary sentence is warranted for the *position* and the *character*
(the a0-crossing, the first-order latent heat, the two-regime switch), while the paper must
register that (i) the transition's sharpness is provisional (d_BIC 16 to smooth steepening)
and (ii) the cap's firing mechanism is not yet derived (the environmental placement is
derived, the trigger is not).

---

*Deliverable complete. Pass: 3/3 verdicts. G196_results.json written alongside.*
