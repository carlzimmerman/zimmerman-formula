# Independent function-agent review: matrix and flux packets

2026-10-20. Base `431f22bd6`, criteria-only `89bf113b0`.
Independent analytic reconstruction of the root's matrix packet and
the flux agent's compactification packet. No script, scan, download,
build, compilation, Lean edit or git operation was performed.

**Verdict: pass within the stated approximations and source contracts;
no required correction remains.** Neither packet derives the requested
same-state MOND invariant. The matrix frequency test is not a residue
or full spectrum certificate. The flux stability test is classical
linear stability of the specified unwarped vacuum, not a quantum or
nonlinear theorem.

## Exact reviewed files and independence

SHA256 verified from saved bytes:

| File | SHA256 |
| --- | --- |
| MATRIX_MODEL.md | `49605568df5daba99f73b57c5a41a042d5567680a81150af2d2bf85a7fb0edf1` |
| SOURCES_MATRIX.md | `1a8620dd2374cface7943ee44ca4da98206a59e63da20b95d5dbe27539601a94` |
| FLUX_GEOMETRY.md | `1ef130e0479dff44f961f54a5b7aaadb92dfd13114f3a26babe759f5f588681f` |
| SOURCES_FLUX.md | `4c5d8e4c713f12165f6db33438990c9708668c3609c57436106088dd79173c85` |

`SINGLE_FUNCTION.md` and `SOURCES_FUNCTION.md` are this reviewer's own
work and are not independently certified here. No root RESULT/verdict
was read. The induced-quantum packet is outside this saved review's
assigned scope; earlier messages checked two isolated pressure/frame
formulae and do not constitute a review of that entire packet.

## 1. Matrix vacuum functional: isolated sign and scope

I checked the versioned primary definitions `rho^2=sqrt|G|/rho_M`,
the fixed symplectic density and the matter stress convention. Writing
`A=rho_M^2 V0`, the displayed isolated vacuum term is

    S_v=-integral A/sqrt|G|.

At fixed A,
`delta(1/sqrt|G|)=(G_mu nu delta G^{mu nu})/(2sqrt|G|)`.
Comparison with `delta S_m=-(1/2)integral sqrt|G|T_mu nu delta G^{mu nu}`
therefore gives

    T_v,mu nu=+rho^(-4)V0 G_mu nu,
    epsilon_v=-rho^(-4)V0.

Independently, `delta ln rho^2=tr(e^-1 delta e)` gives the positive
frame variation printed in the primary. Thus the isolated-functional
calculation has the sign reported in MATRIX_MODEL, and the next printed
Einstein equation uses the opposite sign for that term. This comparison
is explicit in the checked HTML. I did not independently check the PDF
rendering of this discrepancy; the author's separate PDF check is
recorded in SOURCES_MATRIX.

The restriction is essential: V0, compact-space data and the symplectic
measure were held fixed for this derivative. Divergence-free frame
constraints, dilaton terms, background anharmonicity and compact-space
equations remain part of a full solution. The calculation is not a
negative-vacuum theorem for the entire matrix theory. Likewise a fixed
measure does not make the displayed dilaton-dependent functional
non-gravitating.
[Primary definitions and variations, Eqs. (2.40), (3.9), (3.12)--(3.14)](https://arxiv.org/html/2601.08031v1).

## 2. Matrix radial force: source mass remains linear

For the displayed approximate halo
`rho_eff=M delta3+M k^2 cos(kr)/(4pi r)`, I integrated the density rather
than using a rotation-curve label:

    M_eff(r)=M[cos(kr)+kr sin(kr)],
    Phi=-G_force M cos(kr)/r,
    Phi'=G_force M[cos(kr)+kr sin(kr)]/r^2.

The point-source normalization follows from
`Delta[cos(kr)/r]=-k^2 cos(kr)/r-4pi delta3`.
The small-radius correction is indeed `+G_force M k^2/2` in the signed
radial force. This uses the specified boundary/Green sector and no
independently populated homogeneous halo mode.

Every term is proportional to M for a fixed background and fixed k.
The stronger invariant statement is linearity under an arbitrary source
rescaling. This differs from the square-root source scaling of a cubic
MOND constitutive law regardless of how a finite radial interval looks.
The report correctly keeps its overall Newton normalization conditional
on the retained physical matter/dilaton/frame response, and does not
extend this linear failure to uncomputed nonlinear matrix solutions.
[Primary static Green response, Eqs. (3.34)--(3.37)](https://arxiv.org/html/2601.08031v1).

## 3. Independent commuting-mode frequency calculation

Let `u>0`, `x>=0`, `v00<0` and

    p(t,x)=(x-t)(t-x/5+u)+v00+v01 t
          =-t^2+S(x)t-P(x),
    S=6x/5+v01-u,
    P=x^2/5-ux-v00.

I independently obtained

    min_(x>=0) P=-5u^2/4-v00,      x_min=5u/2,
    discriminant=16x^2/25+(12v01+8u)x/5
                                      +(v01-u)^2+4v00.

Positive roots at x=0 require `v01>u`. Under this condition the
discriminant is increasing on x>=0. Thus the report's strict conditions

    v00<-5u^2/4,       v01>u+2sqrt(-v00)

are sufficient and necessary for two distinct strictly positive real
t roots at every x>=0 in this scalar model. If coincident positive roots
are admitted, the second inequality may be weakened to >=; its equality
gives a positive double root at x=0. The product inequality remains
strict because its equality creates a zero root at x=5u/2.

The source's V coefficients can act on components and need not be
simultaneously diagonalizable. This check therefore applies only to a
commuting single-mode scalar diagnostic. It does not identify a selected
background, prove the inequalities for physical coefficients, check
propagator residues or certify constrained ghosts/nonlinear/quantum
health. The retained scope in the report is correct.
[Primary polynomial, Eq. (4.46)](https://arxiv.org/html/2601.08031v1).

## 4. Flux action, minimum and critical endpoint

Starting with the displayed six-dimensional Einstein--Maxwell action,
I recomputed the determinant and flux factors of the stated metric:
`sqrt(-G6)=R0^2 exp(-psi)sqrt(-g4)sqrt(g_S2)` and
`F^2=2Q^2 R0^-4 exp(-2psi)`. They give exactly the potential

    V=A x-B x^2+C x^3,       x=exp(-psi),
    A=4pi R0^2 Lambda6,
    B=M4^2/R0^2=4pi M6^4,
    C=2pi Q^2/(g_e6^2 R0^2),
    chi=M4 psi.

The radion kinetic normalization, flux held fixed, and mass dimensions
agree. I did not infer a flux integer from the target.

Direct differentiation gives `V_x=A-2Bx+3Cx^2`,
`x_+=(B+Delta)/(3C)`, `Delta=sqrt(B^2-3AC)` and
`V_chi chi=2Delta x_+^2/M4^2` at the minimum. Its positive height
requires `0<Delta<B/2`. At the fold both first and second derivatives
vanish but

    V_chi chi chi=-6V0/M4^3 !=0.

It is a stationary inflection with a canonical massless dynamical field,
not a stable algebraically eliminable auxiliary vacuum. The report does
not replace its matter-trace source by a gradient-squared spurion.
[Checked primary reduction and radion context](https://arxiv.org/html/2312.03184v2).

## 5. Flux scale identity and literal harmonic blocks

At the actual vacuum reference psi0=0, direct substitution gives

    M4^2 m_rad^2=-2B+6C,
    3M4^2 H^2=B-2C,
    m_rad^2+9H^2=R^-2.

The first physical spin-two KK mass squared is `2/R^2`; the report
correctly distinguishes it from the inverse-radius scale. In the stable
positive branch `H^2R^2<1/9`, so the physical massive spin-two tower is
above its de Sitter Higuchi bound.

I specialized and diagonalized the supplied q=2 scalar and vector
blocks, checking the stated traces, discriminants and determinants.
The scalar determinant is `k_l^2(k_l^2-2/R^2)` using
`mu=-2/R^2+3c_F^2/2`. It is positive for l>=2; the special l=1 physical
scalar and l=0 fixed-flux radion require the separate treatment retained
in the report.

For the vector matrix, the trace is `2k_l^2-6H^2` and determinant is
again `k_l^2(k_l^2-2/R^2)`, because `c_F^2+6H^2=2/R^2`. Its literal
roots are centered at `k_l^2-3H^2`, with one exact Killing zero mode at
l=1. I directly checked that the primary HTML's printed root has the
opposite +3H^2 center while its displayed matrix and following Killing
claim support the report's minus sign. I did not independently check
that discrepancy in the PDF. The report correctly flags it rather than
silently quoting or altering a source formula.
[Primary blocks and qualifications, sections 5.1.1, 5.2.1, 5.4--5.5](https://arxiv.org/html/1310.6360v2).

This review checks those constraint-reduced blocks and their q=2
specialization, not a fresh derivation of every six-dimensional gauge
constraint. The source's ordinary Einstein/Maxwell signs and harmonic
decomposition contract remain part of the classical stability claim.
No arbitrary-matter, quantum or nonlinear compactification theorem is
inferred from the positive masses.

## 6. Geometric source and the actual available force window

The specified neutral zero-internal-momentum particle gives
`m(chi)=m0 exp(-chi/(2M4))`, hence `alpha=-1/(2M4)`. Its same-sign
source/test product produces attractive scalar exchange. Solving the
canonical scalar equation yields exactly the report's Yukawa potential,
`G_S=G_T/2`, and the force factor `(1+m_rad r)exp(-m_rad r)`.
The conformal spatial potential has the opposite scalar sign. The
formal gamma=1/3 and force coefficient `3G_T/2` require both an unscreened
radion and a valid four-dimensional/subcurvature regime; they are not
automatically operational calibration data.

The identity above gives
`min(m_rad^-1,H^-1)<=sqrt(10)R`. More directly, `r/R>=L`, `Hr<=eps`
and `L>3eps` imply

    m_rad r>=sqrt(L^2-9eps^2),
    g_radion/g_tensor<=
       (1+sqrt(L^2-9eps^2))exp(-sqrt(L^2-9eps^2))/2.

I checked the inequality using the decreasing function `(1+x)e^-x`.
Thus a parametrically four-dimensional subcurvature domain suppresses
the scalar. The result does not exclude a finite few-radius interval or
every other compactification, but it rules out the claimed parametric
unscreened zero-mode window in this toy.

The on-shell scalar energy has the negative nonlocal binding form
`-alpha^2 rho(-Delta+m_rad^2)^-1 rho/2`. It is not a local positive
gradient cubic, and its sign is not a ghost diagnostic. The nonzero-mass
flux equation and source-mass linearity also agree with the report.

## Source-authentication and final scope

Direct primary browser checks in this review were bounded to the exact
versioned HTML for Steinacker 2601.08031v1, Seo 2312.03184v2 and
Brown--Dahlen 1310.6360v2, and the header/context of Steinacker
2303.08012v1. I have not independently recomputed the IKKT one-loop
spectral integrals, authenticated every earlier cited theorem, or
constructed the matrix quantum state. The spectral coefficients remain
quoted one-loop inputs with the report's background qualifications.

Within those bounds the raw vacuum-sign, radial mass law, scalar
frequency, compactification minimum/fold, scale and force claims all
reconstruct. Neither report conflates a common microscopic/classical
functional with a selected positive cubic amplitude. No required
correction remains in the pinned documents, and no end-to-end physical
or Lean normalization claim is certified by this review.
