# AS500.C01 — Matter-only Ward separation at the CA5-GNC-R pin (gate 5's open atom)

**Run:** `AS500-C01-r1-20260929T000610Z-dsv4f-hermes`
**Task:** `deepseek_push/astra_spawn_ideas/branches/AS500/AS500.C01.md`
**task_sha256 (verified before execution, matches pinned):** `7d0a46c2825ced3133d1d8c44bef2c59c550464bfe70ae17b3274a30d18a2caf`
**Action pins (verified on disk):** `FINAL_ACTION.md` = `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`
(CA4-GNC / CA5-GNC-R); k04 four-form promotion = `15c0a7e13eb9b7a5fdb403c8826bd01912d68dc81614609fddb6cd6ed9d32399`.
**Worker:** deepseek/deepseek-v4-flash-0731 (provider openrouter) via Hermes Agent focused subagent; identity taken from the executing system context.
**Started:** 2026-09-29T00:06:10Z · **Finished:** 2026-09-29T00:12:00Z (approx.; wall of the final research run 2.5 s)
**Parent evidence:** AS500 run `AS500-r1-20260928T204459Z-dsv4f-hermes` (gate-lattice audit; flagged P5 matter-only as the first missing bridge);
AS138.C01 run `AS138.C01-20260928T1950Z-dsv4f-hermes` (total-Ward assembly LANDED: on-shell closure is the zero polynomial in r = Z/β² — the SUM identity; NOT re-run here, used as the total-Ward balance);
AS137 (matter Ward), AS147 (U(1) divergence J_total), AS133 (terminal heat BC), AS651 (vacuum stress), AS658 (q = const bulk three-form).

**Verdict:** **(a) LANDS — decoupling proven.** On the pinned action, compact closed leaf, all
fields on shell, terminal heat BC (AS133: L_b = −R_W, λ0 = L_0): each cross-source sector
current closes on shell by its OWN sector equations, so

```text
div Q_heat |_shell = 0 ,  div Q_U1 |_shell = 0 ,  div Q_vac |_shell = 0
  =>  div(Q_heat + Q_U1 + Q_vac) |_shell = 0  identically in the audited couplings
  =>  (total-Ward balance, AS138.C01)  div Q_b = -div(Q_heat+Q_U1+Q_vac) = 0  in N sqrt(h)
  and independently (P1, AS137 minimal coupling): div Q_b = E_b(xi.dpsi) = 0 for E_b = 0.
```

The ordinary-matter sector carries **no nonmetric force** on this pin; the gate-P5 matter
atom is **landed on the cell**. NEG-1 and NEG-2 both fire: the decoupling lemma is
load-bearing (without it the residual is nonzero: 15 resp. 20 at exact rational witnesses),
and no (b)-witness can be built on q ≠ const (three-form EOM residual ≠ 0).

---

## 1. Framework cell, premises, conventions

**Mandatory framework inputs (adopted, not derived here):** a0 = κc√(Gρ_Λ), **κ = 1/2 ADOPTED**
(as in all sibling runs; C7 of the parent shows κ is NOT forced — this child does not need it).
ρ_Λ = 4a0²/(Gc²); G_N = 6.67430e-11, c = 299792458, M_sun = 1.98847e30, pc = 3.085677581491367e16 (SI);
**G_N/G_bare/G_cosmo kept as separate symbols** (only G_N enters the footing prints).
Both footings carried separately: canonical a0 = 9.3619e-11 m/s² (ρ_Λ = 5.844412454e-27 kg/m³)
and alternative a0 = 1.1279e-10 m/s² (ρ_Λ = 8.483089620e-27 kg/m³); κ back-check = 0.5 on both.
They never share both fixed density and fixed κ (κ_eff = 0.602388 relabel is diagnostic only).

**Domain of the claim:** compact closed C² leaf (no spatial boundary), orthonormal-adapted
foliation, all fields on shell, terminal heat BC, N√h measure. All statements are
dimensionless identities ⇒ apply identically to both footings.

**The ten landed premises (used as premises; none re-derived here; hashes in result.json):**

| # | Premise (landed run) | Content used |
|---|---|---|
| 1 | AS137 (Tier-0) | ∇_μT_b^{μν} = E_b∇^νψ off shell, 0 on shell; S_b contains NO host fields (minimal coupling; check [5] classification) |
| 2 | AS138 (Tier-0) | δ_ξS_heat = N[Σ_k E_Wk(ξ∂W)_k + Σ_k E_Lk(ξ∂L)_k + (R_W+L_b)ξ∂W_b + (λ0−L_0)ξ∂W_0 + E_λ0ξ∂λ0 + E_Uξ∂U] (CHK-3 display; endpoint multipliers load-bearing) |
| 3 | AS147 (Tier-0) | div J_φ = +E_ex, div J_χ = −E_ex ⇒ div J_total = 0 on shell (exchange cancels) |
| 4 | AS651 (Tier-0) | ε_vac = (Z/2+bβ²)q² > 0, T_μν = −ε_vac g_μν ⇒ div T_vac = −(Z+2bβ²)q(g^{μν}∂_μq); flux EOM ⟹ ∂_μq = 0 (constancy) |
| 5 | AS658 | three-form bulk EOM: EOM = 0 ⟺ ∂_μP_q = 0 ⟹ q = const in the bulk (P_qq = Z+2bβ² > 0); residual with q nonconst = −(Z+2bβ²)∂q ≢ 0 |
| 6 | AS133 (Tier-0) | terminal heat BC: L_b = −R_W, λ0 = L_0 (endpoint closing) |
| 7 | AS138.C01 | total-Ward assembly: Q_total = Q_b + Q_heat + Q_U1 + Q_vac closes on shell with no (Z,b,β)-hypothesis (zero polynomial in r); the lapse-source gate/compensator pair is eq-(13)'s source, NOT a Ward divergence |

## 2. Step 1 — on-shell sector identities in the N√h measure

On the pinned class, all fields on shell, terminal heat BC (AS133: L_b = −R_W, λ0 = L_0):

```text
heat   : E_Wk = E_Lk = E_lam0 = E_U = 0 (all k)          (heat EOMs, N sqrt(h) measure)
U(1)   : div J_phi = +E_ex , div J_chi = -E_ex           (phi,chi EOMs; AS147)
vacuum : d_mu q = 0                                       (three-form flux constancy; AS651/658)
matter : E_b = 0 ; S_b[g] contains no host fields         (minimal coupling; AS137)
```

These are the exact on-shell identities the child's step 1 must supply. Each is taken from
the landed premise runs (AS138 CHK-3 display, AS147 exchange pair, AS651 step 3 / AS658 D4b,
AS137 checks [2]-[3], [5]); none is re-derived here.

## 3. Step 2 — symbolic computation of div Q_heat, div Q_U1, div Q_vac and their sum on shell

Assembled cross-source charges (premises P2–P4):

```text
Q_heat = N[ sum_k E_Wk (xi.dW)_k + sum_k E_Lk (xi.dL)_k + (R_W+L_b)(xi.dW)_b
            + (lam0-L_0)(xi.dW)_0 + E_lam0 (xi.dlam0) + E_U (xi.dU) ]
Q_U1   = div J_phi + div J_chi            (raw; on shell -> E_ex + (-E_ex))
Q_vac  = -(Z + 2 b beta^2) * q * (g^{mu nu} d_mu q)
Q_b    = E_b (xi.dpsi)
```

On-shell substitution set S (the sector-decoupling lemma):

```text
E_Wk = E_Lk = E_lam0 = E_U = 0 ; dq = 0 ; dJphi = +E_ex , dJchi = -E_ex ;
L_b = -R_W ; lam0 = L_0 ; E_b = 0
```

Sympy reduction (exact, `raw_output.txt`):

- **div Q_heat |_shell = 0** — the endpoint display closes by the AS133 BC: (R_W + L_b) = 0,
  (λ0 − L_0) = 0; all interior Euler terms vanish. ✓
- **div Q_U1 |_shell = 0** — E_ex + (−E_ex) = 0 (the phi,chi EOM pair cancels the exchange). ✓
- **div Q_vac |_shell = 0** — dq = 0 kills the metric-proportional stress divergence. ✓
- **div Q_b |_shell = 0** — E_b = 0 (minimal coupling; the matter sector alone is closed). ✓
- **SUM div(Q_heat + Q_U1 + Q_vac) |_shell = 0 exactly;** as a polynomial in r = Z/β² it is
  `Poly(0, r)` and as a multivariate polynomial in (Z, b, β, q) it is `Poly(0, Z, b, beta, q)`
  — **the zero polynomial: zero monomial in the couplings.** Closure consistency with
  AS138.C01's K2 (zero polynomial in r) is re-confirmed on the cross-source sum.
- 100 random exact-rational jets (seed 20260928): on-shell sums ≡ 0 in 100/100; off-shell
  residuals ≠ 0 in 100/100.

**Conclusion of step 2 — (a) LANDS.** The decoupling statement holds identically over the
audited band α ∈ (0,2), K_B ∈ [0,1/4], r = Z/β² ∈ (0,∞), ℓ = 0.04, δ = 0.05 (the identity
contains none of them: it closes for every coupling cell, κ included — both footings).

**Numeric residuals at 5 sampled coupling points** (exact on-shell sum 0.0 at every point;
NEG-1/NEG-2 residuals nonzero and growing with r — see residuals.json):

| point | α | K_B | r = Z/β² | on-shell sum | NEG-1 |res| | NEG-2 |res| |
|---|---|---|---|---|---|---|
| P1 | 1/2 | 0 | 1.0 | 0.0 | 1.9788 | 0.310803 |
| P2 | 1 | 1/8 | 4.0 | 0.0 | 21.9638 | 1.21013 |
| P3 | 3/2 | 1/4 | 7.963989212911… | 0.0 | 48.3754 | 2.39865 |
| P4 | 7/10 | 0 | 16.0 | 0.0 | 101.979 | 4.8108 |
| P5 | 19/10 | 1/4 | 64.0 | 0.0 | 421.949 | 19.2095 |

## 4. Negative controls (each capable of failing; all fired)

**NEG-1 (fires).** The total-Ward identity alone (∇·Q_total = 0, AS138.C01) determines
∇·Q_b = −∇·(Q_heat+Q_U1+Q_vac) but does NOT make the RHS zero. Only after substituting the
sector-decoupling lemma S does the matter-only atom follow. Without the lemma (generic
off-shell jets: retained E_Wk, E_Lk, E_λ0, E_U, dq, L_b+R_W, λ0−L_0), the residual
−(div Q_heat + div Q_U1 + div Q_vac) is nonzero:

- witness (a): heat EOM dropped (E_W0 = 3/2, N = 10, dW0 = 1) → **residual = 15 ≠ 0** (exact);
- witness (b): terminal BC dropped (L_b = −R_W + 1, λ0 = L_0 − 1, N = 10, Wbp = W0p = 1) →
  **residual = 20 ≠ 0** (exact).

If the residual were zero, (a) would have been hiding in the equations; it is not — the
separation is genuinely carried by the four sector identities (heat EOMs + AS133 BC; U(1)
exchange pair; flux constancy; matter EOM), and each is individually load-bearing.

**NEG-2 (fires).** The three-form bulk EOM (AS658 D4b/D4d) is EOM = 0 ⟺ ∂_μP_q = 0 with
P_qq = Z + 2bβ² > 0, hence **q = const in the bulk**; a q non-const state has EOM residual
−(Z+2bβ²)·q1 ≢ 0. Numeric witness at the tuned ratio: q = q0(1+0.3 sin x0) gives EOM
residual **−2.40000000000 ≠ 0**. Therefore any (b)-witness declaring div Q_vac ≠ 0 through
∂q ≠ 0 is OFF shell, violates a retained hypothesis, and cannot establish (b). (b) is
excluded on the vacuum side; combined with NEG-1, the verdict (a) stands.

## 5. The exact on-shell statement (scoped claim)

On the CA5-GNC-R pinned action (FINAL_ACTION b8c04d4e…7546e; k04 15c0a7e1…2399), compact
closed C² leaf, all fields on shell, terminal heat BC L_b = −R_W, λ0 = L_0 (AS133), in the
N√h measure:

```text
div Q_heat = 0   (heat EOMs + AS133 terminal BC)
div Q_U1   = 0   (phi,chi EOM exchange pair, AS147)
div Q_vac  = 0   (three-form flux constancy d_mu q = 0, AS651/AS658)
div(Q_heat + Q_U1 + Q_vac) = 0          -- identically in the audited couplings
div Q_b    = 0                          -- matter-only Ward separation (gate-5 atom)
```

Domain: any configuration of the pinned class; couplings α ∈ (0,2), K_B ∈ [0,1/4],
r = Z/β² ∈ (0,∞), ℓ = 0.04, δ = 0.05 free (the identity is a zero polynomial in all of
them); κ-free (κ = 1/2 ADOPTED input, unneeded by the separation); both footings.

## 6. What it means for gate P5

The parent AS500 audit listed P5's atom "matter-only Ward separation" as the first missing
mathematical bridge, with the total-Ward identity (AS138.C01) as computational prerequisite
only. This child closes that bridge on the pinned cell: the sector currents decouple on
shell, so **ordinary matter sees the physical metric only** — the minimally coupled baryon
equation of motion carries no nonmetric force; requirement-5's ordinary-matter conservation
atom is proved for the cell. Mechanism change is NOT needed on this pin. (Gate P5 as a whole
is not promoted to "closed" by a single cell: the audit's other P5 constituents — e.g. the
full coupled conservation statement on the kid leaf ensemble — remain outside this run's
scope; see limitations.)

## 7. Lean 4 certificate (hard bar met)

`AS500C01_matter_ward_decoupling.lean` (+ `AS500C01_axioms_probe.lean`), compiled on the
compile host `cd fable_independent_2026/lean_2026 && lake env lean <abs>.lean` — **exit 0,
zero sorry** (9 theorems). Unfiltered `#print axioms` for all nine:
**exactly {propext, Classical.choice, Quot.sound}** (`lean_axioms.out`). Theorems:
`matter_closes_on_shell`, `heat_closes_on_shell`, `u1_exchange_zero`,
`vacuum_div_zero_on_shell`, `cross_source_closes` (the decoupling identity on shell, no
hypothesis on Z, b, β, q), `matter_decoupling` (the matter-only atom), `neg1_heat_eom_omitted`
(15 ≠ 0), `neg1_terminal_bc_omitted` (20 ≠ 0), `eom_rejects_nonconst_q` (NEG-2).
House traps handled: `rw` followed by `ring` (tactic left no goals after rw alone);
adjacent doc comments avoided (each declaration has exactly one attached doc comment);
the (1:ℝ)/2 annotation not needed here (no halves in statements); `mul_ne_zero` +
`neg_eq_zero` route for the NEG-2 product (no `Real.mul_self_sqrt` needed). Compiled from
the run directory; nothing written into `fable_independent_2026/lean_2026`.

## 8. Bounds actually enforced

- CPU: `ulimit -t 120` (shell-enforced) on the research script; `ulimit -t 300` on Lean.
- Wall (measured): research script 2.50 s; Lean compile 2.41 s (main) / 2.05 s (axioms).
- Memory (measured `/usr/bin/time -l`): max RSS 68,583,424 bytes ≈ 65.4 MiB ≪ 512 MB
  (macOS has no RLIMIT_AS — measured peak is the guarantee, house convention).
- Threads: 1 (`OPENBLAS/OMP/MKL/VECLIB/NUMEXPR_NUM_THREADS=1`); no multiprocessing.
- Precision: exact sympy symbolic reductions; exact rational witnesses; Float at 20+ digits
  for the 5 sampled points; mpmath not needed (pure polynomial algebra).

## 9. Commands (as executed)

```text
shasum -a 256 branches/AS500/AS500.C01.md   -> 7d0a46c2825ced3133d1d8c44bef2c59...2caf (pinned)
cd results/AS500.C01/AS500-C01-r1-20260929T000610Z-dsv4f-hermes
bash -c 'ulimit -t 120; OPENBLAS_NUM_THREADS=1 ... python3 as500c01_matter_ward.py > raw_output.txt 2> time_mem.txt'  (EXIT=0, 2.50 s)
cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS500C01_matter_ward_decoupling.lean  (EXIT=0)
cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS500C01_axioms_probe.lean            (EXIT=0)
```

## 10. What this does NOT establish / next step

- Gate P5 as a whole is not closed: this run lands the ordinary-matter conservation atom on
  the single pinned cell (compact closed leaf, on shell). Leaf-ensemble/multiple-leaf,
  coupled-evolution, and any statement about P2/P3/P4/P6–P13 atoms are outside scope.
- No claim that ∇·Q_b = 0 holds off shell, or on the gate/compensator lapse-source channel
  (that channel is the pinned eq-(13) source, not a Ward divergence).
- The results rest on the ten landed premise runs (all unreviewed); the premises are listed
  in result.json input_sha256 and are not re-proven here.
- κ = 1/2 remains adopted; the AS651/AS138.C01 κ-continuum conclusion is untouched.
- Next unresolved implication (upstream): whether the same decoupling holds under the
  coupled evolution/leaf-ensemble (P5's full atom), and the P1 weak-field filtered system
  on a compact source (P1 full atom; parent Q11).

**Verdict (per work order):** (a) — matter-only Ward separation PROVED on the pinned cell;
decoupling ∇·(Q_heat+Q_U1+Q_vac) = 0 on shell is an identity in the audited couplings;
NEG-1 and NEG-2 both fire; Lean certificate 9/9, axioms {propext, Classical.choice, Quot.sound}.