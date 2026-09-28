# AS234 — Derive alpha2 from a longitudinal moving-source response — run report (declare-rescue)

**Run dir:** `deepseek_push/astra_spawn_ideas/results/AS234/AS234-r1-20260928T195311Z-dsv4f-hermes/`
**Seed:** `AS234_derive_alpha2_from_a_longitudinal_moving_source_response.md`, sha256 `137ce4fcdd0715388850e23252530cc44b3ef2e500c6c37a3372216a6cb0de89`
**Dispatch slot (claims registry, untouched):** worker `sa-1-3062fce3`, reserved 2026-09-28T19:21:09Z, dispatched 19:22:13Z; run started 19:53:11Z.

## 1. Status

**Execution: COMPLETED** (sympy derivation `as234_derive.py` ran to completion; `derive_raw.out` holds the real residuals).
**Packaging: COMPLETED BY RESCUE.** The original worker executed the derivation but died before packaging; its Lean certificate did not compile and contained algebraic claims that were not identical to the executed residual. The certificate was corrected and now compiles (zero `sorry`; all axioms ⊆ {propext, Classical.choice, Quot.sound}).

**Classification (per seed completion criterion):** the same-action alpha2 extraction is **FAILED BY AN EXPLICIT RESIDUAL / OBSTRUCTED** at order v² in the tied sector: the order-v² consistency residual of the E_A momentum equation is

```
R = -8 rho / D ,   D = S_k alpha ell - 2 S_k c_N ell - 2 S_k ell - 4 alpha + 8 c_N + 24
```

(R is **k-independent** and c2-free after reduction; `derive_raw.out` prints the branch value `-2*rho/7`.) For rho > 0 this is nonzero at the branch-faithful point and, in fact, nowhere on the pinned branch (D≠0): the rest-isotropic pinned configuration cannot carry the conserved moving-source stress at order v², and the two printed extraction windows give mutually inconsistent tentative alpha2 values. This is a **counterexample-style obstruction witness**, not a derived alpha2.

## 2. Mandated framework inputs (unused numerically — pure dimensionless algebra)

- `a0 = kappa c sqrt(G rho_Lambda)`, `kappa = 1/2` **adopted** (not derived here; no independent normalization argument in this run).
- Footings: canonical `a0 = 9.3619e-11 m/s^2` and alternative `1.1279e-10 m/s^2`. This result is a dimensionless-in-parameters algebra identity (all quantities are coefficients/symbolic densities in the action); no G, c, or rho_Lambda number enters, so **both footings apply unchanged**; no per-object a0 fit was made.
- `G_N`, `G_bare`, `G_cosmo` remain separate symbols (only the coefficient cell below is used).
- Branch dictionary respected: the calculation is performed in the tied **CA5-GNC-R physical-metric quadratic action**; Q/RAR/MU2/EXP/MONO laws are never invoked, so no inter-branch translation was needed.

## 3. Pinned action / mode cell (what was executed)

- Quadratic sector `L2 = (M_P^2/2)[ R^(2) - c2 K^2 + alpha|a-DZ|^2 + 4 a.DZ - 2|DZ|^2 - 2 cN |D(phi-Z)|^2 - 4 cN DZ.DU ]` + `S_b-linear` dust coupling `-rho phi + rho v chi - rho v^2 (Psi+A)` (units M_P^2/2; FINAL_ACTION (4) style; static anchor AS226).
- Mode ansatz `f(t,z) = Re[ a exp(i(omega t - k z)) ]`: `d_t -> i omega`, `d_z -> -i k`; **longitudinal sector k || v || z**; uniformly moving conserved dust `T^00=rho, T^0i=rho v^i, T^ij=rho v^i v^j`, `omega = k v`.
- Physical metric `g00=-(1+phi)^2+chi^2`, `g03=chi`, `g11=g22=1-2Psi`, `g33=1-2Psi-2A`.
- Ties: `Z = (ell S_k/4) phi` (eq. (6), f=0) and `U = phi - Z` (eq. (7), rho_d=0).
- Gauge/pins: real-response gauge `a_f = ac_f` at every order; rest-isotropy pins setting static/anisotropic amplitudes to zero; order-by-order block solve in v through v².
- Nothing here is a historical branch comparison; all statements are about this tied action.

## 4. Executed results (exactly what the raw output says)

`derive_raw.out` (116 KB), main run `time_mem_derive.txt` (real 6.60 s):

1. **Solve consistency:** "substitution-back residuals vanish through v^2 at exact rational sample: True" (sampled at k=3/2, M_P^2=5/2, c_N=3/2, alpha=1/2, c2=1/3, ell=1/20, S_k=1/2, rho=2/3). The order-by-order solve is self-consistent on its domain.
2. **Obstruction witness (main residual):** the order-v² row of `E_A` has no unknown coupling (A drops out of every EOM at this order; `a_A = 0` printed). Its consistency residual at the solved series prints as the long rational expression whose branch-eval is printed as `branch-eval (alpha=0):  -2*rho/7`. Full reduction (sympy on the printed expression): **R = -8 rho / D**, where D = S_k alpha ell - 2 S_k c_N ell - 2 S_k ell - 4 alpha + 8 c_N + 24; **k cancels in every printed term** (k-independent) and c2 cancels. At the rational sample R = -1280/8133 ≠ 0 (D = 2711/80). For rho>0, R ≠ 0 for every finite D ≠ 0: **no crossing on the pinned branch** (alpha = 14/3 is a pole, D = 0).
3. **Tentative alpha2 extraction (window inconsistency — no unique value):**
   - g'03 window: `alpha2 (g'03 window)` simplifies to (-S_k alpha ell + 2 S_k c_N ell + 2 S_k ell + 4 alpha + 4 c2 - 8 c_N - 8)/(M_P2 c2 D); at branch = **-2/(7 M_P^2)**.
   - g'00 window: `(g'00 - [-1+2U_N]) v^2-coeff, /(rho/k^2)` at branch = **(49 M_P^2 - 2 rho)/(49 M_P^2 rho)** (tentative alpha2 = minus that). Both depend on M_P^2/rho without any G factor (dimensionally non-uniform), and the two windows disagree: no clean PPN alpha2 can be read off — consistent with the v² obstruction.
   - GR limit control: `alpha2(alpha=0,c2=0,ell=0) = nan` (division by c2 — singular); the extraction has no finite GR limit in this window.
4. **Static tied-sector checks vs the AS226 anchor (informational):** substituting the AS226 static phi0 leaves nonzero residuals in the tied system: E_phi residual branch value rho/2 (generic -rho(alpha-2)/(4 c_N)), E_psi residual branch 4 rho/3 (generic -4 rho/(c_N(S_k ell-4))), E_U residual 0 exactly. The tied (Z,U) static sector is not the AS226 anchor; the solve re-derives it and the back-substitution check (item 1) applies to the solved series.
5. **Negative control (density-only moving source):** printed `C_M (density-only, chi=0)`, "fires (nonzero)? True" (expression still contains free conjugate amplitudes, so it fired symbolically, not as a closed numeric value). With the (Psi+A)-rho v² shift-matter source removed from the E_A residual, the model control residual is 6 c2 rho/D = **3 rho/14 at branch** (k2 = 1, D = 28), nonzero for rho>0: the obstruction does not come from the shift-matter coupling — it is a property of the static sector.
6. **Early attempt (`time_mem_derive_obstructed.txt` + `order2_obstruction_debug.out`):** an earlier variant of the order-2 block was singular — `NonInvertibleMatrixError` ("Matrix det == 0") with the 5x5 `order-2 M` printed, whose E_A row is the zero row `[0, 0, 0, 0, 0]` (real 1.57 s, max RSS 64,929,792 B). This is the mechanical shadow of the same A-decoupling; the final code path treats the A row as a pure consistency condition and reports item 2.

## 5. Controls (each capable of failing — all fired where they should)

| Control | Requirement | Observed |
|---|---|---|
| Back-substitution through v² at exact rational sample | vanish | **True** (raw print) |
| E_A consistency at branch (alpha=0, c_N=1, S_k=ell=1, c2=1) | 0 for a valid pinned config | **-2 rho/7 ≠ 0** (rho>0) — FAILS |
| Residual closed form | check k-dependence | **-8 rho/D, k-independent** (sympy on printed expr.) |
| Crossing search on pinned branch | none expected | none: residual ≠ 0 for all finite D≠0; alpha=14/3 is a pole |
| Negative control (density-only) | fires (nonzero) | **fires** (raw: "fires (nonzero)? True"; model 3 rho/14 ≠ 0) |
| GR limit control | finite | **nan** — FAILS (singular window) |
| Window consistency (g'00 vs g'03) | same alpha2 | **disagree** (-2/(7 M_P^2) vs (49 M_P^2-2 rho)/(49 M_P^2 rho)) — FAILS |
| Lean certificate | compiles, 0 sorry, axioms ⊆ {propext, Classical.choice, Quot.sound} | **yes** (all 12 theorems exactly that axiom set; `as234_alpha2_axioms.txt`) |

## 6. Lean certificate (rescued)

`as234_alpha2.lean` certifies the branch-faithful algebra of the executed residual:
branches: D(0,1,1,1)=28; executed residual resid_EA2(rho,Dv) = -8 rho/Dv, branch value resid_branch: resid_EA2 rho (D 0 1 1 1) = -2 rho/7; obstruction witness resid_nezero (rho≠0, Dv≠0 ⇒ residual ≠ 0); the worker's s0p/EA2 model with **k2 explicit**: EA2_closed: EA2 = rho(12 c2 k2 - Dv)/(2 Dv), EA2_branch: rho(3 k2 - 7)/14, EA2_branch_k1: -2 rho/7 (the executed branch value); density-only control EA2_dens_branch: 3 k2 rho/14, k2=1: 3 rho/14, densities_nezero; D_cross_candidate (algebra-only: the old alpha=8/3 crossing lives in a model that is *not* the executed residual — the executed -8 rho/D has no such crossing) and pinned_no_crossing.

**Rescue fix record:** the original file claimed EA2_closed = rho(12 c2 - Dv)/(2 Dv) and EA2_dens at branch = 3 rho/14, dropping the wave-number factor k2; the resulting goal `k2 * rho * 56 = rho * 56` is unprovable from k2 ≠ 0 (it would assert k2 = 1). The rescue keeps k2 explicit (matching the definitions' own algebra; the executed residual is k-independent, so k2 is a pure bookkeeping symbol that must be normalized, not silently dropped) and certifies the k2=1 specializations for the executed branch values. Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>/as234_alpha2.lean` — **exit 0**, real ≈ 3.3 s.

## 7. Honest limitations — what this does NOT establish

- No numerical alpha2 (no m/s², no G/c/rho_Lambda numbers, no 9.3619e-11/1.1279e-10 evaluation — no a0 footing was exercised; the obstruction is footing-independent algebra).
- No resolution of the obstruction: why the rest-isotropic pin violates E_A at v², and which relaxation (anisotropic static A, altered Z/U tie, altered pinning, or a genuinely different moving-source stress model) restores consistency, is **not** derived here.
- The negative control fired only symbolically (free conjugate amplitudes remain in the printed C_M); its closed numeric value at the solved series was not printed by the executed code.
- The GR-limit "nan" and window inconsistency mean no PPN alpha2 of any sign is certified.
- Lean certifies the algebra in the file, not the physical derivation; the physics claims rest on the executed sympy output and its printed residuals.

## 8. Next unresolved implication / suggested follow-up

**Next unresolved implication:** the order-v² E_A consistency of the tied CA5-GNC-R action under a conserved moving source: derive the constraint that the pinned rest-isotropic sector must satisfy for R = -8 rho/D = 0 (requires either a modified tie or an explicitly non-rest-isotropic static A sector), i.e. the missing equation/hypothesis named by this obstruction.

**Suggested follow-up (one discriminating continuation):** relax the rest-isotropy pin (admit an O(v⁰) anisotropic A / Psi sector or an anisotropic Z tie) and re-run the identical order-v² block: if a non-rest-isotropic pin makes the E_A consistency row satisfied at branch, the extraction can be completed; if the row remains nonzero for all pins, the alpha2 target is a no-go in this action branch and should be closed as such. Route stop: no new physics runs were made in this rescue beyond algebra on the printed output.