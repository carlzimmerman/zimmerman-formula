# Handoff: photon recycling implemented; finite collision chemistry open

Base d35dc672f15a379c58ef78abf14615194e0dae91. Publication branch remains
codex/two-state-mechanism-findings-2026-10-24. Pinned inputs immutable.

Active code: photons.py (dynamic radiative network), fast.py (singular
collision-equilibrium limit). Both use the preceding refined23-level spectrum.
Four science runs and two figure runs complete;57 trajectories total, with
scope/convergence distinctions in AUDIT.md. Figure v2 supersedes layout only.

Key findings:
- Explicit photon storage, absorption, stimulated capture and sphere escape
  conserve energy and charge; no assigned radiation temperature.
- Photon recycling produces a derived photon-mediated T+C <-> 2A channel.
  This is distinct from direct electron-impact dissociative recombination.
- At alpha=.2,mC=10MeV,M/mC=100, refined charged molecular fractions for the two
  dwarf/disk/cluster profiles are4.11457e-7,2.25955e-5,.0415933,.132425.
  No80%/20% success; cluster molecular fraction exceeds disk.
- Three of six radiative choices pass all stated screens; fast-limit six of six.
  Fast-limit maximum disk fraction~1.22e-26; conditional all-density equilibrium
  mass cap .559546302. Previous irreversible4.42% cap does not apply to recycling.
- Main maximum energy-ledger error1.20e-15 E_H/pair, charge1.12e-16.

First unresolved microscopic implication:
The one-electron g/u spectrum does not determine two-electron neutral channels
or scattering couplings for direct DR, associative ionization, impact breakup,
three-body formation or neutral/negative-ion chemistry. Detailed balance fixes
ratios only. Rescaling ordinary hydrogen is a separate approximate route, not a
first-principles solution at mass ratio100. SOURCES.md records the source check.

Continuation routes still OPEN:
1. Build neutral/negative-ion electronic surfaces and channel couplings; derive
   state-resolved finite collision S-matrices at the SAME particle masses and
   interaction. Include product electronic excitation in the energy ledger.
   Do not assign a total ordinary-H2+ DR coefficient to every present state.
2. If using published rescaled rates as a diagnostic, label and quantify the
   mass/state/temperature assumptions; do not claim the missing amplitudes solved.
3. Replace the homogeneous moment closure by spatial radiative transfer before
   claiming an opaque halo result. Preserve frequency, energy and charge.
4. Couple populated chemistry, countercharge transport, gravity and rotation;
   demonstrate actual tethered orbits and test RAR. Not yet reached.

Do not imply the two kinetic limits bound every intermediate trajectory. Do not
count charged molecules automatically as tethered matter. No manuscript edits.
