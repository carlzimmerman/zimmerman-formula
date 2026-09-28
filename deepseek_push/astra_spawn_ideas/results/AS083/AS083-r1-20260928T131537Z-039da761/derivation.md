# AS083 — Virial surface term with BOTH boundaries (shell form of the virial identity)

Run: `AS083-r1-20260928T131537Z-039da761`
Seed: `deepseek_push/astra_spawn_ideas/AS083_virial_surface_term_with_both_boundaries.md`
(sha256 `5110591c95e2b379972e69661f734d00575d83fbcd315b64cac166fca07c3b8e`, verified before execution)

## 1. Claim under test (boxed in the seed, quoted verbatim)

> The pressure boundary contribution is `4*pi*(R^3*P(R) - r_in^3*P(r_in))`.

Sector: the conditional deep-equilibrium sector of the framework,
Φ = C·ln r log well, isothermal phantom density ρ(r) = A/r², P = σ²·ρ,
κ = 1/2 ADOPTED (a0 = κ·c·√(G·ρ_Lambda)). The shell is the spherical annulus
r ∈ [r_in, R] with BOTH surfaces retained.

## 2. Framework inputs (κ = 1/2 ADOPTED)

| quantity | formula | canonical a0 | alt a0 |
|---|---|---|---|
| a0 | registered footing | 9.3619e-11 m/s² | 1.1279e-10 m/s² |
| ρ_Lambda | 4·a0²/(G·c²) | 5.84441245402e-27 kg/m³ | 8.48308961956e-27 kg/m³ |
| C = v_flat² | √(G·M_b·a0), M_b = 6.5e10 M_sun | 1.836552995e+51 m²/s² | 2.015843278e+51 m²/s² |
| r_M | √(G·M_b/a0) | 9.8375 kpc | 8.9626 kpc |
| A | C/(4πG) | 2.1897e+29 kg/m | 2.4031e+29 kg/m |
| σ² | C/2 | 9.1828e+50 m²/s² | 1.0079e+51 m²/s² |

Numerics: G = 6.67430e-11, c = 299792458, M_sun = 1.98847e30,
pc = 3.085677581491367e16 (SI), all literals converted to mpmath at 50 digits.
G_N/G_bare/G_cosmo are kept SEPARATE — no leg conflates them.

## 3. Derivation (as executed)

**C1 — integration by parts (the IBP core).** For any differentiable P on
[r_in, R]:

    d/dr (r³·P) = 3r²P + r³P′  ⇒  [r³P]_{r_in}^R = 3∫r²P dr + ∫r³P′ dr     (exact)

**Shell virial identity.** Multiply the hydrostatic balance x·(∇P + ρ∇Φ) = 0
by dV and integrate over the annulus; x·∇P = r·P′ so, with dV = 4πr²dr,

    3 ∫_{r_in}^R P dV = 4π [ R³P(R) − r_in³P(r_in) ] + Q,
    Q := ∫ ρ (x·∇Φ) dV = 4π ∫_{r_in}^R ρ(r)·r·Φ′(r)·r² dr.

The claim is the identification of the surface term
**B = 4π(R³P(R) − r_in³P(r_in))** with both boundaries retained.

**C2a — phantom closed form.** In the log well Φ = C·ln r (r·Φ′ = C),
ρ = A/r², P = σ²A/r²:

    3∫P dV = 12πσ²A(R−r_in)
    B      = 4πσ²A(R−r_in)          (via r³P = σ²A·r at both surfaces)
    Q      = C·M_shell = 4πCA(R−r_in)

The identity 3∫PdV = B + Q therefore holds **iff 12πσ²A(R−r_in) =
4πσ²A(R−r_in) + 4πCA(R−r_in), i.e. exactly at σ² = C/2** — the framework
value. Verified symbolically (exact) and numerically at 50 digits on 10 shell
geometries per footing: 6 diagnostic shells (r_in/R ∈ {0.01, 0.1, 0.5} ×
R/r_M ∈ {0.62, 1}) + 4 deep shells (r_in/r_M ∈ {10, 100} × R/r_in ∈ {2, 10}).
Residuals ~1e-51 (quadrature noise), `rel = 0.0` for the closed-form cases.

**C2b — hydrostatic consistency.** P′ = −ρ·Φ′ with ρ = A/r², Φ = C·ln r
holds iff 2σ² = C — the SAME condition the two-surface virial imposes.
The virial reading and the hydrostatic balance coincide; this generalizes the
G091 V3 surface-pressure point to the two-surfaces shell.

**C3 — one-boundary limit and leading neglected term.** Omitting the inner
surface at finite r_in gives the one-boundary residual

    res_1b := 3∫PdV − (4πR³P(R) + Q) = 4πσ²A(R−r_in) − 4πσ²A·R = −4πσ²A·r_in,

and Δ := 4π r_in³·P(r_in) = 4πσ²A·r_in:

    residual + Δ = 4πA(R−r_in)(2σ² − C)   (general), and = 0 EXACTLY at σ² = C/2.

As r_in → 0 the one-boundary formula is recovered with leading neglected term
Δ = σ²·M_ph(<r_in), linear in r_in for the isothermal phantom (r³P = σ²A·r).
The same Δ is the misbooking in the σ²-reading: fitting the one-boundary
formula to the exact identity yields σ²_mis = C·(R−r_in)/(R+r_in)²·…; at
r_in/R = 0.5 the one-boundary misreading gives σ²_mis = C (vs C/2 exact) —
the inner surface is a factor-2 effect at a halfway edge.

**Newtonian regime (N2) — 1/r well, two representations.**
(a) Truncated envelope with vacuum edge P(R) = 0, M(<r) = M_b + 4πA(r−r_in):

    P(r) = (GAM_b/3)(1/r³ − 1/R³) + 4πGA²[ (1/2)(1/r² − 1/R²) − (r_in/3)(1/r³ − 1/R³) ]

Balance: finite-difference relres 3.3e-18 (method floor), exact-derivative
relres ~2e-51; virial identity relres 0.0 / 1.4e-51. B ≠ 0 here — the
truncated envelope genuinely carries a two-surface boundary term.
(b) Infinite point-mass envelope P = GAM_b/(3r³) (pressure continues past R):
r³P = const, so **B = 4π(R³P(R) − r_in³P(r_in)) = 0 exactly** — in the pure
1/r well the two surfaces cancel; the identity reduces to 3∫PdV = Q
(relres ~1.5e-51). The one-boundary formula 4πR³P(R) = 4πGAM_b/3 ≠ 0 would
misbook a purely interior quantity. (An earlier draft's spurious 4π in the
M_b term was found and removed; that version was NOT hydrostatic and the
identity failed with relres 1.5882 — the control caught a real bug.)

**N3 — constant-density shell** ρ = ρ0, P from the balance with P(R) = 0:
identity relres = 0.0 exactly, both footings.

**N1 — phantom numeric sweep** (both footings): 20 shells total, max relres
~1e-51 (< 1e-40 tolerance set before evaluation).

## 4. Negative control (capable of failing)

**NC1 — one-boundary form at finite r_in (12 shells: 6 geometries × 2
footings).** Retain finite r_in but drop the inner pressure term:

    res = 3∫PdV − (4πR³P(R) + Q) = −Δ < 0   (the one-boundary form OVERSHOOTS)

Measured: |residual| = 4πr_in³P(r_in) to rel 1e-40; ratio residual/Δ = −1
exact; |residual|/outer-term = r_in/R = 0.01, 0.1, 0.5 (all to 12 decimals,
e.g. −1.83655e+49 J vs Δ = 1.83655e+49 J at r_in/R = 0.01, canonical).
The control is live: it would pass vacuously only if Δ = 0 (r_in → 0).

## 5. Cross-checks and footings

- **V1 (G091 cross-check):** 4πR³P(R) at R = 0.62 r_M equals G091's
  3·P_s·V = σ²·M_T (frontal cap surface pressure of the phantom), rel ~0.
- **V2 (equipartition / a0-only pressure):** at R = r_M the outer surface
  term equals σ²·M_b = 1.836553e+51 J (canonical), and P(r_M) =
  a0²/(8πG) = 5.2249533e-12 Pa with no M_b and no r in the expression
  (rel = 3.7e-51 / 0.0).
- **V3 (footings separate):** ρ_L(canonical) = 5.844412454022e-27 kg/m³,
  ρ_L(alt) = 8.483089619559e-27 kg/m³, both at the same κ = 1/2 with their
  OWN densities (ratio 1.451487157). The fixed-density leg gives
  κ_eff = 0.602388404 recorded for accounting only — the footings do not
  share both fixed density and fixed κ.

## 6. Dimensional surface terms (equilibrium phantom)

Canonical footing, R = 9.84 kpc (1 r_M), r_in/R = 0.5: B = 9.1828e+50 J =
outer 1.8366e+51 J − inner 9.1828e+50 J (inner/outer = 0.5).
P(R) = 5.2250e-12 Pa ≪ P(r_in) = 2.0900e-11 Pa — the inner surface term is
the larger pressure edge at halfway geometry; both surfaces must be carried.

## 7. Verification summary

27/27 checks PASS with actual residuals (no literal-True steps). Exact
symbolic identities (sympy) at the top; 50-digit mpmath numerics below;
residuals reported above are measured, not booleans.

## 8. Lean 4 certificate

`AS083_virial_surface_identity.lean` — 7 theorems: T1 generic IBP;
T2 phantom integral; T3 two-surface algebra; T4 the virial equivalence
(12πσ²A(b−a) = 4πσ²A(b−a) + 4πCA(b−a)) ⟺ σ² = C/2; T5 one-boundary
residual = −4πσ²Aa at σ² = C/2; T6 Newtonian surface cancellation
(r³P = const ⇒ B = 0); T7 composite phantom virial identity ⟺ σ² = C/2.
Compiled with `lake env lean` (exit 0); #print axioms on all theorems:
exactly {propext, Classical.choice, Quot.sound}, zero sorry, zero sorryAx.

## 9. Bounds (ACTUALLY enforced)

declared: wall ≤ 120 s, mem ≤ 512 MiB, threads = 1.
enforced: wall 2.15 s (kill at 120 s armed, not triggered); max RSS
98.9 MiB (external supervisor poll 0.1 s, SIGKILL > 512 MiB armed, not
triggered — macOS 26.5.2 refuses in-process RLIMIT_AS/DATA/RSS lowering);
in-process RLIMIT_CPU soft=hard=115 s; OMP/OPENBLAS/MKL/VECLIB/NUMEXPR
pinned to 1; single process, no spawns.

## 10. Limitations and open implication

Limits: (1) the identity is proven for the equilibrium isothermal phantom
P = σ²A/r² and the hydrostatic balances enumerated; it is an algebraic–
bookkeeping statement plus its hydrostatic consistency — no dynamics, no
time evolution, no observational data; (2) the physical origin of the inner
edge r_in (why the log-well phantom ceases at a finite radius) is NOT
derived here; (3) the Newtonian regime was sampled deep inside r_M
(R/r_M = 0.01); (4) branches Q, RAR, MU2, EXP, MONO remain DISTINCT
comparison objects (criterion B); this run establishes the two-boundary
surface bookkeeping in the log-well sector only.

Open implication: the inner-surface term Δ = 4πr_in³P(r_in) = σ²·M_ph(<r_in)
is precisely the quantity that must vanish for the one-boundary limit and
that encodes the truncation scale r_in — the next unresolved question is
what fixes r_in physically (the handover from the deep log well to the
Newtonian core). See child proposal AS083.C01.
