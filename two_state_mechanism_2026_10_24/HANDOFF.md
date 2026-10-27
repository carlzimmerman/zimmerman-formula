# TS-2026-10-24-A continuation

Original target remains open: simultaneous dwarf/cluster excess and disk RAR.
Base checkpoint is the Git SHA in DESIGN.md. All new work is confined to this
directory; current evidence is pinned by the four final run manifests.

## Executed routes and their scopes

- Fixed mixture / static coexistence: derived the exact free-source correction.
  This is an obstruction to treating extra F mass as invisible to the RAR.
- Conservative conversion impulse: specified the energy difference and
  demonstrated finite-time retention in a spherical softened toy model.
  This closes neither the receiver's physical origin nor the conversion rule.
- Common-gap reversible selector: implemented rates and tested chemical
  stationarity. The declared frozen-profile separation fails for any common
  nonnegative bath energy. This selector is rejected; the broader two-state
  program remains open.

## Next discriminating construction

Add a physically specified state-dependent interaction or metastable barrier,
not a galaxy-type label or separately fitted fraction per object. It must
change the failed implication: the same gap/bath otherwise converts disks
before it can make dwarfs mostly free. Derive its energy and rate together,
including the receiver and its backreaction, before a data fit.

For orientation, in a purely irreversible constant-rate toy process starting
all T, q(t)=exp(-Gamma_TF t). Requiring q_dwarf<=0.1 and q_disk>=0.95 gives

    Gamma_dwarf/Gamma_disk >= [ln(10)/(-ln(.95))] t_disk/t_dwarf
                            ~=44.9 t_disk/t_dwarf.

This is a necessary rate contrast under those assumptions, not a derived
mechanism. If back-conversion must leave 90% F over a retention interval,
Gamma_FT t_retention <= -ln(.9) in the isolated irreversible reverse-process
test. General simultaneous forward/reverse evolution needs the full equation.

For a locally varying equilibrium offset instead, the frozen profiles require

    epsilon_disk - epsilon_dwarf >= 49652.26 + 5.14166 theta

in (km/s)^2 for the chosen q thresholds, using the most constraining disk.
This quantifies the missing environmental dependence; it does not license
assigning those offsets by hand.

Deferred obligations: microscopic interaction and independently specified
parameters; coupled live T/F evolution with conversion and receiver;
nonzero angular momentum and 3D stability; stiffness and tidal fields;
reservoir/catchment formation; age-matched observational tests. The current
frozen-profile chemical test cannot adjudicate those extensions. None is
marked exhausted. Resume with a written interaction that changes the failed
selector, then first test disk contamination and conserved energy.
