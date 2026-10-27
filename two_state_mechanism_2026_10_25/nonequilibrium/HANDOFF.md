# Handoff: nonequilibrium molecular path remains unsuccessful

Parent publication97b95ad15df9d49ca2f24da3c0c824277981be48 on
codex/two-state-mechanism-findings-2026-10-24. This stage is ready as a bounded
research finding, not a closed research program or a successful galaxy model.

Current implementation: electronic.py -> spectrum.py -> kinetics_v3.py.
Original kinetics.py and v2 intentionally remain as failed provenance artifacts.
Use refined run_refine/results.json for production rates. Read README/AUDIT
before interpreting any raw scan. All pinned inputs immutable.

Results:23 levels; D0=.0809956548 E_H; formation-rate refinement .023%;
228 finite-age proxy runs at57 shared parameter choices,12 common passing
screens,0 target successes. Best passing disk charged-molecule fraction
.0002916191 at alpha=.15,mC=3.16228e8 eV,M/mC=100. Charge and energy conserved.
An interpolant-wide radiative-subnetwork bound caps molecular mass at.04414146
for T in[1e-8,.05], independently of density and duration. It is conditional on
the network, absence of photo-recycling and the numerical microscopic rates.

Next discriminating work:
1. Evolve photon number/energy with the same photoelectric dipoles where opacity
   invalidates escape; include reabsorption and spatial or controlled group
   transport. Do not apply the irreversible kinetic bound there.
2. Derive/test dissociative recombination and collisional breakup from this parent;
   allow neutral molecules/excited states. Spin/exchange and mass corrections
   need a specified microscopic particle model.
3. Only after a viable populated charged phase is demonstrated, couple this
   actual chemistry to countercharge transport and gravity/rotation. Do not label
   charged molecules tethered without orbital binding/force evidence.
4. Compare full acceleration curves, baryon relation and free bound mass; this
   remains entirely open.

Do not retry a density-only or time-only scan of the same irreversible network:
the bound already addresses that. M,alpha,mC remain hypotheses; no unique scale
has been derived. Do not claim the fixed-density gas scans simulate disks.
