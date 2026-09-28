# AS057.C01 — Ready child specification (for orchestrator dispatch; NOT run)

**Status:** `ready_for_orchestrator` — no child was dispatched by this worker (no spawn mechanism in the subagent toolset; nothing claimed as run).
**Parent:** AS057, run `AS057-r1-20260928T080406Z-dsv4f-hermes`
**Parent evidence:** `derivation.md` + `AS057_derive.py` (26/26 checks) + `AS057_static_channel_rank.lean` (compiled, axioms ⊆ {propext, Classical.choice, Quot.sound}); parent task hash `dabeefc18b2509122638df4dd87ce8db1671c19a13b020d10fa7385d3ec892c6`; parent outcome `supports_scoped_claim` (unreviewed).
**Suggested owner/runner:** any available AS worker; resources ≤ 120 s / 512 MB / 1 thread.

## 1. Exact new claim (target)
**C01-T:** *The operative filtered-MONO action of the amended thirteen-item target (`Delta u = 4πGρ`, `ΔΦ = 4πGρ + S*·div[(ν_mono(|∇Su|/a0)−1)∇Su]`, `S = exp((ξ²/2)Δ)`), restricted to the admitted static, weak-field, diagonal galactic sector, reduces to a two-potential system whose linearized Einstein sector is the diagonal ansatz of AS057 — i.e. its metric potentials (lapse and spatial conformal factor) enter only through the two combinations `(d−1)ΔΨ` and `(d−1)Δ(Φ−Ψ) + (d−1)(3−d)ΔΨ` with `d = 3`.* If the reduction fails, the counterexample isolates the first operator that breaks the diagonal form (target-native no-go), preserving the AS057 rank theorem as a statement about the linearized-geometry sector only.

## 2. Why the parent result does not already answer it
AS057 proved the rank theorem for the *linearized geometry* (carrier algebra). It did not prove that the operative action's static sector *is* that diagonal two-potential geometry — the branch-translation lemma is the explicitly listed "next unresolved implication" of AS057. C01 is exactly that bridge; without it AS057 governs the geometric sector only.

## 3. Scientific fingerprint (duplicate check)
- (action/source revision: filtered MONO action, FRIED_CHICKEN_SPEC amendment, Sept 26 base; branch: MONO-B/gate translation; assumptions: static weak-field diagonal, criterion B; domain: galactic, r ≫ r_M; target claim: two-potential reduction + channel identity; observable/operator: linearized Einstein operator content of the action's static sector; new input: none — existing action, no new functions).
- Duplicate search: `manifest.json` (AS catalog), `results/`, `claims/`, `fresh_gravity_followups/queue.json` — **no existing seed or child targets this reduction** (no AS seed contains "two-lever"/"lever reduction"; closest priors: PD01 B1 (channel content of linearized GR — not the operative action), k01 (zero-mode audit of a *different* action class), L212 (decoupling branch — different target). This child is not a rename or re-parametrization of any of them.

## 4. First-principles premise and closure implication
Premise: the operative action's field content (metric + scalar response) with the heat filter `S` and gate definitions must be fixed by the FRIED_CHICKEN_SPEC amendment block; variation gives both metric potentials and the scalar equation. Closure implication: proving C01-T transfers the AS057 rank/dimension theorem (count n = 2 for all d ≥ 2, d=3 decoupling) into the operative same-action cell — closing the "carrier premise" gap of the kappa = 1/2 derivation chain (A03 group), with criterion B and PUER untouched (checked, not altered).

## 5. Ordered bounded steps + one negative control
1. Pin the action and dictionary from `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` (hash `98d9149f…`), `FINAL_ACTION.md` and the transport records; record hashes.
2. Vary the action in the static diagonal sector symbolically; derive the Euler–Lagrange system for `(Φ, Ψ, u)` and the metric potentials; compare the linearized Einstein operator content with AS057's two channels (symbolic, then substituted at d=3).
3. Identical check in a second representation: numeric finite-difference variation on a spherical grid (construct the operator, evaluate on Gaussian probes, record residuals; threshold set before evaluation).
4. **Negative control (capable of failing):** insert an explicit off-diagonal perturbation source (e.g., a nonzero `h_{ij}` traceless slip beyond the conformal form) into the action's admitted sector and demonstrate the channel decomposition fails there — showing C01-T's domain boundary is real, not assumed.
5. Report: theorem (reduction holds) or no-go (first breaking operator identified); branch status MONO-B; acceptance: exact operator identity at the symbolic level + residual < 1e−3 numeric, or a target-native counterexample.

## 6. Owner/runner state and escalation
Owner requested but not assigned; runner required (not claimed run). Escalation condition: if the action's static sector contains operators beyond the two-potential form (e.g., kernel-mediated nonlocalities that break the diagonal structure in the admitted domain), return the exact operator and stop — AS057's next implication then splits into a repair/no-go decision by the orchestrator.