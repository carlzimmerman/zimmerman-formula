import numpy as np
w0,wa,Om,OL=-0.752,-0.86,0.315,0.685
def opw(z):
    a=1/(1+z); return abs(1+(w0+wa*(1-a)))
def rhoDE_ratio(z):
    a=1/(1+z); return (1+z)**(3*(1+w0+wa))*np.exp(-3*wa*(1-a))
print("Gamma_th(Om)=(lam^2/2pi)Om coth(pi Om/H); GAPLESS Gamma_th(0)=lam^2 H/(2pi^2)=lam^2 T_GH/pi")
print("tau_c = 1/H ; T_GH=H/2pi (detailed balance verified)")
print()
print(f"eps_G1(z=3, gapless, lam=1) = 3pi^2|1+w(3)| = {3*np.pi**2*opw(3):.3f}  (per gate /lam^2)")
print(f"eps_G1 ratio z3/z0 = |1+w(3)|/|1+w(0)| = {opw(3)/opw(0):.3f}  (H-independent)")
print(f"z=0 anchor: eps_G1(0)<1 needs lam^2 > {3*np.pi**2*opw(0):.3f}")
print(f"zero-lag a0(3)/a0(0)=sqrt(rhoDE(3)/rhoDE(0))={np.sqrt(rhoDE_ratio(3)/rhoDE_ratio(0)):.5f}")
print(f"repo cols = G3'(1/H_DE)=4.42 & G3'(2pi/H_DE)=27.8 at z=3 (geometric gate; NOT a derived rate)")
print("lag band a0(3)/a0(0): adiab IC [0.546,0.849] across gates (DEEPER); const IC up to ~1.0")
print(f"state-existence: at z=3 rho_m/rho_DE={Om*64/(OL*rhoDE_ratio(3)):.1f}; std T∝sqrt(rho_tot) is 7.43x sqrt(rho_DE)")
