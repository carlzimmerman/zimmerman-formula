# CFG689 addendum A1 — no ΛCDM assumption anywhere in the BAO chain (FROZEN before any CFG689 run or number)

Owner, 2026-10-20: "swing harder bro .. make sure no acdm assumptions in BAO". Base criteria 1c237145d and script 5bd973fb1 have
never run: a 1024³ job (NC1x) is live and the waiter has not fired. This addendum is committed before any run, so it changes the
design, not a result. It overrides the base file where they differ.

## A1.0 Audit: every inherited ingredient in the chain DESI table → CFG689 verdict
Rule (owner 10-10): ΛCDM late-time fit results, ΛCDM growth/nonlinear machinery and ΛCDM priors never enter a verdict. Pre-switch
physics (GR + photons + neutrinos + baryons + cold energy as cold matter, CFG654 principle) is the framework's own physics.
DESI numbers below were read directly on the arXiv HTML pages on 2026-10-20, not through a summariser, unless marked "reported by
the reading agent". DESI's own extraction settings, from those pages and the agent:
- fiducial = Planck 2018 ΛCDM;
- template = CLASS linear P(k) at the fiducial;
- damping Σ free with Gaussian priors centred on values calibrated on mocks;
- systematics already in the DR2 table errors: 0.1–0.22% (iso), 0.22–0.33% (AP).

| # | ingredient | where | class | treatment in CFG689 (after A1) |
|---|---|---|---|---|
| U1 | fiducial cosmology (Planck 2018 ΛCDM) for redshift→distance and template AP | DESI | ΛCDM late-time | bounded: P4 (our native background vs DESI's tested fiducial span) |
| U2 | BAO template = linear P(k), wiggle/no-wiggle split | DESI | pre-switch physics | native (same physics, A1-equivalent ω's); broadband marginalised by DESI |
| U3 | reconstruction with a fiducial ΛCDM growth rate f(z) and bias (DR1 Table 4: f 0.68–0.93) | DESI | ΛCDM growth | bounded: P5 (framework vs Newtonian, same pipeline) + DESI's own recon tests (P4); **removed at DR1 precision by B12** (pre-recon α_iso); removed fully by lane L2 |
| U4 | nonlinear damping Σ and peak shift calibrated on ΛCDM N-body | DESI | ΛCDM nonlinear | bounded: P5 |
| U5 | covariances from ΛCDM mocks | DESI | survey calibration (errors, not centres) | disclosed; removed only by L2 |
| U6 | galaxy-bias / HOD systematic from ΛCDM halo catalogues | DESI | ΛCDM halos | bounded by DESI's HOD tests (reported) + P5 particles vs gravitating field; removed only by L2 |
| U7 | Lyα forest: fiducial, template, mocks, contaminant models | DESI | mixed | reported from DESI; Lyα dropped in bracket B10 |
| D1 | **flat geometry** (Ω_k = 0) | CFG681–689 | ΛCDM/inflation; the framework has no flatness statement (THEORY_CANONICAL v2) | **REMOVED: curvature free in the primary (A1.1)**; flat kept as bracket F |
| D2 | CMB ω_b, ω_c (Planck TT,TE,EE+lowE column, extracted with a ΛCDM late-time model) | CFG654 A1 | pre-switch densities, ΛCDM-assisted extraction | B8: σ doubled; B5: BBN + h grid; B9: no CMB and no H0 at all |
| D3 | N_eff 3.044, standard recombination, CAMB r_drag | CFG654 | pre-switch physics | native |
| D4 | ρ_m ∝ (1+z)³ after recombination | CFG253 | framework result | B4 ±3% |
| D5 | Pantheon+ zHD: peculiar velocities from 2M++ linear theory (ΛCDM f) | CFG681 | ΛCDM growth | B7: zCMB with z > 0.03; BAO-only always reported |
| D6 | Pantheon+ BBC bias corrections from simulations at a fiducial cosmology | CFG681 | survey calibration | disclosed; BAO-only always reported |
| D7 | Σm_ν = 0 | CFG654 A1 | choice | B2 |

## A1.1 Primary becomes curvature-free
H(z)²/(100 km s⁻¹ Mpc⁻¹)² = ω_m(1+z)³ + ω_r(1+z)⁴ + ω_k(1+z)² + w(z), with ω_k ≡ Ω_k h² free and flat over [−0.25, 0.25].
χ = ∫ c dz/H. D_M = sinh(sχ)/s for ω_k > 0, sin(sχ)/s for ω_k < 0, and χ at ω_k = 0, where s = 100 √|ω_k| / c (h-free). D_L =
(1+z) D_M. Derived: h² = ω_m + ω_r + ω_k + w(0) and Ω_k = ω_k/h². E(z) includes the ω_k term. Parameters: 6 w-nodes + ω_k + ω_b + ω_c.
- **P0 (new):** posterior Ω_k (median, 68/95%). FLAT CONSISTENT if |median|/σ < 2; HINT 2–3; CURVATURE REQUIRED ≥ 3. Reported for
  BAO + SN and BAO only.
- P1/P2/P3 of the base file apply to the curvature-free primary. P2's constant model keeps ω_k free.
- **Bracket F** is the base file's flat primary, unchanged (BAO + SN and BAO only).
- **Verdict line:** both the primary and F are reported. If F's P1 or P2 class differs from the primary's, the verdict carries
  FLATNESS-SENSITIVE.
- Brackets B1–B6 run curvature-free.
- MUTATE: M1, M2, M3 run flat exactly as frozen (M3 is compared with F) and keep the frozen pass rules. M1k and M2k repeat M1 and M2
  with curvature free; they are reported (power), not pass/fail.
- K3 is unchanged (flat code path). New **K5:** at ω_k = ±0.05 (constant w = 0.31), D_M from this code matches an independent
  scipy.integrate.quad evaluation of χ, passed through the same sinh/sin form, to ≤ 1e-6 (relative) at z = 0.5 and 2.33.

## A1.2 New brackets
- **B7:** SN with zCMB instead of zHD (no peculiar-velocity model), keeping zCMB > 0.03; same STAT+SYS covariance restricted.
- **B8:** ω_b, ω_c σ doubled (0.00030, 0.0028); the late-time-agnostic extraction allowance (declared, not measured).
- **B9 (no CMB, no H0):** BBN ω_b 0.02193 ± 0.00022, ω_c free over [0.05, 0.25], flat, no h prior, w(z) ≥ 0 at every node (the
  tracking law needs ρ_DE ≥ 0). Reported: the 95% upper bound on ω_m and the H0 range. This is the positivity bound alone.
- **B10:** Lyα dropped (DESI galaxies + QSO only).
- **B12: no reconstruction anywhere (removes U3 at DR1 precision).**
  - Data: DESI DR1 pre-reconstruction α_iso (arXiv 2404.03000 Table 15, read on the HTML page 2026-10-20): BGS 0.9646 ± 0.0258,
    LRG1 0.9760 ± 0.0171, LRG2 0.9505 ± 0.0191, LRG3+ELG1 1.0027 ± 0.0114, ELG2 0.9882 ± 0.0176, QSO 0.9967 ± 0.0229.
  - These sit at the DR1 z_eff 0.295 / 0.510 / 0.706 / 0.930 / 1.317 / 1.491 (arXiv 2404.03002 Table 1).
  - Conversion: D_V/r_d = α_iso × (D_V/r_d)_fid, using this script's fiducial (checked by K7). The error is σ_α ⊕ 0.245% (DR1 Table 13,
    ξ(r) total systematic) × the fiducial value. Isotropic only; the tracers are taken as independent.
  - DR2 Lyα D_M/r_d and D_H/r_d are added unchanged (the forest is never reconstructed). SN, curvature and priors are as in the primary.
  - DR1 and DR2 share galaxies, so B12 replaces the DR2 galaxy/QSO points instead of adding to them.

## A1.3 P4: is our native background inside DESI's tested fiducial span? (U1, U3)
- At each tracer z, α_⊥ = (D_M/r_d)_native / (D_M/r_d)_fid and α_∥ = (D_H/r_d)_native / (D_H/r_d)_fid, from the primary best fit
  and DESI's fiducial (flat ΛCDM: h 0.6736, ω_b 0.02237, ω_c 0.1200, one 0.06-eV neutrino; arXiv 2503.14739 Table 1, read
  on the arXiv HTML page 2026-10-20), computed with this script's own distance code and CAMB r_d. Combined as α_iso = (α_⊥² α_∥)^(1/3)
  and α_AP = α_∥/α_⊥.
- INSIDE TESTED SPAN if at every tracer α_iso ∈ [0.963, 1.075] and α_AP ∈ [0.976, 1.029]: the grid offsets DESI's alternative
  fiducials c001–c004 covered (arXiv 2404.03000 Table 10, read on the HTML page 2026-10-20), where the residual bias was ≤ 0.1%
  (adopted fiducial systematic). Otherwise OUTSIDE: the fiducial-cosmology systematic is then extrapolated, and disclosed as such.
- **K7:** this script's fiducial reproduces DESI's own fiducial D_H/r_d = 8.6172 and D_M/r_d = 39.1879 at z = 2.33 (same Table 1)
  to ≤ 1e-3 (relative). This independently checks the distance code and the CAMB ruler.

## A1.4 P5: framework-native bound on the nonlinear / reconstruction assumptions (U3, U4, U6)
- Same-seed pairs from committed 1024³ runs: NC1x (theory-v2, native ICs, canonical) vs NCS0 (Newtonian S0, same ICs); T1x
  (canonical) and T2x (alt) vs cfg596 P0 S0 (inherited ICs). K6: seed, L, z_i and N must match, else that pair is not used.
- r(k, z) = P_fw(k)/P_S0(k) − 1 for k ≤ 0.33 h/Mpc at z = 1, 0.5, 0. P_fw is computed two ways: the gravitating field (P_grav) and
  the particles (P).
- Bound: Δα_NL ≤ max|r| × s_NL, with s_NL = 0.01. That is a declared conservative scale, larger than every nonlinear or
  reconstruction BAO shift in DESI's systematic budgets: theory 0.1% (iso) / 0.2% (AP) after reconstruction (DR1 Table 13; DR2) and
  Lyα 0.3% (DR2 Lyα §VI.1, reported by the reading agent and not re-read). NEGLIGIBLE if Δα_NL ≤ 0.1 × the smallest DESI fractional
  error in the table (0.70%, LRG3+ELG1 D_M), so ≤ 7e-4. Otherwise NOT NEGLIGIBLE: a bracket B11 then adds Δα_NL in quadrature to
  every BAO error, run afterwards as a separate disclosed commit.
- Disclosed limit: the box is L = 100 Mpc/h, so k < 0.063 h/Mpc is absent. Those modes are linear in both runs with the same
  background. The smallest available k bin is the trend check.
- P5 runs only after NC1x has finished (mode P5, last).

## A1.5 Lane L2 (proposed, separate id, NOT part of CFG689)
Re-measure BAO from the raw DESI DR1 clustering catalogues with a framework-native pipeline: native fiducial (CFG689 primary),
native template, NO reconstruction (pre-recon), free damping, no ΛCDM mocks for centres. Compare with DESI DR1's published values
per tracer. This removes U1, U3–U6 directly instead of bounding them.
- Data (per DESI DR1 papers, reported by the reading agent): the v1.2 LSS catalogues at
  data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/. The whole LSS tree is about 4.4 TB; only the per-tracer
  clustering catalogues plus a few random files would be fetched.
- The directory listing could not be opened (connection refused), so the download size is not yet known.
- DR2 catalogues are not public (expected by early 2027).
- Needs owner approval of an id and of the download.

## A1.6 Modes and order (waiter)
primary, F, M1, M2, M3, M1k, M2k, B1, B2, B3m, B3p, B4m, B4p, B5a, B5b, B5c, B6, B7, B8, B9, B10, B12, P5. The verdict needs primary,
F, M1–M3, K1–K7. Everything else is reported.

κ fitted; cold energy mass required; not theory closed; nothing here says the data favour the framework over ΛCDM.
