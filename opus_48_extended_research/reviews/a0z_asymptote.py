import numpy as np
# rho_DE ratio = (1+z)^{3(1+w0+wa)} * exp(-3 wa (1-a)), a=1/(1+z)
# As z->inf: a->0, exp term -> exp(-3 wa). With wa=-0.86 => exp(2.58)=13.2 (const).
# power law (1+z)^{3(1+w0+wa)}: 1+w0+wa = 1-0.752-0.86 = -0.612; x3 = -1.836
# So rho_DE -> 13.2 * (1+z)^-1.836 -> 0. a0 DECLINES toward 0 early. Confirmed.
# But sign of 3(1+w0+wa) matters across DESI cases:
cases = {
 "DR2 DESY5": (-0.752,-0.86),
 "DR2 Union3": (-0.667,-1.09),
 "DR2 Pantheon+": (-0.838,-0.62),
}
print("High-z asymptotic index n where rho_DE ~ (1+z)^n :")
for nm,(w0,wa) in cases.items():
    n=3*(1+w0+wa)
    print(f"  {nm:14s}: 3(1+w0+wa) = {n:+.3f}  => rho_DE {'DECLINES' if n<0 else 'GROWS'} as (1+z)^{n:.2f}; a0 ~ (1+z)^{n/2:.2f}")
print("\nAll DESI CPL fits give n<0 => a0 SHRINKS at high z (toward 0). Recombination/BBN a0 ~ 0.")
print("Compare matter/radiation: rho_m~(1+z)^3, rho_r~(1+z)^4 grow MUCH faster.")
print("=> the RATIO a0(z)/g_typical collapses even harder early. No early MI scale.")
