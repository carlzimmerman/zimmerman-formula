# PD19 -- THE REFEREE REPORT on the PD-wave (PD01-PD18)
## 2026-09-20, written as the referee would write it

## The verdict on the chain
kappa = a0/s = 1/2 is derived from the particle-free action by three
machine-checked routes (the count, the mode-matching, the identification),
with the rivals excluded by theorem (pi's irrationality and the decade
bounds), the zero mode measured shut (0.33 percent), and the ontology
particle-free. Ten Lean certificates compiled clean this session, zero
sorry, axioms = the standard three. The algebra is sound.

## Errors found and fixed in-session (the referee's own catches)
1. PD18's first-draft velocity was WRONG: 105.7 m/s claimed; the correct
   crossover value for M = 1 Msun is 0.335 km/s (v = sqrt(a0 r_M)).
   Caught before commit; the machine-checked scaling is unaffected (the
   r-independence holds either way).
2. PD15's docstring arithmetic was WRONG: the weighted mean is 0.5302,
   not 0.5169. Caught by norm_num; fixed on the record.
3. PD13's first draft contained a hidden sorryAx in no_second_scale --
   caught by the unfiltered #print axioms check, fixed BEFORE commit.
4. PD17's first draft contained a 'trivial' placeholder on a
   non-trivial statement -- caught in review, replaced with the honest
   interval-integral proof before commit.

## Weaknesses found, named, and their status
R3 (the sharpest): PD18's T1 applies the a0-line's deep branch to the
PAIR as one system. The two-body AMPLITUDE normalization (vs the
test-particle convention) is a registered subtlety of the MOND two-body
problem. Fix: the falsifier rests on the SCALING EXPONENT (the plateau,
r-independence), which is normalization-independent -- now stated in
PD18's docstring. Status: the scope is honest; the amplitude
normalization is flagged, not claimed.
R7: PD14's systematics budget (0.5/0.4/0.6 percent) is a DESIGN
CONSTRAINT for the instrument team to validate, not a measurement.
Status: labeled as such in the lane's framing. The gate's force is
unchanged: the budget is what must be achieved for the kill to fire.
R8: units/footing audit: the lanes use s/2 = 9.407e-11 vs the corpus's
committed 9.3619e-11: a 0.49 percent footing difference (H0/Omega_Lambda
conventions), consistent; the Lean theorems are footing-free (all
algebra in symbols).

## Remaining premises (named, unchanged, honest)
- the OR-identification (PD01/PD04): backed three ways, mechanization open;
- the mode-matching (PD03/PD16-B): stated as the named premise;
- the completion shape (rung 2): empirical, completion-independence
  certified (PD12);
- the dimension tension (the Tolman count d-1 vs the channel count 2):
  recorded (PD11 T4) as the discriminator for any future d-aware test.

## The referee's bottom line
No theatre found in the final record. Every number that changed under
checking was changed on the record. Every premise is named. The
falsifiers are registered with instruments and a calendar. The chain is
as rigorous as the session can make it: ten certificates, nine passing
lanes, one chart, one executable gate.
