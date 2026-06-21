# SETUP — AeST |Φ|-boundary cluster door: exact equations + the boundary-Φ mechanism

*The DERIVE+SET-UP leg of the deferred Durakovic–Skordis 2024 calculation. Equations
extracted verbatim from the source PDFs (pdftotext); deep-MOND limit verified symbolically
(`aest_phi_setup_verify.py`, all checks EXACT). Framework footing: a0 = c²√(Λ/32π) =
9.36e-11 (INPUT, quarantined, never derived). The AeST {µ (=K₂/K_B-set), λ_s, a0} are FREE
inputs; a0 imported from the framework, µ CMB-pinned (1/µ ~ 1 Mpc). Both-ways enforced.*

## 1. The exact weak-field AeST field equations (the PDEs/ODEs to solve)

**Source 1 — Durakovic & Skordis 2024, arXiv:2312.00889, JCAP 04 (2024) 040** (the cluster
paper). The two-component static weak-field AeST equations reduce, in spherical symmetry
(curls negligible), to a **single modified-Helmholtz / AQUAL-plus-mass equation** for the
gravitational potential Φ:

> **div[ M(x) grad Φ ] + µ̃² Φ = 4πG_N ρ_b** &nbsp;&nbsp;(Eq 2.33), &nbsp; x ≡ |grad Φ|/a₀
>
> spherical (Eq 2.40): **(1/r²) d/dr[ r² M(x) Φ′ ] + µ̃² Φ = 4πG_N ρ_b(r)**

- **Interpolation** M(x) (Eq 2.39, simple-µ / λ_s→∞ choice):
  **M(x) = (−1 + √(1+4x)) / (1 + √(1+4x))** — limits M→1 (Newton, x≫1), M→x (deep-MOND, x≪1).
- **Mass term** µ̃² = (1+β₀)µ² (Eq 2.35), β₀ = 1/λ_s (Eq 2.36). The **+µ²Φ** sign makes it a
  **modified Helmholtz operator** — this is the NEW AeST term, absent from AQUAL/Bekenstein–Milgrom.
- **Two-component non-singular form** (Eq 2.43–2.44), used to integrate through the |Φ′|=0
  oscillation nodes: `(1/r²)d/dr[r²(Φ′−χ′)] + µ̃²Φ = 4πG_Nρ_b`, `β·χ′ = Φ′`, with β = 1+J_Y.
- **Hamiltonian / canonical-momentum form** (Sec 3): evolve P_Φ instead of Φ to remove the
  *apparent* singularities at the zeros of Φ′ (DS24's key numerical device; confirmed it is
  what the prior corpus solver `cluster_aest_massterm_BVP_implB.py` already uses).

**Source 2 — Blanchet & Skordis 2024, arXiv:2404.06584, JCAP 11 (2024) 040** (Khronon, the
SAME weak-field structure). Modified Poisson **div[(1+J_Y) grad ϕ] + µ²ϕ = 4πG ρ** (Eq 3.21),
MOND function **f(y) = 1 + J_Y(Y)** (Eq 3.22), y ≡ |grad ϕ|/a₀, Y ≃ a₀²y²/c⁴, **free function**
(Eq 3.23):

> **J(Y) = Λ − Y + (2c²/3a₀) Y^{3/2} + O(Y²)**  ⟹  J_Y = −1 + (c²/a₀)√Y  ⟹  **1+J_Y = y** (deep-MOND).

BS24's (1+J_Y) ≡ DS24's M(x): **the same forced √-law interpolation, the same +µ²ϕ mass term**
(BS authors: "very similar to AeST [59]"). **a₀ enters in EXACTLY ONE place — the coefficient of
the forced Y^{3/2} term** — into which the framework plugs 9.36e-11. Λ is J's additive constant
(orthogonal to a₀; Λ ~ a₀²/c⁴, BS24 below Eq 3.7).

**Source 3 — Skordis & Złośnik 2021, arXiv:2007.00082, PRL 127 161302**: the AeST action
(one metric + unit-timelike aether A_µ + shift-symmetric scalar) whose static weak-field limit
the above two papers reduce. a₀ lives only in the spatial-gradient Y-sector (provably absent
from linear cosmology — the a₀↔CMB decoupling).

## 2. The boundary-Φ mechanism (what the |Φ| dependence IS + why it enhances clusters)

**Why a |Φ|-boundary dependence exists at all.** Pure AQUAL/MOND `div[M(x)gradΦ]=4πGρ` is
**shift-invariant** (Φ→Φ+const; only gradΦ appears) — the zero-point of Φ is unphysical. The
AeST **+µ²Φ term breaks that shift symmetry** (Φ appears *undifferentiated*; sympy-confirmed:
shift changes it by C·µ²≠0). So **the absolute boundary/asymptotic level of Φ becomes physical**
and feeds back as an effective source density −µ²Φ/(4πG).

**What the "boundary value of the gravitational potential" is, precisely (DS24):**
- vacuum/extended-source case → the **shift ΔΦ** (Eq 2.42, Fig 7 left);
- **isothermal (cluster) case → the asymptotic constant χ∞** (Sec 3.5, Fig 7 right;
  Appendix B.2 iterates the inner BC until Φ(r→large)→χ∞).

It is a **finite-radius integration constant of the Helmholtz operator**, NOT a local |Φ|/c²
coupling. Because the operator is Helmholtz, the homogeneous solutions are oscillatory
`[C₁cos(µr)+C₂sin(µr)]/r`, both decaying as 1/r, so **Φ(∞)→0 does NOT select a unique solution** —
a one-parameter family survives, parametrized by χ∞.

**Why it enhances clusters (DS24, verbatim).** Abstract: *"the AeST RAR … can display a peak,
an enhancement with respect to the MOND RAR, at an acceleration range determined by [1] the value
of the AeST weak-field mass parameter, [2] the mass of the system and [3] the boundary value of
the gravitational potential. For lower accelerations, the AeST RAR drops below the MOND
expectation, as if there is a negative mass density."* Sec 3.5: *"The peak is made larger by a
**more negative shift** of the potential."* Deferral (conclusion): *"a full quantitative
comparison with observations will require **going beyond the isothermal case** … left for future
work."* Mechanism: a deeper (more negative) boundary Φ ⟹ a more positive −µ²Φ phantom density
over the core ⟹ a RAR peak above MOND. **Clusters sit in a deeper integrated potential than
galaxies — the one scalar where clusters out-rank galaxies** (density orders backwards; the no-go).

## 3. Parameters (AeST inputs + framework values)

| symbol | meaning | value | status |
|---|---|---|---|
| a₀ | MOND scale = coeff of forced Y^{3/2} | **9.36e-11 m/s²** | framework INPUT, quarantined (AeST adopts 1.2e-10 pheno; −22%, both in RAR band) |
| Λ | additive const of J(Y) | 1.090e-52 m⁻² | from a₀ (=3Ω_ΛH₀²/c² to ratio 1.000); orthogonal to a₀ in J |
| µ | AeST weak-field mass (=√[2K₂Q₀²/(2−K_B)]) | 1/µ ~ 1 Mpc | **FREE**, CMB-pinned (BS24 Eq 3.25: µ⁻¹ ≳ 1 Mpc) |
| λ_s | screening (β₀=1/λ_s) | →∞ (simple-µ) ⟹ β₀=0, M=Eq 2.39 | **FREE** |
| χ∞ / ΔΦ | boundary value of Φ | **the lever** | DS24 leave it FREE; crux = is it cosmologically pinned? |

µ̃² = (1+β₀)µ²; oscillation onset r_C ~ (r_M/µ²)^{1/3}, r_M = √(G_N M/a₀) (DS24 2.41–2.42, BS24 3.24).

## 4. Deep-MOND check (verified, EXACT — `aest_phi_setup_verify.py`)

- DS24: M(x→0) = x (deep-MOND), M(x→∞) = 1 (Newton) — sympy exact.
- BS24: 1 + J_Y = y exactly in the deep-MOND limit (J_Y = −1 + (c²/a₀)√Y, √Y = a₀y/c²).
- Force law: deep-MOND `|gradΦ|²/a₀ ~ g_N ⟹ g_obs = √(g_N a₀)` — **identical to the framework's
  dS-Unruh modified inertia.** The forced n=3/2 exponent is the framework's √-law.

## 5. The equations staged for the full non-isothermal solve (the deferred step)

Solve (two-component non-singular Eq 2.43–2.44, OR Hamiltonian P_Φ form), spherical, REAL
baryon ρ_b(r):
- (a) **rich cluster** M500=1e15, β-model gas + Hernquist stars, embedded with the cosmic
  Φ-boundary χ∞ → boost η(R500)=g_AeST/g_MOND; does it close the ~30–49% core residual?
- (b) **SPARC-like disk** (shallow Φ) → galaxy-veto: RAR scatter shift must stay < 0.05 dex.
- (c) **Solar System** (deep local g≫a₀, shallow integrated Φ) → Cassini |γ−1|.
- Report magnitude vs the naive local |Φ|/c² coupling (~0.003%; cluster |Φ_bar|/c² ≈ 1.1e-5).

**The crux χ∞ must decide:** is χ∞ **physics-pinned** (cosmological matching: turnaround radius,
Λ / mean-field) to a value giving the cluster peak with NO per-cluster tune AND galaxy+Cassini
safe (→ closes clusters, paper FLIPS), or a **free per-object knob** (→ descriptive, no-go holds)?

## 6. Prior corpus this builds on (do NOT re-derive — extend)

- `CLUSTER_AEST_MASSTERM_BVP_implB_2026-06-14.md` + `cluster_aest_massterm_BVP_implB.py` — already
  solved this SAME +µ²Φ Helmholtz eq (two independent methods); found a **NON-tuned/physical
  boundary gives a DEFICIT (~0.2–0.5×, even repulsive for a realistic deep-MOND profile) at R500,
  NOT the +2 boost**; η=2.15 reachable only by a per-cluster χ∞ tune; galaxies stay MOND-pure at
  1/µ=1 Mpc but clusters need a *larger* µ → the Mistele-2023 galaxy↔cluster squeeze.
- `cluster_chi_out_cosmological_matching.py` — tried to PIN χ∞ by cosmological turnaround
  matching; χ∞ scales ~M^{2/3} (universal function, not per-object) but the resulting η-trend is
  the wrong shape vs flat eRASS1.
- `CLUSTER_GRAVITY_LAST_DOORS_2026-06-20.md` (Route A) — the |Φ|/c²-depth-keyed boost is the
  **strongest no-particle door** (closes G1 magnitude + ~flat shape, galaxy-safe at the floor,
  Cassini-safe) but dies on **G3 naturalness** (needs amp ~1.5e5 vs O(1)); the framework's
  dS-Unruh MI is a function of g alone (T_eff~cH_Λ, horizon-set, **blind to local Φ**), so no
  framework field carries the required coupling.

**Net for the solve leg:** the full non-isothermal numeric solve on the framework's own
a₀=9.36e-11 with REAL baryon profiles must re-decide whether the NONLINEAR χ∞ boundary mechanism
delivers MORE than the naive ~0.003% local coupling — and whether any physics-pinned χ∞ closes
the cluster core without a per-cluster tune, without breaking galaxies, and within Cassini.
Both-ways: prior banked work leans toward "deficit / per-cluster-tune / naturalness-fail," but
that was the bare mass-term route; this leg supplies the exact equations to test it cleanly with
real profiles. Do not manufacture a close; do not high-priest the AeST authors' flagged lever.

## Sources
- Durakovic & Skordis 2024, arXiv:2312.00889, JCAP 04 (2024) 040 — Eqs 2.33, 2.35, 2.36, 2.39,
  2.40, 2.42, 2.43–2.44; Sec 3.4–3.5; abstract + conclusion (boundary-Φ + deferral, verbatim).
- Blanchet & Skordis 2024, arXiv:2404.06584, JCAP 11 (2024) 040 — Eqs 3.21, 3.22, 3.23 (J(Y)),
  3.24, 3.25; deep-MOND J ~ Λ − Y + (2c²/3a₀)Y^{3/2}.
- Skordis & Złośnik 2021, arXiv:2007.00082, PRL 127 161302 — the AeST action / a₀ slot.
