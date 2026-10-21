# Independent P3 cross-review of P0, P1 and P2

2026-10-20. Reviewer: vector-completion/critical-CFT agent. Base
`b37b50b1c`, criteria-only `1d58a0851`. Read-only analytic reconstruction
of the other authors' displayed actions, followed by this review file.
No script, download, scan, build, Lean edit/run or git operation.

**Verdict: pass within the stated local/action-level scope; no required
correction remains.** None of these packets proves a healthy microscopic
MOND theory, a universal supersymmetry no-go, or selection of the target
amplitude. Their explicit qualifications are necessary to this verdict.

## Exact reviewed artifacts

SHA256 values verified from the saved files:

| Artifact | SHA256 |
| --- | --- |
| LOCAL_SUSY.md | `d1b104c3440decf0473540f974d963ebc4a3c113c340ba2e489b08b5458cbecb` |
| SOURCES_LOCAL_SUSY.md | `91948b04636314961337c2d12dc4f33b9b5d804531e9a58006efb5eac752be72` |
| GOLDSTONE.md | `a29364b134bd4768bdb7a4ffd5114a1f8a6b51c43611423c560d2e31285ec21c` |
| SOURCES_GOLDSTONE.md | `4995d39fe8dd13159e37d9823d3a54c182190a1984de5bdea15def752058ed3e` |
| EXTENDED_SUSY.md | `321aa3c412e19d683f3a946cf7c65ec11c01d0498b0920b6361738b0e6a20314` |
| SOURCES_EXTENDED.md | `ba2e140b70d65f804783f8013d7ba7b8c56e395b3b4d7cd3bf0ba0db07219206` |

The current P3 files `CRITICAL_SYMMETRY.md` and `SOURCES_CRITICAL.md` are
this reviewer's own work and are not independently certified by this
review. Their independent reviews belong to the other authors/root.

## 1. Local N1: the precise allowed deformation

I independently differentiated the displayed Kahler potential before
taking the real slice. It gives `K_A Abar=Z^2/2`. The real constrained
matter multiplet has no independent matter auxiliary to reinsert into
an unconstrained potential. The exact constrained formula gives

    U=f_eta(chi)^2-3w^2
     =epsilon+eta chi^6/(1+chi^2)^6.

The local square-root branch exists because the radicand is nonzero on
the real axis; this is a local holomorphic statement, not an entire
superpotential on the complex plane. With eta>=0,
`0<=chi^6/(1+chi^2)^6<=1/64`, so the required nonzero F_S is retained.
The deformation begins at sixth order in chi. Vacuum energy, vacuum
auxiliary scale, gravitino mass and all vacuum quadratic terms therefore
stay fixed. The reflection allows it; an extra genuine shift would
forbid it but would also have to act consistently on the inherited
gradient coefficients.

The finite ordinary S,T parent was checked separately, using its ordinary
supergravity potential. On `S=0,T=x` real, `W=D_T W=K_T=0`, and the
inverse metric gives

    V=f0^2/z_eta(x)=epsilon+eta r(x).

There is no transverse tadpole. Writing `T=x+iy`, the e^K factor yields
`epsilon Z^2 y^2`; canonical normalization yields `m_y^2=2epsilon`.
For S, the inverse SSbar metric contributes
`4c|S|^2/Lambda^2`. The remaining quadratic |S|^2 pieces from e^K,
`D_S W` and `-3|W|^2` cancel, giving
`m_S^2=4c epsilon/Lambda^2`. The x mass is zero. These masses and the
positive local Kahler metric are unchanged by eta because z_eta-1 starts
at order x^6. They are local bosonic spectrum statements; the packet
properly leaves the full fermionic/gravitational health theorem open.

For the separately inherited static implication, the minimized function
`M^2/s+M^2 s/(9a0^2)+eta/s^3`, s>0, diverges at both ends and has
strictly positive second derivative for eta>=0. Its unique minimum obeys
the envelope derivative `dC3/deta=1/s_eta^3>0`. The transfer is correctly
conditional: these supergravity potentials do not yet supersymmetrize
the entire MOND/fluid action.

I independently opened the exact Dall'Agata--Farakos v2 primary and
checked its real-scalar constraint/reduction and Eqs. (78)--(79).
[Checked primary](https://arxiv.org/html/1512.02158v2).
The finite ordinary parent is the report author's calculation, not a
model attributed to that source.

## 2. Goldstone, flat/AdS brane and Galileon checks

For the internal point generator, the coefficient of `(partial chi)^2`
forces Q'=0; the independent h^2 and h^4 coefficients then force Q=0.
The finite canonical-line isometries reduce to the reflection, which
allows the stated tail. This classification fixes the physical metric,
coefficients and arbitrary matter source and does not classify all
mixed metric/fluid/spacetime transformations. The displayed broken-shift
current divergence has the correct sign and both derivatives E_chi and
U_chi check directly.

For flat DBI I varied the nonlinear broken boost directly:

    delta P=partial_mu(pi b^mu P)
               +[2(1+X)P_X-P] b.partial pi.

The allowed boundary constant yields the stated square-root Ward ODE
and `P=-T sqrt(1+X)+B`. B is not fixed by that Ward identity. The static
energy derivatives are positive on the regular branch, with quadratic
small-gradient and linear large-gradient powers. The induced-metric
matter variation gives the report's `(T gamma^{mu nu}-T_m^{mu nu})`
Euler current. Thus a constant flat brane has no linear matter charge.
The separately inserted source gives
`h=D/sqrt(T^2-D^2)`, valid for D<T, and is explicitly symmetry breaking.

For AdS I expanded the particle action and brane kinetic term at the
specified normalized constant brane. They give `q_pi=-1/ell`,
`q_canonical=-1/(ell sqrt(T))` and
`G_scalar=1/(4pi T ell^2)>0`. The sign is attractive: both source and
test-body charges carry the same negative sign and their product is
positive. The resulting IR is quadratic/Newtonian, not MOND.
The potential derivative forces `A_t=T` at a finite stationary flat
brane. The final report correctly restricts its zero vacuum height to
the displayed additive-constant convention: a flat-probe B0 shifts the
height while preserving the scalar Ward identity, with its gravitational
meaning still requiring the bulk/metric completion.

For the cubic Galileon I independently obtained

    EOM=c2 Delta pi+c3[(Delta pi)^2-(partial_i partial_j pi)^2]/Lambda^3,
    flux=c2 r^(n-1)h+(n-1)c3 r^(n-2)h^2/Lambda^3.

The stated radial powers follow. The full four-dimensional polynomial
with d1 removed from the perturbation background gives h powers
`r^-2`, `r^-1/2`, `r^0` for single linear/quadratic/cubic polynomial
dominance. The static quintic vanishes by the zero time Hessian
eigenvalue. The final report explicitly fixes a stationary asymptotic
background and does not apply this localized polynomial with an untuned
tadpole. It neither makes an all-Galileon instability claim nor treats
scalar-loop nonrenormalization as matter/gravity protection.

I opened and checked the version headers and relevant primary brane
actions/AdS tadpole and spherical Galileon polynomial:
[de Rham--Tolley v2](https://arxiv.org/html/1003.5917v2),
[Nicolis--Rattazzi--Trincherini v2, Eqs. (56)--(58)](https://arxiv.org/html/0811.2197v2).

## 3. Extended N2, FI constant, retained source and higher jet

The displayed auxiliary equations give

    V=[(e+m s)^2+xi_FI^2]/t+m^2 t+2mp.

In the regular tau chart its minimum is `s=-e/m,t=xi_FI/m`,
`V0=2m(xi_FI+p)`. The field-independent p contribution is load-bearing
for any absolute vacuum claim and is retained. I independently checked
the exact APT primary Eq. (17), its minimum Eq. (21), and the paragraph
after Eq. (24) keeping p independent and discussing gravity.
[Checked primary PDF, v1 header](https://arxiv.org/pdf/hep-th/9512006).
This does not itself construct a local N2 supergravity with positive
same-state gravitating energy.

For `tau=i t0+c a`, `a=u+iv`, I obtained the report's potential expansion
and canonical masses `m_can^2=m^2 c^2/t0^2`. The stipulated scalar source
is Yukawa at linear order. Holding u fixed and minimizing over t gives
`t_*=sqrt(t0^2+c^2u^2)` and the displayed analytic square-root
*potential*. The packet correctly retains that these scalars are
dynamical; no replacement of u by a gravitational gradient is derived.
The conventional charged-hyper mass yields a canonical u charge
`1/sqrt(t0)`, whose ratio to inertial mass depends on the matter mass.
It does not furnish universal metric coupling.

I differentiated the exact local prepotential family independently.
It indeed gives `tau=i t0+c a+d a^5`, with unchanged vacuum and
quadratic data. On v=0 the potential has the stated u^6 correction and
the nonzero transverse derivative
`V_v=-m^2 s(u)^2 s'(u)/t0^2`. The nonstationary slice is explicitly not
called a consistent one-field truncation. At d=0 the true local branch
has `v_*=c u^2/(2t0)+O(u^4)`. Its envelope variation has `V_t=0`,
`delta s=d u^5+O(u^7)`, giving the retained correction
`2m^2 c d u^6/t0`. This is an N2-allowed local higher potential jet,
not a globally realized microscopic MOND counterfamily.

The displayed SQED moment-map potential is nonnegative and vanishes at
the quoted Higgs configuration. It gives no positive vacuum there and
its regular metric starts at two derivatives. The report's distinction
between this rigid unbroken-N2 branch, a broken-FI Coulomb state, and a
gravitational higher-derivative action is essential. I reviewed the source
cards' stated theorem domains; I have not independently reconstructed
every Higgs-metric or full-superspace classification theorem. The present
review certifies the displayed action-level counterexample/response
algebra and the report's conservative use of those source domains, not
an enlarged nonrenormalization theorem.

## 4. Remaining obligation and independence

Across these three packets, an exact local symmetry is not identified
with a microscopic UV realization, a rigid vacuum constant is not
automatically a supersymmetric gravitating vacuum, and a protected
potential/central charge is not substituted for the sourced constitutive
law. The surviving task is still a single healthy microscopic action and
state whose exact symmetry fixes the physical vacuum and both actual
force regimes, while forbidding every relevant deformation.

No independent compilation, quantum-state construction, complete
fermionic spectrum, halo theorem, cutoff proof or end-to-end Lean bridge
was performed or inferred by this review. No mathematical correction to
the final pinned P0/P1/P2 artifacts is required within this scope.
