"""CORRECTION (referee lane Z6, agents/Z6_memory_kernel_referee): the premise below (record kernel = Sciama r dr kernel with cutoff c^2/a0) is TRUE ONLY FOR THE MOMENT M1, NOT FOR THE KERNEL. The record's kernel is a free-weight memory in proper-time lag on the rapidity gap (no G, no density); the cutoff it implies is 2, 8/3, 4/3 or 2/3 x R* depending on shape and scales as 1/M0; at Sciama's physical strength it would be 0.683 R*; the long-memory branch at T = c/a0 violates the ephemeris bound by ~1e12. So the table below is a table of what a cutoff at each horizon WOULD give for a generic 1/r-type kernel, and the particle-horizon-diameter agreement is NOT evidence for the record's kappa = 1/2.

p11: the Machian-cutoff reading of the record's memory moment.  Record (mi_N_count_and_kappa_iff_2026.py): kappa=1/2 <=> M1 = (4/3) t_Lambda, with M1 = (2/3) c/a0.
X3 (agents/X3_extended_thermo_mach): for a sharp retarded 1/r (Sciama) kernel, weight r dr on [0, R_c/c], M1 = (2/3) R_c/c, so the record's premise is R_c = c^2/a0 = 2 R*, R* = c/sqrt(G rho_Lambda).
QUESTION: which physically motivated cutoff length equals c^2/a0?  Candidate cutoffs DECLARED BEFORE computing (principle: a Machian inertia integral is cut off where matter stops being causally connected):
  E  event horizon (radius, ~ c/H_Lambda asymptotically), P particle horizon (radius), D particle-horizon diameter 2 R_p, H Hubble radius c/H0, S = R* , S2 = 2 R*.
FIRST RUN (kept): check 4 expected P(random length within 8% of 2R*) < 0.05; it is 0.124, so the control says the particle-horizon-diameter match is WEAK evidence (that is the honest reading, and check 4 now asserts it).
Check 6 expected d_p H/c = 2 at z = 50; it is 1.785 because radiation shortens the horizon (~1 - sqrt(a_eq/a)); it is tested below with radiation switched off.
Convention: this is a numerology-risk table; it is a TEST of one declared principle per candidate, not a fit.  Planck-2018-like LCDM: H0 = 67.4, Om = 0.315, OL = 0.685, Or = 9.1e-5 (radiation), flat.
"""
import numpy as np, sys
from scipy.integrate import quad
c=2.99792458e8; Mpc=3.0856775814913673e22; Gyr=3.15576e16
H0=67.4e3/Mpc
Om,OL=0.315,0.685; Or=9.1e-5; Om_eff=Om-Or
E=lambda a: np.sqrt(Or/a**4+Om_eff/a**3+OL)          # H/H0 as function of scale factor
ok=[]
def chk(n,cnd): ok.append(bool(cnd)); print(("PASS " if cnd else "FAIL ")+n)
# proper horizon distances today (a=1)
Rp=c/H0*quad(lambda a:1/(a**2*E(a)),1e-12,1,limit=400)[0]      # particle horizon (proper, today)
Re=c/H0*quad(lambda a:1/(a**2*E(a)),1,np.inf,limit=400)[0]     # event horizon
RH=c/H0
G=6.674e-11; rhoL=OL*3*H0**2/(8*np.pi*G)
Rstar=c/np.sqrt(G*rhoL)
print("   particle horizon R_p = %.2f Gly = %.3f c/H0 ; event horizon = %.2f Gly = %.3f c/H0 ; c/H0 = %.2f Gly ; R* = %.2f Gly = %.3f c/H0"%(Rp/c/Gyr/1e9*1e9/1e9*1e9/1e9 if False else Rp/(c*Gyr)/1,Rp/RH,Re/(c*Gyr),Re/RH,RH/(c*Gyr),Rstar/(c*Gyr),Rstar/RH))
cands={"E event horizon":Re,"P particle-horizon radius":Rp,"D particle-horizon diameter":2*Rp,"H Hubble radius c/H0":RH,"S R*":Rstar,"S2 2R* (record's premise)":2*Rstar}
a0_sparc=1.0766e-10
print("   a0 = c^2/R_c for each candidate cutoff, vs SPARC 1.0766e-10 (5.4% stat, ~12% analysis scatter) and vs the record's premise c^2/(2R*):")
tab={}
for k,R in cands.items():
    a0=c**2/R; tab[k]=a0
    print("   %-30s R_c = %6.2f Gly   a0 = %.3e   a0/SPARC = %.3f   R_c/(2R*) = %.3f"%(k,R/(c*Gyr),a0,a0/a0_sparc,R/(2*Rstar)))
chk("1 reproduces R_c = c^2/a0 <=> a0 = c^2/R_c and 2R* = Z * c/H_Lambda (Z = sqrt(32 pi/3)) with H_Lambda = H0 sqrt(OL)",
    abs(2*Rstar/(c/(H0*np.sqrt(OL)))-np.sqrt(32*np.pi/3))<1e-9)
chk("2 event-horizon cutoff gives a0 well above SPARC (>= 3x): the Deser-Levin/Z=1-type outcome is excluded by the data",
    tab["E event horizon"]/a0_sparc>3)
D=tab["D particle-horizon diameter"]/a0_sparc; S2=tab["S2 2R* (record's premise)"]/a0_sparc
chk("3 particle-horizon DIAMETER lands within 5%% of SPARC (ratio %.3f) and within 10%% of 2R* (R_D/2R* = %.3f): reported, not a result"%(D,2*Rp/(2*Rstar)), abs(D-1)<0.05 and abs(2*Rp/(2*Rstar)-1)<0.10)
# decoy control: how often does a random 'natural' length in [1,10] c/H0 land within 8% of 2R*
rng=np.random.default_rng(3); lens=rng.uniform(1,10,100000)
frac=np.mean(np.abs(lens/(2*Rstar/RH)-1)<0.08)
chk("4 control (my <0.05 expectation was WRONG): a length drawn uniformly in [1,10] c/H0 lands within 8%% of 2R* with probability %.3f, so an 8%% match among ~6 declared candidates is expected ~%.0f%% of the time: the particle-horizon match is NOT informative"%(frac,100*(1-(1-frac)**6)), frac>0.05)
# evolution: if the cutoff is the (proper) particle-horizon diameter, a0(z) = c^2/(2 d_p(z)), d_p(z) = a * c int_0^a da'/(a'^2 H)
def dp(a): return a*c/H0*quad(lambda x:1/(x**2*E(x)),1e-12,a,limit=400)[0]
a0_of=lambda z:c**2/(2*dp(1/(1+z)))
r=[a0_of(z)/a0_of(0) for z in (0.5,1,2.5,5)]
Hz=lambda z:E(1/(1+z))
print("   particle-horizon-diameter law a0(z)/a0(0):  z=0.5 %.2f  z=1 %.2f  z=2.5 %.2f  z=5 %.2f   (H(z)/H0 at 2.5 = %.2f; flat law = 1.00; LCDM-native +0.33 dex = 2.14 at 2.5)"%(r[0],r[1],r[2],r[3],Hz(2.5)))
chk("5 that law RISES with z (tracks ~H(z) at high z, matter-era d_p = 2c/H): it is the rival, not the framework's flat law; at z=2.5 it predicts +%.2f dex"%np.log10(r[2]), r[2]>3)
# matter-era check d_p ~ 2c/H
z=50
Er=lambda a: np.sqrt(Om/a**3+OL)                               # radiation off
dpr=(1/(1+z))*c/H0*quad(lambda x:1/(x**2*Er(x)),1e-12,1/(1+z),limit=400)[0]
chk("6 matter-era check with radiation off: d_p(z=50) H(z)/c = %.4f (matter domination -> 2); with radiation on it is %.3f (radiation shortens the horizon: first-run miss explained)"%(dpr*H0*Er(1/(1+z))/c, dp(1/(1+z))*H0*Hz(z)/c), abs(dpr*H0*Er(1/(1+z))/c-2)<0.02)
print("\n%d/%d"%(sum(ok),len(ok))); sys.exit(0 if all(ok) else 1)
