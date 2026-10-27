# Conserved photon and matter equations

Units mC=hbar=Q²/(4pi epsilon)=1; c=1/alpha. N is initial heavy/light pair density.
B_A=1/2, B_b=D_b; targets s=(a,t_b), incoming products p=(xc,ax).
x=1-a-2sum(t_b), c=1-a-sum(t_b). Here c as a species fraction is distinct from
light speed. Each molecule carries+Q and each free C carries-Q.

At photon quadrature nodes omega_q with weights w_q define
G_q=omega_q² w_q/pi² and occupation f_q=N y_q/(alpha³ G_q),
where y_q is photon number per initial pair. Let sigmahat=sigma/alpha/aD².
For atom sigmahat is the hydrogenic photoelectric formula; for b it is
(4pi²/3)omega S_b(omega-D_b), zero below threshold.
K_j=(mu_j T/(2pi))^1.5 exp(-B_j/T)/g_j,
mu_A=1 (same leading BO convention), mu_b=100*101/201, g_A=1,g_b=2J+1.
The spontaneous coefficient divided by alpha³ at this quadrature node is
k_jq=sigmahat_jq G_q g_j(2pi/(mu_j T))^1.5 exp[-(omega_q-B_j)/T].
This is the Milne inverse of absorption, with no separate normalization.

For dimensionless elapsed time t/age, the signed reaction event rate is
r_jq=age N alpha³ p_j k_jq(1+f_q)
     -age N s_j sigmahat_jq y_q.
Then da=sum_q r_Aq-sum_bq r_bq; dt_b=sum_q r_bq;
dK=-sum_jq(omega_q-B_j)r_jq;
dy_q=sum_j r_jq-lambda_esc,q y_q;
dQesc=sum_q omega_q lambda_esc,q y_q.
K=1.5T(1+x). The ledger
E=K-.5a-sum_b(.5+D_b)t_b+sum_q omega_q y_q+Qesc
is conserved exactly by the differential equations. Both constituent counts and
net charge are algebraic invariants. Retain K as an independent state to expose
rather than enforce numerical energy conservation.

For a homogeneous sphere radius L with pure absorption coefficient kappa,
straight-line geometry gives beta=<exp(-kappa s)> over uniform emission points
and isotropic directions. A ray-to-boundary path has density
P(s)=3/(4L)*(1-s²/(4L²)), 0<s<2L.
Thus beta=integral_0^2 (3/4)(1-u²/4)exp(-tau u)du, tau=kappa L.
The mean photon residence time to absorption/escape is (1-beta)/(c kappa).
Choose loss hazards reproducing these first-flight moments:
Gamma_abs=c kappa, Gamma_esc=c kappa beta/(1-beta).
Thin limit Gamma_esc=4c/(3L), thick limit=3c/(4L).
Here kappa=alpha N sum_j s_j sigmahat_jq. Re-emission and repeated recycling
are handled by the chemistry and photon populations, not by an assigned escape
probability per reaction. This is a homogeneous memoryless moment closure,
not full angle/position radiative transfer or a diffusion solution.

At closed-box Saha equilibrium p_j/s_j=K_j/N and
N y_q=alpha³G_q/(exp(omega_q/T)-1), each r_jq vanishes individually.
Use this to test the discrete Milne relation including stimulated emission.

Missing collision stoichiometries on the SAME species set:
 A+C <-> X+2C (impact ionization / three-body recombination),
 T_b+C <-> A+X+C (impact breakup / three-body association),
 T_b+C <-> 2A (dissociative recombination / associative ionization),
 T_b+C <-> T_d+C (internal collisional transitions).
Energy defects come from the same binding levels, without fitting them.
Their equilibrium constants are all fixed by K_A and K_b. In particular
(n_Tb n_C)/n_A²=K_A/K_b, so k_AI/k_DR=K_A/K_b when the reverse
volumetric event rate convention is k_AI n_A² (no additional factor1/2).
Absolute rates require scattering amplitudes beyond this one-electron spectrum.
Taking these collisions infinitely fast gives the Saha manifold, a distinct
limit test, not derived finite rates or a rigorous bracket on all trajectories.
