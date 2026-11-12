# Ungraded review arithmetic: reads DESI DR2 Results III Table 4 against the DW1 lane's A=1 line.
# Independent SI recomputation (not an import of dw1.py). Diagonal errors only.
import math, json
G=6.67430e-11; MSUN=1.98847e30; KPC=3.0856775814913673e19
MB=6.681e10*MSUN
A0={"canonical":9.36e-11,"alt":1.13e-10}
R=[20,25,30,35,40,45,50,55,60,65,70,75,80]
F=[0.9408,0.9642,0.9777,0.9856,0.9903,0.9931,0.9947,0.9958,0.9964,0.9967,0.9969,0.9970,0.9972]
ALL=[1.94,2.30,2.65,3.05,3.54,4.08,4.51,4.88,5.19,5.56,5.88,6.14,6.36]
ALLlo=[0.12,0.11,0.13,0.15,0.17,0.21,0.26,0.31,0.34,0.38,0.43,0.46,0.48]
ALLhi=[0.12,0.12,0.14,0.16,0.18,0.22,0.27,0.32,0.36,0.40,0.46,0.50,0.53]
RRL=[1.97,2.38,2.65,3.11,3.79,4.38,4.81,5.19,5.49,5.79,6.05,6.24,6.40]
RRLlo=[0.16,0.16,0.16,0.19,0.24,0.31,0.38,0.45,0.50,0.54,0.57,0.59,0.59]
BHB=[1.93,2.24,2.63,2.97,3.37,3.89,4.34,4.72,5.04,5.43,5.79,6.10,6.38]
BHBlo=[0.14,0.13,0.16,0.18,0.19,0.25,0.30,0.35,0.40,0.46,0.55,0.60,0.66]
def nu(y): return 1.0/(1.0-math.exp(-math.sqrt(y)))
def Mfw(i,a0,A=1.0,eN=0.0):
    Mb=A*F[i]*MB; g=G*Mb/(R[i]*KPC)**2
    return nu((g+eN*a0)/a0)*Mb/MSUN/1e11
print("r   DESI_all  RRL   BHB  | fw_can(A=1) z_all z_RRL z_BHB | fw_alt(A=1) z_all z_RRL z_BHB | Vc_DESI km/s")
for i,r in enumerate(R):
    row=f"{r:3d}  {ALL[i]:5.2f}  {RRL[i]:5.2f} {BHB[i]:5.2f} |"
    for f in ("canonical","alt"):
        m=Mfw(i,A0[f])
        # model below data -> use lower error bar
        row+=f"  {m:5.2f}   {(m-ALL[i])/ALLlo[i]:+5.2f} {(m-RRL[i])/RRLlo[i]:+5.2f} {(m-BHB[i])/BHBlo[i]:+5.2f} |"
    vc=math.sqrt(G*ALL[i]*1e11*MSUN/(r*KPC))/1e3
    print(row, f"{vc:6.1f}")
# check against the lane's stored 80 kpc numbers
print("check 80 kpc: can %.3f (lane 5.691), alt %.3f (lane 6.218)"%(Mfw(12,A0['canonical']),Mfw(12,A0['alt'])))
print("with scalar-additive EFE eN=0.01273: can %.3f (lane 4.307), alt %.3f (lane 4.508)"%(Mfw(12,A0['canonical'],eN=0.01273),Mfw(12,A0['alt'],eN=0.01273)))
# log slopes
def slope(M,i,j): return math.log(M[j]/M[i])/math.log(R[j]/R[i])
for name,M in (("DESI all",ALL),("DESI RRL",RRL),("DESI BHB",BHB)):
    print(f"{name}: dlnM/dlnr 20-50 = {slope(M,0,6):.3f}, 50-80 = {slope(M,6,12):.3f}, 20-80 = {slope(M,0,12):.3f}")
for f in A0:
    M=[Mfw(i,A0[f]) for i in range(13)]
    print(f"framework {f}: dlnM/dlnr 20-50 = {slope(M,0,6):.3f}, 50-80 = {slope(M,6,12):.3f}, 20-80 = {slope(M,0,12):.3f}")
# NFW comparator the paper draws: M200c=1.19e12, c=12, rho_c from h=0.6777 (Auriga/Planck) -> use 200 rho_c
H0=67.77*1e3/3.0856775814913673e22; rhoc=3*H0**2/(8*math.pi*G)
M200=1.19e12*MSUN; r200=(3*M200/(4*math.pi*200*rhoc))**(1/3); c=12; rs=r200/c
mu=lambda x: math.log(1+x)-x/(1+x)
N=[M200*mu(r*KPC/rs)/mu(c)/MSUN/1e11 for r in R]
print(f"NFW(1.19e12,c=12): r200={r200/KPC:.1f} kpc; M(<20)={N[0]:.2f}, M(<50)={N[6]:.2f}, M(<80)={N[12]:.2f}; slopes 20-50 {slope(N,0,6):.3f}, 50-80 {slope(N,6,12):.3f}")
# GME: raw power law M ~ r^(1-gamma)
for g in (0.44,0.45,0.46): print(f"GME gamma={g}: raw dlnM/dlnr = {1-g:.2f}; with f(r) 0.8->0.9 over 50-80 kpc add {math.log(0.9/0.8)/math.log(80/50):.3f}")
print("GME prior sigma_gamma = %.4f; framework slope 50-80 needs gamma = %.3f (can) -> %.1f prior sigma from prior mean 0.440"%(math.sqrt(0.0021),1-slope([Mfw(i,A0['canonical']) for i in range(13)],6,12),(0.440-(1-slope([Mfw(i,A0['canonical']) for i in range(13)],6,12)))/math.sqrt(0.0021)))
# individual-method 80 kpc masses vs the framework (1e11)
ind={"GME RRL":(5.3,0.5),"GME BHB":(6.4,0.6),"emPDF BHB":(6.7,1.7),"emPDF RRL":(7.8,2.0),"Joint":(6.36,0.48)}
for f in A0:
    m=Mfw(12,A0[f]); print(f, "A=1 no EFE M80=%.2f:"%m, "; ".join(f"{k} {(m-v)/s:+.2f}" for k,(v,s) in ind.items()))
# deep-MOND asymptote
for f in A0: print(f, "V_flat=(G Mb a0)^(1/4) = %.1f km/s"%((G*MB*A0[f])**0.25/1e3))
# Lya AP sensitivity: fraction of H^2 from dark energy at z=2.33 (Om=0.3042, flat LCDM) and CPL example
Om=0.3042; z=2.33; E2m=Om*(1+z)**3; print("LCDM: DE share of H^2 at z=2.33 = %.3f"%((1-Om)/(E2m+1-Om)))
w0,wa=-0.75,-0.86; f=(1+z)**(3*(1+w0+wa))*math.exp(-3*wa*z/(1+z)); print("CPL(w0=-0.75,wa=-0.86) illustrative: rho_DE(z=2.33)/rho_DE(0) = %.3f -> a0 ratio %.3f"%(f,math.sqrt(f)))
print("D_H 0.77%% -> H^2 1.5%% -> rho_DE(z)/rho_DE(0) resolution at fixed Om h^2, r_d: +-%.2f"%(2*0.066/8.600*(E2m+1-Om)/(1-Om)))
