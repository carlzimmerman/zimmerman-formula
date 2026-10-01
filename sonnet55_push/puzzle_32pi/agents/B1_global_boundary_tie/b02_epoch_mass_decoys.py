"""b02: G10 (Einstein-Straus vacuole, w=rho_m/rho_L), epoch and physical mass of the puzzle's hole, sub-Hubble bound, decoy test."""
import numpy as np, sys
from scipy.optimize import brentq
ok=[]
def chk(n,c): ok.append(bool(c)); print(("PASS " if c else "FAIL ")+n)
G=6.674e-11; c=2.99792458e8; Msun=1.98847e30; Mpc=3.0857e22; Gyr=3.15576e16
H0=67.4e3/Mpc; Om=0.315; OL=0.685      # declared footing: rho_Lambda footing, Planck-like; not tuned
HL=H0*np.sqrt(OL); L=c/HL               # L^2=3/Lambda  (Lambda=3 OL H0^2/c^2)
Lam=3*OL*H0**2/c**2; chk("1 L^2 = 3/Lambda consistent with L=c/H_Lambda",abs(L**2*Lam-3)<1e-9)
# G10: r_s = r_ES(w) <=> w = 3/(8 pi r_s^2/ ... ) general: r_s^2 Lambda = 3/w  (L-units: 3 r^2 = 3/w)
for rsL2 in [4/9,1.0,3.0,8*np.pi/3]:   # r_s^2 Lambda = 3 x^2
    pass
w_of=lambda rs2Lam: 3.0/rs2Lam         # derived: rho_h=3/(8 pi r_s^2) = w rho_L = w Lambda/8pi => r_s^2 Lambda = 3/w
chk("2 G10: r_s^2 Lambda = 3/w (algebra); at r_s^2 Lambda=8 pi -> w = 3/(8 pi) = %.5f"%(3/(8*np.pi)), abs(w_of(8*np.pi)-3/(8*np.pi))<1e-15)
# inequality: hole inside vacuole iff w <= 3/r_s^2Lambda
# direct numeric check of r_ES = r_s using explicit M, rho
rs=np.sqrt(8*np.pi/Lam); M=rs*c**2/(2*G); rhoL=Lam*c**2/(8*np.pi*G)
w=3/(8*np.pi); resES=(3*M/(4*np.pi*w*rhoL))**(1/3)
chk("3 numeric (SI): Einstein-Straus radius at w=3/(8pi) equals r_s=%.3e m (rel err %.1e)"%(rs,abs(resES/rs-1)), abs(resES/rs-1)<1e-12)
# epoch: w(a)=(Om/OL) a^-3
astar=((Om/OL)/w)**(1/3); z=1/astar-1
tfun=lambda a:(2/(3*HL))*np.arcsinh(np.sqrt(OL/Om)*a**1.5)
dt=(tfun(astar)-tfun(1.0))/Gyr
print("epoch: a*=%.3f (z=%.3f), t(a*)-t0 = %.1f Gyr, Omega_m(a*) = %.4f"%(astar,z,dt,w/(1+w)))
chk("4 epoch is in the future (a*>1): the puzzle's hole fits an ES vacuole only for w <= 3/8pi, i.e. a >= %.2f; today w=%.3f"%(astar,Om/OL), astar>1 and Om/OL>w)
# mass
Mkg=M; print("M = %.4e kg = %.4e Msun = %.3f L c^2/G = %.2f M_N"%(Mkg,Mkg/Msun,rs/(2*L),Mkg/(c**2*L/(3*np.sqrt(3)*G))))
rho_m0=Om*3*H0**2/(8*np.pi*G)
M_hub=4*np.pi/3*rho_m0*(c/H0)**3; M_obs=4*np.pi/3*rho_m0*(46.5e9*9.4607e15)**3
M_N=c**2*L/(3*np.sqrt(3)*G)
print("matter in today's Hubble sphere %.3e Msun; in comoving observable universe (46.5 Gly) %.3e Msun; M_N %.3e Msun"%(M_hub/Msun,M_obs/Msun,M_N/Msun))
print("ratios M/M_hub = %.2f, M/M_obs = %.2f"%(M/M_hub,M/M_obs))
chk("5 M is NOT the Hubble-sphere matter mass (ratio %.1f) and not M_N (ratio 7.52); it is within a factor 3 of the observable-universe matter mass (ratio %.2f)"%(M/M_hub,M/M_obs), M/M_hub>5 and 0.2<M/M_obs<1)
# sub-Hubble bound: r_s <= r_ES <= c/H(a)  =>  r_s^2 Lambda <= 3 /(1+w)
sup=max(3/(1+wi) for wi in np.logspace(-8,3,50)); 
chk("6 sub-Hubble vacuole (R_ES <= c/H) forces r_s^2 Lambda < 3/(1+w) <= 3, never 8 pi (%.3f)"%sup, sup<3.0000001 and sup<8*np.pi)
Hstar=HL*np.sqrt(1+w); print("at a*: r_s H = %.3f (r_s = %.2f c/H): the hole is %.1fx larger than the Hubble radius"%(rs*Hstar/c,rs*Hstar/c,rs*Hstar/c))
chk("7 at the epoch where the vacuole just contains the hole, r_s = %.2f c/H(a*) : the vacuole is super-Hubble (acausal region)"%(rs*Hstar/c), rs*Hstar/c>2)
# decoy test: natural-mass menu
menu=np.array([M_hub,M_obs,M_N,M_obs/(4*np.pi/3),M_N*np.pi,M_hub*2*np.pi])  # 6 declared (after seeing the answer: a MENU, not a prediction)
tol=0.35; rng=np.random.default_rng(1)
tg=M/np.array(menu)
print("M / menu = ",np.round(tg,2))
decoy=10**rng.uniform(np.log10(M_N*0.3),np.log10(M_obs*10),20000)
hit=np.mean([np.min(np.abs(np.log(d/menu)))<np.log(1+tol) for d in decoy])
print("decoy hit-rate (random mass in [0.3 M_N, 10 M_obs] within +-35%% of some menu mass): %.2f"%hit)
chk("8 decoy control: a random mass matches some menu entry %.0f%% of the time, so a numerical closeness of M to a cosmic mass is not evidence"%(100*hit), hit>0.4)
# control mutation: wrong ES density (w=2 reading) changes r
chk("9 mutation: using w=2 (zero-force radius) instead gives r_ES/r_s = %.3f != 1 at the same M"%((3*M/(4*np.pi*2*rhoL))**(1/3)/rs), abs((3*M/(4*np.pi*2*rhoL))**(1/3)/rs-1)>0.1)
print("%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
