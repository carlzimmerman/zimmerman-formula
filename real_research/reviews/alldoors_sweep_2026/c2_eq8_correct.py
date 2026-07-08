#!/usr/bin/env python3
"""
Get the eq(8) MOND-mass relation RIGHT and re-derive the a0 scaling, validating vs BM table.

Definitions (from paper, verified):
  M_N,dyn : Newtonian hydrostatic TOTAL dynamical mass (the big 'missing-mass' number, eq 4/5).
  M_M,dyn : MOND dynamical (baryonic-equivalent) mass -- the mass MOND needs to explain dynamics.
  eq(6): mu(g/a0) g = g_N, mu=x/sqrt(1+x^2).
  Here g = G M_N/r^2 (total physical accel from hydrostatic mass), g_N = G M_M/r^2 (accel the
  MOND baryonic mass would give Newtonianly). So:
     G M_M/r^2 = mu(g/a0) * g = mu(G M_N/(a0 r^2)) * G M_N/r^2
     => M_M = mu(G M_N/(a0 r^2)) * M_N,          mu(x)=x/sqrt(1+x^2).
  Let X = G M_N/(a0 r^2) = g/a0. Then M_M = X/sqrt(1+X^2) * M_N.
  Deep MOND (X<<1): M_M -> X * M_N = G M_N^2/(a0 r^2).  [door's shortcut]

  eq(8) rearranged: M_N = M_M / sqrt(1 - (a0 r^2/(G M_M))^2)? Let's just USE M_M = mu(X) M_N and
  validate against BM's tabulated M_MOND. That is unambiguous and is the framework's own mu.

Scaling with a0: M_M(a0) = mu(g/a0) M_N, g fixed (from M_N, observed). LOWER a0 -> larger X=g/a0
-> mu larger -> M_M LARGER. So required MOND baryonic mass RISES as a0 falls. Deep limit: M_M ~ 1/a0.
"""
import numpy as np
G=6.674e-11; Msun=1.989e30; kpc=3.086e19
rout=np.array([2241,1728,1417,783,1334,1062,1791,2236,1644,387,1322,780,1672,2029,632,934,
1915,1830,1264,1558,1223,1076,1402,1502,790,1234,948,1485,216,1175,1830,1600,1725,1954,487,
1889,2021,1926,1897,1773,840,977,2200,1373,1257,1302,1343,2537,2360,2509,1300,2216,1773,1684,
1730,2589],float)
MN=np.array([9.02,6.88,3.13,0.48,1.39,1.42,9.51,11.96,5.5,0.373,2.51,1.54,6.91,11.45,0.548,
2.12,12.82,4.01,4.97,5.28,5.77,3.67,10.05,4.06,1.69,3.19,0.78,7.15,0.088,2.35,5.39,8.16,7.38,
11.57,0.3,3.85,7.03,5.14,8.76,9.03,0.92,1.79,12.77,2.4,2.96,8.01,3.03,15.93,5.62,28.51,3.81,
10.46,8.36,10.51,9.82,10.69],float)
MMOND_BM=np.array([1.83,1.76,0.55,0.04,0.13,0.2,3.07,3.18,1.26,0.102,0.41,0.43,1.89,3.49,0.086,
0.57,4.79,0.55,1.67,1.29,2.34,1.26,5.1,0.82,0.5,0.75,0.08,2.5,0.019,0.45,0.98,2.81,2.03,3.81,
0.043,0.48,1.37,0.81,2.37,2.84,0.14,0.38,3.71,0.35,0.62,3.83,0.58,4.36,0.65,13.19,0.96,2.49,
2.45,4.13,3.47,1.93],float)
a0m=1.2e-10; a0c=9.36e-11; a0a=1.13e-10
r_m=rout*kpc; MN_kg=MN*1e14*Msun
g = G*MN_kg/r_m**2
def mu(x): return x/np.sqrt(1+x**2)
def MM(a0): return mu(g/a0)*MN_kg/(1e14*Msun)

print("=== VALIDATE M_M = mu(g/a0) M_N vs BM tabulated M_MOND (Milgrom a0) ===")
rat = MM(a0m)/MMOND_BM
print(f"  g/a0: min {(g/a0m).min():.3f} median {np.median(g/a0m):.3f} max {(g/a0m).max():.3f}")
print(f"  median MM_pred/MM_BM = {np.median(rat):.3f}   16-84: {np.percentile(rat,16):.3f}..{np.percentile(rat,84):.3f}")
print()

# closure, baryon = 0.88 * MM(Milgrom), fixed
Mbar = 0.88*MM(a0m)
print("=== CLOSURE via correct full mu, both footings ===")
for lab,a0 in [("Milgrom",a0m),("canonical 9.36e-11",a0c),("alt 1.13e-10",a0a)]:
    f=Mbar/MM(a0)
    print(f"  {lab:20s}: mean closure {np.mean(f)*100:5.1f}%  deficit {100-np.mean(f)*100:4.1f}%  scatter std {np.std(f)*100:.1f}%")
print()

factor=np.mean(MM(a0c)/MM(a0m))
print(f"=== rescale factor MM(canon)/MM(Milgrom) mean = {factor:.3f} (deep shortcut = {a0m/a0c:.3f}) ===")
print()
print("=== envelope: 88 is a LOWER BOUND (conservative M/L). true Milgrom closure -> framework ===")
for base in [88,95,100,110]:
    print(f"  Milgrom {base}%  -> framework canonical {base/factor:.1f}%")
print()
# stellar M/L headroom (gas=52% IMF-fixed, stars=36% at Milgrom)
gas_new=0.52/factor; star_new=0.36/factor
boost=(1.0-gas_new)/star_new
print(f"=== M/L headroom to reach 100% at canonical a0: gas {gas_new*100:.1f}%, stars {star_new*100:.1f}%, boost x{boost:.2f} ===")
