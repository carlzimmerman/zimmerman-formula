# Protected auxiliary continuation

**The original microscopic normalization goal remains open.** Under
criteria-only commit 3a6b85cac, [RESULT.md](RESULT.md) tests whether
supersymmetric auxiliary sectors can fix vacuum energy and a MOND cubic
together. No healthy model here forces the requested amplitude ratio.

The chiral prototype does calculate positive rigid vacuum energy and a
positive static cubic correction. Positive quadratic coefficients at its
constant-field fold are insufficient: its critical branches disappear
for small timelike gradients, while every surviving real branch has a
decoupled physical scalar ghost. Its infrared quadratic stiffness also
survives, and its displayed large-gradient action has quartic response.
The nominal local Taylor ratio 1/9 is not a force-calibrated MOND ratio.
A permitted derivative-coefficient deformation varies even that number.

The ordinary/minimal vector auxiliary class supplies a different test.
Its regular convex branches cannot generate the required cusp. For the
specified extra portal, a finite critical cusp violates the stated
convexity class; a parity-even case has an explicit supermetric photon
mode. These are restricted results, not a theorem about all supersymmetric
actions. Born-Infeld plus an ordinary FI term genuinely calculates a
displayed vacuum/nonlinearity relation, but retains a free FI/tension
ratio and gives a quartic rather than cubic diagnostic correction.
Its rigid energy normalization is not a gravitating dark-energy result.

[ChiralFold.lean](ChiralFold.lean) verifies six exact algebraic statements:
the vacuum factorization, fold expansion, timelike root bound, two negative
coefficient implications and nominal Taylor arithmetic. The component
dictionary, identification of the physical mode, eliminated asymptotics,
gravity and quantum health remain analytic inputs. This brings W4-08 to
seven partial modules; it does not provide an end-to-end physical proof.

The true rational controls pass. Dropping the timelike hypothesis makes
the claimed root bound false; asserting a positive auxiliary Jacobian at
the exact fold is also false. Both separate controls exit 1 with only an
unsolved False goal, without import or type errors. All six critical
theorem axiom sets are subsets of propext, Classical.choice, Quot.sound.

Reproduce from the repository root with fresh output directory names:

```sh
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py protected_auxiliaries/ChiralFold.lean protected_auxiliaries/runs/local_fold
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py protected_auxiliaries/controls/Normal.lean protected_auxiliaries/runs/local_normal
```

Run controls/DropTimelike.lean and controls/RegularFold.lean separately;
each must exit 1 at False. The shared runner uses the existing read-only
pin, one worker, 1024 MiB, 30s CPU and 45s wall. No broad build or download
was used. [check_evidence.py](check_evidence.py) validates the selected
manifest, source, dependency, object and log hashes and binds the additional
frozen contract without altering the raw runner records.
[REVIEW.md](REVIEW.md) records independent audit scope and development
history; [SOURCES.md](SOURCES.md) records primary component dictionaries.
