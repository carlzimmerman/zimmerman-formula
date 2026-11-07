# Conservative gradient balance survives; its absolute-value estimate is open

Use the jump-free compact BV class of PF14–15 and the native Riemann source
from pf08/principal_review/RIEMANN_SOURCES.md. Write

    D_sigma=n+sigma c e,
    z_sigma=theta+sigma I(r,A),
    D_sigma z_sigma+omega(D_sigma)=F_sigma,
    W_sigma=e(z_sigma)+omega(e).

Derivative terms now mean Radon measures with canonical diffuse approximate
values. Auxiliary Lipschitz bounds make F_sigma bounded. The conservative
identity has the useful weak form

    div_2(D_sigma W_sigma-e F_sigma)=R_base/2.             (1)

Here e F_sigma is the vector field e multiplied by F_sigma, not a claimed
classical derivative. The identity follows directly: substitute the Riemann
equation in the flux, cancel the two sigma c terms, and obtain

    (n tensor e-e tensor n)Dz_sigma
        +omega(e)n-omega(n)e.

The divergence of the first term is the density-corrected curl of Dz_sigma,
zero by commuting distributional partial derivatives. The second gives the
base curvature by the Cartan identity. This avoids multiplying two singular
derivatives. The independent audit derives this cancellation explicitly.

For smooth solutions one rewrites (1) as a transport equation for W_sigma,
takes its absolute value, bounds e(F_sigma), and obtains the PF09 variation
estimate. These are additional steps. Bounded F_sigma alone does not imply
that div_2(e F_sigma) is a measure with a controlled total variation. Even
if that source estimate were proved, a signed measure transport equation
does not automatically imply its absolute-value inequality.

A precise non-native countertest illustrates the latter distinction. Let
b(x)=delta sqrt(|x|), delta>0, and choose a waiting time a. On t>=0 set

    X(t)=0 for t<=a; X(t)=delta^2(t-a)^2/4 for t>a.

Both X(t) and the constant zero path solve X'=b(X). Thus
mu_t=Dirac_(X(t))-Dirac_0 solves partial_t mu+partial_x(b mu)=0,
with zero initial measure and positive total variation after a. Verification
is just d/dt psi(t,X(t))=psi_t+b(X(t))psi_x for smooth tests on each path;
X is C1 even at a. A zero-source Kato estimate forcing ||mu_t||<=||mu_0||
would fail. This example is neither an AC2q solution nor its gradient measure.
It does not prove native nonuniqueness. It shows why the native coupled
structure must actually be used to justify renormalization, rather than
invoking the signed equation alone.

The remaining theorem must control source variation and acoustic transport
for the actual gradients while retaining auxiliary reconstruction and all
Einstein equations. Neither a square of a Cantor measure in the Riccati
formula nor an assumed unique characteristic flow supplies that theorem.
