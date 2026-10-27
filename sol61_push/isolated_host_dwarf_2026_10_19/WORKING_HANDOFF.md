# Completed computation — historical checkpoint below

All 13 declared evolution records (11 physical runs, two diagnostic replays) and the final analysis completed. All 115 output checks and 14 focused unit tests pass; all scientific manifests and the successful geometric retry validate. The self-contained final result is README.md and analysis_run_001/. No runs remain active. The host mass is unconverged: doubling particles changes M300 from2.436645 to4.978576 million Msun, while the matched isolated value is11.461254 million. Both100pc density structure and transport convergence remain unestablished. The text below is retained as a historical mid-run checkpoint, not current instructions to restart anything.

User request: run the same initially diffuse dwarf isolated and around a host using actual cold-energy equations, without inserting a core; track energy and angular momentum. Continue through the running numerical checks and final report. Do not stop at this checkpoint.

## Scope and immutable code

This is the original prepared dilute Phi/X daughter-carrier Newtonian kinetic–Poisson subsystem (MASTER lines183–195,493–511), not the unclosed full canonical polarization framework. User was told this before runs. Actual revised elastic kernel: sigma0/m=.3cm²/g,u*=.02,r_lambda=2; all material is prepared daughters, no source population. CFG541 drift/target, CFG654 shell draw, ARGON action and inserted cold core are excluded.

Only this new directory was written during this run; root MASTER edit predates the current experiment. No AGENTS.md found. Base git d8611577f599b7919a894c91a15b4ec7a75f0bc8; sources hashed in source_inputs.json. Do not edit active run inputs: CONTRACT.md, source_inputs.json, run_dwarf.py, dynamics.py, direct_gravity.c/.dylib, launch.py, test_driver.py, test_dynamics.py. Remnant replay inputs also include run_dwarf_remnant.py,remnant.py,test_remnant.py,launch_replay.py,DIAGNOSTIC_REFINEMENT.md. The active simulations must finish with their before/after hashes unchanged.

Scenario: stellar mass574272.9377Msun, cold inventory53.64times stars=30.804millionMsun; cold uniform ellipsoid axes2000/1600/1200pc; cold2K/|Wvir|=.2 and10%rotational kinetic fraction. Live Plummer starsa193.22pc. All initial positions/velocities prepared inputs, not native cosmology. Host prescribed static Plummer6e11Msun,b10kpc; orbit starts80kpc,0.65localvc; pericentre~23.8kpc. Full3D softened mutualgravity eps40pc. No target/thermostat/deleted particles. Baseline2048cold+256stars,10Gyr, dt2Myriso/.5Myrhost. Refinements halfdt,doubleN,h200→100pc; extra eps20pc/dt1iso.

## Processes / queued work

Completed scientific cases: base_iso,base_host,nocoll_iso,nocoll_host,dt_iso,dt_host,eps_iso,replay_iso,replay_host. Three small pilots also retained; coarse hostpilot failed1%energygate, prompting hostdt.5 before production.

Remaining checks were requeued into two parallel one-thread low-priority processes after dt_host completed:
- exec session71748: `python3 launch.py n_iso h_iso h_host`
- exec session37073: `python3 launch.py n_host`
Both launched on19Oct~22:19NewYork. N_host may take~15–20min. Each runner wallcap1800sec/CPU1750sec, one numericalthread, low schedulingpriority. No unrelated job touched.

Old sequential queue parent71865 was SIGSTOPed while its dt_host child finished, then SIGTERM+SIGCONT after completed manifest. Session30470 may return terminated; this is queue bookkeeping, not a failed scientific simulation. No active child was interrupted. Extra epsilon session22688 completed; diagnostic replay session71793 completed.

## Existing finite evidence

- Isolation: old centre initialM300=.210574millionMsun; remnant-centred finalM300=10.964901million. Persistent300pc concentration assembled from diffuse material. At200Myr already47.36%of stock inside300pc, onlyONE C22 collision: early formation is gravity/violent-relaxation dominated.
- Collisionless iso remnantM300=10.994983million, only.274%different; this is not a distinctive microscopic-interaction mechanism.
- dt1iso remnantM100/M300=1.669553/11.235639million.
- eps20/dt1iso remnantM100/M300=2.421604/11.446213million: matched softening comparison changes100pcmass45.05%,300pcmass1.874%. Do NOT claim a converged100pc density core or universal core radius.
- Host old stellar shrinking centre fails after severe stripping (retains>=Nstar/4despite tails). Remnant.py finds potential/density bound core15.2kpc away: M100=.345943million,M300=2.436645million,162coldparticles/12stars. Local instantaneous self-unbinding unchanged inside300pc for500–2000pcoutercuts. Host weakens/strips this particular cloud/orbit; not all hosts or measured satellite excess explained.
- Diagnostic replays change only centring and data recording. BOTH iso/host initial AND final x,v,m,cold arrays were checked BITWISE IDENTICAL to v1. Replays save trajectory.npz (100Myr snapshots) and per-particle host work/torque in final.npz. Use replay outputs for representative profiles, histories and core-cohort budgets.
- All-step energyerrors normalized to initial dwarf internal binding: baseiso.588%,basehost.707%,dtiso.133%,epsiso.213%. J ledger errors tiny (~1e-12orless). No radiation or live host response in model. Host totalJ about origin conserved; internal/orbitalJ exchange balances.
- Corrected iso final-core cohort loses4.54764446e8 energyunits (Msun pc²/Myr²); outer cold receives nearly all, stars small share. Vector budgets in replay results.
- Host remnant cohort deltaE=3.5073e10, hostwork3.5489e10, internalexchange=-4.16295e8; othercold internal+4.96891e8,stars-8.057995e7. These are whole-original-dwarfCOM accounts including remnant bulkmotion; distinguish own-core spin via analyse.py.

## Files and final steps

1. Wait on both queued execsessions with bounded polling; inspect manifests/results, not stdoutprogress (runner pipes buffer8192bytes, so logs may remain empty until exit). Communicate meaningful updates. Do not extend routine tests after checks resolve them.
2. `analyse.py` can generate working summaries/images in this directory while cases finish; it now uses independent remnant endpoints for comparisons and prefers replay histories. `eps_iso` compares to dt_iso, avoiding timestep confounding. Host v1 late-Gyr stellar-centred masses are retained only as explicitly unreliable legacy diagnostics.
3. `audit_outputs.py` expects all13scientificcases, verifies completion, no deletion, E/J closure, paired initial state and replaybitwiseidentity. It calls analyse and uses per-particle replayreceipts to follow the SAME iso-selected and host-selected cold cohorts across environments; writes JSON/CSV.
4. Once all13cases complete, run `python3 finalize.py` here. This records fresh analysis_run_001/ with manifest, analysis.json,comparison.csv,isolated_host_comparison.png,same_material_transfer.json/.csv,audit.json. Input closure includes all casejson/initial/final/manifests and analysis/importedcode. Validate using skill scripts/validate_manifest.py --root PROJECT, with /opt/homebrew/bin/python3.12. Run.status matters. If a new diagnostic bug is found, preserve failed analysisrun and use a NEW outputdir, never overwrite.
5. Run final14unittests: `/usr/bin/python3 -m unittest discover -v` here. Root py_compile hit an unwritable systemcache; ASTparse and tests are the successful checks; no unresolved permissionblock. Avoid py_compile without explicit writable PYCACHEPREFIX.
6. Write README.md scientific report with actual N/h conclusions, exact scope, budgets/limitations, reproducibilitycommands, links to final analysismanifest/data. Do not edit original theory/manuscript or claim fulltheorycompletion. Inspect final scientific PNG with view_image and fix plottingonly if needed; regenerate under fresh provenance if changes affect analysis.
7. Final answer concise: isolated centralcomponent forms in this prepared carrierlimit; stronghostorbit strips it; gravitycontrolmatches; outercold and orbitalmotion receive E/J;100pcprofileunconverged; link report/plot. State particlecountconvergence limitations if present. Show PNG if useful. No commit/push requested.

Independent geometric evidence: geometric_bound.py,GEOMETRIC_BOUND.md,geometric_contract.json. Successful manifest geometric_run_001/retry_cpu_bounded/manifest.json, validated with --root. Exact saved-coordinate dyadic geometry proves ANY300pcsphere in baseline host finalsnapshot contains<=192coldparticles=9.375%initialstock, below205particle10%candidategate. This does not deny smaller boundremnant. Parent geometric_run_001 hard-address-space launch failed on macOS and is retained; use successful retry. Root should read proof/code before citing. No physics files changed.

14focused directory tests passed; code/ledger reviewed independently by equation_selection and kernels/remnant implemented and tested by diagnostic_design. The full physical initialstate, continuum limit, universal100pccore and fullcanonicaltheory remain unproved.
