# CFG113 — does GC orbital anisotropy rescue the law's SLUGGS deficit? FROZEN CRITERIA

Written 2026-09-29, before any number of this lane was computed. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure.

## Why

CFG111 (6e1b04092) gave each SLUGGS galaxy its published GC density slope γ_i. The law's JAM-calibrated deficit stayed at 3.6σ, and the rule fitted (1.55σ). Isotropic orbits (β = 0) were assumed.

Anisotropy is the other half of the mass–anisotropy degeneracy. This lane tests it, as the orchestrator approved: declare the range first, with isotropic orbits as the control.

## Physics expectation (declared before any number; from the scale-free Jeans solution, not from this lane's data)

For a power-law tracer ν ∝ r^−γ in a flat-rotation-curve potential with constant β:

σ_los² / v_c² = (γ − β(γ − 1)) / (γ(γ − 2β)).

So σ_los rises with β when γ < 3, falls when γ > 3, and does not depend on β at γ = 3. With γ_i between 2.49 and 3.43, radial anisotropy raises the prediction and shrinks the deficit, but only modestly unless β is close to 1.

## The anisotropy prescriptions (declared)

- **The bracket:** constant β ∈ {−0.5, −0.25, 0, +0.25, +0.5} for every galaxy. It spans the signs and sizes reported for early-type GC systems (read from the arXiv abstracts on 2026-09-29; no file downloaded):
  - NGC 5846 (Napolitano et al. 2014, arXiv:1401.1501): red GCs β ≈ 0.4 outside about 3 R_e, blue β ≈ 0.15, both isotropic near 1 R_e;
  - NGC 1407 (Wasserman et al. 2018, arXiv:1712.01229): metal-rich GCs radially biased, metal-poor tangentially biased;
  - M87 (Li et al. 2020, arXiv:2005.09410): red GCs tangential, blue near isotropic.
- **The control:** β = 0, which is CFG111.
- **Beyond the bracket (reported only):** β = +0.75 and +0.9, larger than any value above.
- **Held fixed:**
  - the tracer slopes are CFG111's published γ_i;
  - the masses are CFG55's JAM calibration, which does not depend on the GC orbits;
  - the sample is CFG55's 16.
- **Machinery:** CFG111's per-galaxy pipeline (CFG55 exec'd read-only). β enters only h50's `sigma_r2` and `sigma_los`, which already take a constant β.
- **Not tested:** radially varying β(r).

## Checks

- **C1 CONTROL:** at β = 0 the machinery reproduces CFG111's committed per-galaxy offsets (law and rule, both footings) to 1e-9.
- **C2 CONTROL:** in a flat-rotation-curve potential (g = v_c²/r) with a power-law tracer, h50's `sigma_r2` and `sigma_los` reproduce the analytic σ_los²/v_c² above to 0.3%, at R = 5 kpc, for γ ∈ {2.5, 3.43} and β ∈ {−0.5, +0.5}.
- **H1 [HEADLINE; MUTATE must fail]:** with the published γ_i, the law's JAM-calibrated SLUGGS deficit exceeds 2σ at every β in the bracket, on both footings. The minimum over the bracket is the quantity tested.

## Reported rows

- **R1:** the law and the rule, mean ± error and σ, at every β in the bracket and beyond it, on both footings.
- **R2:** per galaxy, the constant β in [−1, 0.99] that nulls the law's offset (or none), beside the galaxy's γ_i and any value above (NGC 5846).
- **R3:** the one constant β in [−1, 0.99] that nulls the law's mean offset (or none), on both footings.
- **R4:** with γ = 3 for every galaxy (CFG55's baseline), the law and the rule at β = ±0.5.
- **R5:** SLUGGS's population masses at β = ±0.5, with the published γ_i.
- **R6:** the four group and cluster centrals excluded, at β = +0.5.

## MUTATE

MUTATE=1 removes the deficit and keeps the scatter. On each footing, every galaxy's observed outer dispersions are multiplied by 10^(−D). D is the law's mean offset at the radial end of the bracket (γ_i, β = +0.5), computed in the same run from the unmodified data. The mean offset at β = +0.5 is then zero, so H1 must fail and the script must exit 1.

## Readings (declared)

- **H1 PASS:** orbital anisotropy inside the measured range does not rescue the law. R2 and R3 say what β the law would need.
- **H1 FAIL:** radially biased GC orbits inside the measured range bring the law's deficit below 2σ. The SLUGGS failure is then degenerate with the GC orbits, and the reading reports the β at which that happens.
- **The rule (R1)** is reported at every β. No verdict on the rule rests on this lane.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.
