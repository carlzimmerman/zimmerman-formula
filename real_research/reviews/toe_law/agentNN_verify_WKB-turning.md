# agentNN VERIFY — hostile referee of Route WKB / Langer turning point

Date 2026-06-13. Referee mission: is the claimed index-1/3 Airy structure REAL and
PUMP-SPECIFIC, or is it the FREE turning point agentMM (fb0ff706) already killed
(simple-pole / Rayleigh–Jeans, slope −1), smuggled back in? Default skepticism: assume the
Airy was wished into existence until the pump-specific mechanism is shown explicitly.

Independent re-derivation by a DIFFERENT method than the route's hand argument. Code:
`agentNN_verify_WKB-turning.py` (V1–V4), `_V5.py` (kill test), `_V6.py` (smuggle guard).
The route (`agentNN_routeWKB.md`) saved NO code — fully reproduced here from scratch.

---

## V1 — free Poschl–Teller turning-point ORDER (independent sympy series)

V(ξ)=s(s−1)κ²/(4 sinh²ξ), s=2. Solved V(ξ*)=ν² and differentiated:
**(V−ν²)′(ξ*) = −2√3 ≠ 0** (machine, exact). A SIMPLE zero ⇒ LINEAR turning point IS present
in the FREE khronon. CONFIRMS the route's STEP-1 claim. (Note: the √3 surfaces here too — the
same √3 that LL ties to index 1/3 — but here it is just the slope at the turning point, not yet
a connection index.) This "looks like an MM contradiction" only until the GLOBAL connection (V2).

## V2 — GLOBAL connection across the symmetric barrier = THERMAL (index 1). MM reproduced.

Exact Poschl–Teller S-matrix factor |Γ(iν/κ)|² verified against π/(ν sinh(πν/κ)) to **ratio
1.0000000000** at ν=5,20,80 (independent of the route's hand-quote). Exponential decay rate
d/dν log|Γ|² → **−π** (machine: −3.19, −3.15, −3.145, −3.1424 → −π) = KMS/Boltzmann thermal
tail, **index 1, NOT 1/3.** The single linear turning point's local Airy is washed into a
Boltzmann tail by the two-sided KMS-symmetric barrier. **This EQUALS MM's free kill (slope −1 /
simple pole / Rayleigh–Jeans). NO contradiction with MM — the free linear turning point gives a
THERMAL, not an Airy, spectral edge.** Independently confirmed.

## V3 — generalized turning-point index law m/(m+2), re-derived from the phase integral

Saddle of the connection integral for a turning point of order m: action ~ W^{(m+2)/m},
spectral index m/(m+2). Machine table: m=1→1/3, 2→1/2, 3→3/5, 4→2/3. **m=1 (linear) ⇒ index
1/3.** CONFIRMS the route's table by an independent saddle computation.

## V4 — q=1/4 ⟺ index 1/3 conversion (independent sympy saddle)

Edge measure e^{−g x^{−q}} with κ~x^{−1/2}, τ~x^{1/2}, Laplace in w: saddle of −g t^{−2q}−wt gives
transform index = **2q/(2q+1)** (sympy-exact). Table q={1/8,1/6,1/4,1/2,1} → index
{1/5,1/4,**1/3**,1/2,2/3}; **q=1/4 ⟺ index 1/3 exactly.** CONFIRMS LL's conversion theorem and
the route's exact rational chain by an independent derivation.

## V5 — THE KILL TEST: is the free-vs-pump distinction load-bearing, or relabeling?

**Q3 (decisive).** Free khronon dispersion ω=c_χ k ⇒ group velocity dω/dk = **c_χ = const,
NEVER zero**. No turning-point degeneracy, NO fold in the free theory. At the edge b→c_χ (c_χ>1,
agentU corner): amplitude A(b)~1/(c_χ²−b²) is a SIMPLE POLE (q=0, slope −1, MM-1); κ(b)=H/√(1−b²)
is FINITE at b=c_χ>1 (1−c_χ²<0) — no vanishing scale, no softening. **The FREE theory has NO soft
fold and NO x^{−1/4} branch — CONFIRMS MM.**

**Q3b.** A genuine fold (vanishing group velocity) requires a NEW dispersion term. Test
ω²=c_χ²k²−αk⁴: vg=0 has a REAL root k*=√2 c_χ/(2√α). The k⁴ term is a HIGHER-DERIVATIVE /
DISPERSION modification of the EOM — **DYNAMICS, not a state and not a constant gain.** The HH
pump's Ω²=c²(1+f)+ĝ′−ĝ² carries w-dependent f,ĝ that CAN supply an effective dispersive
correction; the free khronon cannot. **The named input is a dispersion modification, genuinely
absent from the free operator.** The free-vs-pump distinction is LOAD-BEARING, not a relabel.

## V6 — smuggle guard + internal-consistency audit

**(A) The route's "z(w)~w^{2/3}" WKB gloss is LOOSE.** Naive Airy bookkeeping (decaying partner
exp(−(2/3)z^{3/2}), z~w^a, index 1/3) gives a=2/9, not 2/3. So the route's O2 phrasing
"z(w)~w^{2/3}" is NOT the correct Airy-3/2 power bookkeeping — it is a heuristic mislabel. **But
it is NOT load-bearing:** the verdict rests on V1/V2 (free=thermal), V4 (q=1/4⟺1/3, sympy-exact),
V5 (free has no fold; k⁴ does) — the "z~w^{2/3}" line appears in none of them. Cosmetic prose
slip, no verdict impact. (LL-2's actual path to index 1/3 is the negative-argument *oscillatory*
Airy connection, index 1/3 in its own argument — correct; the route just glossed it loosely.)

**(B) SMUGGLE GUARD — q=1/4 is NOT auto-forced by "add a fold."** Build the fold action from
ω²=c_χ²k²−αk⁴: barrier top ω²_max=c_χ⁴/(4α). If the new-dispersion scale α~(c_χ−b)^β at the edge,
the fold edge measure gives **q = 3β/4**, so **q=1/4 requires β=1/3 specifically** (machine table:
β=1/3→q=1/4→index 1/3; β=1/2→q=3/8→index 3/7; β=1→index 3/5). A generic fold does NOT land on
q=1/4. **The route correctly leaves DERIVING ρ(b) (confirming q=1/4) as the OPEN next_calc — no
fourth-root is smuggled-closed.** This is the honest posture.

---

## REFEREE VERDICT

**The Airy is NOT the free turning point relabeled.** The free Poschl–Teller turning point IS
linear (V1) but its GLOBAL connection is the Γ-function THERMAL S-matrix (V2: rate→−π, index 1,
slope −1) = exactly MM's free kill, reproduced by an independent method. The index-1/3 / Airy
normal form is gated behind a NAMED, UNBANKED input: a vanishing-sonic-edge-group-velocity FOLD,
i.e. a soft/nonlinear DISPERSION term (k⁴-type) genuinely absent from the free khronon (V5). Even
granting the fold, q=1/4 is not automatic — it requires the dispersion to soften with a specific
edge exponent, left correctly OPEN (V6-B). **The free-vs-pump distinction HOLDS; the route does
NOT contradict MM — it re-derives MM in the free sector and isolates a dynamical input for the
rest.**

- recompute_agrees: **yes** — every load-bearing object (linear t.p., thermal global connection,
  m/(m+2) law, q=1/4⟺1/3, free constant group velocity, fold needs k⁴ dispersion) reproduced
  independently; the Γ-function S-matrix matched to ratio 1.0000000000.
- One LOOSE spot found and graded: the "z~w^{2/3}" WKB phrasing is an internally-inconsistent
  heuristic (should be a=2/9 by Airy bookkeeping), but it is NON-load-bearing prose; no verdict
  impact. This is the only blemish — it does not rise to a downgrade because the machine-proven
  chain (V4) carries the index-1/3 result without it.
- free_vs_pump_distinction_holds: **YES.** The free group velocity is constant (no fold); a fold
  requires a new dispersion term = dynamics the free operator lacks. Not the MM turning point.

**REGRADE: CONFIRMED. Regraded verdict: DIRECTION-NARROWED** (unchanged). The route honestly
reproduces MM's free kill and isolates a concrete, named, unbanked dynamical input (soft khronon
dispersion / vanishing sonic-edge group velocity producing a symmetry-broken fold caustic), with
the q=1/4 confirmation correctly left as an open forward calculation. No Airy was wished into
existence; no fourth-root smuggled. Coefficient quarantine intact (ζ̃, (16π/3)^{1/4} never used;
all numbers raw; q=1/4↔index 1/3 is a class/exponent REQUIREMENT-MATCH, no Z claim).
