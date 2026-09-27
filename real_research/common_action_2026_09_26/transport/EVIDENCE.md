# Transport evidence — CD26-4

All nine accepted manifests listed below were validated with the installed mathbox
`validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula`.
Inputs and declared outputs match their recorded hashes. All returned completed
with exit zero. The matrix contains 163 exact/finite checks and 21 Lean
declarations, with their distinct scopes retained below.

| Accepted run | Scope | Runtime | Cap |
|---|---|---:|---:|
| [run_001/manifest.json](run_001/manifest.json) | 41 exact/finite transport controls | 2.237649 s | 60 s wall |
| [run_charge_001/manifest.json](run_charge_001/manifest.json) | 11 exact fixed-charge identities | 0.536938 s | 60 s wall |
| [run_lean_001/manifest.json](run_lean_001/manifest.json) | 13 compiled transport algebra statements | 72.754353 s | 160 s wall |
| [run_spatial_001/manifest.json](run_spatial_001/manifest.json) | 22 conservative spatial controls | 1.762165 s | 60 s wall |
| [run_spatial_energy_001/manifest.json](run_spatial_energy_001/manifest.json) | 11 independent energy/timestep controls | 1.133818 s | 60 s wall |
| [run_conversion_001/manifest.json](run_conversion_001/manifest.json) | 19 exact/finite coherent-conversion checks | 1.607364 s | 60 s wall |
| [run_conversion_packet_001/manifest.json](run_conversion_packet_001/manifest.json) | 16 full nonlinear conversion-packet controls | 5.783564 s | 120 s wall |
| [run_conversion_lean_001/manifest.json](run_conversion_lean_001/manifest.json) | 8 compiled conversion algebra statements | 48.191824 s | 160 s wall |
| [run_homogeneous_frw_002/manifest.json](run_homogeneous_frw_002/manifest.json) | 43 exact/finite coupled homogeneous Einstein-carrier controls | 14.133204 s | 120 s wall |

Each manifest records its exact Git revision/dirty state and command. Initial
revision was `ecffd2af3623ff3e32318234fd51e1fac50b9126`; concurrent work may advance
the tree, so individual hashes delimit the scope. Standard Python runs had
60-second wall/50-second CPU caps; the conversion packet and homogeneous FRW
runs had 120-second wall/110-second CPU caps. Lean had 145-second per-process CPU caps and 150-second
child timeouts inside 160-second runner caps. All used a cooperative thread
cap of one; no memory or affinity cap is claimed.

The separately retained [run_homogeneous_frw_001/manifest.json](run_homogeneous_frw_001/manifest.json)
is a valid failed-run record and is excluded from every accepted count. In
8.337137 seconds it reached the final comparison and failed the two-tolerance
Hubble-agreement assertion; no scientific result file was accepted. Its
source is retained unchanged. The accepted refinement tightens both ODE
tolerances and checks the Friedmann residual against the vacuum density,
not only the much larger initial density. Both manifest records validate
with their exact input hashes. This numerical accuracy failure does not
refute the separate analytic homogeneous theorem.

Both Lean sources completed with exit zero, no warnings/errors and only
printed axioms `propext`, `Classical.choice`, `Quot.sound`. The 21 statements
are explicitly scoped real-algebra positivity, transport and resonance bridges.
They do not certify the variational/PDE derivation, global energy-space theorem,
packet simulations, full gravity or observational behavior.

## Accepted source and result hashes

- `check.py`: `bf99aa42fc6e2c02c3e6eb9bc6aebad8c0391c2379ae73b6c7fdfa7bf3f5eb14`.
- `charge_transition_check.py`: `6a1e60ada26c9f368d8f764284c048b8855501bbfc15813c50274d51816a5e03`.
- `spatial_check.py`: `0de6fe97d4da234577de54debe50003876df66905d36ecdfe52e3410fa9824b1`.
- `spatial_energy_audit.py`: `20de3b4b3c21317ccfd3f9cfd13def23ecb012dfe76687710fd4079ed8bec7ad`.
- `conversion_check.py`: `32443a386bc62ede9e44cc3eac8d3ca48e5c0ad5293867165c3115a453bcd10c`.
- `conversion_packet.py`: `28cb172ea71aabab45fc2b8f2cec90fd32de364848f9b281fbbe52de2ed9d5b2`.
- `homogeneous_frw_refined_check.py`: `e4d7bdb2cac3212613c703504be66526bea8f015267f384bb20925071f3c056b`.
- `CommonTransport20260926.lean`: `171e6e14f17f0276ac847c70d23ba83892a6e4dd0d83069765237939084ab576`.
- `ConversionTransport20260926.lean`: `2a3fb7707dd51e0a565d1b6c0f87603a8e8cffc71989b11bf675652caac0e9aa`.
- `verify_lean.py`: `cad05603e4218b4d3349fa00888ffebdf420b92cf11898b57dc0950cc204ac3f`.
- `verify_conversion_lean.py`: `f7bab72e330ae7b1fd227798fcf65f521421dca4121f1736d55354b8be9f6a9e`.
- `run_001/results.json`: `517bac050ab2fcfd92fb74183eedc3228f1f9bbabce51585733bb04e5c7dd97a`.
- `run_charge_001/results.json`: `b10b3e662bfe604271c3e83799492bea5c4f8b1c03290d152b3c69c80f9259b6`.
- `run_lean_001/results.json`: `0feb11abbf698c9e6ce444e9d75e83971f3ee0e751ccbd93a1506b6f2ca62cdf`.
- `run_spatial_001/results.json`: `413b4c2d08eff59d7898ebd96a9b33f1dd5c59d222da742c05e74aa5fa09661e`.
- `run_spatial_energy_001/results.json`: `38ee76832e8823765f4db35939ce8e605de66bf51c002b969134f241e401f2eb`.
- `run_conversion_001/results.json`: `10ab261cdebb59ed54aa6e7558784a8d1ba09598ed5636ff51fbc3633b779fae`.
- `run_conversion_packet_001/results.json`: `cdf736cd53b322b19a986a305d44781ca26717fc69e9183fe91ddafe961d4f21`.
- `run_homogeneous_frw_002/results.json`: `6157e4686befbf80f05ee63b9f2df4555756d35bcd6a6c8fc1f123f633b7d854`.
- `run_conversion_lean_001/results.json`: `029d7668fc4de052dc1d130d8e84dc6d52d714af121ce685af3341b34968cca0`.
- `run_lean_001/stdout.txt`: `d618dc4cd3a250a7078eea699ec6af7f482ac53112c3eb55f79d9373e30e3bf7`.
- `run_conversion_lean_001/stdout.txt`: `ef57ffb86ac4fb85ebaf3039e2a7a7aea9368db5bd164afbed87ec145448f7de`.

Prior-source versions for the prescription audit are pinned in run_001:
L365, L377, L380, L373, the prior canonical-clock report and Fisher transport
report. Historical expensive carrier simulations were read, not executed.

The scientific controls preserve negative outcomes: the neutral transition
retains more local charge than the uncoupled packet; a zero classical seed
does not trigger; pump-induced mass can close coherent resonance. The full
conversion packet exports charge but its region clearing remains approximately
9.75e-5, far short of a claimed cosmological evacuation result.

The fixed-background global energy-class continuation argument, including
fixed smooth static inhomogeneous lapse/gate/metric coefficients on a compact
leaf, is displayed in CONVERSION.md using the Sobolev product and weighted
Duhamel estimates. Its analytic
scope is distinct from all finite outputs and from the still-open coupled
gravity/gate problem. No external paper is used as an unverified theorem
premise in these new derivations.

The later [HOMOGENEOUS_FRW.md](HOMOGENEOUS_FRW.md) proves a distinct
nonlinear future-global, asymptotically de Sitter branch of the actual PQ
common action, with flat compact homogeneous leaves, all masses and the
vacuum floor strictly positive, and expanding constrained initial data.
Its proof uses compact energy sublevels and an explicit omega-limit
argument. The 43 finite checks verify the displayed identities and one
two-tolerance coupled trajectory; neither those checks nor the existing
Lean algebra certificates formalize its infinite-time ODE proof. Spatial
inhomogeneous global gravity remains open, and no homogeneous evacuation
claim is made.
