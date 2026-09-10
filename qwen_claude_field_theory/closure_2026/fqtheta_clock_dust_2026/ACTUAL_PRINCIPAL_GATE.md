# Actual exponential principal gate

`fqtheta_adm_scalar_dirac.py` found a generic local scalar in the affine
`F(Q)Theta` sector.  This follow-up removes the generic-jet loophole.  It
starts from the weak-field action used by `fqtheta_gate.py` and differentiates
the spatial mode directly:

\[
L_{\rm stat}^{(2)}=M^2(2\Psi'^2-4\Phi'\Psi')+
2M^2a_0^2G\left(y_0+\frac{\pi'}{a_0}\right),
\qquad G(y)=y^2+2(1+y)e^{-y}-2.
\]

After period averaging, the actual local jet is

\[
U_{\zeta\zeta}=4M^2,\qquad U_{n\zeta}=-4M^2,
\qquad U_{\pi\pi}=2M^2G''(y_0),
\qquad U_{nn}=U_{n\pi}=0.
\]

These coefficients are then inserted into the affine principal ADM action

\[
L_2=-3M^2s^2+2M^2k^2\beta s+U,
\qquad s=\dot\zeta-\frac{F_Q}{2M^2}(\dot\pi-Q_0n),
\]

and all primary/secondary constraints and their Poisson brackets are derived
by SymPy.  On the exact sample \(M^2=F_Q=Q_0=H_0=y_0=k=1\), the six-by-six
bracket matrix has nonzero determinant and the local mode count is one.  The
zero mode is evaluated independently: the spatial secondaries vanish and the
count is zero.  The reduced symplectic coefficient is

\[
\Omega_{\zeta\pi}=\frac{U_{n\zeta}}{Q_0}k^2,
\]

while the characteristic polynomial is

\[
\lambda^2+\frac{Q_0^2G''(y_0)}{2}=0.
\]

Thus the mode has a finite frequency gap independent of `k` for `y0>0`, but
its symplectic form collapses as `k² -> 0`.  The exact exponential law also
gives

\[
G''(y)=2[1+(y-1)e^{-y}],\qquad G''(y)\to0\quad(y\to0^+),
\]

so the longitudinal constitutive stiffness loses ellipticity at the exact
zero-field point.  This is a concrete non-uniform-limit/strong-coupling
obstruction to treating `pi` as a harmless non-propagating auxiliary.  It is
not a no-go for every relativistic MOND action: the omitted full khronon,
vector/tensor, nonlinear background, and PPN sectors still require separate
derivations.

There is also a parameter-independent dichotomy on the affine dust locus. The
derived bracket determinant factors as

\[
\det C=\frac{64F_Q^4M^4k^{16}}9,
\]

independent of \(y_0\) and hence of the constitutive stiffness. Setting
\(F_Q=f=0\) does remove this braiding, but the same action then has
\(K_{QQ}=0\), charge \(C=-Aa^3\), and density \(\rho=B\). On an expanding
branch, charge conservation forces \(A=0\), so there is no nonzero conserved
charge and no \(a^{-3}\) dust term. Thus the nonzero dust mechanism requires
\(f\neq0\), exactly the branch with one local scalar for every generic
\(k\neq0\). This closes the displayed affine dust route as a
two-tensor-plus-auxiliary construction; it does not rule out a different
covariant action.

Run:

```sh
python3 -B qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/fqtheta_actual_principal_gate.py \
  --output qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026/run_001/actual_principal.json
python3 -B -m unittest discover \
  -s qwen_claude_field_theory/closure_2026/fqtheta_clock_dust_2026 \
  -p 'test_*.py' -v
```

The candidate remains **OPEN**, with this route failing the requested
controlled auxiliary/zero-field gate unless a further covariant regulator is
derived without changing the exact `mu(y)` branch.

The follow-up `FQTHETA_REGULATOR_TRILEMMA_REPORT.md` closes the local repair
options for this same mixed principal architecture. Direct reduction gives
`K_red = -U_nz^2 k^2/(2 Q0^2 U_pp)` and
`omega^2 = Q0^2 U_pp U_zz/U_nz^2`: the exact elliptic branch (`U_pp>0`) is a
ghost, a sign flip (`U_pp<0`, `U_zz>0`) is a gradient instability, and
`U_nz=0` collapses the symplectic form. An independent `p_dot^2` regulator
contains `p_ddot` in the varied equation and therefore makes the intended
auxiliary clock dynamical. The Python gate is 12/12 and the Lean sign
certificate exits 0; this is scoped to the displayed architecture, not a
universal no-go.
