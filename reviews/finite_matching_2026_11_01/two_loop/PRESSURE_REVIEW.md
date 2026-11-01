# Independent audit of finite matched phase pressure

Reviewed the coordinator's frozen pressure.py and ORDER_AND_STATE.md,
their full finite result, and the actual positive-gap follow-up. This is
a thermodynamic/order audit of the stated local native-phase action,
conditional on the separately reviewed finite current coefficient. It is
not an independent derivation of every component-current loop.

**Verdict: the algebra, order bookkeeping and saved finite numerical
pressure statement pass under the stated weak-coupling local-action
restrictions.** No all-order, all-mode-gapped or cold-halo conclusion follows.

## Thermodynamic reconstruction

For Omega(s,omega)=V-Fq-Jq^2/2, q=omega^2, the stationary equation is
Vs-Fs q-Js q^2/2=0. The implemented positive root
q=2Vs/[Fs+sqrt(Fs^2+2JsVs)] is the numerically stable quadratic solution
on the declared Vs>0,Fs>0 branch.

At fixed omega define

    N=Omega_ss=Vss-Fss q-Jss q^2/2,
    C=-Omega_omegaomega=2F+6Jq,
    M=Omega_somega=-2omega(Fs+Jsq),
    D=N+M^2/C.

D is the fixed-charge radial Schur complement. The charge is
n=-Omega_omega=2omega(F+Jq), and its relaxed susceptibility is
chi=C+M^2/N=CD/N. Therefore the implemented infrared sound speed
cs^2=nN/(omega C D) is correct on its admitted response branch.
Positive D and C alone do not guarantee positive sound speed; N changes
sign at the pressure endpoint and controls that instability.

The vacuum-subtracted pressure and energy are

    Pex=Fq+Jq^2/2-V+Vvac,
    Eex=Fq+3Jq^2/2+V-Vvac.

The field-independent classical vacuum may be omitted from both V,Vvac
without changing these quantities. The reported wex=Pex/Eex is the excess
carrier ratio, not the cosmological equation of state including the full
gravitating baseline. The separate finite-difference thermodynamic check
dP/dlnn=cs^2*n*omega is the correct independent identity.

## No double counting and order

The heavy square expands to
-.5(CWa^2/Haa+CWb^2/Hbb)+omega^2 CWb Fb/Hbb
-omega^4 Fb^2/(2Hbb). Consequently V includes vacuum relaxation once,
F includes -CWb Fb/Hbb once, and J=Fb^2/Hbb. These are one matching
term's three pieces, not independent additions. No RG-resummed logarithm
is added to the explicit complete two-loop diagrams.

At fixed scaled field and Q^2/e, V2 scales as e^4, deltaF scales as e,
and J as e^-2. Together with q of order e^3/16pi^2 on this branch, all
three retained heavy/current corrections contribute at the same order.
Ordinary gapped one-loop q^2 graphs contribute at the next retained-order
level in this counting. Solving the truncated action exactly generates
extra terms, but does not determine or bound the missing higher orders.

The direct-current Landau component anomalous dimensions must be combined
with the heavy pullback. CURRENT_PULLBACK_AUDIT.md records the necessary
reduced fixed-X scale identity; the graph alone does not have the reduced
chiral running. The coordinator's independent bounded check supports that
identity. The singlet X has matching component/chiral gamma through the
orders used, as checked against Martin7.5–7.9.

## Numerical coverage and actual massive gaps

The 48 pressure cases are exactly2 interpolation sizes times2 weak
couplings times4 partial/complete schemes times3 separately solved field
stencils. Off-node exact graph/current values and direct e-scaling are
checked. At the finest29-node/.0025-stencil matched cases:

| e | X_endpoint/Xmin | endpoint wex | cs² at X/Xmin=1.3 |
|---:|---:|---:|---:|
| .01 | 1.21394372 | .61414732 | -.56038355 |
| .03 | 1.21818639 | .60916684 | -.49404151 |

All recorded D,C remain positive, sound speed is positive at1.2 and
negative at1.3, and the endpoint remains pressure rich. The largest
last-two-stencil root change is3.3e-11 and the largest21/29-node root
change is3.3e-10. These are diagnostics, not interval certificates.

The original omega²/(2e) is a reference singlet-mass ratio, not the
smallest physical gap. A separate full-spectrum run now checks the
actual smallest positive scalar, Weyl and vector masses at both matched
endpoints and at1.3, for both weak couplings. The largest omega²/gap
ratios among these four points are

    scalar: 1.22e-9, Weyl: 7.64e-10, vector: 2.10e-13.

Thus the admitted angular frequency is far below every positive *tree*
mass in those samples. The calculation explicitly retains14 scalar zeros
(12 Goldstones and the two real flat coordinates),13 Weyl zeros
(12 unbroken gauginos and the Goldstino), and12 massless gauge fields.
They have not been replaced by artificial IR masses or integrated out.
Tree gaps are not loop-corrected pole masses, and a massive-sector
hierarchy does not cure the observed retained-sector negative sound speed.

The remaining scope is the stated local low-momentum finite-order action:
full nonlocal massless response, higher orders, anomalous charge dynamics,
lifetime, cosmological occupation and gravity are not established here.
