# Independent reciprocal-max action audit, with a repaired stress identity

Primary verdict on the **current corrected artifact**: **proved as written**
for the scoped spherical static reciprocal construction, full-vector norm
convexity result, Newton-OFF convexity obstruction, and displayed radial-orbit
price/window. This does not certify a healthy cosmological/covariant theory,
nonlinear wave formation or collective/nonradial stability.

The initial report required a substantive correction to its field-stress
formula. The author repaired that formula, added an exact nonlinear test, and
produced fresh main_c/control_c provenance. This review accepts that repair;
it does not retrospectively treat the initial stress formula as correct.
No peer files were edited or peer computation scripts executed by this reviewer.

## Raw reconstruction of the source law

Use aligned scalar fluxes b,d>=0, p(b)=sqrt(b^2+a b)-b, and
I(b,d)=integral_0^b[p(s)-d]_+ds. Its activation boundary is
b_t=d^2/(a-2d) for 0<d<a/2. Differentiating b_t gives
2d(a-d)/(a-2d)^2>0. On activation, the moving lower boundary contributes
terms that cancel because p(b_t)=d. Thus

    H_b=b+p(b), H_d=k d+b_t,

whereas OFF H_b=b+d,H_d=b+k d. Both gradients match at activation. The
boundary is C1 but not generally C2, which the report states. On activation,
H_b has zero d derivative, so reciprocity requires H_d independent of b.
Keeping an unchanged Newtonian b+d dark force is therefore inconsistent.
This is a force-integrability statement, not a no-go against the changed force.

In the displayed independent-flux action, integration by parts gives
H_B=grad phi_b,H_D=grad phi_c, while multiplier variation imposes each
Gauss source. Eliminating a quadratic flux produces the familiar negative
potential-gradient gravity action. The signs of the dual action are correct;
positive H convexity is not a positive physical gravitational Hamiltonian.
Spherical Gauss constraints give b=GM_b(<r)/r^2,d=GM_c(<r)/r^2. The baryon
force is then b+max(d,p), with a genuinely positive material source. No
subtraction of a decreasing enclosed residual is needed in this changed action.
The cold wave would couple to phi_c rather than FL1's u, so no FL1 growth or
assembly pass transfers automatically.

## Stress error found and corrected

The initial formula subtracted delta_ij H from B_j H_Bi+D_j H_Di. For
nonlinear H its divergence does not equal the material force source even
when the constitutive gradients are curl-free. A direct one-dimensional
counterexample uses this action's active b=x,d=.1,a=k=1. At x=1, b'=1,d'=0.
The required source is H_b=sqrt(2), but the claimed stress derivative is
b H_bb=3/(2sqrt(2)), whose difference is -sqrt(2)/4. This obeys all one-
dimensional curl conditions and lies well inside activation.

The corrected trace is the Legendre density

    L*=B dot H_B+D dot H_D-H,
    T_ij=[B_j H_Bi+D_j H_Di-delta_ij L*]/(4piG).

Its derivative satisfies

    4piG partial_j T_ij
    =div B H_Bi+div D H_Di
     +B_j(partial_j H_Bi-partial_i H_Bj)
     +D_j(partial_j H_Di-partial_i H_Dj).

The last terms vanish on potential solutions. This is the precise source-
reaction identity. In one dimension T_11=H/(4piG), so the preceding
counterexample now has exactly the required divergence. The updated report
contains the corrected expression and scopes it to smooth solutions.

The updated script also builds an exact three-dimensional quartic energy
with cross coupling, arbitrary affine fluxes, and explicitly retains the
constitutive curl residuals. Its corrected trace leaves only those curls,
while the old trace is nonzero after removing the same curls. Inspection
confirms this is a meaningful nonlinear identity check, rather than a
quadratic special case that would conceal the error. Fresh main_c and
newtonian_dark_control_c manifests both validate against the repository root.

## Full-vector convexity and its physical price

For H_norm(B,D)=H_k(|B|,|D|), the radial active Hessian is diagonal
(1+p',k+b_t'); inactive it is [[1,1],[1,k]]. Coordinate derivatives are
nonnegative. Norm composition therefore gives joint convexity, including
axes via the stated nonsmooth extension. At nonzero fluxes, transverse
coefficients H_b/b and H_d/d are positive, and the report's full six-vector
Hessian has the correct n t^T mixed block. It does not restrict directions
to aligned perturbations.

For k>1, mu=[1+k-sqrt((k-1)^2+4)]/2 is positive, below both 1 and k. The
inactive minimum radial eigenvalue is mu; active values and transverse
coefficients exceed it. Subtracting mu(b^2+d^2)/2 leaves a convex scalar
function with nonnegative coordinate derivatives, so norm composition
proves global strong convexity, not merely sampled Hessian positivity.
The existence/unique-flux minimizer conclusion is correct conditional on
its explicitly nonempty weakly closed affine flux set and compatible domain.
It does not prove smooth multipliers or dynamic stability.

The baryon norm cusp at B=0,D!=0 is real: H_b(0,d)=d produces a subgradient
ball. A unique flux minimizer alone does not supply a unique baryonic test
potential there. The report makes this price explicit.

The Newton-vector obstruction is also valid under its unrestricted domain.
On the connected OFF set |D|>=a/2, prescribed gradients B+D fix
H=|B+D|^2/2+C. Oppositely shifted pairs (B+V,D-V) and (B-V,D+V) can both be
OFF with the same total sum and midpoint an aligned active point. Convexity
bounds the active value by that fixed OFF value. But for fixed d<a/2,
integrating the required baryon maximum adds I(b,d), which grows linearly
with slope a/2-d>0 as b becomes unbounded. No finite pure-cold boundary
F(d) can satisfy the bound globally. The theorem genuinely excludes all
finite globally convex completions with those OFF vector gradients, rather
than merely the naive angular extension. Restricted domains or changed OFF
behavior escape it and are correctly excluded from the verdict.

## Cold orbit theorem and chosen support

For compact source fluxes proportional to r^-2, differentiating
 g_d=k d+b_t(d) gives

    r omega_r^2=3g_d-2d dg_d/dd
      =k d-d^2(a+2d)/(a-2d)^2.

This independently reproduces the unstable d=.3,a=b=r=1 examples and the
d=.1 stable control. For general nonnegative pure-cold force F'(d), universal
active stability would require g_d/d^(3/2) nonincreasing. Since g_d>=b_t
diverges as d approaches a/2 from below, no finite interior initial value
can satisfy that monotonicity on the unrestricted interval. The ability to
choose b above b_t is essential; imposing a mass-ratio domain can avoid it.

For eta=d/b fixed, activation implies t=d/a<1/(eta+2). The stability threshold
function t(1+2t)/(1-2t)^2 is increasing, and its limiting value is
(eta+4)/eta^2. Thus all open active compact-source radii are stable when
k eta^2-eta-4>=0, giving exactly
eta>=[1+sqrt(1+16k)]/(2k). This is a restricted stable-ratio theorem, not
a universal point-source stability claim.

The fixed-profile tracer and moving ordered-shell derivatives are properly
distinguished. A fixed cold profile contributes its density derivative;
a moving cold shell with conserved enclosed mass has d'=-2d/r and lacks
that term. Inactive shell calculations use the stipulated background baryon
profile, which may contribute b'=4piG rho_b-2b/r. A simultaneous arbitrary
two-fluid collective perturbation is not established by these one-shell signs.
The matching finite positive Plummer ratio eta=5.36 lies in the stable active
window for k=1,2 and supplies chosen circular angular momenta. This proves
existence of this radial support prescription, not its formation, quantum
spectral state, nonradial stability or merger fate. The report retains those
limits and the absence of dilute baryonic cold-tracer capture.

## Reviewed evidence and remaining implication

Current reviewed SHA256:

    REPORT.md: d34814c30b32ea587d662b76927874dba6828028d5b72620ff594146ea7325ea
    checks.py: 3bc9871e8adfebc48946b077bf223dc1b316e2e63460a326775068db883c18fc

No hash of the pre-repair report was captured before the peer edit; the failed
formula and exact counterexample are retained above. The final script's fresh
main_c/control_c records were checked with validate_manifest --root, without
executing its scientific script. The symbolic primitive/orbit/window identities
were independently reconstructed in inline SymPy calculations.

The corrected static reciprocal construction and scoped price theorems are
accepted. This closes the displayed reaction-stress gap, not the original
cold identity goal. The smallest remaining implication is physically justified
assembly under the changed cold potential, paying its OFF-vector/capture and
radial-support prices while retaining the same action's cosmological stress
and perturbations. None of these obligations is supplied by norm convexity
or the finite test count.
