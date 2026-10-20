# Regular current continuation

The original why-4 goal remains open. [RESULT.md](RESULT.md) records
three executed current/gauge routes under criteria commit 33e139648.
No route derives positive vacuum normalization or the requested ratio.
Reviewed result/evidence commit: 73cb47a32. Campaign rows K680-K685
record the six distinct scoped outcomes; none adds a determinate trial.

The strongest new obstruction is explicit: an apparent cubic induced by
a Jacobian charge under local neutrality has a cheaper electric-flux
trial for compact profiles in the trivial boundary sector. Its fully
relaxed excess energy is bounded between zero and C delta^4; it cannot
have a positive leading cubic. Nontrivial boundary/charge sectors remain
outside that proof. A regular interaction with the condensate's own
current instead leaves its neutral vacuum empty and gives quartic
corrections at fixed charge.

[CurrentEnergy.lean](CurrentEnergy.lean) verifies six exact Legendre,
positivity and charged-minimum statements. [FluxComparison.lean](FluxComparison.lean)
verifies the flux-trial jet cancellation, its quartic Maxwell energy and
the quartic-versus-cubic comparison. The field/current derivation,
integration, admissibility, variational infimum, limits and quantum
health remain analytic inputs; these files do not certify those bridges.
All nine printed theorem axiom sets use only standard axioms. The two new
modules bring the W4-08 total to six partial modules, not an
end-to-end physical derivation.

The normal rational controls pass. Omitting the current's canonical
shift and asserting an occupied zero-energy neutral vacuum each reduce
to False and fail separately. Initial control runs lacked the rational
Field import and are preserved with source snapshots; they are not
accepted mutation evidence. Final v2 controls have no import failures.

Reproduce from the repository root with fresh output directory names:

```sh
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py current_interactions/CurrentEnergy.lean current_interactions/runs/local_current
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py current_interactions/FluxComparison.lean current_interactions/runs/local_flux
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py current_interactions/controls/Normal.lean current_interactions/runs/local_normal
```

Run WrongCurrent.lean and OccupiedVacuum.lean in controls separately;
each must exit 1 with only an unsolved False goal. The shared read-only
pin/runner uses one worker, 1024 MiB, 30s CPU and 45s wall. No download,
broad build or reserved file modification occurred. A current process
inspection confirmed the previously recorded large simulation still
running; no limits were raised and no job was interrupted.

[check_evidence.py](check_evidence.py) checks current hashes, selected
manifest/log/object hashes, the pin, printed axioms and exact control
failures. It explicitly binds the additional frozen current contract to
the runner manifests without modifying those raw records or the original
runner. [REVIEW.md](REVIEW.md) records independent analytic scope checks;
[SOURCES.md](SOURCES.md) records the authenticated primary CS dictionary.
