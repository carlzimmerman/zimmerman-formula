# Continue the parent and excess mechanism investigation

Checkpoint PC-2026-10-22-1, base e9e534936852643bb3f3ca9df07a31ed2734a30c. Owner: this chat. Write scope: this directory. Original goal remains open. No .mathbox ledger was present. No asynchronous job was started. Other work in mechanism_reassessment and CFG960 is separate; inspect current status before relying on it.

Read RESULT.md and AUDIT.md first. Source hashes for scripts/contracts and Git dirty-state observations are in the run manifests. Artifact hashes are in CHECKPOINT_SHA256.json. These are research provenance, not peer-review certificates.

## Route dispositions

- Hard identity and unchanged instantaneous gates: prior failed constructions; do not rerun without changing their failing hypotheses.
- Constant finite compliance: fails the declared static/local-growth pair. Closed only under that reduced action and those diagnostics; a full FRW response is not proved impossible.
- Material power compliance: open but restricted. m=2/3 is marginal under an idealized early-matter condition; high-density and field-dependent completions remain possible. No actual halo profile was solved.
- Passive susceptibility: global-equilibrium stiffening excluded for the stated energy class. Metastability/drive are outside the claim.
- Rotationally driven susceptibility: constructive finite-dimensional checkpoint. Field completion, observational backreaction and a physical coupling strength remain open. Do not rename the toy an explanation of pressure-supported excess.
- Existing A33 constraint/radiation route: open elsewhere; no claim of supersession.

## Next executable discriminator

Write a reciprocal mediator action coupled to a baryonic current and to e=rho-rhobar-divP. Starting prototype is RESULT.md's positive-energy auxiliary oscillator. A vorticity field coupling is a hypothesis, not yet fixed by the theory. First derive the kinetic matrix and characteristic speeds with baryon motion included; do not eliminate the mediator outside its frequency range. Then derive the homogeneous background and a rotating versus nonrotating solution at identical baryon density. Any coupling that only measures density fails to distinguish those two by construction.

The main cost is quantified: Delta I/I0_reference=f(S-1). Require a declared, independently justified bound on this backreaction rather than fitting it away with stellar mass. A large susceptibility gain with tiny f requires a correspondingly soft phase potential; those scales must be derived or listed as new inputs. No value is currently selected.

Before a dwarf/cluster fit, specify finite cold mass, source/receiver E and J, outer boundary, and initial state. Existing formation-roadmap criteria for Draco, Sextans, Fornax and Leo I still apply. A unique positive mechanical minimum is insufficient: an isolated Hamiltonian orbit does not settle into it. Outgoing mediator radiation must be calculated if it is the receiver, and its energy/angular-momentum flux counted.

Deferred, untried continuations: full reciprocal covariant field embedding; FRW beyond the quasistatic EdS diagnostic; regular finite-stiffness material-dependent radial BVP; high-density stabilization; source coarse-graining; conservative transport and rates; real-data scoring. They are open, not exhausted. Proceed once the relevant explicit action/constitutive choice is stated; do not silently add functions or claim parameter-free predictions.

## Reproduction

From repository root, direct checks (new output names avoid overwriting preserved evidence):

    OMP_NUM_THREADS=1 python3 sol61_push/parent_compliance_2026_10_22/checks.py --output /tmp/pc_checks.json
    OMP_NUM_THREADS=1 python3 sol61_push/parent_compliance_2026_10_22/scaling_checks.py --output /tmp/pc_scaling.json
    OMP_NUM_THREADS=1 python3 sol61_push/parent_compliance_2026_10_22/phase_checks.py --output /tmp/pc_phase.json
    OMP_NUM_THREADS=1 python3 sol61_push/parent_compliance_2026_10_22/rotation_checks.py --output /tmp/pc_rotation.json

Each accepts --mutate, expected exit 1. Original runner argv and limits are in each manifest. Runtime was approximately one to two seconds per run, single-thread settings, 45-second wall cap and 40-second CPU cap. No memory hard cap was set, so do not claim memory was enforced. An attempted nice adjustment was denied by the environment; execution proceeded without it. No dependency installation, network download, large simulation, commit or push was performed.

Final runs: run2, scaling_run, phase_run, rotation_run. Expected failed controls: mutation_run, scaling_mutation, phase_mutation, rotation_mutation. run is the preserved inaccurate-anchor failure and is not current supporting evidence.
