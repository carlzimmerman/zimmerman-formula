# I007 — Does U still saturate once a0 is a FIELD? (S4)

**Verdict:** KILL
**Decisive number:** max over the whole (y, s, r, footing) grid of U_eff/s = **0.999698 <= 1**
(ceiling Fmax*s = (1+1.39e-12)*s; both footings: a0_canon = 9.3619e-11 m/s^2, a0_alt = 1.1279e-10 m/s^2)
**Script:** `runs/i007_field_a0_saturation.py`  (checks: 4/4, exit 0)

## Hypothesis
Legality forces U -> s in v = sqrt(Y)/a0, but a0 depends on the local charge, so the
OBSERVABLE U at fixed radius, plotted against y = g_bar/a0(0), "need not be bounded."
If true, this would void the legality obstruction that produces the 233x saturation gap.

## What I actually did
Built U_eff(y) = F * U(v) exactly as the brief prescribes:
F = a0(nu)/a0(0) = [(1+nu0^2)/(1+nu^2)]^(1/4) (N4), nu = nu0*rho/rho0 with nu0 = 2.36e-6
(N4 ceiling), rho = g_bar/(4*pi*G*r) (point-mass enclosed density, brief), v = sqrt(Y)/a0(nu)
= g_bar/a0(nu) = y/F, U(v) = v/(1+v/s) (the brief's "inversion" of J_Y = v/(1-v/s)), and
U_eff = F*U(v). Swept y in {1, 2, 10, 1e3, 1e6, 6.33e7}, s in {1.27e-5, 1e-3, 0.219},
both a0 footings, and radii {1, 10, 100} kpc. I added an algebraic bound check (check 4)
over r in [1e19, 1e28] m independent of rho0, footing, and s, which is the actual decisive
test of "need not be bounded." I did not consume `rar_sparc_a0units.json` — the analytic
grid is closed-form and the JSON would only resample the same monotone curve, so it is not
load-bearing here (noted under "Owed").

## The math
Chain of substitutions:

1. y = g_bar/a0(0)  =>  g_bar = y*a0(0).
2. rho(r) = g_bar/(4 pi G r) = y*a0(0)/(4 pi G r).
3. nu = nu0*rho/rho0  =>  nu = (nu0/rho0)*y*a0(0)/(4 pi G r).
4. F = a0(nu)/a0(0) = [(1+nu0^2)/(1+nu^2)]^(1/4).
5. v = sqrt(Y)/a0(nu). Since sqrt(Y) = g_bar = y*a0(0) and a0(nu) = F*a0(0),
   v = y*a0(0)/(F*a0(0)) = y/F.   (the a0(0) cancels: v depends on y only through F.)
6. U(v) = v/(1+v/s), so U(v) = (y/F)/(1 + y/(F s)) = y*s/(F s + y).
7. U_eff = F*U(v) = F*y*s/(F s + y).

**The bound.** Is U_eff <= s for every rho(g_bar)?
   F*y*s/(F s + y) <= s   <=>   F*y <= F s + y   <=>   y(F - 1) <= F s.

F = (1+nu0^2)^(1/4) / (1+nu^2)^(1/4). Two branches:
- Physical branch, rho >= rho0  =>  nu >= nu0  =>  1+nu^2 >= 1+nu0^2  =>  F <= (1+nu0^2)^(1/4)
  AND F <= 1. So F - 1 <= 0, hence LHS = y(F-1) <= 0 <= F s. **U_eff <= s strictly.**
- Unphysical branch, rho < rho0  =>  nu < nu0  =>  F in (1, Fmax] with Fmax = (1+nu0^2)^(1/4).
  Here U_eff <= Fmax*s. With nu0 = 2.36e-6, Fmax = (1+5.57e-12)^(1/4) = 1.00000000000139,
  i.e. an excess of 1.39e-12 over s — physically nothing.

Therefore U_eff <= Fmax*s <= s(1+1.4e-12) for ALL (y, s, r, footing). The hypothesis that
U_eff "need not be bounded" is FALSE. This is a composition of two bounded factors:
F <= Fmax ~ 1 (a suppression, never an enhancement, by construction for nu >= nu0) and
U(v) = v/(1+v/s) monotone in v saturating at s. Their product cannot exceed s(1+1.4e-12).

**Why the small ratio is a red herring.** U_eff(6.33e7)/U_eff(2) is < 1e-2 everywhere
(1.86e-4 to 7.57e-4 across footings/radii), so the brief's PASS ratio condition is
numerically met. But it is small because F COLLAPSES at high y (rho up, nu up, F -> 0,
U_eff -> s*F -> 0), i.e. strong suppression, not unbounded growth. A small high-y ratio is
the signature of *more* boundedness, not less.

## Numbers
| quantity | value | note |
|---|---|---|
| a0 (canon footing) | 9.3619e-11 m/s^2 | computed 9.3154e-11 (ratio 0.995) |
| a0 (alt footing)   | 1.1279e-10 m/s^2 | PROTOCOL line 1 |
| nu0 (N4 ceiling)   | 2.36e-6 | most suppression-favourable |
| Fmax = (1+nu0^2)^(1/4) | 1.00000000000139 | global ceiling of F; excess 1.39e-12 |
| U_eff/s over full grid | **0.999698** | <= 1 => bounded (decisive) |
| exceed count over r in [1e19,1e28] | 0 | U_eff never above Fmax*s |
| ratio U_eff(6.33e7)/U_eff(2), canon r=10kpc s=.219 | 2.606e-4 | < 1e-2 but by suppression |
| ratio U_eff(6.33e7)/U_eff(2), canon r=100kpc s=.219 | 7.569e-4 | same |
| ratio range all footings/radii (s=.219) | 1.86e-4 .. 7.57e-4 | all < 1e-2 |
| U(v) monotone in v, all s | True | dU/dv = s/(1+v/s)^2 > 0 |

## Why this verdict
Pre-registered **KILL condition: "U_eff bounded by s for every rho(g_bar)."** It fired.
The algebraic proof (check 4, exceed_count = 0 over r in [1e19, 1e28] m) and the grid sweep
(check 3, max U_eff/s = 0.999698 <= 1) both show U_eff <= Fmax*s <= s(1+1.4e-12) at every
y, s, radius, and footing. The field-a0 promotion a0(nu)/a0(0) is a *suppression* factor
(F <= 1 for nu >= nu0), so multiplying U(v) by F cannot create unboundedness. The 233x
legality obstruction (ephemeris needs s <= 2.4e-3, RAR needs s >= 0.558) is NOT relieved
by making a0 a field.

The brief's PASS ratio condition (< 1e-2) was also numerically met, but it does not rescue
the hypothesis: a small high-y ratio is the signature of F-driven suppression, and the
direct boundedness test is the decisive one. When the two pre-registered conditions conflict,
the one that tests the literal hypothesis ("need not be bounded") governs, and it is KILL.

## Against my own result
1. **The construction is a made-up mapping.** The brief's U(v) = v/(1+v/s) is the "inverse"
   of J_Y = v/(1-v/s), not the a0-line kernel U = sqrt(y^2+y)-y (PROTOCOL line 3, saturating
   at 1/2). The KILL is robust to this because the bound U_eff <= s holds for the *specific
   form chosen*, but it would need re-deriving for any other legal kernel. A different legal
   U(v) could in principle behave differently. (Mitigant: any legal kernel saturates at a
   finite s, so the same "F is a suppression" argument re-applies.)
2. **The rho = g_bar/(4 pi G r) tie is a point-mass heuristic**, not a real galaxy density
   profile. But the bound does not depend on this tie: U_eff <= Fmax*s holds for ANY positive
   rho, since it only requires F <= Fmax, which is a property of the N4 formula alone, not of
   rho(r). So the result is robust to the density choice — which is also the strongest reason
   it is almost trivially true.
3. **The "field" promotion is built to suppress.** a0(nu)/a0(0) = [(1+nu0^2)/(1+nu^2)]^(1/4)
   is <= (1+nu0^2)^(1/4) ~ 1 by construction for nu >= nu0. Given that F is designed to be a
   suppression, the conclusion "F*U cannot exceed s" is nearly a tautology. The real question
   the idea hoped to answer — *could* a field a0 ever amplify U — cannot be tested by a
   formula that is by definition bounded above. This is a genuine weakness: the test does not
   rule out a *different* field-promotion that amplifies; it only rules out this one.
4. **Both footings agree** (ratio 0.995 between computed a0 and canon), so the footing is not
   the source of the result; the suppression factor is.

## Owed / not computed
- Did not ingest `qwen_38_experiment/data/rar_sparc_a0units.json`. Not load-bearing: the
  analytic U_eff(y) is closed-form and monotone, and resampling the empirical RAR points onto
  it would only reconfirm U_eff <= s. To use it one would bin the 3389 points by log10(g_obs/a0)
  and overlay the computed U_eff curve; the verdict (bounded) would not change.
- Did not test amplifying field-promotions (F > 1 unbounded). The brief fixes F =
  [(1+nu0^2)/(1+nu^2)]^(1/4); a different N6/N4 promotion is out of scope for this idea and
  would be a separate idea.

## Files touched
- `qwen_claude_field_theory/runs/i007_field_a0_saturation.py` (created prior session; fixed
  two cosmetic report lines 131-132 that returned a stray loop var instead of the ratio;
  checks/verdict/exit unchanged: still 4/4, KILL, exit 0)
- `qwen_claude_field_theory/results/I007_field_a0_saturation.md` (this file)
- `qwen_claude_field_theory/LEDGER.md` (one row appended)
