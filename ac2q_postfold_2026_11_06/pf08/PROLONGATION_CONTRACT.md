# Spatial refinement at a valid checkpoint

Fourier prolong only from a valid checkpoint, never a stopped state. Transfer
beta and adapted momentum, preserving lambda and independent mean momentum;
transfer polarization derivative as an initial guess then solve all constraints.
This is not new fine-grid initial-data evidence: unresolved modes before the
checkpoint cannot be recovered. Compare against lower resolutions and retain
all compatibility, domain, canonical-rate and spectrum stops.
