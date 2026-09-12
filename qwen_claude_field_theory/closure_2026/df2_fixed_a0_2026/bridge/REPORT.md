# DF2: fixed-action bridge and conditional static observable

Date: 2026-09-12. Parent supplied base revision: `593612171`; no Git operation
was performed by this audit. Scope: independent source inspection and analytic
derivation, with one new report and no changes to prior artifacts.

**Primary verdict: incomplete, with the smallest missing implication.**
The inspected relativistic clock action has not been shown to reduce to the
exponential AQUAL action with physical acceleration scale
\(a_0=9.3619\times10^{-11}\,\mathrm{m\,s^{-2}}\). A DF2 solution of that
AQUAL equation is consequently a **conditional static diagnostic**, even when
its PDE and numerical convergence are correct. This finding neither excludes
every solution of the clock action nor establishes a same-action DF2 explanation.

## 1. Claim, sources, and missing bridge

The claim being checked is that the unchanged functions \(P,W,V\), unchanged
\(\gamma\), common cosmological data, and observed baryonic source imply the
physical weak-field equation

\[
 \nabla\!\cdot[(1-e^{-|\nabla\Phi|/a_0})\nabla\Phi]=4\pi G_N\rho_b,
 \qquad a_0=\frac c2\sqrt{G_N\rho_\Lambda},
\]

including the appropriate external-field boundary condition. Here \(\Phi\)
is a potential per unit mass in SI units; \(\rho_\Lambda\) is a mass density.
This is not an identity about either scalar's spatial gradient alone.

The actual action in
`clock_response_repair_2026/nonlinear_clock_response_2026/REPORT.md` is

\[
 S=\int\!\sqrt{-g}\,[M^2(R-2\Lambda)/2+P(X,\tau)-V(\tau)
             +sW(Y,\tau)+\gamma X\Box\chi]+S_m,
\]

with \(X=-\nabla\chi\cdot\nabla\chi\),
\(s=\sqrt{-\nabla\tau\cdot\nabla\tau}\), and
\(Y=(g^{\mu\nu}+n^\mu n^\nu)\chi_{,\mu}\chi_{,\nu}\).
The imported `nonlinear_evolution_2026/constitutive.py` defines exactly

\[
 P=-\frac U2\log\frac{U-2dX}{U-2d\bar q^2}
        +3\gamma\bar q\bar H(X-\bar q^2),\qquad V=U,
\]
\[
 W=U+2d\ell(\sqrt{1+Y/\ell}-1)-2\gamma\bar q^2\bar q'.
\]

Its reference history begins with \((a,m,v)=(1,0.1,0.5)\), sets
\(M^2=1,\Lambda=0.7\), and defaults to \(\gamma=10^{-6}\). The referenced
nonlinear-clock report explicitly describes the witnesses as an uncalibrated
dimensionless history and distinguishes physical \(Q\) from reference
\(\bar q\). These functions must not be replaced with an exponential kernel
and then described as a derivation from the unchanged action.

`clock_response_repair_2026/cosmological_bridge_2026/REPORT.md`, lines 72–92,
prints the same functions and explicitly states that no MOND \(a_0\) operator
has been established and the global scale remains an input. Its lines 31–34
also state that the exponential law has not been derived. Conversely,
`exact_exponential_aqual_efe_kepler_2026/REPORT.md`, section 1, **starts by
specifying a nonrelativistic AQUAL action**; it does not derive it from these
clock functions. The symbolic source's lines 14–40 verify that specified
AQUAL action's variation, not the missing relativistic reduction.

The required dependency chain is

\[
 \text{fixed clock action + common physical background + baryons}
 \ \xrightarrow{\text{missing controlled reduction}}
 S_{\mathrm{AQUAL}}[\Phi;G_N,a_0]
 \ \longrightarrow\ \text{static PDE}
 \ \longrightarrow\ \text{field + conditional virial observable}.
\]

| Obligation | Finding |
|---|---|
| Identify the actual unchanged functions | Passed by source inspection |
| Physical baryon stress and metric force are defined | Passed at the stated dust/weak-field levels below |
| Reduce the clock constraints/evolution to the exponential kernel | Not established in the inspected sources |
| Match the measured \(G_N\), physical units, and fixed \(a_0\) | Not established by the dimensionless witness |
| Vary the independently specified AQUAL action | Passed analytically; matching symbolic implementation inspected |
| Derive its external-field linear operator | Passed analytically for nonzero external field and small internal field |
| Turn a field into a global LOS second moment | Conditional on steady collisionless equilibrium and vanishing surface stress |
| Turn that moment into DF2 aperture/GC dispersion | Not determined without tracer/selection/dynamical modeling |

The smallest missing implication is a controlled weak-field reduction of the
**same** coupled metric, scalar and clock equations, on a physically normalized
branch, that produces this flux in the physical dynamical potential for the
specified baryons and environmental data. Recovering a scalar stationary root,
an initial constraint slice, or a finite linear response does not supply that
implication. The sources' restricted affine instability and dust obstruction
must not be extended to all nonaffine or collisionless branches.

## 2. Where physical acceleration, density, and scale enter

Matter couples to the metric. In the linear sourced calculation,
`spherical_baryon_bridge/README.md`, lines 95–109, reconstructs separately
\(\Phi_{\rm dimless}=n+\dot\beta\) and
\(\Psi_{\rm dimless}=-\zeta-H\beta\). Thus the nonrelativistic acceleration
is \(-c^2\nabla_{\rm physical}\Phi_{\rm dimless}\). The shift derivative
cannot simply be omitted. In a static zero-shift spherical metric,

\[
 ds^2=-N^2c^2dt^2+A^2dr^2+R^2d\Omega^2,
 \qquad a_{\hat r}=-\frac{c^2N'}{NA}
\]

for a particle initially at rest, as derived in
`spherical_baryon_bridge/action/MATTER.md`, lines 113–118 (there \(c=1\)).
Neither \(Q\) nor \(\chi'\) is this measured acceleration.

The same matter source file, lines 16–74, uses minimally coupled dust
\(S_d=-\frac12\int\sqrt{-g}\,\rho_b[(\nabla\theta)^2+1]\).
On shell \(\rho_b\) is proper rest density, with
\(T_{\mu\nu}=\rho_bu_\mu u_\nu\) in its \(c=1\) convention. The lapse
source is normal-frame energy \(\epsilon_b=\rho_b U_b^2\), equal to rest
density only at rest. The conserved mass is
\(4\pi\int AR^2\rho_bU_b\,dr\). A prescribed static stellar density is a
collisionless equilibrium assumption, not a stationary solution of this single
pressureless dust flow. `nonlinear_evolution_2026/REPORT.md`, lines 95–128,
already derives that distinction.

If \(\rho_\Lambda=\Lambda c^2/(8\pi G_N)\) denotes the mass equivalent
of a physical cosmological constant, the requested scaling is equivalently

\[
 a_0=c^2\sqrt{\frac{\Lambda}{32\pi}}.
\]

For energy density \(\epsilon_\Lambda\), substitute
\(\rho_\Lambda=\epsilon_\Lambda/c^2\). This dimensional relation identifies
the requested normalization; it does not prove that the coefficient of the
action's galaxy response takes that value. \(\Lambda=0.7\) in a dimensionless
test history cannot be substituted as an SI cosmological constant. Likewise,
the bare Einstein normalization \(M^2=(8\pi G)^{-1}\) in natural units does
not alone establish that \(G\) equals the full theory's measured local \(G_N\).

## 3. Independent conditional action-to-EFE derivation

Assume the specified nonrelativistic action

\[
 S_A=-\int dt\,d^3x\left[\frac{a_0^2}{8\pi G_N}{\cal G}(y)
            +\rho_b\Phi\right],\quad
 y=|\nabla\Phi|/a_0,\quad
 {\cal G}(y)=y^2+2(1+y)e^{-y}-2.
\]

Since \({\cal G}'(y)=2y(1-e^{-y})\), variation with fixed boundary values
gives the requested nonlinear PDE. Writing
\(\Phi=\mathbf g_e\cdot\mathbf x+\phi\), with \(\mathbf g_e=g_e\hat z\)
the external **potential gradient** (physical acceleration has opposite sign),
its full equation remains

\[
 \nabla\cdot\{\mu(|\mathbf g_e+\nabla\phi|/a_0)
                      (\mathbf g_e+\nabla\phi)\}=4\pi G_N\rho_b.
\]

Keep the fixed global \(a_0\) when varying environmental boundary data.
The Jacobian of \(\mu(|\mathbf p|/a_0)\mathbf p\) is

\[
 D_{ij}=\mu\delta_{ij}+y\mu'(y)\hat p_i\hat p_j.
\]

For \(\eta=g_e/a_0>0\), \(\mu_e=1-e^{-\eta}\), and
\(q=1+\eta/(e^\eta-1)\), the external-field-dominated expansion therefore is

\[
 \mu_e(\partial_x^2+\partial_y^2+q\partial_z^2)\phi
           =4\pi G_N\rho_b.
\]

It requires \(|\nabla\phi|/g_e\ll1\); it is not the full nonlinear EFE
equation at arbitrary source strength. Here \(1<q<2\). At \(g_e=0\) this
linearized operator degenerates and cannot be used as an isolated solution.
Its Green function is
\(-G_N/[\mu_e\sqrt{\Delta z^2+q\Delta R^2}]\), obtained by setting
\(z'=z/\sqrt q\) and transforming the source delta function. An algebraic
relation \(\mu(g/a_0)g=g_N\) follows by Gauss integration only in the
isolated spherical situation; it is not a replacement for the EFE PDE.

## 4. Global tensor virial and line of sight

Let \(\nu(r)\) be a prescribed spherical stellar tracer density, normalized
by \(L=\int\nu\,d^3x\). It can be a luminosity or number weight. Suppose
a stationary collisionless distribution realizes that density in the computed
axisymmetric internal potential \(\phi(R,z)\). The first velocity moment of
its collisionless equation is

\[
 \partial_j[\nu\overline{v_i v_j}]=-\nu\partial_i\phi.
\]

Multiply by \(x_k\), integrate, and assume the surface integral
\(\oint x_k\nu\overline{v_i v_j}n_j\,dS\) vanishes. Integration by parts
then gives

\[
 \frac1L\int\nu\overline{v_i v_k}\,d^3x
       =\frac1L\int\nu x_k\partial_i\phi\,d^3x.
\]

Azimuthal symmetry removes cross terms and gives

\[
 s_\perp^2=\frac1L\int\nu\frac R2\phi_R\,d^3x,\qquad
 s_\parallel^2=\frac1L\int\nu z\phi_z\,d^3x.
\]

For a line of sight at angle \(i\) to the external-field axis,

\[
 \boxed{\langle v_{\rm los}^2\rangle_{\rm global}
       =s_\perp^2\sin^2i+s_\parallel^2\cos^2i.}
\]

Velocities here are relative to the systemic velocity in the freely falling
galaxy frame. The uniform external acceleration contributes no tensor virial
for a centered spherical tracer; any tidal variation must be included in the
internal force if relevant. The formula is a necessary equilibrium moment,
not proof that a nonnegative distribution with this density exists.

This is a **total second moment**, including ordered streaming. In projected
notation its global numerator is
\(\int\Sigma[\sigma_{\rm los}^2+\bar v_{\rm los}^2]\,d^2R_{\rm sky}\).
Subtracting a resolved rotation field changes it. The globally averaged
streaming velocity can vanish even while its squared contribution is nonzero.
For a finite aperture or sparse selected globular clusters, the boundary
stress term and selection matter; global tensor virial does not fix an
aperture dispersion without further dynamical and observation modeling.

### Analytic EFD check for a spherical self-gravitating profile

For \(\nu\propto\rho_b=\rho_*(r)\), symmetrize the pair-force virial from
the Green function. The separation distribution of any spherical profile is
isotropic, so its radial integral factors from the angular integral. Relative
to the Newtonian global one-component moment

\[
 \sigma_N^2=\frac{4\pi G_N}{3M_*}\int_0^\infty
                 \rho_*(r)M_*(<r)r\,dr,
\]

put \(k=\sqrt{q-1}>0\). Direct angular integration gives

\[
 \frac{s_\parallel^2}{\sigma_N^2}
   =\frac3{\mu_e}\int_0^1\frac{u^2\,du}{[q-(q-1)u^2]^{3/2}}
   =\frac{3(k-\arctan k)}{\mu_e k^3},
\]
\[
 \frac{s_\perp^2}{\sigma_N^2}
   =\frac{3q}{2\mu_e}\int_0^1\frac{(1-u^2)\,du}{[q-(q-1)u^2]^{3/2}}
   =\frac{3[(1+k^2)\arctan k-k]}{2\mu_e k^3}.
\]

Both tend to \(1/\mu_e\) as \(q\to1\); their orientation-averaged ratio
is \(\arctan k/(\mu_e k)\). At the joint deep-EFD limit \(q\to2\),
the perpendicular and parallel ratios are respectively
\(3(\pi-2)/(4\mu_e)\) and \(3(4-\pi)/(4\mu_e)\). For a Plummer mass
profile of scale \(b\), direct radial integration gives
\(\sigma_N^2=\pi G_NM_*/(32b)\). These are conditional analytic solver
benchmarks. The pair-symmetrization argument here assumes mass follows the
tracer; use the earlier field integral for a different tracer distribution.

## 5. Audit provenance and permitted conclusion

The proof-audit workflow was used to separate the unchecked action bridge
from the two analytic consequences of the explicitly specified AQUAL action.
Checks comprised local source reads, searches for the acceleration-scale and
physical-potential definitions, independent differentiation, integration by
parts, EFD coordinate normalization, and the Newtonian/deep-EFD limits above.
No external theorem, numerical DF2 fit, symbolic rerun, or new computation
manifest is claimed by this report. No `.mathbox/` directory was found
at the repository root in the bounded inspection.

SHA-256 of load-bearing files at inspection:

| File relative to `closure_2026/` | SHA-256 |
|---|---|
| `clock_response_repair_2026/nonlinear_evolution_2026/constitutive.py` | `eab8586467cfefb16d3d6c51c72bab5a0e3e951dc8bd026cf0ade28b359c7f1c` |
| `clock_response_repair_2026/nonlinear_clock_response_2026/REPORT.md` | `767c4fbe45b31944cefc2f36c564aa07fc16604b1b75155ea3f6e4d5e4fd82fe` |
| `clock_response_repair_2026/cosmological_bridge_2026/REPORT.md` | `c27d4f380df6d98dd7fedeb06060cf98728f383aa8757c90bb3aecb853968f6d` |
| `clock_response_repair_2026/spherical_baryon_bridge/action/MATTER.md` | `7c89db6573187322a2d782baa6ecfb3d52104831c0514ff134f058440b0d676b` |
| `exact_exponential_aqual_efe_kepler_2026/symbolic_action_audit.py` | `4a2ca8e56628393cb1ba7e8d654975a9d51abbf2e7596d84eae496095b2d8882` |

The strongest safe result is an environmental, fixed-\(a_0\), conditional
AQUAL prediction of a global moment for a stated tracer and equilibrium
assumption. It can compare boundary conditions without changing \(a_0\).
It cannot yet be credited as the requested unchanged relativistic action's
DF2 prediction. The next bridge check is to carry the physical metric force,
proper baryon source, common clock data and units through the actual coupled
weak-field equations, then identify whether the resulting flux is exponential.
