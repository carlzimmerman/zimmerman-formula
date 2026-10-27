# Photon recycling and missing collision channels

Base checkpoint d35dc672f15a379c58ef78abf14615194e0dae91.
User target: physical assembly/dissociation, photon trapping, conserved charge and
energy, fewer independent parameters, common equations for dwarf/disk/cluster
profiles. Actual galaxy formation/RAR is the unresolved parent target.

Implementation choice: retain the computed M/mC=100 Coulomb g/u spectrum and all23
bound levels. Use frequency-resolved photons with spontaneous/stimulated capture,
atomic photoionization and molecular photodissociation. Photons store number and
energy and can escape a homogeneous sphere. The sphere is a transport closure,
not the earlier3D live-gravity code. No morphology flags or fitted opacity.

Alternative1, borrowing ordinary-hydrogen chemistry rates by dimensional scaling,
is a useful approximate literature model but does not determine state-resolved
rates at mass ratio100. Alternative2, computing two-electron MQDT/scattering,
is the correct microscopic extension but requires new electronic surfaces and
couplings. Neither will be passed off as already obtained from the one-electron
spectrum. Selected approach: explicit photon dynamics plus a separate
rapid-collision-equilibrium limit with the same conserved energy and chemistry.
This is partial progress on the requested finite-rate full network.

Three routes/checks:
1. Multigroup photon recycling from existing dipoles: compare optically thin
   limit, Planck/Saha stationarity, frequency/time refinement, energy/charge.
2. Fast missing collision chemistry: reversible ionization/three-body formation,
   dissociation/association and dissociative recombination/associative ionization
   impose one thermochemical equilibrium manifold. Derive that manifold and
   evolve its radiation. No independent collision amplitude is introduced.
3. Structural reduction: conservation, detailed balance cycle identities and
   equilibrium molecular abundance bound. This bound applies only to fast
   chemistry, not the general nonequilibrium photon network.

Implementation sequence: derive and test photon quadrature/stoichiometry;
execute finite-rate radiative parcels; construct fast-chemistry energy inversion;
compare both limits with common mass/radius inputs; audit numerical convergence;
record missing microscopic information and publish findings on the existing branch.
No claim that two limits bracket every intermediate-rate trajectory. Neutral
molecules, negative ions, excited atoms and their scattering remain outside both
networks; this is explicitly NOT complete Coulomb chemistry.
