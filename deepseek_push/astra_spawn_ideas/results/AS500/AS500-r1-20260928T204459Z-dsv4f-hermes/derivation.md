# AS500 — Logical independence and redundancy of the thirteen closure gates

**Run:** `AS500-r1-20260928T204459Z-dsv4f-hermes`
**Seed:** `deepseek_push/astra_spawn_ideas/AS500_logical_independence_and_redundancy_of_the_thirteen_closure_gates.md`
**Task sha256:** `dcecb81be8236a9fcba6cc16d6bf3288d8b7954886725f7d500ab91f2c1bab5e` (verified at start, matches pinned value)
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter) via Hermes Agent subagent; single worker; macOS 26.5.2
**Branch:** one frozen explicit theory, full13-requirement conjunction; operative filtered MONO + causality criterion B. Q/RAR/MU2/EXP/MONO kept distinct (never silently identified).
**Framework (mandated):** `a0 = kappa*c*sqrt(G*rho_Lambda)`, `kappa = 1/2` **ADOPTED INPUT** (not derived); `r_M = sqrt(G*M_b/a0)`, `v_flat^4 = G*M_b*a0`; `G_N=6.67430e-11`, `c=299792458`, `M_sun=1.98847e30`, `pc=3.085677581491367e16` (SI); G_N/G_bare/G_cosmo separate symbols.

Source pins verified: FRIED_CHICKEN_SPEC.md `98d9149f…3e8f`, breakthrough_review README `22cacef2…32ab`,
FINAL_ACTION.md `b8c04d4e…546e` — all three match SOURCE_MANIFEST.json and the seed's stated pins.

---

## 1. Step 1 — the thirteen amended gate predicates

Let a candidate-domain point be `C = (action A, kernel K, filter F, couplings λ, boundaries ℬ, footings)`
with the amended September-26 target: K = ν_mono, F = heat filter `S = exp((ξ²/2)Δ)`, causality by criterion B.
Each gate is a predicate on C with explicit atoms (a gate is TRUE iff **all** atoms are proved in the
candidate's common action cell):

| # | Gate (operative text) | Atoms | Domain arguments |
|---|---|---|---|
| P1 | Exact MOND phenomenology with ν_mono | ν_mono kernel (RAR up to y\* = 2.3374 < y_p = 2.5396, monotone phantom continuation, 0.0104-dex bound); weak-field eqs ∇²u = 4πGρ_b and ∇²Φ = 4πGρ_b + S\*∇·[(ν_mono−1)∇Su]; deep g² = a0·g_N ⇒ v⁴ = G a0 M_b | y = g_N/a0 ∈ (0,∞); both footings |
| P2 | Exactly two propagating gravitational DOF, N_grav = 2 | two tensor polarizations; no hidden scalar graviton; no propagating auxiliary disguised as constraint; no ghost | full action, leaf/cluster of the KA |
| P3 | Correct lensing / no slip | Φ = Ψ (both from field equations) on the galactic branch ⇒ γ_PPN = 1 | weak-field galactic branch geometry |
| P4 | Full PPN, derived | β≈1, γ≈1, α₁≈0, α₂≈0, α₃≈0 within current limits | PPN gauge, solar-system domain |
| P5 | Ordinary matter conservation | ∇_μT^{μν} = 0 for minimally coupled baryons (Noether–Ward) | compact closed leaf, on-shell, N√h measure |
| P6 | Correct GW sector | c_T = c; positive tensor kinetic energy; two polarizations; GW170817-type constraints | tensor sector, vacuum |
| P7 | Stability + criterion B causality | no ghosts; no gradient instabilities; no strong-coupling pathology; no hidden scalar pole; global time function; no backward signals; no CTC; well-posed mixed Cauchy problem | global preferred foliation |
| P8 | Viable cosmology | expanding FLRW, H ≠ 0; homogeneous k = 0 modes separate from local k ≠ 0 | FLRW ansatz |
| P9 | Controlled zero-field limit | controlled y→0 treatment; ellipticity/constraint-rank control | y → 0 edge of kernel domain |
| P10 | Newtonian/GR recovery | μ→1 at high acceleration; **measured G_N derived** from the action, not assumed equal to bare coupling | high-acc limit; Cavendish-type source |
| P11 | One physical metric | matter and photons minimally coupled to the same g; no photon/graviton speed mismatch | matter coupling, photon coupling |
| P12 | Preserve exponential law | ν_RAR below the phantom peak; exact AQUAL primitive G(y) historical only | kernel clause |
| P13 | a0–vacuum scale relation | a0 = (c/2)√(G ρ_Λ) preserved *or genuinely derived*; honest labeling; no faked derivation | vacuum sector; both footings |

**Registry status (evidence = the nine audited upstream results + this run's checks; all upstreams
unreviewed, cited as evidence, not as accepted theorems):**

- **Landed (proved components):** P12 (kernel definition itself + numeric witness C2a); P1-components
  (deep-law y·ν²→1, MONO landmarks C1–C4, EFE-tensor deep limit C_L/C_T→1/2 [AS245], hydrostatic deep
  slope [AS080], heat gate a0-free [AS133]); P2-components (three-form zero bulk modes [AS658],
  18 primaries, metric sector no primary [AS151]); P5-component **total** ∇·Q_total = 0 [AS138.C01],
  off-shell jet-level Ward [AS138]; P10-component G_N = G_bare/c_N, c_N = 1−α/2 [AS226] + kernel tail →1 (C6).
- **Open (no landed proof in the evidence set):** P3, P4, P6, P7, P8, P9, P13 (statuses in residuals registry).
- **Open atoms of partial gates:** P1 full weak-field filtered system; P2 secondary/tertiary constraint
  chain; P5 matter-only; P10 fixing α (one-parameter family); P11 photon sector.

---

## 2. Step 2 — selected implications (derived here)

### Arc A (principal): P1 ⇒ P12 — strict redundancy in the MONO branch

*Claim.* On the operative branch, any candidate with the ν_mono kernel satisfies gate 12:
`ν_mono(y) = ν_RAR(y) for y ≤ y* = 2.3374` and `y* < y_p = 2.5396`, with the AQUAL primitive G(y)
historical only.

*Derivation.* The operative kernel definition (recipe §user-decision 2026-09-26; contract branch
dictionary) is  `h_RAR(y) = y(ν_RAR − 1) = y/(e^√y − 1)`,  `h′_mono = max(h′_RAR, δ·h_p/(y + y_p))`,
`h_mono(y) = ∫₀^y max(h′_RAR, δ·h_p/(s+y_p)) ds`,  `ν_mono = 1 + h_mono/y`, δ = 0.05.
`h′_RAR(y) = (ν_RAR−1) + y·ν′_RAR`, `ν′_RAR = −e^{−√y}/(2√y (1−e^{−√y})²)`. h′_RAR → ∞ at 0+,
decreases to 0 at the peak y_p; the floor δ h_p/(y+y_p) is positive and decreasing. The unique crossing
of h′_RAR = δ h_p/(y+y_p) defines y\* (the max switches branch there); below y\* the max selects h′_RAR,
so h_mono = h_RAR and ν_mono = ν_RAR exactly on [0, y\*]. Hence P1's kernel clause contains P12's
preservation clause verbatim, and P1's retirement of the AQUAL μ as target (amended R1/R12 wording)
covers P12's "historical only" clause. Numeric witnesses (capable of failing): landmarks
y_p = 2.5396382822 (claim 2.5396), h_p = 0.6476102379 (claim 0.6476), y\* = 2.3374124053 (claim 2.3374);
max |ν_mono − ν_RAR| on [0, y\*] = 0 (5000-node grid); h′_RAR − floor ≥ 0 on [0, y\*] (min margin ≥ 0,
= 0 at y\*); dex bound max |log₁₀(ν_mono/ν_RAR)| = 0.010370 at y = 14.3549 (spec: 0.0104 dex, most at
y = 14.35 — the corrected wording); splice C_L continuity 0.006640 = h′_mono(y\*) with slope jump
h″_RAR(y\*) = −0.03607 → floor slope −0.0013613 (spec: 0.0066; −0.0361 → −0.0014). All residuals recorded
in `residuals.json` (C1–C4). *Converse fails:* P12 does not imply P1 (P1 additionally carries the filter
S, the weak-field system and the deep law) — recorded, not asserted.

### Arc B: P3 ⇒ P4(γ-component) — algebraic, conditional on the ansatz

*Claim.* In the metric ansatz of requirement 3, `ds² = −(1+2Φ/c²)c²dt² + (1−2Ψ/c²)δ_ij dxⁱdxʲ`, the PPN
isotropic matching gives **γ_PPN = Ψ/Φ**; hence Φ = Ψ on the galactic branch forces γ_PPN = 1 there
exactly.

*Derivation (symbolic + Lean-certified).* PPN isotropic form: g₀₀ = −(1+2U/c²)c², g_ij = (1−2γU/c²)δ_ij
with U = Φ in the req-3 sign convention; matching the spatial part gives Ψ = γΦ, i.e. γ = Ψ/Φ.
Φ = Ψ ⇒ γ = 1. Certified in Lean (`AS500_gate_lattice_certificates.lean`: `ppn_gamma_one_of_no_slip`,
axioms exactly {propext, Classical.choice, Quot.sound}, zero sorry). Sympy residual 0 (C8).
*Scope discipline:* this identifies the PPN-γ atom only; P4's β, α₁, α₂, α₃ atoms are **not** touched
(no redundancy claimed), and the solar-system PPN domain still needs Φ, Ψ derived there (P3 itself open:
the galactic-branch Φ=Ψ derivation is not landed in the evidence set).

### Arc C: conjunctive completion — (P6 ∧ P11) ⇒ requirement 11's speed-match clause

Definitional: P11 gives photons on the metric g (null speed c in g); P6 gives gravitons with c_T = c in
the same preferred foliation; together they close "no photon/graviton speed mismatch". Neither alone
suffices (P11 alone has no c_T statement; P6 alone has no photon coupling statement). Recorded as a
conjunctive lattice edge, not an implied single gate.

### Independence: P13's derive-arm is **not** implied by the landed components of P1–P12

*Claim (in-class independence).* In the audited cell (CA4-GNC/CA5-GNC-R pin + k04 four-form, κ-continuum
family of AS651/AS138.C01), there are witnesses satisfying the landed components of the other gates with
κ ≠ 1/2: the family r ↦ κ(r) = √(2/(r+2b)) with r ∈ (0,∞) (b = jsat/(8π), jsat = 0.452524896675131
reproduced from the RAR integral C7), every member conserving (∇·Q_total = 0 as an identity in the
couplings, AS138.C01), every member with G_N = G_bare/c_N at its own α (AS226), and every member with
the same kernel-level deep and Newton limits (this run C5/C6). Hence the conjunction of these landed
components cannot force the specific value κ = 1/2: consistent with AS075's T2O decomposition
(kappa derivable iff obligations A **and** B) and AS651's B-ii/B-iv failures (continuum projection:
κ-projection injective — Lean-certified `kappa_projection_injective`; κ(r\*) = 1/2 exactly at
r\* = 8 − 2b = 7.963989212911001 — Lean-certified `kappa_half_at_rstar`). The seven-point witness set
reproduces AS651 E1 to 2e-6 (C7e) with r\* member = 0.5000000000.

**Both footings:** every statement above is an identity in the dimensionless y (kernel) or
dimensionless r (lattice); the two registered footings a0_can = 9.3619e-11 and a0_alt = 1.1279e-10 m/s²
therefore do not alter any implication. They enter only through the absolute conversions, carried
separately: ρ_Λ(can) = 5.844412454e-27, ρ_Λ(alt) = 8.483089620e-27 kg/m³ (κ = 1/2 fixed in each; the
fixed-density relabel κ_eff = 0.602388404 is a diagnostic only — the two footings never share both
fixed density and fixed κ, per contract). Representative derived kernel-tail constants at Earth orbit
(a_E = 5.930263e-3 m/s²): y_E = 6.334465e7 (canonical) → ν_mono − 1 = 1.858624e-8; y_E = 5.257791e7
(alternative) → ν_mono − 1 = 2.227754e-8. These are kernel-level numbers, **not** a PPN derivation
(gate P4 open).

---

## 3. Step 3 — strict redundancy vs computational prerequisite

| Relation | Type | Proof status |
|---|---|---|
| P1 ⇒ P12 | **strict redundancy** (kernel clause nesting, MONO branch) | derived + numeric C1–C4 |
| P3 ⇒ P4(γ) | **strict, conditional**: algebraic, only the γ atom, only where the req-3 ansatz with Φ=Ψ holds | Lean C-cert + C8 |
| (P6 ∧ P11) ⇒ R11 speed-match clause | **conjunctive completion**, definitional | recorded |
| P2 ⇒ P7(no-scalar-pole atom) | overlap only; P7 has 7 more atoms | not asserted |
| a0 value (P13 or adopted input) → P1's y-argument | **computational prerequisite** (parameter flow), not entailment | — |
| Ward machinery (AS138) → P5 matter-only atom | **computational prerequisite**; total identity ≠ matter-only atom | open bridge → AS500.C01 |
| G_N = G_bare/c_N (AS226) | supplies R10's measured-G atom with α **free** — conditional implication | one-parameter family |

No "unknown treated as true" enters any landed edge: the honest registry (below) rejects every edge
whose target atom is unlanded.

## 4. Step 4 — minimal proven implication graph and open questions

```
      P1 ──(strict kernel clause)──▶ P12             (closed edge, this run)
      P3 ──(PPN match, γ atom)─────▶ P4[γ]           (closed edge, this run; P4[β,α_i] independent)
      P6 ∧ P11 ────────────────────▶ R11-speed-match (conjunctive clause)
      P13: derive-arm ◀── NO landed component of P1–P12 implies it
           (T2O: needs obligations A∧B; B-ii/B-iv fail in k04; conservation leaves continuum)

   Remaining independence questions (each is a live obligation, not a hidden TRUE):
   Q1  P4: β, α₁, α₂, α₃  — no landed derivation (PPN on the pin)
   Q2  P6: c_T = c, tensor kinetic sign         Q3  P7: criterion B (global time function, no CTC, well-posed mixed Cauchy)
   Q4  P8: expanding FLRW, k=0 handling         Q5  P9: controlled y→0, ellipticity/constraint rank
   Q6  P3: Φ = Ψ derived from the field equations (γ atom merely identified, P4's domain needs solar-system derivation)
   Q7  P5: matter-only ∇·Q_b = 0 (total Ward landed; separation open → child AS500.C01)
   Q8  P2: secondary/tertiary constraint chain (primary level landed)
   Q9  P10: fixing α (G_N = G_bare/c_N is a one-parameter family)
   Q10 P13: E* existence outside the audited class (AS075.C01/AS651.C01 tracked)
   Q11 P1: full weak-field filtered system on a compact source (all atoms jointly)

   Minimal closing set (for a final full13 witness, distinct from the lattice result):
   {P3, P4, P6, P7, P8, P9, P11[photons], P13[E* or explicit-adopted label]} ∪ completions
   {P1[WF], P2[secondary], P5[matter-only], P10[fix α]}.
   The lattice deliverable is the implication/independence structure above — the final all-gate
   witness is NOT assembled here (seed stop rule).
```

---

## 5. Controls (all capable of failing; all observed)

1. **CTRL1 — all-green table with unknowns hidden as true must fail.** An optimistic verifier that
   marks the seven open gates (P3, P4, P6, P7, P8, P9, P13) TRUE emits "ALL 13 GATES CLOSED — FINAL
   WITNESS EVALUABLE". The honest registry keeps them open and rejects the closure call with the
   explicit open-atom list. **Observed: control fires** (honest open set NON-empty). Capable of failing:
   it would fail (i.e., the optimistic and honest tables would coincide) only if every gate were actually
   landed — which is the false reading the control is designed to expose.
2. **CTRL2 — out-of-class countermodel cannot establish independence.** The independence claim "P13
   independent of P5, witnessed by a TWO-flux k04 sector" is rejected because the witness cell
   (two-flux, membrane ensemble) ≠ the audited cell (single-flux, no membranes, pinned): changing the
   class changes the model (contract: same-theory discipline). **Observed: control fires.**
3. **Kernel-level controls (this run):** landmarks y_p/h_p/y\* (C1); ν_mono ≡ ν_RAR on [0, y\*] (C2a);
   max-selection margin ≥ 0 with equality at y\* (C2b); dex bound 0.0104 at y = 14.35 (C3); splice
   continuity 0.0066 and slope jump −0.0361→−0.0014 (C4); deep law (y·ν)²/y → 1 with analytic leading
   correction 1+√y+O(y) (C5, residuals 3.204e-2/1.000e-3/3.0e-5 vs the 1.5√y tolerances); Newton tail
   monotone decreasing, ν_mono(1e6)−1 = 1.0429e-6, ν_mono(1e12)−1 = 1.490e-12 (C6 — the MONO tail
   converges only logarithmically, O(δ h_p ln y / y), which is why R10/PPN recovery must come from the
   heat filter, not the kernel tail); jsat reproduction 0.452524896675131 / b = 0.018005393544499 /
   r\* = 7.963989212911001 (C7); γ = Ψ/Φ symbolic (C8); footings separate (C9).

**Result: 28/28 checks PASS, 0 FAIL, both negative controls fire.**

## 6. Execution bounds (actual)

- Wall: **0.76 s** (final run; ulimit -t 120 CPU-second shell cap enforced) — inside the 120 s prototype bound.
- Memory: **max RSS 65,143,296 bytes ≈ 62.1 MiB** (`/usr/bin/time -l`; RLIMIT_AS not enforceable on macOS —
  recorded convention of AS067/AS068/AS075/AS651; actual pressure far below the 512 MB budget).
- Threads: **1** (single CPython process; OPENBLAS/OMP/MKL/VECLIB/NUMEXPR threads = 1; no multiprocessing).
- Precision: mpmath dps = 60; sympy exact symbols for C8; grids: 5000 nodes (C2), 8006 log-spaced nodes (C3).
- Lean: two `lake env lean` invocations (certificates + axiom probe), compile host `fable_independent_2026/lean_2026`
  not written into; Lean 4.34.0-rc2.

## 7. First-principles inputs vs derived

- **Primitives:** κ = 1/2 adopted (never derived); G_N, c, M_sun, pc; both registered footings;
  kernel definition ν_RAR/h_RAR/h′_mono with δ = 0.05 (operative target's own primitives, not fitted);
  FRIED_CHICKEN_SPEC/FINAL_ACTION/recipe pins; audited upstream results as evidence (unreviewed).
- **Derived here:** γ = Ψ/Φ (PPN match); landmark consistency y_p, h_p, y\*; ν_mono ≡ ν_RAR on [0, y\*];
  dex = 0.010370 at 14.3549; splice C_L continuity + slope jump; deep-law leading correction;
  logarithmic Newton tail with asymptotic form and Earth-orbit values on both footings;
  jsat/b/r\* reproduction; κ(r) continuum injection + κ(r\*) = 1/2 (Lean); registry verdicts.
- **Boundary/initial data:** none needed (static algebra + kernel identities + registry; no dynamics,
  no causality statement, no observational claim).

## 8. Limitations (what this result does not establish)

- No gate value is promoted to "closed" here; the registry's open atoms are exactly the unresolved list.
- The independence statement for P13 is **class-scoped** (audited k01/k04/CA4/CA5 cells): an E*
  outside the class could succeed (that is the tracked AS075.C01/AS651.C01 search).
- Kernel-landmark and dex checks are numeric (60-dps) finite evidence; exactness of the kernel nesting
  rests on the operative definitions; the algebraic lattice edges are Lean-certified.
- The Earth-tail numbers are kernel-level; they are NOT a PPN derivation (P4 open) and NOT an empirical test.
- Upstream results are cited as evidence with their own scopes; all remain `unreviewed`.
- json registry duplicates are intentional (residuals.json is the machine record; this document the prose).

## 9. Child proposal

`branches/AS500/AS500.C01.md` (ready spec, NOT dispatched): matter-only Ward separation at the
CA5-GNC-R pin — prove ∇·Q_b = 0 on shell (decoupling) or exhibit the exact nonzero cross-source term
(gate-P5 atom verdict). No spawn mechanism in this worker; returned to the orchestrator.