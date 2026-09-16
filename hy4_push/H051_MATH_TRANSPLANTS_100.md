# H051 — 100 MATHEMATICAL TRANSPLANTS
Real, named machineries mapped to unsolved problems. Each has STEPS an agent
executes and a SEARCH target to verify current work. No invented citations.
RULES: both a_0 footings; measurement AND threshold separate; Lean exit 0 with
ZERO sorry (delete unprovable theorems).

## I. PDE (M001-M010)
**M001 De Giorgi-Nash-Moser.** fprime <= 2 sqrt K -> 0: the EOM is DEGENERATE
elliptic, not uniformly elliptic. (1) write div[A(grad phi) grad phi]=0, A=fprime;
(2) show uniform ellipticity FAILS at K=0; (3) determine if solutions are C^alpha
or singular; (4) if singular, H045's ghost may be a regularity artifact.
SEARCH: "degenerate elliptic regularity De Giorgi".
**M002 Viscosity solutions.** (1) reformulate as HJ-type; (2) define viscosity
sub/supersolutions AT the degeneracy; (3) prove comparison; (4) gives
existence/uniqueness where classical methods fail. SEARCH: "viscosity solution
degenerate elliptic comparison".
**M003 Caffarelli free-boundary.** The G132 transition IS a free boundary.
(1) write two-zone as an obstacle problem; (2) coincidence set = r < r_M;
(3) apply Caffarelli regularity; (4) DERIVE the jump condition = Cluster Door C2.
SEARCH: "Caffarelli free boundary obstacle regularity".
**M004 Signorini / thin obstacle.** The cap truncates: a unilateral constraint.
(1) phantom mass as obstacle solution; (2) solve Signorini; (3) does the contact
set match r_cap? SEARCH: "Signorini thin obstacle contact set".
**M005 Mean-field games.** Two states = two strategies. (1) dust as agents
minimizing cost; (2) coupled HJB + Fokker-Planck; (3) does the phantom/dust
split emerge as a mean-field equilibrium? SEARCH: "mean field games Lasry Lions".
**M006 Fisher-KPP fronts.** (1) transition as bistable reaction-diffusion;
(2) compute front speed; (3) does the speed give the cluster amplitude?
SEARCH: "Fisher KPP front speed bistable".
**M007 Homogenization.** Does cosmic a_0 differ from local? (1) homogenize the
EOM; (2) compute the effective coefficient; (3) is 0.5 c sqrt(G rho_L) the
homogenized or bare value? Attacks the 22 percent (N1). SEARCH: "homogenization
effective coefficient".
**M008 Gamma-convergence.** DERIVE the deep law. (1) build F_eps; (2) show
Gamma-convergence to the MOND functional as eps -> 0. SEARCH: "Gamma convergence
variational limit".
**M009 Wasserstein / JKO gradient flow.** (1) relaxation as Wasserstein gradient
flow of an entropy; (2) derive the PDE; (3) is the phantom the minimizer?
Extends G084. SEARCH: "JKO scheme Wasserstein gradient flow".
**M010 Bakry-Emery.** (1) define the entropy; (2) compute the curvature
condition; (3) exponential convergence rate = a testable timescale.
SEARCH: "Bakry Emery criterion convergence".

## II. GEOMETRIC ANALYSIS (M011-M020)
**M011 Positive mass theorem.** H045 says energy is unbounded below.
(1) formulate ADM mass for the parent; (2) apply Schoen-Yau; (3) failure IS the
ghost, derived independently. SEARCH: "positive mass theorem scalar curvature".
**M012 Penrose inequality.** (1) horizon mass with the phantom; (2) test the
inequality; (3) violation signals instability. SEARCH: "Penrose inequality
apparent horizon".
**M013 Inverse mean curvature flow.** (1) run IMCF on spatial slices;
(2) monotonicity gives the mass; (3) consistency check. SEARCH: "inverse mean
curvature flow monotonicity".
**M014 Yamabe problem.** (1) is there a conformal frame where equations simplify?
(2) solve Yamabe on the slice; (3) separate the ghost mode. SEARCH: "Yamabe
problem conformal Laplacian".
**M015 Ricci flow.** Why is Sigma universal? (1) run Ricci flow at cluster scale;
(2) is the two-zone a fixed point or SOLITON? (3) solitons explain universality.
SEARCH: "Ricci soliton gradient shrinking".
**M016 Pinching / finiteness theorems.** (1) test pinching for framework
solutions; (2) finiteness of topological types would explain universality.
SEARCH: "pinching theorem finiteness topology".
**M017 Bishop-Gromov.** (1) effective Ricci bound from the phantom;
(2) volume comparison gives a mass-profile bound; (3) compare to -2.29.
SEARCH: "Bishop Gromov volume comparison".
**M018 Isoperimetric inequalities.** (1) apply on the spatial geometry;
(2) bound Sigma; (3) compare to a_0/(2 pi G). SEARCH: "isoperimetric inequality
Ricci manifold".
**M019 Concentration-compactness.** Solitonic carriers (Door B3). (1) energy
functional; (2) prove a minimizer exists; (3) compute its profile. SEARCH:
"concentration compactness Lions soliton".
**M020 Prescribed mean curvature.** The transition surface. (1) treat the
interface as PMC; (2) compute the shape in a cluster; (3) compare to observed
ellipticity. SEARCH: "prescribed mean curvature surface existence".

## III. PROBABILITY (M021-M030)
**M021 Large deviations.** DERIVE the 0.150 dex RAR scatter. (1) model as a
large-deviation event; (2) compute the rate function; (3) is 0.150 the predicted
scale? Attacks Q3's 0.108 dex floor. SEARCH: "large deviations rate function".
**M022 Extreme value theory.** The 2/55 RAR violators. (1) fit EVT to residuals;
(2) are violators consistent with the tail or genuine? SEARCH: "extreme value
theory generalized Pareto".
**M023 Random matrix theory.** (1) covariance of the 12 X-COP profiles;
(2) compare eigenvalue spectrum to Marchenko-Pastur; (3) separate signal from
noise. SEARCH: "Marchenko Pastur spectrum covariance".
**M024 Gaussian processes.** MODEL-FREE slope. (1) fit a GP to the cluster mass
profile; (2) differentiate; (3) cleanest -2 vs -3 test (C5). SEARCH: "Gaussian
process derivative estimation".
**M025 Information geometry.** Why n=2? (1) Fisher-Rao metric on the mu_n
family; (2) is n=2 a special point (max curvature)? SEARCH: "information
geometry Fisher Rao metric".
**M026 Maximum entropy (deepen G084).** Derive the one-half. (1) maximize
entropy subject to the virial constraint; (2) show one-half is forced;
(3) is it the SAME one-half as in Sigma and c_s^2(0)? SEARCH: "maximum entropy
virial theorem".
**M027 SPDE / KPZ.** (1) add noise to the EOM; (2) derive the SPDE;
(3) scaling exponents vs the 0.150 dex scatter. SEARCH: "KPZ universality
scaling exponents".
**M028 Exclusion processes.** (1) dust as simple exclusion; (2) hydrodynamic
limit; (3) compare to the phantom profile. SEARCH: "exclusion process
hydrodynamic limit".
**M029 Gibbs measures / DLR.** (1) construct the Gibbs measure; (2) prove
existence (DLR); (3) phase coexistence = the phantom/dust split. SEARCH: "DLR
equations Gibbs measure coexistence".
**M030 Renormalization group.** Does n run? (1) RG flow for the kernel;
(2) beta function for n; (3) is n=2 a fixed point? SEARCH: "renormalization
group beta function fixed point".

## IV. DYNAMICAL SYSTEMS (M031-M040)
**M031 Center manifold / normal forms.** (1) reduce the G132 transition to the
center manifold; (2) compute the normal form; (3) classify the bifurcation,
confirming or denying "first-order-class". SEARCH: "center manifold reduction
bifurcation".
**M032 KAM theory.** (1) nearly-integrable Hamiltonian; (2) apply KAM;
(3) surviving tori = long-lived structures. SEARCH: "KAM theorem invariant tori".
**M033 Lyapunov exponents.** Is the EOM chaotic? (1) compute the spectrum for
the two-zone system; (2) chaos would ruin predictability of the break radius.
SEARCH: "Lyapunov exponent numerical".
**M034 Fenichel / geometric singular perturbation.** (1) fast-slow form;
(2) apply Fenichel; (3) the slow manifold IS the phantom branch. SEARCH:
"Fenichel geometric singular perturbation".
**M035 Inertial manifolds.** Is the phantom an attractor? (Complements H038.)
(1) prove an inertial manifold exists; (2) show the phantom lies on it.
SEARCH: "inertial manifold existence attractor".
**M036 Equivariant bifurcation.** Does symmetry force n=2? (1) identify the
kernel's symmetry group; (2) apply equivariant bifurcation. SEARCH: "equivariant
bifurcation symmetry breaking".
**M037 Ergodicity.** (1) test ergodicity of the dust; (2) non-ergodicity
explains why both states persist. SEARCH: "ergodic theorem mixing".
**M038 Arnold diffusion.** (1) estimate diffusion rates; (2) stable over a
Hubble time? SEARCH: "Arnold diffusion nearly integrable".
**M039 N-body relaxation (the G111 spec, never run).** (1) N-body with the
framework's force law; (2) run relaxation; (3) does it reach the phantom
equilibrium? SEARCH: "N-body relaxation modified gravity".
**M040 Averaging theory.** (1) average the external field; (2) derive effective
g_ext; (3) test against the 2MRS estimate. SEARCH: "averaging method perturbation".

## V. ALGEBRA / TOPOLOGY (M041-M050)
**M041 Characteristic classes.** (1) compute classes of the field bundle;
(2) nonzero = no global section = forces a topological carrier (Door B1).
SEARCH: "characteristic classes obstruction section".
**M042 de Rham cohomology.** Conserved quantities WITHOUT Noether (since J^0=0).
(1) find closed non-exact forms; (2) their integrals are conserved; (3) this is
the unassigned dark mass (Door B4). SEARCH: "de Rham cohomology conserved".
**M043 Morse theory.** (1) Morse function on configuration space; (2) Morse
inequalities bound the number of equilibria; (3) does it give exactly TWO
(phantom, dust)? SEARCH: "Morse theory critical points".
**M044 Atiyah-Singer index.** (1) index of the ghost operator; (2) nonzero =
protected zero modes = possibly the dark sector. SEARCH: "Atiyah Singer index
zero modes".
**M045 Spectral sequences.** (1) set up for the field complex; (2) compute;
(3) read off conserved densities. SEARCH: "spectral sequence cohomology".
**M046 Operads / category theory.** (1) formalize the constraint structure;
(2) look for a universal property forcing mu_2. SEARCH: "operad universal
property".
**M047 Representation theory.** (1) TT modes as a rep of SO(D-2); (2) decompose;
(3) is the rep unique? Generalizes H017. SEARCH: "transverse traceless
representation rotation group".
**M048 Lie algebra cohomology.** (1) compute H^2; (2) nonzero = deformable;
(3) deformations give the screened parent. SEARCH: "Lie algebra cohomology
deformation".
**M049 Knot solitons.** (1) classify knot solitons; (2) their conserved charges;
(3) are they the dark matter? (Door B3) SEARCH: "knot soliton topological charge".
**M050 Homotopy groups.** (1) compute pi_n of the vacuum manifold; (2) nonzero =
stable defects (strings, textures) as candidates. SEARCH: "homotopy group vacuum
manifold defect".

## VI. NUMERICS (M051-M060)
**M051 Discontinuous Galerkin.** (1) implement DG for the two-zone system;
(2) the r_M discontinuity handled by the numerical flux; (3) robust cluster
solution. SEARCH: "discontinuous Galerkin hyperbolic conservation".
**M052 Adaptive mesh refinement.** (1) AMR around r_M and r_cap; (2) resolve the
break; (3) redo the cluster test properly. SEARCH: "adaptive mesh refinement
astrophysical".
**M053 Symplectic integrators.** (1) symplectic scheme for the framework's force
law; (2) conserve energy over 10^4 dynamical times (for M039). SEARCH:
"symplectic integrator energy conservation".
**M054 Multigrid.** (1) multigrid for the degenerate EOM; (2) preconditioner for
the K=0 degeneracy. SEARCH: "multigrid degenerate PDE".
**M055 Polynomial chaos / UQ.** (1) PCE for observables; (2) propagate the 22
percent a_0 uncertainty; (3) rank which tests are most sensitive. SEARCH:
"polynomial chaos uncertainty quantification".
**M056 Bayesian model selection.** (1) evidence for two-zone vs NFW on X-COP;
(2) the Bayes factor IS the honest verdict (C5). SEARCH: "Bayesian evidence
model comparison".
**M057 Nested sampling.** (1) implement; (2) get evidences; (3) report the Bayes
factor with uncertainty. SEARCH: "nested sampling evidence".
**M058 Approximate Bayesian computation.** (1) summaries = slope, break radius;
(2) run ABC; (3) posterior for the framework's parameters. SEARCH: "approximate
Bayesian computation likelihood free".
**M059 Compressed sensing.** (1) sparsity in a wavelet basis; (2) reconstruct the
cluster profile from limited bins; (3) sharpen the slope. SEARCH: "compressed
sensing sparse reconstruction".
**M060 Automatic differentiation.** (1) EOM solver in JAX; (2) differentiate
through it; (3) fit a_0 and n jointly. SEARCH: "automatic differentiation
differential equation".

## VII. INFORMATION / STATISTICS (M061-M070)
**M061 Minimum description length.** (1) MDL for framework vs LCDM on the same
data; (2) fewer bits wins; (3) honest complexity penalty. SEARCH: "minimum
description length model selection".
**M062 Fisher information / Cramer-Rao.** (1) Fisher matrix for a_0 from rotation
curves; (2) the bound gives the floor; (3) is 5 percent achievable? (N3)
SEARCH: "Fisher information Cramer Rao bound".
**M063 Cross-validation.** (1) k-fold CV framework vs NFW on SPARC; (2)
out-of-sample predictive score; (3) guards against overfitting. SEARCH:
"cross validation predictive assessment".
**M064 Causal inference.** (1) causal graph; (2) is M_b to g_obs causal or
confounded? (3) strengthens or weakens the RAR's interpretation. SEARCH:
"causal inference do calculus".
**M065 False discovery rate.** (1) Benjamini-Hochberg on the 22 cluster checks;
(2) control FDR; (3) which PASSes survive correction? SEARCH: "false discovery
rate Benjamini Hochberg".
**M066 Hierarchical Bayes.** (1) cluster-level plus population-level parameters;
(2) partial pooling of the 12 clusters; (3) robust population slope. SEARCH:
"hierarchical Bayesian partial pooling".
**M067 Time-series / GP.** (1) test whether a_0 varies with z using cosmic
chronometers; (2) GP modeling; (3) a detection would be transformative. SEARCH:
"Gaussian process cosmological time series".
**M068 Matched filtering.** (1) build a matched filter for the -2 slope;
(2) apply to weak lensing; (3) S/N for -2 vs -3 (C5). SEARCH: "matched filter
weak lensing".
**M069 Nonparametric tests.** (1) rank-based tests on the slope; (2)
distribution-free; (3) robust -2 vs -3 verdict. SEARCH: "nonparametric test
slope distribution free".
**M070 UMAP / PCA on residuals.** (1) embed the RAR residuals; (2) look for
low-dimensional structure; (3) structure = missing systematic or new physics.
SEARCH: "manifold learning residuals structure".

## VIII. CONVEX / VARIATIONAL (M071-M080)
**M071 Convex duality.** (1) is f(K) convex? (2) if not, find the convex envelope;
(3) non-convexity may BE the ghost, a clean diagnosis. SEARCH: "convex envelope
Legendre transform".
**M072 Semidefinite programming.** (1) energy bound as an SDP; (2) solve
numerically; (3) positivity certificate or counterexample. SEARCH: "semidefinite
programming positivity certificate".
**M073 Sum-of-squares / Positivstellensatz.** LEAN-FRIENDLIEST ghost proof.
(1) express positivity as an SOS; (2) get an ALGEBRAIC certificate; (3) it
compiles in Lean. SEARCH: "sum of squares Positivstellensatz certificate".
**M074 Constrained variation.** Resolves the H034 vs H008 inconsistency (Door D4).
(1) impose the frozen constraint with a Lagrange multiplier; (2) vary;
(3) does the SOURCED or SOURCELESS equation result? SEARCH: "constrained
variational Lagrange multiplier".
**M075 Quasiconvexity (Morrey).** (1) test quasiconvexity of the energy;
(2) failure means no minimizer = energy unbounded below = the ghost. SEARCH:
"quasiconvexity Morrey existence minimizer".
**M076 Monotone operators.** (1) show the operator is monotone; (2) apply
Browder-Minty for existence; (3) solutions despite degeneracy. SEARCH: "monotone
operator Browder Minty".
**M077 Minimax / saddle.** (1) show the energy has a saddle; (2) is it a
constrained extremum? (3) tachyon vs ghost distinction. SEARCH: "minimax saddle
point energy".
**M078 Pontryagin optimal control.** (1) relaxation as a control problem;
(2) maximum principle; (3) the optimal path IS relaxation to the phantom.
SEARCH: "Pontryagin maximum principle".
**M079 Shape optimization.** DERIVE the -2 profile. (1) minimize energy over
profiles; (2) is -2 the optimum? SEARCH: "shape optimization calculus variations".
**M080 Varifolds / GMT.** (1) the interface as a varifold; (2) prove regularity;
(3) handles singularities in the cluster transition. SEARCH: "varifold geometric
measure theory".

## IX. SPECTRAL / HARMONIC (M081-M090)
**M081 Second-variation spectrum.** LOCATE the ghost. (1) build the second
variation; (2) compute its spectrum; (3) a negative mode = the ghost, precisely
located. SEARCH: "second variation negative mode instability".
**M082 Scattering theory.** GW off a phantom halo (D095). (1) scattering problem;
(2) phase shift; (3) measurable dispersion. SEARCH: "scattering theory phase
shift".
**M083 Microlocal / wavefront sets.** (1) wavefront set of solutions; (2) locate
singularities (the transition surface); (3) where the two-zone approximation
breaks. SEARCH: "microlocal analysis wavefront set".
**M084 Spherical harmonics.** CMB (H4). (1) expand; (2) framework's CMB power
spectrum; (3) test against Planck. SEARCH: "spherical harmonic CMB power
spectrum".
**M085 Wavelets.** (1) wavelet-transform the cluster profile; (2) localize the
break; (3) scale-dependent slope. SEARCH: "wavelet transform localization".
**M086 Green functions.** H004's screened propagator. (1) Green function for the
biharmonic operator; (2) verify (1-e^{-r/xi})/r; (3) apply to the ghost. SEARCH:
"Green function biharmonic screened".
**M087 Pseudospectra.** (1) pseudospectrum of the fluctuation operator; (2)
transient growth could MIMIC instability without a true ghost. SEARCH:
"pseudospectra non-normal transient growth".
**M088 Fredholm index.** (1) show the operator is Fredholm; (2) compute the
index; (3) protected modes. SEARCH: "Fredholm operator index zero mode".
**M089 Harmonic analysis on symmetric spaces.** (1) TT modes as harmonics; (2)
the count D(D-3)/2 falls out; (3) generalizes H017. SEARCH: "harmonic analysis
symmetric space".
**M090 Time-frequency (Wigner-Ville).** (1) apply to a_0(z); (2) detect any time
variation. SEARCH: "time frequency analysis Wigner Ville".

## X. DISCRETE / ALGEBRAIC (M091-M100)
**M091 Spectral clustering.** Cosmic web (D077). (1) build a graph; (2) spectral
clustering; (3) do filaments host the phantom? SEARCH: "spectral clustering
graph Laplacian".
**M092 Matroid theory.** (1) constraints as a matroid; (2) minimal independent
set; (3) removes redundant assumptions. SEARCH: "matroid independence".
**M093 Combinatorial optimization.** Settles the H039/D036 disagreement. (1)
break location as a combinatorial problem; (2) solve EXACTLY, not gradient
descent; (3) avoids local minima. SEARCH: "combinatorial optimization change
point".
**M094 Change-point detection.** (1) apply to the cluster slope; (2) break radius
WITH uncertainty; (3) settles the break question (C1/C4). SEARCH: "change point
detection segmented regression".
**M095 Fano / minimax bounds.** (1) bound for distinguishing -2 from -3;
(2) is the measurement even possible with current data? SEARCH: "Fano inequality
minimax lower bound".
**M096 Tropical geometry.** (1) tropicalize the constraint variety; (2) the
tropical limit is the deep-MOND regime; (3) combinatorial structure of the
transition. SEARCH: "tropical geometry degeneration".
**M097 Homotopy continuation.** ALL solution branches. (1) set up the algebraic
system; (2) solve with homotopy continuation; (3) no missing branch. SEARCH:
"homotopy continuation numerical algebraic geometry".
**M098 Grobner bases.** (1) eliminate variables; (2) exact relation among
observables; (3) Lean-checkable. SEARCH: "Grobner basis elimination ideal".
**M099 o-minimality.** (1) are the definable sets o-minimal? (2) o-minimality
forbids pathology and guarantees finiteness. SEARCH: "o-minimal tame geometry".
**M100 Proof mining (Kohlenbach).** (1) take the relaxation existence proof;
(2) extract an explicit convergence RATE; (3) the rate is a testable timescale
(M039/M010). SEARCH: "proof mining Kohlenbach rate".
