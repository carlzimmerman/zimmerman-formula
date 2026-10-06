# Robust tail freedom in every audited spatial dimension n>=3

This is an analytic extension of REPORT.md, using the independently audited formal n-dimensional QUMOND operator in ../continuum_external_field/general_dimension/REPORT.md. It does not extrapolate a fitted three-dimensional gravitational coupling or supply the relativistic vacuum dictionary.

For n>=3, let p=1/(n-1), r_M=(mu_n/a0)^p, and normalize the point-source force by mu_n. The parent derivation establishes

    Q_n(e)=(a0/r_M)c_n integral f(y)y^p F_n(e/y)dy,
    c_n=n² Omega_(n-2)/[(n-1)² Omega_(n-1)],
    F_n(q)=O(q²) as q->0,

with F_n analytic below its q=1 shell. Its explicit compact angular expansion proves the O(q²) cancellation for every n>=3; this is not inferred from a finite list of dimensions. Hence B_n=sup_{0<q<=1/2}|F_n(q)|/q² is finite for each fixed n.

Use exactly the same dimensionless tail stretch T_L and f_L as REPORT.md. Its positivity, inverse-source inequality, strict decrease and onto moment range are independent of n. With Y>=2E the external-field difference obeys

    sup_(0<e<=E)|Delta Q_n(e)|
      <=(a0/r_M)c_n B_n E² integral_Y^infinity (f_L-f0)y^(p-2)dy
      <=(a0/r_M)c_n B_n E² f0(Y)Y^(p-1)/(1-p).

Since 0<p<=1/2, the last quantity tends to zero with Y, independently of L. Thus the finite-window no-upper-bound theorem holds for each fixed n>=3, with the target moment still C=integral y f(y)dy. There is no assertion of a bound uniform in n.

In n=3, p=1/2, c3=9/8 and F3=-2F_parent, so B3=2B_parent. The coefficient reduces exactly to (9a0/(2rM))B_parent E² f0(Y)/sqrt(Y), matching the three-dimensional report. Q_n has units a0/rM (inverse time squared); e,y,C and the tail map are dimensionless, and no hbar is present. General relativistic curvature/vacuum couplings in d=n+1 dimensions remain additional physics. The theorem rules out this observational selection route; it does not force an alternative value of kappa.
