# FN1b_fixed_length_static: frozen criteria

Committed alone, before any script or number. Sub-lane of FN1_action_call (criteria 72f9d70fd6), which found option
(b)'s static limit not fully graded at a fixed universal length. κ = ½ FITTED, held fixed. Footings canonical
a0 = 9.3603e-11 and alt 1.1312e-10 m/s², never pooled. Not theory closed. Nothing here says the data favour the
framework. No cold component, no particle. **Not blind:** KT14–KT19, KT33, KT34, CZ1–CZ5, CW1 and CW3 were read first;
expectations are written at the end.

## Question

Does one Gaussian length L, the same for every mass, pass the five static gates on either footing?

## Two forms

- **R, reciprocal (primary).** Φ = Φ_N[ρ] + S Φ_ph[Sρ]. S is the normalised 3D Gaussian of standard deviation L.
  Φ_ph[ρ̃] = QUMOND[ρ̃] − Φ_N[ρ̃], with the board law's simple ν. This is the static limit of any action in which matter
  couples to the phantom sector through the fixed kernel S. The force is then the gradient of E_N[ρ] + E_ph[Sρ], so the
  outer S enters as the adjoint (KT33's map). Option (b)'s labels come from R.
- **SO, source-only (beside).** Φ = Φ_N[ρ] + Φ_ph[Sρ]. This is the record's KT14–KT19 rule. It has no action: KT33 shows
  its linear response is not symmetric. It is reported so the record's numbers carry over.
- Plain QUMOND (L = 0) is the reference.

## Scan

L ∈ {0.024, 0.1, 0.25, 0.5, 1.0, 2.0} kpc: the L★ window from 24 pc (CFG820) to beyond 1 kpc (CFG691), plus 2 kpc.
The window is borrowed as a scan range only. v3s's L★ is not this length: its screened core is ℓ_γ = L★²/(2 r_M)
(CFG691), which shrinks with mass. No row here grades v3s.

## Gates

Pass lines are the record's and are not changed.

**T0, Milky Way.**
- Cells: KT13/UX5's 1,375 in-prior cells per footing.
- Lines: KT14's four, L1, L2a, L2b and L3. A cell passes when it passes all four. T0 passes when at least one cell passes.
- There is no host field, so the CZ1 defect cannot enter.
- SO rows: KT14's own code, loaded from `kt14.py` without running its loop, at 0.024, 0.1 and 0.25 kpc. The 0.5, 1.0
  and 2.0 kpc rows are carried from `kt14.json`, since KA1 checks that the code reproduces.
- R rows: KT33's `mw_reciprocal` engine at refine 1 and cut 120 kpc, with lmax raised to the grid's full even rank,
  2(Nt − 1), and a fixed σ = L. An R row is graded only where V1(a) and V1(b) pass; elsewhere T0 for R is NOT EVALUABLE.

**T1, Cassini.**
- The Sun is a point mass in a uniform Newtonian Galactic field: η = g_eN/a0, with ν(η)η = 2.32e-10/a0 (CZ1/CZ2).
- Primary: the exact linear response for a Gaussian-smoothed Sun. It holds when the smoothed Sun's field is far below
  g_eN everywhere, which is true at every L here (L/r_M ≥ 600).
  - SO: q = (4/45)√(2/π) η ν′(η)/σ³, with σ = L/r_M.
  - R: σ → √2 σ.
  - |Q2| = (3/2)(a0/r_M)|q| (KT16's normalisation).
- T1 passes when |Q2| ≤ 5.2e-27 s⁻² (KT16's ceiling). The Hees line 9.0e-27 is reported. CZ4's environment quadrupole
  bound is reported beside.

**T2, 24 Local Group dwarfs.**
- Model: CZ2's 1D model. KT15's Plummer with a = R2 and M = Υ_V L_V + 1.33 M_HI; Υ_V ∈ [1, 3]; a dwarf passes within
  2 e_σ.
- Field: E1. MW satellites get G M_MW/D² with M_MW = 7e10; the others get 0.
- T2 passes at ≥ 15/24 (CZ2's line). STRICT (≥ plain E1) and E2 (MW + M31 vector sum) are reported beside.
- R: the phantom's radial field is smoothed again by S. Its phantom density is smoothed with the same radial kernel.
- D3 row, beside and not graded: the l = 0 monopole of the anisotropic phantom with the vector ν argument (CZ5's plain3
  with the smoothed field). A fixed width has no |g|-dependent ξ, so the saddle that decided CZ5 does not enter.

**T3, SPARC.**
- KT19's model and statistic: 175 galaxies, Υ 0.5 / 0.7, the spherical smoothing approximation, galaxy-equal rms, with
  ξ = L for every galaxy.
- T3 passes when KT19's label reads SURVIVES SPARC (d rms ≤ 0.005 and |median| ≤ 0.05). HURT and FAILS are fails.
- R: the phantom's enclosed-mass profile is smoothed again with KT19's radial kernel and applied as a ratio at the data
  radii.

**T4, planets.**
- AZ12's gate as in CZ3: radial monopole, orbit-averaged secular rate, six planets, Z = |rate|/max(EPM, INPOP).
  T4 passes when the worst Z ≤ 2.
- The Sun's own term comes from the exact linear response, A(r) = −(√(2/π)/3)[(ν(η) − 1) + η ν′(η)/3](GM/L³) r for SO,
  with L → √2 L for R.
- CZ4's disc term at the planets is reported beside. It bounds any filter that leaves the Galactic phantom unscreened at
  the Sun. CZ4's star term is not recomputed for L ≥ 24 pc.

## Known answers, run first

A miss is a failed check, reported.

- **KA1.** KT14's code at ξ = 0.25 kpc reproduces `kt14.json`'s 0.25 entries per footing: n_pass, every line count,
  K_min_L1, vc_max and best D. Counts exact; floats rel ≤ 1e-6. KT14's own C3 smoothing test runs at 0.024 and 0.1 kpc
  (line 1e-3); a miss makes that width's SO row NOT EVALUABLE.
- **KA2.** KT33's engine at its own settings (lmax 24, refine 1, cut 120, KT25 widths) reproduces
  `mw/grid_run/results.json` for the first 25 in-prior cells per footing: vc, K0 and cO of source_only and corrected,
  rel ≤ 1e-6.
- **KA3.** CZ2's dwarf code reproduces CZ2's E1 counts, plain 18 and HALF 18 per footing. It also reproduces KT15's
  universal 2 kpc arm on alt with KT15's field (200 km/s)²/D: 9/24 with the field and 10/24 isolated.
- **KA3b.** The D3 code at L = 0 reproduces CZ5's plain3 E1 counts, 17 (canonical) and 18 (alt), and Fornax at Υ = 2,
  12.59 and 13.15 km/s (2 decimals).
- **KA4.** KT19's code reproduces KT19's ε = 0.55 rows: filter rms 0.1720 / 0.1697 and d rms +0.0029 / −0.0004
  (4 decimals).
- **KA5.** KT33's `quadrupole()` reproduces `cassini/run_002/results.json`'s baseline q_hessian_signed for
  source_only_hessian and reciprocal at ε = 0.5 with η = 2.32e-10/a0, rel ≤ 1e-6. Its q_flux with η_N at σ = 0.5
  reproduces CZ2/CW1's HALF numbers, 1.179 and 2.97 × the ceiling, to 4 significant digits.
- **KA6.** CZ3's planet code reproduces CZ3's HALF Saturn Z, 11.17 and 18.13 (4 significant digits).

## Validation

These decide evaluability. A miss is reported and makes the named rows NOT EVALUABLE.

- **V1, the MW engine for R, per L and footing.**
  - Test density: the disc and gas parts of the fixed cell VC1 = {BV2, Σ_b 53.9, M_bb 2.12e10, R_d 2.6, h_thin 0.35,
    h_thick 1.08, thick share 0.35, R_d,thick 2.0}.
  - Reference: KT14's separable smoothing of the same parts (radial_matrix × vsmooth), mapped to the grid.
  - (a) KT33's S.forward on the cell-averaged density, against the reference, compared through the Newtonian
    observables.
  - (b) KT33's S.adjoint on Φ_N of the unsmoothed parts, against Φ_N of the reference.
  - Lines for (a) and (b): |Δv_c(R0)| ≤ 0.3 km/s, max |Δv| over the Ou radii ≤ 0.5 km/s, |ΔK(R0)| ≤ 0.3 M☉/pc².
  - (c), reported only: KT33-engine SO against KT14 SO on KT14's best-D cell at that L, with the same lines plus
    |ΔcO|/cO ≤ 0.05. A miss flags the R rows at that L [ENGINE-DEPENDENT]; the label is unchanged.
- **V2, the Cassini formula.** KT33's `quadrupole()` with η_N at σ = 20 and 50 r_M, both forms, against the analytic q:
  |ratio − 1| ≤ 0.02. A miss makes T1 NOT EVALUABLE.
- **V3, the planet formula.** CZ3's numeric monopole at L = 24 pc (field a0·gh(r/r_M, L/r_M), SO), against the analytic
  Saturn Z: |ratio − 1| ≤ 0.02. A miss makes T4 NOT EVALUABLE.
- **V4, the reciprocal paths in 1D.** With ν − 1 replaced by the constant 1 (a test, not physics), R's phantom field at
  L must equal the field of the density smoothed at √2 L (S_L S_L = S_√2L). Lines: max relative difference ≤ 1e-3 on
  r ∈ [0.1a, 10a] for Fornax at every L; and on the data radii where the √2 L ratio is ≥ 0.1, for NGC 2403 at every L.
  A miss makes T2 or T3 for R NOT EVALUABLE.
- **Convergence, reported only.** The best-D cell and up to 10 passing cells per (R, footing, L) are rerun at refine 2
  with full lmax. A pass that flips, or |ΔK0| > 1, is flagged [GRID-DEPENDENT].

## Labels

- **Per (form, footing, L):** ALL FIVE PASS; or FAILS: <gates>; or, only when no gate fails, NOT EVALUABLE: <gates>.
- **Per (form, footing):**
  - A UNIVERSAL LENGTH PASSES (L = …);
  - NO UNIVERSAL LENGTH PASSES;
  - UNDECIDED, when no L passes and some L is NOT EVALUABLE.
- Option (b)'s static-limit label is form R's. SO's is reported beside.

## MUTATE twin

ν ≡ 1 in every path, so there is no phantom. The twin bites when KA1–KA6 fail (their stored values are MOND numbers) and
the dwarf count falls to 3/24 at every L. It exits 1.

## Compute and files

- One thread, nice 15, a 1 GB RSS target; peak RSS is reported. No downloads.
- Engines are imported or copied verbatim. No file outside this folder is edited.
- The MW runs one footing per process, about 10 minutes each; the rest takes a few minutes.
- `fn1b_small.py` is rerun once and its outputs compared by SHA-256. The MW runs are not rerun.
- Outputs: `fn1b_mw_{canonical,alt}.{json,out}`, `fn1b_small.{json,out}`, `fn1b_label.{json,out}`, the MUTATE twins
  `*_MUTATE.*`, `.time` files and `README.md` with the label first.

## Expectations, written before any run

- T1 and T4 pass at every L, both forms and footings, by ≥ 1e6, since Q2 scales as GM/L³.
- T2 passes at L ≤ 0.25 kpc and fails at ≥ 1 kpc. KT15 read 9/24 at 2 kpc with the defect field.
- T3 survives at L ≤ 0.25 kpc and is hurt at ≥ 1 kpc.
- T0 for SO: no cell at L ≤ 1 kpc on either footing (KT14); alt only at 2 kpc.
- T0 for R: not known. KT33 found the outer adjoint removed radial support at widths near 5 kpc.
- So I expect NO UNIVERSAL LENGTH PASSES for SO on both footings, and probably the same for R.
