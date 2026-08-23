# Master Candidate Action — GR/York + cuscuton DE clock + elliptic QUMOND carrier + single metric

**Status: COMPLETE PROPOSED ACTION — CANDIDATE FIELD THEORY, NOT PROVEN.** This is the most
coherent single-action assembly of all developed pieces (CMC clock, dark-energy density/pressure,
redshift evolution, MOND dynamics, elliptic lensing carrier, single physical metric). It is *not* a
certified theory of nature. The remaining certification gates are listed in §Open; gate (2) is the
causal-evolution problem that the accompanying no-go
(`RESULT_york_cmc_mond_and_lensing_nogo.md`) addresses **adversely** — so this candidate and that
no-go are two views of one object.

## Fields
g_μν, T (cuscuton clock), Φ, Ψ (elliptic MOND potentials), λ (multiplier), matter ψ.
u_μ = −∇_μT/√(−∇_αT∇^αT),  h_μν = g_μν + u_μu_ν,  K_μν = h_μ^α h_ν^β ∇_α u_β.

## Action
    S = (M_Pl²/2) ∫ N√h ( K_ij K^ij − K² + ³R )                          [GR/York, ξ=1, η=0]
      + ∫ √−g [ μ_T² √(−∇T·∇T) − V(T) ]                                  [cuscuton DE clock]
      + (1/8πG) ∫ N√h [ −2 D_iΦ D^iΨ + a₀²(T) F(D_iΨ D^iΨ/a₀²(T)) ]      [elliptic MOND carrier]
      + S_m[g̃_μν, ψ]  +  S_CMC
    F'(s) = ν(√s),  ν(y) = √(1+1/y);   a₀²(T) = κ² c² G V(T)

Physical (single) metric:  d s̃² = −N² e^{2Φ} dt² + e^{−2Ψ} h_ij dx^i dx^j,  MOND branch Φ=Ψ=Φ_MOND.

## What it packages (all in one action, not separate patches)
- **DE sector (cuscuton):** ρ_DE = V(T), p_DE = μ_T²√X_T − V(T), w_DE(z) = −1 + μ_T²√X_T/V(T);
  T is NON-propagating (cuscuton) ⇒ protects the 2+0 count.
- **Acceleration scale (coefficient reading):** a₀(z) = κc√(G ρ_DE(z)) ⇒ **a₀(z)/a₀,₀ =
  [ρ_DE(z)/ρ_DE,0]^{1/2}**. For w=−1, ρ_DE=const ⇒ **a₀ = const** (no evolution). a₀ ∝ H only under
  DE-domination. This is the √ρ_DE footing fork — the correlated chain w_DE→ρ_DE→a₀→galaxy dynamics
  is the distinctive, DESI-testable prediction. (NB: the *clock* reading a₀ ∝ K = 3H — from
  `cosmology_flrw_2026.py` — is the OTHER fork; the two agree only under DE-domination and diverge at
  high z. Pick one and state the assumption; √ρ_DE is the cleaner.)
- **MOND:** D²Ψ = 4πGρ, D²Φ = D_i[ν D^iΨ] ⇒ ρ_ph = (1/4πG)D_i[(ν−1)D^iΨ] (the νρ source);
  g² = g_N² + a₀ g_N; single metric ⇒ Φ=Ψ ⇒ g_lens = g_dyn = νg_N, c_γ=c_GW=c at tensor level.
- **Background:** 3M_Pl²H² = ρ_m + ρ_DE, −2M_Pl²Ḣ = (ρ_m+p_m) + (ρ_DE+p_DE).

## Open (why this is candidate, not proven)
1. Full nonlinear Dirac algebra of the ENTIRE action (aux + cuscuton + matter coupled).
2. **Well-posed CAUSAL evolution of the elliptic MOND sector** — this IS the trilemma: the elliptic
   Φ is instantaneous and matter couples to it ⇒ a physical super-luminal channel unless the carrier
   is hyperbolized (which costs 2+0 → 2+1). Expected to FAIL causal viability at 2+0.
3. Full relativistic PPN / Cassini (inherited μ-function EFE-Q₂ ~ few-σ liability).
4. Cosmological perturbations from the same action.
5. Tensor propagation on nontrivial backgrounds.
6. Strong-coupling / cutoff analysis.
Ceiling: **κ, Z postulated/fitted, not derived** — only the a₀(z) proportionality (√ρ_DE) is
predicted.

**Honest label for a paper: "candidate field theory," never "proven theory."** The defensible,
certified subset + the no-go is in `RESULT_york_cmc_mond_and_lensing_nogo.md`.
