# Fresh independent audit of the general-torus Schwinger-model formula

**Normalized claim.** For every L>0, m>0 and τ=τ1+iτ0 with τ0>0, on the flat periodic torus [0,L)² with metric [[|τ|²,τ1],[τ1,1]], the general-τ coefficients printed in Sachs–Wipf (SW), hep-th/9508142v1 equations (119)–(122), agree with the direct spectral kernel K=V⁻¹Σn≠0[pn²(pn²+m²)]⁻¹ and thereby support the intrinsic inverse-L condensate correction used in Urban–Zhitnitsky (UZ), 0906.2165v2 equations (41)–(44), at fixed nondegenerate τ.

**Primary verdict: refuted, with the smallest valid counterexample.** The coth coefficient in SW (119) is incorrect for τ1≠0 under its own metric and coordinate conventions. Its denominator must be 2mL|τ|, whereas the PDF prints 2mLτ0. For example τ=(3+4i)/5, any L>0 and m>0, gives the exact nonzero discrepancy

    m²K_printed − m²K_spectral = −[1/(8mL)] coth(2mL/5).

No numerical experiment is needed. At fixed shape the correctly normalized massive scalar Green function has an exact image expansion with only exponentially small finite-size corrections. In the pure massless one-flavor Schwinger model, inserting that kernel into SW (115), including its global prefactor, gives an exponentially corrected chiral condensate. This invalidates this particular source-equation route to the claimed inverse-L term. It does not prove any general theorem about finite-size effects in four-dimensional QCD.

This report is an independent source and mathematical audit. The raw hand derivation was saved as RAW_DERIVATION.md before reading the source equations themselves. No coordinator claim, checker, results, author verdict or other team report was opened. Overall fermion-sign and factor-of-two conventions are separated from the finite-size ratio below.

## Exact objects and dependency graph

Put b=τ0, c=τ1, r=|τ| and V=bL². The nonnegative Laplacian −Δ, on periodic scalar modes, has eigenvalues

    pn²=(2π/L)²[(n0−c n1)²/b²+n1²], n∈Z².

The mode normalization is V⁻¹/². The full massive Green function Gm includes the n=0 term 1/(Vm²); the massless G0′ omits it. Both coincident kernels require a common local logarithmic subtraction, but K is finite and independent of that subtraction. All sums defining K converge absolutely for m>0, b>0.

Dependencies audited:

1. Metric and periods → V and pn²: internal linear algebra/Fourier analysis.
2. pn² → one-dimensional resolvent sum → exact K: internal hand derivation.
3. Local subtraction → eta expression for G0′: convergent product/sum identity.
4. Heat-kernel Poisson summation → winding/Bessel expression for Gm: internal analytic identity, m>0.
5. Exact K plus SW (115)'s condensate/global-sector prefactor → pure-Schwinger condensate: verified algebra under that formula's measure and observable conventions; not an independent rederivation of every functional-integral step in the paper.
6. SW general-τ evaluation → UZ condensate expansion: source-equation comparison; fails as printed and under the natural typographical repair.
7. Two-dimensional calculation → a four-dimensional QCD vacuum-energy coefficient: missing physical bridge; not established here.

## Direct derivation and translation to SW notation

For a point split in x1, physical distance is |x1|. Define

    G_reg = lim[x1→0]{G(x1)+(1/(2π))log|x1|}.

An arbitrary common subtraction scale changes Gm,reg and G0′,reg by the same constant and leaves K unchanged. Summing n0 first, with μ=mL/(2π) and rn=√(n²+μ²), gives

    Gm,reg = (1/(2π))log(L/(2π))
              +(1/(2mL))coth(mLb/2) − F0/(2π)+H0/π,
    F0=Σn≥1[1/n−1/rn],
    H0=Σn≥1 Re{1/[exp(2πb rn−2πicn)−1]}/rn.

This follows from Σk∈Z[(k−u)²+v²]⁻¹=(π/v)sinh(2πv)/[cosh(2πv)−cos(2πu)]. The n1=0 contribution alone fixes the first coth coefficient to 1/(2mL); this is a direct normalization check independent of eta functions.

For the massless Green function, the n1=0,n0≠0 term is b/12, and the eta product reorganizes the remaining thermal sum:

    G0′,reg = (1/(2π))log(L/(2π)) − (1/π)log|η(τ)|.

The exact spectral identity is

    m²K = G0′,reg − Gm,reg +1/(Vm²).                 (1)

The last term is compulsory because the prime excludes n=0 in K. In particular, writing G0′−Gm with an unprojected Gm without the correction would be a different kernel. SW (116) must either use the zero-mean massive inverse or include this correction explicitly; SW (119)'s own displayed 1/(m²V) confirms the relevant prescription.

To compare to SW's F and H directly, sum n1 first instead, or exchange the lattice generators:

    τ′=−1/τ,  L′=Lr,  Im τ′=b/r²,  L′² Im τ′=V.

In this notation let A=mLr/(2π), sn=√(n²+A²), and define precisely the sums in SW (120)–(121):

    F=Σn≥1[1/n−1/sn],
    H=Σn≥1(1/sn){1/[exp(2πb sn/r²−2πicn/r²)−1]
                         +1/[exp(2πb sn/r²+2πicn/r²)−1]}.

Thus H here is twice the real-part sum H0 in the transformed frame. This prevents a factor-of-two ambiguity. Direct spectral summation yields

    m²K = −[1/(2mLr)]coth(mLb/(2r)) +1/(m²V)
           +(1/(2π)){−log|η(−1/τ)|²+F−H}.           (2)

In particular F's mass argument, H's exponents, the coth argument and the eta argument all agree with SW (119)–(121). Only the coth *coefficient* in SW (119) differs: its printed b replaces the required r. There is no change of coordinate convention or local renormalization that can fix only this coefficient while retaining all of those other terms and the stated V=bL².

Subtracting (2) from the printed SW expression gives the exact discrepancy stated at the start. On the rectangular locus c=0, r=b, this error is invisible. That is precisely why agreement with the rectangular temperature formula does not check the arbitrary-τ result.

## No fixed-shape inverse-L term

A winding vector w has physical length

    ℓw=L√[b²w0²+(cw0+w1)²].

Poisson summation of the scalar heat kernel, followed by the positive-t integral, gives

    Gm,reg = −[log(m/2)+γ]/(2π)
              +(1/(2π))Σw≠0 K0(mℓw).              (3)

Here K0 denotes the modified Bessel function, not the fourth-order scalar kernel. The local term is fixed by the plane massive Green function. For fixed b>0 and fixed c, the winding lattice has a strictly positive shortest length per L. Consequently the sum in (3) is exponentially small as L→∞; it contains no algebraic inverse-L term.

The same cancellation is visible in the sum used by the sources. Poisson summation (or differentiating the convergent F sum before applying it) gives

    F(A)=γ+log(A/2)+1/(2A)−2Σk≥1K0(2πkA).

Thus F contributes +π/(mLr) to the condensate exponent, and the correct coth term contributes −π/(mLr), with coth−1 exponentially small. H is also exponentially small for fixed shape. The cancellation is exact at algebraic order. Replacing r by b in only the coth coefficient leaves instead

    π/(mL)(1/r−1/b),

which is exactly the coefficient displayed in UZ (42). This identifies its source algebraically.

The result is nonuniform under a shape degeneration depending on L. It does not address boundaries, corners, a fixed-temperature cylinder limit, altered sectors, or a finite-size observable defined using a different global ensemble.

## Global factors, eta, bosonization and the condensate

The scalar result alone does not license dropping the gauge torons, flux sectors, constraints on Hodge scalars, or determinant/eta prefactors. SW's relevant prescriptions include the mean-zero auxiliary-field measure (37), the mean-zero gauge potentials and toron domain (81), the mass relation (86), and the flux-sector and toron integrations (112)–(115). Its current-bosonization discussion (93)–(94) explicitly concerns non-harmonic currents; a single-valued scalar does not encode the harmonic currents unless winding sectors are added. A local current identity is therefore insufficient by itself to establish the full condensate vertex normalization.

For the pure Schwinger limit g2=0, m=mγ and e²=πm², with σ=χ=0, SW (115) reduces in magnitude to

    C_L=(1/L)|η(τ)|² exp[−2π/(m²V)+2πm²K].

Insert (1). The 1/(m²V) correction in m²K cancels the explicit global flux factor. The eta factor cancels against the massless Green function. One obtains

    C_L=(1/(2π))exp[−2πGm,reg]
       =[m e^γ/(4π)] exp[−Σw≠0K0(mℓw)],
    C_L/C_∞=exp[−Σw≠0K0(mℓw)].                   (4)

This is also the normal-ordered Gaussian vertex expectation with vertex charge 2√π. It shows why the massive image calculation applies to this condensate only after the global ingredients have been checked. A full Dirac condensate can differ by a factor of two, and its sign depends on field/Euclidean conventions; neither changes (4). A θ-dependent chiral phase likewise does not restore an intrinsic inverse-L coefficient in the magnitude.

A different prescription that projects out the massive scalar constant mode changes its Green function by −1/(Vm²), and changes the corresponding vertex normalization by exp[+2π/(Vm²)]. Such a prescription must be declared. At fixed b it is an inverse-area effect, and it does not justify the source's sheared-torus inverse-L coefficient. Even in the full massive Green function, the isolated constant-mode term is not its full large-L asymptotic: the other modes compensate its algebraic appearance in (3).

For comparison, using SW's F,H notation, the consistent pure-Schwinger formula equivalent to (4) is

    C_L=(1/(Lr)) exp[−π/(mLr)coth(mLb/(2r))+F−H]. (5)

SW (115) is a source input here; I have checked its consequences and its explicitly stated zero/global-mode prescriptions, not reconstructed all finite-volume fermionic determinant measures from first principles. Accordingly (4) is verified under those conventions and the usual pure massless Schwinger theory. The scalar counterexample to SW (119) has no such conditional dependency.

## Pixel-level source audit

All numbering below refers to the assigned arXiv PDF versions. The relevant pages were rendered and inspected visually, rather than interpreting signs from text extraction alone.

| Source item | Actual check | Outcome |
|---|---|---|
| SW (13), printed p.6 / PDF p.7 | Metric, square coordinate periods, invariant volume | Agrees with the assignment: V=bL² at σ=0. |
| SW (115), printed p.42 / PDF p.43 | Global prefactor and coefficient of K | Its K exponent is positive; its flux factor and eta prefactor produce the cancellations above. Full functional-integral proof not independently audited. |
| SW (118), printed p.43 / PDF p.44 | Massless local subtraction | Agrees with G0′,reg after adding log(μR)/(2π), where μR is the source's renormalization scale. Its τ0 cancels V's τ0. |
| SW (119) | Complete coth term, constant-mode term and eta term | Coth denominator b is wrong for c≠0; (2) requires r. Constant-mode and eta structure agree. |
| SW (120)–(121) | Definition of F,H,A,z± | Agree with the direct spectral resummation in the exchanged-generator frame. |
| SW (122) | Sign and coefficient of the coth exponent | The PDF visibly prints a **positive** coth exponent. Even the printed SW (119) combined with SW (115) gives a negative one. The printed general denominator is also b instead of r. This is an additional internal inconsistency, not an OCR artifact. |
| UZ (41), printed/PDF p.8 | Whether its two exponentials multiply or add | The PDF visibly **adds** two separate terms, each with prefactor 1/(Lr). The next equation treats their exponents as combined. As printed, (41) does not imply (42); its first term alone is of order 1/L and its second has different asymptotics. |
| UZ (42) | Linear coefficient and its derivation under the charitable intended product reading of (41) | The coefficient π(1/r−1/b)/(mL) follows from SW's erroneous denominator. With the correct r both inverse-L pieces cancel. The first displayed line of (42) also uses addition where its later line uses exponent combination. |
| UZ (43)–(44) | Dependence on the condensate coefficient | The displayed inverse-L susceptibility term inherits the unsupported coefficient from (42). The separate τ0 normalization in the susceptibility and its Ward-identity definition were not independently settled by this bounded audit. |

A literal reading of UZ (41) and a charitable reading as a typographical product repair both fail to validate the stated route, for different reasons. I do not silently treat the product repair as an authenticated source equation. The rectangular locus b=r removes the particular coefficient mismatch but does not make all printed sign/addition problems correct.

## Obligation matrix and limits

| Obligation | Status | Evidence or remaining condition |
|---|---|---|
| Spectrum, volume, mode normalization | passed | Direct inverse metric and Fourier eigenfunctions. |
| Projected K and full massive constant mode | passed | Exact termwise partial-fraction identity (1). |
| General-τ coefficient in SW (119) | failed | Exact discrepancy at τ=(3+4i)/5. |
| Massless eta/local subtraction | passed | Product identity and agreement with SW (118), with explicit scale translation. |
| Fixed-shape scalar asymptotic | passed | Exact heat-kernel/Bessel image representation (3). |
| Pure-Schwinger condensate ratio | conditional | Verified from SW (115) and its stated global-mode conventions; not a new first-principles audit of all gauge-sector measures. |
| Printed SW (122), UZ (41)→(42) algebra | failed | Pixel-checked sign/addition inconsistencies. |
| Claimed inverse-L term after charitable typo repair | failed | Exact cancellation using corrected spectral coefficient. |
| All orders in a nonzero fermion mass | not addressed | UZ uses a small mass relation; the present calculation controls the massless condensate used at leading order. |
| Four-dimensional QCD or cosmological vacuum energy | out of scope | No dimensional/reconstruction/topological-sector bridge has been proved. |
| Novelty or literature-wide priority | not addressed | No novelty claim or global search performed. |

The strongest safe statement is that these specific printed equations, in these exact versions and this flat-torus setup, do not provide a valid derivation of an intrinsic inverse-L condensate correction. Correcting the scalar spectral coefficient and preserving the global factors gives (4), with exponentially small corrections at fixed shape. This does not rule out power corrections for other geometries, ensembles, observables, massless sectors, or four-dimensional theories. It supplies no numerical prediction for QCD.

No finite numerical computation supports the verdict, so no computation-audit contract is needed. The audit is a hand proof; PDF extraction/rendering, hashing and provenance collection are documentary operations only. The cheapest independent next check is to sum n1 first directly from the displayed pn² and verify its n0=0 term: it must be (2mLr)⁻¹coth(mLb/(2r)). A later review of arbitrary fermion mass or four-dimensional QCD would be a new physical obligation.

## Source authentication and provenance

Checked 2026-10-19 UTC. Primary arXiv abstract pages authenticated the following metadata:

- SW: I. Sachs and A. Wipf, *Generalized Thirring Models*, hep-th/9508142v1, submitted 1995-08-25 18:47:06 UTC. Journal reference: Annals of Physics 249 (1996), 380–429. Metadata: https://arxiv.org/abs/hep-th/9508142 . Exact-version locator: https://arxiv.org/abs/hep-th/9508142v1 .
- UZ: Federico R. Urban and Ariel R. Zhitnitsky, *The cosmological constant from the ghost. A toy model*, 0906.2165v2, revised 2009-09-11 22:06:11 UTC, after v1 on 2009-06-11. Journal reference: Physical Review D 80, 063001 (2009). Metadata: https://arxiv.org/abs/0906.2165 . Exact-version locator: https://arxiv.org/abs/0906.2165v2 .

The first exact-version web opens failed with cache misses; the canonical primary arXiv pages then succeeded and displayed their version histories. The assigned local PDFs have matching title/author/arXiv version stamps. Local PDF production timestamps (2024 for SW; 2018 for UZ, including UZ's printed 2018 date) are not submission/revision dates and were not used as version evidence. I did not assert that a later published rendering or corrigendum was checked.

Exact inputs:

- /private/tmp/fsp3-hep-th-9508142v1.pdf: SHA-256 559a000ac43c50089d8b3a5e7d40486c1723e44380146333f6421b310b45636b ; 59 pages.
- /private/tmp/fsp3-0906.2165v2.pdf: SHA-256 1c2039aaad5564b29cd4967bb771a311ae6759c0acbf68736d957132934cb8bc ; 13 pages.

Read scope: SW title/version page; metric and periods around (13); global constraints (37),(81); mass relation and determinant/partition discussion (86)–(88); bosonization/global caveats (93)–(96); projected massless inverse (101); flux and toron integration (112)–(115); and (116)–(126) for definitions, local subtraction, general-torus formula and rectangular comparison. UZ title/version page; the torus subsection on PDF pp.7–9, especially (38)–(46) and the requested (41)–(44). Full PDF text was temporarily extracted for equation-location searches, but only these selected passages were read; the temporary full-text files were removed after inspection. Page screenshots used for decisive checks: SW PDF pp.7,43,44 and UZ PDF p.8. Only review artifacts were written to the assigned schwinger_fresh directory.

The corresponding source implications are **inapplicable** for the inverse-L claim because a checked coefficient mismatch and printed algebraic inconsistencies prevent the proposed implication. SW (13),(118),(120)–(121) and the specified-mode parts of the derivation are verified after notation translation. The pure-Schwinger application of SW (115) is conditional on its full measure/normalization convention. No evidence or ledger outside this review directory was edited.
