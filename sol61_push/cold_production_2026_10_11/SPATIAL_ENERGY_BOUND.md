# Positive kinetic-energy budget in the spatial envelope

2026-10-11. This checks coldness within the spatial approximation used in
SPATIAL_CONVERSION and QUANTUM_HANDOFF, independently of its daughter yield.
It is not an additional theorem about the full quantum field theory.

Let R=M/m>2, d_0=(R-2)/epsilon, and
Q=<|A|^2+|B|^2>. The spatial Hamiltonian is

\[
 E_r=\langle2A^*L_AA+B^*L_BB+2\operatorname{Re}(B^*A^2)+k|A|^4\rangle.
\]

Separate positive free kinetic dispersions from the rotating frequencies:
L_A=T_A-d_0/2 and L_B=T_B, with
T_A=(sqrt(1+u_*^2q^2)-1)/epsilon and
T_B=(sqrt(R^2+u_*^2q^2)-R)/epsilon. Both are nonnegative for every momentum.
Completing a local square gives the exact identity for this envelope:

\[
 D_r:=E_r+d_0Q=
 K_r+d_0\left\langle\left|B+{A^2\over d_0}\right|^2\right\rangle
 +\left(k-{1\over d_0}\right)\langle|A|^4\rangle,
 \quad K_r=\langle2A^*T_AA+B^*T_BB\rangle.
\]

Thus whenever k>=1/d_0, 0<=K_r<=D_r. This holds for arbitrary spatial
fields with finite terms, or for the finite Fourier/collocation Hamiltonian
used by the code. It does not assume a narrow occupied spectrum. In fixed
volume E_r and Q are conserved, so D_r is a fixed upper bound on kinetic
energy during conversion and moving-source production.

The physical energy represented by the envelope is
E_phys=N_s m(RQ+epsilon E_r), and its kinetic part is
K_phys=N_s m epsilon K_r. Therefore

\[
 {K_{\rm phys}\over E_{\rm phys}}
 \le {\epsilon(E_r+d_0Q)\over RQ+\epsilon E_r}.
\]

For a uniform source and infinitesimal daughters, Q=1 and E_r approaches
zero, giving the bound (R-2)/R=1-2m/M, about 5e-7 for u_*=0.001.
Matched states must use their actual E_r and Q; the existing outputs record
both. The minute time-integration energy drift is a numerical uncertainty,
not exact conservation by the integrator.

The free-particle kinetic stress trace obeys P_kin V<=2 K_phys/3, even for
relativistic dispersion. Consequently the kinetic contribution to P/rho
is bounded at approximately 3.34e-7 in this benchmark. This does **not** bound
the total instantaneous stress: local interaction stress is separate. The
full-action classical virial results address that different question.

Here k=0.2000001 and 1/d_0 is approximately 0.100000025, so the positive
quartic remainder has a wide margin. Because d_0 is close to threshold,
evaluate it as 2u_*^2/[epsilon(sqrt(1+u_*^2)+1)] to avoid subtraction.
The chosen leading-nonrelativistic vertices and retained relativistic free
dispersion define the envelope being tested; this identity does not remove
the approximation error between that envelope and the original action.

The useful conclusion is conditional but structural: redistribution among
source and daughter modes need not be simulated perfectly to bound the
kinetic budget in this envelope. The model cannot turn most of its rest
energy into kinetic heat while preserving its Hamiltonian and charge.
This does not establish a cosmic abundance, quantum corrections, halo
relaxation or the repo's acceleration scale. The derivation is a self-audited
square completion and contains no external theorem or numerical proof claim.
