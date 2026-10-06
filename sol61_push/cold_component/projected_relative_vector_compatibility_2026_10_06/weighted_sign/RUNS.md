# Frozen bounded runs

Current evidence is the four b runs. Their manifests validate against corrected REPORT `962bbaa384511a3f92cd64697ff9962166336666a355f06d2415fd84ef18fdd7` and unchanged checks `93044ea7bc4b52a1229112a7fddb604e992077080efdcc87664c72550efd0153`. Exact arithmetic; 20 CPU /30 wall seconds, one library thread.

The a runs are historical, superseded and stale against current REPORT. Their preserved report is REPORT_a_superseded.md SHA `49ba27798366310eaf1c135ea567b5f527a9bc72f08774431628a3f1ae1e5f9f`. The sole correction is the prose benchmark R=−3 cos(2x), replacing the erroneous plus sign; computed R and I=−3/4 were correct throughout. No code changed.

- control_mean_b: 7/8; failures: candidate zero mean residual guarantees compatibility.
- control_negative_b: 7/8; failures: candidate universal nonpositive integral.
- control_transport_b: 6/7; failures: weighted integration identity.
- main_b: 7/7; failures: none.
