#!/usr/bin/env python3
"""Bounded exact zeta identities and independent finite heat-sum checks."""
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path
import mpmath as mp

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

def bernoulli(n):
    a = [Q(0)] * (n + 1)
    for m in range(n + 1):
        a[m] = Q(1, m + 1)
        for j in range(m, 0, -1):
            a[j-1] = j * (a[j-1] - a[j])
    return a[0] if n != 1 else -a[0]

def hz_negative(p, q):
    # zeta(-p,q)=-B_(p+1)(q)/(p+1), B1=-1/2.
    n = p + 1
    poly = sum(Q(math.comb(n, k)) * bernoulli(k) * q**(n-k)
               for k in range(n + 1))
    return -poly / n

q = Q(5, 2)
a = Q(1, 4)
b = Q(9, 4)
zT0_poly = hz_negative(3, q) - Q(9, 4)*hz_negative(1, q)
zT0 = zT0_poly + a*a/Q(4) - Q(9, 8)*a
zTm1_poly = (hz_negative(5,q) - (a+Q(9,4))*hz_negative(3,q)
             + Q(9,4)*a*hz_negative(1,q))
zTm1 = zTm1_poly + Q(9,16)*a*a - a**3/Q(12)
zS0 = (hz_negative(3,q)-Q(1,4)*hz_negative(1,q)
        + b*b/Q(4)-b/Q(8))/3
scale_W = -zT0+zS0+2
assert zT0 == Q(19,30)
assert zS0 == -Q(61,90)
assert scale_W == Q(31,45)

# Separate derivation of K_T(t) through t^1 using Euler--Maclaurin.
# Sum_n n(n^2-9/4) exp[-t(n^2-1/4)] has integral and endpoint terms.
# mpmath.diff at t=0 of t^2 is avoided; symbolic heat coefficients use
# Hurwitz expansion of exp(-t n^2) with polynomial multiplicity.
# Integral: e^(a t) [1/(2t^2) - (9/8)/t].
heat_coeff = {}
for j in (0,1):
    integral = Q(1,2)*a**(j+2)/math.factorial(j+2) - Q(9,8)*a**(j+1)/math.factorial(j+1)
    discrete = sum(a**(j-k)/math.factorial(j-k) * Q((-1)**k, math.factorial(k))
                   *(hz_negative(2*k+3,q)-Q(9,4)*hz_negative(2*k+1,q))
                   for k in range(j+1))
    heat_coeff[j] = integral + discrete
assert heat_coeff[0] == zT0
assert heat_coeff[1] == -zTm1

# Independent direct spectral sums, two precisions and exactly declared caps.
# The tail is bounded explicitly by replacing d_l <= (l+3)^3 and
# exp[-t(l+1)(l+2)] <= exp[-t(l+1)^2] and integrating the decreasing
# positive majorant for l>=N. We report bounds rather than infinite sums.
rows=[]
for dps in (60,80):
    mp.mp.dps=dps
    for t_str in ('0.02','0.01','0.005','0.0025'):
        t=mp.mpf(t_str)
        N=300
        K=mp.fsum(mp.mpf(l*(l+3)*(2*l+3))/2*mp.exp(-t*(l+1)*(l+2))
                  for l in range(1,N+1))
        # For x>=N, (x+3)^3 e^-t(x+1)^2 is decreasing; discrete tail
        # sum_(l=N+1)^infty f(l) <= integral_N^infty f(x) dx.
        tail=mp.quad(lambda x:(x+3)**3*mp.exp(-t*(x+1)**2),[N,mp.inf])
        estimator=(K-1/(2*t*t)+1/t-mp.mpf(zT0.numerator)/zT0.denominator)/t
        rows.append({'dps':dps,'t':t_str,'l_min':1,'l_max':N,
                     'zeta_minus_one_estimator':mp.nstr(-estimator,45),
                     'tail_bound':mp.nstr(tail,12)})
        # This is only an asymptotic consistency bound at the declared t.
        expected=mp.mpf(zTm1.numerator)/zTm1.denominator
        assert abs(-estimator-expected)<mp.mpf('0.004')

# Orthogonal flat-current moment: one free unit-charge Dirac field.
# rho(s)=(1/(12pi²))(1+2m²/s)sqrt(1-4m²/s), m=1.
# u=sqrt(1-4/s) maps integral rho(s)/s² ds into finite polynomial.
mp.mp.dps=70
moment=mp.quad(lambda u:u*u*(3-u*u)/(48*mp.pi**2),[0,1])
expected_moment=1/(60*mp.pi**2)
assert abs(moment-expected_moment)<mp.mpf('1e-65')

# Positive low-mode nonlocal countermodel supported only on l=1,2,3.
# F_l=gamma*(Lambda/H)^3 w_l/x_l, w_l=1 for l<=3 else0.
# This finite exact sum is a diagnostic, not a local/unitary QCD model.
low_sum=sum(Q(l*(l+3)*(2*l+3),2)/((l+1)*(l+2)) for l in range(1,4))
result={
 'status':'all declared assertions passed',
 'exact':{'zeta_T_0':str(zT0),'zeta_T_minus1':str(zTm1),
          'zeta_scalar_nonzero_0':str(zS0),'Maxwell_dW_dlog_a':str(scale_W),
          'heat_T_t0':str(heat_coeff[0]),'heat_T_t1':str(heat_coeff[1]),
          'pole_residue_correction_zT0':str(zT0-zT0_poly),
          'pole_residue_correction_zTm1':str(zTm1-zTm1_poly),
          'low_mode_sum_d_over_x_l1_to3':str(low_sum)},
 'heat_rows':rows,
 'Dirac_flat_current_M1_m1':mp.nstr(moment,60),
 'Dirac_flat_current_expected':mp.nstr(expected_moment,60),
 'non_claims':['No QCD LEC values determined','Finite heat checks do not prove a complete expansion',
               'Global countermodel is not a reflection-positive local QCD construction']
}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
