# Fully varied transition: elliptic gravity worsens stiffness, with a finite-band repair

Checkpoint SOL61-CONSTRAINED-TRANSITION-20261005-A. Supplied base `11b994fee`;
observed initial HEAD `614eab208a205314e7076c4edfe018c9b78e47f7`. Actual inputs
are pinned by both version-2 runner manifests. Writes confined to this directory.
**No complete main theory is obtained.** The new action result is a fully
sourced nonrelativistic gated-AQUAL example in which elliptic constraint
elimination cannot rescue a negative frozen transition direction. It actually
creates a finite-rate instability at an explicitly frozen-stable point. A
positive spatial internal-state energy yields an exact finite unstable band
and positive ultraviolet characteristic speeds; its gas cost is quantified.

This advances the earlier omitted constitutive variation rather than repeating
its fixed-B scan. It is not the C-H/K chassis, QUMOND, candidate B's prescribed
ownership rule, or CFG349's first-order irreversible ratchet. CFG349 now records
its ordinary-action energy liability and CTP reaction failure, plus embedded
class-E inheritance failure. The present construction uses positive internal
kinetic energy and varies reciprocal gravity; it inherits none of CFG349's
host/FRW results. The bounded internal comparison does not establish worldwide
novelty.

## 1. An explicit action and the physical variables

Use a single nonrelativistic baryon fluid, particle mass m>0, number density n,
velocity v, positive internal-state inertia I and stiffness K. Let Dq/Dt=
q_t+v dot grad q. A longitudinal-sector variational action is

    S = integral dt d^3x {
      mn |v|^2/2 + nI(Dq/Dt)^2/2
      -e(n)-nK[q-Q(n)]^2/2 -mn Phi-U(q,grad Phi)
      +lambda[partial_t n+div(nv)] },

    U(q,g) = [|g|^2+f(q)(2|g|^3/(3a0)-|g|^2)]/(8piG),
    g=grad Phi.

The continuity multiplier enforces particle-number conservation. Varying v
and lambda gives the usual fluid potential representation; the quadratic
longitudinal density/displacement mode is physical, not a freely imposed
source. This action is sufficient for the studied irrotational/local sector;
it is not a general collisionless baryon or vorticity model. All source and
q dependence is varied before eliminating Phi. The positive fluid/internal
kinetic terms are retained. Standard variational boundary conditions or
periodic nonzero Fourier modes are assumed.

Choose smooth bounded f in [0,1], flat OFF/ON outside [0,1], and a density
reader Q with flat endpoints. The finite controls use the C^2 quintic
smoothstep f(x)=10x^3-15x^4+6x^5 and Q(n)=f(n-1), with constant extension.
They introduce threshold/profile, K,I and optionally kappa: these are declared
new choices, not a zero-constant construction. This kernel is the simple
local deep-MOND AQUAL kernel on its ON plateau, not nu_mono or P2 and not a
specified high-acceleration interpolation. The example supplies a sourced
action, not the adopted force law's complete phenomenology.

The Phi equation is

    div {[(1-f)+f |grad Phi|/a0]grad Phi} = 4piG mn.

At f=0 it is Newtonian; at f=1 it is the standard deep-MOND elliptic equation.
The internal equation, using number conservation, is

    nI D^2q/Dt^2 + nK(q-Q)+U_q = 0.

No one-way response was added. Translation/time invariance of the underlying
bare action gives the usual coupled momentum/energy balance subject to flux
boundaries. This does not establish a covariant conserved cosmology.

**Background limitation.** A uniform n0 with constant nonzero g0 is not a
global solution of the sourced Poisson/AQUAL equation. The calculation is a
local WKB/Jeans patch of a presumed slowly varying background, or a zero-mean
periodic perturbation problem with prescribed affine external field and the
uniform acceleration removed. Mean subtraction/boundary forces are background
inputs. All k are local perturbation labels; the small-k endpoint is a formal
constant-coefficient diagnostic, not a verified global halo mode. No global
hydrostatic equilibrium, mean-density variation, FRW or turnaround was solved.

## 2. The actual variational sign and elliptic block

The constrained static Hamiltonian contains e+nK(q-Q)^2/2+mnPhi+U. Its field
block in Phi is positive, although eliminating Phi produces negative attractive
source energy. This is the correct Newtonian gravitational sign, not a claim
that the full matter/gravity Hamiltonian is positive.

For g0>0 and a perturbation direction making cosine mu with g0,

    a_parallel=U_gg=[1-f+2f g0/a0]/(4piG),
    a_transverse=U_g/g0=[1-f+f g0/a0]/(4piG),
    a_field=a_parallel mu^2+a_transverse(1-mu^2)>0,
    h=U_qg mu=f'(g0^2/a0-g0)mu/(4piG).

This proves radial and transverse local ellipticity for 0<=f<=1,g0>0.
It is not uniform ellipticity on a gate-ON zero-field point, where deep-MOND
can degenerate. In particular, do not infer general zero-field health or a
QUMOND auxiliary-field sign from these coefficients.

At fixed g0, define B=[g0^2-2g0^3/(3a0)]/(8piG)>0 for g0<3a0/2. The static
local energy has the previous frozen form E=e+nK(q-Q)^2/2-B f(q). Let
E_nn,E_nq,E_qq be its *full* Hessian at a stationary local q (nK(q-Q)=B f').
The field-source and constitutive mixing are both present. With Fourier k!=0,

    H_frozen = [[E_nn,E_nq],[E_nq,E_qq]],
    C = (m, i k h)^T,
    H_PhiPhi = a_field k^2,
    H_reduced = H_frozen - C C^dagger/(a_field k^2).

The density inertia is m/(n k^2), because delta n=-n div xi and fluid inertia
is mn|xi_dot|^2/2. Internal inertia is nI. Both are positive. Phi has no time
kinetic term; its primary momentum-zero and elliptic secondary constraint
eliminate Phi and its momentum. They do **not** remove the nonzero Fourier density displacement, which
preserves total particle number. The global k=0 number mode is not
part of this argument.

For every allowed physical vector x,

    x^dagger(H_frozen-H_reduced)x
       = |C^dagger x|^2/(a_field k^2) >= 0.

Thus a strictly negative frozen direction stays negative after field
elimination, and the least normalized eigenvalue cannot increase. This is a
proof for this positive elliptic variational block. It does not apply by
assertion to indefinite multi-auxiliary QUMOND actions, lapse/shift/gauge blocks
or a constraint that actually removes the density direction. Those require
their own constrained reduction. It also does not assert that every negative
static direction is a catastrophic pathology.

## 3. Full coupled dispersion and an instability missed by freezing gravity

Put w=omega^2, a=a_field and

    A(k)=n E_nn k^2/m - J,       J=nm/a,
    b=(E_qq-h^2/a)/(nI),
    L=E_nq^2/(mI),              M=m h^2/(a^2 I).

The exact local longitudinal/internal characteristic polynomial is

    [A(k)-w][b-w] - [L k^2+M] = 0.                         (1)

In particular the reduction contains both the usual attractive density term
-m^2/(a k^2), an additional q stiffness -h^2/a, and the Hermitian density/q
mixing E_nq+i m h/(a k). The imaginary Fourier mixing is not a dissipative
force; its modulus contributes the M term. Dropping f' variation misses both
of its effects. No oscillation frequency is obtained from static stiffness
alone: equation (1) retains the physical kinetic matrix.

Finite example, units 8piG=a0=m=1:

    n=1.5, g0=.2, K=100, I=.01, e''=0,
    q=.500433332682373,
    E_nn=527.181250244110,
    E_nq=-281.206666731763, E_qq=150.000450665651,
    a_parallel=1.399025001953, a_transverse=1.198700002604,
    h=-.599999098670.

At k=10^4 the frozen low mode is +.0298069123, but the full field variation
makes it -17.1249437284. The limit is -17.1249457582. The added constitutive
correction h^2/a, about .25732129, overwhelms a small positive frozen Schur
margin. This is a sourced local counterexample to extending frozen transition
health to the varied field, not an observed host or a complete candidate-B
counterexample. The mutation that drops h produces the wrong UV sign and
fails the two decisive witness/UV checks, with its failed run retained.

The finite transition scan covers 19 n values in [1.05,1.95], three angles
mu=0,.5,1 and k=.01,1,10,10^4. Ellipticity and inertia remain positive, and
the full low eigenvalue never exceeds the frozen one on all 228 points.
That scan corroborates the exact Schur theorem, not a global sampling proof.

## 4. Bounded spinodal growth is a different physical premise

If E_nn>0 and b>0, define alpha=n E_nn/m. The high-k low root of (1) tends to

    w_infinity = [E_qq-h^2/a-E_nq^2/E_nn]/(nI).              (2)

A negative finite value is a spinodal/internal relaxation-direction instability,
not a negative kinetic energy and not a growth rate proportional to k. The
other root grows as alpha k^2>0. If E_nn<0 instead, the fluid high-k root is
negative proportional to k^2 and growth is unbounded: that is the dangerous
Hadamard case, separate from the example. Nothing here proves an all-background
strongly hyperbolic nonlinear evolution; cold plateau dust and shell crossing
retain their own limitations.

There is also an **exact uniform rate bound**, not just a finite-k plateau.
For s=gamma^2>=0, substituting w=-s into (1) gives

    P(-s)=k^2[alpha(b+s)-L]+(s-J)(b+s)-M.

Let s_infinity=L/alpha-b and
s_0=(J-b+sqrt((J+b)^2+4M))/2. For s>=max(s_infinity,s_0) both terms are
nonnegative. Since the upper frequency root is positive under these premises,
no negative root can have magnitude greater than that s. The two k endpoints
attain the corresponding limits, so

    sup_k gamma(k)=sqrt(max(s_infinity,s_0)).

The implementation rationalizes s_0 to avoid cancellation. At the example
I=.001,.01,.1,1,10 give UV rates 13.0862,4.13823,1.30862,.413823,.130862.
At I=1 the exact uniform maximum is approximately 1.03634, only just above
J^1/2=1.03546. Thus a larger finite internal inertia really can slow the new
transition mode to a gravitational timescale; the assertion is exact within
the constant-coefficient patch, with finite controls corroborating it.
The long-wave maximum includes ordinary attractive Jeans growth. It cannot
be advertised as a new uniquely selected formation signal.

This keeps a plausible changed-premise door open: allow a finite formation
instability rather than require every local omega^2>0. But without spatial
state energy, its short-wave rate reaches a nonzero constant, so there is no
intrinsic smallest fragment scale. Nonlinear saturation, turbulent heating,
initial seeds and a physically selected scale remain absent; boundedness alone
does not predict selective host formation or ownership.

## 5. Inertia/pressure response costs are not removed

For the same full-field action family, a pressure control e''=20,I=10^-8 has
positive coupled roots at all 198 points n in [1.01,1.99] (99 samples), k=1,10,
mu=1. Compared with the ordinary gas-plus-gravity baseline
w_gas=n e'' k^2/m-J, the maximum low-branch fractional change is .0550116.
At these fast-response controls b is far above the tested gas frequencies;
mode identity is unambiguous. The e''=5 and 10 controls instead change the gas
mode by .243558 and .113681 at their worst points. These are dimensionless
pressure/inertia examples, not astrophysically allowed temperatures, and not
transferred CFG347 gas tests.

There is an explicit shared-inertia tension across hypothetical media with
the same n=1.5,q,K,g0 but different gas stiffness. Requiring the cold UV rate
not exceed J^1/2 requires I>=.159721515. The pressure-supported e''=20 state
satisfies the tested 10% gas response at k=1,10 only for
I<=7.65295774e-5 on the followed low branch. These bounds differ by a factor
2087.06. This is a scoped common-parameter discriminator across cold/warm
states, not a universal no-go: gas equation of state, density width, K, gravity
kernel, state dependence of I, allowed formation rate or relevant physical
wavenumbers can change it. Comparing a low branch after mode exchange would
be misleading; the 10% boundary here occurs in the unambiguous fast-response
regime.

## 6. Constructive spatial-gradient completion: a finite formation band

Add the physical positive static energy kappa|grad q|^2/2, kappa>0, equivalently
L_grad=-kappa|grad q|^2/2 to the same action. It gives +kappa k^2 in E_qq and
adds the appropriate gradient force/reaction; it is not post-variation smoothing.
The full q equation acquires -kappa Delta q on its left. For E_nn>0 the
high-k principal speed squares become

    c_fluid^2=n E_nn/m,     c_q^2=kappa/(nI),

both positive. The density/q off-diagonal terms grow only as k and do not
change these leading characteristic roots. No relativistic luminality claim
is made for the dimensionless NR example.

The zero-frequency determinant has the sign of the quadratic in y=k^2:

    kappa E_nn y^2
    +[E_nn(E_qq-h^2/a)-E_nq^2-m^2 kappa/a] y
    -m^2 E_qq/a.                                           (3)

If E_qq>0 there is one positive root y_cut. With positive high root, unstable
modes occupy k<sqrt(y_cut), and both modes are positive above it. Thus this
is an exact finite-band completion under the local premises. Conventional
Jeans instability remains at the long-wave end; it is not a fully stable halo.

For the example, I=.01:

| kappa | k_cut | maximum sampled growth | fastest sampled k | local q length proxy |
|---|---:|---:|---:|---:|
| .0001 | 50.6906 | 3.86792 | 12.6474 | .00081650 |
| .01 | 5.14368 | 2.29225 | 2.96483 | .00816495 |
| 1 | .773440 | 1.07226 | .347536 | .08164954 |

Growth maxima are finite grid values (1001 log-k points from .001 to10^4),
while cutoffs are computed from exact equation (3). The length proxy is
sqrt(kappa/E_qq); it is not a solved spatial edge. In particular the soft
spinodal length can be much larger than this internal restoring length.

The completion has a measured response cost. On the e''=20 fast-inertia warm
midpoint control, at k=1,10 the maximum gas-mode changes for the same three
kappa values are .0469386,.129981,10.5311. The smallest gradient control keeps
the finite UV cutoff and local gas fidelity but permits growth about 3.74 times
the Jeans rate. The large-gradient control slows the growth nearly to Jeans
but badly fails that gas comparison. Saturated constant-q branches keep their
zero internal-gradient stress, but a real spatial edge has gradient energy and
forces; its width and host profile must be solved before importing any data
pass. This explicitly states what the new door buys and what it costs.

## Audit and next implication

Passed as derived in this action's local sector: actual Hamiltonian sign;
radial/transverse ellipticity; nonzero physical density mode; full sourced
field/constitutive Schur reduction; dispersion; uniform finite growth bound;
positive-gradient principal roots/cutoff; concrete pressure and inertia costs.
No broad no-go against QUMOND, relativistic constraint systems, multi-fluid
cold matter or a differently coupled internal sector follows.

Still open: a global sourced background and moving edge, baryonic mean/reference
variation, full relativistic stress, the adopted kernel, FRW perturbations,
collisionless/multistream baryons, nonlinear formation/saturation, ownership,
cold distribution and matching to the reciprocal cold lane's action.
A negative mode is not evidence that the desired formation and mergers happen.
The positive-gradient completion is the next live constructive route: solve a
finite spatial boundary with the same action and conserved fluid, then test
its stress/response at independently fixed physical K,I,kappa and density
width. There is no permission to splice its characteristic result into another
gate or carrier action.

## Reproduction and provenance

Author self-review. Code `checks.py`; exact contract `contract.json`;
authoritative `runs/main_a/{manifest.json,results.json,stdout.txt,stderr.txt}`.
The bounded runner completed and validate_manifest --root passed. Its
`runs/mixing_drop_a/` negative control exits 1 and is itself a valid failed
provenance record; source inputs remain unchanged. Wall30s, CPU20s/process,
1MiB output, cooperative single-thread numerical libraries; no memory or
CPU-affinity cap requested. Raw custom preliminary/corrected/gradient/uniform
checkpoints are retained, but they are secondary to final manifests.

An initial symbolic cutoff check used an erroneous normalization m*n*I and
an extra k^2. The explicit polynomial and numerical cutoff were correct;
fixing the comparison to m*I made the identity pass. Its preliminary result
records that failed check. The pre-fix script itself was not snapshotted and
its hash is unavailable, so that record is historical, not fresh evidence for
the final script. No mathematical failure or negative mutation was deleted.

Rerun into a new directory under this lane:
`python3 .../constrained_transition/checks.py --output-dir <new lane subdirectory>`.
Add `--mutate-drop-constitutive-mixing` for the expected failing control.
Exact proofs above, rather than the check count, establish the scoped results.
