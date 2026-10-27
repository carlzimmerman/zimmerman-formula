# MCP-20261022 continuation handoff

Base3d82af0a7eb241322237e1ca1257fc9debddd372; predecessorCS-20261022. Owner/write scope: this chat / this directory only. No .mathbox ledger initialized. Original joint target remains open. Read RESULT.md, AUDIT.md and four contracts before further runs.

New durable results:
1. Mi=m+eta/3 integral|gradP|²+Mchi/3 integral|gradchi|²; beta=m/Mi. Conditional dilute core dynamics is Vlasov-Poisson with beta force, not automatically ordinary dust. Fitted canonical core gives(Mi-m)/m=.184346878 eta rho_scale in fixed-chi limit.
2. Abundance n=F rho_c/m is a constraint only. At declared Omega_c=.25,H0=70 and inherited fitted m1.095e7Msun, n0=3104.8F/Mpc³. F,m and initial phase-space density are not selected. The smooth quasistatic instability has no finite fastest-growing k.
3. Positive Plummer DF derived/checked. A finite n3 polytrope and infinite-tail Plummer with identicalM,E demonstrate that those moments do not select the spatial profile. This is a collisionless equilibrium nonselection result, not a full-theory formation impossibility theorem.
4. Cluster common population over Newtonian baryons: M2.181e14Msun,b.5805Mpc, ~19.9million dwarf-sized cores; INNER observed/model1.834±.438, OUTER1.085±.149. Gas/R500 scaling similar. Favorable coarse shape test, not a predicted inventory or self-consistent baryon/kinetic equilibrium. Full law PLUS population overshoots OUTER (A~.74/.73); keeping galaxy law but replacing cluster response needs an actual environmental/phase derivation.
5. Central filling~.00338; geometric overlap interval~26Myr. Tidal stretching small, but collision/field interaction cannot be assumed negligible. Need an action-derived collision kernel, not a geometric destruction claim.
6. Same mean population density makes a small illustrative galaxy force correction, yet gives only.00338 expected dwarf cores inside321.5pc if independently sampled. Central dwarf occupation remains unpredicted. Earlier dwarf fits remain conditional isolated/law-plus-core fits.
7. All-core growth beta>=.996992 for99% retention in the full-duration EdS limit, but fixed-size all-core population at recombination is invalid (filling577). It becomes <1% mean filling only belowz27.5 atF1. For diffuse-to-core conversion atz10,beta1, final amplitudes .999500(k.1) and .955659(k1). Late conversion does not restore early diffuse suppression. Matching/size/fraction histories remain inputs.

Route status / no-repetition rules:
- Single central cluster core: earlier scoped shape failure remains; do not rerun.
- Extended cluster population: open and shape-compatible when it supplies the dark component. Do not report fittedM,b as derived or add it to already counted cold inventory.
- Abundance/distribution selection: not supplied by equilibrium, virial moments or Vlasov. Next work needs a specified parent-action parameter set and cosmological initial state, then formation/merger/transport with mass, momentum and energy budgets. Core-core scattering and stable traveling solutions must precede claiming a collisionless halo. This is deferred for missing physical specification, not exhausted.
- Galaxy/dwarf preservation: requires a joint baryon + core + diffuse-medium solution and central occupation mechanism. Transferring a density or a catalogue label is not that derivation.
- Cosmology: use formation_run rather than claiming physical all-core-from-z1100 growth. Full FRW/radiation, formation fluctuations/compensation, and late nonlinear transfer remain open.

Reproduction (repo root):
    python3 sol61_push/moving_core_population_2026_10_22/checks.py --output /tmp/population_checks.json
    python3 sol61_push/moving_core_population_2026_10_22/transport.py --output /tmp/population_transport.json
    python3 sol61_push/moving_core_population_2026_10_22/selection.py --output /tmp/population_selection.json
    python3 sol61_push/moving_core_population_2026_10_22/formation.py --output /tmp/population_formation.json
    MPLCONFIGDIR=/tmp/moving_core_mpl python3 sol61_push/moving_core_population_2026_10_22/plot.py
Use the four runner contracts for hash-preserving provenance; transport/formation consume run/result.json. Current evidence:run16checks,transport_run4,selection_run3,formation_run3;26total. All manifests completed and validated, no active jobs. CHECKPOINT_SHA256.json indexes this checkpoint and the predecessor records used for context. Self-review only.
