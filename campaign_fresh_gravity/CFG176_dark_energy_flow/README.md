# CFG176: what the flowing-vacuum picture implies for the dark energy (door 11; equation of state and w(z) only)

The frozen question is in `FROZEN_QUESTION.md`. Its body and Addendum 1 (the owner's "no rest mass, not a particle" clarification, relayed by the coordinator) were both written before any script. The script is `CFG176_de_flow.py` and runs in about 7 s. Results:

- **Main run:** rc = 0, 25/26 checks, no load-bearing failure. The one FAIL is the reported R-Q1f, an expectation miss kept as run: the contrast C came out at 1.1×10⁴–4.8×10⁵, not the 10³–10⁵ that was pre-declared.
- **`MUTATE=1`:** replaces the momentum inertia (ρ + p) with ρ (dust-like). This is the assumption behind CFG174's "swept column". It fails **H1 and H2**, rc = 1.
- **`MUTATE=2`:** replaces the accumulation with a steady deposit. It fails **H3 and H4**, rc = 1.

Each mode writes its own `.out` and `_results.json`.

## Bottom line

**A cosmological constant cannot flow.** For w = −1 the stress tensor is the same in every frame. It carries no momentum and cannot be compacted anywhere. So in this picture the flow is either:
- a description with no new content: 11A as GR's Painlevé–Gullstrand "river", or 11C as the cosmic time direction. Both give ΛCDM's background with w = −1; a dynamical time-flow adds only a rescaled cosmological G.
- a real medium, which then **is not a cosmological constant**: every flow observable scales as (1 + w).

**Can a real flowing medium supply the effect?** Tested against the committed DESI DR2 fits, the momentum such a medium can carry is capped by the null energy condition. Over the cosmic age it carries **at most 0.078** of the vacuum column. CFG174's picture needs **0.293** (0.354 on the alt footing). Closing that gap would need a 4–11% anisotropy in today's expansion.

**Three further results:**
- A massless (null or radiation-like) medium cannot be the dark energy.
- A compacted DE-like medium repels rather than attracts.
- The accumulation reading implies a phantom or decaying vacuum. That lies outside every DESI chain, and gives a₀(2.5) 0.6 dex below CFG6's band.

This is a scoped no-go for a flowing dark energy in GR. It is not a no-go for a flow that couples to gravity non-minimally; that is where the door-11 variants CFG171–173 must go. κ = ½ stays FITTED. The dark mass is still required (door-11 addendum 2). Nothing here says the theory is closed or that the data favour the framework over ΛCDM.

## Results

| Q | result |
|---|---|
| **1 A moving vacuum** | **Sympy results.** T(u) is independent of u, and boost-invariant, **iff ρ + p = 0** (S1a, S1b). For w = −1 every timelike vector is an eigenvector, so there is no rest frame (S1c). The CMB-frame momentum density is g = (1+w)ργ²β (S1d). The energy equation u·∇ρ = −(ρ+p)∇·u, so compaction scales as 1 + w; a Λ-vacuum is rigid (∂ρ = 0), and for constant w, ρ ∝ n^{1+w} (S2). **For any NEC-respecting stress, g/e ≤ (1 + w_∥)/2.** A w = −1 medium given an energy flux is Hawking–Ellis type IV (eigenvalues −ρ ± iq) and violates the NEC (S3). In FRW a DE flow relative to the CMB decays as γ²v ∝ a^{3w−1}, with an e-fold time of 4.4 Gyr at w = −0.75; it must be driven (S4). **Minimum departure needed to carry CFG174's column R:** 1 + w_∥ ≥ 2R = 0.59 / 0.71 for any medium. For a perfect fluid, the CMB-frame 1 + w_eff = R(1/β + β/3) ≥ 0.39 / 0.47, reached only as β → 1 and with anisotropy Δ = Rβ (S5). At 600 km/s the rest-frame 1 + w would be 146, violating the dominant energy condition, which needs β ≥ 0.15 / 0.18. **Active density ρ(1 + 3w):** a compacted w < −1/3 medium **repels**. Above the threshold speed it attracts, e.g. β > 0.85 at w = −0.75. To present the law's density at r_M (C = 1.1×10⁴–4.8×10⁵ ρ_Λ, ∝ M^−½), a DE-like medium must be volume-compressed by 10^16–10^23 at 1 + w = 0.25. |
| **2 11C, time direction** | With T = −ρ_Λ g the Hubble-flow identification adds nothing: ΛCDM, w = −1, a₀ flat (branch A). For a dynamical unit vector along the Hubble flow, minisuperspace in sympy gives K₁ = 3H², K₂ = 9H², K₃ = 3H², K₄ = 0. That yields **H² = 8πG(ρ_m + ρ_Λ)/[3(1 + β/2)]**, β = c₁ + 3c₂ + c₃, with the matching acceleration equation. The flow's energy −(β/2)ρ_crit tracks H² (w_flow = w_total), so **the shape of H(z) is exactly ΛCDM's (w_DE = −1)**. The only content is G_cos = G/(1 + β/2) (S6, H5). The θ-channel (stopping the expansion in bound regions) would need \|β\| ≥ 1.6×10⁴–4.9×10⁵ to present the law's density; scoped to the homogeneous term. |
| **3 Accumulation (CFG174)** | **3-I, density tie** (a₀ ∝ t ⇒ ρ_DE ∝ t²), solved self-consistently. The result is **phantom at every z**: w = −1 − 2/(3Ht), w₀ = −1.647, w → −2. CPL (−1.70, −0.52); H₀t₀ = 1.030; H(0.5) is 13% below ΛCDM. The weighted chain mass with w₀ ≤ −1.647 is 0 in all three combinations; the Gaussian-proxy distance is 27–36σ, against 3.0–4.3σ for ΛCDM's point (H3). a₀ = −0.34 / −0.53 / **−0.75 dex** at z = 0.85 / 1.5 / 2.5. That is **0.60 dex below CFG6's band** [−0.153, +0.268] (all DE branches, all three combinations, 16–84%) (H4). **3-II, the vacuum pays** (a decaying non-HT vacuum). For f_dep = 0.01–1: w₀ = −0.997 to −0.606, but **wa = +0.04 to +0.44 (w rising into the past)**. Every chain has p(wa ≥ model) = 0.000 and p(wa > 0) ≤ 0.0006. a₀(2.5) ≈ −0.71 dex. |
| **4 Bounds on 1 + w and the flow** | **Committed (CFG6):** DESI DR2 CPL 1 + w₀ = 0.248 / 0.162 / 0.333 (DESY5 / Pantheon+ / Union3), crossing w = −1 at z ≈ 0.36–0.44 in 99.8–100% of the posterior. Healthy thawing (posterior-conditioned) gives w₀,eff −0.88 to −0.95. ΛCDM gives 0. **From the committed chains:** 1 + w₀ 97.5th percentiles are 0.36 / 0.27 / 0.51, and wa < 0 at 97.5%. **Momentum today:** g/ρ_DE ≤ (1+w₀)/2 ≤ 0.18 / 0.14 / 0.26 (97.5%), and ≤ 0.27 / 0.21 / 0.38 for a perfect fluid at β → 1. Taken alone, today's rate would reach R in 26% of Union3's posterior. **Integrated over the history** (the fits' crossing kills the carrying at z ≳ 0.4), the perfect-fluid bound at 97.5% is **0.049 / 0.035 / 0.078**; the thawing best nodes give 0.039 / 0.016 / 0.019. Against R = 0.293 that is 3.7× short at best and 6–16× short at the medians (H2). Making up the shortfall through anisotropic stress needs σ/H₀ = 0.37Δ = 0.04 / 0.11 (Bianchi I, S7). The observational shear bound is not in the record and is not scored. |
| **5 No rest mass (Addendum 1)** | A traceless (massless) medium has isotropic **w_eff = 1/3 in every frame**. A null flow has w_∥ = 1, dilutes as a⁻⁴ and has active density +2e (S8). **It cannot be the dark energy.** Carrying the column today it needs Ω_null = 0.20 / 0.24. It would dominate matter before z = 0.54 / 0.28 and raise H(2.5) ×1.77 / ×1.89 (H6). That is about 2200–2700× the CMB-plus-neutrino density; T_CMB and N_eff are standard values, reported only. **11A's river** (PG metric, any v(r); S9) has p_r = −ρ, ρ = (rv²)′/(8πGr²). With v² = 2GM/r + H²r² it is pure Λ, so the river is a frame, not a medium. The linear superposition needs a **negative-energy** medium −3H√(2GM)/(8πGr^1.5) (219–1230 ρ_Λ at r_M), and its pull there is only 0.001–0.005 a₀. |

**Stress-energy each reading needs:**
- **11A:** M1 (a GR frame, no content), or a WEC-violating medium.
- **11B′:** M3, a field flow with 1 + w > 0 bounded by the DESI fits (H2); or M2, massless and excluded as dark energy (H6).
- **11C:** M1 or M4, a preferred-frame vacuum with T ∝ g. This gives w = −1 and only G_cos; PPN α₁ and α₂ are door gate G6 and not scored here.
- **Accumulation:** a phantom dark energy (3-I) or a non-HT decaying vacuum (3-II), both excluded by the chains.

## DERIVED / POSTULATED / OPEN

- **DERIVED** (sympy or numerics in the script):
  - S1–S9: the vacuum's lack of a rest frame, momentum and compaction; the NEC momentum bound; the type-IV result; FRW tilt decay; the boosted-fluid CMB-frame formulas; the aether minisuperspace; the Bianchi-I shear equation; traceless ⇒ w_eff = 1/3 and null dust ∝ a⁻⁴; PG-river stress.
  - Every number in the table.
  - Controls: C1 and C2 reproduce CFG174's R and a₀(z) (difference 0); C3 reproduces CFG6's B5 crossing fractions (difference 0); C4 is an FRW Ricci sanity check.
- **POSTULATED** (these are the readings under test, not results):
  - a₀ ∝ t (CFG174's accumulation).
  - The density tie a₀ = κc√(Gρ_DE) for 3-I.
  - A deposit ∝ t per comoving volume, dust-like, drawn from an intrinsic-w = −1 vacuum, with f_dep free (3-II).
  - CFG174's column R, meaning a flow at c over t₀ against a constant ρ_Λ, as the benchmark.
- **FITTED:** κ = ½.
- **OPEN:**
  - A medium that violates the NEC, for which there is no momentum bound. The DESI CPL fits are themselves phantom at z ≳ 0.4, and following them needs a ghost or braiding (CFG6 B5).
  - A flow whose boost is not its stress-energy (non-minimal coupling). This is the door-11 variants' job.
  - A focused, inhomogeneous flow. The cosmic-mean bound does not apply directly, although compaction still scales as 1 + w.
  - Perturbations (G2 is undefined here).
  - The observational anisotropy bound.
  - The record's own khronon G_cos, and the aether's G_N and PPN (not computed).
  - A unified dark fluid whose w depends on compaction (Chaplygin-type, from memory). This is the natural escape from Q1f, and CFG43's barotropic obstruction is the record's closest result.

## Exact hypotheses (scope)

- **Gravity:** GR with minimal coupling, used for the active density, PG, Bianchi I and FRW.
- **Q1:** perfect fluid for the tables, tilt decay and compaction, with constant w for the latter two. Any stress obeying the NEC for the momentum bound. The flow is homogeneous relative to the CMB frame.
- **Q2:** Einstein-aether terms c₁–c₄ with the vector along the Hubble flow, on the FRW background only. A khronon is identical on FRW.
- **Q3:** flat, no radiation, Ω_m = 0.3111 and H₀ = 67.66 held fixed as in CFG174. This is a toy: a real fit would move them.
- **Q4:** the committed thinned chains, flat, no radiation. w(z) is CPL, and phantom epochs are clipped to zero carrying, which gives an upper bound. The thawing rows come from CFG6's own solver at its posterior-conditioned best nodes.
- **Q5:** T_CMB = 2.7255 K and N_eff = 3.044 are standard values, not committed, and are used for a reported ratio only.

## Reading notes for other owners (flagged, not edited)

1. **CFG174 Q1.** "The vacuum column swept at c" gives a Λ-vacuum dust-like inertia. The relativistic energy flux of a w-medium is (1+w)ργ²βc³, which is zero for Λ. CFG174 already declared its Q1 pass to be the a₀–Λ coincidence restated. This lane quantifies the point: with the committed DESI fits, a NEC-bounded flow carries at most 0.078 of that column, and MUTATE=1 here is exactly that assumption.
2. **The door-11 gates file, "Target" line.** It writes the P2 kernel as ν = ½ + √(¼ + a₀/g_N). The record's P2 (`CFG4_common.nu_p2`, CFG44, used by CFG174) is ν = √(1 + a₀/g_N). This lane uses the record's form.

## Disclosures

- **First debug run:** rc = 1. S9 failed only because r was declared real rather than positive, so sympy would not reduce √(1/r)·r⁻¹ to r^−3/2. The chain covariance also printed spurious Accelerate-BLAS matmul warnings. I fixed r to be positive and replaced the matmul with explicit sums; no number changed.
- **R-Q3II tolerance.** After the first MUTATE pair, the reported check R-Q3II was seen to pass in MUTATE=2 on floating-point noise (wa = +5.8×10⁻¹⁶). A 1e-6 guard was added. It cannot affect the main run, where wa ≥ 0.04, and it now fails in MUTATE=2 as it should.
- **Final order and determinism.** The final sequence was MUTATE=1, then MUTATE=2, then main. The main .out is byte-identical to the run before the guard.
- **Literature from memory, not re-read:** the Einstein-aether G_cos form (Carroll & Lim 2004); the Hawking–Ellis types; ghost condensate; Chaplygin/UDM fluids. G_cos was re-derived here; the others are only cited.

## Reproduction

From the repository root:
```
MUTATE=1 python3 campaign_fresh_gravity/CFG176_dark_energy_flow/CFG176_de_flow.py   # rc 1 (H1, H2)
MUTATE=2 python3 campaign_fresh_gravity/CFG176_dark_energy_flow/CFG176_de_flow.py   # rc 1 (H3, H4)
python3 campaign_fresh_gravity/CFG176_dark_energy_flow/CFG176_de_flow.py            # rc 0
```
The script reads CFG6_common.py, CFG6's results JSON, the committed thinned DESI chains and CFG174's results JSON, all read-only. It writes only in this directory and writes no bytecode.


## Corrections after the independent referee CFG195 (e6cd64049; re-run in a scratch copy by the orchestrating session, all outputs identical; appended 2026-09-29)
The referee reproduces this lane's numbers to about 1e-5, including 0.078 (Pantheon+ 0.0490 / DESY5 0.0345 / Union3 0.0781). Corrections to the framing:
1. **0.078 is a perfect-fluid number.** The null-energy-condition (NEC) maximum is g/e = 0.866 (1 + w_iso), giving 0.057 / 0.040 / 0.090, still 3.2× below the needed 0.293.
2. **The DESI total w bounds a flow only if every component respects the NEC.** With a phantom compensator (w ≥ −2), R is reached at total 1 + w = 0.05 with a phantom fraction of 0.29. Without one, R is never reached. The CPL posterior is phantom for 65–71% of cosmic time, and those epochs are clipped to zero carrying.
3. **"A Λ vacuum cannot be compacted"** needs the separate conservation of the dark-energy stress (a premise), which the bottom line did not state.
4. **The |β| range across both footings** is 1.55e4–6.53e5; the 1.6e4–4.9e5 quoted is canonical-only.
5. **Two gaps and one counterexample.** The repo holds no DESI-alone or no-SN chain, so that case is untested. The referee's free-form attack A3 finds a NEC-respecting ρ_DE(z) that mimics the CPL background and reaches the needed column when Ω_m is free; it is kept as a failure of this lane's bound.
