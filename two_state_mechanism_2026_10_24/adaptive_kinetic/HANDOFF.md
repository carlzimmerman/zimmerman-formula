# ADAPTIVE-KINETIC-2026-10-24 checkpoint

User requested adaptive kinetic local capture, same conservative3D field and live
gravity, rotating T formation with dwarf/cluster F retention and no type switches.
Implemented spatially adaptive octree kinetic collision quadrature and independent
velocity samples, plus independent analytic benchmarks and live controls. Physical
formation objective and live continuum convergence remain OPEN.

Final new sources: octree.py, kinetic.py; imports predecessor field3d_capture files
unchanged. run.py supplies base/space/velocity/cell/time/seed suites; shape.py and
high_resolution.py add controls. Gaussian field exact self +3D nonlinear
interference retained. Full constant softened gravitational self energy added for
invariance under uncharged velocity replication; forces unchanged. Cells affect
only collision rates, so regridding does not change Hamiltonian energy.

Local Boltzmann normal-flux operator gamma=C*mB*incoming/Vcell replaces physical
neighbor coincidence. Physical h=.1kpc enters the local-limit assumption, not
cell support. Do not call macro separations physical collision distances.
Octree splits by maxwidth and crowding; never expands to find a partner. Central
impulses conserve pair P/L and finite field work plus radiation receiver. Separate
T/F/B trajectories. No vorticity gate, global pump, type-dependent parameters or
prescribed T density. Effective collision-mass ratio5.364 remains an assumption.

Independent benchmarks: uniform and Gaussian density/velocity integrals. Finest
Gaussian rate0.989526 of exact, standard error0.007832 over8 seeds,8192 spatial
nodes/species,2 velocities/node,width cap.25. Coarse64-node Gaussian rate~.70;
particle count alone at coarsewidth stalls~.95. Cold compression creates a spurious
finite-cell rate that halves when width halves; preserve this error control.
Fixed-partition boost/rotation tests are not rebuilt-grid rotational invariance.

48 completed default-coefficient formation runs,2 completed seeded-field controls.
Base8,space8,velocity8,cell4,time4,seed4,shape8,high4. Formation lasts2 initial
Tdynamical; most seed11,seed-control29. Highest live resolution256 spatial nodes
with2 independent velocities each =>512 samples/species; do not conflate this
with the8192-node manufactured benchmark. All default inputs use same coefficient.

Final default result: maxT1.5625%; boundF98.4375–100%;10 proposals,7 captures,0
releases. Largest normalized energy error1.03370e-5 including active-field controls;
collision mismatch3.023e-18. Best RAR RMS.164622dex and max.354111dex. No joint target
success. In high-res large-system pair unordered has2/512T,rotating0; coarse choices
sometimes favor rotation. Small counts do not establish either population ordering.
Maximum recorded default opacity proxy.293681; max actual individual hazard-step
product.00971966. Proposal exposure per sample never exceeds.016989 in defaults.

The optional100x-rate stress probe was intentionally interrupted through its exec
session after becoming spatially under-resolved (recorded opacity~9.25). Runner
finally stops/waits for child, but KeyboardInterrupt skips final manifest write.
run_stress has partial exploratory files and INTERRUPTED.md, NO completed manifest;
exclude it from validated formation evidence. Do not invent before/after hashes.
A separately bounded stress_screen run shows initial large-system/cluster opacity
3.263/.5439 already above chosen1/3 reference screen. It is a numerical applicability
screen, not an empirical mean-free-path constraint or a physical no-go theorem.

All finalized manifests validated; all jobs ended. Analysis only stderr is a font
cache notice. Final results/figure run_analysis. No source changes to predecessor,
no commits, manuscript edits, external publication or independent referee claim.

Next routes: scalable gravity/field evaluation to permit genuinely converged live
phase-space sampling; dense-collision treatment before strong-rate claims; and a
physically justified durable binding/transition mechanism with reciprocal work and
angular-momentum transfer. The isotropic local kernel has no direct dependence on
global circulation coherence. Field smoothing, packet reaction granularity,
quasistatic longitudinal closure, local-limit assumption, radiation closure,
long-time evolution and actual observational fits remain independent obligations.
Do not claim that successful collision-integral benchmarks solve those physics.
