# Assembly and live spherical gravity: declared experiment

Base revision: 70cf9990884b9f6896337d73d54fdaf0b5de4901.
Parent evidence: ../vorticity_gate/run_angular{64,128,256} and run_diagnostics.
Goal remains formation of tethered disks plus sufficient retained free mass
in pressure-supported objects with one interaction and no type assignment.

This checkpoint tests a necessary reduced-model obligation. Live spherical
shells move under the derivatives of a common energy, including self-gravity,
centrifugal support and the tether field. They can cross and expand. A single
collective phase is an optimistic coherent-phase restriction, not a 3D disk.
It cannot demonstrate disk morphology or spatial phase stability.

Routes and discriminators:
1. Passive assembly: changing gravity alone cannot move exactly x=0 under
   the parent's gradient dynamics (its phase derivative vanishes). Test the
   no-cross-coupling control. This obstruction only rules out that closure.
2. Reciprocal contraction/phase dissipation: radial contraction pumps x while
   the equal reciprocal force pays its energy cost. Integrate live shell
   trajectories and receiver energy. This is the main constructed candidate.
3. Energy sufficiency and retention falsification: compare positive formation
   work against lost mechanical energy; measure snapshot-bound free fraction
   and actual monopole acceleration residual instead of imposing the RAR.

Same numeric mass/size profiles as parent, crossed with angular-momentum
coherence f=0,.3,.95. Coherence is the net vector angular momentum divided by
the sum of its constituent magnitudes. Tangential kinetic energy is held fixed
while orbit orientations differ. All equations use C=f², not object names.
Spherical gravity conserves each angular momentum, so this C stays constant.
It is a new collective approximation to ordered motion, not the parent's
local vorticity estimator. Net angular momentum does not prove a disk.

Initial baryon shells sample a Plummer sphere truncated at 10b; medium shells
sample the parent's finite reservoir profile. Both expand initially by 3.
All runs begin exactly free. Initial radial speed=-.3 vc and tangential
speed=sqrt(.7) vc, with vc from the actual all-F gravitational energy.
No conditional removal of baryons or assignment of dark states is allowed.

Uniform qT=sin²(pi x/2), qF=1-qT. Field energy is integrated over all space;
the collective barrier beta C sin²(pi x)/pi² times uW'(u) also spans that
field. This collective extension differs from the earlier material-domain
barrier and is not an independently established microscopic interaction.
Spatial phase stiffness vanishes in this constrained uniform-phase sector.

Rayleigh functional R=Gamma(vbar + A C xdot)²/2 + eta xdot²/2.
vbar is the baryon-mass-weighted radial velocity, Gamma=10 Mb/tdyn,
eta=.01 |Ugrav(initial)| tdyn, A=alpha times initial baryon half-mass radius.
beta=20; alpha is scanned at .1,.3,1,3 with common values for every profile.
The zero-coupling control is alpha=0. All parameter choices are exploratory.
Qdot=2R; Emechanical+Efield+Ebarrier+Q is conserved analytically.

Numerical gates: finite-difference energy forces and phase derivative <1e-4
relative; instantaneous energy identity <1e-9 scaled; integrated relative
energy error <1e-4, refined time tolerance and quadrature if needed. Record
domain/saturation failures rather than clipping the field or energy.
Initial pilot: 12 shells per species, 512 logarithmic quadrature cells,
30 initial half-mass dynamical times. Compare resolved candidates at twice
shell/quadrature resolution; hold initial profiles and physics fixed.

Illustrative target: high-coherence qT>=.95 plus actual monopole RAR residual
<=.05 dex over baryon radii .5–5 current half-mass radius; low-coherence
snapshot-bound free mass>=.9 of initial medium and >=one baryon mass.
These are engineering thresholds, not observational mass requirements.
Actual dwarf/cluster sufficiency requires observed profiles and uncertainty.
Bound classification uses instantaneous Newtonian shell potential for free
matter; it is not a proof of asymptotic retention in a changing potential.
