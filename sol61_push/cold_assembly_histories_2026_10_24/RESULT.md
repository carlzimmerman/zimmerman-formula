# CCT-004: histories change the profiles, but do not close the budgets

Original target remains OPEN. Five bounded simulations test whether a generated envelope can retain cold mass/spin under different gas rearrangement histories, while paying for the external work. Same cold initial patch, eta=.7, gas mass .2, stellar source .02, source expansion 1->5->1, and selective two-potential coupling in every run. No galaxy-specific amplitudes, cold collision term, uncounted friction, manual mass-retention cap or feedback efficiency was fitted.

These are prescribed dimensionless gas histories, not assembly histories derived from Draco/Sextans/Fornax/Leo I data. No cold accretion, cosmological initial spectrum, host orbit, live gas hydrodynamics or baryonic recoil is represented.

## What the experiments distinguish

| history | initial cold stock inside r<3 at T60 | cold mass removed | inner specific spin final/initial |
|---|---:|---:|---:|
| quiet, gas stays compact | 84.41% | 4.76% | .650 |
| three early rapid-expansion/slow-return cycles | 63.39% | 6.79% | .630 |
| same cycles late | 65.39% | 5.96% | .520 |
| slower symmetric early cycles | 67.77% | 6.41% | .651 |
| early, padded box at matched dx | 64.77% | 6.71% | .642 |

Every run gains central mass relative to its diffuse initial condition, but none meets the stated 50% specific-spin reduction, late-mass stationarity and old-Sextans retention targets together. The late case's .520 spin ratio is close to the toy .5 line and is not a robust physical exclusion on its own; its large excess loss and insufficient old-Sextans central stock are separate failures.

Quiet assembly holds a denser cold profile than bursty assembly. The early/late/symmetric histories lower the test-aperture cold mass by about 20–25% relative to quiet, despite identical cold initial conditions, eta, gas mass and scale excursion. Thus a physically counted external potential can generate nonhomology without binary collisions. It does NOT demonstrate the much stronger selective outcome required by the four-dwarf reference.

The older catalogue-B0 Sextans target places .98854 of its remaining stock in the source aperture and leaves .01146 available outside it. These simulated trajectories retain only .932–.952 total mass at all by T60. If their boundary removal is interpreted as irreversible escape and their normalisation as that stock, this branch already fails before all the remaining envelope could accrete. Boundary removal is not independently certified physical escape; returning material would require a new evolved trajectory, not a ledger correction. The newer Sextans population/selection mass problem is still unreconciled.

## The energy and spin receivers are explicit

Gas mass is conserved; its Plummer scale changes. The cold equation contains the resulting time-dependent baryonic Newtonian potential. External work is measured as integral rho_c delta Phi_b with two fixed-state switches around each midpoint evolution, so

    E_final + E_removed - E_initial = W_gas + numerical residual.

W_gas is 0, .006043, .005497, .003252 and .005557 in the table's order. These are cold-field work receipts, not the full energy cost of gas motion, a supernova budget or a derived star-formation efficiency. The agent driving the gas is external. Cold energy includes the full integral rho_c Phi_b plus one-half of its self-potential energy. Neither gas work nor cold mass is created by the phase law.

Mass-ledger residuals are <1e-8; relative energy/work residuals are <1.1e-4 of initial |E|. Initial late/quiet angular ledgers pass 2%; early and slow base boxes fail (2.84%, 2.55%). Padding early reduces the angular residual to .1415% while retaining the qualitative high-loss/insufficient-core outcome. Physical isolation, positive outward energy at infinity, late-history padding and time-step convergence are not certified. Failed base gates remain failed.

## Stellar response is not free

512 identical massless stellar tracers in each run feel the cold Newtonian field and the baryon-only extra law from the stated bridge. Paired frozen-initial-potential tracers check initial-orbit drift. These are truncated Plummer-radius/tangential-velocity samples, NOT equilibrium distribution functions of the nonspherical evolving galaxy. The finite stellar source remains prescribed and does not recoil with them. All tracer orbits stay inside the declared domain margin.

Compared with the quiet case, late-time half-mass-radius response ratios are 1.179 (early), 1.470 (late), 1.158 (symmetric), 1.174 (padded early, after its own frozen-control normalisation). One-dimensional velocity-variance ratios are 1.046, .884, 1.080 and 1.041. Variance is sigma^2, not sigma. A larger stellar distribution can have lower velocity variance after energy injection; the .884 number is not evidence of no heating. These are response flags, not observed Fornax/Leo I exclusions or a fitted stellar likelihood.

The natural next observational constraint is therefore the joint cold-profile AND stellar-size/kinematic response to a data-constrained gas history. The current prescription cannot simply clear cold mass from Fornax/Leo I while declaring the stars unchanged.

## Four-dwarf library diagnostic

Allowing different histories breaks the previous common-profile assumption. The saved response library nevertheless fails an optimistic necessary test under the older stocks and a common physical eta. Length units obey L_i=eta_phys^2/(eta_code^2 G M_i), so physical aperture arguments scale as M_i R_i. This uses the cold equation only; the fixed code-a0 stellar response is not transferred to observed stellar sizes or calendar ages.

Even the largest retained mass in the library is below Sextans' .98854 target. To meet it with the untracked removed material, and assuming that removed material stays outside absorber onset r=12, Sextans' mapped aperture must be at least 12. Fornax's aperture would then be at least 664–670 and Leo I's at least 41.7–42.0. All saved retained fields lie inside radius 34.65, so either galaxy would enclose at least the smallest retained mass fraction, .9321, regardless of which saved history was assigned. The older required fractions are only .0131/.00546 for Fornax and .0345/.0290 for Leo I. The retained cold masses therefore exceed those reference requirements by at least factors 71/171 and 27/32.

This is a conditional central-value response-library contradiction, NOT a universal assembly-history or wave-field no-go. It permits an arbitrary history choice per dwarf only as an optimistic diagnostic, not a proposed selector. It assumes no return of removed material into r<12, the older stock and baseline, the tested physical coupling/scaling, and the saved dimensionless evolutionary stages. Very different generated profiles, inventories, gas histories, tidal evolution or returned waves can change the premise. The actual cold inventory of the new coupling must be derived again; these older stocks are not automatically its predictions.

## Gravity was counted once, but the framework remains incomplete

Cold mass sources Phi_c once. Phi_b contains the prescribed stars+gas once. The cold wave evolves in Phi_c+Phi_b; stellar tracers additionally feel Xi_b, whose source contains only baryons. This implements the Newtonian limit of the NEW, selectively coupled action in ../continuous_cold_envelope_2026_10_24/COUPLING_BRIDGE.md. No cold source is added to Xi_b or added again after solving its Newtonian field.

That bookkeeping avoids a duplicate force in this candidate. It does not suppress real cold gravity, derive eta or a0, establish a covariant healthy action, preserve the old nonspherical galaxy fits, or determine cosmological supply. A gas history cannot repair those obligations by itself.

## Continuation

The useful positive result is a measured, energetically accounted way for histories to produce different cold profiles and stellar responses. The tested histories do NOT produce a high-retention, stationary, low-spin Sextans-like core while allowing small Fornax/Leo I central cold fractions. Next work needs observationally constrained gas/orbital histories and inventory, including the energy source for gas motion, to generate much stronger nonhomology without excessive stellar response. Extending the history library without those constraints would become free fitting. No claim covers all possible histories, and no theory-completion claim is made.

All five jobs finished, peak memory <241 MB, one numerical thread. Shared heavy jobs and frozen criteria/publications were untouched. No automation or external publication/push was performed.

Reproduce simulations from runs/RECEIPT.json; replay analysis with `python3 sol61_push/cold_assembly_histories_2026_10_24/analyze.py` and small forcing/bookkeeping controls with `python3 sol61_push/cold_assembly_histories_2026_10_24/verify.py`. Parent equations and failed receiver routes are retained separately.
