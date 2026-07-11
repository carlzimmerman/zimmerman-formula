import numpy as np
c=2.99792458e8
# Lambda from Planck: rho_Lambda; use Lambda ~ 1.1e-52 m^-2
Lam=1.1056e-52  # m^-2 (Planck 2018-ish)
Z=np.sqrt(32*np.pi/3)
H_Lam=c*np.sqrt(Lam/3)
a0_can=c*H_Lam/Z
a0_can2=c**2*np.sqrt(Lam/(32*np.pi))
print("Z =",Z)
print("H_Lam =",H_Lam,"s^-1")
print("a0 = c H_Lam/Z =",a0_can)
print("a0 = c^2 sqrt(Lam/32pi) =",a0_can2)
print("ratio to 9.36e-11:",a0_can/9.36e-11)
# alt footing rho_tot/cH0
H0=67.4*1000/3.086e22  # s^-1
a0_alt=c*H0/Z
print("a0_alt = cH0/Z =",a0_alt,"ratio to 1.13e-10:",a0_alt/1.13e-10)
