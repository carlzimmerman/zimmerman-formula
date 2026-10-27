# Static source response of the same full GP–degenerate-baryon state

Continuation of the frozen equilibrium packet. Only this new
`equilibrium/static_response/` directory is written. No original equilibrium
note, numerical input, old run, action, manuscript or global navigation is
modified. Existing background: `run_002/profiles.json`, SHA-256
`9af24bea714233fd6428495d6b77c65d01efec510c4961e39825f1598ad2c74c`, and
`run_002/results.json`, SHA-256
`60c5810456f95f50ca0c21fbf485a82750b7db32c449e56bea617f7fa3077df3`.
Select `tau=0.05;L=14.0;tol=2e-07`. Both files are pinned before and after the
new run, and the code checks these expected hashes itself.

**Result.** The existing coupled GP plus gamma=5/3 baryon stationary candidate
has a nonzero, source-specific static l=1 response at finite wavelength after
removing the total COM. The affine source has exactly zero response and frame
multiplier -1. The finite-k response approaches k^4 times the cubic-source
susceptibility divided by 100. This is an actual calculation for the same EOS
and profile as the equilibrium lane; it is not a complete mode spectrum,
certification of this numerical background as the global minimum, a selected
population, a saturation calculation, or a universal normalization.

## 1. Linearization and physical source

Use the background f0(r),U0(r),rho_b(r), scalar multiplier mu_d and baryon
multiplier mu_b already computed, in units 4piG=1,K=1/2,K_b=2/5. The actual
linearized baryon compressibility is

\[
 \kappa_b={d\rho_b\over d(\mu_b-U_0)}
   ={3\rho_b^{1/3}\over5K_b}.
 \tag{1}
\]

Take external potential \(U_{\rm ext}=-E\phi(r)\cos\theta\). Its l=1
finite-wavelength profile is \(\phi_k=3j_1(kr)/k\); this is the l=1 part
of sin(kz)/k. Other spherical harmonics are not included in this calculation.
The l=3 part also begins at order k² and can contribute at order k^4 to the
full plane-probe susceptibility, so the table is strictly the l=1 component.
The cubic profile phi=r^3 is a finite-box derivative control, not a claim of
global nonlinear binding in an unbounded cubic external potential.

Write the scalar amplitude perturbation as s(r)cos(theta), potential
perturbation as v(r)cos(theta), and add the COM constraint multiplier lambda.
For E=1 define F=phi+lambda*r. Differentiating the original stationary GP,
the *declared* baryon EOS and the one-copy Poisson equation gives

\[
 \begin{split}
 L_1s+f_0v&=f_0F,\quad
 L_1=-\tau\Delta_1+6Kf_0^2+U_0-\mu_d,\\
 b\equiv\delta\rho_b&=\kappa_b(F-v),\qquad
 d\equiv\delta\rho_{\rm total}=2f_0s+b,\\
 \Delta_1v&=4\pi Gd,\quad
 \Delta_1u=u''+2u'/r-2u/r^2.
 \end{split}
 \tag{2}
\]

Each species' total mass perturbation vanishes by the l=1 angular integral.
The additional COM requirement is the total mass dipole

\[
 D_{\rm COM}={4\pi\over3}\int_0^Lr^3d(r)dr=0.
 \tag{3}
\]

Regularity is s'−s/r=0 and v'−v/r=0 at the center. The outer finite-box
conditions are s(L)=v(L)=v'(L)=0. The extra condition is made possible by
lambda. For the vacuum exterior, v is proportional to r^-2; requiring its
coefficient to vanish removes the induced total COM dipole. Indeed (2) implies

\[
 {4\pi\over3}\int_0^L r^3 d(r)\,dr
 ={4\pi\over3(4\pi G)}[L^3v'(L)-L^2v(L)].
 \tag{4}
\]

The volume moment and the boundary expression are evaluated separately. They
agree within the numerical errors stated below; zero volume dipole is not
silently inferred from the imposed boundary alone.

The measured generalized source is

\[
 D_\phi=\int\phi(r)\cos\theta\,\rho(x)d^3x,\qquad
 \chi_\phi={dD_\phi\over dE}\bigg|_0
   ={4\pi\over3}\int_0^Lr^2\phi(r)d(r)dr.
 \tag{5}
\]

Both fluids contribute to d, with no replicated baryon host. Gravity has been
linearized once, not supplemented by a separately added spring. With phi=r,
s=v=b=0 and lambda=-1 solve (2) exactly. This is the required affine
cancellation, independent of the density profile.

## 2. Surface-resolved numerical formulation

Set s=r*a and v=r*c. The equations for a,c have radial derivative terms
4a'/r and 4c'/r, with a'(0)=c'(0)=0. A first attempt in direct r coordinates
failed at the fine cubic solve because the mesh cap was reached. This failed
record is retained as `static_response/run_001/manifest.json`; it is not
positive response evidence and has no completed result files. The
susceptibility coefficient kappa_b vanishes as sqrt(R_b-r), so its derivative
is singular at the free surface. This is a coefficient-resolution issue, not
an observed physical instability.

One targeted remedy splits the BVP into interior and exterior pieces sharing
a parameter t in [0,1]:

\[
 r_{\rm in}=R_b t(2-t),\qquad
 r_{\rm out}=R_b+(L-R_b)t^2.
 \tag{6}
\]

The square-root surface behavior is linear in the distance from the endpoint
in these coordinates. The eight field variables are a,a',c,c' on both pieces;
their four values and physical radial derivatives match at the interface.
Two center conditions, three outer conditions and four interface conditions
give nine boundary conditions for these eight variables and lambda.

The only singular center term is treated analytically by solve_bvp's S
matrix: r'_in/r_in=1/t−1/(2−t), so S has -4 on the interior a',c' equations.
No physical coefficient or requested tolerance is relaxed. The actual
interpolated EOS surface U0(R_b)=mu_b is root-solved before splitting;
R_b=2.444647172511382, differing by 1.88e-8 from the original profile's
BVP-derived root because this run uses its retained sampled arrays.

Background f0 uses cubic Hermite interpolation with the retained f0 and f0'
arrays. U0 uses cubic splines with U0'(0)=0 and the existing exterior monopole
condition U0'(L)=−U0(L)/L. The baryon susceptibility is reconstructed from
this potential and the original mu_b using exactly (1). No new equilibrium
is fitted or regenerated. Background interpolation and finite-box error are
additional approximations beyond the linear solver tolerance; the current
controls do not rigorously bound their continuum effects.

For finite k, write phi_k/r=1+z_k(r), solve for ell=lambda+1, and use the
series for z_k near kr=0. This analytically removes the affine component and
avoids cancellation in the small-k susceptibility. The susceptibility with
phi and with phi−r are separately integrated and compared. Integration uses
the same smooth surface coordinates, independently of the solver's adaptive
mesh. The run retains quadrature error estimates; these are not certified
interval bounds.

## 3. Independent quadratic-work check

Let V=6Kf0^2+U0−mu_d. The constrained grand-energy Hessian evaluated on this
amplitude/density perturbation is

\[
 Q={4\pi\over3}\int_0^Lr^2\left[
 2\tau\left((s')^2+{2s^2\over r^2}\right)+2Vs^2
       +{b^2\over\kappa_b}+dv\right]dr.
 \tag{7}
\]

Set b²/kappa_b=0 where kappa_b=0, or evaluate as kappa_b(F−v)² to avoid
division by zero. Multiplying the scalar equation in (2) by 2s, the baryon
equation by b, integrating by parts and imposing s(L)=0 gives

\[
 Q={4\pi\over3}\int r^2 d(r)F(r)\,dr
   =\chi_\phi+\lambda D_{\rm COM}.
 \tag{8}
\]

Thus in the COM-constrained continuum problem Q=chi_phi. This check includes
the attractive Poisson term and both matter stiffnesses; agreement is not
merely a mass-boundary residual. The numerical comparisons use the affine-
projected source for better conditioning. The small nonzero integrated COM
residual and the independent quadrature errors limit the exactness of (8).

## 4. Executed finite result

Five source profiles were solved at tolerances 2e-5 and 2e-7, with unchanged
maximum 4,000 nodes, wall45s, CPU30s per process and one requested library
thread. The surface-split run_002 completed and current-input manifest
validation passed. It used at most 546 nodes, far below the cap; stderr is
empty. Existing background hashes match before and after execution.

The fine-tolerance results below are dimensionless source-specific
susceptibilities (5). Raw full-precision values and uncertainties are in
`run_002/results.json`; the displayed digits are not precision claims.

| source | chi_phi, COM projected | lambda | integrated COM moment |
|---|---:|---:|---:|
| r | 0 exactly in the solve | -1 exactly | 0 |
| r^3 | 513.11948 | -3.86955694 | 3.78e-7 |
| q=kR_b=.1 | 1.4348954e-5 | -.999352707 | -6.40e-12 |
| q=.3 | .00115090106 | -.994188053 | -5.71e-11 |
| q=1 | .127086793 | -.937121867 | -6.51e-9 |

The largest fine reported RMS residual is 1.995e-7. The cubic coarse/fine
susceptibility change is 2.77e-10 relative; the q=1 change is 7.75e-11.
The two smaller finite-k sources already satisfy both tolerances on the
initial 301-point coordinate mesh and therefore have identical discretizations
in that comparison; this is *not* an independent refinement check for them.

The largest relative quadratic-work discrepancy is 3.66e-9. The finite-k
direct-vs-affine-projected susceptibility differences are at most 5.3e-7
relative. The q=.1 projected quadrature error estimate is 1.81e-9 absolute,
about 1.3e-4 relative, which is a conservative practical accuracy limit for
that small value here. The cubic COM quadrature estimate is 8.72e-8 absolute;
its integrated COM residual 3.78e-7 is finite and reported, while its boundary
moment is below 7e-23. No exact continuum zero or stringent COM error bound
is inferred solely from those floating quantities.

Provided the regular constrained static inverse exists, the expansion

\[
 \phi_k=r-{k^2r^3\over10}+O(k^4r^5)
\]

and affine cancellation imply

\[
 \chi_{\phi_k}={k^4\over100}\chi_{r^3}+O(k^6).
 \tag{9}
\]

Numerically chi_(r^3)/100=5.1311947982, while chi_k/k^4 is 5.12489535,
5.07478587,4.53905214 at q=.1,.3,1. The ratios to the leading prediction
are .9987723,.9890067,.8845995. These finite controls support the predicted
small-k behavior; they are not a certified expansion radius or a mode-gap
theorem.

The actual dimensional conversion is also state-dependent. If a is the
length unit and h_c the specific-potential unit, Poisson normalization is
4piG rho_unit a²/h_c=1. For the finite-k length-valued source,

\[
 \chi_{D,\rm physical}={a^3\over4\pi G}\chi_{\rm dimensionless},\qquad
 4\pi G\chi_{\rm per\ volume}
 ={a^3\over V_{\rm averaging}}\chi_{\rm dimensionless}.
 \tag{10}
\]

This is a genuine inverse-G normalization for a specified object's static
response, retaining its volume, state and k factors. It is not the target
universal local coefficient. In particular, (9) keeps the long-wavelength
source suppression, and neither object population nor averaging volume has
been selected by the original scalar action.

## 5. Reproduction and status

`contract.json` and `parameters.json` define the exact finite assertion and
four execution inputs. The executed command is the computation-audit runner
with those four repeated `--input` paths, output directory
`static_response/run_002`, declared `results.json` and
`response_profiles.json`, and limits
`--timeout 45 --max-output-bytes 65536 --max-cpu-seconds 30 --max-threads 1`.
The child command is

```bash
python3 sol61_push/shared_state_2026_10_19/equilibrium/static_response/check_static_response.py \
  sol61_push/shared_state_2026_10_19/equilibrium/static_response/run_002
```

Use the full argv in its manifest to reproduce with a *new* output directory.
The manifest records Python3.9.6, NumPy1.26.2, SciPy1.11.4, observed Git/dirty
state, actual runtime and all before/after hashes. No hard memory or affinity
caps were requested. The earlier failed run_001 remains historical evidence
of the direct-coordinate mesh-cap failure, not a successful calculation.

Outcome: **finite numerical stationary-background response verified in the
stated cases, conditional on interpolation, finite box and floating tolerance**.
Analytic affine cancellation, source/COM bookkeeping, the work identity and
the conditional k^4 relation were reconstructed from the full same-EOS
Euler–Lagrange operator. There is no new full-spectrum, occupancy, nonlinear
saturation, universal-normalization, formation or original-action closure claim.
