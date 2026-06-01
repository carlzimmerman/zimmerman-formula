# The surviving framework: a scaling-MOND cosmology from the Schwarzschild free-fall scale

**2026-06-01.** This is what is left standing after a full audit of the Z² program
(see `../README.md` for the post-mortem and `reviews/DATA_AUDIT.md` for the evidence).
It is **not** a Theory of Everything, and it does **not** derive the constants of
nature — those claims were numerology and are quarantined in `../ai_slop/`. It is one
real empirical anchor, one genuinely novel geometric reading, and **one falsifiable
prediction** that can be tested with real data.

---

## 1. The one empirical fact

From the real SPARC database (175 galaxies, 2807 points; `reviews/sparc_rar_honest.py`):

$$a_0 = (1.13 \pm 0.06)\times10^{-10}\ \mathrm{m/s^2},\quad \text{RAR scatter } 0.14\ \mathrm{dex}$$

This reproduces McGaugh+2016. It is the MOND acceleration scale — solid, real,
mainstream. Everything below is an attempt to *explain* this number and predict how
it behaves at high redshift.

## 2. The original formula (2026-03-17) and the novel refinement

The repo's first commit was a real observation: **a₀ ≈ cH₀** to an O(1) coefficient —
the 40-year-old Milgrom coincidence. The Zimmerman-specific content is the **value of
that coefficient** and its **geometric reading**:

$$\boxed{\,a_0 = \frac{cH}{Z},\qquad Z = 2\sqrt{8\pi/3} = \sqrt{32\pi/3}\approx5.789\,}$$

The genuinely novel piece — the one thing that came out of this audit rather than the
original numerology — is **what the coefficient is** (`reviews/schwarzschild_factor_and_density_fork.py`):

$$a_0 = \frac{c^2}{2R},\qquad R = \sqrt{\tfrac{8\pi}{3}}\,\frac{c}{H} = c\,t_{\rm ff}$$

the **Schwarzschild surface-gravity form** $c^2/2R$ of the cosmic **free-fall scale**.
Of the four candidate horizon readings, *only* this one carries the factor ½:

| reading | coefficient |
|---|---|
| de Sitter horizon surface gravity (cH) | 1 |
| de Sitter temperature / modified inertia | 2 (overshoots) |
| **Schwarzschild c²/2R of the free-fall scale** | **1/Z = 0.173 ✓** |

The ½ is Schwarzschild, the √(8π/3) is the free-fall-vs-Hubble clock ratio (Friedmann).
**Honest caveat:** R is *not* a literal black hole (the enclosed mass is 8π/3× the
Schwarzschild mass), so "Schwarzschild" is the functional form, a heuristic — the
coefficient 1/Z is **not derived from first principles**; the rigorous entropy routes
only *bracket* it (1/6 … 1/2π). 1/Z remains the single posited number.

## 3. The falsifiable prediction (with a real fork)

Because $a_0 = (c/2)\sqrt{G\rho}$ tracks a cosmic density, it **evolves**. Which density
forks the prediction — this is the payoff of the Schwarzschild reading:

$$\boxed{\,\frac{a_0(z)}{a_0(0)} = \begin{cases} E(z)=\sqrt{\Omega_m(1+z)^3+\Omega_\Lambda} & \text{(total density / apparent horizon)}\\[4pt] (1+z)^{3/2} & \text{(matter free-fall only — }\Lambda\text{ does not collapse)}\end{cases}}$$

Both are **H₀-independent and Z-independent** (the coefficient cancels in the ratio), so
the test is immune to the Hubble tension and to the M/L systematic. The two branches
separate cleanly: at z=1 the BTFR zero-point shifts by −0.25 dex (E(z)) vs −0.45 dex
((1+z)^1.5); standard constant-a₀ MOND predicts 0. **One measurement decides among all
three.** The honest test is `a0_evolution_pipeline.py` (self-anchored BTFR zero-point,
no monotonicity trick).

## 4. The relativistic completion

The classical scaling law needs a covariant home. The honest choice is **AeST**
(Aether-Scalar-Tensor; Skordis–Złośnik 2021): a real, Lagrangian, CMB-capable
relativistic MOND theory with $c_{\rm GW}=c$ (survives GW170817). Promoting its fixed
a₀ to a₀(z)=cH(z)/Z is the single new ingredient; because AeST's dust-mimicking sector
is shift-symmetric (a₀-independent), the scaling is plausibly CMB-safe — but the
Boltzmann re-fit is **unrun** and is the honest open theory task.

## 5. The ledger — every layer at its true confidence

- **REAL (data):** a₀ = 1.13×10⁻¹⁰ from SPARC. MOND phenomenology. *(reproduced here)*
- **NOVEL (this audit):** the ½ is Schwarzschild surface gravity of the free-fall scale;
  the density fork E(z) vs (1+z)^1.5. *(geometric, defensible, not first-principles)*
- **POSITED:** the coefficient 1/Z — one dimensionless number, hostage to H₀, bracketed
  but not pinned by entropy arguments.
- **OPEN, now sharpened:**
  - *(i) the coefficient* — **no uncontested route pins it.** Bare holography gives
    Newton (no a₀); MOND needs an extra volume-entropy ingredient. Verlinde's
    **contested** emergent gravity gives ≈cH/6; the geometric reading gives cH/Z by
    construction; the two agree to 3.5% and the H₀-hostage data cannot choose
    (`coefficient_from_horizon_entropy.py`). Neither $1/6$ nor $1/Z$ is *derived* — the
    coefficient stays the one posit. *(The prediction below is coefficient-free, so this
    does not touch it.)*
  - *(ii) AeST CMB consistency* — the background is provably a₀-independent (100θ\* =
    1.0411, unchanged); the one residual step is the perturbation-level Boltzmann re-fit
    with time-dependent a₀(z) (`aest_cmb_consistency.py`). Likely safe, not yet proven.
  - *(iii) the prediction itself*, **untested** for lack of real high-z deep-MOND kinematics.
- **DEAD (in ../ai_slop/, with the audit that killed it):** α⁻¹=4Z²+3 and all constant
  numerology; the 20.6 Gpc T³ topology; chirality/parity "detections"; topological
  ghosts; the protein/abiogenesis "resonance"; the Z² hurricane model; the E₆-orbifold
  "Theory of Everything" bolt-on. None of it survived real data.

## 6. What this is

A **single falsifiable claim** — a₀(z)=cH(z)/Z — resting on one real anchor (SPARC),
one novel geometric reading (Schwarzschild free-fall), and one honest open number (1/Z),
with a covariant completion (AeST) and a clean test (`a0_evolution_pipeline.py`) awaiting
real high-z rotation velocities. It can be **confirmed** (first genuine positive result of
the program) or **killed** (the null, constant a₀, wins) by a single dataset. That is the
entire honest content — no more, and no less.

---

*Reproduce:* `python reviews/sparc_rar_honest.py` (the anchor) ·
`python schwarzschild_friedmann_core.py` (every derivation, self-checking) ·
`python a0_evolution_pipeline.py` (the predictions) ·
`python a0_evolution_pipeline.py --selftest` (estimator check) ·
`python coefficient_from_horizon_entropy.py` (front 1: the coefficient) ·
`python aest_cmb_consistency.py` (front 2: CMB safety). ·
TOE scope and the emergent-gravity path: `TOE_REVIEW.md`.
*Foundations:* Milgrom 1983; McGaugh, Lelli & Schombert 2016 (SPARC); Skordis & Złośnik
2021 (AeST); Cai & Kim 2005 (apparent-horizon thermodynamics).
*Supersedes* the v12 "TOE" papers in `papers/`, which overreached by bolting on the
E₆-orbifold and constant-deriving claims now in `../ai_slop/`.
