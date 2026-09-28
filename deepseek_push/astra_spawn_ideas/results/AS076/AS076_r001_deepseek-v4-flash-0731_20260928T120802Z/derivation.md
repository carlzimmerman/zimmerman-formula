# AS076 — Fixed-well Euler-Lagrange density

**Run:** `AS076_r001_deepseek-v4-flash-0731_20260928T120802Z`
**Worker:** deepseek-v4-flash-0731 (openrouter), Hermes subagent
**Task sha256:** `614a07d8f39fb2160d2f0a4b1b19bf56ac61409f1924910fabb5992473d84474` (verified on disk before execution)
**Status:** audit executed; scoped conditional theorem + quantified negative control; **unreviewed**.

Sources (hashes match SOURCE_MANIFEST.json):
- `deepseek_push/G084_maxentropy_law.py` `752999fdf6c07b0cf0fb419290177f90151a239d63c7707029b240fef46735ec`
- `deepseek_push/G091_virial_triad.py` `8164360f95fdc340824a92a5db3ccdabf3ce28430bdd1c375e276a77ba67ece5`
- `deepseek_push/G233_eos_noscalar.py` `ad89298d967ae4f2d574a47f91d5adc54addae40b6a5e47d0bd83cf5564a8b03`

Numerics (task mandate): `G = 6.67430e-11 m^3 kg^-1 s^-2`, `c = 299792458 m/s`,
`M_sun = 1.98847e30 kg`, `pc = 3.085677581491367e16 m`; `M_b = 7e10 M_sun` (MW proxy,
G233 register). Footings: canonical `a0 = 9.3619e-11` and alternative
`1.1279e-10 m/s^2` carried separately (C0).

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

**Claim under audit (the "Fixed-well Euler-Lagrange density" implication).**
In the fixed baryon well `Phi(r) = C ln(r/r_ref)` (`C = sqrt(G M_b a0)`, `r_M = sqrt(G M_b/a0)`),
on the finite shell `0 < r_in <= r <= R` (`R <= r_M` for the interior fixtures), with
`sigma` and the well fixed, the functional
`S - alpha M - beta E` with
`S = -int rho ln(rho/rho_ref) dV`, `M = int rho dV`,
`E = int rho (3 sigma^2/2 + C ln(r/r_ref)) dV`
is stationary at `rho(r) = A r^(-gamma)`, `gamma = beta C`; the *extra condition*
`beta = 1/sigma^2` (thermal identification) turns this into
`gamma = C/sigma^2`; with the virial input `sigma^2 = C/2` (G091),
`gamma = 2` exactly: `rho = A/r^2`, `A = M_b/(4 pi (R - r_in))`
(equipartition limit `A -> C/(4 pi G)` as `r_in -> 0`, `R -> r_M`).

**Symbol dictionary.** `rho` phantom mass density [kg m^-3]; `A` amplitude [kg m^-1]
(this is what `rho r^2 = A` implies: `A` has units of [kg/m] for the r^-2 law);
`C = v_flat^2 = sqrt(G M_b a0)` [m^2 s^-2]; `sigma` 1-D velocity dispersion [m s^-1];
`beta` energy Lagrange multiplier [s^2 m^-2]; `alpha` mass multiplier [1];
`gamma = beta C` [1]; `rho_ref`, `r_ref` reference scales (enter `A` only);
`Phi_self` phantom self-potential [m^2 s^-2].

**Assumptions (all stated).** (i) spherical, static, collisionless isothermal fluid
(no phase-space occupancy issues; Tremaine–Gunn excluded by scope, G084 V3);
(ii) imposed (baryon) log well, *not* the phantom's own gravity, is the potential in
`E`; (iii) `sigma` and the well are **fixed during the variation** (the seed's own
wording, step 2); (iv) `beta = 1/sigma^2` is an input (Boltzmann identification),
*not* a consequence of the variation (checked, C1b); (v) `sigma^2 = C/2` is an input
from G091 (virial + fluid closure; hash-verified derivation, not re-derived here);
(vi) the VACUUM scale enters only through `a0 = kappa c sqrt(G rho_Lambda)`,
`kappa = 1/2` adopted (framework input); `G_N = G_bare = G_cosmo` are **not** assumed
equal anywhere in this calculation — only `G_N` enters (via `C` and `Phi_self`).

**Framework inputs vs conclusions.** Inputs: `G_N`, `M_b`, `a0` (both footings),
`kappa = 1/2`, `rho_Lambda = 4 a0^2/(G c^2)`, `sigma^2 = C/2` (G091), `beta = 1/sigma^2`
(thermal identification), the shell `[r_in, R]`. Conclusions (derived here):
the EL stationary profile family `rho = A r^(-beta C)`; the exponent pinning
`gamma = 2` under (iv)+(v); the normalization `A = M_b/(4 pi (R - r_in))`;
the missing-term identity and self-consistency breakdown of the negative control;
the full-kernel error bound for the deep exterior.

---

## 2. The variation (seed step 2)

Functional `S - alpha M - beta E`, `Phi`, `sigma` fixed. First variation:

```
delta S = -int [ln(rho/rho_ref) + 1] delta rho dV
delta M = int delta rho dV
delta E = int (3 sigma^2/2 + C ln(r/r_ref)) delta rho dV
```

Stationarity `delta[S - alpha M - beta E] = 0` for all `delta rho` on the shell:

```
-ln(rho/rho_ref) - 1 - alpha - beta(3 sigma^2/2 + C ln(r/r_ref)) = 0
```

```
rho(r) = rho_ref exp(-1 - alpha - 3 beta sigma^2/2) * r^(-beta C)
       = A r^(-gamma),   gamma = beta C,
A = rho_ref exp(-1 - alpha - 3 beta sigma^2/2) r_ref^(beta C)   [kg m^-3]
```

All scale factors are explicit: `rho_ref` and `r_ref` enter `A` only; the exponent
`gamma = beta C` is dimensionless and reference-free. Units: `beta` [s^2 m^-2]
times `C` [m^2 s^-2] is [1]; `A` carries `[kg m^-3] * m^(beta C) = [kg m^-3]`.

**The extra condition `beta = 1/sigma^2` (C1b, capable of failing).**
The rho-variation leaves `beta` free. A sigma-variation does **not** produce
`beta = 1/sigma^2`:
- with the seed's `S` (no sigma-dependence): `d/d(sigma^2)[S - beta E] = -beta(3/2)M = 0`
  forces `beta = 0` (the E-constraint becomes inert);
- with G084's `S = -int rho ln(rho sigma^3/rho_ref) dV`:
  `-(3/2)M/sigma^2 - beta (3/2)M = 0` forces `beta = -1/sigma^2`.

So `beta = 1/sigma^2` is the independent thermal-equilibrium (Boltzmann)
identification `rho ∝ exp(-Phi/sigma^2)` for an isothermal fluid at temperature
`k_B T = m sigma^2` — exactly the seed's "identify the extra condition". With
`sigma^2 = C/2` (G091 input, hash-verified): `gamma = beta C = C/(C/2) = 2` exactly.

**Second variation / uniqueness (C3).** `-x ln x` is strictly concave
(`d^2/dx^2 = -1/x < 0`), both constraints are linear in `rho` at fixed well and
sigma, so `delta^2 S = -int (delta rho)^2/rho dV < 0` strictly: the stationary
point is the unique global maximum in the fixed well. Numeric central differences
on M- and E-preserving modes match `-eps^2 int dm^2/rho` to <5% (8 modes; fixture
(0.1, 0.62) r~M canonical).

**Dynamical attainment** is a *distinct* obligation: the max-entropy extremum is
not a dynamical attractor (G081 marginal mode `omega^2 = 0`; G035's Newtonian
attractor kill; entropy decreases along the local modes — G084). Not re-derived
here; recorded as the open dependency (see Section 6).

---

## 3. Intermediate algebra, integration, signs, units (seed step 3)

**Normalization (C2).** `M = int rho dV = 4 pi A int_{r_in}^R r^(2-gamma) dr`; at
`gamma = 2`:

```
A = M_b / (4 pi (R - r_in))        [kg m^-1]
```

verified to `1e-10` relative (all 6 fixtures, both footings), and

```
A * 4 pi G / C = 1 - r_in/R  ->  1       (equipartition limit, r_in -> 0, R -> r_M)
=> A -> C/(4 pi G) = sqrt(G M_b a0)/(4 pi G)
```

(canonical `3.516e19 kg/m`, alt `3.860e19 kg/m`).

**Second-variation integral** is closed-form exact (`-int (drho)^2/rho`).
**Energy/entropy diagnostics** (constraint values at the stationary profile,
`rho_ref = 1 Msun/pc^3`, `r_ref = r_M`): e.g. canonical (0.01, 1.0) fixture
`E = -8.353e50 J`, `S = 4.642e41 kg` (constants shift `A` only). These are
diagnostics, not conclusions: the max-entropy `E` is the constraint value in the
well, distinct from G091's virial energy `E = T + W = -(lambda/4) M_b C`.

**Deep/Newtonian limits (control 2).** The log well is the *deep*-exterior
potential: for the Q/RAR/MONO branches `g -> sqrt(a0 B) = C/r` deep, so
`Phi -> C ln r` is the deep point-source potential. In the **Newtonian regime**
(`B >> a0`), `Phi -> -G_N M_b/r` and the r^-2 profile is maximally non-stationary:
EL residual spread vs `Phi_N = G M_b (1/R - 1/r)` over `[0.0062, 0.62] r_M` is
`310.1` (C5b; the ansatz is a deep-exterior object — domain boundary, stated).

---

## 4. Independent checks (seed step 4) — actual residuals, not booleans

1. **Symbolic (sympy):** `ln(A r^(-beta C)) + 1 + alpha + beta(3 sigma^2/2 + C ln r)`
   with `A = exp(-1-alpha-3 beta sigma^2/2)` simplifies to `0` identically (C1a).
2. **Direct substitution/differentiation (C1e):** `d/dr[ln rho + beta(...)] =
   (beta C - gamma)/r`; finite-difference derivative at `(2, C/2)` has max
   absolute value `1.1e-27` on the 4001-point grid (exact 0 analytically).
3. **EL residual spread (C1c, both footings, all 6 interior fixtures + analytic
   closed form `|beta C - gamma| ln(R/r_in)`):**

   | (gamma, sigma^2)   | spread at r_in/R = 0.01 | spread at 0.1 | spread at 0.5 |
   |--------------------|-------------------------|---------------|---------------|
   | (2, C/2)           | 1.4e-14                 | 1.4e-14       | 1.4e-14       |
   | (2, 0.9 C/2)       | 1.023 (pred 1.023)      | 0.512         | 0.154         |
   | (2.3, C/2)         | 1.382 (pred 1.382)      | 0.691         | 0.208         |

   Exact identity at the starred point to machine precision; every off-point
   nonzero (the control discriminates).
4. **50-digit mpmath spot check (C1d):** same spread at (2, C/2) on (0.1, 0.62),
   canonical, `dps = 50`: spread `< 1e-40` (measured `~1e-49`) — the zero is an
   exact identity, not float noise.

---

## 5. Negative control — self-gravity in E with the fixed-well variation kept (seed step 5)

**Setup.** `E_self = int rho (3 sigma^2/2 + C ln(r/r_ref)) dV + (1/2) int rho Phi_self dV`
(correct total energy including the phantom's own gravity; the 1/2 is the
self-interaction factor). Varying `S - alpha M - beta E_self` at fixed well and
sigma, holding `Phi_self` fixed while varying `rho` (the inconsistent "fixed-well
variation" the control targets), the EL equation acquires the term

```
-ln(rho/rho_ref) - 1 - alpha - beta(3 sigma^2/2 + C ln r + Phi_self(r)) = 0
                            ^^^^^^^^^^^^^^^^^^^  MISSING TERM in the fixed-well theory
```

**Closed form of the missing term (C4, Lean-certified).** For `rho = A/r'^2`
truncated at `[r_in, R]`, the shell theorem gives

```
Phi_self(r) = -G_N [ int_{r_in}^r 4 pi A dx / r  +  int_r^R 4 pi A/x dx ]
            = -4 pi G_N A [ (1 - r_in/r) + ln(R/r) ]
```

(inner integral `4 pi A (r - r_in)`, outer `4 pi A ln(R/r)` — the log of the
well-ratio). Verified by independent trapezoid quadrature (rel err 5e-9 to 2e-7,
honest finite-grid levels) and by 50-digit mpmath radial quadrature of the defining
kernel `1/max(r, r')` (rel err 3e-51 on the full (0.1, 0.62) canonical fixture).

**Exposure — the r^-2 profile is NOT a stationary point of the self-gravitating
energy.** With `beta = 1/sigma^2`, `sigma^2 = C/2`, `gamma = 2`, the
self-consistent EL residual has spread

```
spread[res_self] over [r_in, R]  =  |beta * 4 pi G_N A| * [ln(R/r_in) - (1 - r_in/R)]
```

measured (both footings, all 6 fixtures, matching the analytic values):

| r_in/R | R/r_M = 0.62 | R/r_M = 1.0 |
|--------|--------------|-------------|
| 0.01   | 11.78        | 7.30        |
| 0.1    | 5.03         | 3.12        |
| 0.5    | 1.25         | 0.77        |

O(1), never small. The missing term `beta Phi_self(r)` is *r-dependent* (its
end-point difference is `4 pi G_N beta A [ln(R/r_in) - (1 - r_in/R)]` — Lean
certified), so it cannot be absorbed into the multipliers. Quantitatively: the
inconsistent fixed-`Phi_self` variation doubles the effective exponent to
`gamma_eff(R) = beta C + beta * 4 pi G_N A (1 - r_in/R) in [4.00, 5.23]`
(measured `4.0000` at R/r_M = 1, `5.2258` at 0.62 — the phantom's well adds
`4 pi G A = C` at equipartition).

**The consistency that rescues the reading (C4b, G084 honest status (ii)).**
Only because the phantom's own source is the same log well — `Phi_self = C ln r +
const` exactly when `4 pi G_N A_eq = C` (equipartition) — do the two pinnings
agree: `sigma^2 = C/2` (virial + fluid closure, G091) equals `sigma^2 = 2 pi G A`
(hydrostatic self-consistency of the singular isothermal sphere) to `0.0` relative
(machine). So the fixed-well r^-2 is the max-entropy state of the *baryon*-well
problem; the phantom's self-gravity reproduces the well as a *posterior*
consistency check, and including it in the varied energy would double-count the
logarithmic well (the framework contract's flagged hazard). The seed's control
exposes precisely that double counting: the fixed-well variation against a
self-gravitating `E` misses the `beta Phi_self(r)` term.

**Deep exterior — full-kernel error bound (C5; do not transfer the interior
ansatz to filtered MONO without this check).** On shells `r_in/r_M in {10,100}`,
`R/r_in in {2,10}`: for `y = B/a0 = (r_M/r)^2 < y_star ~ 2.34`, MONO = RAR (the
splice is at `y_star`). The RAR deep expansion

```
nu_RAR(y) = y^(-1/2) [1 + sqrt(y)/2 + y/12 + ...]
=> g_RAR(r) = (C/r) [1 + (r_M/r)/2 + (r_M/r)^2/12 + ...]
```

gives the kernel error

```
|g_RAR - C/r|/(C/r) = (r_M/r)/2 + (r_M/r)^2/12 + O((r_M/r)^3)
```

measured 5.083% at `10 r_M`, 0.501% at `100 r_M` (both footings; leading-term
bounds 5.65% / 0.51%). The r^-2 max-entropy profile is the exact stationary point
of the *leading* log well; against the full RAR potential its EL residual is
`-r_M/r + O((r_M/r)^2)` (analytic; measured spread over the shells `0.0506` and
`0.0090` vs `r_M (1/r_in - 1/R) = 0.0500` / `0.0090`). The heat filter
`S = exp[(xi^2/2) Delta]` adds a smoothing error that needs the filter scale
`xi`, which **is not specified in this task's parameter cell** — explicit open
dependency (Section 6).

---

## 6. Strongest surviving statement, domain, and next implication

**Strongest surviving statement (conditional theorem).** Under the assumptions of
Section 1 (in particular: fixed well = baryon log well, fixed sigma, thermal
identification `beta = 1/sigma^2` as input, G091's `sigma^2 = C/2` as input), the
unique maximum-entropy profile of the fixed-well problem on `0 < r_in <= r <= R`
is exactly `rho = A/r^2` with `A = M_b/(4 pi (R - r_in))`, both footings, all
fixtures; the residual of the EL equation at `(gamma, sigma^2) = (2, C/2)` is
zero to machine (50-digit: `1e-49`) precision and nonzero at every other
`(gamma, sigma^2)`; the negative control (self-gravity in E, fixed-well variation
kept) fails exactly as the seed demands: the missing term `beta Phi_self(r)` is
O(1) with spread up to 11.78 and the double-counted exponent jumps to 4.0–5.2.
Domain: interior fixtures `R/r_M in {0.62, 1}` test the historical imposed-log-well
ansatz; deep exterior `r >= 10 r_M` carries the quantified kernel error
`(r_M/r)/2 + O((r_M/r)^2)`; Newtonian regime excluded (residual 310).

**1st first-principles framing.** The variation derives the *profile shape only*
conditional on the multipliers; the temperature-like number `sigma^2`, the
thermal identification `beta = 1/sigma^2`, the well `C ln r`, and `kappa = 1/2`
all remain inputs (G091's virial treats `sigma^2 = C/2`; neither is derived from
the action of the field theory). Max-entropy extremum, virial balance, source
normalization, and dynamical attainment are four distinct obligations; this result
covers the first (stationarity + uniqueness) and the third (normalization) in the
fixed well, and exposes the double-counting hazard for the second if attempted by
variation.

**Next unresolved implication.** (1) *Attainment*: no mechanism in this result
drives the baryonic dust/phantom to `sigma^2 = C/2` (G035 kill, G081 marginal
mode) — the equilibrium surface is derived, not the approach to it. (2) *Filter
scale*: the transfer of the deep-shell bound to operative *filtered* MONO needs
`xi` from `S = exp[(xi^2/2) Delta]`, which the task's parameter cell does not
specify — the kernel (branch) part of the error is bounded here; the filter part
is an open dependency, not a pass. (3) Nearby gate: the framework's own
equilibrium-sector obligation "double counting of the logarithmic well needs its
own derivation" is now quantified (C4), but the *self-consistent* self-gravitating
problem's entropy-maximum status (LBW gravothermal catastrophe) remains cited,
not re-derived.

---

## 7. Controls that failed and what changed

All controls are live (no literal-True passes):
- C1c off-point residuals (2, 0.9 C/2) and (2.3, C/2) are nonzero and match
  `|beta C - gamma| ln(R/r_in)`; C1b shows the sigma-variation gives `beta = 0`
  (seed S) or `beta = -1/sigma^2` (G084 S), never `+1/sigma^2` — the extra
  condition is genuinely extra;
- C4 residual spreads (0.77–11.78) are hugely nonzero; the quadrature rel err was
  first implemented with a gradient-based cumulative rule (systematic bias,
  reported 4.65) — replaced by trapezoid segments + 50-digit mpmath radial
  quadrature (3e-51); both levels reported honestly;
- C5b Newtonian-limit residual (310) and C5 kernel error (5.08% / 0.50% at
  10/100 r~M) pin the domain boundaries;
- C1d: 50-digit spread test (passed at `1e-49`); C2: normalization to 1e-10;
  C3: second-variation modes match analytic to <5% (all negative).

**Attempted-then-fixed audit-code issues (preserved in the run log):** (a) EL
identity passes float inputs to mpmath -> spread stuck at 1e-16 (fixed: mpf
inputs, `1e-49`); (b) Newtonian residual swamped by the `-G M_b/r` gauge constant
in float64 (fixed: gauge-zero-at-R form); (c) gradient-based cumulative
quadrature bias (fixed as above).

---

## 8. Reproducibility

- `AS076_audit.py` — the full audit; run as `python3 AS076_audit.py` (1 thread,
  env `OMP/OPENBLAS/MKL/NUMEXPR=1`): 0.24 s wall, 85 MB RSS (enforced <=120 s /
  <=512 MB / 1 thread). All 23 checks PASS; residuals in `AS076_audit_results.json`
  and `audit_run.log`.
- `AS076_fixed_well_el.lean` — Lean 4 certificate (6 theorems; EL identity,
  exponent pinning, normalization, self-potential closed form, missing-term
  spread, nonzero instance). Verified: `cd fable_independent_2026/lean_2026 && lake
  env lean <abs>/AS076_fixed_well_el.lean` (exit 0, zero sorry); axioms of every
  theorem: `{propext, Classical.choice, Quot.sound}` (see `lean_axioms_out.txt`).
- `AS076_axioms_check.lean`, `lean_compile_out.txt`, `audit_run.log`,
  `AS076_audit_results.json` — raw outputs.

**Limitations.** (1) Conditional on the fixed baryon well, fixed sigma, G091's
`sigma^2 = C/2`, and the thermal identification — none derived here from a common
action; (2) no dynamics/attainment; (3) the filter scale `xi` for filtered MONO
is absent from the task's parameter cell; (4) `M_b = 7e10 M_sun` is a proxy
register value; (5) finite grid results are numerical consistency checks — the
exact identities are the sympy/Lean/analytic statements; (6) both footings give
the identical dimensionless structure; dimensional values quoted per footing.

**Child proposal (recorded, not dispatched — no runner available in this seed
execution):** AS076.C01 "self-consistent singular isothermal sphere: entropy
extremum vs LBW non-existence on the truncated domain" — target: the
entropy-functional curvature of the *self-gravitating* problem on `[r_in, R]`
(finite-domain gravothermal stabilization), discriminating observable: the sign
of the configurational heat capacity; depends on this run's C4c closed form;
parent `AS076_r001...Z`, task sha `614a07d8...`, no duplicate found in
`manifest.json`/results (checked AS071-AS074 neighbors; no AS076 sibling runs).