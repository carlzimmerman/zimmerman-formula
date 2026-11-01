# Independent bar-selector and angular-momentum review

Reviewed 2026-11-01. Requested checkpoint base: `c2bed2da878ab9843a5d121f0cf6f0315f08c1d4`; observed shared-tree HEAD during this review: `a7bade87f24f37a759b840f0ebb78b80a2d82aac`. The tree is dirty and advancing concurrently. This review does not attribute all current files to either revision. No scientific input, script, result or manifest was modified. The only persisted output of this reviewer is this file.

## Exact verdict

**The finite structural preference and the stated mass/AM rescaling arithmetic are supported. A physical selective response has not been obtained.** The fixed external ELN proxy preferentially marks the target spirals compared with dwarfs in this 123-galaxy subset. It neither predicts their bars nor supplies a torque, irreversible heating, final density profile, dwarf preservation, or a rotation-curve pass. It also marks many galaxies above the desired velocity window.

The AM ratios are conditional on an exponential, circularly streaming stellar reservoir, one of four imposed geometries, perfect delivery of steady-pattern work, and the historical ER1 energy functional. That last functional is a reproducible comparator but is **not generally the cold component's exact mechanical energy in a fixed extended baryonic potential**. Consequently the AM screen is not yet a necessary-or-sufficient physical energy test.

Outcome label: **audited, with independent read-only recomputation of selector, mass normalization, angular-momentum integrals, geometry, and rescaling; interpretation conditional**. The production scripts' main programs were not rerun. Their two completed v2 manifests validate against current files. No ng80 result was used here.

## Independent derivation and normalization

For an exponential stellar surface mass density `Sigma(R)=Sigma0 exp(-R/Rd)`, integrating `2 pi R Sigma dR` gives `Md=2 pi Sigma0 Rd^2`. Thus, using catalogue brightness `I0` in solar luminosities/pc², `Sigma0=0.50 I0` in solar masses/pc², and `Rd` in kpc,

`Md_phot/Msun = 2 pi (0.50 I0) (1000 Rd)^2`,

`epsilon = Vmax / sqrt(G Md/Rd)`.

The factors of 1000, solar mass and kpc in `bar_screen_v2.py:114,131,133` are consistent. The alternative expression at line 133 is the same dimensional quantity. There is no acceleration scale in this construction.

The original [Efstathiou, Lake & Negroponte paper, MNRAS 199 (1982), pp.1069–1088](https://adsabs.harvard.edu/pdf/1982MNRAS.199.1069E), p.1069 and its numerical setup on pp.1070–1071, supplies the cold exponential-disc empirical threshold 1.1 and self-gravitating-disc coefficient approximately 0.63. Its halo was a fixed force component. This authenticates the formula and its historical numerical context, not its applicability as a universal instability theorem. [Athanassoula, arXiv:0808.0016v1 (2008), abstract](https://arxiv.org/abs/0808.0016v1), explicitly rejects general bar-stability classification by this criterion; full text of that paper was unavailable through the browser during this review.

Writing the tabulated disc contribution at unit stellar mass-to-light ratio as `Vd,max`, the force proxy assumes `sqrt(0.50) Vd,max = 0.63 sqrt(G Md_force/Rd)`. Therefore

`Md_force = 0.50 Vd,max^2 Rd/(0.63^2 G)`,

`epsilon_force = 0.63 Vmax/[sqrt(0.50) Vd,max]`.

This is algebraically correct, but it assigns the mass of an exponential disc having the tabulated force peak. A real nonexponential disc with the same peak need not have that mass. The total-light proxy `0.50 L36` assigns all catalogue stellar light to the disc; its mass allowance includes bulge light, whereas the spherical energy comparator uses disc Upsilon 0.50 and bulge Upsilon 0.70. These are deliberately different conditional constructions, not one measured baryonic decomposition.

Important mass-consistency findings from the rows and raw catalogue:

- The central-exponential-light mass exceeds the catalogue **total** stellar mass at the same Upsilon in **101/123** galaxies; its ratio to total ranges from 0.2771 to **73.3552**. This invalidates interpreting that extrapolation as measured total disc mass or measured disc AM.
- The force-exponential mass also exceeds the same total-light mass in **46/123**, including **9/25** and **7/18** target spirals. The maximum ratio is 2.8105. Even the force-clean subsets contain 3/12 and 4/7 such cases. Force-based AM is therefore another model normalization, not a recovered observed stellar mass.
- The two total-light rows and force rows still show a similar broad structural preference. The preference does not depend solely on the failed central-light extrapolation.

## Population and denominator check

Parsing the 175-row table independently and applying `Q<=2`, `inc>=30`, `20<=Vflat<400` reproduces exactly the 123 names in both results files. The bins are half-open. DDO170, with Vflat exactly 60, belongs only to 60–100 here; historical ER1 used inclusive endpoints and counted it in both adjacent bins. There are no exact 150/200/250 boundary cases in this selected table.

Independent raw-curve recomputation of `epsilon<1.1` gives:

| Vflat km/s | n | Central-light selected | Force selected | Total-light selected | Post-result force-clean selected/n |
|---|---:|---:|---:|---:|---:|
|20–60|12|3|0|1|0/8|
|60–100|35|14|1|1|0/25|
|100–150|23|14|5|6|3/16|
|150–200|25|21|20|22|12/12|
|200–250|18|16|12|15|6/7|
|250–400|10|7|6|7|2/2|

Thus the force proxy selects 32/43 target spirals versus 1/47 below 100 km/s; the total-light proxy selects 37/43 versus 2/47. Neither isolates the window: force and total-light select 6/10 and 7/10 above 250 km/s. These are sample counts, not measured bar incidences or inferred response probabilities.

The originally predeclared clean cut, which also excludes central-exponential luminosity exceeding total, leaves only 2 and 1 target galaxies. The force-clean cut is a disclosed post-result sensitivity and must retain that status. Its larger target fractions are not an independent validation set. The main all-row counts do not silently drop discrepant galaxies.

## Jacobi work, reservoir, and geometry

For an otherwise steady potential `Phi(R,phi-Omega_p t)`, the equations of motion give `dE/dt=partial_t Phi=-Omega_p partial_phi Phi`, while `dLz/dt=-partial_phi Phi`. Hence `dE=Omega_p dLz` exactly for constant pattern speed. E and L may be per unit mass or totals if used consistently. This agrees with [Sellwood & Binney (2002), section 2, equations (1)–(4)](https://adsabs.harvard.edu/pdf/2002MNRAS.336..785S). Their next step distinguishes random-motion energy from changes of circular-orbit energy; at corotation, AM exchange need not heat at first order. The identity is total orbital work, not an irreversible-heating law. A bar that changes amplitude or slows requires actual time-dependent work accounting.

For circularly streaming exponential stars,

`Ld = integral R Vphi dM = Md Rd integral_0^infinity x^2 exp(-x) Vphi(x) dx`.

This yields `Ld=2 Md Rd Vflat` for a flat curve. Code units are kg m²/s. Multiplying by `Omega_p` in s⁻¹ gives joules, so `Ereq/(Omega_p Ld)` is dimensionless. Its interpretation assumes the donor disc loses the required positive AM and the recipient gains the associated work. Using observed gas circular speed as stellar streaming speed neglects stellar asymmetric drift; the exponential shape and inner/outer extensions are also imposed. These features make it an allowance under a model, not a universally bounded observed AM reservoir.

The geometry pairs `(a_bar/Rd,R_CR/a_bar)=(0.6,1),(0.6,1.4),(1.4,1),(1.4,1.4)` use external alternatives, applied to every galaxy. [Erwin, astro-ph/0508590v1, abstract](https://arxiv.org/abs/astro-ph/0508590v1), gives means near 0.6 and 1.4 and much broader distributions. [Aguerri, Debattista & Corsini, astro-ph/0209377v1, abstract and section 1](https://arxiv.org/pdf/astro-ph/0209377), reports five early-type bars consistent with 1–1.4. Those data authenticate these alternatives; they do not make them a universal bracket or SPARC measurements. `Omega_p=Vobs(R_CR)/R_CR` is evaluated only within observed coverage.

For the **force-normalized** disc, exact denominators and medians in geometric order are:

| Geometry | 150–200 covered n | Median Ereq/(Omega Ld) | Whole-disc ratio <=1 | 200–250 covered n | Median Ereq/(Omega Ld) | Whole-disc ratio <=1 |
|---|---:|---:|---:|---:|---:|---:|
|0.6,1.0|17|0.25875|16/17|15|0.11844|15/15|
|0.6,1.4|21|0.39987|19/21|16|0.16426|16/16|
|1.4,1.0|24|0.56799|20/24|17|0.25734|17/17|
|1.4,1.4|25|0.72128|21/25|18|0.34795|17/18|

These medians/counts concern **all covered target galaxies**, not only ELN-selected ones. Selected-and-affordable force counts are respectively 13/13,16/16,18/19,19/20 in 150–200 and 9/9,10/10,11/11,12/12 in 200–250. A large fraction of the entire disc AM is demanded in some alternatives; the fixed original baryonic disc cannot simultaneously be assumed to survive that loss without calculation.

For both force and total-light normalization, no covered target galaxy has `Ereq/(Omega L(<a_bar))<=1` in any of the four geometries. The smallest force ratio is 1.04558, safely above the independent quadrature discrepancy below. This rules out spending only that initial enclosed reservoir **against this inherited comparator** under these assumptions. `L(<a_bar)` is not a theorem bounding an evolving bar's access to the outer disc, gas, growing bar extent, or previous AM transfers. A stellar bar is an orbit-supported density pattern, not a rigid rotating body; the scripts correctly avoid identifying its energy with `I Omega_p^2/2`.

The README's conditional OLR arithmetic is correct: flat circular epicycles give `R_OLR/R_CR=1+1/sqrt(2)` and radii 1.0243,1.4340,2.3899,3.3459 Rd. It has no demonstrated native-field resonance or radial-response implication.

## Energy target: what is reconstructed, and what remains unproved

The numerator is the historical ng64-era ER1 bookkeeping target, not ng80. The code reconstructs A with `log10(Mc/Msun)=11.18+0.90[log10(Mbar/Msun)-10]` and A's own h, rather than treating the retained B energy dictionary as A. Retained B is reproduced by the recorded code to 7.21e-15. The A/B full-undo energy ratio 0.94456–0.96696 is consistent with the reported reconstruction. This review inspected the original ER1 definition and its overwrite path; it did not independently validate the native-profile formation/evolution pipeline or rerun the A energy quadrature.

The target `f_req` is a **bin median Upsilon crossing** on ER1's finite f grid: 0.20 and 0.466667 in the two target bins, with linear interpolation of per-galaxy energy at that shared f. It is not the energy separately inferred as required by each galaxy's data. Elsewhere f_req=1 is capped to the gravity-only reference 0.872, so Ereq is zero there **by construction**. Zero dwarf demand or an empty affordability denominator therefore says nothing about a bar's actual dwarf response. Only the structural counts bear on prospective selection.

There is an additional physical energy-functional limitation. Let the cold component be h and the fixed spherical baryonic proxy b. Define

`W_h = U_hh + W_hb^vir`,

`W_hb^vir = - integral [G Mb(<r)/r] dMh`,

`U_hb = integral Phi_b(r) dMh`.

With zero surface terms and equilibrium endpoints, `2K_h+W_h=0`, but the cold mechanical energy is

`E_h = -W_h/2 + U_hh + U_hb = U_hh/2 + U_hb - W_hb^vir/2`.

ER1 instead assigns the positive part of `Delta W_h/2`. Equality requires the change in the external potential-energy term to match the change in the external virial term, as with a point-mass potential, or a separately justified cancellation. For extended baryons,

`Phi_b(r) = -G[Mb(<r)/r + integral_r^infinity dMb(s)/s]`,

so `U_hb` and `W_hb^vir` generally differ by a term that changes as cold matter moves. ER1's code does not calculate that term. Its input `Mb(<r)` itself is a monotone spherical proxy built from the observed disc/gas/bulge radial force; it is not the actual three-dimensional disc potential. Finite outer boundaries, common total mass and equilibrium endpoint assumptions also require checking before interpreting a difference as work. This issue does not invalidate reproducing ER1 **as the same functional**; it prevents calling its AM ratios exact physical affordability bounds. A separate energy-functional audit is required before a mechanical exclusion or feasibility conclusion.

## Numerical checks, provenance, and code limitations

The following checks were performed read-only with Python 3.9.6, NumPy 1.26.2, SciPy 1.11.4 quadrature, macOS 26.5.2 arm64, numerical threads set to one, no randomness, and `python3 -B` to avoid bytecode output. The independent numerical calculation took approximately 0.13 seconds after imports.

- Independently parsed all table/curve inputs for the 123 selected names, units, three mass formulas, both speed normalizations, and force-epsilon closed form. Maximum relative errors versus saved rows: mass 2.22e-16, maximum-speed epsilon 3.33e-16, flat-speed epsilon 4.44e-16, direct force epsilon 4.44e-16, Omega 2.22e-16.
- Integrated `x² exp(-x) V(x)` with adaptive quadrature **split at every measured radius**, using the declared linear inner extension, velocity linear in log radius, and flat outer extension. Maximum discrepancy versus production trapezoids: whole-disc AM 1.108e-6 relative; `Lbar/Ldisc` 2.426e-5 relative. This is small compared with all enclosed-reservoir affordability margins. The production 20–30Rd check alone tests tail/trapezoid stability, not every cumulative radius.
- Independently checked every rescaled row and selected name; maximum AM/rescaling discrepancy 4.44e-16. Recounted geometry coverage, selected-target, selected-affordable and all-target affordable counts directly from rows. No material count or inverse-rescaling error found.
- Ran the installed `validate_manifest.py ... --root /Users/carlzimmerman/new_physics/zimmerman-formula` separately on run002 and run003. Both returned `valid evidence record (run status: completed)`. This validates declared current hashes and structure, not the physical model. Run002 recorded commit `3b2fae101a0d788c19ef94df93a0a599d5c14db1`, run003 `ffd99d845182cd508339f46203d4e2dd0d72a6ee`, both dirty.
- Inspected v2's split outer tail correction and original failed-run description. The correction removes trapezoidal sampling across a speed discontinuity; it does not add evidence for the physical extrapolation.

No consequential implementation bug was found in the reviewed selector/rescaling paths. Some built-in checks are narrow: the quadrupole Jacobi check substitutes two hand-written derivatives of the same identity, and the rescaler asserts selection **counts**, not independent raw-data selection identities. Their success is arithmetic consistency; the independent checks above supply additional coverage. No uncertainty propagation, stellar streaming/dispersion measurements, measured bars, time history, native-field wake, phase-space/caustic completion, or final data grading is present.

Current SHA256 values (paths relative to `rebuild_2026_10_22/ER2_clump_route/bar_selector/`):

| File | SHA256 |
|---|---|
|CONTRACT_v2.md|9133ad777f0d933a63aae64c5a8a5476bba7359faa8fd4d20dcb0ad1ef16c081|
|RESCALING_CONTRACT.md|89743190909fd78baa8ee8b51cf074ef75cb6ea8e28438dd1430fdaa797184d4|
|bar_screen_v2.py|b68ebfc8bde2be96c73f9c2789c346c485a09c72266aa3cdf8bd2589e1324bb8|
|rescale_mass_proxies.py|472f3e581a6ae4d115b4bb7d65d2fea813856a479e4efccae26e0e89ba6432f3|
|run002/results.json|ba0d80d038022068486fb9be71e7449c50b18030d24722ec29e548aae82783d8|
|run003/results.json|16cf3a41b7e7f7071dd999bf2c6cac34c1789119472a03685cde7f84406ac378|
|run002/manifest.json|0f62ad7a1cd1c2f8afcaba337c656e5e6e2f62dc2a03a3dd63bf06563619ae84|
|run003/manifest.json|8bb10f587c95d644b72dcde46a466295476de5df2b5e57232cef8b68c5c88e54|
|README.md|0c2ae304353623b37d17179fd5797e7e18afd404939ea65cea16df8fb54f438f|

Raw source inputs are individually pinned in the validated manifests. External sources above were checked 2026-11-01; no full texts were retained by this reviewer.

The remaining discriminating work is to correct or explicitly retain the energy functional, measure bar/stellar quantities independently, and compute a native-field response with a justified completion. A fitted epsilon-to-response switch would not close that missing implication.
