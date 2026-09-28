# AS653 — General flux power fixes acceleration homogeneity: derivation

**Run:** `AS653-r1-20260928T140712Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (openrouter) via Hermes agent subagent; host macOS 26.5.2
**Task file:** `deepseek_push/astra_spawn_ideas/AS653_general_flux_power_fixes_acceleration_homogeneity.md`
sha256 `ab203bd974e5a21bbd3ad3baf83b9cab6a03971528d67c27a0eca9a5e8913b15` (verified before execution).
**Branch declared by the seed:** explicit coefficient-mechanism diagnostic on the k04
four-form promotion; cannot be identified with Q / RAR / MU2 / EXP / MONO.
**Explicit prerequisite AS651:** no landed result exists in `results/` at execution time
(proposed-only); this run therefore stands on the cited k04 source itself and on the
landed upstream results AS039 (deep energy homogeneity degree 3/2), AS051
(deep-slope transfer κ = 1/b), AS063 (deep data fix the product n·λ only).

---

## 0. Framework base (adopted inputs, not derived here)

- `a0 = kappa * c * sqrt(G * rho_Lambda)` with **kappa = 1/2 adopted**.
- `r_M = sqrt(G M_b / a0)`, deep `v_flat^4 = G M_b a0`, `C = sqrt(G M_b a0)`.
- Numerics: `G = 6.67430e-11 m^3 kg^-1 s^-2`, `c = 299792458 m/s`,
  `M_sun = 1.98847e30 kg`, `pc = 3.085677581491367e16 m`.
- `G_N` (measured Newton coupling of the galaxy force), `G_bare` (action coupling of
  the four-form sector) and `G_cosmo` (coupling in the a0 definition) are kept
  **separate symbols**; they are reconciled only through explicit ratios, never by
  silent identification. The final condition is a pure equality of exponents and is
  therefore *independent* of which coupling ratio is assumed; the coefficient
  relation is quoted with the ratio explicit.
- Both footings carried separately: canonical `a0 = 9.3619e-11 m/s^2`
  (`rho_Lambda = 5.844412e-27 kg/m^3` at κ = 1/2) and alternative
  `a0 = 1.1279e-10 m/s^2` (κ fixed: `rho_Lambda = 8.483090e-27 kg/m^3`;
  rho fixed: `kappa_eff = 0.602388`). Never both fixed simultaneously (B3).

## 1. Step 1 — fix the source equation, variables, boundary conditions and measure

Cited source: `kappa_closure/k04_four_form_promotion_consistency.py`, pinned
SHA-256 `15c0a7e13eb9b7a5fdb403c8826bd01912d68dc81614609fddb6cd6ed9d32399`
(verified identical to the working tree and to SOURCE_MANIFEST.json).

**Construction (k04 convention, restated):** a three-form gauge sector whose
four-form field strength is `F = q * eps` (q the dual flux amplitude, `eps` the
spacetime volume 4-form). Standard four-form facts adopted from the cited branch
(Duff–van Nieuwenhuizen 1980; Bousso–Polchinski 2000): `dF = 0` forces `q`
constant in the vacuum sector, there are **no propagating modes**, and the stress
tensor is vacuum-like, `T_mu nu = (P - q P_q) g_mu nu`, so the gravitating energy
density is the **Legendre form**

```text
eps_vac = q P_q - P           (k04 F1: "+b a0^2/G", a Legendre form, NOT -P)
```

**Independent variables:** `q` (the flux amplitude), with `P` a function of the
single invariant `q` only. `P` and the promotion `a0` are the declared functions.

**Boundary data and measure:** `q != 0` (seed domain: a0 != 0); `lambda > 0`,
`n > 1`, `m > 0`; the homogeneous vacuum cell: `q` constant over spacetime, uniform
`eps_vac`; the flux amplitude is an **integration constant of the vacuum sector** —
no equation in the cited source fixes its value — which is precisely what step 3 of
the seed demands be kept free.

**Seed's generalisation under test:**

```text
P(q) = lambda * |q|^n ,        a0 = beta * |q|^m ,
q != 0 ,  lambda > 0 ,  n > 1 ;   beta > 0 symbolic, m > 0 symbolic
```

(k04 is the special case n = 2, m = 1 with `lambda = Z/2 + b beta^2` and the
`G`-fold `a0 = beta sqrt(G) |q|`; see §5.)

**Additional assumption needed for the target (stated):** the promotion is a pure
power `a0 = beta |q|^m` (leading-homogeneity ansatz, the seed's declared cell) and
`m > 0` so that the MOND scale vanishes with the flux (vacuum-off → MOND-off).
Since every physical quantity below depends on `|q|` only, `q > 0` is taken
WLOG (recorded; the `|q|` derivative gives `q * d|q|^n/dq = n |q|^n` for
`q != 0`, so all formulas are even in q).

## 2. Step 2 — the condition for a0^2 / (G_N eps_vac) independent of the flux amplitude

**Legendre energy (exact).** For `P = lambda |q|^n`, `q != 0`:

```text
eps_vac = q P_q - P = n lambda |q|^n - lambda |q|^n = lambda (n - 1) |q|^n        (1)
```

Sign control (A1/B2): `eps_vac > 0` iff `n > 1` (positive gravitating vacuum
energy, k04 F1 convention); `n = 1` gives `eps_vac ≡ 0` (the action is linear in
q — the vacuum does not gravitate, the ratio is undefined); `n < 1` gives
`eps_vac < 0` (κ² would be negative — inadmissible). The seed's `n > 1` is thus
exactly the positivity of the Legendre form.

**The ratio (exact).**

```text
kappa_N^2(q) := a0^2 / (G_N * eps_vac)
              = beta^2 |q|^(2m) / (G_N * lambda * (n - 1) * |q|^n)
              = [ beta^2 / (G_N lambda (n - 1)) ] * |q|^(2m - n)                 (2)

d ln kappa_N^2 / d ln |q| = 2m - n                                                (3)
```

**Condition.** `kappa_N^2` is independent of the flux amplitude (for all `q != 0`)
**iff** `2m - n = 0`, i.e.

```text
n = 2m                                                                             (4)
```

the flux power must be **twice** the promotion exponent. Under (4):

```text
kappa_N^2 = beta^2 / (G_N lambda (n - 1)) = beta^2 / (G_N lambda (2m - 1))         (5)
```

constant, with kappa = 1/2 requiring

```text
lambda * (n - 1) * G_N / beta^2 = 4        <=>      lambda G_N / beta^2 = 4/(n - 1)   (6)
```

**Same condition from two independent routes:**

- *Dimensional analysis (control C1 / A4):* `[lambda] = M L^-1 T^-2 [q]^-n`,
  `[beta] = L T^-2 [q]^-m`, so `[kappa_N^2] = [beta]^2/([G_N][lambda])/[q]^0 =
  [q]^(n-2m)` — κ² is dimensionless **iff n = 2m**. Dimensional consistency for a
  constant of proportionality of a dimensionless ratio forces the same relation.
- *Cosmological-constant route (independent representation, §5):*
  `Lambda_eff = 8 pi G_bare eps_vac/c^4` and
  `a0 = kappa c sqrt(G_cosmo rho_Lambda)` with `rho_Lambda = eps_vac/c^2` give
  `a0^2 = kappa^2 G_cosmo lambda (n-1) |q|^n`, which is consistent with
  `a0^2 = beta^2 |q|^(2m)` iff `n = 2m` and then `kappa^2 = beta^2/(G_cosmo lambda (n-1))`.
  Both routes agree; the exponent condition is coupling-ratio independent.

## 3. Step 3 — keep every integration constant and coupling independent until an equation fixes it

- `q` was never eliminated by hand: it enters (2) explicitly and survives into the
  condition (4) through the exponent balance. The cancellation at n = 2m is
  **derived**, not imposed by normalisation.
- `lambda`, `beta` (and, in the k04 kernel, `Z`, `b`) remain free couplings. At
  n = 2m the deep observables fix exactly **one** relation (6) in the three
  unknowns `(lambda, beta, n)` (n enters via its exponent role and via `n-1` in the
  denominator). Identifiability (B2): the constraint manifold has
  `rank J = 1`, residual freedom 2, exhibited by two explicit one-parameter
  families with identical κ = 1/2:
  - `(lambda, beta) -> (t^2 lambda, t beta)` at fixed n leaves `lambda/beta^2`
    invariant (exact);
  - `lambda(n) = 4 beta^2/(G_N (n-1))` solves kappa = 1/2 for **every** n > 1 (exact).
- Consequence: the seed's "why this half?" is now phrased as **why
  `lambda G_N/beta^2 = 4/(n-1)`**, in direct generalisation of k04's
  "why Z/beta^2 = 8 - 2b = 7.96". The amplitude problem is closed; the
  **coefficient problem is not** — one datum replaced by one ratio, rank 1, the
  same structure AS063 found for the product n·λ.

## 4. Step 4 — altered premise: infer amplitude cancellation for arbitrary (n,m) → FALSE

Negative control (B1, capable of failing — it fails):
attempt the inference "κ_N² is amplitude-independent for arbitrary n, m".
From the original equation (2) the residual is exact:

```text
kappa_N^2(q2)/kappa_N^2(q1) = (q2/q1)^(2m - n)                                       (7)
```

Fixtures (mpmath 80 digits, q1 = 1, q2 = 2):

| (n, m) | 2m − n | κ²(2)/κ²(1) | cancellation |
|---|---|---|---|
| (3, 1) | −1 | 0.5 | **fails** (residual q^−1) |
| (5, 2) | −1 | 0.5 | **fails** |
| (3/2, 1) | +1/2 | 1.414213562… | **fails** |
| (4, 1) | −2 | 0.25 | **fails** |
| (2, 1) | 0 | 1.0 (exact) | cancels |
| (3, 3/2) | 0 | 1.0 (exact) | cancels |
| (4, 2) | 0 | 1.0 (exact) | cancels |

Endpoint behaviour at fixed `(lambda, beta, G_N)`: for `n = 2m`, κ² → constant as
q → 0; for `n > 2m` (e.g. (3,1)) κ² ~ q^{2m-n} → **∞** as q → 0 — the deep-law
coefficient runs with the flux and diverges toward the vacuum-off limit; for
`n < 2m` it → 0. The lost hypothesis for cancellation is exactly
`2m − n = 0`; every "proof" of amplitude independence for arbitrary (n,m)
must silently assume it (this is the false premise the control removes).
The control is a genuine discriminator: it passes on (2,1), (3,3/2), (4,2) and
fails on four distinct (n,m) with the residual exponent exhibited.

The scalar implication for the framework: with n ≠ 2m, a region-by-region flux
(which k04 F3 already shows is environmental) would make a0, and with it the whole
deep law `v_flat^4 = G M_b a0`, position- and flux-dependent — **acceleration
homogeneity fails**; n = 2m is precisely the flux-power condition that fixes
acceleration homogeneity.

## 5. Step 5 — verification: substitution and the independent k04 representation

**(a) Substitution (exact).** Plugging `P = lambda q^n`, `a0 = beta q^m` into the
definition `kappa_N^2 = a0^2/(G_N (q P_q - P))` and simplifying symbolically
returns (2) identically (A2: sympy residual 0). Substituting n = 2m returns (5)
(A3a: q-free, dκ²/dq = 0 exact).

**(b) k04 kernel reproduction (independent representation, A5).** k04's own kernel
`P = Z q^2/2 + b beta^2 q^2`, `a0 = beta sqrt(G) |q|` is the (n=2, m=1) instance
with `lambda = Z/2 + b beta^2`. The general formula (2) specialised reproduces

```text
kappa^2 = 2 beta^2 / (Z + 2 b beta^2)        (k04 F2, exact)
kappa = 1/2  <=>  Z / beta^2 = 8 - 2 b
```

(with the convention map beta_k04² = G · beta_cell², G = G_N in k04's single-G
cell). Numerically with the RAR kernel of the cited source
(Delta(s) = s/(e^{sqrt s} − 1), b = 2 I/(16 pi), I = j_sat computed at 80 digits):
`I = 0.45252…`, `b = 0.01801…`, `Z/beta^2 = 7.96399…`, matching the source's
stated 7.96 (A5d).

**(c) Cosmological-constant route (independent representation).**
`Lambda_eff = 8 pi G_bare rho_Lambda/c^2` with `rho_Lambda = eps_vac/c^2`:
`Lambda_eff = 8 pi G_bare lambda (n-1) |q|^n/c^4`; combined with
`a0 = kappa c sqrt(G_cosmo rho_Lambda)`:
`kappa^2 = a0^2/(G_cosmo eps_vac) = beta^2 |q|^(2m-n)/(G_cosmo lambda (n-1))` —
identical exponent structure to (2) with G_N → G_cosmo; amplitude independence
iff n = 2m in every coupling convention. The measured ratio used by the seed,
`a0^2/(G_N eps_vac)`, differs from the vacuum-definition κ² only by the ratio
`G_cosmo/G_N` — the exponent condition is unaffected.

**(d) Finite fixture + refinement (C1, mpmath 80 digits).** Fixture
(n=2, m=1, beta=1, G_N=1, lambda=4): κ²(q) = 1/4 to 80 digits for
q ∈ {1e-12, 1, 1e12}; refinement dps 50 → 80 identical. Failing fixture
(n=3, m=1): κ²(1) = 1/2, κ²(2) = 1/4 with ratio 2^{2m−n} = 2^{−1} exact to 80
digits.

## 6. Lean certificate (formal, compile-verified)

`AS653_certificate.lean` — 8 theorems + derivative fact, zero `sorry`,
`lake env lean` exit 0, and the unfiltered `#print axioms` output for every
theorem is exactly `[propext, Classical.choice, Quot.sound]`:

- **T1** derivative fact `HasDerivAt (fun t => lam*t^n) (n*lam*q^(n-1)) q` (q>0)
  + Legendre identity `epsVac = lam*(n-1)*q^n`;
- **T2** sign control `0 < epsVac` for lam>0, n>1, q>0;
- **T3** the ratio: `kappa2 = beta^2*q^(2m-n)/(gN*lam*(n-1))` (exact, q>0);
- **T4** amplitude-free: `n = 2m` ⟹ κ²(q1) = κ²(q2) for all q1,q2 > 0;
- **T5** analytic lemma `(2:ℝ)^a = 1 ⟹ a = 0` (Real.log route);
- **T6** negative control: `2m − n ≠ 0 ⟹ κ²(1) ≠ κ²(2)` — the formal witness
  that arbitrary-(n,m) cancellation fails;
- **T7** the equivalence: (∀ q1 q2 > 0, κ²(q1) = κ²(q2)) ↔ n = 2m;
- **T8** coefficient gate: n = 2m ∧ `lam*(n-1)*gN = 4*beta^2` ⟹ κ² = 1/4.

Compile command (compile host only — no files written into `fable_independent_2026/lean_2026`):
`cd fable_independent_2026/lean_2026 && timeout 580 lake env lean <run_dir>/AS653_certificate.lean`
(exit 0) and the axioms probe (exit 0, output in `raw_outputs/AS653_axioms.out`).
Lean 4 (version per lakefile; `Real.hasDerivAt_rpow_const` present,
`sq_ne_zero`/`nlinarith`/`ring_nf` absent — worked around, see failed_attempts).

## 7. Exact claim and domain

**Claim.** In the k04 four-form cell with `P(q) = lambda |q|^n` (lambda > 0,
q ≠ 0, n > 1) and promotion `a0 = beta |q|^m` (beta > 0, m > 0):

(i) `kappa_N^2(q) = a0^2/(G_N eps_vac) = beta^2 |q|^(2m-n)/(G_N lambda (n-1))` — exact,
with `eps_vac = lambda (n-1) |q|^n` the Legendre vacuum energy (positive iff n > 1);
(ii) amplitude independence ⟺ **n = 2m** — equivalently, κ_N² dimensionless ⟺
n = 2m (dimensional route); residual exponent `2m − n`, exhibited in (7) and at
the q→0 endpoints;
(iii) at n = 2m, `kappa_N^2 = beta^2/(G_N lambda (2m-1))`; kappa = 1/2 requires
`lambda G_N/beta^2 = 4/(n-1)` — one relation in three couplings (rank 1), so the
**coefficient** remains a free datum (k04's "why Z/beta^2 = 8" generalised);
(iv) k04's amplitude cancellation is the n = 2m = 2 instance (reproduced exactly,
numeric b = 0.01801, Z/beta^2 = 7.96399 vs 7.96);
(v) negative control: for arbitrary (n,m) the cancellation inference is **false**;
it fails exactly when 2m − n ≠ 0, with the residual quantified.

**Domain.** Homogeneous vacuum cell, q ≠ 0, lambda > 0, n > 1, m > 0; identities
exact (sympy + Lean), finite witnesses mpmath 80 digits with a 50→80-digit
refinement. The statement is dimensionless in the exponents and applies
**identically to both footings** (canonical 9.3619e-11 and alternative
1.1279e-10 m/s²; the footings fix only the numerical wrapper a0 ↔ rho_Lambda,
reported separately in B3). Excluded: local-sector environmental feedback
(k04 F3 — a separate equation making a0 position-dependent), filtered MONO and
criterion B, nonspherical geometry, and any derivation of the value 1/2 itself.

## 8. Closure implication and next unresolved bridge

**Named gate:** CORE coefficient κ-cell of the four-form promotion (the k04
"why Z/β² = 8" gap) / acceleration-homogeneity gate.
**Implication:** a pure-power flux sector renders the deep-law coefficient
flux-independent **iff n = 2m**; under that condition the acceleration scale is
homogeneous in the flux, and the kappa value reduces to the single ratio
`lambda G_N/beta^2 = 4/(n-1)`. The amplitude half of the coefficient mechanism is
derived; the value half is not.
**First missing bridge (next_unresolved_implication):** an equation that fixes the
ratio `lambda G_N / beta^2` (equivalently k04's Z/β²) — i.e. a fourth datum or a
dynamical relation beyond the Legendre/vacuum cell (e.g. the local feedback
equation of k04 F3, a nucleation/brane boundary condition in the
Bousso–Polchinski sense, or a coupling-variation identity tying lambda to the
already-counted degrees of freedom of the common action). Without it, κ = 1/2 (and
any value) remains an adopted input; n = 2m is necessary but not sufficient for
closure of this gate.
**Compatibility note:** this result does not transfer to the operative filtered
MONO target (criterion B); a separate bridge (deep-slope transfer in the MONO
variable set, as named by AS051) would be required. G_N/G_bare/G_cosmo are kept
separate; the exponent condition is invariant under their ratios, the coefficient
relation is quoted per convention.

## 9. Numbers produced (all real — no synthetic results)

- 26/26 checks PASS; wall 0.16 s (deadline 120 s enforced in-process,
  `time.monotonic()` checkpoint + abort), peak RSS 63.5 MB (≤ 512 MB; RLIMIT_AS
  not settable on macOS — in-process RSS watchdog enforced), 1 thread
  (single process, OMP_NUM_THREADS=1).
- Lean: compile exit 0 ×2 (certificate + axioms probe), axioms exactly
  {propext, Classical.choice, Quot.sound} for all 9 statements, zero sorry.
- Raw outputs: `raw_outputs/compute_as653.out`, `raw_outputs/checks.json`,
  `raw_outputs/compute_as653.time`, `raw_outputs/AS653_axioms_probe.lean`,
  `raw_outputs/AS653_axioms.out`, `raw_outputs/probe_api{1,2,3}.lean`
  (Lean API probes).

failed_attempts (implementation, all resolved):
- compute_as653.py ×3: `check()` missing default tolerance; sympy `Symbol('G')`
  assumption-mismatch in the k04 convention map (A5b) — fixed by substituting
  `(G, G_N)` on the same symbol; `mpmath.findmax` absent in this build — replaced
  by grid + `findroot` of the derivative (A5d).
- AS653_certificate.lean ×4 iterations: `hasDerivAt_rpow_const` has implicit p;
  `← rpow_one` over-rewrites (base q became q^1 inside q^(n-1)) — replaced by a
  calc; Nat-vs-Real exponent clash on `(q^m)^2` — bridged by `pow_two` +
  `rpow_add`; `field_simp at heq` cancels beta² and flips orientation (heq :
  1 = 2^a) — `exact heq.symm`; `rw [← hc']` direction — `rw [hc']`. All resolved.
