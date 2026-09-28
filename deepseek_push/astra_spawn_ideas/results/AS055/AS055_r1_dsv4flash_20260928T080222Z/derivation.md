# AS055 — Correlation freedom in the two-channel response: derivation and audit

**Run:** `AS055_r1_dsv4flash_20260928T080222Z` · **Seed sha256:** `e112db835db90d562d53e8e0c756263460a63623d9cd029edb9d976666784e38`
**Framework (mandatory input):** `a0 = kappa*c*sqrt(G*rho_Lambda)`, `kappa = 1/2` ADOPTED;
`s = c*sqrt(G*rho_L)`, `Y = g/s`, `rho_L = lambda*rho_Lambda` ⇒ `s = 2*a0*sqrt(lambda)` on
the canonical footing.  Branch used: CORE coefficient; conditional MU_n statistical
response.  Q, RAR, MU2, EXP, MONO are used only as labelled comparisons (MU2 is the
independent two-channel member of the statistical family under test); no other branch is
imported to repair anything.

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Claim under audit.**  The corpus derives `kappa = 1/2` from a channel count: PD01
("the slope is a channel count, completion-independently") asserts that in the OR class
-- *n equal, independent* channels with per-channel engagement `p(Y)`, `p(0)=0`,
`p'(0)=1`, `p(inf)=1` -- the response `U = 1-(1-p)^n` has deep slope `n`, so the metric
carrier's TWO channels give deep slope 2 and `kappa = 1/n = 1/2` (PD08 Step 5).  This
audit asks whether that derivation removes a *genuinely independent freedom*.  A
derivation of kappa must remove an independent freedom; a channel count or adopted
normalisation is useful only with its physical identification separately justified.

**Symbol dictionary (all SI unless dimensionless).**

| symbol | meaning | value / status |
|---|---|---|
| `a0` | framework acceleration scale | `9.3619e-11 m/s^2` (canonical), `1.1279e-10 m/s^2` (alternative) — input footings |
| `kappa` | `a0 / (c sqrt(G rho_Lambda))` | `1/2` ADOPTED (canonical); `0.602388` (alternative at fixed rho_Lambda) |
| `rho_Lambda` | vacuum mass density | fixed from canonical footing: `rho_Lambda = 4*a0^2/(G c^2)` |
| `s` | two-channel scale `c*sqrt(G rho_L)` | `1.87238e-10 m/s^2` at lambda = 1, i.e. `2*a0_canonical` (verified, rel. < 1e-9) |
| `lambda` | `rho_L / rho_Lambda` | diagnostics at `1/2, 1, 2` |
| `Y` | `g/s` | dimensionless, `>= 0` |
| `p(Y)` | per-channel engagement probability | `p = Y/(1+Y)` (the corpus's member; `p(0)=0`, `p'(0)=1`, `p(inf)=1`) |
| `A, B` | channel-engagement events | `P(A) = P(B) = p`, `p in [0,1]` |
| `U(p)` | `P(A ∪ B)` = two-channel response | `2p - P(A∩B)` |
| `C(p)` | correlation correction `P(A∩B) - p^2` | deviation from stochastic independence |
| `alpha` | family parameter `C_alpha(p) = alpha (p - p^2)` | `alpha in [0,1]` |
| `n` | channel count (independent class) | integer `n >= 1`; fractional n is diagnostic only |
| `mu_n(Y)` | `1 - (1+Y)^(-n)` | independent-n-channel response; MU2 = `mu_2` |

**Boundary conditions / normalisations used (all stated, none silently imported from a
different branch):** `U(0) = 0` (zero drive ⇒ no union response), `U(1) = 1` (both
channels certain ⇒ union certain), `lim_{Y→∞} U = 1` (saturation, the corpus L230
normalisation), `p(0) = 0`, `p'(0) = 1` (the s-unit fraction identity, PD08 Step 3),
`p(inf) = 1`.

**Assumptions (explicit, conditional):** (A1) the two-channel response is a Boolean OR
of two engagement events with equal marginals `p` — a *statistical* model; the audit
does not assert that a probability space exists in the gravity field (the seed: "do not
assume statistical events actually exist"); (A2) the common engagement is
`p(Y) = Y/(1+Y)` for the finite-part checks (the slope statements are completion-free
within the OR class, as in PD01 Part A).  Everything below is a **conditional theorem**;
conditions are listed in §7.

**Framework inputs vs conclusions:** `kappa = 1/2`, both `a0` footings, `rho_Lambda`,
`G`, `c` are inputs.  Conclusions to be established: admissible bounds on `C`; the
effect of a nonzero linear term in `C` on the deep slope; the sharp union bounds; the
negative control; the mapping of the correlation freedom onto the kappa-normalisation
freedom.

---

## 2. Step 2 (seed order) — admissible probability bounds on C; how a nonzero linear
##    term changes the deep slope

For two events of common probability `p` the intersection is Fréchet-bounded:

```
max(0, 2p-1) <= P(A∩B) <= p        (1)
```

so the correlation correction obeys

```
max(0, 2p-1) - p^2 <= C(p) <= p - p^2        (2)
```

In particular `-p^2 <= C(p) <= p - p^2` (the box used in the Lean certificate).
The union response is

```
U(p) = 2p - p^2 - C(p)                        (3)
```

and by (1)–(3) — or directly from `P(A∪B) >= P(A)` and `P(A∪B) <= P(A)+P(B) <= 1`:

```
p <= U(p) <= min(2p, 1)                        (4)   sharp.   (Lean: as055_union_bounds)
```

Sharpness: `U = p` ⟺ `C = p - p^2` ⟺ `P(A∩B) = p` ⟺ `A = B` a.s. (**perfect
correlation**); `U = 2p` ⟺ `P(A∩B) = 0` (**mutual exclusion**, possible only for
`p <= 1/2`).  Note `2p - p^2` (independence) is an *interior* member of `[p, min(2p,1)]`,
not an upper bound: anticorrelated channels give `U = 2p > 2p - p^2` (verified, B3).

**Linear term.**  Let `C(p) = theta*p + O(p^2)` (theta admissible in `[0,1]` by (2),
since `C(p)/p in [-p, 1-p]`).  Then

```
U(p) = (2 - theta) p - (1 + c2) p^2 + ...        (5)
```

so the **deep slope is `2 - theta`**, i.e. a nonzero linear term in the correlation
correction lowers the deep slope from 2 toward 1; a quadratic term changes only the
subleading coefficient (verified B5).  Realised family

```
C_alpha(p) = alpha (p - p^2),   alpha in [0,1]:
   P(A∩B) = p^2 + alpha (p - p^2)  in [p^2, p]   (between independence and identity)
   U_alpha(p) = (2 - alpha) p - (1 - alpha) p^2
   deep slope  = 2 - alpha                         (6)
```

**Exact closed form in Y** (`p = Y/(1+Y)`):

```
U_alpha(Y) = (Y^2 + (2 - alpha) Y) / (1 + Y)^2    (7)   (Lean: as055_alpha_family)
```

**Scale and units:** every quantity above is dimensionless.  `s = c sqrt(G rho_L)`:
`[m/s] * sqrt([m^3 kg^-1 s^-2] [kg m^-3]) = [m/s^2]`; with `rho_L = lambda rho_Lambda`
and `a0 = (1/2) c sqrt(G rho_Lambda)` we get `s = 2 a0 sqrt(lambda)` on the canonical
footing (verified numerically: `s = 1.87238e-10 = 2 * 9.3619e-11`).

**General n (independent class, seed's "symbolic n >= 1").**  For n equal, *independent*
channels `U = 1 - (1-p)^n = 1 - (1+Y)^(-n) = mu_n(Y)` (verified A3), deep slope `n`
(D3).  Fractional n (e.g. `n = 1/2`, slope `1/2`) is a response-family diagnostic with
**no** channel-count (OR) reading.

---

## 3. Step 3 (seed order) — intermediate algebra with scale factors, signs, units
##    and the limiting-regime leading terms

**Spherical deep matching** (PD08 Step 5 generalised to slope `m = 2 - theta`): with
`mu ≈ m Y = m g/s` the static equation `(1/r^2) d/dr [r^2 g mu] = 4 pi G rho` for a
point mass `M` gives `m g^2 r^2 / s = G M`, i.e.

```
g^2 = (s/m) g_N ,    a0_eff = s/m = kappa_eff s ,    kappa_eff = 1/m = 1/(2 - theta)   (8)
```

At fixed vacuum density (`lambda = 1`, `s = 2 a0`):

| `alpha` | `theta = alpha` | deep slope `m = 2-alpha` | `kappa_eff = 1/m` |
|---|---|---|---|
| 0 (independence) | 0 | 2 | **1/2 = canonical** |
| 0.339941 | 0.339941 | 1.66014 | **0.602388 = alternative footing** |
| 1 (perfect correlation) | 1 | 1 | 1 |

In `x = g/a0` units the deep x-slope is

```
sigma_x = (2 - alpha) * a0/s  =  (2 - alpha)/(2 sqrt(lambda))       (9)
```

**Diagnostic counterexamples at lambda = 1/2, 1, 2** (seed requirement): the *identical*
two-channel model with the *same* correlation gives different deep x-slopes —
`lambda=1/2,alpha=0: sqrt(2) = 1.4142`; `lambda=1,alpha=0: 1`; `lambda=2,alpha=0:
1/sqrt(2) = 0.7071`; `lambda=1,alpha=1: 1/2` (all verified, C1, residual
`<= 9e-25`).  The deep slope is fixed by the **pair** `(alpha, lambda)`, never by the
channel count alone; the observed deep law fixes only the combination
`(2 - alpha) a0/s = 1` (unit x-slope, gate check D2).  This is the operator-level
content of the audit: a measured deep slope cannot be inverted to a channel count
without adopting both the correlation and the vacuum-density scale.

**Both footings separately:** canonical `x' = g/9.3619e-11`: x'-slopes `alpha = 0 -> 1`
(unit; the deep law `g^2 = a0 g_N`), `alpha = 1/3 -> 2/3`, `alpha = 1 -> 1/2`.
Alternative `x' = g/1.1279e-10`: `alpha = 0 -> 1.2048` (NOT unit: the alternative
footing is *not* the independent two-channel result), `alpha = 0.339941 -> 1` (the
alternative footing IS the correlated two-channel model with
`theta = 2 - 1/kappa_A = 0.339941` at fixed `rho_Lambda`), `alpha = 1 -> 0.6024`.
Equivalently, at fixed `kappa = 1/2` the alternative magnitude requires the changed
density `lambda = (a0_A/a0_C)^2 = 1.451487` (contract: "if rho_Lambda is held fixed,
compute its effective kappa; if kappa is held fixed, identify the changed density" —
both done, C2, consistency `(2 - alpha_alt) a0_A/s = 1` to < 1e-30).

**Limiting regimes.**  Deep: slope freedom `[1,2]` (above).  Newtonian: exact identity
`1 - U_alpha(Y) = (1 + alpha Y)/(1+Y)^2` (verified, D1, residual < 1e-60 at Y = 1e8);
`U -> 1` for every admissible `C` with subleading `O(1/Y)` for `alpha > 0`,
`O(1/Y^2)` for `alpha = 0` (independence saturates fastest).  Boundary: `U(0) = 0`,
`U(1) = 1` (A4b); `C(1) = 0` is forced by the Fréchet upper bound.

---

## 4. Step 4 (seed order) — independent check in a different representation

High-precision prototype `as055_correlation_audit.py` (mpmath, dps 80; dps 200 for the
cancellation-sensitive general-n block; deterministic seed 5521; single thread;
wall 0.034 s; RLIMIT_AS 512 MiB enforced in-process, peak RSS 19.8 MB).  Residuals,
not booleans:

| check | representation | measured residual | tolerance → verdict |
|---|---|---|---|
| A1 | `2p-p^2` vs `1-(1+Y)^(-2)`, p = Y/(1+Y), 34-pt log grid 1e-8..1e8 | max < 1e-45 | 1e-45 → **PASS** |
| A2 | alpha-family vs closed form (7), alpha in {0, 1/3, 0.33986, 1} | max < 1e-45 | 1e-45 → **PASS** |
| A3 | `1-(1-p)^n` vs `1-(1+Y)^(-n)`, n in {1,2,3,5} | max < 1e-45 | 1e-45 → **PASS** |
| A4/A4b | Frechet box + normalisation | exact | → **PASS** |
| B1 | slope `(U(eps)-U(0))/eps` vs exact finite-eps `(2-alpha)-(1-alpha)eps`, eps 1e-6..1e-12 | max < 1e-50 | 1e-50 → **PASS** |
| B2 | **negative control** perfect correlation: slope at eps 1e-6..1e-12 | = 1 to < 1e-30, and |slope-2| > 0.5 | **PASS** |
| B3 | mutual exclusion `U = 2p`, p in {0.1, 0.3, 0.49}; `U > 2p-p^2` | exact | → **PASS** |
| B4 | 2000 seeded arbitrary admissible C: `p <= U <= min(2p,1)` | 2000/2000 | exact → **PASS** |
| B5 | quadratic correlation term: slope still `2 - alpha` (finite-eps prediction) | < 1e-50 | 1e-50 → **PASS** |
| C1 | sigma_x = (2-alpha)/(2 sqrt(lambda)), lambda in {1/2,1,2} | rel. err <= 9e-25 (two-point estimator floor) | 1e-20 → **PASS** |
| C2 | alternative footing decomposition (kappa_A, alpha_alt, lambda_alt; consistency 1) | < 1e-30 | → **PASS** |
| C3 | x'-slopes per footing (unit law on both footings) | < 1e-30 | → **PASS** |
| D1 | Newtonian exact identity | < 1e-60 | 1e-60 → **PASS** |
| D2 | operative-gate deep x-slope mu2'(0) = 1 | 1 + O(1e-24) | 1e-20 → **PASS** |
| D3 | independent class slope = n (geometric-sum prediction), n in {1,2,3,5}; n=1/2 diagnostic | < 1e-55 | 1e-55 → **PASS** |
| SCALES | s = 2 a0_canonical | rel. < 1e-9 (a0 rounding) | → **PASS** |

**17/17 PASS, exit 0.**  B2 is a control that was *capable of failing*: had the
categorical claim "deep slope = channel count = 2 for the two-channel OR" been asserted
without fixing the correlation, perfect correlation would have falsified it; it failed
to reach slope 2 by construction (`= 1` to < 1e-30).

---

## 5. Step 5 (seed order) — negative control, strongest surviving statement, and the
##    first additional implication

**Negative control (specified):** perfectly correlated channels (`C(p) = p - p^2`,
`P(A∩B) = p`, `A = B` a.s.) give deep slope **one, not two** — PASS (§4 B2;
Lean `as055_perfect_corr_slope`).

**Strongest surviving statement (conditional theorem, all conditions in §7):**

> In the two-channel OR model with common engagement `p(Y) = Y/(1+Y)` and correlation
> correction `C(p) = P(A∩B) - p^2`, the union response satisfies the sharp bounds
> `p <= U <= min(2p,1)`, equivalently
> `max(0,2p-1) - p^2 <= C(p) <= p - p^2`; if `C(p) = theta p + O(p^2)` the deep slope is
> `2 - theta` with `theta in [0,1]`; the family `C_alpha = alpha(p-p^2)` realizes every
> slope `2 - alpha in [1,2]`.  In the spherically matched gravity law
> `g^2 = (s/m) g_N` this is `kappa_eff = 1/(2 - theta) in [1/2, 1]` at fixed vacuum
> density, and `sigma_x = (2-alpha)/(2 sqrt(lambda))` at general density ratio.  Within
> the stochastically independent class (`C ≡ 0`) the slope is the channel count `n` for
> every integer `n >= 1` (completion-independent, PD01 Part A holds).

**Audit verdict on the sources** (PD01 `37e39d…74d`, PD08 `83f605…0cfb`,
k01 `8df5a3…b25c`; hashes match SOURCE_MANIFEST.json): the two-channel *derivation* of
`kappa = 1/2` does **not** remove the correlation freedom — it adopts it.  Specifically:

1. PD01's OR class is defined as "n equal, **independent** channels": the slope = count
   theorem is true **inside that class** (re-verified, A1/A3/D3) but the independence
   premise has no physical identification in the sources.  The metric's two Poisson
   operators (PD01 part 2) are **operator-decoupled** — `G00 = 2∇²Psi`,
   `Gkk = 2∇²(Phi-Psi)` are two independent *linear operators* — while the slope
   theorem needs **stochastic** independence of the engagements.  Operator decoupling of
   equations that share the same single source `rho_b` and the same potentials does not
   imply `P(A∩B) = P(A)P(B)`.  This is the "genuinely independent freedom" the seed
   asks about: `C'(0) = theta in [0,1]` is unconstrained by anything in PD01/PD08/k01.
2. Pedantically, the binary claim "kappa in {1/2, 1}" (PD01 part 2) is **false within
   the OR model with free correlation**: the continuum `kappa in [1/2, 1]` includes the
   project's own alternative footing `kappa = 0.6024 in (1/2, 1)` — which is exactly the
   two-channel response with `theta = 0.3399` (C2/C3).  Only re-imposing independence
   restores the binary outcome.
3. k01's zero-mode theorem is the same missing-premise pattern at the action level: no
   local action fixes the absolute normalisation, and the correlation slot is one more
   unconstrained normalisation.  PD01 part 3 (the data selection) is *skipped here* as a
   data comparison: the audit's finding is structural (the count derivation leaves an
   independent freedom), and the audit makes no claim about which empirical kappa the
   data prefer.

**First additional implication needed to transfer the result to the full theory** (the
exact unresolved implication): the physical identification or derivation of the
correlation structure — a probability space whose events are the two sector
engagements, or an independent argument fixing `P(A∩B)(p)` (equivalently `theta`) from
the carrier dynamics; or a no-go proof that no such probability space exists in a
deterministic two-Poisson-sector theory (G009's predicted zero shot noise is evidence in
that direction but not the required derivation).  Until then `kappa = 1/2` (and
`alpha = 0`) remains an **adopted** normalisation, and **any** value in the alternate
footing's neighbourhood is equally derivable from the two-channel response — the
correlation freedom is exactly the kappa freedom re-parameterised.  No other branch
(Q/RAR/MU2/EXP/MONO) is imported to repair this; the seed's instruction "do not assume
statistical events actually exist in the gravity field" is respected by keeping every
gravity-facing statement conditional on the statistical model.

---

## 6. Lean certificate

File: `AS055_correlation_freedom.lean` (in this run dir), compiled with
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>` on
Lean 4.34.0-rc2 (lakefile.toml toolchain `leanprover/lean4:v4.34.0-rc2`).
**Exit 0, zero sorry, axiom sets (unfiltered `#print axioms`, in `lean_output.txt`):**

```
'as055_independent_union_mu2'      depends on axioms: [propext, Classical.choice, Quot.sound]
'as055_alpha_family'               depends on axioms: [propext, Classical.choice, Quot.sound]
'as055_union_bounds'               depends on axioms: [propext, Classical.choice, Quot.sound]
'as055_perfect_correlation'        depends on axioms: [propext, Classical.choice, Quot.sound]
'as055_alpha_family_admissible'    depends on axioms: [propext, Classical.choice, Quot.sound]
'as055_deep_slope_family'          depends on axioms: [propext, Classical.choice, Quot.sound]
'as055_perfect_corr_slope'         depends on axioms: [propext, Classical.choice, Quot.sound]
```

i.e. axioms ⊆ {propext, Classical.choice, Quot.sound} — the hard bar.  Certified
content (dimensionless; applies to both a0 footings unchanged): (1) independent-OR ==
MU2 identity `1-(1+Y)^(-2) = 2p-p^2`; (2) alpha-family closed form; (3) sharp union
bounds `p <= U <= 2p` from the Fréchet box; (4) perfect-correlation collapse `U = p`;
(5) alpha-family admissibility `p^2 <= P(A∩B) <= p`; (6) deep slope `2 - alpha` as a
genuine Tendsto limit at the punctured origin; (7) the negative control slope 1.  House
traps applied: `mul_left_cancel₀` not needed; no trailing tactic after a closing
`field_simp`; `Tendsto.congr'` with the eventually-eq argument first
(`(hcont.tendsto.mono_left nhdsWithin_le_nhds).congr' hEq.symm`, the H046-validated
idiom).

---

## 7. Domain, conditions, limitations

**Domain.** `p in [0,1]`; `Y in [1e-8, 1e8]` (34-pt log grid), finite-part checks;
`alpha in {0, 1/3, 0.33986, 1}` (the continuum result is analytic, (5)-(6));
`n in {1,2,3,5}` integer + `1/2` diagnostic; `lambda in {1/2, 1, 2}`; 2000 seeded
arbitrary admissible C samples; both footings; eps in {1e-6, 1e-9, 1e-12}; dps 80
(200 for D3).

**Conditions of the theorem.** (C1) a probability space with events A, B exists and
models the two-channel response (NOT established for the gravity field — open
dependency); (C2) equal marginals `P(A) = P(B) = p`; (C3) the union is the observable
response (no interference between channels at the response level); (C4) `p(Y) = Y/(1+Y)`
for the finite-part numerical claims (slope claims are completion-free, PD01 Part A);
(C5) the spherical matching (8) applies.  Missing dynamics or data is an explicit open
dependency, never a pass.

**Limitations.** (i) Conditional on the statistical model; a deterministic field theory
may admit no such probability space — the audit does not assume one exists and does not
construct one.  (ii) No action, no dynamics, no criterion-B or well-posedness content:
this audit concerns the coefficient/premise structure only.  (iii) A finite grid or a
finite residual is finite evidence; the structural statements are additionally
Lean-certified.  (iv) No observational comparison was run (PD01 part 3 is out of scope
for the premise audit); notably, "a nonzero linear term changes the deep slope" says
nothing about which `theta` the data select.  (v) The mapping `kappa = 1/(2-theta)` is
at fixed vacuum density and within the OR model; it is not a claim about any other
kappa-derivation route.  (vi) `p(0)=0, p'(0)=1` (PD08 Step 3) is used as an adopted
normalisation, not re-derived.

## 8. Closure implication and children (ready specs, NOT dispatched)

**Closure implication.**  Affected operative gate: amended requirement 13 (a0–vacuum
relation preserved as input or genuinely derived).  Implication: the two-channel
response does not provide the genuinely derived option; the relation stays inside the
"preserved as input" branch; the correlation freedom is the exact missing premise.
No closure candidate submitted (`closure_candidate = null`).

**Child proposals (specifications only; no worker ran them):**
- **AS055.C01** — *Target-native repair/no-go:* derive `P(A∩B)(p)` for the two Poisson
  sectors from carrier dynamics, or prove no such probability space exists in the
  deterministic theory.  New target: joint engagement distribution of the two sectors
  conditional on a single source `rho_b`; parent: this run (`AS055_r1_…080222Z`
  sha256 of derivation.md); dependencies: PD01 part 2 (operator structure at pinned
  hash).  Control: the constructed P satisfies the Fréchet bounds and differs from
  `p^2` on a nonempty set — or the no-go proof.  Why existing evidence does not answer
  it: PD01 part 2 gives operator decoupling only; G009 gives shot-noise zero, which
  argues against any stochastic reading but is not a derivation of the correlation.
- **AS055.C02** — *Gate consequence:* with `theta` free, the deep-law zero point fixes
  only `a0 = s·(1 - theta/2)…`-combination; propose the distinct observable that could
  separate `(kappa, rho_Lambda, theta)` in the req-13 gate — e.g., a cross-sector
  covariance probe under a stochastic-source ensemble — and state its predicted value
  under the alpha-family.  Existing results do not answer this: no AS result fixes the
  correlation.
- **AS055.C03** — *Documentation of the premise:* convert "independence" into an
  explicit named axiom of PD01/PD08 (not a derivation), with the changed theorem
  statement `kappa = 1/2 ⟸ (count = 2 AND independence) AND spherical matching`; check
  which controls then remain non-circular.  (Review/cleanup role; no new computation.)

Duplicate check performed against `manifest.json`, `results/`, `claims/` and
`fresh_gravity_followups/queue.json` scope note: AS012 ("propagating correlated vacuum
uncertainties") concerns uncertainty propagation through the scale relation, not the
OR-class correlation freedom; no overlap found for these children.

## 9. Reproducibility

Run everything from the repository root:

```bash
R=deepseek_push/astra_spawn_ideas/results/AS055/AS055_r1_dsv4flash_20260928T080222Z
(cd $R && perl -e 'alarm 125; exec @ARGV' python3 as055_correlation_audit.py > raw_output.txt 2>&1)
cd fable_independent_2026/lean_2026 && lake env lean $PWD/../../$R/AS055_correlation_freedom.lean
```

Raw outputs: `raw_output.txt`, `raw_numerics.json`, `lean_output.txt`.  All input
hashes in `result.json` `input_sha256`; all artifact hashes in `artifacts_sha256`.