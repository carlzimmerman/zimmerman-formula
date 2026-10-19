# SU(2) charge-normalization bridge: NB-001

**Verdict: ill-typed or internally inconsistent.** There is no single dictionary
that preserves the stipulated microscopic action, its coupling g, L, mW=v,
smooth flux 4pi, and unit vertex exp(i phi), while identifying both the printed
Unsal-Yaffe (3.15) core action and (3.25) dual kinetic term with that same
theory. The local mismatch is exactly a factor two. This verdict concerns the
specified equations as printed, not the validity of the whole paper.

The raw derivation was frozen before either project report was read; its hash
and the exact audit scope are in AUDIT_CONTRACT.md. This is an independent
derivation relative to those reports, followed by a source comparison; no
independent symbolic/numerical computation is claimed.

## 1. Forced microscopic dictionary

For T^a=sigma^a/2, tr(T^a T^b)=delta^{ab}/2, and the ordered mu,nu contraction
in S4=(1/(2g^2)) integral tr F_mu nu F_mu nu, define
B_i^3=(1/2) epsilon_ijk F_jk^3. Then

    SB = KB/2 integral (B^3)^2,       KB=L/g^2,
    div B^3=4pi rho,                 rho=sum q_j delta(x-x_j).

Insert exp[-i/(4pi) integral phi(div B^3-4pi rho)] and integrate B. The vertex
is exp(i q phi), phi has period 2pi, and

    Sdual,kin = kappa_d/2 integral (d phi)^2,
    kappa_d = g^2/(16pi^2 L),
    Spair = (4pi L/g^2) sum_(i<j) q_i q_j/r_ij.

More generally, div B=Q rho forces the invariant

    KB Q^2 = 1/kappa_d.

The BPS square including A4 gives SBPS=4pi L v/g^2; at v=mW=pi/L,
S0=4pi^2/g^2. Thus kappa_d*S0=1/(4L). Fundamental Wilson probes carry
charges +/-1/2 in A^3, W bosons +/-1; in the canonically normalized 3D field
they are +/-g3/2 and +/-g3, g3=g/sqrt(L). The canonical monopole flux is
4pi/g3. The fundamental and W Dirac products are 2pi and 4pi respectively.

## 2. Exact source comparison

Source: Unsal-Yaffe, [0803.0344v2](https://arxiv.org/abs/0803.0344v2),
22 March 2008. The supplied PDF's SHA-256 matches a fresh official arXiv
download. PDF pages 4,16-19 were read as pixels, covering (2.1), footnote 13,
(3.9), (3.15), (3.17), (3.20), (3.25), and footnote 14.

The source roots are alpha=(1,-1), alpha^2=2. Its (3.9) vector magnetic field
is explicitly the list of diagonal matrix magnetic fields divided by g:

    Bvec = (B^3/(2g), -B^3/(2g)),
    flux(Bvec)=(2pi/g) alpha.

Consequently the original trace action requires SB=L integral |Bvec|^2.
Its printed Coulomb formula (3.17) instead uses the energy appropriate to
SB=(L/2) integral |Bvec|^2. For equal unit SU(2) charges it gives
2pi L/(g^2 r), half the microscopic result. Equation (3.20) agrees with
(3.17): its ordered-pair sums supply the ordinary additional factor two.
There is no remaining pair-counting ambiguity.

In (3.25), set sigma_vec=(phi/2,-phi/2), so alpha.sigma=phi and
|d sigma_vec|^2=(d phi)^2/2. Its kinetic term then gives

    kappa_d,printed = g^2/(8pi^2 L).

It agrees with the printed Coulomb sector, but its product with the unchanged
(3.15) core action is 1/(2L). Footnote 14 prints a diagonal Maxwell coefficient
L/(4g^2) times sum_j (F_mu nu^(j))^2; the original trace action gives
L/(2g^2) times that same diagonal sum. This independently locates the same
factor two. Footnote 13's choice tr(t^a t^b)=delta^{ab} changes the component
basis; it does not change the trace of the matrix field strength or the
fixed monopole flux. Canonical eigenvalue-vector fields would be sqrt(2)Bvec,
with electric root charges (g/sqrt(2))alpha and magnetic charges
(2pi sqrt(2)/g)alpha, preserving the Dirac products and giving the microscopic
energy. Dirac products alone do not fix the Coulomb coefficient.

A global reinterpretation g_printed^2=g_micro^2/2 would repair the dual
coefficient but turn the printed S0 into 8pi^2/g_micro^2. It therefore fails
to repair the simultaneous dictionary. Rescaling phi changes its period and
unit vertex. An extra compact-cell multiplicity changes neither local energy
nor this invariant. The already documented cosine/fugacity factor two is a
separate issue and cannot repair the kinetic term.

Second primary check: Poppitz-Schaefer-Unsal,
[1205.0290v2](https://arxiv.org/abs/1205.0290v2), 26 September 2012,
PDF page 7, (2.8)-(2.12), was read as pixels. It has dual kinetic coefficient
g^2/[2(4pi)^2 L], unit factors exp(+/-i sigma), and S0=4pi^2/g^2,
exactly the microscopic scalar normalization above. Its fermionic dynamics
are not imported; only the tree photon/core dictionary is compared.

## 3. Project impact and strongest safe statement

`vacuum_matching/REPORT.md` M6-M9 consistently use KB=L/g^2, a unit tail
B=1/r^2, and core action 4pi KB v. In particular M8's charged magnetic wall
term is 2pi KB/R and M9's conditional cloud term is 2pi KB m. Their common
dual stiffness is 1/(16pi^2 KB), not the closed report's source-derived value.
Their stated screened-scalar/charged-exterior conditions remain essential.
The exterior's mass m=m_h screens the holonomy scalar. The closed model's
m^2=u/kappa is instead the dual-photon/plasma mass; these are different
modes. A net charged exterior and an exactly neutral compact ensemble are
different boundary/charge sectors even when their local Maxwell dictionary
agrees. M8 cannot be transferred to a closed vacuum stress by identifying
either the masses or the radii.

`closed_dual_qcd/DERIVATION.md` section 1 accurately translates the printed
(3.25), but cannot also call kappa=g^2/(8pi^2L) matched to the stipulated
microscopic action and the printed S0 at the same g. That source-to-microscopic
claim must be qualified, or the leading tree dictionary corrected to
kappa=g^2/(16pi^2L) and the common fugacity/hard matching re-established.
Holding an abstract potential amplitude u fixed would double m^2=u/kappa;
a physical numerical mass still requires common matching of u and kappa.

The following closed-model statements as functions of independently matched
positive u,kappa (or mR) are unaffected by this normalization mismatch:
exact neutrality/topological integrality,
theta periodicity, the canonical zero-mode Jacobian and its cancellation of
the apparent 1/(2V) response, the scalar spectrum/determinant, and the absence
of a 1/R spatial or temporal response at fixed matched local parameters.
The determinant curvature powers and dimensionless dependence on mR do not
depend on which microscopic coupling dictionary is used. Coefficients after
substitution of a physical g or fugacity do require the corrected bridge.
The possible omitted metric-dependent matching factor is still uncomputed;
this audit neither proves its absence nor determines a cosmological term.
This is an impact assessment; the full curved determinant and ensemble
calculation were not re-audited here.

All normalization obligations above passed except the simultaneous printed
source-to-microscopic identification, which failed. Full determinant/core
matching, curved hard matching, strong-coupling QCD, and electromagnetic
identification are out of scope. No prior lane or executed input was edited.
