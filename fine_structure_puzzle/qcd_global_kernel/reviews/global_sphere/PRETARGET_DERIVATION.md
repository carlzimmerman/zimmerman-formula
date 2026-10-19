# Independent source-first derivation

Saved before opening the target derivations, code, inputs, source records, or manifests. Independent isolated reviewer `global_sphere_review`; 2026-10-19. Scope: positive-mass one-loop scalar determinant on a round S4 and the massless weak-coupling gauge-theory logarithm. This is not a derivation of physical full QCD or a preferred electromagnetic coupling.

## Definitions and scalar spectrum

Let `x=t H^2`, `z=M^2/H^2`, `q=z+12 xi`, `V=8 pi^2/(3 H^4)`, and use the stipulated convention `W=-log Z`, `rho=-H d_H W/(4V)`. For one real scalar,

`K_xi(x)=exp(-12 xi x) sum_{l>=0} [(l+1)(l+2)(2l+3)/6] exp[-x l(l+3)]`.

Writing `n=l+3/2`, the degeneracy is `n^3/3-n/12` and `l(l+3)=n^2-9/4`. The otherwise added `n=1/2` term has zero degeneracy. The Hurwitz-zeta / Euler-Maclaurin expansion of the half-integer sum therefore gives

`K_0(x)=1/(6x^2)+1/(3x)+29/90+(37/189)x+(149/1890)x^2+...`.

Multiplication by `exp(-12 xi x)` gives

* `a0=1/6`;
* `a1=1/3-2 xi`;
* `a2=29/90-4 xi+12 xi^2`;
* `a3=37/189-(58/15)xi+24xi^2-48xi^3`.

The heat coefficients here are coefficients of the integrated unit-sphere trace, including the real-scalar normalization only when the determinant's `1/2` is inserted below.

## Decoupling prescription and stress

For fixed renormalized masses and curvature couplings, the stated subtraction defines

`B_xi(x)=K_xi(x)-a0/x^2-a1/x-a2`,

`w(z,xi)=-(1/2) integral_0^infinity dx exp(-zx) B_xi(x)/x`.

This is a convergent definition for `z>0` and `q>0`. It fixes the finite dimension-0, 2, and 4 local subtraction prescription; it is not the unsubtracted determinant. At fixed `M,xi`, `H d_H w=-2z w_z`, so

`rho_one=3H^4 z w_z/(16 pi^2)`,

`w_z=(1/2) integral exp(-zx) B_xi(x) dx`.

The factor `1/2` is essential. A complex charged scalar is two real scalar determinants. The ultraviolet subtraction is global: it is not an expansion used at all proper times in place of the spectrum.

For a useful independent spectral benchmark set `nu=sqrt(9/4-q)` and `P(q)=psi(3/2+nu)+psi(3/2-nu)`. Polynomial division of the resolvent gives

`d_l/[l(l+3)+q]=n/3-(q-2)n/[3(n^2+q-9/4)]`.

Matching the local terms to the preceding integral fixes the finite expression

`2 w_z = (q-2)[P(q)-log z]/6 +2/9-2xi-a2(xi)/z`.

For `q>9/4`, the two digammas are complex conjugates; for `0<q<9/4`, both arguments are positive real. The coalescence at `q=9/4` is regular. The pole at `q=0` is the scalar zero mode, not a numerical branch to discard. This formula's subtractions and `log z` are required: replacing `log z` by `log q` changes the prescription at nonzero xi.

## Charge derivative and uniform massive limit

Let `u=e^2`, `b=2C/F^2`, `z(u)=(M^2+b u)/H^2`, and `xi(u)=-2u k15`. For the two real charged modes,

`d_u W_ch|0=2[(b/H^2)w_z-2k15 w_xi]_(z,0)`,

`d_u rho_ch|0 = 3H^4/(8pi^2) * [(b/H^2)(w_z+z w_zz)-2k15 z w_zxi]_(z,0)`.

It is incorrect to differentiate only the explicit `z` in the prefactor or to vary the renormalized mass or coupling with H without stating an RG prescription.

On a compact xi interval and a positive physical mass neighborhood with a common lower bound on the full eigenvalue `M(u)^2+12xi(u)H^2`, small-x heat remainders and their needed xi derivatives are uniformly `O(x^2)` after subtracting `a3 x`. Split the integral at any fixed positive x: the tail is exponentially suppressed for large z and the small-x integral is bounded by the corresponding gamma integral. This yields, with differentiated remainders,

`w=-a3/(2z)+O(z^-2)`, `w_z=a3/(2z^2)+O(z^-3)`, `w_zz=-a3/z^3+O(z^-4)`, `w_zxi=a3'/(2z^2)+O(z^-3)`.

Thus `rho_one=3a3 H^6/(32pi^2 M^2)+O(H^8/M^4)` and

`d_u rho_ch|0 = -3 b a3(0) H^6/(16pi^2 M^4) -3 k15 a3'(0) H^6/(8pi^2 M^2)+O(H^8)`.

Here `a3(0)=37/189` and `a3'(0)=-58/15`. The bound concerns fixed positive masses as H tends to zero; it is not uniform in a massless limit. A finite local EFT `R^3/M^2` operator shifts precisely the leading `H^6/M^2` coefficient. Subtracting only through curvature squared does not eliminate this independent EFT coefficient.

The exact `l=0` eigenvalue is `M^2+12xi H^2`; its unsubtracted contribution is `(1/2)log[(M^2+12xi H^2)/mu^2]`. At xi=0 with M>0 it has zero H derivative. Artificially retaining `(1/2)log z` without its `(1/2)log H^2` partner produces spurious stress. The minimal massless determinant has a divergent Gaussian constant mode and needs a separately defined zero-mode prescription. No positive-mass asymptotic result resolves it.

## Primary gauge-sphere source and normalization

Primary source inspected: F. De Cesare, L. Di Pietro, M. Serone, *Free Energy on the Sphere for Non-Abelian Gauge Theories*, arXiv:2212.11848v1, submitted 2022-12-22, 50 pages. Local pinned PDF: `coordinator/source_archive/2212.11848v1.pdf`; SHA256 `677ed007e8e1e6696c2ce60fd21637cb7818349f841f0b4b488dc8df6b2ad06c`. The v1 cover and the official versioned arXiv abstract were checked. Relevant locators: printed pp. 6-7, (2.1)-(2.11); pp. 15-17, (4.1), (4.11); p.20, (4.30), (4.34), (4.37), (4.39); pp.21-22, (4.40)-(4.46) and footnote 8. The p.20 equations were also visually rendered to exclude a text-extraction sign error.

Set sphere radius `R=1/H`, `dG=dim G`, `B=11 C_A-4 n_f T_f`. Equation (4.1) uses a gauge-group volume convention independent of g and contains `-(dG/2)log(g0^2 R^(4-d))`, free determinants, curvature counterterms, and `-(g0^2/2)G2`. Equation (4.39) states

`G2_fin=dG [ C_A(49+33L)/(144pi^2) - n_f T_f(5+3L)/(36pi^2)]`, `L=gamma+log(4pi R^2)`.

After renormalization `R -> mu R` in this logarithm (footnote 8), its total log coefficient is `dG B/(24pi^2)` multiplying `log(mu R)`. Hence

`W_int= -dG B g^2/(48pi^2) log(mu R) + H-independent terms + O(g^4)`.

This is a weak-coupling result at fixed renormalized `g,mu`. It is not equation (4.45)'s fixed-point specialization, and is not the physical full-QCD answer at arbitrary H.

There is an internal source inconsistency that must remain visible: printed (4.37) has a positive fermion finite term while (4.39) has a negative one. Also (4.30)'s fermion pole is `dG n_f T_f/(6pi^2 epsilon)` while the fermion part of the purported sum (4.34) is `dG n_f T_f/(12pi^2 epsilon)`. The latter sum, (4.39)'s logarithm, the gauge normalization, and the renormalization formula (4.42) are mutually consistent; the individual fermion equations cannot all be accepted simultaneously. No assumption that all v1 equations are error-free is made here.

The log coefficient has an independent RG consistency check using only (4.1), (4.40)-(4.42), (4.46): `beta_g=-B g^3/(48pi^2)+O(g^5)` and the curvature beta function has no `g^2` term. Acting on `-(dG/2)log g^2` gives `+dG B g^2/(48pi^2)`, which is canceled by `mu d_mu W_int`. This checks the summed logarithm without relying on (4.37). It does not independently recompute the two-loop vacuum graph's finite constant.

## Abelian exchange, free anomaly, and H derivative

For one photon coupled to colored Dirac flavors, replace the exchange graph's group trace `dG n_f T_f` by the actual current trace `S=N_c sum_f Q_f^2`; set gauge self-interactions to zero. This is a current-trace replacement, not an `SU(1)` continuation. The consistent summed logarithm yields

`W_QED,int= S u/(12pi^2) log(mu/H) + H-independent terms + O(u^2,u g^2)`,

`H d_H W_QED,int= -S u/(12pi^2)`,

`rho_QED,int= S u H^4/(128pi^4)`, `d_u rho|0=S H^4/(128pi^4)`.

One can obtain the same log from `beta_e=S e^3/(12pi^2)` and the one-photon gauge normalization `-(1/2)log u`, with no order-u curvature beta term. This derivation is conditional on the source's renormalized sphere partition convention and its consistent summed/renormalization equations; the source's conflicting individual fermion terms are not additional corroboration.

For the free fields, (4.40),(4.43) give the usual integrated anomaly

`A=31 dG/45+11 N_Dirac/90`, `W_free=A log(H/mu)+H-independent terms`,

so `rho_free=-A/(4V)` in the stipulated rho convention. For QCD plus a photon, `dG=N_c^2-1+1` and `N_Dirac=N_c N_f` if the active quarks are massless; other charged matter contributes separately. The QCD interaction yields `rho_QCD,int=-dG B g^2 H^4/(512pi^4)`. A finite four-dimensional local `E` or `R^2` counterterm integrates to an H-independent constant on S4 and cannot change this fixed-parameter stress. Free anomaly and gauge normalization must be retained even though their direct charge derivative vanishes at fixed H (the normalization has a singular raw `d_u W` at u=0).

A finite H-independent coupling normalization `W -> W+f(u,g)` changes the raw sphere free energy and charge derivative by `f` and `f_u`, including scheme-dependent finite order-u constants. It leaves `rho` and its charge derivative unchanged at fixed renormalized couplings. Allowing an H-dependent normalization would change the observable definition and is not an ordinary finite dimension-four local counterterm. Running couplings inserted before taking the derivative define another derivative and cannot be silently substituted for the fixed-parameter one.

## Preconditions and non-claims

The scalar result requires a stable positive spectrum and a specified local subtraction, with possible independent higher-curvature EFT terms. The UV result requires weak couplings, effectively massless active flavors relative to H, and source normalization/renormalization conventions. These regimes are separate. Neither result supplies interpolation through confinement, chiral low-energy constants, full QCD stress, a nonlocal topological term, or a stationary/minimizing value of alpha.
