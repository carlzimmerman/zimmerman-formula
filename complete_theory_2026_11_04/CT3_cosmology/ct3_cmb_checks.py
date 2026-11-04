"""CT3 small check (review lane, no frozen gate; numbers only). Vanilla CLASS 3.3.4 (classy) + the raw Planck PR3 TT file
already on disk (diagonal errors only, no foreground/calibration model: NOT a likelihood). Part 1: peak heights of the raw
spectrum vs CLASS at the true peak positions (not fixed l). Part 2: H3/H2 against omega_x/omega_b in the dust family, and
sensitivity to n_s, omega_b. Part 3: no-cold cases (baryons only; 3 x 0.45 / 1.0 eV neutrinos). Run:
OMP_NUM_THREADS=1 nice -n 10 python3 ct3_cmb_checks.py > ct3_cmb_checks.out   (about 1 min, 0.37 GB RSS).
kappa = 1/2 FITTED and unused here. Adopts nothing; reinstates nothing."""
import os
import numpy as np
from classy import Class
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
# ---- ct3_peaks ----
TT=os.path.join(EXT,"cmb_lensing_raw/planck_PR4_lensing/planckpr4lensing/data_pr4/iswliks/COM_PowerSpect_CMB-TT-full_R3.01.txt")
a=np.loadtxt(TT); l=a[:,0]; D=a[:,1]; e=0.5*(a[:,2]+a[:,3])
def peak_fit(l,D,e,lo,hi):
    m=(l>=lo)&(l<=hi); x=l[m]; y=D[m]; w=1/e[m]**2
    c,cov=np.polyfit(x-x.mean(),y,4,w=np.sqrt(w),cov='unscaled')
    xs=np.linspace(x.min(),x.max(),4000); ys=np.polyval(c,xs-x.mean()); i=np.argmax(ys)
    # MC errors
    rng=np.random.default_rng(1); hs=[]
    for _ in range(400):
        cc=rng.multivariate_normal(c,cov); yy=np.polyval(cc,xs-x.mean()); hs.append(yy.max())
    return xs[i],ys[i],np.std(hs)
win={1:(150,300),2:(440,640),3:(720,920)}
P={k:peak_fit(l,D,e,*v) for k,v in win.items()}
print("RAW Planck PR3 TT (diag errors, quartic fits, foregrounds not removed):")
for k,(lp,h,s) in P.items(): print(f"  peak{k}: l={lp:.0f} D={h:.0f} +- {s:.0f} uK^2")
r32=P[3][1]/P[2][1]; r21=P[2][1]/P[1][1]
print(f"  H3/H2 = {r32:.3f} +- {r32*np.hypot(P[3][2]/P[3][1],P[2][2]/P[2][1]):.3f};  H2/H1 = {r21:.3f}")
base={"h":0.6736,"omega_b":0.02237,"A_s":2.1e-9,"n_s":0.9649,"tau_reio":0.0544,"N_ur":3.046,"YHe":0.2454,"output":"tCl","l_max_scalars":2000}
def run(oc,h=0.6736):
    c=Class(); p=dict(base); p.update({"omega_cdm":oc,"h":h}); c.set(p); c.compute()
    cl=c.raw_cl(2000); ll=cl["ell"][2:]; DD=ll*(ll+1)*cl["tt"][2:]/(2*np.pi)*(2.7255e6)**2
    der=c.get_current_derived_parameters(["rs_d","100*theta_s","z_d"])
    # local maxima
    pk=[(ll[i],DD[i]) for i in range(5,len(DD)-5) if DD[i]==DD[i-5:i+6].max() and ll[i]>100][:4]
    c.struct_cleanup(); return pk,der,DD,ll
for oc,h in [(0.1200,0.6736),(0.0,0.6736),(0.0,0.45)]:
    pk,der,DD,ll=run(oc,h)
    hs=[p[1] for p in pk]
    print(f"omega_c={oc} h={h}: peaks l={[int(p[0]) for p in pk]} D={[round(x) for x in hs]}  H3/H2={hs[2]/hs[1]:.3f} H2/H1={hs[1]/hs[0]:.3f}  fixed-l D(816)/D(537)={DD[814]/DD[535]:.3f}  r_d={der['rs_d']:.1f} 100theta_s={der['100*theta_s']:.4f}")
# ---- ct3_scan ----
base={"h":0.6736,"omega_b":0.02237,"A_s":2.1e-9,"n_s":0.9649,"tau_reio":0.0544,"N_ur":3.046,"YHe":0.2454,"output":"tCl","l_max_scalars":2200}
def peaks(p):
    c=Class(); q=dict(base); q.update(p); c.set(q); c.compute()
    cl=c.raw_cl(2200); ll=cl["ell"][2:]; DD=ll*(ll+1)*cl["tt"][2:]
    pk=[DD[i] for i in range(5,len(DD)-5) if DD[i]==DD[i-5:i+6].max() and ll[i]>100][:3]
    rd=c.rs_drag(); c.struct_cleanup(); return pk[2]/pk[1],pk[1]/pk[0],rd
for oc in [0.0,0.02,0.04,0.06,0.08,0.10,0.11,0.12,0.13,0.14]:
    r32,r21,rd=peaks({"omega_cdm":oc}); print(f"omega_c {oc:.2f} ratio {oc/0.02237:5.2f}: H3/H2 {r32:.3f} H2/H1 {r21:.3f} r_d {rd:.1f}")
for ns in [0.93,1.0]:
    r32,r21,rd=peaks({"omega_cdm":0.12,"n_s":ns}); print(f"n_s {ns}: H3/H2 {r32:.3f} H2/H1 {r21:.3f}")
for ob in [0.0212,0.0232]:
    r32,r21,rd=peaks({"omega_cdm":0.12,"omega_b":ob}); print(f"omega_b {ob}: H3/H2 {r32:.3f} H2/H1 {r21:.3f}")
r32,r21,rd=peaks({"omega_cdm":0.0,"n_s":1.3}); print(f"omega_c 0, n_s 1.3: H3/H2 {r32:.3f} H2/H1 {r21:.3f}")
r32,r21,rd=peaks({"omega_cdm":0.0,"N_ur":0.0}); print(f"omega_c 0, N_ur 0: H3/H2 {r32:.3f} H2/H1 {r21:.3f}")
# ---- ct3_nu ----
for m in [0.45,1.0]:
    p={"h":0.6736,"omega_b":0.02237,"omega_cdm":0.0,"A_s":2.1e-9,"n_s":0.9649,"tau_reio":0.0544,"N_ur":0.00641,"N_ncdm":1,"m_ncdm":m,"deg_ncdm":3,"YHe":0.2454,"output":"tCl,mPk","l_max_scalars":2200,"P_k_max_h/Mpc":2}
    c=Class(); c.set(p); c.compute(); cl=c.raw_cl(2200); ll=cl["ell"][2:]; DD=ll*(ll+1)*cl["tt"][2:]
    pk=[DD[i] for i in range(5,len(DD)-5) if DD[i]==DD[i-5:i+6].max() and ll[i]>100][:3]
    print(f"3x{m} eV nu, no cold: omega_nu {c.Omega_nu*0.6736**2:.4f} H3/H2 {pk[2]/pk[1]:.3f} sigma8 {c.sigma8():.4f}")
    c.struct_cleanup()
c=Class(); c.set({"h":0.6736,"omega_b":0.02237,"omega_cdm":0.0,"A_s":2.1e-9,"n_s":0.9649,"tau_reio":0.0544,"output":"mPk","P_k_max_h/Mpc":2}); c.compute(); print("baryons only sigma8",round(c.sigma8(),4)); c.struct_cleanup()