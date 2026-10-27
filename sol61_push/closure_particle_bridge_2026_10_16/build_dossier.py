"""Assemble existing equation/proof reports into one standalone LaTeX source.

Scientific statements are retained under explicit checkpoint headings. The
current front matter supersedes only earlier 'next execution' prose.
"""
import hashlib
import json
import re
from pathlib import Path

p=Path(__file__).parent
inputs=[
 ('COLD_DARK_ENERGY_AND_PARTICLE_BRIDGE.tex','Equation inventory and the first production construction'),
 ('THERMAL_PHASE_AND_CHARGE_KINETICS.tex','Thermal phase and charge-resolved collision audit'),
 ('PAIR_CONVERSION_AND_ABUNDANCE.tex','Pair-conversion evolution and pressure-aware exchange'),
 ('SOURCE_ASSISTED_MATCHING_AND_RATES.tex','Source-assisted channels and pole matching'),
 ('ASSISTED_EVOLUTION_AND_GALAXY_BRIDGE.tex','Enlarged evolution and the missing galaxy bridge'),
 ('PASSIVE_RESPONSE_AND_CLOSURE.tex','Finite-time collective response and soft particle matching'),
 ('RECIPROCAL_CARRIER_MEDIUM_BRIDGE.tex','A reciprocal carrier--medium density candidate'),
 ('CHARGE_EVEN_PARTICLE_MATCHING.tex','Charge-even particle matching and the density vertex'),
 ('RADIATIVE_THRESHOLDS_AND_VACUUM.tex','Radiative thresholds and vacuum matching'),
 ('PLANCK_SCALED_FLUX_LINK.tex','A Planck-scaled flux vacuum--force candidate'),
 ('COVARIANT_HOST_STRESS_AND_DENSITY.tex','Covariant host stress, density scaling and finite-stock tails'),
 ('FINITE_CHARGED_PHASE_AND_EXTERIOR.tex','A finite charged scalar phase and its reciprocal exterior'),
 ('MEDIATOR_COMPLETION_AND_VALIDITY.tex','An explicit mediator origin and validity of the scalar phase'),
 ('QUANTUM_FORMATION_GRAVITY_NORMALIZATION.tex','Quantum control, formation, response cones and vacuum normalization')]
preamble=r'''\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array}
\usepackage[hidelinks]{hyperref}
\newcommand{\dd}{\mathrm d}
\newcommand{\DE}{\mathrm{DE}}
\newcommand{\Pl}{\mathrm{Pl}}
\newcommand{\Mb}{M_b}
\newcommand{\lp}{\lambda_{HX}}
\newcommand{\lt}{\lambda_{\rm tot}}
\newcommand{\eq}{\mathrm{eq}}
\title{Cold energy, dark energy, and a particle bridge\\
Equations, physical roles, executed routes, and remaining closure}
\author{Zimmerman programme: consolidated CPB-QFG-2026-10-16 dossier}
\date{16 October 2026}
\begin{document}
\maketitle
\section*{Current result and reading guide}
The physical theory remains incomplete. This is one standalone equation
dossier containing the current inventory and the successive calculations
needed to understand its limits. It is not a single unified action assembled
by identifying unrelated fields, nor a claim that every historical candidate
in the repository is physically compatible.

Three physical roles remain distinct: vacuum stress, massive cold excitations,
and collective gravitational response. The proposed link
$a_0=\kappa c\sqrt{G\rho_{\rm DE}}$, with fitted $\kappa$, remains a target.
The particle construction supplies actual interactions, while its
identification with the galaxy-response medium remains unresolved.

Part I gives the equations and initial scalar production construction.
Part II executes its thermal and charge audit, including a nonzero
number-changing amplitude. Part III executes a reduced kinetic checkpoint:
the pole-free reaction $\Phi\Phi^*\leftrightarrow XX^*$ and fast source
conversion can change the final daughter count substantially. An isolated,
energy-conserving reduced gas calculation is executed from specified initial
states. It does not yet derive those states from the Higgs era or include
the complete real-intermediate-state-consistent collision hierarchy.

The original 1-MeV thermal comparison and the separately specified 2-MeV
evolution are different candidates. The latter's moderate initial state
nearly doubles its weighted count in the reduced model; the hottest state
fails the original dilution gate. No observational abundance or coldness
verdict is inferred. That calculation also extends the dust exchange
identity to a warm gas, preventing internal rest/kinetic conversion from
being misidentified as vacuum exchange.

Part IV records the collision audit. The same action has a missing
pole-free source-assisted channel, $X+\Phi+\Phi^*\leftrightarrow\Phi+\Phi$.
Its two conjugate channels add approximately 4.95 times the pair-conversion
coefficient at $T_d=m$ in the chosen common-MB approximation. The old
abundance curves therefore remain reduced-network results. Exact source-pole
factorization identifies further required reactions. A positive interior
pole-matching construction has an explicit smooth-profile error bound;
physical endpoint and overlapping-pole matching remain unfinished.

Part V executes that pole-free source-assisted evolution. Its final weighted
yield ratios are approximately 1.02719, 1.95810 and 4.49358 for the three
specified initial temperatures. The hottest state still fails the original
dilution gate. These remain reduced-network results, with further resonant
channels and the actual production history unfinished. The same part derives
the direct Higgs-induced baryonic contact response: at the chosen galactic
density its fractional shift is about $7\times10^{-48}$. An ideal-gas halo
occupation check also prevents simply assuming a MeV condensate. These are
candidate-specific constraints, not exclusions of collective media.

Part VI derives a finite-time bound for stable canonical quadratic response.
Large static susceptibility from a soft mode does not imply large response
at a fixed time. It applies this test to the existing scalar/polarization
construction with explicit limits on the approximation. A separate one-loop
calculation shows that a tree-zero daughter Higgs coupling acquires a finite
soft contribution. Its chosen galactic effect remains tiny. This soft vertex
is not a hard Higgs decay calculation or a full renormalization result.

Part VII constructs a separately specified NR density bridge to the nodal
medium. Its canonical occupation energy and a chosen repulsive contact
give a sufficient joint convexity condition. Both cold and fermion densities
are varied at fixed inventories in a prescribed external baryon potential.
A neutral cubic-response interval survives, with compensating signed fermion
charge elsewhere. The strong branch has a proved boundary-sensitive
large-radius limit and can lose the desired baryonic mass scaling. This is
an explicit effective candidate, not a matching from the MeV scalar action,
an evolved halo, or a relativistic closure.

Part VIII constructs a charge-even scalar bridge directly to $|\Phi|^2$.
A completed-square potential retains the carrier mass lower bound in the
specified positive-energy density-functional extension. The actual neutral
stock is distinguished from signed charge. Chosen vacuum tree scattering
and a new mediator decay are calculated. A direct band calculation supplies
the density-vertex kernel, its uniform Ward zero, finite-momentum absorption
and a conservative static RPA test. The original mass-vertex response cannot
be substituted for this density vertex. Neither full quantum stability,
neutral-mixture EOS, a populated-mediator thermal history nor galaxy closure
is established.

Part IX computes selected scalar loop effects. A small carrier mass shift
can close the narrow source decay in a diagnostic with fixed MS mass inputs;
finite on-shell matching remains possible and a weaker comparison keeps the
decay open. Tadpole, mass and vacuum matching are separate conditions.
Partial scalar vacuum terms do not predict the cosmological constant.
A known sequestering gravity route is checked conditionally; directly
coupling an acceleration coefficient to its auxiliary vacuum parameter
changes the constraint, so the previous cancellation argument cannot be
inherited without the new variation. Neither residual vacuum magnitude nor
the acceleration normalization is derived.

Part X varies an explicit auxiliary-action extension with a separate
conjugate flux $Q$. A Planck-scaled flux energy with selected power two
survives the projected metric equation, unlike an unscaled constant flux.
A chosen inverse-flux cubic response produces $a_0\propto Q$ while that
flux energy is proportional to $Q^2$. Residual flux/history terms, a
covariant microscopic matter/frame action, the functional choice and the
normalization remain required inputs or obligations. The scalar inverse-square
force is counted in the Newtonian dictionary. The annular response has
logarithmically divergent infinite-tail energy, so it is not a complete halo.
This is a conditional classical action candidate, not physical closure.

Part XI supplies a covariant barotropic material frame and its stress.
A material-scaled negative band sea has radiation-like pressure and fails
by itself; a specified positive host repairs the elementary longitudinal
signs while introducing new EOS inputs. A fixed-velocity material spectrum
makes the cubic acceleration vary with density. Compensating this coefficient
requires a density-dependent critical subtraction and its host rearrangement.
On a prescribed finite-count profile, neither persistent cubic response nor
the compensated regulated tail has finite infinite-radius band energy.
The material alternative returns to an inverse-square toy tail after leaving
the controlled small-gap regime. These tests identify what an actual phase
interface must solve; no full fermion/frame or finite halo is obtained.

Part XII tests a different particle-level host: a sextic charged scalar
phase with a computed planar wall and a chosen reciprocal local response.
Fixed-charge spherical solutions have a cubic-dominated interior annulus
and a finite-energy inverse-square exterior. Two numerical resolutions and
a fixed-charge scaling identity check stationarity; finite radial amplitude
Hessians have positive sampled curvature. This is not the repulsive MeV
carrier or a microscopic nodal-band matching. Its exterior changes the
Newtonian force coefficient substantially, while its charge inventory,
formation, dynamic/metric health and cosmology remain unclosed.

Part XIII supplies a renormalizable two-scalar particle model for the
attractive host phase. Its selected family has an algebraically proved
unique global classical vacuum and a unique charged coexistence density.
Exact matching shows a controlled heavy-mediator limit, including the
amplitude kinetic correction. Improving that tree limit increases a
quartic-cancellation requirement. Quantum thresholds, a derivation of the
response coupling and a new two-field finite-body/formation calculation
remain required. This is a classical particle-potential bridge, not a
completed theory of cold energy, dark energy or gravity.

Part XIV explicitly tests quantum corrections, formation, gravity response
and vacuum normalization. One-loop running exposes the unprotected original
quartic/mass matching. A weak-coupling classical-limit scaling controls the
selected loop sensitivities while increasing the required charge and energy.
Actual charged homogeneous scalar backgrounds exhibit a finite clumping
instability band; nonlinear formation and the initial charged state are
not yet derived. The minimal Lorentz scalar cubic-response completion has
radial characteristics approaching $\sqrt2$ times the metric light speed;
additional physical dynamics are needed for a common-cone completion.
Independent response parameters and flux/history data prevent a unique
prediction of the dark-energy magnitude or acceleration normalization.

The reports retain their exact model boundaries, sources and evidence.
Their local ``next'' sections describe their own checkpoints; the current
next steps are to match the remaining
source-assisted and six-point contributions at actual thermal boundaries,
then compute the stabilized production/thermal history. Galaxy
formation, finite supply, source selection, relativistic lensing, native
cosmology, parameter origins and joint empirical validation remain open.
No global novelty or independent-referee claim is made.

\tableofcontents
\clearpage
'''
parts=[preamble]
records=[]
for filename,title in inputs:
    source=(p/filename).read_text()
    assert source.count(r'\begin{document}')==1 and source.count(r'\end{document}')==1
    body=source.split(r'\begin{document}',1)[1].rsplit(r'\end{document}',1)[0]
    body=body.replace(r'\maketitle','',1).strip()
    parts.extend([r'\part{'+title+'}\n',body,'\n\\clearpage\n'])
    records.append({'path':filename,'sha256':hashlib.sha256((p/filename).read_bytes()).hexdigest()})
parts.append(r'\end{document}'+'\n')
document='\n'.join(parts)
labels=[tail.split('}',1)[0] for tail in document.split(chr(92)+'label{')[1:]]
bibkeys=[tail.split('}',1)[0] for tail in document.split(chr(92)+'bibitem{')[1:]]
assert len(labels)==len(set(labels)), 'duplicate mathematical labels'
assert len(bibkeys)==len(set(bibkeys)), 'duplicate bibliography keys'
destination=p/'COLD_AND_DARK_ENERGY_DOSSIER.tex'
destination.write_text(document)
(p/'dossier_sources.json').write_text(json.dumps({'checkpoint':'CPB-QFG-2026-10-16',
    'inputs':records,'output':destination.name,'output_sha256':hashlib.sha256(destination.read_bytes()).hexdigest(),
    'generation':'python3 sol61_push/closure_particle_bridge_2026_10_16/build_dossier.py',
    'scope':'Source assembly and checkpoint guide; proofs retained from the fourteen named reports.'},indent=2)+'\n')
print(destination)
