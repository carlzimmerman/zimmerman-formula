# AS086 — External logarithmic-well virial term

**Run:** `AS086-r1-20260928T133517`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter, Hermes subagent) — see `result.json`
**Task:** `deepseek_push/astra_spawn_ideas/AS086_external_logarithmic_well_virial_term.md`
(sha256 `358f0833bed924a7d149c661ccb53ddd4338c63ea90477f290275e04b759d4a5`, verified before execution)
**Sources (hashes verified against SOURCE_MANIFEST.json):** `G084_maxentropy_law.py` `752999fd…35ec`,
`G091_virial_triad.py` `8164360f…7ece`, `G233_eos_noscalar.py` `ad89298d…8b03`.
**Branch:** Conditional deep-equilibrium sector (static, non-relativistic bookkeeping; no field dynamics).
**Gate/action cell:** none varied here — the object is a *virial-term identity* of the fixed external well; no action is written or varied. G_N (single coupling) for baryon well and phantom self-gravity; G_bare/G_cosmo not invoked (no vacuum-curvature action in this sector).

---

## 1. Precise claim, symbol dictionary, boundaries, assumptions

**Claim (the seed's principal test).** For the external logarithmic well
Φ_ext(r) = C·ln(r/r_ref) with C > 0 and r_ref > 0, and any non-negative density ρ on the
finite shell r_in ≤ r ≤ R (r_in > 0),

```text
W_ext := -∫ ρ r (dΦ_ext/dr) dV = -C·M,   M := ∫ ρ dV .
```

**Symbols and units (SI).**

| symbol | meaning | value/unit |
|---|---|---|
| a0 | the framework acceleration scale | m/s²; canonical `9.3619e-11`, alt `1.1279e-10` |
| κ | a0/(c√(G ρ_Λ)) | **1/2 ADOPTED as input** (STANDING: fitted, not derived) |
| ρ_Λ | = 4a0²/(Gc²) (mass density implied by the adopted relation) | kg/m³ (differs between footings) |
| C | = √(G M_b a0) = v_flat² = deep-MOND well coefficient | m²/s² |
| r_M | = √(G M_b/a0) | m |
| r_ref | arbitrary reference radius of the log well, r_ref > 0 | m |
| ρ(r) | phantom mass density, ρ ≥ 0, supported on [r_in, R] | kg/m³ |
| M | = ∫_shell ρ dV | kg |
| W_ext | virial-form coupling (Σ r·F for force F = −∇Φ_ext) | J = kg·m²/s² |
| A | = C/(4πG) equipartition amplitude of the SIS ρ = A/r² (g03e/G091) | kg/m |
| σ² | 1-D velocity dispersion of the phantom | (m/s)² |

**Boundary conditions / domain.** 0 < r_in < R; interior diagnostics r_in/R ∈ {0.01, 0.1, 0.5},
R/r_M ∈ {0.62, 1.0}; **deep exterior shells** r_in/r_M ∈ {10, 100} with R/r_in ∈ {2, 10}
(the identity is verified on both families; the interior/exterior distinction matters for the
*transfer question*, §7, not for the algebra).

**Assumptions.** (i) ρ ≥ 0 with finite M (no other profile condition — the identity is
profile-independent); (ii) the well is of pure log form with r dΦ/dr = C wherever ρ > 0;
(iii) static sector, Newtonian shell integration, G = G_N for both wells; (iv) κ = 1/2 adopted
input; a0 values per footing with ρ_Λ adjusted so that κ = 1/2 exactly (the two footings carry
*different* ρ_Λ by factor (a0_alt/a0_can)² = 1.4514871574 — never the same density and the same
κ). **Framework inputs vs conclusions:** {G, M_b, a0(κ adopted), r, boundaries} = inputs;
W_ext = −CM, σ² = C/3, σ² = C/2 (bookkeeping), all double-count/Newtonian deviation formulae =
conclusions.

## 2. Derivation of the identity (without self-gravity)

The well is Φ_ext(r) = C ln(r/r_ref). For r > 0:

```text
dΦ_ext/dr = C/r            (the reference radius drops out of the derivative)
r·dΦ_ext/dr = C            (constant! — this is the entire content of the log form)
```

Substituting into the virial form (definition of W_ext in the claim):

```text
W_ext = -∫_shell ρ(r) · r·(C/r) · 4πr² dr = -C · 4π∫_shell ρ r² dr = -C·M.
```

Every scale factor, sign and unit: the derivative contributes C/r [m²/s² per m = m/s²];
r·dΦ/dr = C [m²/s²]; dV = 4πr²dr [m³]; ρ [kg/m³]; the product under the integral is
ρ·C·4πr²dr [kg·m²/s²] = [J]; the total is −C·M with C [m²/s²] × M [kg] = [J]. The sign is
fixed by the definition (the force of the well is F = −∇Φ_ext, so the virial sum
Σ r·F = −∫ρ r·∇Φ dV = −CM < 0: a bound configuration, as required for the equilibrium sector).
No self-gravity of the phantom is inserted anywhere in §2 — the phantom's own field is
decoupled; only its mass M enters.

**The potential-energy form is NOT the virial term.** ∫ρ Φ_ext dV = C·M·⟨ln(r/r_ref)⟩ is
r_ref- and profile-dependent (not even sign-definite once R > e·r_ref) and deviates from −CM by
up to 4.65× on the test grid (check B3 — the control fails as required, showing the claim −CM is
about the *virial* form, exactly as the seed states it).

## 3. Dispersion with and without pressure boundaries

Phantom = isothermal fluid ρ = A/r², P = σ²ρ, T = (3/2)Mσ², in the fixed log well (still no
self-gravity; W_ext = −CM enters once).

**Virial theorem of the truncated fluid** (Clausius with surface-pressure moments):

```text
2T + W_ext = ∮ P (r·n̂) dS = 4π [ R³ P(R) − r_in³ P(r_in) ]      (the AS083 twin-moment identity)
```

The two moments are *both* required: n̂ points outward, so the inner surface contributes
−P(r_in)·r_in·4πr_in². With P = σ²ρ:

```text
4π[R³·σ²A/R² − r_in³·σ²A/r_in²] = σ²·4πA·(R − r_in) = σ²·M        (exact, any shell; twin_moment_sis)
```

**Reading A — no pressure boundaries** (collisionless bookkeeping): 2T + W_ext = 0:

```text
3Mσ² − CM = 0  ⇒  σ² = C/3        (any ρ, any shell; profile-independent)
```

**Reading B — fluid closure with both moments:**

```text
3Mσ² − CM = Mσ²  ⇒  2Mσ² = CM  ⇒  σ² = C/2        (exact, any (r_in, R), any M)
```

Note: for the log well the C/2 result carries **no** log-ratio fine print — unlike the Newtonian
well bookkeeping (AS085/G091), where the ratio [1 + (1/λ)ln(R/r_b)] forces r_b = r_break for the
C/2 reading. The deep log-well bookkeeping is the cleaner statement.

**Control C3 (live):** drop the inner moment (outer-only): 3Mσ² − CM = σ²·4πA·R ⇒
σ² = C(R − r_in)/(2R − 3r_in), which equals 0.50254·C at r_in/R = 0.01, 0.52941·C at 0.1, and
**exactly C at r_in/R = 0.5** — up to 100% deviation from C/2. The inner surface moment is
load-bearing (Lean-certified: `outer_only_half_ne_half`).

## 4. The double-counting control (the seed's mandatory negative control)

The truncated SIS's own gravitational field (Newtonian integral), for r_in ≤ r ≤ R,
M(<r) = 4πA(r − r_in):

```text
Φ_self(r) = −G M(<r)/r − 4πGA ln(R/r)  ⇒  dΦ_self/dr = 4πGA·(1/r − r_in/r²)
```

The self-field's log coefficient is C_self = 4πGA, which **equals C** under the equipartition
normalization A = C/(4πG) (G091/g03e): the self field and the external well are the *identical
logarithmic field* in the r_in → 0 limit (Φ_self → 4πGA·ln(r/(R·e)), same r-slope C/r).

Exact self-energy (with its own integral, AS084-domain bookkeeping):

```text
W_self = (1/2)∫ρ Φ_self dV = −16π²GA² [ R − r_in(1 + ln(R/r_in)) ]   (closed form, quadrature-verified)
```

**The control.** If one books the *same* field twice — W_self := −C·M_T (external formula applied
to the self field) **and** W_ext := −C·M_T — the total is −2CM_T instead of the true single-coupling
value −CM_T:

- singular limit (r_in/R = 1e−15 row): total = **2.000000000000 ×** the true self virial —
  exact factor 2, the control failing by construction (D1, tolerance 2.0 ± 1e−9);
- the mis-inferred dispersions are σ² = 2C/3 (bare) or σ² = C (closure) instead of C/3, C/2
  (Lean-certified `dblcount_bare_sigma2`, `dblcount_closure_sigma2`);
- at finite r_in the external formula applied to the self field *mis-states* W_self by
  4.88% / 34.4% / 225.9% at r_in/R = 0.01 / 0.1 / 0.5 (D2: the self field is only
  asymptotically the log well; |W_self(exact) − (−C M_T)|/|W_self| → 3.4e−14 at r_in/R = 1e−15).

**Resolution (once-only rule):** the virial term −CM is the *external* coupling — one copy per
distinct well; the phantom's self-gravity is booked by its own integral W_self (AS084), never by
the external-well formula, even though the coefficients coincide.

## 5. Newtonian limiting regime (control E1, AS085 domain)

For the baryon point well Φ_b = −GM_b/r: r·dΦ_b/dr = GM_b/r ≠ const, so the log-well identity
must FAIL. Its exact replacement:

```text
W_newt = −∫ ρ r dΦ_b/dr dV = −4πGA M_b ln(R/r_in) = −M_b·C·ln(R/r_in)     (AS085's object; quadrature-verified)
```

Deviation from the log-well formula value −C·M_T on the diagnostics:
|W_newt + C·M_T|/|C·M_T| = **6.50 / 3.13 / 1.24** at r_in/R = 0.01 / 0.1 / 0.5, both footings —
the identity fails by factors 1.24–6.50 (my pre-estimate ">10" was too strict; the exact
deviation is |(M_b·G/C)·ln(R/r_in)/(R − r_in) − 1|, reproduced numerically to 8.9e−16). The
control is live: it fails exactly where it must, showing the −CM claim is specific to the deep
log well (r·dΦ/dr = C), and the Newtonian virial term keeps its own log ratio (which is what
G091's W_bar and AS085 book).

## 6. Independent check (step 4) and domain coverage

- **Direct quadrature** of the defining integral −∫ρ r dΦ/dr dV on log grids (N = 65536): **80
  cells** = 2 footings × (6 interior + 4 deep-exterior) shells × 4 profiles (A/r², A/r^1.5,
  A/r, const) → max relative residual **3.55e−16** vs pre-registered 1e−9 (B1). (For the SIS the
  integrand ρ·C·4πr² is literally constant, so its trapezoid residual is 0 at all N; the stated
  max is over the non-trivial profiles.)
- **Independent representation:** 60-digit mpmath tanh-sinh quadrature of the *raw* integrand
  (all-mpf inputs) reproduces −C·M to **1.02e−61** (B2, tolerance 1e−40).
- **Boundary/normalization case:** the well's field at r_M is C/r_M = a0 exactly (rel. dev 0),
  and v_flat⁴ = (√C)⁴ = G M_b a0 — the deep relations anchor the well (F1).
- **Both footings** throughout: canonical C = 2.949127e10 (m/s)², r_M = 10.209 kpc,
  σ²(C/2) = 1.4746e10; alt C = 3.237030e10, r_M = 9.301 kpc, σ²(C/2) = 1.6185e10 (m/s)².
  All dimensionless ratios (σ²/C = 1/3, 1/2; double-count factor 2; deviations) are
  footing-invariant; the two footings differ by C_alt/C_can = √(a0_alt/a0_can) = 1.09762 in
  absolute units and by ρ_Λ ratio 1.4514871574 — κ = 1/2 fixed in both.

## 7. Strongest surviving statement and the first missing bridge

**Strongest surviving statement (conditional lemma, no dynamics claimed).** Let Φ_ext = C ln(r/r_ref)
be the deep-MOND well of a baryon mass M_b (C = √(G_N M_b a0), κ = 1/2 adopted), and let a phantom
of total mass M occupy the finite shell r_in ≤ r ≤ R (r_in > 0) with ρ ≥ 0. Then, without any
profile assumption: (i) the virial-form coupling is exactly W_ext = −C·M (quadrature-residual
3.6e−16; 60-digit residual 1e−61); (ii) the bare fixed-well virial pins σ² = C/3; (iii) with the
fluid closure and the AS083 twin surface moments (outer minus inner) the fixed-well dispersion is
σ² = C/2 exactly on every shell — the with/without-pressure comparison of the seed; (iv) the
same field counted twice (W_self + W_ext both −CM) mis-states the virial by exactly the factor 2
(asymptotically) and mis-infers σ² = 2C/3 or C; (v) the identity is specific to the log well —
the Newtonian point well's virial term fails the −CM claim by 1.24–6.50× and keeps its own
−M_b C ln(R/r_in) form. Lean-certified algebra (9 theorems, zero sorry, axioms ⊆ {propext,
Classical.choice, Quot.sound}).

**Domain:** SI units; 0 < r_in < R; interior diagnostics r_in/R = 0.01–0.5, R/r_M = 0.62, 1;
deep-exterior shells r_in/r_M = 10, 100, R/r_in = 2, 10 (identity holds identically there —
geometrically the log well is the same object; this is the check the seed demands before any
exterior transfer); both footings; ρ ∈ {A/r², A/r^1.5, A/r, const}; M_phantom arbitrary;
M_b = 7e10 M_sun proxy for the dimensional tables only (contract constants: G = 6.67430e−11,
c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16).

**First missing implication (what this result does NOT provide).** (a) The deep log well is the
*deep limit* of the operative branch, not the branch: transferring C ln r (and hence σ² = C/2)
to filtered MONO requires proving the reduction of the operative kernel to the log potential on
the relevant domain — explicitly not done here, per framework contract "A shared deep limit is
not a shared finite law". (b) The fixed-well C/2 pins the *energy surface*, not the *attainment*:
how the phantom dynamically reaches σ² = C/2 remains open (G035's Newtonian-attractor kill
stands; G081's marginal mode is cited, not re-derived). (c) The self-consistent composite
(baryon Newtonian well + phantom self-gravity + twin moments, finite r_in) is not solved here
for σ² — that is child AS086.C01.

---

## Checks executed (with actual values; all from `as086_raw_output.txt`)

| # | check | measured | tol (pre-registered) | result |
|---|---|---|---|---|
| A1 | adopted footing bookkeeping, κ = 1/2 with per-footing ρ_Λ | κ = 0.5, 0.5 | 1e−12 | PASS |
| B1 | W_ext = −CM quadrature, 80 cells, 4 profiles, both footing families | max 3.55e−16 | 1e−9 | PASS |
| B2 | mpmath 60-dp raw-integrand representation | 1.02e−61 | 1e−40 | PASS |
| B3 | potential-energy form ≠ virial term (control fails as required) | up to 4.65× | > 0.5 | PASS |
| C1 | bare virial σ² = C/3, all shells | 1.64e−16 | 1e−12 | PASS |
| C2 | twin-moment closure σ² = C/2, all shells | 3.27e−16 | 1e−12 | PASS |
| C3 | outer-only bookkeeping CANNOT give C/2 (100% off at r_in/R = 0.5) | 1.0000 | > 1% | PASS |
| D1 | same log field counted twice → exact factor 2.000000000000 in the singular limit | 2.000000000000 | 2.0±1e−9 | PASS |
| D2 | self-field → C ln r well as r_in/R → 0; mis-statement grows to 226% at 0.5 | 3.4e−14 / 226% | <1e−6, >0.5% | PASS |
| E1 | Newtonian well breaks the −CM claim by 1.24–6.50×; own closed form exact | 6.50; quad 7.7e−15; analytics 8.9e−16 | ≥1; <1e−9; <1e−6 | PASS |
| F1 | g(r_M) = a0; v_flat⁴ = GM_b a0 (both footings) | 0 / 3e−16 | identities | PASS |

Negative controls that are **live** (they fail exactly where they should): B3 (energy form),
C3 (missing inner moment), D1 (double count), E1 (Newtonian well). 11/11 checks pass.

## Lean certificate

`AS086_virial_cert.lean` — 9 theorems: `logwell_integrand` (r·(C/r) = C), `bare_virial_sigma2`
(σ² = C/3), `closure_sigma2` (σ² = C/2 with the twin-moment bookkeeping), `dblcount_bare_sigma2`
(σ² = 2C/3), `dblcount_closure_sigma2` (σ² = C), `outer_only_half` and `outer_only_half_ne_half`
(incomplete bookkeeping gives σ² = C ≠ C/2), `half_ne_third` (C/2 ≠ C/3 for C ≠ 0),
`twin_moment_sis` (4π(R³P(R) − r_in³P(r_in)) = σ²M for the SIS). Compiled with
`lake env lean` (Lean 4.34.0-rc2, fable_independent_2026/lean_2026): **exit 0, zero sorry,
unfiltered `#print axioms` ⊆ {propext, Classical.choice, Quot.sound}** for all nine.
Compile host only — no files written into `fable_independent_2026/lean_2026`.

## Resources (actually enforced and measured)

wall 0.091 s (budget ≤120 s; bound by construction — fixed-size grids, no unbounded loops);
peak RSS 75.25 MiB = 78,905,344 bytes (budget ≤512 MB; macOS ru_maxrss bytes, cf. AS002 record);
1 thread (OMP/OPENBLAS/MKL/NUMEXPR/VECLIB = 1, no multiprocessing). Lean compile: single
process, seconds.

## Files in this run directory

- `derivation.md` (this file)
- `as086_compute.py` — runnable source (bounded prototype)
- `as086_raw_output.txt`, `as086_stderr.txt` — raw outputs
- `as086_checks.json` — structured checks (checks, footing table, bookkeeping, controls)
- `AS086_virial_cert.lean`, `lean_compile_and_axioms.txt` — Lean certificate + compile log
- `result.json` — RESULT_CONTRACT.json schema-v2 record
