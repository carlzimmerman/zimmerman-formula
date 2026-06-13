# VERIFY — agentWW ROUTE 2 (dssyk-quantum): hostile referee (2026-06-13)

**Mission.** Did ROUTE 2 establish a genuine STRUCTURAL bridge (a real operator-algebra
identity), or OVERCLAIM a DERIVATION from what is really a reproduction of already-banked
semiclassical objects (Gibbons–Hawking T_dS, the dS QNM ladder, the dS mass–dimension
relation)? The route self-graded **STRUCTURAL-BRIDGE**. Default ceiling: STRUCTURAL-BRIDGE
unless an algebra-internal derivation of a0 (its scale or coefficient) is shown. I re-derived
every load-bearing number independently (`/tmp/verify_dssyk*.py`) and arXiv-checked the one pin.

---

## 1. Independent recomputation of the load-bearing claims — ALL REPRODUCE

| # | Claim (route) | My independent check | Result |
|---|---|---|---|
| A | q-Hermite → physicists' Hermite as q→1; n=4 ratio 0.952/0.9952/0.99952/0.999952 | ratio = 1 − 0.48(1−q) exactly (smooth q→1→1); continuous q-Hermite → classical Hermite at q=1 is the standard Ismail limit | **REPRODUCES** (phi-independent) |
| B | QNM ladder Γ_n = sinh((Δ+n)λ) → (Δ+n)λ as q→1; λ↔H | sympy series of sinh((Δ+n)λ) at λ→0 = λ(Δ+n) exactly; spacing λ (Δ-free), offset Δλ | **REPRODUCES** (= banked dS QNM ladder) |
| C | matter mass m² = 4Δ(1−Δ) (N-V dS₃) | sympy: roots Δ=0,1; max m²=1 at Δ=1/2 = standard dS mass↔dimension; **arXiv 2310.16994 confirms verbatim** "m²=4Δ(1−Δ) in a 3D de Sitter space-time" | **REPRODUCES + PIN VERIFIED** |
| D | raw band E₀ = 2/√(1−q) DIVERGES as q→1 | sympy limit q→1⁻ = −∞ (i.e. +∞ magnitude); finite physical energy needs an origin choice = placement | **REPRODUCES** (q→1 is placement-conditional) |
| E | entropy S(θ)=(2πθ−2θ²)/λ, max π²/(2λ) ⇒ S_dS~1/λ~1/G_N; λ=coupling not temperature | sympy: dS/dθ=0 at θ=π/2, S_max=π²/(2λ); so λ~G_N | **REPRODUCES** (λ is a coupling) |
| F | a0 = cH/Z: NOT a DSSYK output (needs a and c_chi, both absent) | see §2 — the central test | **CONFIRMED (no derivation)** |
| G | MOND sign p=(s+1)/(s+2): center s=0→p=1/2 (MOND), edge s=1/2→p=3/5 (anti-MOND) | sympy: p(0)=1/2, p(1/2)=3/5; sign FLIPS with placement; algebra supplies both | **REPRODUCES** (placement-conditional) |
| H | new q-QNM output ~1e-122 invisible | λ~1/S_dS~1e-122 ⇒ correction ~((Δ+n)λ)²/6 ~ 1e-244 | **REPRODUCES** (empirically null) |

**arXiv pin (the route's single fetch, N-V 2310.16994):** I independently fetched the abstract.
It confirms `R_dS/G_N = 4πN/p²` and `m²=4Δ(1−Δ)` in dS₃ exactly as the route cited, and the
"infinite temperature" character of the doubled-SYK / center placement. **Pin accurate.**

Numerical/symbolic integrity: every block is a closed-form sympy/mpmath identity, not a fit.
No number in the route's compute log failed to reproduce.

---

## 2. THE CENTRAL TEST — structural or derivational? Does the algebra fix a0?

This is the whole mission. The framework's a0 sits at **a ~ cH** (Link 2–3), reached only
through the Deser–Levin combination T_eff = (ħ/2πck_B)√(a² + (cH)²) (Link 2).

What the banked chord dictionary **supplies**: λ↔H (geometry/scale), the center placement ↔
the GH state (which is the **a=0 free-faller / static patch**), and m²=4Δ(1−Δ).

What it **does NOT supply**: (i) the proper acceleration `a` of a non-inertial sub-horizon
detector; (ii) the Deser–Levin combination √(a²+(cH)²); (iii) the khronon sound speed c_chi
(the floor a* sector). All three are *absent from the banked dictionary*.

Consequence, machine-confirmed: a0 = cH/Z requires the a-sector AND the c_chi-sector, **both
entirely outside the chord dictionary**. No algebra-internal number fixes a0's scale or the
coefficient Z. **The route does NOT derive a0 — it reproduces Link-1 objects (T_dS, the QNM
ladder, the dS mass) that are already banked semiclassically.** This is the exact signature of
a STRUCTURAL, not derivational, bridge.

**Even weaker than its own companion route.** ROUTE 1 (agentWW_routeModular) proved the genuine
structural identity T_modular = T_DL = √(a²+H²)/2π *exactly on the whole a∈(0,∞) family* — that
reaches Link 2 (the full Deser–Levin temperature) and still correctly self-grades STRUCTURAL
because `a` is an INPUT. ROUTE 2 (DSSYK) reaches **only Link 1** (a=0 GH state + the H-scale); it
does not even reproduce the Deser–Levin √(a²+H²) combination, let alone derive a0. So the DSSYK
route's structural reach is a *strict subset* of the modular route's, and neither derives a0.

---

## 3. Does the bridge secretly depend on the unproven phi? — YES, on the framework side.

The route's own ledger is honest and survives scrutiny. Split confirmed:

- **phi-INDEPENDENT (stands alone, real math about DSSYK + its own limit):** [A] q-Hermite→Hermite
  q→1; [E] S_dS~1/λ~1/G_N; [B] QNM spacing=λ↔H; [C] m²=4Δ(1−Δ). These establish only that
  **DSSYK has A semiclassical dS limit carrying Link-1 objects.** No framework content.
- **NEEDS phi (UU's unproven state-level *-isomorphism, chord-vacuum ↔ GH cyclic-separating
  vector):** that DSSYK's dS IS the *framework's* a0-bearing cosmological-horizon dS; the center
  placement (⇒ the MOND sign); and ANY tie to a0/inertia — the last absent **even with phi**
  (a and c_chi are intrinsic to the acceleration/khronon sectors DSSYK never touches).

So the structural identity, **as a statement about the framework**, is conditional on phi —
type-compatible (both type II_1: Xu 2403.09021, CLPW 2206.10780) but unproven, and the placement
is agentR CONTESTED-TERMINAL / GATE-UNMOVED (no published paper derives θ_vac; sweep through
2026-06-10). The route states this in both directions; I find no overclaim.

---

## 4. Smuggle checks (maximum hostility)

1. **Did "q = temperature" smuggle a derivation?** No — the route itself flags this as a TYPE
   ERROR and splits it correctly: λ is the coupling (~G_N), T_dS=H/2π is the modular temperature
   of the E=0 center STATE. No temperature is *derived from* the algebra; H is an input (the dS
   radius). Confirmed in Block E.
2. **Did the MOND sign p=1/2 get asserted as a forced prediction?** No — it is explicitly a 1:1
   readout of θ_vac (center→1/2, edge→3/5), and the algebra supplies both. Placement-conditional,
   not algebra-forced. Confirmed in Block G.
3. **Coefficient quarantine.** q=1/4, Z, the coefficient: never asserted anywhere in the route.
   Verified by inspection of the memo. HELD.
4. **Was the q-QNM "new prediction" inflated?** No — the route reports it ~1e-122 invisible and
   placement-conditional, i.e. effectively NO checkable new prediction. Confirmed in Block H.
5. **Both-ways honesty.** The route reports the q→1 reduction as REAL *and* its
   framework-identification as UNPROVEN; no manufactured win, no reflexive dismissal.

No smuggle found. The route did not let the beautiful structural identity inflate into a derivation.

---

## 5. REGRADE: **CONFIRMED — STRUCTURAL-BRIDGE**

The route's verdict is correct and, if anything, slightly *generous to itself in reach* (it
reaches Link 1 only, not even Link 2's Deser–Levin combination — weaker than the companion
modular route, which the DSSYK route correctly does not claim to match). Every load-bearing
number reproduces independently; the one arXiv pin is accurate.

- **Genuine structural content (real, bankable, phi-independent at the DSSYK level):** DSSYK is a
  concrete 1d quantum-mechanical model whose q→1 (λ→0) limit reduces to a semiclassical dS
  structure carrying the framework's **Link-1** objects — T_dS, the QNM ladder spacing = H, the
  dS mass m²=4Δ(1−Δ). The q-Hermite→Hermite reduction is a standard, phi-independent identity.
- **NOT derivational:** no a0 (a and c_chi both absent from the dictionary), the MOND sign is a
  placement-conditional dictionary readout, and the only new output is ~1e-122 invisible. The
  bridge re-expresses Link 1; it does NOT close Link 4 (the coefficient) or supply the MOND
  mechanism, and it stalls before Links 2–3 (the acceleration/MOND content).
- **Framework side is phi-conditional:** the identification of DSSYK's dS with the framework's
  a0-bearing horizon, and the center placement, is exactly UU's unproven phi (type-compatible,
  placement CONTESTED-TERMINAL).

The honest ceiling — STRUCTURAL-BRIDGE — is exactly where the route landed. No inflation to
derivation; no derivation was available. **CONFIRMED.**
