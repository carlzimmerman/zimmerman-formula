# AS082 — Inner boundary mass and self-gravity: derivation

**Run:** `run_AS082-r1-20260928T131254Z-dsv4f-hermes`
**Seed hash (verified):** `4b5a3471372f7f5bd8b005c8ff313528b8b9a97d12c3028bf9ff3be5920bae03`
**Branch:** Conditional deep-equilibrium sector (Group A04 — finite-domain equilibrium and virial closure). No automatic particle ontology; filtered MONO is NOT used for any conclusion in this task — the operative field kernel enters only through the deep-exterior transfer control (NC4/NC5), where its asymptotic bound is computed and the transfer is shown to fail.
**Worker:** dsv4f-hermes (Hermes subagent; model deepseek/deepseek-v4-flash-0731 via openrouter)
**Sources inspected (hashes match SOURCE_MANIFEST.json):** G084_maxentropy_law.py `752999fdf6c07b0cf0fb419290177f90151a239d63c7707029b240fef46735ec`, G091_virial_triad.py `8164360f95fdc340824a92a5db3ccdabf3ce28430bdd1c375e276a77ba67ece5`, G233_eos_noscalar.py `ad89298d967ae4f2d574a47f91d5adc54addae40b6a5e47d0bd83cf5564a8b03`.

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Claim P (conditional).** Let the phantom occupy `rho(r) = A/r^2` on `[r_in, R]` with
`0 < r_in <= r <= R <= r_M`, and let the (spherically symmetric) region `r < r_in`
carry total mass `M_in` ("inner boundary mass"). Evaluating the phantom's own
gravity with the Newtonian shell theorem (coupling `G_N`; spherical, static),
the enclosed mass and self-acceleration at every shell radius are

```
M(r)    = M_in + 4*pi*A*(r - r_in)
g_self(r) = G_N * M(r) / r^2
```

Then the exact logarithmic-well condition

```
g_self(r) = C/r  for every r in [r_in, R]        (equivalently Phi = C ln r + const)
```

holds **if and only if**

```
(A)  A = C/(4 pi G_N)         (the equipartition amplitude, cf. G091 V1a/G084)
(B)  M_in = 4*pi*A*r_in = (C/G_N)*r_in = M_b * (r_in/r_M)      (the boundary mass)
```

**Symbols.** `rho` phantom mass density `[kg/m^3]`; `A` density coefficient `[kg/m]`;
`r_in` inner boundary radius `[m]`, `R` outer truncation `[m]`, `r_M = sqrt(G_N M_b/a0)`
the equipartition radius; `M_in` mass inside `r_in` `[kg]`; `M_b` baryon mass (framework
scale parameter); `C = sqrt(G_N M_b a0) = v_flat^2` `[m^2/s^2]`; `a0 = kappa*c*sqrt(G*rho_Lambda)`
with `kappa = 1/2` **adopted**; `G_N` the Newtonian Poisson coupling (kept separate from
`G_bare`, `G_cosmo` — no relation between them is derived here); `g_self >= 0` inward
acceleration magnitude; `Phi` gravitational potential per unit mass.

**Boundary conditions / assumptions (explicit):**
1. static, spherically symmetric Newtonian arrangement; shell theorem valid;
2. profile exactly `A/r^2` on the shell; nothing asserted for `r < r_in` except the
   integrated mass `M_in` (a point mass is the minimal representation; any
   spherically symmetric distribution of the same total mass gives the same field
   outside by the shell theorem);
3. `R <= r_M` for the diagnostic fixtures (`R/r_M in {0.62, 1}`, `r_in/R in {0.01, 0.1, 0.5}`);
4. `a0`, `C`, `r_M` enter only through the two relations certified below;
5. Poisson sector uses `G_N`; `rho_Lambda` is fixed by `a0 = kappa*c*sqrt(G*rho_Lambda)`,
   `kappa = 1/2` — NOT an independent input.

**Framework inputs vs conclusions.** Inputs: `kappa = 1/2`, `G_N`, `c`, `M_sun`, `pc`,
`M_b`, the profile ansatz `rho = A/r^2`, and the equipartition amplitude `A = C/(4 pi G_N)`
(from G091 V1a/G084 — a source, inspected). Conclusions to be established by this task:
the boundary-mass value `M_in = M_b r_in/r_M`, the iff (A)∧(B) ⟺ exact `C/r`, the
residual decomposition, the failure of the `M_in = 0` reading, and the transfer check.

---

## 2. Derivation of g_self and of the central mass M_in (step 2)

**Enclosed mass.** For `r in [r_in, R]`:

```
M(r) = M_in + ∫_{r_in}^{r} 4 pi s^2 (A/s^2) ds = M_in + 4 pi A (r - r_in).      (1)
```

(Integrand `4 pi A` is constant; exact.) Units: `A [kg/m]`, `4 pi A (r - r_in) [kg]` ✓.

**Self-acceleration** (shell theorem: outer shells exert no field inside; the interior
mass acts as a point mass at the centre):

```
g_self(r) = G_N * [M_in + 4 pi A (r - r_in)] / r^2.                            (2)
```

**Exact-C/r condition.** `g_self(r) = C/r` for every `r in [r_in, R]` (an interval with
more than one point) is, after multiplying by `r^2 > 0`,

```
G_N * M_in + 4 pi G_N A r - 4 pi G_N A r_in = C r        for all r in [r_in, R].  (3)
```

An affine function equals a linear function on a two-point domain iff constants and
coefficients separately match:

```
(4 pi G_N A - C) = 0            =>  A = C/(4 pi G_N)                     (A)
G_N M_in - 4 pi G_N A r_in = 0  =>  M_in = 4 pi A r_in                  (B)
```

**Boundary-mass value.** With (A), `M_in = 4 pi A r_in = (C/G_N) r_in`. Using the
equipartition identity `C/G_N = M_b/r_M` (both follow from the definitions:
`C/G_N = sqrt(G_N M_b a0)/G_N = sqrt(M_b a0/G_N) = M_b/sqrt(G_N M_b/a0) = M_b/r_M`),

```
M_in = M_b * (r_in / r_M).              (dimensionless ratio, footing-independent)
```

**Physical interpretation (not hidden in A).** `M_in` is the mass that the phantom's own
linear enclosed-mass law `M_ph(<r) = 4 pi A r = M_b (r/r_M)` (the G091 V1a equipartition
identity; cf. also `M(<R) = M_b R/r_M` below) attributes to the excluded central hole
`[0, r_in)`: it is the analytic continuation of the truncated profile's own mass law,
**not an independent particle/dark object and not a free parameter**. The point-mass
Keplerian term `G_N M_in/r^2` exactly cancels the shell's inner-edge deficit
`-4 pi G_N A r_in/r^2`, so the combined system behaves as one "mass linear in r",
`M(r) = (C/G_N) r`, at every shell radius. As `r_in -> 0`, `M_in -> 0` and the
perfect un-truncated singular isothermal sphere `g = C/r` for all `r > 0` is recovered.
The sign is fixed: `g_self > 0` (inward), consistent with `Phi = C ln r + const`,
`-dPhi/dr = -C/r`.

With both conditions in place the linear law is exact across the whole shell:

```
M(<R) = M_in + 4 pi A (R - r_in) = M_b (R/r_M);   at R = r_M:  M(<r_M) = M_b   (2')
```

i.e. the equipartition normalization `M_ph(<r_M) = M_b` survives the truncation with the
boundary mass included — the boundary mass is what makes the truncated model's mass law
identical to the untruncated one's.

## 3. Intermediate algebra, scale factors, signs, units (step 3)

**Residual decomposition (exact identity, no limiting regime needed):**

```
g_self(r) - C/r = (G_N M_in - 4 pi G_N A r_in) / r^2  +  (4 pi G_N A - C) / r.   (4)
```

The two terms are independent errors: the `1/r` term is killed only by the amplitude
condition (A), the `1/r^2` term only by the boundary mass (B). Each scale factor:
`G_N M_in [m^3 kg^-1 s^-2 * kg = m^3/s^2]` over `r^2 [m^2]` gives `[m/s^2]` ✓;
`4 pi G_N A [m^3/(kg s^2) * kg/m = m^2/s^2]` over `r [m]` gives `[m/s^2]` ✓;
`C/r [m^2/s^2 / m = m/s^2]` ✓. Verification of (4) is check C1 (max relative
disagreement `3.20e-16` over the sample grid, score scaled by `C/r`).

**Negative control M_in = 0.** Setting `M_in = 0` in (2) with (A) holding:

```
g_self(r) = (C/r)(1 - r_in/r),      g_self(r) - C/r = -C r_in / r^2.            (5)
Phi(r) = -C (ln r + r_in/r) + const  =  C ln r + C r_in/r + const  (not a log well).
```

Relative error `r_in/r`, exactly `1` at `r = r_in` (where the open shell's own field
vanishes: a hollow shell exerts no field at its inner surface) and `r_in/R` at the cap.
Stated differently: the potential acquires a `1/r` term — the well is log-plus-Keplerian,
not logarithmic. This is the mandated control; it is capable of failing and fails the
"exact logarithmic self-gravity" claim.

**Limiting regimes.**
- *Newtonian limit* `r -> r_in^+`: `g_self -> G_N M_in/r_in^2 = C/r_in` (continuous
  value); interior of the hole is purely Keplerian `g = G_N M_in/r^2`, which crosses
  `C/r` exactly at `r* = G_N M_in/C = r_in` (with (A)+(B)); the slope is kinked
  (Keplerian `-2C/r^2` vs `C/r`'s `-C/r^2`) — a genuine boundary-layer statement.
- *Deep limit* `r -> +inf` at fixed `r_in`, `M_in = 0`: `g_self = C/r + O(r_in/r^2)`
  — asymptotic only; the leading neglected term is `-C r_in/r^2` (relative `r_in/r`).
  With (B) the identity is exact at every finite `r`, no limit needed.

## 4. Independent check in a different representation (step 4)

Four independent representations, all executed, actual residuals saved
(`raw_output.json`):

1. **Direct shell-theorem field** (the defining expression (2)) across 2000 log-points
   per shell, 6 diagnostic shells × 2 footings: worst `|g - C/r|/(C/r) = 5.73e-16`
   (canonical), `4.19e-16` (alternative) — float roundoff on an exact identity
   (check C2). Enclosed mass follows `M(<r) = M_b r/r_M` to `4.5e-16`.
2. **Two-branch potential integral**: `Phi(r) = -G_N M_in/r - G_N ∫_{r_in}^r dM(s)/r
   - G_N ∫_r^R dM(s)/s` (inner mass acts at r, outer shells act at s — genuinely
   different representation), then `g = +dPhi/dr` by a 5-point stencil on a uniform
   4000-point grid: max rel `2.01e-11` (fourth-order truncation only; check C3a).
3. **Density recovery**: `rho = (dM/dr)/(4 pi r^2)` via central finite differences of
   `M(r)`: max rel `2.78e-14` vs `A/r^2` (check C3b).
4. **Decimal(60) direct evaluation** at 3 radii: max rel `9.55e-17`, flooring at the
   float64 precision of the input constants — no cancellation pathology (check C3c).
   The exact identity is also captured as a Lean-4 certificate (below).

## 5. Negative control, strongest surviving statement, transfer check (step 5)

**NC1 (mandated):** `M_in = 0` at finite `r_in` while claiming exact logarithmic
self-gravity — **FALSE**: residual `-C r_in/r^2`, rel err `1.0` at `r_in` (check NC1,
analytic form match on the grid). The open-shell ansatz does **not** give the log well.

**NC2 (independence of the two conditions):** `A -> 1.05 A` (boundary mass still matched
to the perturbed A): max rel residual `0.0500 = |pert - 1|` exactly; `A -> 0.9 A`:
`0.1000` (checks NC2). The slope condition (A) is necessary even with (B) adjusted.

**NC3 (limits):** `r*/r_in - 1 = -1.1e-16`; `|g_K(r_in) - C/r_in|/(C/r_in) = 0.0`;
deep rel error with `M_in = 0`: `1.00e-2` (i.e. `r_in/R` at `R = r_M`, `r_in = 0.01 R`),
with `M_in` included: `0.0` (check NC3).

**NC4 (deep-exterior transfer — the seed's "do not transfer" check):** on shells
`r_in/r_M = 10, 100` with `R/r_in = 2, 10`, exact `C/r` would require
`M_in = 10..100 x M_b`; the capped model's total phantom mass is `M_T = lambda M_b`
(`lambda = r_break/r_M in {0.62, 1.0}`), so the required boundary mass exceeds the
entire phantom by factors `10..161` (check NC4). Moreover the truncated Newtonian model
is Keplerian outside the cap with discontinuity factor
`g_ext/g_int = (1+lambda)/lambda = 2.61` (lambda = 0.62) — the interior ansatz **does
not** continue to the deep exterior. The actual deep exterior is an asymptotic property
of the operative kernel, not of Newtonian continuation.

**NC5 (full-kernel error bound for the operative deep exterior):** for `y = B/a0 <
y* = 2.3374` the operative `nu_mono` equals `nu_RAR`, and for a point baryon mass
`B = G_N M_b/r^2`:

```
g_ph = B (nu_RAR(y) - 1) = B/sqrt(y) + B/2 + B sqrt(y)/12 + O(B y^{3/2})
     = C/r  [1 + (1/2) sqrt(y) + (1/12) y + O(y^{3/2})]
```

Leading neglected term `B/2`, relative to `C/r`: `r_M/(2r)` — `5.0e-2` at `r = 10 r_M`,
`5.0e-3` at `r = 100 r_M`; next correction `y/12` = `8.33e-4` / `8.33e-6`. This bound
is analytic-lane (series of the exact `nu_RAR`); the heat filter `S = e^{(xi^2/2)Delta}`
adds an unquantified smoothing error `O((xi/r)^2)` — recorded as an open dependency,
not claimed.

**Strongest surviving statement (conditional theorem, both footings).**

> On `0 < r_in <= r <= R <= r_M` with `rho = A/r^2` and interior mass `M_in`, the
> phantom's Newtonian self-gravity satisfies `g_self(r) = C/r` for **every** shell
> radius (equivalently the well is exactly logarithmic, `Phi = C ln r + const`) **if
> and only if** `A = C/(4 pi G_N)` **and** `M_in = M_b r_in/r_M`. The boundary mass is
> the analytic continuation of the equipartition linear mass law into the excluded
> central hole — uniquely determined, dimensionless ratio `M_in/M_b = r_in/r_M`,
> footing-independent. With `M_in = 0` the well is `Phi = C ln r + C r_in/r + const`
> (residual `-C r_in/r^2`, relative error `1` at `r_in`). The interior ansatz does not
> transfer to the deep exterior (`r_in >= 10 r_M` demands `M_in >= 10 M_b` while the
> capped phantom totals `<= M_b`; the truncated model is Keplerian outside the cap,
> mismatch `(1+lambda)/lambda`); the deep `C/r` is an asymptotic property of the
> operative MONO/RAR kernel with leading neglected term `B/2` (relative `r_M/(2r)`).

**Footings.** All statements are scale-invariant in structure; the two footings enter
through `r_M` only. Canonical `a0 = 9.3619e-11 m/s^2` ⇔ `rho_Lambda = 4 a0^2/(G c^2) =
5.8444e-27 kg/m^3` at `kappa = 1/2`. The alternative `a0 = 1.1279e-10 m/s^2` cannot
share both fixed `rho_Lambda` and fixed `kappa`: at fixed `kappa = 1/2` it requires
`rho_Lambda' = 8.4831e-27 kg/m^3` (ratio `1.4515`); at the fixed canonical
`rho_Lambda` it corresponds to `kappa_eff = 0.6024` (check F1). Representative numbers
(MW proxy `M_b = 6.5e10 M_sun`):

| footing | C = v_flat^2 [m^2/s^2] | v_flat [km/s] | r_M [kpc] | A [kg/m] | M_in at r_in = 0.01 R, R = 0.62 r_M [M_sun] | M_in/M_b |
|---|---|---|---|---|---|---|
| canonical | 2.8418e10 | 168.6 | 9.84 | 3.3883e19 | 4.030e8 | 0.0062 |
| alternative | 3.1193e10 | 176.6 | 8.96 | 3.7191e19 | 4.030e8 | 0.0062 |

(the ratio `M_in/M_b = r_in/r_M` is identical in both footings, as the theorem requires;
`M_in` at a *fixed fraction* of `r_M` is footing-independent because `M_b` is shared).

**Lean certificate** (`AS082_inner_boundary_mass.lean`, compiled `lake env lean`, exit 0,
zero `sorry`, axioms exactly {propext, Classical.choice, Quot.sound} for all ten
theorems): T1 integrand `s^2 (A/s^2) = A`; T2 `∫_{r_in}^r 4 pi A = 4 pi A (r - r_in)`;
T3 forward (two radii ⇒ both conditions); T4 backward; T5 the iff (∀r form, cleared
polynomial); T6 `M_in = (C/G) r_in`; T7 `M_in = M_b r_in/r_M`; T8 negative control
(`M_in = 0`, `C != 0`, `r_in != 0` ⇒ no exact C/r); T9 residual numerator `-C r_in`;
T10 `4 pi A = C/G`. Deep-asymptotics series (NC5) is analytic-lane (not Lean-certified)
and is stated as such.

---

## Assumptions ledger, open dependencies, and what this does NOT establish

- `kappa = 1/2` is an **adopted input** (framework contract), not derived here.
- `A = C/(4 pi G_N)` is an input from G084/G091 (inspected, hashes pinned) *and*
  independently re-derived here as the self-consistency (amplitude) condition (A) —
  two routes to the same amplitude.
- Equality `G_N = G_cosmo` (needed for `Lambda = 32 pi a0^2/c^4` in the vacuum
  identity) is **not** derived; the Poisson sector here uses `G_N` only.
- The heat-filter smoothing error `O((xi/r)^2)` of the operative kernel at the deep
  exterior is not bounded in this task (kernel bound NC5 is the unfiltered
  `nu_RAR = nu_mono` series at a point source).
- Static only: no dynamics, no attainment (virial gives the energy surface, not
  relaxation — G035's kill stands); entropy-maximum and virial closure are the
  inspected sources' content, not re-derived here beyond (A) and (2').
- Numerical agreement at float precision is finite evidence; the exact identity is
  the certified algebra (Python residual `<= 5.7e-16` + Lean).

## First-principles inputs (separate)

Primitive/adopted: `kappa = 1/2`; `G_N = 6.67430e-11`, `c = 299792458`,
`M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (SI); `M_b = 6.5e10 M_sun` (MW
proxy); static spherical Newtonian shell-theorem evaluation; profile ansatz
`rho = A/r^2` on `[r_in, R]`; equipartition amplitude (G091/G084). Genuinely derived in
this run: `M(r) = M_in + 4 pi A (r - r_in)`; the iff (A)∧(B) with `M_in = M_b r_in/r_M`;
the residual decomposition (4); the `M_in = 0` failure (5); the deep/Newtonian-limit
statements and the interior→exterior transfer no-go with the kernel bound (NC4/NC5).

## Return package (in this directory)

- `AS082_compute.py` — bounded prototype (stdlib, 1 thread, 120 s self-deadline;
  actual wall 0.01 s; maxrss 15.4 MB; RLIMIT_AS enforcement refused by macOS, recorded)
- `run.log`, `raw_output.json` — actual residuals (9/9 checks PASS)
- `AS082_inner_boundary_mass.lean`, `lean_compile_out.txt`, `lean_probes/probe1.lean`
- `derivation.md`, `result.json`