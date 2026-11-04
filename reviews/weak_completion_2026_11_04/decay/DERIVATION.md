# CC11 leading on-shell neutral decay matching

The physical leading on-shell mixed-gaugino amplitudes are now computed from
the ordinary fixed-vacuum vertices. The full six-topology sum cancels its UV
constant and its Rxi gauge dependence, passes mass-block basis rotations,
agrees with an independent supersymmetric messenger benchmark, and has the
required weak scaling. The Goldstino exit is forbidden by an exact unbroken
unitary charge-conjugation symmetry. The additional allowed octet decay into
two SU3 gauginos is included in the inclusive normalization.

All results here use the prescribed pole x=25.4000254000381, e=.003,
mu=2e6 GeV and g=sqrt(29/200)e. CC10 sources and outputs were kept frozen.

| Leading width / mu | S8_0 | S3_0 |
|---|---:|---:|
| Two unbroken gauge bosons, frozen complete CC10 calculation | 4.631658829e-29 | 3.001424320e-26 |
| One chi and one adjoint gaugino, on shell | 2.859914283e-29 | 2.646097304e-26 |
| Two SU3 gauginos | 4.445295711e-31 | forbidden |
| Adjoint gaugino plus Goldstino | forbidden | forbidden |
| Inclusive total | 7.536026069e-29 | 5.647521625e-26 |

The mixed canonical couplings have magnitudes
|y8|=5.212050665e-13 and |y3|=8.112478254e-12. The octet coupling is real and
the triplet coupling imaginary in the declared CP slice. These rates use
massless external gauginos consistently at leading one-loop order: their
loop-generated masses change the phase space only at higher order and by
less than 1e-14 fractionally in this packet.

## Ordinary vertices, complete inventory and external legs

The canonical component data determine the symmetric Yukawa tensor Y_ija,
potential cubic C_aij, vector mass insertion K_avw, scalar gauge-current
matrix D_vas and fermion current matrix G_vaI. The external parent is projected
onto its actual lightest adjoint eigenspace and aligned with a normalized
unbroken Cartan generator. Internal traces sum every representation copy and
component, without a singlet color-factor replacement.

There are six one-loop 1PI triangle classes:

    FFS, FSS, FFV, FVV, FSV, FVS.

FSS contains the potential cubic; FFS and FFV contain the parent Yukawa;
FVV contains K; and the two mixed classes contain the ordinary derivative
scalar–scalar–vector current. Scalar propagators include physical scalars and
Goldstones. Goldstones acquire xi mV^2 while physical zero-mass singlets do
not. Ghosts have no fermion endpoint and supply no triangle of this process.
This topology inventory agrees with
[Goodsell–Liebler–Staub v2, Appendix A.2.3, equations A.99–A.110](https://arxiv.org/pdf/1703.09237v2).
Our Rxi reduction and model insertion are separate calculations; no claim is
made that SARAH's entire supported-model scope covers this SU5 model.

For the mixed chi amplitude all external-leg contributions vanish. A fixed
chi leg at a tree S_adj–fermion–chi vertex is zero because the unbroken U1
generator annihilates S_adj. Mixing an unbroken gaugino with its chiral-adjoint
partner is forbidden by the charge-conjugation symmetry below. Scalar mixing
cannot create a tree scalar–gaugino–gaugino coupling; that block of every
renormalizable Yukawa tensor is zero. Scalar–unbroken-vector mixing is also
odd under that symmetry. Thus no omitted wavefunction or tree counterterm
supplies this loop-induced amplitude.

The self-energy convention used in checking these statements follows
[Martin v2, section III, equation 3.2](https://arxiv.org/pdf/hep-ph/0509115v2).
If G=ext^dagger R U is stored with an external daggered row, an undaggered
external mass insertion uses the conjugate-oriented vector vertices G* G*.
The scalar term uses Y Y. The old CC10 helper used G G in that same matrix.
Its real CP-even mass benchmarks could not reveal the distinction, whereas
its CP-odd derivative could. No historical helper was edited.

## Finite on-shell integration

Choose p1^2=p2^2=0, s=(p1+p2)^2. The right-hand bridge carries momentum k,
the upper propagator k+p1, and the lower one k-p2. Write

    u=k^2, v=2k.p1, w=2k.p2.

After the external Dirac equations are applied, the transverse numerators
are polynomials in these three invariants. For example, FFS reduces to
A u+B; FFV to 4A[u+(v-w-s)/2]+4B; FSS and FVV have constant mass-flip
numerators. The mixed numerators are A(u+2v) and B(-u+2w).
The bridge fermion in the mixed graphs flows opposite to k, so its numerator
is -slash(k)+m. This fixes the relative mixed-graph sign; reversing it fails
the gauge cancellation.

With Feynman parameters x,y,z=1-x-y for upper, lower and bridge propagators,

    Delta=x mt^2+y mb^2+z mr^2-xy s,
    k=l-x p1+y p2,
    u0=-xy s, v0=y s, w0=-x s.

The required moments include

    <u> = u0 J0+4J2,
    <u^2> = u0^2 J0+12u0 J2+24J4,
    <uv> = u0 v0 J0+6v0 J2,
    <uw> = u0 w0 J0+6w0 J2,
    <vw> = v0 w0 J0+2s J2.

The script supplies the corresponding moments for three, four and five
denominators. Each separate topology has a vanishing UV coefficient after
its complete mass-block trace; constant subtraction conventions therefore
drop out of the physical sum.

The full vector propagator is evaluated using

    D_m=q^2-mV^2, D_xi=q^2-xi mV^2,
    P_munu=-i[g_munu/D_m+(xi-1) q_mu q_nu/(D_m D_xi)],
    1/(D_m D_xi)=integral_0^1 dtheta
                 [q^2-mV^2(1+(xi-1)theta)]^-2.

Two longitudinal vector pieces require a five-denominator moment. No unitary
gauge power-divergence subtraction or displaced gauge-fixing projector is
introduced. The Goldstone projector, external states and ordinary vertices
are held at the original vacuum.

All active internal thresholds of the mixed channel are above the external
mass; the parameter denominators are positive. The code rejects a new
internal cut rather than clipping it. Degenerate physical mass blocks remain
complete; a relative coefficient filter removes roundoff-only traces at
1e-12 of the largest block coefficient. Reported precision is numerical and
restricted to the declared range, not an all-parameter theorem.

For L=-S y_ab lambda_a lambda_b/2+h.c., the massless width is

    Gamma=M/(16pi) sum_ordered_ab |y_ab|^2.

The two distinct mixed species therefore give M|y_bY|^2/(8pi). For the octet
pair tensor y_bc=k d_abc, fixed-parent sum_bc d_abc^2=5/3. In the tested
Cartan orientation d_811=1/sqrt(3), so its inclusive pair width is
5M|y_11|^2/(16pi). Several independent color entries reproduce their d-tensor
ratios to better than 4e-11.

## Independent normalization and gauge checks

The Abelian messenger benchmark has W containing lambda X Phi Phi_bar and
mu_X (X-X0)^2/2, with F=0 at X0. Its q_X–gaugino coupling in the soft limit is

    y_q=-sqrt(2) g^2 mu_X/(16pi^2 X0).

At finite s it is multiplied by arcsin(sqrt(tau))^2/tau, with
tau=s/(4 lambda^2 X0^2). The independently integrated triangle gives both
the zero-momentum result and the finite-s result to 2.3e-16 relatively. This
checks the scalar-cubic/Yukawa relative sign, Majorana counting and loop
normalization without a broken-vector loop.

For the actual mixed channel, xi=.5,1,2 agree to 2e-12 relatively. Changing
the UV constant leaves the sum unchanged at comparable accuracy; every
separate topology's UV coefficient also vanishes. Independent orthogonal
rotations within scalar, positive-Takagi-Weyl and vector mass blocks reproduce
the result. Refining Feynman quadrature from 24x24 with ten longitudinal
nodes to 36x36 with sixteen nodes changes the mixed amplitudes below 2e-12.
The smaller octet-pair amplitude passes its xi check below 1e-8.

`run_bridge001` compares the ordinary soft vertex with the corrected finite
background self-energy derivative. They agree to better than 3e-8, limited
by that derivative's finite differencing. The ordinary soft vertex retains
a tiny off-shell gauge dependence, while its on-shell continuation cancels
it. The on-shell/soft amplitude ratios at xi=1 are .9998840068 and
1.004123229. The old triplet result 3.8068e-12 is consequently not the
physical rate: its conjugate-vector orientation omitted a contribution that
adds in the CP-odd channel. The checked ordinary soft magnitude is instead
8.0791660e-12, followed by the controlled finite-momentum correction.

At fixed sqrt(e)x and g/e, each on-shell amplitude scales as e^3 and each
width as e^(13/2). Direct e=.001 and .01 evaluations pass this scaling check
with the full finite-momentum integrals.

## Goldstino selection rule and remaining two-body exits

Let eta_a be the transpose parity of fundamental generator t_a. The model has
an unbroken unitary symmetry

    X -> X,
    A -> A^T, B -> B^T,
    psi_A -> psi_A^T, psi_B -> psi_B^T,
    V -> -V^T, lambda -> -lambda^T.

This is a gauge-group outer automorphism with the displayed matter action,
not complex conjugation of the chiral fields. The canonical kinetic terms and
W=fX+hX Tr(A^2)/2+lambda Tr(A^2 B) are invariant. The diagonal complex
background is invariant. The tree Goldstino, aligned with F*, is even.

For a parent component, S_a has parity eta_a and lambda_a has -eta_a.
The only residual-group invariant for S_adj lambda_adj G is delta_ab, and
that product is odd. The same symmetry forbids unbroken lambda–chiral-adjoint
mass mixing. Hence this Goldstino exit vanishes, including its external-leg
contributions, at every order preserving the symmetry. Gravitino longitudinal
interpretation requires the usual gravity equivalence regime and a gravity
sector preserving this same symmetry; the existing invariant leading packet
introduces no such breaking.

The component audit checks this symmetry directly on z,Y,M_F,H and R, with
maximum absolute residual below 3e-14. Full SF/VF off-diagonal self-energies
and the explicit Goldstino triangle-plus-leg amplitudes leave only roundoff
remainders. They are not treated as physical nonzero widths. A loop-corrected
Goldstino mass at a constrained nonstationary background is not inferred
from that diagnostic self-energy.

For S3, the symmetric product of two SU2 adjoints has no triplet, so a pair
of SU2 gauginos is forbidden. For S8, the allowed SU3 d-tensor pair is the
additional width in the table. Other light-gaugino combinations lack the
required residual representation. Other massive scalar/fermion two-body
thresholds remain closed in this lightest-adjoint packet. A scalar-to-scalar
plus one on-shell massless gauge boson has no gauge-invariant nonzero
two-body amplitude. No additional open leading two-body sink is silently
used to normalize the branches.

The same symmetry makes a chi–lambda_adj–F_adj transition dipole odd. Although
the leading masses are m_lambda8=43.4574 keV and m_lambda2=62.9241 keV, below
m_chi=104.731 keV, a one-gauge-boson chi decay is thus not introduced.
There is also no direct tree chi current for unbroken gauge bosons because
the U1 generator commutes with the unbroken algebra. These facts support
keeping a separate hard chi cohort. They do not replace a calculation of
higher-operator scattering or secondary multibody decays if those become
material in a common history.

## Checked branches and the retained partner ledger

| Inclusive quantity | S8_0 | S3_0 |
|---|---:|---:|
| Rest lifetime | 4.367102 ms | 5.827441 microseconds |
| Direct gauge-pair branch | .6146022833 | .5314586680 |
| chi + adjoint-gaugino branch | .3794989902 | .4685413320 |
| Adjoint-gaugino-pair branch | .0058987266 | 0 |
| Birth energy fraction in chi | .1897494951 | .2342706660 |
| Birth energy fraction in partner gauginos | .1956482216 | .2342706660 |

`run_production002/result.json` supplies 96-node exponential source cohorts
for chi, each partner gaugino and each gauge sector. Each cohort stores its
physical number per initial parent, birth time/scale factor, mass and
comoving momentum in GeV with a_today=1. Two-body kinematics use the actual
loop masses. Branch normalization, two daughters per event and the complete
birth-energy partition pass independently. A partner's energy is not assigned
to chi or to direct gauge radiation; its interactions and secondary evolution
remain separate state variables.

For early-NR, fixed-pole mothers in the frozen SM RD/entropy benchmark, the
mean chi propagation lengths become 302.137 and 67.3818 Mpc, with present
mean speeds 86.2009 and 10.7371 km/s. This is still a hot source compared
with 1 kpc. The cosmological benchmark does not replace the evolving parent
orbit or establish a physical full-history normalization.

Using the distinct late finite memory-stage yields gives a chi rest-density
fraction 2.18309e-7 of DM and direct gauge energy-equivalent Delta N_eff
7.83646e-7. The separately retained partner rest fraction, if stable, would
be 1.27397e-7. Transplanting the earlier warm checkpoint yields into these
fixed pole rates gives .00133400 of DM in chi and direct gauge Delta N_eff
.0253394. Those are conditional normalizations, not joined endpoints of a
new history. Partner energy is explicitly excluded from the quoted direct
gauge Delta N_eff. The former 83.8424-times-DM neutral parent estimate is
intermediate massive storage, not a final stable-relic prediction.

## Evidence and preservation

The authoritative v2 records are `run005/manifest.json`,
`run_legs003/manifest.json`, `run_bridge001/manifest.json` and
`run_production002/manifest.json`. All declare complete local input closures,
one numerical thread, wall cap 240 s and CPU cap 235 s, and measured RSS.
Their statuses are `completed` and their mathematical checks pass. The main
matching run takes about one second, with measured RSS below 341 MB.
`INTERFACE.json` describes the pole-rate and source-cohort handoff.

The initial ordinary mixed-graph attempt had its bridge-fermion momentum
sign wrong and failed the gauge test. The first inclusive color-pair attempt
merged physical zero scalars with Goldstones and failed its gauge test.
Those sources and outputs are preserved. Two serialization-only attempts
also remain preserved; they were not physics failures. `SOURCE_ARCHIVES.json`
maps superseded active-source paths to exact hash-matching originals.
No old review, skill runner, Git state, account or installation was changed.

Self-review covered the new equations, units, index orientation, source
versions, numerical transcriptions and the distinction between completed
microscopic matching and an unfinished common cosmological history.
