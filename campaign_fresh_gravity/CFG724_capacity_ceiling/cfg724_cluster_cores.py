"""CFG724 addendum: projected dark surface density in cluster cores vs the cold-energy capacity a0/(pi G).
Inputs from the record (PROVISIONAL where marked): Bullet strong lensing M(<250 kpc) 2.5e14 (main) / 2.0e14 (sub) [Paraficz+16, recalled];
baryons inside 250 kpc from CFG625 static (B3, projected) main 4.85e13 / sub 1.50e13 (canonical). kappa = 1/2 FITTED."""
import numpy as np
G = 4.30091e-3; conv = 3.0857e10
for k, a0 in (("can", 9.3603e-11), ("alt", 1.1312e-10)):
    cap = a0 * conv / (np.pi * G)
    for name, Mlens, Mb in (("Bullet main", 2.5e14, 4.85e13), ("Bullet sub", 2.0e14, 1.50e13)):
        R = 250e3; Sig = (Mlens - Mb) / (np.pi * R**2)
        print(f"{k} {name}: dark Sigma(<250 kpc) = {Sig:.0f} Msun/pc^2 vs capacity {cap:.0f} -> {Sig/cap:.1f}x the ceiling")
