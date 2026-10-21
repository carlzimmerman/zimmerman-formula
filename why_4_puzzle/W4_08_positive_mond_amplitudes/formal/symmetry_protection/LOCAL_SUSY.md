# Local supersymmetry permits the specific amplitude deformation

2026-10-20. Base b37b50b1c; criteria-only1d58a0851. Root-authored
analytic construction. This packet tests whether local N1 supersymmetry
forbids the operator from ../geometric_source/GRAVITY_PHASE.md. It does
not claim a supersymmetric completion of that full MOND action, a
renormalizable microscopic theory or a healthy ultraviolet model.
The original independent normalization and full Lean goal remain open.

## 1. Exact constrained-superfield construction

Use reduced Planck units, M_Pl=1, and real f0>0,w,eta>=0 with
epsilon=f0^2-3w^2>0. Let S and A be chiral superfields constrained by

    S^2=0, S(A-Abar)=0.

The second constraint removes the imaginary scalar, matter fermion and
matter auxiliary in terms of the goldstino. In unitary goldstino gauge,
S=theta^2 F_S and A=chi is a real scalar. The constraints require F_S!=0;
they are not obtained by treating the removed auxiliary as independent.

The exact component result in Dall'Agata-Farakos1512.02158v2 section3.2,
Eqs71-79, applies to

    K=S Sbar-Z^2(A-Abar)^2/4,
    W=w+S f_eta(A), Z>0,
    f_eta(A)^2=f0^2+eta A^6/(1+A^2)^6.

Choose the holomorphic square-root branch positive on the real axis.
At each finite real chi the radicand is positive and the poles A=+/-i
are absent. The inverse function theorem gives a local holomorphic
branch; overlapping real neighborhoods glue with the chosen positive
branch. No globally entire superpotential on all complex A is asserted.
The constrained physical scalar is real. This is a local supergravity
EFT statement, not an identification of its global UV completion.

Differentiating K before taking the real slice gives K_AAbar=Z^2/2.
The source's constrained potential and gravitino mass on that slice give

    L_bos=R/2-Z^2(partial chi)^2/2-U_eta(chi),
    U_eta=f_eta(chi)^2-3w^2
         =epsilon+eta chi^6/(1+chi^2)^6,
    m_3/2=w, |F_S|=f_eta(chi).

The sign convention for R is translated to the lane's -+++ convention;
the kinetic energy and potential above have their physical signs.
Using the ordinary unconstrained potential for A would introduce an
incorrect |D_A W|^2 contribution. Its auxiliary has been removed.

The potential is Z2 invariant under A->-A. This also preserves K, the
constraints and W, with S unchanged. For r(chi)=chi^6/(1+chi^2)^6,

    0<=r(chi)<=1/64,
    f0<=f_eta(chi)<=sqrt(f0^2+eta/64).

The bound follows from chi^2/(1+chi^2)^2<=1/4. Thus F_S never vanishes
on the real slice. About chi=0, f_eta=f0+eta chi^6/(2f0)+O(chi^8).
Changing eta preserves the vacuum energy, scalar kinetic term,
supersymmetry-breaking scale, gravitino mass and every quadratic
variation about that vacuum. The complete gauge-fixed physical quadratic
action in this packet is unchanged, including the fermionic terms.

This explicitly makes the proposed forbidden operator compatible with
nonlinearly realized local supersymmetry. A nonrenormalization theorem
would preserve each allowed holomorphic input; it does not choose eta.
An additional exact symmetry could restrict f_eta, but must also preserve
the required gravitational response and matter operators.

## 2. Regular linear-multiplet diagnostic at finite mass

The preceding construction alone does not establish a microscopic
completion of its constraints. To check that this freedom is not merely
an artifact of imposing nilpotency, consider instead two ordinary,
unconstrained chiral multiplets S,T in a local supergravity sigma model.
Set w=0, epsilon=f0^2>0, x=(T+Tbar)/2, and define

    r(x)=x^6/(1+x^2)^6,
    z_eta(x)=f0^2/[f0^2+eta r(x)]>0,
    K=-Z^2(T-Tbar)^2/4+z_eta(x) S Sbar
                           -c(S Sbar)^2/Lambda^2,
    W=f0 S, c>0, Lambda>0.

These are a real analytic Kahler potential and a holomorphic
superpotential. The ordinary N1 scalar potential is now appropriate:

    V=e^K(K^i_jbar D_iW D_jbar Wbar-3|W|^2).

At S=0,T=x real, K=K_T=W=D_TW=0, D_SW=f0 and the metric is diagonal:

    K_TTbar=Z^2/2, K_SSbar=z_eta(x)>0,
    V(0,x)=f0^2/z_eta(x)=epsilon+eta r(x).

S=0 and Im T=0 are stationary transverse to this real slice. No heavy
field is eliminated without its equation. The scalar kinetic term of x
on the slice is exactly Z^2/2 at every eta. The Kahler metric is positive
in an open neighborhood of S=T=0; the displayed negative quartic is a
local EFT term and is not claimed to define the metric at arbitrarily
large S.

Because z_eta-1 starts at x^6, all local vacuum and quadratic data are
eta independent. At the common de Sitter point S=T=0, direct expansion
gives, writing T=x+iy,

    V=epsilon+epsilon Z^2 y^2
       +(4c epsilon/Lambda^2)|S|^2+O(fields^3),
    H^2=epsilon/3,
    m_y,canonical^2=2epsilon,
    m_S,canonical^2=4c epsilon/Lambda^2,
    m_x^2=0.

The inverse Kahler metric must be expanded with the same quartic: its
SSbar entry is 1+4c|S|^2/Lambda^2+..., which supplies the positive
sgoldstino mass. The other |S|^2 terms cancel between the exponential,
covariant derivative and -3|W|^2. There is no S tadpole because W=0
on the slice. The added sector is an ordinary finite-mass local
supersymmetric EFT with regular bosonic vacuum kinetic and mass data.
It is not a renormalizable UV model or a full fermionic/cosmological
unitarity theorem. The longitudinal gravitino and any added MOND portal
would require their own complete spectrum.

In particular, this scalar-gravity theory alone does not generate MOND.
Its role is an explicit supersymmetric realization of exactly the
potential deformation, with a regular unconstrained local scalar parent.
Appending an uncompleted bosonic higher-gradient portal is not enough
to claim a supersymmetric MOND model. The freedom is nevertheless not
removed by N1 symmetry itself.

## 3. Transfer to the established local amplitude test

The earlier gravitational-phase calculation is an explicitly separate
static EFT implication. If the same operator is permitted in that
local response, its relaxed coefficient is

    C3(eta)=min_(s>0){M^2[1/s+s/(9a0^2)]+eta/s^3},
    dC3/deta=1/s_eta^3>0,
    C2=M^2, epsilon fixed.

This changes R=epsilon C3^2/C2^3 and hence xi. The transfer does not
certify that the entire higher-gradient/fluid action has been embedded
in the supergravity packets above. It refutes the narrower proposed
protection claim that local N1 symmetry forbids this real scalar potential.

For the target to follow from a microscopic symmetry, that symmetry
must constrain the full metric/source and vacuum/response operators
together. In the constrained family the new parameter is in f_eta;
in the ordinary family it is in the Kahler metric z_eta. Both are allowed
supersymmetric action data. No Ward identity sets the physical invariant
R to128pi/9 in either construction.

## 4. Controls, disposition and continuation

The undeformed eta=0 family has the same positive vacuum and the stated
quadratic data. A genuine added continuous shift A->A+c would forbid
nonconstant f_eta with w fixed and S inert, hence remove the deformation.
But the inherited MOND action's explicit chi^2 and1/(1+chi^2) operators
also violate that shift. Their complete transformation must be supplied
before it can serve as protection. GOLDSTONE.md tests that obligation.

The source permits a broad constrained-superfield EFT; it does not
guarantee arbitrary finite-derivative MOND couplings share that completion.
No microscopic all-SUSY no-go is claimed. Extended supersymmetry, an
additional exact geometric symmetry, or a restrictive UV embedding is
deferred to the separately executed packets. A useful reopening must
derive which invariant forbids the explicit f_eta or z_eta family while
retaining an attractive regular MOND branch and fixing its vacuum ratio.

No script, scan or new Lean module is used for the physics in this packet.
The equations are analytic and require independent action-level review.
