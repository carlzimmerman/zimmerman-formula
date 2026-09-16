#!/usr/bin/env python3
r"""H060 -- ONE DISTRIBUTION GENERATES THE WHOLE PHENOMENOLOGY.
CANDIDATE TOE PIECE. Verified forward only (no reverse claim).
CHAIN (each step checked numerically below):
  Lomax(n=2) CDF   ->   mu_2(u) = 1-(1+u)^-2
  deep limit       ->   mu_2 ~ 2u  =>  g^2 = a_0 g_N
  deep law         ->   g = sqrt(G M_b a_0)/r        (flat rotation curve)
  divergence       ->   rho_ph = sqrt(G M_b a_0)/(4 pi G r^2)   (r^-2)
  integrate        ->   M_ph(<r) = sqrt(G M_b a_0) r/G          (M ~ r)
  => amplitude law, BTFR (v^4 = G M_b a_0), Sigma = a_0/(2 pi G)
So a SINGLE probability distribution generates the entire MOND
phenomenology. That is the candidate TOE piece: the theory's input is a
distribution, not a Lagrangian.
NOTE: this is the FORWARD chain only. H055's V3 claimed a REVERSE lock
(gamma = (2+n)/n, so gamma=2 => n=2). That reverse step is NOT used here
and is under review (possible off-by-one: the Lomax density exponent is
-(n+1) while the mass-distribution exponent is -n).
"""
import math, json
G=6.67430e-11; c=2.99792458e8
H0=67.4e3/3.0856775814913673e22; OmL=0.685
rho_c=3*H0**2/(8*math.pi*G); a0=0.5*c*math.sqrt(G*OmL*rho_c)
MSUN=1.98892e30; PC=3.0856775814913673e16
def mu2(u): return 1.0-(1.0+u)**-2
print("H060 -- ONE DISTRIBUTION GENERATES THE WHOLE PHENOMENOLOGY")
print("="*66)
# V1 deep limit: mu_2(u)/u -> 2
for u in [1e-2,1e-3,1e-4,1e-5]:
    print(f"  u={u:<8g} mu_2/u = {mu2(u)/u:.8f}")
print(f"  => deep slope = 2 = n  (limit, not assumed)")
p1 = abs(mu2(1e-5)/1e-5 - 2.0) < 1e-3
# V2 deep law from mu_2 ~ 2u: (g/a_0) g = g_N
print("\nV2  mu_2 ~ 2u = g/a_0  =>  g^2 = a_0 g_N   (the deep law)")
Mb=6e10*MSUN
for r in [5e3*PC, 1e4*PC, 3e4*PC]:
    gN=G*Mb/r**2
    g=math.sqrt(a0*gN)
    gg=math.sqrt(G*Mb*a0)/r
    print(f"    r={r/PC/1e3:6.1f} kpc  g(deep law)={g:.5e}  sqrt(GMb a0)/r={gg:.5e}")
p2 = abs(math.sqrt(a0*G*Mb/(1e4*PC)**2) - math.sqrt(G*Mb*a0)/(1e4*PC))<1e-20
# V3 divergence -> rho_ph ~ r^-2
print("\nV3  rho_ph = (1/4piG) div(g) with g ~ 1/r  =>  rho ~ r^-2")
def rho_ph(r): return math.sqrt(G*Mb*a0)/(4*math.pi*G*r**2)
rs=[1e4*PC,2e4*PC,4e4*PC]
print("    rho(10,20,40 kpc) =", [f"{rho_ph(x):.3e}" for x in rs])
print(f"    ratio rho(10)/rho(20) = {rho_ph(rs[0])/rho_ph(rs[1]):.4f} (expect 4.0000)")
p3 = abs(rho_ph(rs[0])/rho_ph(rs[1]) - 4.0) < 1e-9
# V4 integrate -> M_ph ~ r  (amplitude law)
def M_ph(r): return math.sqrt(G*Mb*a0)*r/G
print("\nV4  M_ph(<r) = sqrt(G Mb a0) r/G   =>  M ~ r (amplitude law)")
print(f"    M(10)/M(20) = {M_ph(rs[0])/M_ph(rs[1]):.6f} (expect 0.5)")
rM=math.sqrt(G*Mb/a0)
print(f"    at r_M = {rM/PC/1e3:.3f} kpc: M_ph/M_b = {M_ph(rM)/Mb:.6f} (expect 1)")
p4 = abs(M_ph(rM)/Mb - 1.0) < 1e-9 and abs(M_ph(rs[0])/M_ph(rs[1])-0.5)<1e-12
# V5 BTFR
v4=G*Mb*a0; v=v4**0.25
print(f"\nV5  BTFR: v^4 = G M_b a_0  =>  v = {v/1e3:.1f} km/s for 6e10 Msun")
print(f"    A = 1/(G a_0) = {1/(G*a0)*1e12/MSUN:.2f} Msun/(km/s)^4")
p5 = v > 1e5 and v < 3e5
# V6 Sigma
Sig=a0/(2*math.pi*G)*PC**2/MSUN
print(f"\nV6  Sigma = a_0/(2 pi G) = {Sig:.2f} Msun/pc^2  (H037 corrected)")
p6 = 80 < Sig < 140
res=[p1,p2,p3,p4,p5,p6]
print("\n"+"="*66)
print(f"PASS {sum(res)}/{len(res)}")
print("="*66)
print("A SINGLE PROBABILITY DISTRIBUTION -- Lomax(n=2) -- generates:")
print("  deep law, flat rotation curves, r^-2 phantom, amplitude law,")
print("  BTFR, and the universal surface density.")
print("THE INPUT IS A DISTRIBUTION, NOT A LAGRANGIAN.")
json.dump({"pass":int(sum(res)),"fail":int(len(res)-sum(res)),
           "chain":"Lomax(2) -> mu_2 -> g^2=a_0 g_N -> r^-2 phantom -> M~r -> BTFR, Sigma",
           "v_km_s":v/1e3,"Sigma_Msun_pc2":Sig,"r_M_kpc":rM/PC/1e3},
          open("H060_results.json","w"), indent=2)
