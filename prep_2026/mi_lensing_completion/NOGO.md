# NOGO — the sharpened MI-lensing no-go (completeness check for the C1/C2/C3 lane)

**Date:** 2026-07-17 · **Status:** verified, `nogo.py` exit 0 (16/16 checks, both a₀ footings)
**Script:** `prep_2026/mi_lensing_completion/nogo.py` · Frozen repo READ-ONLY throughout.
**Credit:** Deffayet–Woodard 2011 (1106.4984), Skordis–Zlosnik AeST 2021, Milgrom (AQUAL / MOND-as-MI).
**Banked:** `LENSING_TRILEMMA_2026.md` (the A/B/C EEP + one-null-cone exhaustion); covariant/cluster
no-go 10.5281/zenodo.20779562; the assembled single-metric verdict `mi_lensing_final/SOLVE.md`
(F(y) < 1/ν, Brouwer 2021 ~27σ).

---

## The question

Can the ν² lensing wedge (pure MI sources ρ/ν but needs ν·ρ — the factor-ν² gap = the phantom mass
`M_ph = (ν−1)M_bar` that QUMOND/AeST source and MI does not) be closed while keeping **all four**:

- **D** — a₀ **DERIVED** from `cH_Λ/Z` (the passive 0-dof frame `u`, the bounded kernel
  `K(□_u/a₀²)`, `‖K‖≤1`, a₀ living in the kernel *argument* tied to the dS horizon);
- **S** — **single-metric**, `c_γ = c_GW` (no disformal photon term; the disformal route is
  GW170817-dead by ~7 orders — do not reopen);
- **G** — **ghost-free** (no Ostrogradsky / negative-norm mode);
- **L** — **MOND-lensing** (a single-metric phantom source `(ν−1)ρ u_μu_ν`, deep slope
  `g_lens ~ √(a₀ g_bar)`, `F = g_lens/(ν g_bar) → 1`).

**Answer: no — and the obstruction is exact.** `{D, S, L}` is already mutually exclusive (ghost-freedom
G is not even the lever). Within the mandatory single-metric arena **S**, the binding collision is the
**pair**:

> **a₀-DERIVED (passive 0-dof frame, bounded kernel)  ⊕  MOND-LENSING phantom `(ν−1)ρ`  — mutually exclusive.**

---

## The mechanism (each step machine-checked in `nogo.py`)

**1. The phantom is NONLOCAL in the baryons.** For a point mass, closing lensing needs enclosed phantom
`M_ph(r) = (ν−1)M` with `y = GM/(a₀ r²)`; sympy gives `M_ph(r)/r → √(a₀M/G) ≠ 0` as `r→∞` — an
**unbounded halo** whose enclosed mass keeps growing outside the source. A *local* functional of `ρ` and
the passive frame has `T_00` supported on `supp(ρ)` (every variation leg carries an explicit `ρ_m`;
`LENSING_TRILEMMA §2.1(i)`), so it produces **zero** growth off-source. **L therefore requires a nonlocal
carrier** — a term whose variation yields an elliptic equation `∇·[…] = ρ` (the inverse-Laplacian of
QUMOND/AQUAL).

**2. The passive frame is BOUNDED — it cannot be that carrier.** On the RAR shell `K = 1/ν ≤ 1` (deep-MOND
`K→0`: the source is dressed **down**). The phantom needs `uu`-coefficient `ν − 1/ν = 1/√(y(y+1))`
(deep `~1/√y`, unbounded); the passive frame supplies `1/ν`. The **shortfall = ν²−1 = 1/y**, which
**diverges** as `y→0`. The anisotropic (slip) leg is `2K'X/K = 1/(2y+1) ≤ 1` — bounded and tension-signed
(it *reduces* lensing; `SOLVE.md`). A bounded Herglotz kernel (`‖K‖≤1`, the banked positivity result)
supplies only `O(K) ≤ 1` dressing — **never the `O(ν)` phantom**. Keeping **D** confines the modification
to this bounded kernel ⇒ **¬L**.

**3. A local universal `F(y)` is MASS-BLIND.** If instead one writes a local curvature/frame coupling
`F(K)` (the a₀-derived, no-new-constant hope of C1), lensing closure on a point mass forces
`F'_req(y) ∝ √M` — the amplitude carries the **source mass**, `F'_req(M₂)/F'_req(M₁) = √(M₂/M₁)`,
independent of `y`. A local `F` sees only `|a|`, so **no single universal `F` sources the phantom for more
than one object**: fix it on a `6×10¹⁰M_⊙` galaxy and a `10¹⁴M_⊙` cluster receives fraction
`√(6×10¹⁰/10¹⁴) ≈ 0.024` — massive under-lensing. To repair mass-blindness you must go nonlocal → §4.

**4. Nonlocal carrier ⇒ propagation ⇒ a₀ FREE.** Any carrier reproducing the elliptic phantom has a
spatial-kinetic term, so it **propagates** (a new scalar dof) — or its shape is a free function put in by
hand. Either way its acceleration scale is a **free Lagrangian coupling**; nothing forces it to equal
`cH_Λ/Z` (the derivation lives in the *passive* kernel argument, and is number-field gauge-blind: `Z`
carries the transcendental `√π`, banked). So **L ⇒ ¬D**. This is exactly what C2 (Deffayet–Woodard
nonlocal-in-matter) and C3b (frame/dilaton nonlocal carrier) realize constructively.

**5. Dropping S is not an escape.** `¬S` = a second, disformal photon cone (horn B) — GW170817-dead by
~7 orders. So **S is mandatory**, and the collision reduces to the pair `D ⊕ L`.

**6. Dropping G does not rescue `D∧S∧L` either.** Allowing an Ostrogradsky ghost, the local a₀-derived
frame term (C1) **still fails L** by mass-blindness (§3), independent of the ghost. So the minimal
mutually-exclusive subset is **`{D, S, L}`** — G is a *separate* cost, not the binding lever.

---

## The finite logical exhaustion (`nogo.py §5`)

Encoding the mechanism as axioms — `L∧D` collide (§2/§4), `L∧¬S` is GW-dead (§5) — over all 16
assignments of `{D,S,G,L}` leaves these admissible single-metric (S=1) corners:

| D | S | G | L | identity |
|---|---|---|---|---|
| 1 | 1 | 1 | 0 | **pure MI / C3a** — a₀ DERIVED, ghost-free, but UNDER-LENSES (`F < 1/ν`, the current theory) |
| 1 | 1 | 0 | 0 | **C1** local ghostly frame term — still FAILS L (mass-blind) even with a ghost |
| 0 | 1 | 1 | 1 | **C2, C3b** — CLOSES lensing, single-metric, ghost-free, but **a₀ FREE (= MG)** |
| 0 | 1 | 0 | 1 | DW-nonlocal with untamed ghost — closes L, a₀ free, ghost (contested) |
| 0 | 1 | 1 | 0 | GR / trivial |
| 0 | 1 | 0 | 0 | GR + ghost (vacuous) |

**The target `D=S=G=L=1` is absent (unsatisfiable).** Its ghost-relaxed sibling `D=S=1,G=0,L=1` is also
absent. The completion the lane sought does not exist as modified inertia.

---

## Effect on the banked A/B/C trilemma: it CLOSES tighter (no gap)

The new `(ν−1)ρ`-phantom-source specification exposes **no gap** in the horns A/B/C — it **closes the
trilemma tighter and makes horn A constructive**:

- A phantom that gravitates on the shared single cone is felt by geodesic matter (EEP, one null cone),
  forcing the modified-inertia response `μ→1` — **horn A's collapse to modified gravity**. C2 and C3b are
  its explicit realizations (the "correct-lensing one-cone theory reclassifies as MG"), and they pay
  exactly horn A's price: **a₀ free**.
- **Horn C cannot escape:** confining the source to the passive matter/frame sector gives `O(K) ≤ 1`
  (baryon-confined `T_00 = 0` off-`supp(ρ)`) — under-lenses (`F < 1/ν`), the `SOLVE.md` result. C1/C3a.
- The one loophole the trilemma left open (§2.1 anisotropic-stress *slip*) is now **computed shut, not
  merely bounded**: the assembled `K'aa` slip leg is `2K'X/K = 1/(2y+1)`, `O(K)` and **tension-signed**
  (`SOLVE.md`), so it reduces rather than enhances lensing.

So the phantom spec is fully **absorbed** by the existing trilemma. It converts the trilemma's "correct
lensing ⇒ modified gravity or a medium" from an EEP/exhaustion argument into a **constructive** wall with
three independent realizations (C1: `¬L`; C2 & C3b: `¬D`).

---

## Precise statement of the obstruction

**Within single-metric `c_γ=c_GW` (mandatory; the disformal alternative is GW170817-dead):**

> **`{a₀-DERIVED-from-passive-vacuum}` and `{MOND-lensing single-metric phantom `(ν−1)ρ`}` are mutually
> exclusive.** Sourcing the phantom is nonlocal in the baryons, which forces a propagating carrier whose
> acceleration scale is a free coupling (⇒ ¬D); keeping a₀ derived confines the modification to the
> passive frame's bounded kernel `‖K‖≤1`, short of the needed `ν` by `ν²−1 = 1/y → ∞` deep-MOND (⇒ ¬L).
> Ghost-freedom (G) and single-metric (S) are jointly *satisfiable on the L side* (C2/C3b hold both) —
> they are **not** the binding constraints; the minimal unsatisfiable subset is `{D, S, L}`.

**This is not a manufactured no-go and not a manufactured completion.** The theory *can* be completed for
lensing — but only **as modified GRAVITY** (C2/C3b: single-metric, ghost-free, MOND-lensing), at the honest
price of **a₀ FREE**, forfeiting the vacuum-derived `a₀ = cH_Λ/Z`. That is a **partial**, correctly
labeled: the lensing sector completes in the Deffayet–Woodard / AeST class, losing the MI-distinctive
content. Secondary costs of the L-side survivors: C2's would-be ghost is tamed only by the *contested*
retarded prescription; C3b adds a propagating scalar and needs a separate cosmology fit.

---

## Footings

Both `a₀ = 9.36×10⁻¹¹` (canonical `cH_Λ/Z`) and `1.13×10⁻¹⁰` (alt) carried. The wedge is **a₀-free**: the
shortfall `1/y` and the mass-blindness ratio `√(M₂/M₁)` are dimensionless in `y = g_bar/a₀`, and the MOND
relation `g_obs = √(g_bar² + a₀g_bar)` is form-invariant under `(a₀,g_bar) → λ(a₀,g_bar)` (sympy-checked).
On the L side a₀ is **footing-non-diagnostic** — the signature of a **free parameter**, corroborating
`L ⇒ ¬D` from the estimator side. The verdict is footing-independent.

---

*Reproduce:* `python3 nogo.py` (exit 0, 16/16; companions `c1_frame_curvature.py`, `c2_nonlocal.py`,
`c3_carrier.py`, all exit 0). No "proves / solved / complete field theory" language: no candidate passes
all five, so none is claimed. The result is the **sharpened no-go** — the exact obstruction and the exact
mutually-exclusive subset.
