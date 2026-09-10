# Rotated-MMG constitutive candidate

This is the next construction attempt after the affine-dust, G03, and
nonlocal routes.  It uses a Hamiltonian constraint to carry the exponential
constitutive law and an independent rotated slip constraint.  The scalar
constraint block is tested by actual Poisson brackets, with homogeneous and
local Fourier sectors separated.

Run the reproducible gates from this directory:

```text
python3 -B rmmg_constitutive_action.py
python3 -B -m unittest -v test_rmmg_constitutive_action.py
python3 -B spherical_prediction.py
python3 -B -m unittest -v test_spherical_prediction.py
python3 -B hda_closure_gate.py
python3 -B -m unittest -v test_hda_closure_gate.py
python3 -B auxiliary_relay_dirac.py
python3 -B -m unittest -v test_auxiliary_relay_dirac.py
python3 -B ward_covariance_gate.py
python3 -B -m unittest -v test_ward_covariance_gate.py
python3 -B laplacian_multiplier_gate.py
python3 -B -m unittest -v test_laplacian_multiplier_gate.py
python3 -B full_adm_dof_count.py
python3 -B -m unittest -v test_full_adm_dof_count.py
python3 -B spatial_diffeo_gate.py
python3 -B -m unittest -v test_spatial_diffeo_gate.py
python3 -B matter_ward_gate.py
python3 -B -m unittest -v test_matter_ward_gate.py
python3 -B covariant_clock_principal_gate.py
python3 -B -m unittest -v test_covariant_clock_principal_gate.py
python3 -B clock_gradient_repair_gate.py
python3 -B -m unittest -v test_clock_gradient_repair_gate.py
python3 -B flrw_clock_background_gate.py
python3 -B -m unittest -v test_flrw_clock_background_gate.py
python3 -B flrw_clock_evolving_gate.py
python3 -B -m unittest -v test_flrw_clock_evolving_gate.py
python3 -B flrw_clock_friedmann_gate.py
python3 -B -m unittest -v test_flrw_clock_friedmann_gate.py
python3 -B flrw_minisuperspace_dirac_gate.py
python3 -B -m unittest -v test_flrw_minisuperspace_dirac_gate.py
python3 -B rmmg_lapse_constraint_variation_gate.py
python3 -B -m unittest -v test_rmmg_lapse_constraint_variation_gate.py
python3 -B action_angle_invariant.py
python3 -B -m unittest -v test_action_angle_invariant.py
python3 -B sparc_exact_exponential_fit.py
python3 -B -m unittest -v test_sparc_exact_exponential_fit.py
python3 -B run_lean_core.py
python3 -B run_lean_formal.py
```

The result is intentionally marked `OPEN`: the local constitutive/slip gate,
the exact exponential identity, and the separately counted clock witness pass;
the nonlinear hypersurface-deformation algebra, ordinary-matter Ward identity,
boosted PPN parameters, full FLRW perturbations, and the \(y\to0\) completion
still have to be derived from this same action.

The spherical script derives the first finite-acceleration correction to the
flat deep-MOND speed, \(v^2=\sqrt{G_bMa_0}+G_bM/(4r)+\cdots\), directly from
the exact exponential law.

The covariant-clock gate tests the natural Stückelberg completion

\[
n_\mu=-\nabla_\mu T/\sqrt{-X},\quad X=g^{\mu\nu}\nabla_\mu T\nabla_\nu T,
\quad a_\mu=n^\nu\nabla_\nu n_\mu,
\]

with an acceleration constitutive term \(G(c^2\sqrt{a^2}/a_0)\).  For
\(T=t+\pi\), its principal symbol is

\[
P(\omega,\mathbf k)=\omega^2[\lambda_\parallel k_x^2
 +\lambda_\perp(k_y^2+k_z^2)],
\]

so the acceleration-only clock has no \(\omega^0 k^2\) term (zero sound
speed) and its ellipticity determinant vanishes at \(y=0\).  This is a
reproducible obstruction to calling the covariant completion healthy without
either an additional clock-gradient operator or a demonstrated second-class
gauge removal.

The companion `clock_gradient_repair_gate.py` tests the minimal explicit
k-essence repair \(K(X)=-A\sqrt{1-X^2/L^2}\).  It makes the combined scalar
symbol positive and subluminal on a finite \((X,y,k,\theta)\) scan, including
the \(y\to0\) limit, but records the resulting clock as one explicitly
propagating scalar.  This keeps the branch scientifically live while making
the required DOF accounting explicit.

The FLRW gate then applies the same clock Euler equation to \(T=t\): for
shift-symmetric \(K(X)\), \(\partial_t(a^3K_X)=0\) becomes
\(3H K_X=0\).  Therefore \(H\ne0\) forces \(K_X=0\), undoing the gradient
repair; a potential would have to track \(H(t)\) explicitly.

The evolving-clock gate tests the live alternative \(\dot T(a)\ne1\), which
solves the conserved-current equation on an expanding de Sitter witness.  The
DBI current has a unique root \(z=\dot T^2/L\in(0,1)\) for every (a>0), with
positive \(K_\chi\), \(\Sigma\), and subluminal sound speed on the tested
range.  This is the current cosmological branch to carry into the full metric
calculation; it is an existence witness, not yet a Friedmann solution.

The minisuperspace Friedmann gate goes one step further: it derives
\(\rho=A(1+z^2)/\sqrt{1-z^2}\), \(p=-A\sqrt{1-z^2}\), and
\(w=-(1-z^2)/(1+z^2)\), verifies the continuity equation exactly, and finds a
positive-\(H\) expanding witness.  The same branch is dust-like at early \(a\)
and vacuum-like at late \(a\), with \(c_s^2=(1-z^2)/(3-z^2)\in(0,1/3)\) on
the scan; metric perturbation/Dirac closure remains open.

`RMMGFormal.lean` now also kernel-checks the exact algebraic identities

\[
\rho+p=2Az^2/s,\qquad
0<\frac{1-z^2}{3-z^2}<1\quad(0<z<1),
\]

and the implication that a shift-symmetric clock on an expanding branch
obeys \(H\ne0\Rightarrow K_X=0\).  These are formal lemmas for the finite
DBI/FLRW branch; they do not formalize the unresolved covariant metric
variation or its full constraint algebra.

The same Lean file now proves the all-(a>0) existence and uniqueness of the
evolving clock speed: for positive (A,L,C,a), there is exactly one
\(z\in(0,1)\) satisfying
\[
\frac{z^3}{1-z^2}=L\left(\frac{C}{Aa^3}\right)^2.
\]
The proof uses the exact positive factorization of the current-map difference
and the intermediate-value theorem, upgrading the finite bisection scan to a
global homogeneous-branch result.

The homogeneous Dirac gate derives (p_N=0), its secondary Hamiltonian
constraint (C=0), a rank-zero first-class bracket pair, and one physical
clock scalar from \((6-2\times2)/2=1\).  The clock velocity Hessian is positive
on the tested branch, so this scalar is explicit rather than hidden.

The action-level `rmmg_lapse_constraint_variation_gate.py` exposes an
additional defect in the displayed rotated constraint action.  Because
\(u=\log N\) is also inside the \(N\)-weighted MOND constraint, the full
higher-derivative lapse Euler operator is not the advertised constraint.  On
\(N=e^{kx}\), \(u=kx\), the advertised divergence vanishes but the derived
lapse residual is

\[
-k^2\bigl[1+(k-1)e^{-k}\bigr],
\]

which is exactly \(-1\) at \(k=1\).  The Lean witness
`affine_lapse_residual_unit_slope_nonzero` checks that nonzero conclusion
without hard-coding the exponential value.  This is a clean obstruction for
the displayed rotated action; repairing it requires changing the constraint
architecture and redoing the Dirac analysis.

The new `action_angle_invariant.py` extracts a parameter-free weak-static
prediction from the exact deep-MOND orbit quadratures:

\[
\frac{T_r\sqrt{G M_b a_0}}{\ell}=\frac{F(e)}{J(e)}.
\]

For two tracers around one source, the ratio
\(T_{r,1}\ell_2/(T_{r,2}\ell_1)\) cancels (M_b\), (a_0), the common
radius scale, and absolute time calibration.  The symbolic cancellation and
four independent quadrature rows are tested by the accompanying unit gate.
This is a conditional weak-static prediction, not evidence of relativistic
closure.

## Normalized-acceleration parent (2026-09-09)

The adjacent `../normalized_acceleration_parent_2026/` directory tests a new
covariant normalization

\[
S_A\propto\int\sqrt{-g}\,s\,H\!\left(\frac{c^2\sqrt{a^2}}{a_0s}\right),
\qquad H=G-Y^2.
\]

In unitary gauge this is exactly `sqrt(h) H(c^2|DN|/a0)`, so its lapse Euler
equation is a pure divergence and the old affine residual disappears.  The
same executable variation finds a nonzero per-direction metric stress
`Y H'(Y)`.  Therefore the entire scalar-norm lapse-neutral class cannot both
carry a nonzero MOND flux and have exact no-slip stress; this scoped no-go is
now the most direct constraint on the next compensator design.
