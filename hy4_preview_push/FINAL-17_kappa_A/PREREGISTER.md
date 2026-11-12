# FINAL-17 (KAPPA_A) PREREGISTER -- 2026-11-11

**Written alone, before any FINAL17 script exists and before any FINAL17 number is computed.**
Nothing below has been run. The predicted outcome is written down first, on purpose: this lane is
expected to return a NEGATIVE on the coefficient, and the negative is stated here so that it cannot
be softened later.

**Lane.** FINAL MILE, lane **FINAL-17 (KAPPA_A)**. TEST lane, quarantined: adopts nothing,
relabels nothing, registers nothing, edits nothing outside this folder. Footings NEVER pooled
(canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2). Cold dark energy is a gravitating field
component; no particle is added. **kappa = 1/2 FITTED; not theory closed.**

## 0. The question, in one line

> Does the **self-source / capacity** route derive `kappa` in `a_0 = kappa * c * sqrt(G * rho_Lambda)`?

Split again, because the halves have different answers (same discipline as FINAL-16):

- **Q1 (capacity).** Does the route derive the *capacity* -- the ceiling the cold component's own
  self-gravity saturates at -- and show that the self-sourced configuration sits at it?
- **Q2 (coefficient).** Does that capacity condition output the number 1/2, i.e. pin `a_0` against
  the cosmic unit `s := c sqrt(G rho_Lambda)`?

## 1. The record I am auditing (read, not assumed)

Two in-repo records are named by the brief. Both were located and read:

**(a) GF1 / GF2 -- `deepseek_push/GF1_germ_flip/`, `deepseek_push/GF2_closure_half/`, 2026-10-08.**
- **GF1 (the germ-flip).** Reduces every spelling of the tie (`A*Lambda = 32 pi^2`, `Z^2 = 32 pi/3`,
  `G rho_L = 4 a0^2/c^2`, `a0 = c^2/(Z R_dS)`, `kappa = 1/2`) to ONE integer `n`, via the
  n-general tie `a0 = c sqrt(G rho_L)/n`, `Z := c H_L/a0 = n sqrt(8 pi/3)`, and
  `kappa := a0/s` with `s := n a0`. Its own verdicts (V1-V4, pre-registered) are
  **V1 REDUCED**, **V2 UNDERDETERMINED-BY-ONE-INTEGER**, **V3 DATA-CONSISTENT**, **V4 OPEN**, with
  the explicit honesty note H1/H2: *"R1/R2 are identity-class (true by construction, reported as
  reduction, never as derivation)."**
- **GF2 (the closure half).** Derives, in three exact lines from the committed static branch
  `Phi = C ln r` (P1) + Poisson (P2) + stationarity/barotropy (P3):
  `rho = C/(4 pi G) r^-2` (gamma = 2 FORCED), then `sigma^2 = C/2`, hence
  **`kappa := sigma^2 / v_flat^2 = (C/2)/C = 1/2` EXACTLY**, with a ledger counting entries
  carrying the number 1/2: **0**. Plus the uniqueness lemma L2 (gamma = 2 is the unique
  self-sourced hydrostatic equilibrium) and the border list, whose item (iii) reads:
  *"the vacuum coupling (why a_0's VALUE is the vacuum's scale: a0 <-> rho_Lambda normalization):
  OUT of scope here; committed temperature-ladder machinery (G132/G151/G163), cited, not re-run."*
- **So, exactly**: GF2 derives `sigma^2/v_flat^2 = 1/2` -- a **ratio internal to the halo**,
  independent of `M_b` and with **no `rho_Lambda` anywhere in the chain**. It does not derive
  `a_0/(c sqrt(G rho_Lambda)) = 1/2`. GF1's `kappa = 1/n` with `s := n a_0` constrains the **index**
  of the response; the identification `s = c sqrt(G rho_Lambda)` is the tie itself. This reproduces
  FINAL-16's item **J3** verdict (`FAIL = RESTATEMENT`) from a second channel -- and FINAL-16's
  KA-2 control (`sigma^2/v_f^2 = 1/2` for *every* kappa, including 1/3) already shows the 1/2
  does not move with kappa.
- **Note on the brief's date**: the brief says "GF1+GF2, 2026-11-08"; the lane records in the repo
  are dated **2026-10-08**. Both spellings are indexed; "2026-11-08" also carries
  `closure_2026_11_08/VR1_vacuum_response_identity/` (which grades GF2 as KA-2 RESTATEMENT).
  Recorded as a **date discrepancy, not adjudicated.**

**(b) Sigma107v214 / AG4 branch a -- `argon_push/AG4_law_from_action/`, 2026-10-15.**
- **No file or lane named `Sigma107v214` exists in the repo** (searched: filenames and content,
  case-insensitive, for `Sigma107`, `SIGMA107`, `Sigma 107`, `v214`). The identifier resolves to
  **AG4's capacity pair**: `n = 1` (canonical) ⇒ `g_ph < a_0` with
  **`Sigma_bar_max = a_0/(pi G) ~ 214 M_sun/pc^2`** (PAPER49's anchor); `n = 2` (quadratic) ⇒
  `g_ph < a_0/2`, **"~ 107 in the same convention"**. "Sigma107v214" = that pair.
- AG4's landed verdict: **BRANCH (a) CONFIRMED** -- the unique static rest state of the frozen S2
  action IS the canonical law `gbar = g^2/(g+a_0)`; **the quadratic a_0-line is the half-capacity
  (n = 2) variant -- a different theory.** Certified in `AG4_law_from_action.lean` (12 theorems,
  including `T7_n2_quadratic` and `T7_n2_not_canonical`), exit 0, axioms ⊆ {propext,
  Classical.choice, Quot.sound}.
- **So, exactly**: AG4 certifies that the quadratic is NOT the canonical rest state. It does not
  touch `kappa` against `rho_Lambda` at all. A chain that uses the n = 2 branch and then reports
  `kappa = 1/2` from `kappa = 1/n` is **mixing branches**: `kappa = 1/n` is the ratio `a_0/s`
  for the branch indexed by `n`, and branch `n = 2` is a different theory from the one whose
  coefficient is being fitted.

## 2. Conventions (SI; source lanes stated)

- G = 6.6743e-11 m^3 kg^-1 s^-2 (footing convention of the brief); c = 2.99792458e8 m/s (exact).
- **Cosmology, primary**: Planck 2018 TT,TE,EE+lowE+lensing, taken from the sibling lane
  **FINAL-16's PREREGISTER §2** (in-repo, `closure_2026_11_11/FINAL16_kappa_real/`), which is the
  record's most recent explicit freeze of these inputs:
  `H0 = 67.36 km/s/Mpc`, `Om = 0.3153`, `OL = 0.6847`, `Ob = 0.0493`, `Oc = 0.26445`.
  `rho_crit,0 = 3 H0^2/(8 pi G)`; `rho_Lambda = OL * rho_crit,0`.
  Machine-printed in `final16.out`: `rho_crit,0 = 8.522730e-27`, `rho_Lambda = 5.835513e-27`,
  `H_Lambda = 1.806349e-18 1/s`, `c H_Lambda = 5.415298e-10`, `c sqrt(G rho_L) = 1.870954e-10`.
- **Cosmology, cross-check (source-lane systematic)**: the **GF1/F05/G058 register**
  (`deepseek_push/GF1_germ_flip/GF1_germ_flip.py` header; `deepseek_push/F05_results.json`):
  `rho_c = 8.533238720309458e-27 kg/m^3`, `Omega_L = 0.685`, `Z = 5.788810036466141`,
  `a0 = 9.3619e-11`. Difference from primary ≈ 0.12 % in `rho_crit`; reported as a systematic,
  never pooled.
- **Input errors used in propagation** (each flagged if from memory):
  - `H0 = 67.36 +- 0.54` km/s/Mpc (Planck 2018) -- **from the record** (FINAL16 PREREGISTER prints
    the central value; the +-0.54 is Planck 2018 TTTEEE+lowE+lensing, **MEMORY -- flagged**).
  - `Omega_L = 0.6847 +- 0.0073` -- central value from the record; the error is
    **MEMORY -- flagged**. (GF1's own error class is `D_OM_OVER_OM = 1 %`, i.e. 0.0068 -- consistent.)
  - `G`: enters `rho_Lambda` and `sqrt(G rho_Lambda)` with **opposite** powers and cancels
    **exactly** in `kappa = a0 sqrt(8 pi/(3 Omega_L))/(c H0)`. Verified symbolically; G's
    uncertainty is therefore **irrelevant** to kappa at this order. (Flagged: this cancellation is a
    calculation, not a claim from memory.)
  - `a0`: the footings are **definitions**, so `sigma(a0) = 0` by construction; the register spread
    (9.3603e-11 canonical vs 9.3619e-11 in GF1's register) is carried as a separate systematic.
- Cold-component vocabulary (Form B): `r_M := sqrt(G M_b/a0)`, `x := r/r_M`,
  `M_c(<r) = M_b X(x)`, `X = (sqrt(1+4x^2)-1)/2`; phantom field
  `g_c = g - g_N = a0 g/(g+a0)`; `v_inf^4 = G M_b a0`.
  Deep (inner, `x << 1`): `rho_c -> a0/(2 pi G r)` ⇒ universal column `Sigma_c = a0/(2 pi G)`.
  Weak (outer, `x >> 1`): `rho_c -> sqrt(G M_b a0)/(4 pi G r^2)`.

## 3. The arms (criteria frozen NOW)

### A1 -- the capacity identity (graded; predicted class = IDENTITY)
Verify exactly (sympy, residual 0) that for the canonical law `g_N = g^2/(g+a0)`:
  (i)   `u := g - g_N = a0 * g/(g + a0)`;
  (ii)  `u/a0 = nu/(1+nu)` with `nu := g/a0`  -- the response SHAPE carries no `a0`;
  (iii) `0 < u < a0` for all `g>0`, `a0>0`  -- the capacity IS `a0`;
  (iv)  the deficiency `a0 - u = a0^2/(g+a0) > 0` and `-> 0` only as `g -> infinity`;
  (v)   covariance `u(lam*a0, lam*g) = lam * u(a0, g)`;
  (vi)  invariance of the shape `(u/a0)(lam*a0, lam*g) = (u/a0)(a0,g)`.
**Verdict rule (fixed now):** A1 = **IDENTITY** if (i)-(vi) are exact -- the capacity is a
*restatement* of the scale that appears in the law, not a determination of it.
*Predicted:* IDENTITY.

### A2 -- the branch-distinctness audit (graded; predicted CONFIRMED)
Re-verify (sympy) AG4's G3 capacity family: for `K W_rem'(u) = u^2/(a0 - n u)` the rest state is
`u^2 + n*gbar*u = a0*gbar`, so
  - `n = 1` ⇒ `g^2 = gbar(g + a0)`  (canonical);
  - `n = 2` ⇒ `g^2 - gbar^2 = a0*gbar`  (quadratic) EXACTLY;
  - capacity `u -> a0/n`, i.e. `a0` (n=1) vs `a0/2` (n=2);
  - in AG4's column convention `Sigma_bar_max = g_ph,max/(pi G)`: 214 (n=1) vs 107 (n=2).
Also compute the record's deep universal column `Sigma_c = a0/(2 pi G)` in the same units and record
whether it coincides with either ceiling.
**Verdict rule (fixed now):** A2 = **CONFIRMED** iff `n=1` ⇏ `n=2` rest states (residual ≠ 0) and
both ceilings print. *Predicted:* CONFIRMED, **and** `Sigma_c = a0/(2 pi G) ~ 107` coincides
*numerically* with the **n = 2** capacity ceiling, not the canonical one -- which is exactly the
ambiguity AG4's "certified distinct" warning is about. Pre-registered as a **trap to be flagged, not
used.**

### A3 -- the derivation attempt: capacity = a cosmic scale (graded; the lane's point)
The capacity condition outputs `a_0`. `kappa` needs `a_0` pinned against `s := c sqrt(G rho_Lambda)`.
The only way the route can do that is an added premise of the form
`capacity := (dimensionless) x (a cosmic acceleration built from c, G, rho_Lambda alone)`.
**Frozen menu of six such premises (no item added or dropped after the run):**

| id | capacity premise | kappa it forces |
|----|------------------|-----------------|
| C1 | `c^2/R_Lambda = c H_Lambda` (horizon-rate scale) | `sqrt(8 pi/3)` = 2.89440 |
| C2 | `4 pi G rho_L R_Lambda/3 = c H_Lambda/2` (uniform-sphere self-gravity at the horizon) | `sqrt(2 pi/3)` = 1.44720 |
| C3 | `c H_Lambda/(2 pi)` (Milgrom form) | `sqrt(2/(3 pi))` = 0.46066 |
| C4 | `pi G rho_L R_Lambda` (cosmic column gravity) | `sqrt(3 pi/8)` = 1.08543 |
| C5 | `pi G rho_L R_Lambda/2` (half cosmic column) | `sqrt(3 pi/32)` = 0.54271 |
| C6 | `c^2/(2 pi R_Lambda) = c H_Lambda/(2 pi)` -- the *circumference* reading of C3 | `sqrt(2/(3 pi))` = 0.46066 |

**Verdict rules (fixed now):**
- an arm **PASSES** iff `|kappa_arm - 1/2| <= 0.025` **AND** its premise is *derived from the route*,
  not chosen from this menu;
- **menu-freedom test (decisive):** report the **dex span** of the frozen menu and compare with the
  observational half-allowance **0.0411 dex** (half the footing separation
  `log10(1.1312e-10/9.3603e-11) = 0.0822 dex`). **If the menu span exceeds 0.0411 dex, the route
  class cannot fix kappa at the precision a footing selection would need.**
*Predicted:* no arm inside the 5 % band; nearest C3/C6 at 0.4607 (0.0356 dex from 1/2); span
≈ 0.923 dex ⇒ **≈ 22x too much freedom**.

### A4 -- the structural no-go (graded; predicted CONFIRMED)
Exhibit the one-parameter group `G_lam`: `a_0 -> lam a_0`, `g -> lam g`, `g_N -> lam g_N`,
`u -> lam u`, with `c, G, rho_Lambda, M_b` fixed, and verify **symbolically** that the
*whole* self-source/capacity structure is covariant:
  (i)   the law `g_N = g^2/(g+a0)`;
  (ii)  `u = g - g_N` (= A5 above);
  (iii) the capacity bound `u < a0`;
  (iv)  Poisson in the self-sourced branch: `rho_c = C/(4 pi G r^2)`, `C := sqrt(G M_b a0)` -- both
        sides carry `lam^{1/2}` (r fixed);
  (v)   the hydrostatic closure `sigma^2 = C/2` and the ratio `sigma^2/v_flat^2 = 1/2` -- weight 0;
  (vi)  the deep universal column `Sigma_c = a0/(2 pi G)` -- weight 1;
  (vii) the deficiency `a0 - u = a0^2/(g+a0)` -- weight 1.
Then: `kappa = a0/(c sqrt(G rho_Lambda))` is the **only** `G_lam`-charged quantity
(`kappa -> lam * kappa`), and there is **no** `G_lam`-invariant in the route's data
(`{c, G, rho_Lambda, M_b, X, sigma^2/v_f^2, ...}`) that could fix the orbit coordinate; the
capacity statement `u_max = a0` is likewise weight-1, i.e. one equation `a0 = a0`.
**Verdict rule (fixed now):** A4 = **NO-GO CONFIRMED** iff (i)-(vii) hold exactly **and** no
`G_lam`-invariant is available. *Predicted:* CONFIRMED.

### A5 -- the footing ledger, computed not assumed (reported + graded on the band)
Compute, with propagated errors, **`kappa(a0 vs rho_Lambda)`** for each footing, never pooled:
`kappa = a0 * sqrt(8 pi/(3 Omega_L)) / (c H0)`:
- canonical `a0 = 9.3603e-11` ⇒ predicted `kappa = 0.5003 +- 0.0048`;
- alt `a0 = 1.1312e-10` ⇒ predicted `kappa = 0.6046 +- 0.0058`.
Plus the external RAR value `a0 = 1.20e-10 +- 0.02 (rand) +- 0.24 (sys)` (Lelli/McGaugh/Schombert
2017, **PROVISIONAL / MEMORY -- flagged**) ⇒ `kappa = 0.6414 +- 0.0107 +- 0.1283` (FINAL-16 print).
**Footing-selection rule (fixed now):** the route **selects a footing** only if some A3 arm both
(i) lands inside `|kappa - 1/2| <= 0.025` and (ii) has its premise *derived from the route*. Since
no arm is expected to clear (i)&(ii), the pre-registered answer is **SELECTS NEITHER**. Any
near-miss distance is reported as information, never promoted to a selection.

## 4. Known-answer controls (all must PASS, else the apparatus is broken and the lane stops)

- **KA-1.** `Z := c H_L/a0 = 5.788810` on the canonical footing (FINAL-16 print; `sqrt(32 pi/3)`).
  Equivalently `kappa = sqrt(8 pi/3)/Z`.
- **KA-2.** `kappa(a0_can vs rho_Lambda) = 0.500296` and `kappa(a0_alt vs rho_crit,0) = 0.500295`
  (FINAL-16 print) -- both footings realize `kappa = 1/2` against their OWN reference density,
  which is why the tie alone cannot select between them.
- **KA-3.** AG4 `T7_n2_not_canonical`: canonical `g_ph` substituted into the `n = 2` rest-state
  equation leaves residual `gbar * g_ph != 0`, and the `n = 1` frozen EOM takes residual exactly 0.
- **KA-4.** The deep universal column `Sigma_c = a0/(2 pi G)` prints at ≈ 107 M_sun/pc^2 on the
  canonical footing (PAPER49's `Sigma_bar_max = a0/(pi G)` ≈ 214 is the other member of the pair).

## 5. MUTATE -- three false twins, each of which MUST be rejected by the same machinery

- **M1.** *"the Milgrom-form capacity `a_0 = c H_Lambda/(2 pi)` derives `kappa = 1/2`."*
  Machinery must reject on the band: `|0.4607 - 0.5| = 0.0393 > 0.025`, **and** on the
  premise test (it is menu item C3, a choice).
- **M2.** *"the deep universal column `Sigma_c = a_0/(2 pi G) ~ 107` confirms `kappa = 1/2`,
  because 107 is the half-capacity ceiling."*
  Machinery must reject: 107 is the **n = 2 (quadratic)** capacity ceiling in AG4's convention; the
  canonical branch's ceiling is 214. Confirming 107 therefore supports **the other branch**, not the
  canonical coefficient -- and it carries no cosmology.
- **M3.** *"`kappa = 1/2` is a measurement, and it is realized on the alt footing too."*
  Machinery must reject: `kappa(a0_alt vs rho_Lambda) = 0.6046`, i.e. **0.0822 dex** from
  canonical's `0.5003` (3.3x the 5 % band in dex terms); `kappa = 1/2` on the alt footing is
  realized only by *swapping the reference density* to `rho_crit,0`, which is a definition.

**MUTATE arm behaviour:** under `FINAL17_MUTATE=1` the three twins are *asserted as true*; the
machinery must still reject all three. The mutate arm's own pass condition is that the injected
mutation (band widened to 20 % and the premise test switched off) makes at least one twin pass,
which is then reported as `MUTATE VERDICT: PASS (the machinery can be fooled only by disabling it)`.

## 6. Labels

- **KAPPA DERIVED (CAPACITY).** Some arm of the route, with no free dimensionless input, outputs
  `kappa` with `|kappa_out - 1/2| <= 0.025` on both footings.
- **KAPPA NOT DERIVED (FITTED) -- CAPACITY DERIVED.** Q1 = YES (the route derives the capacity and
  shows the self-sourced configuration sits at it); Q2 = NO. *This is the pre-registered expectation.*
- **KAPPA NOT DERIVED (FITTED) -- NEITHER HALF.** Neither.
- **OPEN** if any known answer fails or a numerical step fails.

## 7. Scope

Dimensional analysis, the canonical law's own algebra, Poisson + hydrostatic closure on the committed
static branch, AG4's already-certified capacity family (cited, re-verified not re-derived), a flat
LambdaCDM background, and sympy for every exact step. No new data, no download, no CLASS run, no refit
of `a_0`, no new sector, no verdict on NPJ1's sectors, no re-adjudication of AG4's branches.
Literature attributions PROVISIONAL.
