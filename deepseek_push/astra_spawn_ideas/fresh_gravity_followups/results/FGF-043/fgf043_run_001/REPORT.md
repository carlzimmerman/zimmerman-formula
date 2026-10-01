# FGF043 proof-only report

The inherited static velocity concentration has been tested as one time-independent approximate family on a fixed time slab. The bare cubic-moment mismatch was already proved in the pinned FGF042 independent derivation and is not new evidence here. The new result checks its actual equations, full local energy current and initial/wall terms.

Mass residual is O(N^-2) and separate/combined momentum residuals are O(N^-1) in the declared spatial Lip* norm, uniformly in time. Both actual field residuals are exactly zero; the primitive matter residual also tends to zero weakly. Initial full excess energy is O(N^-1), with no initial energy-density defect. Each state's total energy is exactly constant, so the global scalar energy inequality holds. Walls are unchanged and all perturbative wall currents vanish.

Nevertheless the actual full local-energy residual tends to F_* partial_x delta_(x*) times dt, with F_*>0. Cubic transport produces it; enthalpy and potential transport are explicitly included and vanish together. The initial energy terms cannot cancel it. The residual is sign indefinite and therefore also fails a vanishing-error local dissipative inequality. These are approximate states with a failed local-energy acceptance test, not exact solutions or energy creation.

One bounded-amplitude control removes the defect. For the general FGF042 zero-excess class, the EXTRA condition |j|<=V n with one fixed physical V controls the entire matter energy current. The proof handles vacuum and unbounded densities explicitly: entropy convergence gives integral |n log(n/rho)|<=D(n|rho)+||n-rho||_1, and the velocity cap converts this into enthalpy-current convergence. Kinetic transport is bounded by V times kinetic energy. No action change, physical cutoff or preservation of the velocity cap is asserted.

The proof was frozen before new root/reviewer proof or previews. All nine task ancestry hashes matched. No numerical run, manifest, service, parameter sweep or literature mechanism was used. Both a0 hypotheses, actual signed Q source and separate vacuum/frozen-H/evolving-H references remain explicit. No RAR/M, metric/photon/DOF, physical reservoir, empirical or theory-closure result follows.

The surviving gap is a concrete same-action approximation with a justified local energy-residual estimate, including initial/wall traces. Merely adding a scalar global budget or repeating the static moment mismatch is exhausted. Dynamics need not preserve the sufficient velocity cap, and finite nonzero-energy compactness remains open.
