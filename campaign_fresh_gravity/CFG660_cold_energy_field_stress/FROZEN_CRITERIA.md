# CFG660 FROZEN CRITERIA: the law as the hydrostatic equilibrium of cold energy's own stress

Date: 2026-10-12. Written and committed ALONE, before any CFG660 code exists in the repo. Nothing below may be edited after this
commit; later changes go in dated disclosures in the README. **ID block:** the owner reserved CFG660–669 for this chat
(2026-10-12), after the CFG640 collision.

κ = ½ is fitted. The footings (9.3603e-11 canonical, 1.1312e-10 alt) are judged separately and never pooled. The cold energy's
mass is required. No particle species. Not "theory closed". Nothing here will be phrased as "the data favour the framework".
Yardsticks are raw data only (SPARC rotmod). No knob scans: no constant beyond a₀ (through the law's kernel) and G.

## 0. What has been seen (stated before any choice below)

Exploratory scratchpad scripts by this author, 2026-10-12 (`eos_fluid.py`, `aniso_fluid.py`; to be committed in this lane as
`cfg660_*.py`, rewritten, not edited to change results):
- **Isotropic** field-dependent pressure P(|g|), fixed by the point-mass law (dP/dg = (g/4πG)(1/s − 1), s = dln g/dln g_N): on
  Hernquist spheres (a/r_M = 0.05–10, both kernels) the equilibrium sits +0.26 to +0.58 dex above the law at 0.5–10 a.
- **Field-aligned anisotropic** stress Π = P⊥ I + (P∥ − P⊥) ĝĝ with dP∥/dg = (g/4πG)(1/F′ − 1), P⊥ − P∥ = g(g − F⁻¹(g))/4πG
  (F′ = dg/dg_N along the law): reproduces the law to ≤ 2e-5 dex at 0.5–10 a. Inside about 0.01 a the inward integration
  departs like r⁻² (the growing mode of the ODE amplifying round-off). Deep limit P∥ = −g²/8πG, P⊥ = +g²/8πG.
- **Hand estimate, not computed:** for a medium whose stress depends on g only, the local dispersion along the field looks like
  ω² ≈ i k g/F′ − 4πGρ_c, i.e. growth ∝ √k (ill-posed). This lane computes it properly.
- **Not computed before this commit:** any SPARC score of either version; the WKB analysis with the background density
  gradient; the sympy identities.
- Known record numbers: the law's SPARC rms 0.1003 / 0.1013 dex (CFG634 T1 / CFG624 B, census edge; the edge lies beyond R_HI).

## 1. Definitions

Spherical symmetry, the framework's round rule (R6). g = |∇Φ| with ∇²Φ = 4πG(ρ_b + ρ_c) (G9: only real mass gravitates).
F is the law g = F(g_N) = ν(g_N/a₀) g_N with the record's ν_mono (CFG4_common, read-only); the exponential kernel is a reported
variant. s = dln F/dln g_N, F′ = dF/dg_N = s g/g_N.
- **Isotropic medium (I):** Π = P(g) I, dP/dg = (g/4πG)(1/s − 1).
- **Anisotropic medium (A):** Π = P⊥(g) I + (P∥(g) − P⊥(g)) ĝĝ, dP∥/dg = (g/4πG)(1/F′ − 1), P⊥ − P∥ = g(g − F⁻¹(g))/4πG.
- Equilibrium: radial Jeans with stress, dP∥/dr + 2(P∥ − P⊥)/r = −ρ_c g (I: P∥ = P⊥ = P).

## 2. Checks (in order; each states its consequence)

- **S1 (sympy, general F and general ρ_b(r)):** (A) in equilibrium implies g′ = F′(g_N) g_N′ exactly (the law along any spherical
  baryon profile). Required; if S1 fails the lane is VOID.
- **S2 (sympy):** (I) in equilibrium gives g′ = −s(2g/r − 4πGρ_b), and its residual against the law is s(ν − 1)·4πGρ_b·(g/g_N)/ν
  form (nonzero wherever ρ_b > 0 and ν > 1). Reported identity.
- **S3 (sympy):** deep limit of (A): P∥ → −g²/8πG + const, P⊥ − P∥ → g²/4πG: the stress equals minus the gravitational Maxwell
  stress (g⊗g − ½g²I)/4πG up to a constant. Reported identity.
- **S4 (kinetic realizability):** fix the zero point by P∥(g → 0) = 0 (no stress where there is no field; a kinetic gas has
  P → 0 where ρ_c → 0). Label **NOT KINETIC** if P∥ < 0 anywhere in g ∈ (0, 10 a₀] (a particle gas has P∥ = ρσ_r² ≥ 0);
  else **KINETIC POSSIBLE** with the anisotropy β(g) = 1 − P⊥/P∥ reported.
- **S5 (sympy, local WKB, well-posedness):** medium (A) with background ρ₀, ρ₀′, g₀ (hydrostatic), perturbation ∝ e^{i(kx − ωt)}
  with k along ĝ and k ⊥ ĝ, keeping the ρ₀′ term in continuity and δg from Poisson. Class **ILL-POSED** if max Im ω → ∞ as
  k → ∞ for some direction; **DUST-LIKE** if Im ω stays bounded by √(4πGρ₀)·O(1); **PRESSURE-STABILIZED** if every mode is stable
  at large k. Reported addendum: the same with an added kinetic pressure c_s²ρ (c_s² = V_f²/2 in the deep SIS), giving the
  large-k growth bound in units of 1/τ_ff.
- **N1 (numeric toy, Hernquist a/r_M ∈ {0.05, 0.3, 1, 3, 10}, both kernels):** (A) within 1e-3 dex of the law at 0.5–10 a.
  Required; else the lane is VOID (implementation). (I) reported.
- **D1 (DATA, raw SPARC):** the record's harness (CFG487's exec of CFG4/CFG45, read-only; Υ = 0.61, its points, weights and
  quality mask). Per galaxy, g_N(R) = g_bar from the rotmod columns treated as spherical, (r²g_N)′ by linear interpolation of
  r²g_N between measured radii; integrate (I) and (A) inward from the outermost good point with g = F(g_N) there; predict g at
  every good point. Galaxies with < 3 good points use the law for all three predictions. Score: the harness's weighted rms of
  log g_obs − log g_pred, per footing.
  - (A) must match the law's rms within 0.002 dex (implementation check; else D1 is VOID).
  - (I): **ISOTROPIC EXCLUDED** if rms_I − rms_law ≥ 0.03 dex on both footings; **CONSISTENT** if |rms_I − rms_law| ≤ 0.005 on
    both; else **TENSION**.
- **MUTATE (`CFG660_MUTATE=1`, separate outputs, exit 1 iff all bite):** M1, S1 with P⊥ − P∥ set to 0 must fail the identity;
  M2, D1's (A) integrator with the anisotropy term removed must reproduce rms_I within 1e-6.

## 3. Lane label

"LAW = EQUILIBRIUM OF A FIELD-ALIGNED STRESS (spherical): [S1/N1/D1-A]; ISOTROPIC: [D1 class]; KINETIC: [S4 label];
DYNAMICS: [S5 class]". No claim beyond spherical symmetry; non-spherical systems are stated as open.

## 4. Machine rules

Light: one process, < 2 GB, `nice -n 10`, `OMP_NUM_THREADS=1`; allowed while the 1024³ run is live.
