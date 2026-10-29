# Frozen group-cell quadrature/inventory preflight

Extract original corrected X43 group functions from saved L3.5 executed source,
P4 Hernquist grid/class_stats, original EM1 CLASS-background block and original
X43 EPS construction. No X30/SPARC grading or source output writes. Retain
original FP0 acceleration and every source unit constant, including differences
between group and EM1 solar masses/G. Pin original source/data before arithmetic.
The external Tian TSV is read-only and its absolute-path before/after hash is
recorded by the child; publish the selected63 input rows for reproduction.

At saved L3.5 recover189cells (63 times dlM=0,+.01,-.01), exact source core
column/floor/flag and compact-root parameters, baryonic/halo effective-mass
profiles and velocities. Build a positive common quadrature kernel from actual
XG,LXG,RHO_H. Its mass mapping is s2=(G540/a)*dot(kernel,Meff), with
kernel=trapezoid node widths*4*pi*XG^2*RHO_H/3. Verify all189 against original
source trapz velocities to1e-11 dex and relative s2 to1e-12; these are diagnostic
tolerances, not interval padding. Reconstruct actual grade against run_001 L3.5
all numeric statistics to1e-10 and exact verdict/PASS/count. Independently check
pairwise variance identity and mass slopes. No new calibration or fitted number.

Inventory switch thresholds via Lswitch=3.5*(floor/unflooredColumn)^(.8) for all
189cells. For first future interval[3.5,3.5001], flag any event within relative
1e-10 of either boundary as uncertain. This is only a numerical inventory;
certified interval tests need separately justified coefficient/branch bounds.
An event or uncertainty is never silently ignored. Source X43 EPS versus X53
coarse-column differences are recorded as a pipeline-substitution control.

Require finite positive quadrature/mass arrays, source flags consistent with
same column, exact63/189coverage and stable hashes. Deliberate1%mass/weight
changes and inverted flags must fail diagnostic controls. Save actual EPS tables,
selected catalogue rows, native kernel, masses and cells. Self/adversarial review
must independently recompose all189linear masses and63group statistic, including
changing sample variance and systematic slope. One thread, wall600/CPU480.
No interval exclusion, monotonic Z, analytic EPS certificate or global claim.
