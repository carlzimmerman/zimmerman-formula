# agentMM — HOSTILE VERIFICATION of Route B (Resurgence / trans-series on the free pullback)

**Role.** Hostile referee. The Route-B derivation (agentMM_routeB.md) claims VERDICT = OBSTRUCTED,
carries_fourth_root = NO: the free pullback's large-order/Stokes data is THERMAL (double-pole Matsubara
tower, Gevrey ≤ 1, convergent in worldline time τ), which is the WRONG resurgence class to seed the
target fourth-root x^{-1/4} essential singularity (Gevrey-4 / coeffs ~ (4n)!).

**My job.** (1) Independently RE-COMPUTE the load-bearing step by a DIFFERENT method than the derivation
used. (2) Run the firewall smuggle checklist (S1–S9) line-by-line. (3) Regrade.

**The load-bearing step.** The verdict rests ENTIRELY on a resurgence-class statement:
> The free series sits in Gevrey class ≤ 1 (double-pole/linear Matsubara tower), which CANNOT
> generate, by alien calculus / Borel resummation through an analytic edge map, a Gevrey-4
> (fourth-root, x^{-1/4}) non-perturbative partner. Therefore resurgence on the free data does NOT
> force the fourth-root — it forces a thermal simple-exponential tower instead.

The derivation's method: read Borel singularities OFF the closed form (poles of 1/sinh²), then compare
Gevrey growth rates symbolically.

**My DIFFERENT method:** I will not read poles off the closed form. Instead I will
 (B1) take the ACTUAL Taylor coefficients of the free series, build the BOREL transform numerically,
      and LOCATE its singularity (radius + type) by ratio/Domb–Sykes — confirming pole vs branch
      INDEPENDENTLY of the closed-form factorization;
 (B2) directly construct the fourth-root partner series (coeffs of the asymptotic expansion of a
      function with a genuine x^{-1/4} essential edge) and measure ITS Gevrey order the same way,
      to verify the (4n)! ↔ x^{-1/4} dictionary the derivation asserts;
 (B3) test the decisive map-invariance claim numerically: push a linear simple-pole tower through the
      Deser–Levin analytic √-map and check the singularity TYPE does not upgrade to a quartic branch;
 (B4) cross-check the amplitude Laurent (simple pole) and the √x kinematic edge by an independent
      series route.

All numbers RAW. ζ̃ and (16π/3)^{1/4} QUARANTINED — used nowhere.

---
## PART 1 — INDEPENDENT RE-COMPUTE (different method; all RAW, machine-backed)

Scripts: /tmp/mm_verB1.py … /tmp/mm_verB4.py (rerun verbatim; sympy/mpmath, dps 40–60).

### B1 — Singularity TYPE from coefficient asymptotics (NOT from reading closed-form poles)
Method DIFFERENCE: routeB STEP 3 reads the double poles OFF `1/sinh²` at τ_m=2πim/κ. I instead took
the NUMERICAL Taylor coefficients of g(y)=1/sinh²(y)−1/y² and ran a Domb–Sykes ratio analysis in the
variable t=y², fitting r_j = a_j/a_{j-1} ≈ B + slope/j to extract the nearest singularity t_c=1/B and
the local exponent p.
- RESULT: t_c = −9.8746 vs −π² = −9.8696 (0.05% — nearest sing at y=iπ, the m=1 Matsubara point).
- Local exponent p = −2.03 → **−2: a DOUBLE POLE**, recovered with ZERO input from the closed form.
- => The free Borel/large-order singularity is a double pole at a FINITE, LINEARLY-spaced location.
  Independently reproduces routeB STEP 3 (double-pole Matsubara tower) by coefficient asymptotics alone.

### B2 — The (4n)! ↔ x^{-1/4} dictionary, verified by an independent Gevrey-order estimator
Method DIFFERENCE: routeB STEP 4 used |a_n|^{1/n}/n. I used L_n = log a_n /(n log n) → s for a_n~(s n)!
(isolates the factorial ORDER s, robust to subleading geometric factors).
- s=4 series: L_400 = 4.26 (→4, slow log-correction). s=2: 1.90 (→2). s=1: 0.83 (→1).
- FREE worldline-τ coeffs a_{2j}~(2j+1)·2/π^{2j+2}: L_n → NEGATIVE (−0.38 at j=400) ⇒ **Gevrey-0,
  CONVERGENT**, sub-geometric. Confirmed: target is Gevrey-4, free τ-series Gevrey-0 — DIFFERENT classes.
  The only factorial in the free problem (Bernoulli, the Borel image) is Gevrey-2 at most, never 4.

### B3 — Map-invariance of singularity TYPE (the DECISIVE / load-bearing claim), by composition
Method DIFFERENCE: routeB STEP 4b argued type-invariance verbally. I tested it CONSTRUCTIVELY: a free
pole tower has integer-power essential action E_free(u)~u^p (p = pole order, INTEGER); the banked
Deser–Levin map is u=√x; composition gives E_free(x)=x^{p/2} = HALF-INTEGER powers of x.
- Achievable x-powers: …, x^{-1}, x^{-1/2}, x^{1/2}, x^1, … — **x^{-1/4} is provably NOT in the set**
  (it needs p=−1/2, a half-integer pole order a Matsubara tower does not have).
- To force x^{-1/4} from an integer free action you need a FOURTH-root map u=x^{1/4}, NOT the banked
  √-map — and using x^{1/4} is firewall smuggle S3/S7. Numerically confirmed k=2→Gevrey-2, k=4→Gevrey-4.
- => The analytic √-map CANNOT upgrade a linear pole tower to a quartic branch. The √x (k=1/2) edge is
  reproduced. **Load-bearing OBSTRUCTION claim CONFIRMED by an independent composition test.**

### B4 — Independent cross-checks (sympy, exact)
- (B4a) Amplitude A(b) Laurent at b=c_χ: **SIMPLE POLE**, residue in x exactly H²/(32π²c_χ²) (match True,
  x·A finite & x²·A→0). Reproduces routeB STEP 1 and the edge-map simple-pole class.
- (B4b) Kinematic edge √(c_χ(c_χ²−b²)) = √2·c_χ·√x + O(x^{3/2}): **k=1/2 SQUARE-ROOT** (match True), not 1/4.
- (B4c) deep-MOND 2−t = 2a²/(H²+a²) Taylor at a=0 = 2a²/H² − 2a⁴/H⁴ + … : **analytic in a², geometric**;
  no √a onset (confirms firewall L8 / V no-kernel).
- (B4d) Index map 2q/(2q+1)=1/3 ⇒ unique root q=1/4; map strictly monotone (d/dq=2/(2q+1)²>0). Checked
  LAST as the discovered coincidence, NEVER fed as an input — as the firewall requires.

**PART-1 CONCLUSION.** Every load-bearing element of Route B reproduces by a genuinely different method:
the free Borel singularity is a double pole (B1, from coefficients), the free τ-series is Gevrey-0 while
the target is Gevrey-4 (B2), and the banked analytic √-map provably cannot manufacture the quarter-power
(B3). **My independent recompute AGREES: the free Stokes data does NOT carry / cannot seed a fourth-root.
carries_fourth_root = NO is CONFIRMED.**

---
## PART 2 — FIREWALL SMUGGLE CHECKLIST (S1–S9) run line-by-line on Route B

CONTEXT NOTE. Route B's CLAIM is OBSTRUCTED / carries_fourth_root=NO — it is a KILL of the free route,
not a derivation of q=1/4. The firewall's S-vectors are written to catch a FALSE-POSITIVE "derivation."
For a KILL, the dangerous failure mode INVERTS: a kill is illegitimate if it secretly USED the target
(q=1/4 / σ_req) as an INPUT to its OWN reasoning — i.e. if the obstruction is circular, or if the kill
is actually a disguised requirement-match that smuggled the target in to "find" the mismatch. So I run
each S-vector asking BOTH: (a) did it smuggle q=1/4 in as an OUTPUT it then claims to derive? and
(b) did it smuggle the target in as an INPUT that pre-determines the OBSTRUCTION verdict?

### L0 — PROVENANCE LEDGER (every input Route B consumed)
| input | origin | tag |
|---|---|---|
| W_b(τ) = −H²/[16π²c_χ(c_χ²−b²)sinh²(κτ/2)] | agentEE [2c], banked closed form | [PUMP]/[GEOM] |
| κ(b)=H/√(1−b²), b²=a²/(a²+H²), κ²=a²+H² | Deser–Levin geometry (EE) | [GEOM] |
| A(b)=H²/[16π²c_χ(c_χ²−b²)] | algebra of W_b | [PUMP]-derived |
| deep-MOND 2−t=2a²/(H²+a²) | banked kinematics | [GEOM] |
| Bernoulli/sinh⁻² Laurent coeffs | computed here from W_b | self-computed |
| Gevrey ↔ essential-sing dictionary | standard resurgence math (Costin/Dorigoni) | math fact |
| σ_req ~ u^{-13/8}e^{-ζu^{-1/4}}cos(...) | agentV TARGET | **[TARGET]** — used ONLY as comparison object |
**L0 verdict for a DERIVATION claim: would FAIL (one [TARGET] input).** BUT Route B does NOT claim a
derivation — it uses σ_req solely as the object to test the free data AGAINST, and computes the free
Gevrey class BEFORE the comparison. For an OBSTRUCTION claim the relevant test is whether the [TARGET]
leaked into the free computation. It did not (B1–B3 reproduce the free class with σ_req nowhere in them).

### S1 — BC smuggle (edge flatness imposed as a boundary condition?)
Route B imposes NO boundary/regularity/matching condition. It computes the Laurent and large-order
coefficients of the free W_b directly. No flatness, no all-moments-zero, no "match σ_req at u→0".
**S1 does NOT fire.**

### S2 — Ansatz smuggle (trial measure already contains x^{-q} / essential sing?)
The free series is the GIVEN W_b — no trial ρ(b)=exp(−γx^{-q})cos(...) is written. q never appears as a
free shape parameter. The fourth-root form appears ONLY in the σ_req line, labeled [TARGET]. **S2 does
NOT fire.** (My B1/B3 reproduce the type with no ansatz at all.)

### S3 — Parametrization smuggle (fourth-root only after a deriver-chosen variable change?)
The edge variable u=2π/κ is the banked Deser–Levin invariant, used ONCE. Route B explicitly REFUSES the
shortcut "u~√(c_χ−b) so x^{-1/4}↦u^{-1/2}" (its smuggle_audit names this as the cheat it avoided). B3
confirms: the √-map gives only half-integer x-powers; a fourth-root would need an un-banked x^{1/4} map.
**S3 does NOT fire** — and Route B's verdict turns on REFUSING exactly this move.

### S4 — Fit smuggle (γ/q/φ matched to γ_req / √3 / π/3?)
No optimization, no matching, no "choose constants such that". γ_status = n/a (no fourth-root emerged,
nothing fit). No reference to γ_req in any computation. **S4 does NOT fire.**

### S5 — Inverse-image laundering (correlator traces to V's σ_req, not a forward comp?)
THE HEADLINE FAILURE MODE. The correlator used IS the forward free pullback W_b from EE's construction,
NOT V's σ_req. σ_req enters only as the comparison target on the RHS of the Gevrey-class inequality. The
free coefficients (B1) come from W_b's own Taylor expansion — zero σ_req content. Route B's verdict is
that the free data does NOT reproduce σ_req — the OPPOSITE of laundering σ_req in as a pump output.
**S5 does NOT fire.** (Laundering would have produced a FALSE match; Route B produces a mismatch.)

### S6 — Constant smuggle (derived constant equals ζ̃ or (16π/3)^{1/4}?)
No constant is derived. ζ̃ and (16π/3)^{1/4} appear NOWHERE in the computation (grep-clean). The only
pure numbers reported (π, residues, ratios) are raw geometric/Bernoulli quantities. **S6 does NOT fire.**

### S7 — Map double-use / circularity (edge measure itself a product of the map / theorem⁻¹?)
The free edge data is computed from W_b BEFORE any map push-forward; the √-map type-invariance is tested
ONCE (B3). The obstruction is NOT "target→map⁻¹→required measure→map→mismatch" (that would be circular);
it is "free W_b coefficients → their own Gevrey class → compare to target class". No backward arrow from
the target into the free coefficients. **S7 does NOT fire.**

### S8 — Solve-for-q smuggle (q fixed by an equation referencing index 1/3?)
q is NEVER carried as a free symbol fixed at the end by the target. Route B does not "solve for q" at
all — it classifies the free Gevrey order (=0 in τ, ≤2 in Borel image) and observes it is ≠ 4. The
index-map root q=1/4 (B4d) is checked LAST, as the firewall mandates, as the discovered coincidence —
and it is used to LABEL the target, not to fix anything in the free computation. **S8 does NOT fire.**

### S9 — Member smuggle (oscillatory branch / phase hand-selected to match fingerprint?)
No oscillatory member is selected — none emerged (gamma_status=n/a). No cos(...) is inserted, no −π/4 or
+π/3 phase is borrowed. **S9 does NOT fire.**

**PART-2 RESULT: NONE of S1–S9 fire.** Route B did NOT assume q=1/4 — it computed the free Gevrey class
independently (B1–B3 reproduce this) and found it incompatible with the fourth-root. The single [TARGET]
input (σ_req) is used ONLY as a passive comparison object on the kill side, never fed into the free
computation that produces the obstruction. The kill is not circular and not a disguised requirement-match.

---
## PART 2b — HOSTILE 'hidden-variable' probe (could the kill be wrong?)

A KILL deserves the same hostility as a pass. The strongest way carries_fourth_root=NO could be WRONG:
a hidden (4n)! growth in some natural worldline variable the derivation skipped. Script /tmp/mm_verB5.py:
- (i) τ-series: Gevrey-0 (convergent). (ii) frequency/Bernoulli large-order: |B_2n|~(2n)!, **Gevrey-2**
  (estimator climbing through 1.19 at n=200 toward 2, NOT 4). (iii) b-amplitude: rational, poles only.
- Analytic reparametrization preserves positive radius ⇒ cannot manufacture (4n)! from a convergent
  series; only a different (PUMPED) EOM can. Max free Gevrey order = 2 across ALL natural variables.
- The (2n)!↔(4n)! gap is HARD: (4n)!/(2n)! = 8e493 at n=100, diverges super-exponentially — no subleading
  factor bridges the classes.
**The kill survives the hostile probe. carries_fourth_root=NO is robust, not an artifact.**

### Verdict-label consistency
Route B labels the result **OBSTRUCTED** (free Stokes data cannot seed the fourth-root), with
carries_fourth_root=NO and gamma_status=n/a. This is internally consistent: an obstruction is precisely
the finding that the free route forces NOTHING toward q=1/4 (neither a full nor partial derivation).
The honest residual — explicitly flagged in Route B's smuggle_audit and next_calc — is that a PUMPED EOM
has DIFFERENT Stokes data and COULD in principle be Gevrey-4; the free route simply does not dictate it.
That caveat does NOT overclaim: it is the correct scope statement (the obstruction is about the FREE
series only) and B5(iii) backs it (only a different EOM, not a reparametrization, can change the class).

---
## PART 3 — REGRADE

**Did the fourth-root "emerge"?** NO — and Route B never claimed it did. Route B is a KILL of the free
route: it claims the free Stokes data is in the WRONG resurgence class (Gevrey ≤ 2) to seed the
target fourth-root (Gevrey-4), so resurgence on the free data forces a THERMAL Matsubara tower, not a
fourth-root. My job was to default to skepticism that the fourth-root was smuggled — but there is no
fourth-root output here TO smuggle. The inverted risk for a kill (smuggling the target IN as an input to
manufacture the obstruction) was checked under every S-vector and does not occur.

**(1) Independent recompute AGREES.** By a genuinely different method than Route B used:
- B1 (Domb–Sykes on numerical coefficients, NOT closed-form poles): free singularity = double pole at
  y=iπ — reproduces the Matsubara/thermal class.
- B2 (log a_n/(n log n) Gevrey-order estimator, NOT |a_n|^{1/n}/n): target Gevrey-4, free τ-series
  Gevrey-0, distinct classes — reproduces the class mismatch.
- B3 (constructive composition test, NOT a verbal argument): the banked analytic √-map sends integer
  free actions to half-integer x-powers; x^{-1/4} is provably unreachable without an un-banked x^{1/4}
  map — reproduces the type-invariance / square-root-edge finding.
- B4 (exact sympy): simple pole at b=c_χ, √x kinematic edge, deep-MOND a²-analyticity, unique q=1/4 root.
- B5 (hostile hidden-variable probe): max free Gevrey order = 2 across all natural variables; kill robust.
All agree with Route B's computed claims.

**(2) Smuggle audit: NONE of S1–S9 fire.** Route B did NOT assume q=1/4. q never appears as a free shape
parameter, ansatz exponent, fitted knob, or solved-for symbol; the index-1/3↔q=1/4 root is checked LAST
as the discovered coincidence and used only to LABEL the target. The lone [TARGET] input (σ_req) is a
passive comparison object on the kill side and never enters the free computation (B1–B3 reproduce the
free class with σ_req absent). ζ̃ and (16π/3)^{1/4} appear only in the discipline/caveat lines, never as
computational inputs or derived outputs (grep-clean). Coefficient quarantine intact.

**(3) Grade.**
Route B's own stated verdict: **OBSTRUCTED**, carries_fourth_root=NO.

Against the firewall grading ladder (which grades DERIVATION attempts), Route B is not a derivation
attempt — it is a NEGATIVE result. The correct regrade of a KILL is whether the kill HOLDS and is clean:
- The kill HOLDS (independent recompute agrees, B1–B5).
- The kill is CLEAN (no smuggle survives; not circular; target not laundered in as input).
- The scope/caveat is honest (the obstruction is about the FREE series; a pumped EOM is left genuinely
  open, not falsely foreclosed and not falsely promised).

**REGRADE = CONFIRMED.** The independent recompute agrees AND no smuggle survives. Route B's OBSTRUCTED /
carries_fourth_root=NO is sustained at full strength. (regraded_verdict, in the schema's terms, = OBSTRUCTED.)

No downgrade is warranted: the claim is not stronger than what the disk supports — it is exactly a free-
level obstruction, correctly NOT presented as a derivation, with the pumped-EOM door left honestly open.
No overturn is warranted: nothing is wrong or smuggled.

### Files / repro
- This memo (incremental): real_research/reviews/toe_law/agentMM_verify_B-resurgence.md
- Independent scripts: /tmp/mm_verB1.py (Domb–Sykes), /tmp/mm_verB2.py (Gevrey-order dict),
  /tmp/mm_verB3.py (map-invariance composition), /tmp/mm_verB4.py (sympy cross-checks),
  /tmp/mm_verB5.py (hidden-variable hostile probe). Rerun verbatim; sympy/mpmath, dps 40–60.
- Audited derivation: agentMM_routeB.md + step1..6 scripts. Source closed form: agentEE_sigma_khronon.md [2c].
