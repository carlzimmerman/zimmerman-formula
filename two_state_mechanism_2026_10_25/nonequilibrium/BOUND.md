# Removing density, age and rate normalization from a restricted kinetic bound

Let t=sum_b t_b, c=1-a-t, x=1-a-2t, initially (a,t,c,x)=(0,0,1,1).
In the optically thin radiative-only subnetwork,
 dt/dtime=N k_T a x, dc/dtime=-N k_A x c.
Thus dt/dc=-(k_T/k_A) a/c wherever x>0. If k_T/k_A<=r on the
whole temperature trajectory, positivity and a<=1 give
 t<=r log(1/c). Charge/constituent conservation gives c=x+t>=t.
Consequently t<=r log(1/t), or t<=r W(1/r).
For x=0 rates vanish and the inequality continues by continuity. The charged
molecular mass fraction is (201/101)t. Density, alpha³, and elapsed age cancel.
This is a conditional analytic result for this reaction network, not equilibrium.

The code bounds the actual rate interpolant over every temperature interval:
log k_b-log k_A is cubic. Evaluate endpoints and all real derivative roots,
exponentiate its maximum for each b, sum these upper bounds, then take the
largest interval bound. This is conservative for the PCHIP interpolant, unlike
using just a maximum sampled ratio. Double-precision polynomial calculations
are not rigorous interval-arithmetic enclosures; convergence and independent
continuum normalization tests establish numerical reliability separately.

Changing density or running the same isolated network longer cannot evade
this bound. Photo-recycling, incoming radiation, other reactions, density work,
nonthermal distributions, or new collective physics invalidate its hypotheses.
The rate table itself uses BO/spin/truncated-continuum assumptions; the bound
must not be exported to exact Coulomb chemistry or all possible dark media.
