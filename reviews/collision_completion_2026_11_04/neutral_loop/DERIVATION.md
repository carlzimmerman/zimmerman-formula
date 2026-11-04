# CC10 neutral-adjoint leading radiative exits

At the prescribed pole, neither tree-terminal neutral adjoint is absolutely
stable. Their complete leading vacuum two-gauge-boson amplitudes are nonzero.
The octet decays predominantly to a gluon and the residual U1 boson, and the
triplet to a residual SU2 boson and the U1 boson. These are gauge bosons of the
model's unbroken group; no visible-sector portal is asserted.

For e=.003, mu=2e6 GeV and x=25.4000254000381:

| State | M/mu | Gamma_gauge/mu | Rest lifetime from gauge exit |
|---|---:|---:|---:|
| S8_0, each of eight real components | .002645913359 | 4.631658829e-29 | .007105574711 s |
| S3_0, each of three real components | .01010505261 | 3.001424320e-26 | 1.096499339e-5 s |

This establishes a radiative exit and its local rate. It does not establish
that a moving, hard neutral population has already radiated its energy.
An evolving momentum bin decays with rate Gamma(x) M(x)/E, and the accumulated
optical depth must be integrated along the actual orbit.

## Canonical normalization and block traces

The model uses fundamental generators t=T/sqrt(2), tr(t_b t_c)=delta_bc/2.
Let Q_b denote their matrices on real scalars, Takagi Weyls, or real vectors,
as appropriate, and let P_bc={Q_b,Q_c}/2. The U1 generator is
diag(2,2,2,-3,-3)/sqrt(60), with q^2=5/12 on broken components.

For external real scalar S_a, define the potential cubic C_aij, Yukawa y_ija,
and K_aij=partial M^2_V,ij/partial S_a. Each trace below is within one
equal-mass internal block. Terms connecting different masses vanish because
the unbroken Q_b commute with the mass operators. This is a matrix insertion
trace, including all representation copies; it is not a singlet color-factor
substitution.

With tau=M_a^2/(4m^2), the coefficient convention is

    L_eff = g^2/(32 pi^2) S_a sum_bc
            [CE_abc F_b.F_c + CO_abc F_b.Fdual_c],

    CE_abc = sum_realS 1/4 Tr[(C_a/m^2) P_bc] A0(tau)
           + sum_Weyl 1/2 Tr[(Re y_a/m) P_bc] Ahalf(tau)
           + sum_realV 1/4 Tr[(K_a/m^2) P_bc] A1(tau),

    CO_abc = sum_Weyl 1/2 Tr[(Im y_a/m) P_bc] AhalfP(tau).

An overall convention change for CO has no effect on the reported unpolarized
widths. The form factors are

    A0=(f-tau)/tau^2,
    Ahalf=2[tau+(tau-1)f]/tau^2,
    A1=-[2tau^2+3tau+3(2tau-1)f]/tau^2,
    AhalfP=2f/tau.

For tau<=1, f=arcsin(sqrt(tau))^2; above threshold the usual -1/4(log-i pi)^2
continuation is used. Small-tau series avoid cancellation. The limits are
(1/3,4/3,-7,2). The source normalization and the project translation were
checked against [Djouadi v2, equations 2.45–2.48 and section 2.4.1](https://arxiv.org/pdf/hep-ph/0503172v2).

Independently, a charge-one Dirac fermion comprises two Weyls. For y=m/v the
trace gives CE=Ahalf/v. A complex scalar comprises two reals and gives
CE=C A0/(2m^2). A complex broken vector comprises two real vectors and gives
CE=K A1/(2m^2). Thus a standard K=2m_V^2/v produces A1/v. For one photon,
L=c S F^2 has width c^2 M^3/(4pi). Consequently

    Gamma_a = g^4 M_a^3/(4096 pi^5)
              sum_bc (|CE_abc|^2+|CO_abc|^2).

The ordered b,c sum counts distinct mixed-boson final states twice, correctly
reproducing the width of the combined operator 2c_bc S F_b.F_c. With
CE_abc=k d_abc for SU3 this gives the familiar d_abc d_abc=5/3 for fixed a.
The colored-scalar tensor and mixed-channel phase-space conventions also
agree with [Hayreter–Valencia v3, equations 4 and 23](https://arxiv.org/pdf/1810.04048v3).

## Gauge completion of the vector loop

The vector A1 includes the broken gauge boson, its Goldstone and ghost
contributions. Goldstones are removed from the physical scalar A0 sum.
K is obtained directly by differentiating

    M^2_V,ij=2g^2 Re[(R_i z)^dagger R_j z]

along z -> z + E O_a S_a. No mass-eigenvalue derivative along the singlet
valley is substituted for this adjoint insertion.

The remaining possible physical scalar/vector mixed loop is absent here.
For unbroken b, R_b z=0. The A_b V_i S_r vertex is proportional to
Re[E_r^dagger R_b R_i z]. Replacing R_b R_i z with [R_b,R_i]z shows that
this lies in the Goldstone tangent subspace. Every physical scalar is
orthogonal to that subspace, and unbroken generators preserve it. Thus an
unbroken external gauge vertex cannot convert a broken vector into a physical
scalar. Mixed Goldstone/vector diagrams belong in A1. Unbroken generators
also do not mix massive and massless vector blocks.

The on-shell Goldstone relation is checked directly from the component cubic,

    C_a,G_i,G_j = M_a^2 K_aij/(2m_V^2).

At the pole its maximum error is 4.32e-20. The maximum physical
A_unbroken–V_broken–S vertex is 1.40e-16; the residual is floating-point
Goldstone/physical leakage. Mass/charge commutators, Takagi reconstruction,
and Goldstone orthogonality are recorded in the result.

The U1 charge-squared traces over physical real scalars, Weyls and real
vectors are respectively (15,15,5). Their beta contributions are
15/6+2(15)/3-7(5)/2=-5, matching the charged threshold of the SU5 model with
two adjoint chiral multiplets. This independently checks the vector sign and
real-field counting. Width matrices over each external irrep are proportional
to its identity; internal mass-block rotations reproduce the amplitudes.

## Finite mass, selection and interference

At the pole the octet is CP even in the calculated tensor, with odd amplitude
norm below 6e-15. Its gauge width splits into

    Gamma(gg)/mu = 3.548998867e-33,
    Gamma(gY)/mu = 4.631303929e-29.

The triplet is CP odd, with even tensor norm below 3e-15, and its entire
nonzero gauge width is WY. SU2 has no symmetric d_abc tensor; the mixed
triplet–SU2–U1 tensor is allowed. The octet gY and triplet WY amplitudes are
therefore not selection-forbidden. Forbidden channel residual widths are
below 3e-53 mu at the pole.

The exact/soft width ratios are .9976176305 for S8_0 and 1.0083919801 for
S3_0. Active scalar/fermion/vector tau maxima are respectively
(.25,.1570856683,.00008046963) for the octet, and (0,.01650410383,0) for the
triplet. Spectator masses can have tau>1; their relevant insertion trace is
zero. The code records active mass blocks separately to avoid interpreting
an uncoupled spectator cut as a physical decay channel.

Omitting the vector multiplet would give the octet width 2.321534673e-28 mu,
5.0123 times the full result. Matter-only matching is inadequate even though
the final amplitude is nonzero. At x=100 the widths are 5.112657980e-32 mu
and 4.021187876e-29 mu, corresponding to 6.43708 s and .00818430 s. Continued
outward motion can lengthen the lifetime substantially.

At fixed sqrt(e)x and fixed g/e, masses scale as sqrt(e), cubics as e^(3/2),
and Yukawas as e. Therefore CE,CO scale as sqrt(e) and these widths as
e^(13/2), not as a tree width. Direct evaluations at e=.001,.003,.01 confirm
this relation. The fixed-scaled-pole octet gauge-only lifetime is 8.97196 s
at e=.001 and 2.83718e-6 s at e=.01, holding mu fixed. These are rates in
different microscopic packets, not completed cosmological histories.

## Additional prospective photino source: soft gaugino insertion

`gaugino_vertex.py` differentiates the full finite scalar-plus-vector gaugino
threshold under each canonical component of the actual neutral adjoints.
It holds all twelve old unbroken gaugino columns fixed; it does not
differentiate a singlet-only mass function or rotate the external basis with
the displaced background. The auxiliary F and all mass/vertex dependence
change with z.

The historical `component_data` restricts its Takagi branch to a realified CP
slice and rejects generic CP-odd variations. The local displacement builder
therefore reproduces its H, M_F, M_V and F formulas and uses a generic
2n-dimensional real symmetric Takagi problem. Nearly zero columns can have
an unweighted orthogonality error of 3.4e-6, but their mass-weighted error is
5.43e-15; M_F reconstruction is below 8.1e-16. The baseline threshold agrees
with the original model to 1.35e-11 relatively. Only the chirality-flipping,
mass-weighted combinations enter this threshold derivative.

For L=-S y_ij lambda_i lambda_j/2+h.c. and negligible daughter masses,

    Gamma_soft = M/(16pi) sum_ordered_ij |y_ij|^2,
    Gamma_soft,mixed-chi = M/(8pi) sum_b!=Y |y_bY|^2.

Three central steps (.002,.001,.0005) and Richardson extrapolation give:

| Parent | Mixed channel | norm(y_bY) per component | Gamma_soft/mu, xi=1 |
|---|---|---:|---:|
| S8_0 | lambda_SU3 + chi | 5.212656097e-13 | 2.860578738e-29 |
| S3_0 | lambda_SU2 + chi | 3.806800371e-12 | 5.826649916e-27 |

The source self-energy normalization was checked in
[Martin v2, section III, equations 3.2, 3.4 and 3.6](https://arxiv.org/pdf/hep-ph/0509115v2).
That source and this differentiation establish a soft insertion; they do not
by themselves establish an exact on-shell three-point amplitude.

The triplet soft amplitude changes by 15.29724% between xi=1 and xi=2,
giving Gamma_soft,mixed/mu=4.180363426e-27 at xi=2. Its Q2=1 versus 7
difference is below 1.7e-7. The octet xi and Q differences are below 8.6e-6
and 1.5e-6. The triplet xi dependence is a real limitation of the soft
off-shell derivative, not a numerical step error. The missing implication is
the finite-momentum scalar–gaugino–gaugino three-point function at
p_S^2=M_S^2 and p_lambda^2=m_lambda^2, including Goldstone/gauge and scalar
equation-of-motion contributions required to cancel its gauge dependence.
More specifically, the threshold helper changes its Goldstone gauge-fixing
projector with the displaced z. Relating that background derivative to an
ordinary physical scalar vertex with gauge fixing held at the original vacuum
requires the corresponding gauge-fixing/longitudinal-vector–Goldstone mixed
insertions. The off-shell derivative includes those background variations; it
cannot simply be declared the gauge-independent on-shell S-matrix element.

For mixed chi entries only the old U1-charged heavy sector couples, with
lightest mass .03872983346 mu. M_S^2/m_charged^2 is .00466724 for the octet
and .0680747 for the triplet. The scalar/vector soft-vertex cancellation
condition (norm(y_scalar)+norm(y_vector))/norm(y_total) is 2.34796 and
2.12230. Their products with those expansion parameters are .0109585 and
.144475. These quantify sensitivity; they are not rigorous bounds on the
uncomputed on-shell correction. There is no large cancellation making the
soft nonzero result numerically meaningless.

Using these soft estimates with the certified gauge-pair widths would give
one-chi branching fractions .3818 for the octet and .1626 for the triplet
(.1223 at xi=2). These are conditional estimates, not certified branching
fractions. The one-loop photino mass here is 104.73075 keV; an unboosted
parent gives p_chi/m_chi about 2.5264e7 and 9.6486e7. Such daughters require
their own momentum distribution and subsequent redshift, rather than being
counted as an initially cold population. The mixed soft vertex scales as
e^3 at fixed sqrt(e)x, checked at e=.001 and .01 to 2e-7. Its width therefore
has the same e^(13/2) scaling as the gauge exit: weakening e alone does not
remove this prospective hard-photino branching.

## Records, failures and interpretation

Authoritative numerical records are `run004/manifest.json` and
`run_gaugino003/manifest.json`, both fresh v2, status `completed`. Their
results pin every imported local source and report measured macOS RSS.
The gauge run takes 3.01 s with RSS 303611904 bytes; the final gaugino run
takes 6.41 s with RSS 267403264 bytes. Every job used one numerical thread,
wall cap 240 s and CPU cap 235 s; no address-space or affinity cap was used.
Both final manifests validate with the installed validator and project root.

`run001` failed when an overly broad internal-cut check encountered a
spectator threshold; its exact source is `loop_v1_failed.py`. `run002` then
computed the complex continuation; `run003` added covariance, basis and
weak-scaling checks; `run004` distinguishes active blocks from numerical
CP-forbidden traces. Superseded originals are preserved as `loop_v2_completed.py`
and `loop_v3_completed.py`. `run_gaugino001` failed an unweighted nearzero
Takagi-column check; its result still records the physical derivatives.
`gaugino_vertex_v1_failed.py` preserves that source. The corrected mass-weighted
diagnostic and larger steps are in `run_gaugino002`, with source preserved as
`gaugino_vertex_v2_completed.py`; `run_gaugino003` adds the scalar/vector
cancellation diagnostic. Superseded manifests refer to their original active
source pathname; archive hashes in `SOURCE_ARCHIVES.json` authenticate those
exact originals. They are not claimed to validate against today's active file.

Finite outcome: the full leading gauge-pair vacuum widths, their normalization,
gauge completion, representation covariance, and tested weak scaling are
verified in the stated numerical range. The soft mixed-gaugino insertions are
reproduced and numerically stable, while their conversion into exact on-shell
branching fractions remains conditional. This calculation closes the assertion
of absolute tree-terminal stability and identifies a material additional
photino-source obligation; it does not close the common kinetic history.

Self-review: all new equations and numerical transcriptions were checked in
context; no unrelated mathematical text was edited. Exact primary PDF versions
were authenticated through the web reader on 4 November 2026. No local PDF was
retained, so no retained-file hash is asserted.
