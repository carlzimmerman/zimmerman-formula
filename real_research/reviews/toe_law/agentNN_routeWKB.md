# agentNN — ROUTE 1: WKB / Langer turning point on the khronon mode equation

Date 2026-06-13. Question (Link-5 generator, Route WKB): cast the khronon mode equation as a
Schrödinger problem −ψ'' + V(x)ψ = 0; locate V's turning point as the worldline rapidity → sound
edge b → c_χ (the SONIC horizon). Is V LINEAR there (Langer–Airy, connection index 1/3) or another
class? FREE first (MM commit fb0ff706 says the free/generic pump operator lands NON-Airy:
simple-pole / Rayleigh–Jeans, slope −1 not −1/4). Then: what does the ACTIVE PUMP add to V near
the turning point that the free operator lacks?

Read inputs:
- agentEE STEP 1–3: khronon modes are MINKOWSKI-form (1206.1083), φ(w)=w·e^{icw}, w=k|η|;
  dispersion ω=c_χ k; b-family pullback W_b(τ)=−H²/[16π²c_χ(c_χ²−b²) sinh²(κτ/2)], κ²=H²/(1−b²),
  b=a/κ; family edge at b→c_χ; free cut tail ≡ 0 (pure conformal/DL sinh⁻², KMS at κ/2π).
- agentLL LL-2: fingerprint = Laplace image of NEGATIVE-argument Airy density (oscillatory, index
  1/3, √3 lock = Airy connection formula Ai(−z)=e^{iπ/3}Ai(e^{iπ/3}z)+c.c.). Airy = universal WKB
  connection across a LINEAR turning point.

STANDING KILL TO BEAT (MM): generic turning point already in the free theory CANNOT be the answer.

---

## COMPUTE LOG (incremental)

### STEP 1–3 RESULTS (free khronon, Schrödinger form)

**Schrödinger cast.** The khronon free modes are Minkowski-form (no BD dressing). The worldline
pullback on the b-family is the conformal/Deser–Levin kernel W_b(τ) ∝ 1/sinh²(κτ/2). The reduced
radial sound-mode equation whose retarded kernel carries this is the **hyperbolic Pöschl–Teller**
problem at worldline frequency ν:

    −ψ'' + V(ξ)ψ = ν²ψ,   V(ξ) = s(s−1)κ²/(4 sinh²ξ),   ξ = κx/2,   s=2 (conformal khronon).

**Turning-point ORDER (free).** V'(ξ) = −s(s−1)κ²cosh ξ/(2 sinh³ξ) ≠ 0 at any finite ξ*>0 ⇒ the
turning point V(ξ*)=ν² is a **SIMPLE zero ⇒ LINEAR turning point ⇒ LOCALLY Airy** (Langer index
1/3). *A linear turning point IS present in the free khronon.* This looks like an MM contradiction.

**Reconciliation with MM (decisive).** The single linear turning point's local Airy is WASHED OUT
by the symmetric two-sided 1/sinh² barrier. The GLOBAL connection across the full Pöschl–Teller
barrier is the Γ-function thermal S-matrix: |Γ(iν/κ)|² = π/(ν sinh(πν/κ)), whose tail is
d/dν log = −π/κ ⇒ **index 1 (thermal/Planck/Rayleigh–Jeans), NOT index 1/3.** Machine-confirmed.
This is precisely MM's non-Airy free result (slope wrong): the free edge is thermal because the
turning point sits inside a KMS-symmetric double barrier, so its Airy oscillation cancels into a
Boltzmann tail. **NO contradiction with MM — the free linear turning point gives a thermal, not an
Airy, spectral edge.**

### STEP 4–7 RESULTS (the index-1/3 condition and what the pump must add)

**The generalized turning-point index law (machine, m/(m+2)).** A turning point of order m
(V−E ~ |x−x*|^m) has connection-function spectral index m/(m+2): m=1→1/3, m=2→1/2, m=3→3/5, m=4→2/3.
So **index 1/3 IS the signature of a LINEAR (m=1) turning point** — but ONLY in its OWN local Airy
argument z. LL-2's negative-argument-Airy density (index 1/3) reproduced cleanly: the exact envelope
2·3^{1/3}e^{−(1/2)w^{1/3}}cos(...) has fitted spectral index → 0.3333333333 as w→∞ (target 1/3).

**Why the free linear turning point does NOT deliver index 1/3 (two obstructions).**
- (O1) **KMS mirror symmetry.** The free 1/sinh² barrier is two-sided; the two mirror turning
  points' Airy oscillations combine into the Γ-function thermal S-matrix (|Γ(iν/κ)|², index 1).
- (O2) **Argument map.** The Airy argument z must scale as z(w) ~ w^{2/3} for index 1/3 to appear
  in the spectral variable w. The free thermal barrier has z(w) ~ w (linear) ⇒ Airy washed into a
  Boltzmann tail. The turning point's local energy scale must SOFTEN as w^{2/3}.

**Generic gain pump is NOT enough (ruthless, MM-consistent).** A constant/smooth anti-damping term
V → V − ig breaks KMS time-reversal and can defeat (O1) — decouple the mirror, leave one turning
point. But it does NOT move x*(w) or soften V'(x*), so it does NOT defeat (O2): z(w) stays ~w,
the tail stays thermal (index 1). **A generic pump lands non-Airy — independently re-derives MM.**

**The free edge measure is a SIMPLE POLE (MM's slope −1, reproduced).** The b-family amplitude
A(b) = H²/[16π²c_χ(c_χ²−b²)] ~ 1/(c_χ−b) at the sonic edge: a simple pole, q=0, power-law family-
Laplace image (Rayleigh–Jeans, slope −1). Exactly MM's free/generic-pump kill.

**The exact exponent chain that DOES give index 1/3 (machine, all rational).** Target edge measure
ρ_req(b) ~ e^{−γ(c_χ−b)^{−1/4}} (q=1/4). With κ(b) ~ (c_χ−b)^{−1/2} (Deser–Levin, LL S4b) and
τ ~ 1/κ: edge weight → worldline weight e^{−γτ^{−1/2}} (inverse-sqrt branch, p=1/2) → Laplace
saddle index p/(p+1) = 1/3. **Chain closes exactly.** Independently: 2q/(2q+1)=1/3 ⇒ q=1/4 (machine).

### VERDICT (Route WKB / Langer turning point)

**turning_point_class (computed): LINEAR turning point IS present in the free khronon (Pöschl–Teller
1/sinh² barrier, simple zero of V−ν²), but it delivers a THERMAL (index-1) spectral edge, not Airy,
because of two obstructions — KMS mirror symmetry (O1) and a linear argument map z(w)~w (O2). The
sonic-edge family measure is a SIMPLE POLE 1/(c_χ−b) (q=0). So the FREE edge class is
simple-pole/Rayleigh–Jeans (index 1 thermal / slope −1), reproducing MM. The index-1/3 Airy normal
form is NOT realized by the free operator.**

**airy_available: only-with-named-extra.** A linear turning point is necessary for index 1/3 and IS
structurally present — but the Airy is BLOCKED in the free theory. It becomes available ONLY if the
active pump supplies a specific, named modification (below). A generic/constant gain does NOT suffice.

**what_pump_must_add (mandatory, concrete):** The pump must convert the simple sonic-edge pole
1/(c_χ−b) into a FOURTH-ROOT essential singularity e^{−γ(c_χ−b)^{−1/4}} (q=1/4) in the family edge
measure ρ(b). In WKB/turning-point language this means: (1) BREAK the KMS mirror symmetry so a SINGLE
turning point's Airy survives uncancelled (defeats O1 — a gain/anti-damping term does this); AND,
decisively, (2) make the turning point a FOLD CAUSTIC pinned at the sonic edge — i.e. give the
khronon a NONLINEAR (soft) DISPERSION near the sonic point so the group velocity vanishes like
(c_χ−b)^{1/2}, softening the turning-point energy scale as z(w)~w^{2/3} and making the WKB action
develop a (c_χ−b)^{−1/4} branch (defeats O2). This is a modification of the DISPERSION RELATION
(dynamics), not a state and not a constant gain. It is the named unbanked input — the same place
MM/LL relocated the answer (the pump's own fluctuation kernel Ψ must carry the fold/Airy ramp). The
free operator has only a simple linear turning point inside a symmetric thermal barrier and provably
cannot supply the fourth-root fold by itself.

**verdict: DIRECTION-NARROWED.** The WKB route does NOT independently force the fourth-root edge (MM's
kill survives, fully reproduced: free = thermal/simple-pole). But it converts the requirement into a
precise, named WKB object: the pump must produce a symmetry-broken FOLD CAUSTIC at the sonic horizon
with a (c_χ−b)^{−1/4} action branch (equivalently a soft/nonlinear khronon dispersion with vanishing
sonic-edge group velocity). This is a concrete dynamical mechanism to test, not a free turning point.

**Coefficient quarantine intact:** ζ̃, (16π/3)^{1/4} never used; q=1/4 ↔ index 1/3 is a
class/exponent statement (REQUIREMENT-MATCH), no Z claim, no coefficient computed.
