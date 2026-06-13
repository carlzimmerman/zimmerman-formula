# agentPP VERIFY — hostile re-derivation of ROUTE 1 (QNM spectral moments): is the dS QNM response PEAKED or BROAD? (2026-06-13)

**Referee task.** Route qnm-moments claims: the dS QNM ladder (Gamma_n = sinh((Delta+n)lambda), purely
damped, Re omega=0) gives a BROAD multi-scale spectral response, CS = I2^2/(I1 I3) < 1 always, hence
sigma6 < 0 (UNBOUNDED), k* edge-unpinned. Verdict STILL-UNBOUNDED. This closes — or fails to close — the
framework's deepest gap (a controlled bounded roton fold). HOSTILE PRIOR per the brief: purely-damped
(Re omega=0) modes are zero-centered Lorentzians => BROAD, so a claimed finite-k PEAK must be EARNED, not
assumed. I must (1) re-derive peaked-vs-broad by a DIFFERENT method, (2) check the peak was real not smuggled,
(3) steelman a peak before confirming, (4) regrade.

**Coefficient quarantine.** Only SIGNS (sigma4, sigma6) and edge-pinning STRUCTURE. q=1/4 etc never asserted.

---

## Step 0 — independent re-derivation of the sigma6-sign criterion (NOT trusting PP's algebra)

Before scanning, I re-derive from scratch the map {spectral density rho} -> {sign of sigma6}, so I am not
inheriting PP's reduction "sigma6>0 iff I2^2 > I3 c_chi^2".

Solved the in-medium secular relation `omega^2 = c0^2 k^2 + k^2 Sigma(omega^2)`, `Sigma = -[I1 + omega^2 I2 +
omega^4 I3 + ...]`, order-by-order in k^2 (sympy, `pp_verify_step0.py`). Result, INDEPENDENTLY CONFIRMING PP:
```
c_chi^2 = c0^2 - I1
sigma4  = -I2 * c_chi^2                 (< 0 when c_chi^2>0  => BEND, matches OO+PP)
sigma6  = c_chi^2 (I2^2 - I3 c_chi^2)   => sigma6>0  iff  c_chi^2 < I2^2/I3
```
PP's algebra is correct. **BUT — the hostile catch (Step 0b/0c):** PP's headline order-parameter
`CS = I2^2/(I1 I3)` silently sets `c_chi^2 = I1` (i.e. `c0^2 = 2 I1`). The EXACT criterion is
`sigma6>0 iff c_chi^2 < I2^2/I3`, and `c_chi^2 = c0^2 - I1` depends on the FREE bare UV speed `c0^2` that
PP held FIXED. As `c0^2 -> I1+` (the sonic-edge limit `c_chi^2 -> 0`), `I2^2/(I3 c_chi^2) -> +inf > 1`, so
**sigma6>0 is reachable** — PP's "CS<1 => sigma6<0 => UNBOUNDED" is the WRONG reduction at fixed c0^2.
Worse: requiring a real finite-k dip-AND-rise in the truncated poly `c_chi^2 x + sigma4 x^2 + sigma6 x^3`
(x=k^2) opens a genuine window `(2/3) I2^2/I3 < c_chi^2 < I2^2/I3`, i.e. `c_chi^2/I1 in ((2/3)CS, CS)` —
NONEMPTY. So at the truncated-polynomial level there IS an apparent bounded roton. **This is the steelman
I had to chase to ground before confirming PP.**

## Step 1 — the steelman: PP's own ladder DOES give a truncated roton when c0^2 is scanned

`pp_verify_step1.py`, PP's exact ladder (Delta=0.5, q=0.7, decay=0.5, N=8, rungs x3; CS=0.9524). Scanning the
bare `c0^2` (which PP froze at 2.0 = `c_chi^2/I1 = 1.0`, just ABOVE the window) toward the sonic edge:
```
c_chi^2/I1   sigma4        sigma6        roton(trunc poly)?   k*^2
  1.00       -43.8 (<0)    -26.2 (<0)         no               --      <- PP's frozen point
  0.90       -39.4         +26.0 (>0)         YES             0.968
  0.80       -35.1         +67.2              YES             0.299
  0.70       -30.7         +97.3              YES             0.153
  0.65       -28.5        +108.3              YES             0.107
  0.60       -26.3        +116.5              no               --
```
So a window `c_chi^2/I1 in (0.635, 0.952)` gives sigma6>0 AND a truncated-poly roton dip. **PP missed this by
freezing c0^2.** If this survived, the verdict would flip toward FOLD. It does not — Step 2/3 kill it.

## Step 2-3 — the truncated roton is an IR-TRUNCATION ARTIFACT (full dispersion is monotone)

`pp_verify_step2.py`/`step3.py`: solve the FULL self-consistent secular relation
`x = c0^2 k^2 + k^2 sum_n w_n/(x - W_n^2)` (mpmath, dps=30-40, no k^6 truncation) for the lowest acoustic
branch, at `c0^2 = 1.9 I1` (squarely inside the window). RESULT: omega(k) is **MONOTONE** — no finite-k
minimum. The reason: the truncated roton sits at `k*^2 ~ 0.6-1.0`, i.e. `omega^2 ~ 1.98 ~ 7 * W_min^2`
(W_min^2 = 0.29) — FAR outside the IR radius of convergence (`omega^2 << W_min^2`), where the kept k^6 term is
NOT the leading correction. Scanning `c_chi^2/I1` from 0.99 down to 0.01: **NO finite-k roton minimum in the
full dispersion at ANY c0^2.** There is genuine group-velocity SOFTENING (min vg / c_chi drops to ~0.4, 0.18,
even 0.003) but it always recovers to a monotone rise. The fold the truncated polynomial advertised does not
exist in the exact branch.

## Step 4 — hostile grid: NO true fold anywhere (180 ladder x c0^2 combinations)

`pp_verify_step4b.py` (robust bisection on the lowest branch): scanned Delta in {0.25,0.5,1.0,1.5} x
q in {0.9,0.7,0.5} x decay in {0.7,0.5,0.3} x c_chi^2/I1 in {0.9,0.6,0.3,0.1,0.03} = 180 cases.
**A true finite-k roton dip (omega'(k*)=0 with re-rise) appears in ZERO of them.** Softening yes (min vg/c_chi
down to 0.003 in the sharpest case), fold never.

## Step 5-6 — the method-independent reason: a NO-FOLD THEOREM (Herglotz/Pick positivity)

This is the different-method re-derivation that explains WHY, to all orders, beyond moments. Write the lowest
branch as `k^2 = x / D(x)`, `x = omega^2`, `D(x) = c0^2 + S(x)`, `S(x) = sum_n w_n/(x - W_n^2)`, `w_n > 0`,
on `x in (0, W_min^2)`. Then `S'(x) = -sum_n w_n/(x - W_n^2)^2 < 0` (strictly), so
```
d(k^2)/dx = [D(x) - x D'(x)] / D(x)^2 = [D(x) + x|S'(x)|] / D(x)^2 > 0
```
wherever `D(x) > 0` (the physical-mode condition `k^2 > 0`). So `k^2(omega^2)` is STRICTLY MONOTONE
increasing => `omega^2(k^2)` is monotone increasing => **NO ROTON FOLD, to ALL orders in k, for ANY positive
spectral density rho >= 0, ANY c0^2 > 0** (sympy + mpmath spot-check `pp_verify_step5.py`: min d(k^2)/dx > 0
across Delta in {0.05..1.0}, q in {0.7,0.9}, both edge and bulk c0^2 — always positive). The PASSIVE
(positive-weight) horizon response is a Herglotz/Pick function; its lowest acoustic branch cannot fold. This
is STRICTLY STRONGER than PP's Cauchy-Schwarz argument (which is the truncated-order shadow of this theorem),
and it is the real content of "BROAD": a passive bath softens but never folds.

## Step 8 — closed the last loophole (D(x) zero-crossing / branch end)

`pp_verify_step8.py`: the no-fold theorem assumes `D(x)>0`. Where `D(x)` crosses 0 inside the support
(the sound mode hits the bath, `k^2 = x/D -> +inf` at finite omega), could the turnaround mimic a re-rise?
Checked 18 cases: `D` does cross 0, but `omega(k)` stays MONOTONE up to the branch end in every one — k
diverges while omega is finite, so vg -> 0 from above, never a fold. No hidden roton. Theorem robust.

## Step 7 — anchors: PP's CS numbers and the BEND sign reproduce independently

`pp_verify_step7.py`: delta-limit ladder CS range [0.847, 0.993] (PP 0.92-0.96, max 0.9952 — reproduced);
single delta CS = 1.000000 exact; two deltas (1,3) CS = 0.921 (PP 0.938, same class). sigma4 < 0 (BEND) for
every ladder with c_chi^2 > 0 — HELD, matches OO + PP.

---

## PRIMARY CHECK (the brief's central demand): was a finite-k PEAK claimed, and was it real or smuggled?

**PP did NOT claim a finite-k peak — and that honesty is vindicated.** PP labeled the response
"broad-zero-centered" and never asserted a finite-k resonance. My steelman FOUND an apparent peak (the
truncated-poly roton, sigma6>0 window) that PP's fixed-c0^2 scan had MISSED — but it is a smuggled peak in the
sense that matters: it lives only in the IR-truncated polynomial, at a k* outside the IR radius, and EVAPORATES
in the full self-consistent dispersion. The purely-damped (Re omega=0) QNM modes are exactly the zero-centered
relaxational response the hostile prior named; they soften the sound mode but the Herglotz positivity of the
passive self-energy forbids the dip-and-rise. **No real finite-k peak exists. The response is BROAD.**

## VERDICT — CONFIRMED. STILL-UNBOUNDED.

- **sigma4 < 0 (BEND): CONFIRMED HELD** (independent sympy derivation + grid; matches OO's forced sign).
- **sigma6 > 0 / bounded fold: NOT delivered — CONFIRMED.** PP's CS<1 conclusion is right, though its stated
  *reason* (CS as the order parameter at fixed c0^2) was incomplete: the exact criterion admits a sigma6>0
  window once c0^2 is scanned to the edge, which PP missed — but that window is an IR-truncation artifact with
  no fold in the full dispersion. The robust, all-orders truth is the NO-FOLD THEOREM: a passive (rho>=0) dS
  QNM response is Herglotz-monotone and CANNOT fold the acoustic branch. PP's verdict survives by a *stronger*
  argument than PP gave.
- **k* edge-pinning: NOT delivered — CONFIRMED.** No inflection/minimum exists in the full dispersion;
  nothing to pin. (The truncated "k*" tracked the QNM moment scale, not b->c_chi, as PP noted.)
- **PEAKED-vs-BROAD: BROAD — CONFIRMED**, by an independent method (full-dispersion monotonicity, not moments).

The named unbanked input — "a peaked dS QNM horizon resonance bounds + edge-pins the fold" — is **REFUTED**.
The dS QNM ladder, being a PASSIVE positive-weight response, cannot supply a fold by a theorem, not just a
numerical band. PP's next_calc (1) — a NON-PASSIVE / gain (negative-weight) horizon response, the only way to
break Herglotz monotonicity — is the correct and only remaining direction inside this route. Concur with PP.

**Regrade: CONFIRMED. Verdict STILL-UNBOUNDED. (Strengthened: PP's numerical CS<1 is upgraded to an
all-orders no-fold theorem; PP's one gap — the unscanned c0^2 / sigma6>0 window — was chased down and shown
to be an IR-truncation artifact, not a missed fold.)**

**Coefficient quarantine held:** only signs of sigma4/sigma6 and the monotonicity structure computed;
q=1/4, zeta-tilde, (16pi/3)^{1/4} never touched.

**Scripts:** /tmp/pp_verify_step0.py (sigma6 criterion), step0b/0c (exact-window steelman), step1 (c0^2 scan
finds truncated roton), step2/3 (full dispersion monotone — artifact exposed), step4b (180-case grid: no fold),
step5/6 (Herglotz no-fold theorem), step7 (CS + BEND anchors).
