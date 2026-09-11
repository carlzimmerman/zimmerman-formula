# Next finite-k calculation — derived reduction, NOT integrated

Independent review checked the stress sources, Hamiltonian and momentum
constraints, separate matter Ward identities, background matrix and trace
equation against the unrestricted Euler equations in derive.py. This is an
algebraic handoff, not a claimed transfer-function run.

Use a solved homogeneous background, \(a,s_0>0\), \(p_k=k^2/a^2>0\),
\(W\ne0\), and a nonsingular matrix below. Set \(\mathfrak m=M^2\).
The state is \((\sigma,v,r_1,v_r,\theta_1,\delta_b)\), with
\(v=\dot\sigma-q\alpha,\ v_r=\dot r_1-q_r\alpha,\ \delta_b=\delta\rho_b\).
All dots are *full physical-time derivatives*.

\[
\begin{split}
B&=2P_X+4q^2P_{XX},& j&=2qP_X-6\gamma Hq^2,\\
j_r&=4C_rq_r^3,& R&=12C_rq_r^2,\\
F&=2qP_{X\tau}/W,& G&=-2qW_Yp_k/W,\\
\delta K&=Fv+G\sigma,\\
A&=B-12\gamma Hq-2\gamma q^2F,&
C&=-2\gamma q^2G-2\gamma qp_k,\\
Z&=-2P_X+2s_0W_Y+2\gamma(\dot q+3Hq),\\
R_v&=qB-18\gamma Hq^2-2\gamma q^3F,&
R_\sigma&=-2\gamma q^3G-2\gamma q^2p_k,\\
P_v&=2qP_X+4\gamma q\dot q,&
V_p&=s_0W+2\gamma q^2\dot q .
\end{split}
\]

Solve the actual matrix, testing its determinant and conditioning:

\[
\begin{pmatrix}
A&0&0&qC-\dot j\\
0&R&0&-\dot j_r\\
0&0&1&-\dot\rho_b\\
F+3\gamma q^2/\mathfrak m&0&0&
qG-3\dot H+p_k-3V_p/(2\mathfrak m)
\end{pmatrix}
\begin{pmatrix}\dot v\\\dot v_r\\\dot\delta_b\\\alpha\end{pmatrix}
=-\begin{pmatrix}S_\chi\\S_r\\S_b\\S_K\end{pmatrix},
\]
\[
\begin{split}
S_\chi={}&(\dot A+C+3HA+jF+2\gamma qp_k)v
       +(\dot C+3HC+jG-p_kZ)\sigma,\\
S_r={}&(\dot R+3HR)v_r+j_r\delta K+4C_rq_r^2p_k r_1,\\
S_b={}&3H\delta_b+\rho_b\delta K+\rho_bp_k\theta_1,\\
S_K={}&\left[\dot F+G+2HF+\frac{R_v+3P_v}{2\mathfrak m}\right]v\\
 &+\left[\dot G+2HG+\frac{R_\sigma}{2\mathfrak m}\right]\sigma
 +\frac{12C_rq_r^3}{\mathfrak m}v_r+\frac{\delta_b}{2\mathfrak m}.
\end{split}
\]
\[
\dot\sigma=v+q\alpha,\qquad \dot r_1=v_r+q_r\alpha,\qquad
\dot\theta_1=\alpha.
\]

The trace equation used is
\[
\dot{\delta K}-3\dot H\alpha=-p_k\alpha-2H\delta K
 -\frac{\delta\rho_{\rm tot}+3\delta p_{\rm tot}}{2\mathfrak m}.
\]

In scalar spatial gauge \(e=0\), reconstruct
\[
\begin{split}
J&=j\sigma+2\gamma q^2v+j_rr_1+\rho_b\theta_1,\\
\delta\rho_{\rm tot}&=R_vv+R_\sigma\sigma+12C_rq_r^3v_r+\delta_b,\\
z&=\frac{\delta\rho_{\rm tot}-2\mathfrak m H\delta K}{2\mathfrak m p_k},\qquad
b=-\frac{\delta K+3J/(2\mathfrak m)}{k}.
\end{split}
\]

Differentiating the Hamiltonian and using energy conservation and trace
gives \(p_k[2\mathfrak m(\dot z-H\alpha)+J]=0\).
Total momentum conservation, trace and Hamiltonian imply the shear
equation. Check these numerically as residuals, not assumed zeros in
a reconstructed output metric.

## Required derivative extension before implementation

The current total-derivative helper is sufficient for its exported equations,
but has **no rate for PXt**. Do not use it on \(F\) and silently freeze
\(P_{X\tau}\). Compute additional jets of the SAME existing \(P\):

\[
P_{XXX},\quad P_{XX\tau},\quad P_{X\tau\tau},\qquad
\dot P_{X\tau}=s_0P_{X\tau\tau}+2q\dot qP_{XX\tau}.
\]

They require no new coefficient function or third time derivative of the
barred history. The existing evaluator contains the needed base, first and
second \(\tau\) derivatives. Retain \(\dot p_k=-2Hp_k,\dot q_r=-Hq_r\).

Test jets against independent derivatives before integrating. Record both
background and finite-k matrix determinants. The homogeneous \(k=0\) system
is separate. First obtain a short transfer evolution and constraint/metric
residuals; only then extend the domain and add the full radiation hierarchy.
None of this substitutes for the missing exact MOND action.
