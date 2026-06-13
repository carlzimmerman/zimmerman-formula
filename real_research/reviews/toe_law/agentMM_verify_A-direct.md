# agentMM — HOSTILE REFEREE of ROUTE A-direct: independent recompute + smuggle ledger + regrade

**STATUS: COMPLETE (compute-first; appended after every result).**
Date: 2026-06-12. Repo: zimmerman-formula. Local sympy/mpmath, dps 40-50.
Role: hostile referee. Default to skepticism — if the fourth-root "emerged", assume smuggled until proven otherwise.
Machine record (this run): `/tmp/agentMM_referee1b.py`, `/tmp/agentMM_referee2.py`, `/tmp/agentMM_referee3.py`,
`/tmp/agentMM_referee4b.py`, `/tmp/agentMM_referee5.py`, `/tmp/agentMM_referee6.py`. All exit 0.

DISCIPLINE: zeta-tilde and (16pi/3)^(1/4) QUARANTINED as input. No re-derivation as Z. Pure numbers RAW.
Both-ways: the KILL of the fourth-root is verified as hard as a pass would be; framework-favorable territory
gets MAXIMUM hostility AND no manufactured kill.

Route A's claim under audit: `carries_fourth_root: no`, `verdict: OBSTRUCTED`. The bulk pumped khronon mode
on the Deser-Levin b-family gives a SIMPLE POLE amplitude / Watson power-law response at b->c_chi, NOT a
fourth-root. The fourth-root is FREE input (neither forced nor forbidden), returning only if the pump is
HANDED the locked Gevrey-3 pair.

---

## (1) INDEPENDENT RECOMPUTE — different method than the memo (which did series-first)

I re-derived each load-bearing object by an independent method (root-multiplicity / direct-limit / forward
numeric fit) so a transcription error in the memo's series expansion cannot propagate into my agreement.

**[R1] kappa(b) is FORCED, re-derived by SOLVING the Hadamard normalization (not assuming).**
Setting the tau->0 leading coefficient of W_b(tau) equal to the universal Hadamard -1/(4 pi^2 tau^2) and
solving for kappa returns kappa(b) = H/sqrt(c_chi(c_chi^2 - b^2)); residual of the claimed form is exactly 0
(`referee1b`). FORCED, not free — agrees with the memo. (Caveat carried forward: this is a reconstruction
from the normalization, not an independent banked kappa(b); robust to the pole/Watson classes per LL S4e.)

**[R2] AMPLITUDE edge = SIMPLE POLE, by root-multiplicity (independent of series order).**
1/A = 16 pi^2 c_chi (c_chi^2 - b^2)/H^2. The zero of (c_chi^2 - b^2) at b=c_chi has multiplicity exactly 1
(differentiate-and-evaluate test) => A has a first-order pole. `sympy.residue(A,b,c_chi) = -H^2/(32 pi^2 c_chi^2)`.
Laurent in x=c_chi-b: leading term H^2/(32 pi^2 c_chi^2) * x^(-1) — an INTEGER pole, **no x^(-1/4), no
essential singularity** (`referee1b`). AGREES with the memo exactly (amplitude residue, simple pole).

**[R3] RESPONSE pole CANCELS, by DIRECT LIMIT (not series).**
(c_chi^2 - b^2)^(-1) * kappa(b)^(-2) = c_chi/H^2 exactly; `limit(b->c_chi) = c_chi/H^2` finite (`referee2`).
The state-amplitude pole is annihilated by the 1/kappa^2 response prefactor. AGREES with the memo.

**[R4] Surviving edge EXPONENT vanishes like sqrt(x); FREE response = WATSON POWER LAW.**
rate = sqrt(c_chi(c_chi^2-b^2)) = sqrt(2) c_chi^(3/2) sqrt(x) + O(x^(3/2)) -> 0 like sqrt(x). Unfolding with
the Watson/Laplace endpoint int_0^inf y^sigma e^{-A w y} dy = Gamma(sigma+1)/(Aw)^(sigma+1) gives a PURE
POWER LAW w^(-(sigma+1)) for any analytic measure (`referee2`). No exp(-c w^(1/3)). AGREES with the memo.

**[R5] FORWARD edge-exponent fit, GENERIC analytic pump — THE CRUX (independent build).**
I fed ONLY a generic structureless analytic pump (cos·gaussian + Lorentzian, zero Gevrey-3 / cube-root /
handed content) into the c_chi>1 corner (c_chi=1.3, agentU's corner) and measured the local log-log slope of
the response edge as eps=c_chi-b -> 0:
  eps=1e-3 -> -1.064 ; 1e-5 -> -1.0007 ; 1e-6 -> -1.00007 ; 1e-8 -> -1.0000007 ; 1e-10 -> -1.0
**Slope -> -1.0 = SIMPLE POLE.** NOT -1/4. (`referee3`.) This reproduces the memo's -0.999994 by a fresh
independent build and is the load-bearing kill: the bulk pump does NOT output a fourth-root.

**INDEPENDENT-RECOMPUTE VERDICT: AGREES.** Every load-bearing object reproduces by a different method:
kappa forced, amplitude simple-pole, response pole-cancelled, free edge Watson power law, forward generic-pump
edge slope -1 (not -1/4). The fourth-root does not emerge from Route A's bulk dynamics.

## (1b) BOTH-WAYS — the kill is not an anti-framework reflex (verified as hard as a pass)

**[R6] HANDED Gevrey-3 pump -> the cube-root/fourth-root RETURNS (clean, exact constant).**
Feeding the pump the locked pair e^{2 ctil e^{+-2pi i/3}(z)^{1/3}} (z=omega/kappa), the clean signature
log|G|/z^(1/3) -> -1.0 = 2 ctil cos(2pi/3) EXACTLY (converges 1e3->1e12: -0.944, -1.011, -0.997, -0.9994,
-1.00003) (`referee4b`). So the handed pump CARRIES the cube-root (= fourth-root x^(-1/4) in the b-edge after
the DL kappa~x^(-1/2) sqrt-map). The same test on the GENERIC pump -> ratio -> 0 (no cube-root). **Both-ways
confirmed: the fingerprint is present IFF the pump is HANDED the locked pair — it is INPUT, not output.**
ctil used as a RAW placeholder (=1.0) purely to read the cube-root EXPONENT structure; no Z claim, no
quarantine breach (the value of ctil is never asserted; only that the handed input REPRODUCES its own input).

**[R7] STEELMAN at the c_chi=1 conformal anchor — the one place a fourth root could live — STILL power law.**
At c_chi=1 the response pole cancels to the constant 1/H^2 (`referee5`, exact). The single most dangerous
smuggle was to set u=2pi/kappa ~ sqrt(c_chi-b) and DECLARE the edge u^(-1/2) = fourth-root class q=1/4. I
built the forward generic-pump response density there and measured its edge slope:
  eps=1e-3 -> -0.039 ; 1e-5 -> -0.0004 ; 1e-7 -> -4e-6 ; 1e-9 -> -4e-8  => **slope -> 0 (REGULAR power law).**
And numerically u/sqrt(x) -> 8.8857 constant: u DOES vanish like sqrt(x) (the DL map is genuinely a square
root), but a regular edge variable VANISHING like sqrt(x) is NOT a u^(-1/2) ESSENTIAL SINGULARITY of the
density. Declaring it so would have been the S2/S5 cheat. The actual generic-pump density at the anchor is
regular. **The steelman fails to produce the fourth root — the memo's refusal is vindicated.**

---

## (2) FIREWALL SMUGGLE LEDGER — L0-L8 run line-by-line on Route A

**L0 — Provenance ledger. PASS (zero [TARGET] inputs).**
Route A's inputs: HH [1a] scale-invariant pump ODE [PUMP]; EE [2c] Deser-Levin b-family + kappa(b) [GEOM];
the bulk state Psi (EE 2.3) [GEOM/PUMP]; for the forward fit, a GENERIC structureless analytic pump [PUMP,
target-blind]. NO sigma_req, NO F_req, NO q=1/4 ansatz, NO fourth-root, NO gamma_req, NO zeta-tilde fed into
the forward computation. The locked F_req / handed pair appears ONLY in the explicitly-flagged HANDED
both-ways check [R6], labelled INPUT, never used to source the verdict.

**L1 — Forward direction. PASS.** The computation runs pump -> edge measure -> (DL map, once) -> index.
There is NO arrow from the target back into the edge measure: the slope -1 ([R5]) and slope 0 ([R7]) were
obtained WITHOUT consulting index 1/3 or solving 2q/(2q+1)=1/3. The map theorems [referee6] are recomputed
only AFTER, as discovered coincidences.

**L2 — Edge exponent computed, not assumed. PASS.** q never appears as a free symbol pinned by matching.
The edge exponent came out as the OUTPUT of the forward fit: -1 (pole) for generic pump, 0 (regular) at the
anchor. The discovered-coincidence check (2q/(2q+1)=1/3 has unique root q=1/4, strictly monotone, `referee6`)
is run afterward and confirms that IF a 1/4 edge existed it would map to 1/3 — but Route A did not produce a
1/4 edge, so this check is informational only. **S2 and S8 do NOT fire.**

**L3 — Geometry used once, as banked. PASS (with the standing caveat).** kappa(b)=H/sqrt(c_chi(c_chi^2-b^2))
re-derived by SOLVING the Hadamard norm [R1], applied exactly once as the DL sqrt-map. u~sqrt(x) verified
numerically [R7]. No second square root smuggled into the parametrization. Caveat (logged, both in the memo
and here): kappa is a reconstruction, not an independently-banked read — but the pole/Watson classes are
robust to it. **S3 does NOT fire.**

**L4 — Oscillation is dynamical? N/A — no oscillation was produced.** Route A's generic-pump output is a
plain pole/power law with no cos(...) member. The memo did NOT hand-insert an oscillatory branch; it reported
the ABSENCE of one for the generic pump. The cube-root oscillation appears ONLY in the handed case [R6],
explicitly flagged as carried-by-input. **S9 does NOT fire** (no member was selected to match the fingerprint;
the oscillation was correctly attributed to the handed input, not the bulk dynamics).

**L5 — No boundary-condition flatness. PASS.** No flatness / all-moments-zero / C^infty-flat-at-lightcone /
"match sigma_req at the edge" condition is imposed. The only BC is the Hadamard short-distance norm (which
fixes kappa, a target-blind geometric object). **S1 does NOT fire.**

**L6 — Constants raw; zeta-tilde not claimed. PASS.** Route A reports NO gamma=gamma_req, NO zeta=(16pi/3)^(1/4)
as a result. Its gamma_status is explicitly "n/a — no fourth-root emerged, so no gamma coefficient is
produced"; the gamma_req value is quoted only as the QUARANTINED carryover that WOULD be needed, attributed
to sigma_req as INPUT. ctil in [R6] is a raw placeholder for reading exponent structure, never asserted as a
value. **S6 does NOT fire.**

**L7 — Legality reconciliation (the V-theorem gate). PASS / consistent.** Route A does NOT claim a
dS-invariant derivation of the fourth-root cut. It explicitly finds the bulk pump does NOT produce the cut
(OBSTRUCTED) — so there is no illegal structure smuggled past V's KL positivity wall. The fourth-root, when
present, is attributed to the HANDED invariance-breaking input (the locked Gevrey-3 pair carries the handing),
consistent with V's requirement that the cut live in an invariance-breaking sector. No INCONSISTENT condition
is triggered.

**L8 — Deep-MOND endpoint honesty. N/A / PASS.** Route A makes no claim to derive the exact deep-MOND sqrt(x)
onset from a convergent pump transform. It does not touch L8's failure condition.

**S5 — Inverse-image laundering (the headline failure mode). DOES NOT FIRE — and was actively refused.**
The correlator used in the forward fit traces to a GENERIC structureless pump, NOT to V's sigma_req inversion.
The memo's smuggle_audit explicitly identifies and refuses the laundering: "Second cheat avoided: feeding
HH's locked F_req profile ... and reading the fourth-root back out — pure transcription/inverse-image
laundering (S5); I used only a GENERIC structureless pump for the forward fit so -1/4 had no entry except by
being handed." My independent [R5]/[R7] confirm the generic pump gives -1/0, never -1/4 — so no sigma_req
trace entered. **S5 cleared.**

### Smuggle-vector tally
| # | Vector | Fires? |
|---|---|---|
| S1 | BC flatness | NO — only Hadamard norm BC (target-blind) |
| S2 | Ansatz x^(-q) | NO — q never an ansatz; slope was OUTPUT (-1/0) |
| S3 | Parametrization | NO — DL sqrt-map used once, as banked |
| S4 | Fit gamma to gamma_req | NO — no optimization against any target |
| S5 | Inverse-image laundering | NO — generic pump only; explicitly refused |
| S6 | Derive zeta-tilde | NO — gamma_status n/a; constants raw/quarantined |
| S7 | Map double-use | NO — map applied once at the end |
| S8 | Solve-for-q | NO — q not solved from index 1/3 |
| S9 | Member smuggle | NO — no oscillatory branch hand-selected |

**Did Route A assume q=1/4 anywhere? NO.** The forward fit produced -1 (pole) and 0 (regular) with q absent
from the inputs and intermediate steps; the value 1/4 enters Route A's writeup ONLY in the quarantined
description of what WOULD be needed (gamma_req / the handed F_req), explicitly labelled INPUT/carryover, never
as an output it claims.

---

## (3) REGRADE

**CONFIRMED.**

- Independent recompute AGREES: kappa forced (residual 0), amplitude simple pole (residue -H^2/(32 pi^2 c_chi^2),
  root-multiplicity 1), response pole cancels (limit c_chi/H^2), free edge Watson power law, and the crux
  forward generic-pump edge slope -> -1.0 (NOT -1/4) by an independent build.
- No smuggle survives: all of S1-S9 cleared; the two most dangerous vectors (S5 inverse-image laundering and
  the S2/S5 "u^(-1/2)=fourth-root" anchor cheat) were actively refused by the memo AND independently shown to
  fail [R5]/[R7] — the generic pump and the c_chi=1 steelman both give a regular power law, never the
  fourth-root.
- Both-ways integrity holds: the kill is NOT an anti-framework reflex — the handed pump cleanly reproduces the
  cube-root (-1.0 = 2 ctil cos(2pi/3), exact) [R6], so the fourth-root is genuinely FREE INPUT (neither forced
  nor forbidden by the bulk pump), exactly as Route A states.

The verdict OBSTRUCTED stands CONFIRMED: Route A's `carries_fourth_root: no` is correct, robustly, by an
independent method, with no q=1/4 assumed anywhere. The edge is FREE input — the bulk pump neither forces nor
forbids the fourth-root; it must be handed (HH's F_req / the locked Gevrey-3 pair), which is INPUT carried
over from sigma_req, not output by Route A. gamma_req, zeta-tilde, (16pi/3)^(1/4) remain QUARANTINED, never
re-derived.

**One honesty note (does NOT change the grade):** the standing caveat that kappa(b) is a reconstruction from
the short-distance normalization rather than an independently-banked read is real and carried by both the memo
and this referee. It does not affect the simple-pole or Watson classes (robust per LL S4e), and the forward
fit's -1 result does not depend on it. The grade is CONFIRMED, not DERIVATION — Route A is correctly a
NEGATIVE result (no fourth-root from the bulk), and the firewall's DERIVATION grade was never claimed.

## Files / repro
- This memo: `real_research/reviews/toe_law/agentMM_verify_A-direct.md`.
- Machine record: `/tmp/agentMM_referee1b.py` (kappa solve + pole order/residue), `/tmp/agentMM_referee2.py`
  (response pole-cancel by limit + Watson), `/tmp/agentMM_referee3.py` (forward generic-pump edge slope -1),
  `/tmp/agentMM_referee4b.py` (handed cube-root signature, both-ways), `/tmp/agentMM_referee5.py` (c_chi=1
  steelman -> regular power law), `/tmp/agentMM_referee6.py` (map anchors as discovered coincidences). All
  exit 0; every claim reproduced inline above.
