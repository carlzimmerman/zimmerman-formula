# HB1_barotropic_hydrostatic: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** Replace the shell map by a solve: the cold share as a barotropic fluid in hydrostatic equilibrium with the baryons, spherical, self-consistent with Poisson, on NR3 MEDIAN's path. Two forms. Does it clear the record's lines? Does an outside prediction for one form hold?

**Record check.** `grep -i barotrop` over lanes: DR2 N3 is a static n = 1 toy at one mass with k set by hand, ungraded. BOLTZ1 and X17 bound the sound speed, grade no halo. ER2 and DR5 are torque arguments. JC2's README says this calculation "is not run". GT1 and JC1 are shell maps. DR8 (read only, another agent) is a posited shell rule plus live orbits. CR1 grades classes on a desk. So no lane has solved this; I run it.

**Standing.** kappa = 1/2 FITTED, unused here. Cold dark energy is a gravitating field component, never a particle. No a0 in the cold sector. Not theory closed. Nothing here says the data favour the framework. Inputs NR2 MEDIAN: rho10 1.241, rho11 1.147, eta(1e12) 21.53. Delta 0, EM1, f* 0.034, canonical footing, both backgrounds A, B.

**Not blind.** NR3, UR1, DR3, JC1, JC2, GT1, NR4, DR2, ZN4, BOLTZ1, X17 and CR1 were read. The solve's numbers are unknown to me. The analytic steps below were worked on paper before this file; no script has run.

## The outside claim, scored before computing (Argon, unverified; numbers verbatim)
"A barotropic fluid in hydrostatic equilibrium with baryons, no shell map, gamma = 2, c_s0^2 = |Phi_c0(0) - Phi_c0(R200)|, on NR2's inputs at delta 0. Predicted: global Upsilon 0.58 +/- 0.05; tilt +0.38 +/- 0.08; Upsilon by V_flat bin [0.95, 0.92, 0.74, 0.44, 0.50, 0.66] +/- 0.08 per bin. It withdraws the assessment if the solve gives both |tilt| <= 0.15 and Upsilon(150-200) >= 0.50."

Labels, on Form A, background A, per item (global Upsilon, tilt, each of six bins): **ARGON'S PREDICTION HOLDS** if inside the stated range, else **MISSES**. Its withdrawal condition is stated separately: FIRES or DOES NOT FIRE. On Form B the same table is reported, not scored as its prediction. Gates are separate labels.

## Equations, in the path's own units
Uncontracted core: M_c0 = C B(x), x = r/r0, B = 4[asinh x - x/sqrt(1+x^2)], rho0 = rho_c (1+x^2)^(-3/2), C = pi Sigma r0^2, rho_c = Sigma/r0. Scale the enthalpy by A = 4 pi G rho_c r0^2. Then -Phi_c0 + Phi_c0(infinity) = A H, with H = asinh(x)/x, and hydrostatic equilibrium with Poisson becomes, with no G, m = M/C:

    dH/dx = -(m_c + m_b)/(4 x^2),   dm_c/dx = 4 x^2 rho^(H),   rho^ = rho/rho_c

Integrate from the centre with shooting parameter H_c (this is const'), until the edge x_e, the path's own: R200 for galaxies, groups, LITTLE THINGS; r_ta for clusters and X-COP. Choose H_c so m_c(x_e) = M_c0(edge)/C: mass inside the edge held at N's value. Baryon mass inside the first grid point as the path has it, r^2. Outside the edge, as the grader, nothing added. Baryons feel nothing back.

**Branch.** The root nearest the reference (rho^ = 1) in ln H_c, scanning out both ways. Roots counted on a sample with a wide scan, branch checked by continuation in Phi_b on a sample. No root anywhere: counted, reported; that call returns M_c0 and is flagged. More than 1 % of calls in any graded row with no root: that row is NOT DECIDED.

**Form A, Argon's.** P = K rho^2. c_s^2 = dP/drho = 2 K rho, so h = 2 K rho, and c_s0^2 = 2 K rho_c = |Phi_c0(0) - Phi_c0(edge)| = A q, q = 1 - asinh(a)/a, a = x_e. EOS: rho^ = max(H, 0)/q, K differs by halo. Mass held by H_c as above: the mass-held version is primary, because the claim fixes a mass and the bare version does not hold it. Reported: Phi_b = 0 null, how far it is from the core: sinc radius in r0 units against R200, M(<r0), M(<3 r0) over the core's, central density; the same at the bare K with rho^(0) = 1 unheld, M returned over M_c0. Reading of c_s0: P/rho = c_s0^2 at centre would halve K; run once on SPARC as sensitivity, labelled so.

**Form B, PRIMARY, no chosen gamma.** h(rho0(r)) = -Phi_c0(r) + const, per halo: parametric H = asinh(x)/x, rho^ = (1+x^2)^(-3/2), on H in (0, 1), and x runs past the edge with the same formula, so low H is defined. At H -> 1, rho^ = 1 - 9 (1-H) + ...: the core's central index is exactly gamma = 2, with c_s^2(centre) = A/9. Note that is 1/(9 q) of Form A's value.

**What this form does not fix, stated before numbers.** The core defines h only for rho <= rho_c. Baryons push H above 1, so the EOS above central density is an extrapolation, not a measurement of the core. So "no new number" holds only conditional on a function choice. Frozen:
- **E1, PRIMARY:** C1 tangent, rho^ = 1 + 9 (H - 1): the core's own central gamma = 2 continued.
- **E2, reported:** analytic continuation x = iy: H = asin(y)/y, rho^ = (1-y^2)^(-3/2), rho -> infinity at H = pi/2. Calls that hit the wall counted.
- **E3, reported:** isothermal at the tangent sound speed, rho^ = exp(9 (H - 1)).
If E1, E2, E3 differ in Upsilon at 150-250 km/s by more than 0.05, the result is labelled **[EOS-ABOVE-CENTRE DEPENDENT]**, and the form has a hidden function.

**Baryon potential.** PRIMARY: the path's M_b = GB r^2/G, the same array Blumenthal gets, so the comparison changes only the response. It is not the monopole. Reported on SPARC with the Form B E1 row: DR3's monopole, its primary (SB stars, exponential gas), and its stress (gas inverted from V_gas), through DR3's read-only functions. Clusters, groups and LITTLE THINGS have no disc: unchanged.

**F.** The path's F (baryons initially tracing the cold share) is not used: a hydrostatic solve has no initial shells. Stated. BCG in the cluster path as NR3 has it.

## Runs
Through NR3 MEDIAN's driver, own cache, UR1's tail helpers, `contract` replaced by the solve. Rows: EM1|off, EM1|blum (baselines), Form A, Form A P/rho reading (SPARC), Form B E1, E2, E3, B E1 with DR3 monopole, B E1 with inverted gas. Clusters: keys and X-COP on the path as NR3's gas inputs, and **separately at gas +0.005 (GS4)**, the same path with Mg500 x 10^0.005: baseline off, blum, Form A, Form B E1, f* 0.034; the path used is S-core with r_ta edge, stated. **Against ZN4 separately:** ZN4's chain at gas +0.005, f* 0.034 and 0.0615, its native z = 0 shape (ng 80), with Form B built numerically from each cluster's M0(r) (H from integrating G M0/r^2, rho from dM0/dr, made monotone, count where it isn't); above the innermost tabulated density, tangent gamma, as E1. Baryons pp["Mb"], no BCG, as ZN4's path; X-COP likewise. Base: ZN4's jobs reproduced first. A cusp's own barotrope has a pole (rho ~ 1/r gives rho -> infinity at finite H) so the extrapolation matters more here; say so in the read.

## Read-outs
Upsilon A/B, rms, tilt, Upsilon by V_flat (same bins and quality cut as NR3), groups Z, LITTLE THINGS A/B; 15 keys Z both h, X-COP. **Effective f by bin:** (Q - 1)/(Q_Blum - 1) at r0, 2, 3, 4 R_d, Upsilon 0.5, background A, median by V_flat, against NR4's requirement (f about 0-0.2 at 150-250 km/s, low-mass eta x 1.5). Solver stats: H_c by bin, roots, no-roots, walls, edge density.

## Universal fluid, a real objection
Form B gives one EOS per halo: (rho_c, A) enter. That is one fluid only if h(rho) is the same function at all masses. Test at M_t 1e10, 1e11, 1e12, 1e13, 1e14, 1e15 on N's rule: c_s^2(rho) = rho dh/drho on the overlap of densities; spread between masses in dex. Also direct: take 1e12's EOS, solve at Phi_b = 0 with each other mass held inside its own edge, and read M(<r0)/M_c0(<r0) against that mass's own core. **Label: ONE P(rho) ALLOWED** if spread <= 0.1 dex over the overlap and all direct ratios are in 0.9-1.1; else **NO UNIVERSAL P(rho)**; then Form B is a per-halo function, a halo-by-halo history dependence with no carrier, and that is named. A gamma = 2 with one K has one radius, pi sqrt(K/(2 pi G)), at every mass; r0's range across mass is reported against it.

## Physical consistency, reported, no gate
- c_s(centre) in km/s by mass, Forms A and B; form B c_s at the mean density at z = 0 and z = 3; against X22's <= 6 km/s at z = 3.
- Form A's mu = pi/R_s by mass, against BOLTZ1's floors 56.6, 2.04e4, 1.24e8 per Mpc (quadratic family, same EOS).
- Local Gamma = dlnP/dlnrho along the core; stability at fixed edge, sign of dm(x_e)/dH_c at the null.
- A pressure fluid isn't the zooms' collisionless eta: eta and core normalisation come from pressureless runs, and a fluid with these c_s wouldn't collapse the same way. Named, not fixed. CR1's R5, stream crossing: hydrostatic assumes crossing was cured; nothing here says how. DR2's "pressure is not charge" holds. The owner's rule: no a0, no particle: check the solve contains neither.

## Pass lines (the record's)
SPARC rms <= 0.110 and Upsilon 0.50-0.80 both backgrounds; |tilt| <= 0.15 both; 15 keys |Z| <= 2 at +0.005 (+0.111 not run here; ZN4 has that); X-COP |mean| <= 0.05, rms <= 0.10; groups |Z| <= 2; LITTLE THINGS |median E| <= 0.10.

## Labels, per form, on GATES, separate from Argon's
**CLEARS** all lines; **SPARC LINE, GATES FAIL** (name them); **MOVES, FAILS** (Upsilon moves >= 0.02 from 0.35/0.36 and the line missed); **NO MOVE**. Also **[EOS-ABOVE-CENTRE DEPENDENT]**, as above. CLEARS is never "pass" before verification. **A win verified as hard as a fail:** if Form B E1 clears Upsilon and tilt, rerun on an independent grid (response grid x 4, independent integrator settings) and at NR2's LOW and HIGH before any report; a label differing there takes [NOISE-LIMITED].

## Checks (failed check: no verdict)
K1 EM1|off and EM1|blum through my path against NR3 MEDIAN: Upsilon, rms, tilt, preds, |d| <= 1e-6. K2 Form B, Phi_b = 0: |M/M_c0 - 1| <= 1e-4 on test profiles over 8 decades of r inside the edge, on a sample of calls inside the path, at a truncated edge, and as a whole row (M_b x 0) against EM1|off, Upsilon and rms |d| <= 1e-4 (the 300-point response grid is known to miss 1e-6, NR4's audit). K3 grid doubling: substeps x 2, solver Upsilon, rms |d| <= 1e-3 and M_f on test <= 1e-5. K4 M_b -> 0 limit: M_b x 1e-2, 1e-4, 1e-6: max |M/M_c0 - 1| scales linearly within a factor 3. K5 hydrostatic residual: finished solution against dH/dx, and Poisson by quadrature, <= 1e-4; mass held <= 1e-7. K6 closed forms: Form A in m_b = 0: sinc, rho^ = rho^_c sin(kx)/(kx), k = 3-free form k^2 = 4 rho^... computed from the equation; radius pi/k within 1e-4. Point-mass limit: gamma = 2 outside a point mass matches the known linear ODE by a separate scipy solve_ivp, <= 1e-4. K7 r0 inferred from M0 <= 1e-5 (count failures). **MUTATE** Phi_b x 2: separate output, Form B Upsilon must move by >= 0.02. ZN4 base: chain reproduces its +0.005 jobs |d| <= 1e-6.

## Expectation on record
Form A: the null is badly off. q is about 0.6-0.8, so the sinc radius is about 2.5-2.8 r0 against R200 tens of r0, and mass held puts all the halo inside it, which over-masses the inner curve. So Upsilon is below Argon's, and the shape of its bins misses. Form B: c_s^2 at centre is A/9, small against baryon wells in spirals, so the response is at least Blumenthal-sized at 2-4 R_d at L-star: Upsilon below 0.45 at 150-250 km/s, line and tilt both fail, effective f near or above 1, above NR4's 0-0.2. With no F, clusters pull inward where UR1's expanded: G-IN-Mall worse, keys <= 13 of 15. E1, E2, E3 differ. NO UNIVERSAL P(rho). Low-density c_s far above 6 km/s. If this is wrong, the fluid's a real door.

Only this directory is written. No pushes, no deposits, no new data. MUTATE and verification outputs are named separately.
