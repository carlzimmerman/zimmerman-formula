# CFG938: the cold-energy medium as a relativistic continuum (frozen criteria, committed alone)

Block CFG930–939 (reserved 2026-10-20, owner: "solve the P thing with agents rigorously … find a breakthrough").
This file is written and committed **before** any derivation output, script or number. It fixes the questions,
the checks, the controls and the class rule. Any later change is a dated, labelled amendment in this directory.

**Settings.** κ = ½ FITTED (never derived). Footings a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m s⁻² (alt), never
pooled. Cold energy's mass is required; no dark-matter particle species may be added; if the construction turns out
to be one, that is reported, not hidden. No ΛCDM or standard-MOND yardstick in any verdict. Not "theory closed";
never "the data favour the framework".

**Inputs (read only).** THEORY_CANONICAL_2026-10-14.md S2/S3 (the action, the identification ∇·P = ρ − ρ̄,
∂ₜP = −j); CFG678 gates and scorecard (criteria 72577e919); CFG660/661 (field-aligned stress, ill-posedness);
CFG723 (medium with P = displacement; particle-in-disguise); CFG847 (slip estimate, largest 1.9e-5, class line
1e-2); CFG897 (covariant stiffness on FRW); CFG888 (no self-gravity under ID); CFG932 (settling non-conserving);
CFG638 (settling moments); CFG770/820 (stiffness, L* window [24 pc, ≳ 1 kpc]); astra's
sol61_push/cold_completion_2026_10_20/GRAVITY_ACTION_AUDIT.md and REVIEW_COMMON_ACTION.md (cited, never edited).
CFG935 has no LEDGER row at freeze time; it is not compared and its directory is not touched. CFG939 (sibling lane,
multi-stream displacement) is not duplicated: this lane is single-stream by construction and says so.

## The construction to be tested

Effective field theory of a continuum: comoving label fields φ^I(x^μ), I = 1..3; B^{IJ} = g^{μν}∂_μφ^I∂_νφ^J;
n = √det B; u^μ the unit kernel of ∂_μφ^I (u^μ = ε^{μαβγ}ε_{IJK}∂_αφ^I∂_βφ^J∂_γφ^K / (6 n √−g)); conserved current
J^μ = n u^μ. Signature (−+++). Linear displacement ξ = x − φ.

**Declared internal symmetry: FLUID** (volume-preserving relabellings φ → ψ(φ), det ∂ψ/∂φ = 1, plus internal
shifts). Reason, stated before deriving: S3 says the medium is collisionless rest mass, which has no shear rigidity.
The SOLID alternative (internal SO(3) + translations only) is examined where it changes an answer (background
isotropy; transverse stiffness) and reported as an alternative, never mixed into the fluid's scores.

## Questions (each answered in DERIVATION.md with a sympy check in the script)

**Q1 Background.** On flat FRW with φ^I = x^I (comoving):
- (a) B^{IJ}, n, u^μ and T^μ_ν exactly; homogeneity and isotropy (T^i_j ∝ δ^i_j) for the fluid F(n) and for a generic
  solid F(τ₁, τ₂, τ₃);
- (b) the medium's rest frame vs the cosmic frame;
- (c) w for F = −m c² n;
- (d) the value of P (and of any tether-sector scalar) on FRW;
- (e) a precise answer to "why is there no anisotropy during expansion?".

**Q2 Matching to S2.** Find the continuum term(s) whose static, non-relativistic, weak-field limit gives
−|∇Φ − K P|²/(2K) − ρ_b Φ − W_rem(u) − (γ/2)|∇P|² with ∇·P = ρ − ρ̄:
- (a) the exact (nonlinear) covariant object that P is, and its sign/normalisation relative to ξ;
- (b) whether the tether P·∇Φ is forced (equivalence principle) or chosen;
- (c) whether W_rem (or W_full = W_rem + u²/2K) can be a function of the strain B^{IJ} (or of any local function of
  φ's derivatives); if not, what minimal extra structure is forced, and what u = K|P| is covariantly;
- (d) what the stiffness (γ/2)|∇P|² is for a fluid and for a solid, and what it does on the FRW background
  (early-universe energy for the local version, with declared inputs: Ω_c/Ω_b = 5.364, Ω_b 0.0493, H₀ 67.4,
  T_CMB 2.7255 K, N_eff 3.046, z_BBN = 4e8, BBN tolerance 10% of the radiation density);
- (e) a forced-vs-chosen table.

**Q3 Conservation.** ∇_μT^{μν} = 0 for the derived action (general identity, checked symbolically on the static
sector). What CFG638's settling drift v_s = −ατ∇ψ becomes: absent, needs a dissipative extension (entropy/heat
bookkeeping stated), or appears as conservative dynamics toward the law. Compare with CFG932 Q1.

**Q4 Lensing and slip.** The static weak-field (Φ, Ψ) sourced by the medium + tether sector; anisotropic stress;
the slip on CFG847's five systems (its masses/radii), both footings, in two measures declared now:
- s_∇ = |Φ′ − Ψ′| / Φ′ (lensing vs dynamical acceleration);
- s_847 = 8πG r² |Π| / (c² v_c²) (CFG847's estimator), where Π is the largest magnitude stress component.

**Q5 Well-posedness.** For the linearised continuum about a static medium (WKB, rest frame):
- the dispersion relation;
- speeds² ≥ 0;
- positive kinetic (inertia) matrix;
- growth rates bounded independent of k (Hadamard).
Is CFG678's B3/A2 failure (CFG660: growth ∝ √k) cured, and under what conditions?

**Q6 Scorecard.** All 20 CFG678 gates: PASS / FAIL / CONDITIONAL / UNTESTED / DECLARED, with source, under
CFG678's own rules (no new thresholds; recipes score UNTESTED; both footings).

**Q7 "Particle in disguise" (CFG723).** What the continuum is, stated plainly.

## Checks

**K controls** (must pass, or the lane is VOID until fixed and disclosed):
- **K1 (SPARC reduction).** From the action's static spherical reduction, derived by sympy Euler–Lagrange
  equations (not hand-coded), solve for the field at every radius of NGC 3198 (record SPARC file, Υ_disk = Υ_bul
  = 0.61, the CFG660 harness value) at γ → 0. The result must equal the closed-form law g_N = g²/(g + a₀),
  max |g_CP/g_law − 1| < 1e-6, on both footings.
- **K2 (FRW dust).** F = −m c² n on FRW gives ρ = m c² n, p = 0, w = 0 exactly (sympy).
- **K3 (Newtonian limit).** √−g(−m c² n) for a static medium in the weak-field metric gives −ρc² − ρΦ + O(c⁻²)
  (sympy).

**MUTATE** (separate `_MUTATE` outputs; each must bite; exit 1 by design):
- **M1.** Remove the tether: coefficient of P·∇Φ → 0. Must give Newtonian dynamics (g = g_N to 1e-12), so K1's law
  check fails.
- **M2.** Flip the stiffness sign, γ → −γ. Must show a gradient instability: ω² < 0 at large k with |Im ω| ∝ k.
- **M3 (extra tooth).** Use W_rem instead of W_full in the medium's potential (drop the self-gravity cancellation).
  The reduction must then fail K1.

**Compute.** One core (OMP_NUM_THREADS=1, nice -n 10), one process at a time, an in-script RSS guard aborting
above 1 GB. sympy + small numpy/scipy only. Seconds to minutes. A live 1024³ job runs beside this lane.

## Class rule (frozen)

The candidate is the continuum action that Q2 derives. P1–P5 below are the requirements.
- **P1** S2's static law reproduced from the covariant action (K1).
- **P2** ∇_μT^{μν} = 0 holds for the action.
- **P3** Linearly well-posed: ω² real and bounded below independent of k; no ghost; speeds² ≥ 0.
- **P4** Isotropic FRW background, w = 0 for F = −m c² n, no tether-sector background.
- **P5** Slip within CFG847's largest value (1.9e-5) on both measures and footings, and below the class line 1e-2.

Classes:
- **COVARIANT PARENT FOUND**: P1–P5 hold with no condition beyond γ > 0 and the record's own inputs, and no
  extra field or preferred structure.
- **CONDITIONAL**: P1–P5 hold only under stated extra conditions. Examples: an extra non-propagating field; an
  inequality on the state; a choice between stiffness formulations; validity restricted to the longitudinal or
  spherical sector or to single-stream flow. Every condition is listed.
- **NOT FOUND**: for every formulation examined, at least one of P1–P5 fails, or no local covariant term reproduces
  S2.

Data gates in Q6 (C3, D2, …) are scored separately. They do not change the parent class, but they are reported
with equal prominence.

## Hand expectations (disclosed before any script; not results)

- Tether = the medium's minimal gravitational coupling (−δρ_cΦ = P·∇Φ + divergence), hence forced.
- W is not a strain function (u is an enclosed-mass quantity, nonlocal in φ). A medium-frame auxiliary potential is
  probably needed (an extra, non-propagating field).
- The static stress of the tether sector probably equals CFG660's field-aligned stress.
- Dispersion probably ω² = c_s²k² + Kρ₀ × (non-negative angular factor). That would cure √k, with an inertia
  condition ρ_c c² > (tether stress).
- A local covariant stiffness is probably a stiff equation of state ∝ ρ² that is large at early times.
- The tethered medium probably has no linear self-gravity (CFG888) → a growth flag for D2.
- Expected class: CONDITIONAL. These expectations may be wrong; results are reported as they fall.
