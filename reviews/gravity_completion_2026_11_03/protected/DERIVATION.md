# The protected proposal: what is actually established

The explicit quartic almost-no-scale proposal has a local tuned vacuum in
the stated finite action. It does **not** remove the light neutral decay
channel. The mode orthogonal to the eaten Goldstino is approximately81 eV,
has almost the entire original matter transition current, and gives a
photino partial lifetime about 1.325e20 s. This still exceeds the age test
used in TP04. A large F_total cannot replace F_hidden in that width.

The raw-F-energy dark-energy obstruction remains. The local result is a
conditional tuned Einstein-frame construction, not a selected cosmological
constant or a V3 completion.

## Complex metric and exact potential

Write k=sum |phi_i|^2, Y=H-k/(n M^2), P=H_tau,
Q_H=H_tau_taubar and D_H=|P|^2-H Q_H. The metric, with holomorphic rows and
antiholomorphic columns, is

    g_tau,taubar = n M^2 (|P|^2/Y^2-Q_H/Y),
    g_tau,jbar   = -P phi_j/Y^2,
    g_i,taubar   = -Pbar phibar_i/Y^2,
    g_i,jbar     = delta_ij/Y+phibar_i phi_j/(n M^2 Y^2).

The ordinary inverse matrix has antiholomorphic rows. Thus the potential
contraction is Dbar^T g^-1 D. This orientation matters off the real slice.
Direct inversion gives, for arbitrary complex matter and W_tau=0,

    V=Y^-n {Y F0+(n-3)|W|^2/M^2
               +Y Q_H |S-nW|^2/(n D_H M^2)},
    F0=sum |W_i|^2, S=sum phi_i W_i.

The symbolic one-matter identity is exact with independent conjugate
variables. Rational complex controls with 2,3,4 matter fields also agree
exactly. These supplement, rather than replace, the block-inverse argument:
the matter metric is identity/Y plus a rank-one outer product, so only its
span along phibar couples to the modulus; every orthogonal matter vector
contributes the free Y|W_i|^2 contraction. The remaining two-dimensional
block is the symbolic calculation. For n>0 the positive domain is Y>0 and
D_H>0; H then follows positive. For Q_H=0,n=3,

    V=Y^-2 F0.

W0 cancels its own contribution, not the positive matter auxiliary energy.

## Neutral coordinates, finite action, and stationarity

For h=lambda=e, define canonical singlet matter coordinates

    T=(X+sqrt(30) B_D)/sqrt(31),
    N=(sqrt(30) X-B_D)/sqrt(31), q=-i A_D,
    W=F T+A N-(kappa/2)N q^2+W0,
    F=mu^2/sqrt(31), A=mu^2 sqrt(30/31),
    kappa=e sqrt(31/30), q0=mu sqrt[60/(31e)].

The CP background has T,N,q real. The rigid valley is N=0,q=q0, with
T=sqrt(31)X. This is precisely the SU5 collective model, not the separate
singlet Shih model.

The first solved action is exact neutral tree SUGRA plus the complete
finite-splitting rigid CW function. The small-field canonical rescaling at
fixed Y is e_phys=e Y^(epsilon/2),
mu_phys^4=mu^4 Y^(1-n), X_phys/mu_phys=(X/mu)Y^(-epsilon/4).
This keeps full rigid splittings. It does not add the finite gravity soft
splittings to the one-loop functional determinant.

The finite-normal follow-up uses the same rigid loop order as the canonical
lane. The frozen21/29-node table supplies CW normal sources j_a,j_b and the
unreduced two-loop vacuum diagrams U2diag. In canonical coordinates,

    X=(T+sqrt(30)N)/sqrt(31),
    a=q/sqrt(30), b=(sqrt(30)T-N)/sqrt(930).

The loop action on the real slice is CW(X)+j_a(a-a0)+j_b(b-X)+U2diag.
Tree normal stationarity then generates its relaxation energy once.
U2red is not added. The complex continuation of the j_b term uses the
component of B aligned with X, preserving common X,B R rotation. This is
the linear normal expansion; quadratic normal CW terms and finite loop
kinetic corrections remain omitted, explicitly.

At e=.003, mu=18170662.111498855 GeV, epsilon=1e-4 and b=c=1e8, the preferred
finite result is

| Quantity | Value |
|---|---:|
| X / old rigid X_min |1.02656394539939|
| Re tau |0.4999999999999930553|
| True canonical T |2.508968897e9 GeV|
| CW-displaced N |-3.0071378 GeV|
| (a-a0)/a0 |2.4526858e-8|
| (b-X)/X |6.7835827e-9|
| Phase mass |0.07586885724 GeV|
| Radial mass |0.44320877744 GeV|
| Two modulus scalar masses |168.7261214 GeV|
| Four remaining singlet scalar masses |about 1.4074935e6 GeV|
| Gravitino mass |2.435351790 MeV|
| Leading photino mass |0.9743577944 MeV|

These eight scalar eigenvalues cover the four-chiral commuting singlet
block, including both complex modulus directions. They are not a claim
about the full transverse quantum SU5 Hessian. The independent rigid
nonflat scalar gap is49.21 TeV and the nonflat fermion gap62.07 TeV; those
provide a large classical transverse margin, not the missing loop pole
calculation. Gauge Goldstones are not counted as physical massless scalars.

At the point Y~0.9999999999999861,D_H~1 and the four singlet metric
eigenvalues are approximately 1,1,1,2.9999. The modulus displacement is
consistent with (tau+taubar-1)=-epsilon/(24 n b) at leading order. The
quartic geometric scale M/sqrt(b)=2.435e14 GeV is far above all displayed
masses. This is an EFT scale check, not a UV origin for b,c or epsilon.

The 21/29-node radial masses differ by 3.73e-11 fraction. A separate one-variable
exact-CW leading profile, at 60 and100 digits, gives t=1.02665829661054;
the original full five-variable solve gives1.02665829845497. The tilt is
0.26201844 of the radial fold force. Thus the small minimum is well away
from the fold in this construction. The normal/two-loop correction changes
t by about 9.44e-5; it does not destroy it.

## Fermions and the indispensable Ward correction

The eaten direction is identified using the properly normalized Kähler
metric, not the old rigid Goldstino. In the small-field two-light-direction
limit, canonical basis (sqrt(n)M chi_tau,chi_T), it is proportional to

    eta=(-sqrt(n) chi_tau,canonical+sqrt(epsilon) chi_T)/sqrt(3).

The orthogonal direction is

    zeta=(sqrt(epsilon) chi_tau,canonical+sqrt(n) chi_T)/sqrt(3).

Consequently the original matter current has zeta projection sqrt(n/3),
not F_hidden/F_total. The direct neutral calculation gives

    |<chi_T|zeta>|=.999983333194,
    |<chi_T|eta>|=.005773502754,
    F_hidden=5.930081448e13 GeV^2,
    F_total~1.027120264e16 GeV^2.

The pre-unitary chiral matrix is

    m_ij=e^(K/2M^2) nabla_i D_j W.

Its exact tree scalar Ward identity is checked numerically against
independent derivatives of the potential, with error below 9e-83 in mu
units. Projecting onto the K-normalized kernel of D_iW removes the
gravitino rank-one mixing ambiguity. At a CW-stationary but tree-off-shell
point, however, that projected tree matrix is not a physical loop pole.

At zero matter/M and the tuned relation F^2=epsilon m32^2 M^2, the raw
cross mass is -(n-1)F/(sqrt(n)M). The CW force required for stationarity
supplies the rigid zero-momentum self-energy m_TT=epsilon m32 at leading
gravity order. This follows from differentiating the scalar potential:

    partial_i V=m_ij A^j-2 m32 e^(K/2M^2)D_i W,
    A^j=e^(K/2M^2)g^(j kbar)Dbar_k W.

After the Goldstino subtraction, a convenient representative is

    M_unitary/m32 = [[epsilon^2/(3n), epsilon sqrt(epsilon)/(3sqrt(n))],
                    [epsilon sqrt(epsilon)/(3sqrt(n)), epsilon/3]].

It annihilates eta and has physical eigenvalue

    m_zeta=epsilon/n m32 ~81.1811 eV.

This formula is exact in epsilon within the stated leading small-field,
stationary Ward completion. The original neutral numerical solve gives
81.181116 eV and heavy singlet fermions about 1.40749e6 GeV. Its tree-only
projected light mass is instead about-162.346 eV: taking its absolute value
would miss a loop correction of the same gravity order. At the subsequently
CW-displaced heavy normals, a TT-only correction is again insufficient.
The finite-normal result therefore quotes the leading 81.18110 eV estimate,
and does not promote that incomplete matrix to a matched physical pole.

## Transition current, anomaly terms, and what does not close

The physical leading operator inherited from the actual finite rigid mass
source is

    L_dipole= -sqrt(n/3) m_chi/(sqrt(2)F_hidden)
                    zeta sigma^(mu nu) chi F_mu nu + h.c.

At the finite point its coefficient is about 1.162e-17 GeV^-1. The leading
partial width (the tiny zeta mass has negligible phase-space effect) is

    Gamma_chi->gamma,zeta=(n/3)m_chi^5/(16pi F_hidden^2),
    tau_partial~1.32489e20 s.

The decay survives the heavy-gravitino construction, but still passes the
single-age survival test at this order. This is not a total gravity loss
bound. The modulus, radial and phase scalars are too heavy to be emitted
on shell; the gravitino is also heavier than the photino. Three SU3
gauginos remain kinematically closed. The original transpose involution is
preserved by norm-K, constant W0 and the singlet modulus terms, so its
forbidden transitions are not removed by these specified additions.

The anomaly calculation must retain all three terms in the primary-source
formula. At leading small field,

    K_i F^i/M^2=-n m32,
    (log det K_R)_i F^i/d_R=-m32.

The complete combination then gives

    m_anomaly= -g^2/(16pi^2) epsilon(T_G-T_R)m32.

This algebra is checked for SU5 with its two adjoints and the formal
low-energy SU3,SU2,U1 field contents. It is a local small-field identity;
finite Higgs/chiral threshold matching and the corresponding transition
current remain separate. In particular, m_lambda-m_AdS, not automatically
m_lambda, is the source's eaten-Goldstino coupling. The finite rigid matter
current above is the controlled leading contribution for the uneaten mode.

This dipole projection alone does not determine radial/phase decays into
two uneaten fermions or two gravitinos. Derivatives of the neutral mass
matrix, scalar mixing and the associated 1PI current must be matched for
those cubic vertices. For the phase, terms of order m_zeta/R can compete
with its naive m_phase^2/F_hidden coupling. Any production use of a
projection-only scalar Goldstino width must therefore be labelled an
estimate or a declared uncertainty envelope, not a result established here.

On the leading stable radial profile one can eliminate the parameter
mu sqrt(epsilon) using stationarity:

    m_zeta/m_chi=sqrt(31) psi'(t)/[2 n Z c_chi(t)].

At17 evenly spaced points between t=1 and the first radial fold, this ratio
never exceeds3.919e-4. This is a useful finite discriminator: changing
epsilon and compensating mu along this branch does not obviously yield a
kinematically stable photino. It is not a proof of a profile-wide maximum.
Kinematic closure is not required for the stated age-window result.

## Vacuum meaning and remaining implication

The raw F_hidden^2/rho_DE remains approximately 1.396e74. For this construction
the leading cancellation is epsilon W0^2/M^2~F_hidden^2. V_min has nonzero
derivative with respect to W0, approximately -2epsilon W0/M^2. Matching DE
therefore requires relative W0 precision about 3.58e-75; there is no equation
selecting that residual. The 120-digit preferred packet actually tunes the
specified finite action to 2.52e-47 GeV^4 and reconstructs it from serialized
normalized parameters. This is evidence for numerical cancellation and
local existence, not a prediction of rho_DE.

The preferred packet is run_export_002/result.json. Its round-trip target
error is 6.32e-46 relative. The first export's strict 1e-25 assertion failed
because the full solver stopped at 7.06e-24 relative target error; the
serialized fields themselves reconstructed its result accurately. That
failed source/run is preserved. A final fixed-field W0 Newton refinement
of 2.53e-98 fraction closes the numerical stopping gap without a
material stationarity or spectrum change.

Remaining obligation: a common finite SUGRA 1PI functional whose scalar
stationarity, full neutral/transverse two-point functions, anomaly and
Higgs thresholds, and transition current obey the same Ward identities.
The local scalar construction and leading uneaten current are substantive
checks; they do not close that obligation. A UV selection of the residual
and a V3 multiplet/operator map remain further distinct missing inputs.
