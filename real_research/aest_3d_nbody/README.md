# 3D AeST N-body — settling the last open cluster door (#1)

**Created 2026-06-26.** The one genuinely-un-foreclosed avenue for the AeST cluster residual.

## The question

The published cluster no-go (Zenodo 10.5281/zenodo.20779562; commit `a0bc7620`) showed that **1D spherical
dynamical collapse does NOT phase-pin the AeST scalar's oscillation mode** ω = μc: the shift-symmetric AeST action
has no friction, the free Helmholtz/KG mode is undamped (708 osc/Hubble time), and collapse tracks the initial
conditions ~1:1 — so the +μ²Φ boost stays *descriptive*, not predictive, and can't organically cure the cluster
residual. The cluster theory program is **complete except observational η(R500) and this one item** (commit `5f1e4b0a`).

**Does 3D *asymmetric* collapse — real shear, violent mergers, large-amplitude tensor modes — phase-pin the
ω = μc mode where 1D spherical collapse cannot?** If yes, the cluster residual gets an organic dynamical source
that is galaxy-safe (the 1D case kept a 19× margin under the SPARC veto). If no, the no-go holds in 3D too and the
cluster front is settled as a shared-MOND, gas-tracking, ceiling-bounded gap.

## Honest prior: LOW — and there is a sharp analytic reason

The AS-door workflow (verdict `real_research/GEMINI_AS_PLUS_CLUSTER_IDEAS_VERDICT_2026-06.md`, idea #3) found that
AeST's vector field has a **Maxwell-type (antisymmetric) kinetic term**, giving a mode-coupling matrix `C` with
`v·(C v) = 0` — so **shear injects ZERO power into the free ω = μc mode at linear order.** Combined with the
covariant-MI **passivity → anti-MOND sign theorem** (any causal, ghost-free kernel raises inertia), both point to
"3D won't phase-pin either." This is NOT a closed door, but it is a low-prior one.

## Plan — gate first, build only if warranted

1. **DECISIVE GATE (analytic, cheap).** Is the antisymmetric-coupling obstruction `v·(C v)=0` **robust at nonlinear /
   large-amplitude / merger order**, or is it a linear artifact that nonlinear mode-mixing (the φ–A_μ cross terms,
   merger shocks, O(1) tensor modes) breaks? Robust ⇒ #1 **closes analytically** (settle it, no N-body needed).
   Breakable ⇒ the N-body is genuinely required.
2. **PROTOTYPE (only if the gate doesn't foreclose).** A reduced but genuine 3D AeST field evolution: a few merging
   overdensities on a grid, the scalar+vector field equations, a **phase-coherence diagnostic** (does the ω = μc
   phase organize across the cluster, or track ICs ~1:1 as in 1D?). With **validation gates**: must reproduce the
   1D no-go in the spherical limit and the deep-MOND limit at a₀ = 9.36e-11.
3. **VERDICT.** Does 3D asymmetric collapse phase-pin? Both-ways, against the galaxy veto and Cassini.

## Honest scope

A production-grade AeST N-body campaign is a multi-session numerical undertaking. This folder builds (a) the decisive
analytic gate — which may settle #1 outright — and (b) a genuine, runnable prototype with validation gates, for the
case where the gate leaves the door open. No manufactured cure; the gate decides.

## Files
- `aest_field.py` — the AeST action, field equations, the mode-coupling matrix C (built by the workflow)
- `phase_gate.py` — the decisive nonlinear-robustness analysis of v·(C v)=0
- `collapse3d_prototype.py` — the reduced 3D prototype + phase diagnostic (if warranted)
- `VALIDATION.md` — the 1D-no-go and deep-MOND validation gates
- `VERDICT.md` — the both-ways result
