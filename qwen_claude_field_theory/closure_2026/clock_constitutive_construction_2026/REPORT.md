# Constructive clock and spatial-projector calculation

Base: d6f5f6ef7d63d6f54827f6cfc84a3614db2743a4.
During this calculation Fable committed 9444ec449, L66, identifying that
the integrable-clock construction escapes the specific L60 scalar coupling
obstruction. That action differs from the construction developed here.
The preceding goal turn produced executable evidence; it was progress.

**Status: explicit trial action, partial derivations; the complete gravity
goal remains OPEN.** This work constructs two operators to repair measured
response mismatches. Neither operator's existence proves full closure.

## Same action and its domain

Use c=1, signature (-+++), G_b>0, a normalized timelike clock normal n,
a_mu=n^nu nabla_nu n_mu, a=sqrt(a_mu a^mu), theta=nabla_mu n^mu,
and the induced spatial metric h. All accelerations in this paragraph have
inverse-length units; physical a0 is divided by c².

\[
S={1\over16\pi G_b}\int\sqrt{-g}\left[
 R-2\Lambda-\ell\theta^2+a_0^2 f(a/a_0)
 +\eta_V V_i {\cal H}_1^\dagger V^i+\eta_U U^2
\right]d^4x+S_m[g,\psi].
\]

\[
f(y)=2y^2-C{\cal G}(y),\qquad
{\cal G}(y)=y^2+2(1+y)e^{-y}-2.
\]

Here dagger denotes the inverse on the orthogonal complement of the kernel,
not an extra dynamical field. Take smooth compact closed connected leaves.
The scalar Laplacian Delta_h is negative semidefinite and its inverse removes
the constant mode. Define

\[
P_T w=w-D\Delta_h^\dagger(D\cdot w),\quad
V_i=(P_T)_i{}^jD^mK_{jm},\quad
U=K-\langle K\rangle-\Delta_h^\dagger D_iD_jK^{ij}.
\]

The average uses sqrt(h) d³x. H_1 is the positive spatial Hodge Laplacian on
one-forms; its pseudoinverse removes harmonic one-forms. Thus V H_1^\dagger V
means contraction with the inverse-applied one-form at the same spacetime
point. For all nonzero modes on a flat torus H_1=k² and P_T=I-kk^T/k².
These specifications define an intrinsic nonlocal functional on each leaf.
They do not impose a retarded inverse in physical time. Global domain
dependence and the physical response must be tested.

For FLRW both V and U vanish, including the homogeneous K mode. For a static
clock-rest configuration Kij=0, so both added operators and their first
variations vanish. They therefore preserve that branch's static force law.
There are no scalar or vector carriers in addition to the clock and metric.
The parametric vector construction printed by the script is an alternative
algebraic representation of f, rather than extra fields assumed in this action.

## Static construction: both metric potentials are varied

The leading, fixed-a0 weak static density, after the Einstein-Hilbert boundary
term is removed and with overall 16 pi G_b suppressed, is

\[
L_{\rm stat}=2|\nabla\Psi|^2-4\nabla\Phi\cdot\nabla\Psi
 +a_0^2 f(|\nabla\Phi|/a_0)-16\pi G_b\rho\Phi .
\]

SymPy varies the independent gradient jets. Psi gives
Delta(Psi-Phi)=0. Matching boundary conditions must remove the harmonic
difference; a boundary prescription is necessary even in GR. Only then does
the Phi equation reduce to

\[
\nabla\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]
=4\pi G_N\rho,\qquad G_N={2G_b\over C}.
\]

This leading static variation is not a full covariant metric variation.
The vector terms do not enter it because Kij=0. The equation is isotropic
in the full three-dimensional gradient and is not restricted to spherical
sources. Its spherical exterior integrates to mu(g/a0)g=G_N M/r² and its
deep limit gives v^4=G_N M a0.

Unlike an arbitrary constant offset in J', this construction matches the
measured Newton constant simultaneously. The alternative algebraic vector
has magnitude

\[
u(y)={y[A-C\mu(y)]\over b},\quad
J(u(y)^2)={ (A-C)y^2+2C[(y^2+y+1)e^{-y}-1]\over b}.
\]

Direct differentiation gives J_Y u=y. For A=2 and
0<C<2/(1+e^-2), du/dy stays positive. This extends the existing repository
calibration into the kinetic-response calculation; the monotonicity mechanism
and Newton-constant renormalization are already in the repository.

## Clock principal sector and actual preservation

Let alpha denote the contraction of half the Hessian of a0²f with a unit
wavevector. With its angle theta to the background acceleration,

\[
\alpha_\perp=2-C(1-e^{-y}),\quad
\alpha_\parallel=2-C[1+(y-1)e^{-y}],\quad
\alpha=\alpha_\perp\sin^2\theta+\alpha_\parallel\cos^2\theta.
\]

The maximum of 1+(y-1)e^-y is 1+e^-2, obtained by differentiating
and locating y=2. Thus 0<C<2/(1+e^-2) ensures 0<alpha<2 at every y>0.

In unitary clock gauge, after fixing spatial scalar gauge, the Fourier
Lagrangian is directly assembled from extrinsic curvature and spatial Ricci
terms:

\[
L_s=-6t\dot\zeta^2+4k^2\dot\zeta B-\ell(3\dot\zeta-k^2B)^2
 +k^2(2\zeta^2-4n\zeta+\alpha n^2),\quad t=1-\frac23\eta_U .
\]

The script computes the velocity Hessian, primary constraints, canonical
Hamiltonian, Poisson matrix, and preservation through closure. For the final
witness it finds p_n=p_B=0, two secondaries, an actual rank-four bracket
matrix and one scalar configuration DOF. The raw constraint rows and full
matrix are in the run output. This is the gauge-fixed frozen quadratic
sector only. No full nonlinear constraint count is inferred.

Eliminating n and B independently, and also calculating the determinant of
the unreduced frequency matrix, gives the same clock dispersion. After the
source matching below,

\[
{\partial^2L_{\rm red}\over\partial\dot\zeta^2}
={2C(4-C+3\ell)\over\ell}>0,\qquad
c_{\rm clock}^2={2\ell(2-\alpha)\over C\alpha(4-C+3\ell)} .
\]

For C=5/3, ell=1/100 this is positive and subluminal for every y>0 and angle.
The global upper bound follows from the exact minimum of alpha at y=2,
parallel propagation. A 3,525-point deterministic scan checks the same
coefficient formula for 1e-8<=y<=80 and 25 directions. It is a local
principal-symbol result: lower derivative background terms and global
instabilities have not been bounded.

The two transverse shift variables have no velocities. Their two primaries
generate two secondaries with computed rank-four bracket matrix and zero
vector configuration DOF. The two TT polarizations have the Einstein kinetic
and gradient coefficients, hence c_T²=1 in this principal sector. This
accounts for two tensors and one explicitly counted clock in the tested
quadratic system.

## Constructive transverse repair

For a wavevector along z, directly evaluating Kij gives
V_i V_i/k²=k²(S_x²+S_y²)/4. Scalar and TT Kij give V=0.
The transverse density, including a conserved matter current j_i, gives

\[
L_V={2+\eta_V\over4}k^2S_i^2+16\pi G_b j_iS_i,\quad
S_i=-{32\pi G_b\over (2+\eta_V)k^2}j_i.
\]

In the constant high-acceleration limit, with the usual PPN vector potential
V_i^PPN=4pi G_N j_i/k², the standard transverse PPN definition at gamma=1 is
g_0i^T=-(4+alpha1/2)V_i^PPN. Matching the calculated response yields

\[
\alpha_1={8(C-\eta_V-2)\over \eta_V+2},\qquad \eta_V=C-2.
\]

This is a derived weak-source transverse matching condition, not a full
boosted PPN certification on a galactic background. It sets the computed
alpha1 channel to zero with positive shift quadratic coefficient C/4.
The GR normalization control C=2, eta_V=0 gives g_0i=-4V_i as required.

## Constructive scalar response repair

For a Fourier source proportional to exp(rt+ikz), impose linear matter
conservation through Tzz=-r² rho/k² and div j=-r rho. The source density
added to L_s is, with src=16pi G_b rho,

\[
L_{\rm source}=-{\rm src}\,n+r\,{\rm src}\,B
              +r^2{\rm src}\,\zeta/k^2 .
\]

The script varies this complete quadratic action and solves n, B, zeta.
It computes curvature, retaining the shift:
R_0z0z=-k²(n+rB)+r²zeta and R_0x0x=r²zeta.
It separately re-solves GR with measured G_N as a reference.

The coefficient of r² in the high-acceleration R_0z0z mismatch is

\[
-{{\rm src}[C^2-3C\ell-4C-6\ell t+12\ell+4]\over
  2C^2\ell k^2}.
\]

Solving it, rather than assigning a PPN value, gives

\[
t={ (C-2)^2+3\ell(4-C)\over6\ell},\qquad
\eta_U={-C^2+3C\ell+4C-6\ell-4\over4\ell}.
\]

Both selected curvature components then agree with their GR reference through
order r². The code retains the nonzero order-r^4 remainder and its additional
clock pole. This is not alpha2=0 or beta=1: a general boosted source, all
spatial stresses, nonlinear metric terms, and global matching are still needed.

At C=5/3, ell=1/100 the two operator coefficients are
eta_V=-1/3 and eta_U=-109/36. Negative coefficients in constrained variables
cannot be classified from their signs alone; the computed reduced kinetic
Hessian and the full frequency determinant supply the local health check.

## FLRW, Ward identity and limits

The nonlocal terms vanish on exact homogeneous leaves by their definitions.
The homogeneous action, varied before setting N=1, gives

\[
3(2+3\ell)H^2=16\pi G_b\rho+2\Lambda,\qquad
{G_{\rm cos}\over G_N}={C\over 2+3\ell}.
\]

This admits H!=0 for positive rho or Lambda. For the witness the ratio
is about 0.821. No expansion-history or perturbation-data fit was done here.
On minimally coupled ordinary matter's own equations, diffeomorphism
invariance of S_m gives nabla_mu T_m^{mu nu}=0. That matter identity does
not certify the consistency of every gravitational constraint with it.

At k=0 the inverse operators are defined by kernel removal, not division by
k². The nonzero-k Dirac count is not extrapolated to that sector. Exact
minisuperspace variation supplies a separate background check, but the full
homogeneous constraint analysis remains open.

At y->0, alpha->2 and the clock gradient stiffness vanishes. The kinetic
coefficient stays finite in the reduced calculation, but nonlinear strong
coupling, weak solutions and regular-center behavior remain unresolved.
High-frequency characteristic speed below c is insufficient to certify the
causal response of the spatial inverse operators.

The exact static AQUAL branch retains its existing external-field tests:
this study does not erase the adverse stationary Cassini quadrupole result.
A physically posed moving Solar-System source and clock response must be
computed before deciding whether the same-action dynamical branch changes it.
No successful cluster, binary, CMB or supernova fit is asserted.

## Attribution, literature and Lean

Carl Zimmerman's supplied exponential interpolation, acceleration-density
hypothesis, and suggestion to pursue a primordial clock/memory mechanism
motivate this calculation. The coefficient 1/2 in a0=(c/2)sqrt(G rho_DE)
remains input; no derivation of it occurs here. The spatial-projector repair
is a calculation developed here and has no global novelty certificate.

The base f(a) preferred-foliation mechanism is known:
Blanchet & Marsat, Phys. Rev. D 84, 044056 (2011), action (2.4), DOI
10.1103/PhysRevD.84.044056,
https://www2.iap.fr/users/blanchet/images/PhysRevD.84.044056.pdf .
The notation correspondence is f_BM=Lambda-a0² f_here/2 before ell and
projector terms. Their static limit supports the starting mechanism.

Flanagan, arXiv:2302.14846v2, equations (1)-(9) and the slow-motion discussion,
https://arxiv.org/html/2302.14846v2 , explicitly retains a dynamical khronon;
time-dependent responses need not equal stationary MOND. Its stability
results concern its own action and are not imported as a certificate here.
Primary sources checked 2026-09-09 through the web reader; no local copies
were saved. The search covered the named f(a)/khronometric papers only,
not a comprehensive novelty search for projector operators.

Lean and lake were not found in PATH or the usual .elan/Homebrew locations.
No Lean proof is claimed. SymPy identities and the exact rational Dirac
calculation provide reproducible algebra, not a formal theorem-prover proof.

## Reproduction and next calculation

Run construct.py and test_construct.py via unittest discovery in this folder.
The Mathbox run_001 manifest records source hashes, actual command, environment,
raw stdout/stderr, bounded runtime and actual exit status.

Final recorded checks: construction runner rc=0, six independent controls
rc=0, manifest validation with --root rc=0, whitespace check rc=0. The analytic
upper bound on the repaired witness's clock speed squared is
18(1+exp(2))/[709(exp(2)-5)] = 0.08914829072836318. The lower bound is zero,
approached as y tends to zero; it is strictly positive only at y>0.
The tests include rotated wavevectors, an independent finite-difference
acceleration Hessian, and regular-versus-auxiliary Hamiltonian controls.

The next calculation is the full intrinsic metric/clock variation of the
two spatial operators, including delta(A^-1)=-A^-1(delta A)A^-1 on a fixed
kernel complement and the variations of that complement/leaf average.
Then compute the conserved moving-source curvature response for general
stresses and its finite propagation support. These are obligations of this
explicit action, before any full-theory or novelty announcement.

## V3 follow-up: coefficient-family selection

The follow-up files `parameter_family_gate.py` and `PARAMETER_FAMILY_GATE.md`
turn the V2/V3 coefficient choice into an exact algebraic gate. With free
scalar coefficients `d,t`, order-r^2 matching gives

\[
t={C^2-4Cd-3C\ell+4d^2+12d\ell\over6\ell}.
\]

The independent isotropic-stress k->0 residue factors as

\[
-{F r^2(-C+2d)(-C+2d+3\ell)\over
  2C\ell(-C+4d+3\ell)},
\]

so the scalar-only gate has two branches, `d=t=C/2` and
`d=t=(C-3 ell)/2`. The tensor and transverse-vector equations independently
force their measured-G normalizations to `C/2`. The complete six-symmetric-
seed response is then evaluated for both scalar branches, not assumed from
the witness: at `C=5/3`, `ell=1/100`, the first branch has zero spatial-pole
and wave-factor failures, while the second has 15 of each. The full linear
response therefore selects `d=t=C/2`; the TT repair is not an arbitrary extra
coefficient once the all-polarization gate is imposed.

This is a new structural checkpoint, not closure. It is exact in the stated
constant-coefficient Fourier family, with a finite witness for the factor
divisibility. It does not vary the nonlinear York-TT projector, perform full
Dirac closure on curved leaves, derive boosted PPN, or fit data. The durable
result and provenance are `run_002/parameter_family_results.json` and its
manifest; the corrected package invocation runs all nine tests with rc=0.
