# Hard proton continuation from FSP-009

Base: qcd_hard_vacuum/BASELINE.json, FSP-009; the older scalar full-tensor
UV shell and logarithmic quark/gluon cancellation in FSP-007 are inputs,
not new results here. This package changes two missing steps: finite quark
mass matching and acquisition of newer finite-momentum lattice data.
The complete fixed-MSbar physical proton derivative remains the target.

## A finite local quark matching coefficient

Use u=e^2, unit-normalized canonical quark charges, and a sharp O(4)
photon cutoff |Q|<Lambda in Feynman gauge. Other lines are uncut. Fix the
renormalized MSbar quark masses and strong coupling at mu. At leading
strong order the short-distance quark matching can be determined using
an elementary external quark, with no hadron-model substitution.

For one quark of charge Q_f and mass m, the complete one-loop on-shell
Dirac convolution has (FSP-008 proton_kernel/DERIVATION, equations 7-8)

    D_loop^sharp/m = Q_f^2 [3 log(Lambda^2/m^2)+3/2]/(16 pi^2)+o(1).

The independent dimensionally regulated integral is

    D_MSbar/m = Q_f^2/(16 pi^2) integral_0^1 dx
      [-(4-2x) log((1-x)^2 m^2/mu^2)+(2x-2)]
      = Q_f^2 [3 log(mu^2/m^2)+4]/(16 pi^2).

The second term is an evanescent numerator multiplying the UV pole.
The difference is infrared independent and therefore a local matching
coefficient, after eliminating the redundant quark kinetic operator by
the equations of motion. The physical threshold insertion is

    D_p,ct^q = sum_f Q_f^2 sigma_f^p
        [3 log(mu^2/Lambda^2)+5/2]/(16 pi^2) + O(alpha_s),       (1)
    sigma_f^p = m_f partial M_p/partial m_f.

Here the derivative uses independent flavor masses before setting
m_u=m_d. The sigma insertions include all strong sea contractions.
Equation (1) is a finite cutoff-to-MSbar conversion in the quark
parameter direction, not a complete proton electromagnetic mass.
Its logarithm cancels the quark scalar full-tensor OPE logarithm of
FSP-007. It fixes an actual previously unspecified finite coefficient:
the constant is 5/2 times sum Q_f^2 sigma_f/(16 pi^2), at leading strong
order for this sharp photon prescription. No measured alpha is used.

For the leading-power quark scalar hard tail above Q0, the cutoff
cancellation gives

    D_p,hard^q(Q0;mu) = sum_f Q_f^2 sigma_f^p
        [3 log(mu^2/Q0^2)+5/2]/(16 pi^2)
        + O(alpha_s) + higher-dimension/mass-power contributions. (2)

This is a Wilson contribution. In particular mu=Q0 does not set it to
zero. Equation (2) is useful only when Q0 is hard compared with all
retained active masses and QCD scales. No numerical lower cutoff is
claimed to make its omitted terms small without a bound.

For isoQCD with u,d,s,c active, the rational-charge scalar input is

    S_p = sum Q_f^2 sigma_f^p
        = 5 sigma_piN/18 + m_l g_S^(u-d)/6 + sigma_s/9
          + 4 sigma_c/9,                                     (3)

because sigma_u+sigma_d=sigma_piN and sigma_u-sigma_d=m_l g_S^(u-d).
The source scalar charge uses MSbar(2 GeV), matching m_l there.
The finite numerical conversion at mu=Lambda or the formal Wilson tail
at mu=Q0 equals 5 S_p/(32 pi^2). Source inputs are calibrations from
lattice correlator fits and continuum/model averages, not a no-fit
ab initio determination. The 2026 sigma variational study is checked
for changed systematic qualifications, not silently combined with the
2024 continuum result.

The leading gluonic scalar logarithm is already known from FSP-007.
Its finite sharp-photon-to-MSbar conversion at O(u g_s^2), the same-order
quark correction, threshold decoupling, higher operators and nonlocal
low/intermediate momenta remain missing. The trace anomaly determines a
gluon matrix element but does not determine that finite Wilson matching
coefficient. Equation (1) cannot be applied to the gluon coefficient by
replacing sigma_f with a trace-anomaly remainder.

## New source-dependent harder elastic window

The exact 2507.20910v2 paper is newer than the 1812.10311v2 table used in
FSP-008. Its tables XVI-XVIII contain separate finite-a form factors;
its continuum Table XX contains fitted z/Galster functions, not raw
continuum nodal data. The current actually used in equations (5)-(6)
is (2 j_u-j_d)/3. Thus Nf=2+1+1 sea dynamics does not mean that strange
or charm electromagnetic-current insertions are included. Light
disconnected current matrix elements are included in the proton nodes.

Let t=Q^2, z=sqrt(t)/(2m), tau=z^2. At each tabulated node form

    F1=(GE+tau GM)/(1+tau), A=(GE^2+tau GM^2)/(1+tau),
    B=z(3 F1^2-A)/2 + [(1+z^2)A-3 z^2 GM^2](sqrt(1+z^2)-z).

This includes the Born non-pole Dirac term. Define the nodal integrand

    h(t;m)=B(z;GE,GM)/(8 pi^2 m sqrt(t)).

Then D_B/m=int h(t;m)dt for a true continuous form-factor function.
For the finite assertion here, replace h by its piecewise-linear nodal
interpolant, clip the first/last segments to the declared window
0.56 <= t <= 0.88 GeV^2, and integrate exactly segmentwise. This defines
K_tab(m) independently of an unmeasured interpolation error. No claim
is made that the chosen stencil equals the exact continuous QCD band.
The window avoids the soft endpoint and lies inside all three tables.

The main common comparison holds the declared calibration mass
m_ref=0.9389 GeV fixed (the empirical average nucleon mass used in the
primary ETMC scale paper 2104.13408v3, equation 7 and following text).
It is not a matched finite-a mass or QCD prediction. Sensitivities at
m=0.9000,1.0000 GeV will be shown. A separate B64 evaluation uses the
actual same-ensemble mass 0.9440(44) GeV from 2610.20362v1 section III.4;
the latter source's scale 0.07948 fm differs slightly from 2507's 0.07957
fm. It is a disclosed cross-source kernel calibration, not a retuning.

For each node also reconstruct the light connected-current proton
GE_conn=GE_(u-d)/2+GE_(u+d,conn)/6, and likewise GM_conn. Applying the
same functional then taking K_fullLight-K_connected quantifies the
effect of the displayed light disconnected elastic matrix elements on
this quadratic functional. It is not the complete two-current sea
topology: squaring an elastic form factor includes interference and
the non-Born sea covariance is independently missing.

Published node errors have no joint covariance. We will report only
the first-order covariance-agnostic standard-deviation ceiling
sum_i |partial K/partial x_i| sigma_i conditional on fixed momenta/mass.
That ceiling is neither a nonlinear exact error nor a full theory error.
No continuum extrapolation is performed on three stencils. Source
multi-state/AIC fits, renormalization, empirical scale and mass tuning
remain explicit inputs. No numerical alpha or cosmological target enters.

## Pre-execution audit contract

Before execution, preserve source receipts, exact extracted inputs,
ancestry hashes, this derivation, the code and JSON run contract. Checks:
independent full angular tensor contraction versus Born B; clipped
segment versus nodal weights; constant/linear quadrature cases;
analytic versus finite-difference gradients; exact rational quark charge
and sigma flavor decomposition; Dirac asymptotic primitive versus the
finite conversion and UV logarithm cancellation. These checks validate
the finite transformation, not underlying correlator extraction or the
OPE remainder. Bounded run uses no RLIMIT_AS on macOS.
