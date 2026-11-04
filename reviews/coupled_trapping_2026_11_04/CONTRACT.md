# CT09 coupled capture and depletion

User authorization, 4 November 2026: continue the coupled trapping/depletion
calculation at weak coupling, testing simultaneous vacuum survival, removal of
heavy charged particles, and a cold photino population. Base Git revision:
`285353a57bc1c21662c5565830bbc97ac5b0f7f9`; actual TP06 source hashes, rather
than the moving shared branch alone, fix the numerical ancestry.

Read-only starting evidence: ../gravity_completion_2026_11_03/HANDOFF.md,
thermal_kinetic/STATUS.md and DERIVATION.md, CHARGED_RELIC.md, thermal/STATUS.md.
Do not rewrite those records. All new work belongs in this directory. No Git
mutation, new portal, package installation, production queue, or message to
external parties is authorized by this calculation.

## Target and conventions

Start e=h=lambda=.003, g=sqrt(29/200)e, both recorded canonical and protected
gravity packets, and conditional initial frozen FD charged population with
xi=T_hidden/T_SM=.02. Explicit variations are diagnostics, not inferred
initial conditions. Use exact physical charged masses and vertices as far as
available. Signed U1 charge is conserved; pair number need not be. Neutral
parents that decay back to charged particles are conversions, not depletion.

Success requires one energy- and charge-consistent history through the
equilibrium gap and into the outer cold vacuum, charged rest energy below
10% of rho_DM/s=.44e-9 GeV, photino abundance near the remaining DM budget,
and an explicitly computed cold momentum distribution. A reduced collision
network, absorption bound, stationary minimum, or finite grid alone is partial
evidence. Keep omitted channels and distribution closures explicit.

## Joint dependencies and parallel packages

1. `kinetics/`: coupled scalar and occupation evolution; first test actual
   reaction feedback, then an averaged extension across Hubble cooling.
   Occupation/field energy exchange must be counted once.
2. `microphysics/`: microscopic irreversible exits, charged pair annihilation,
   interconversion and changing lightest charged state. Determine which rates
   can enter a controlled kinetic history; do not label neutral cascades loss.
3. `photino/`: actual charged-to-photino source, stable companion accounting,
   abundance and momentum/coldness implications, and independent necessary
   constraints on any coupled history.
4. Coordinator: reconcile collision closures, independently verify decisive
   invariants, follow newly identified discriminating routes, and maintain a
   single live README plus a precise continuation handoff.

Every numerical experiment has a prior finite contract, exact execution
inputs, fresh v2 runner output, one numerical thread, wall<=240s and CPU<=235s
per job, measured RSS, and numerical/invariant controls. Preserve failed
attempts with their original source hashes. No macOS RLIMIT_AS/affinity caps.
No universal no-go from a finite scan. No complete spectrum claim from the
uncomputed transverse SUGRA 1PI fermion/current coefficient.
