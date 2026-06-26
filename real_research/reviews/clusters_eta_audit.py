#!/usr/bin/env python3
"""Independent audit of the CLUSTER LOSS (eta ~ 2 missing mass) on real eRASS1 data.
   Tests on the FRAMEWORK's OWN footing a0 = 9.36e-11 (pure dark energy), Upsilon~0.7.
   eta = g_obs / (nu(g_bar/a0) * g_bar)  =  M_dyn / M_MOND-predicted  at R500.
   Robustness: interpolation function (simple/standard/RAR-exp/n=2) x baryon budget (fstar 0..0.5).
"""
import numpy as np
from astropy.io import fits

c, G, Msun, kpc = 2.998e8, 6.674e-11, 1.989e30, 3.0857e19
H0 = 2.184e-18                       # 67.4 km/s/Mpc
Om, OmL = 0.315, 0.685
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
RHO_DE0 = OmL*RHO_CRIT0
A0_FRAME = 0.5*c*np.sqrt(G*RHO_DE0)   # framework a0 (pure dark energy)
A0_MOND  = 1.2e-10                     # rival regular MOND

FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

# Interpolation functions nu(y), y = g_bar/a0 ; g_obs = nu * g_bar ; deep-MOND nu -> 1/sqrt(y)
def nu_simple(y):    # "simple" mu(x)=x/(1+x) -> nu = 0.5 + sqrt(0.25 + 1/y)
    return 0.5 + np.sqrt(0.25 + 1.0/y)
def nu_standard(y):  # "standard" mu(x)=x/sqrt(1+x^2) -> nu = sqrt(0.5 + sqrt(0.25 + 1/y^2))
    return np.sqrt(0.5 + np.sqrt(0.25 + 1.0/y**2))
def nu_rar(y):       # McGaugh RAR nu = 1/(1 - exp(-sqrt(y)))
    return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_n2(y):        # n=2 family mu = x^2/(1+x^2)^... ; use g_obs=sqrt(gbar^2+gbar a0) form -> nu = sqrt(1+1/y)
    return np.sqrt(1.0 + 1.0/y)

INTERP = {"simple": nu_simple, "standard": nu_standard, "RAR-exp": nu_rar, "sqrt(g^2+ga0)": nu_n2}

def load(fstar, fgas_lo=0.01, fgas_hi=0.30, zmax=1.0):
    d = fits.open(FITS)[1].data
    f = lambda col: np.array([float(v) if str(v).strip() not in ("","--") else np.nan for v in d[col]], float)
    z, M500, Mgas, fgas, R500, KT = f("BEST_Z"), f("M500"), f("MGAS500"), f("FGAS500"), f("R500"), f("KT")
    M500H, M500L = f("M500_H"), f("M500_L")
    ok = ((z>0)&(z<zmax)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>fgas_lo)&(fgas<fgas_hi))
    M500_kg = M500[ok]*1e13*Msun
    Mbar_kg = (1+fstar)*Mgas[ok]*1e11*Msun
    R_m = R500[ok]*kpc
    gobs = G*M500_kg/R_m**2
    gbar = G*Mbar_kg/R_m**2
    eM = (M500H[ok]-M500L[ok])/(2*np.maximum(M500[ok],1e-6))
    eM = np.clip(np.nan_to_num(eM, nan=0.25), 0.05, 1.0)
    return dict(z=z[ok], M500=M500[ok], gobs=gobs, gbar=gbar, eM=eM, KT=KT[ok], N=int(ok.sum()))

def eta_stats(gobs, gbar, a0, nu):
    y = gbar/a0
    gpred = nu(y)*gbar
    eta = gobs/gpred
    return np.median(eta), 10**np.mean(np.log10(eta)), np.percentile(eta,[25,75])

def main():
    print("="*92)
    print("INDEPENDENT CLUSTER LOSS AUDIT -- eRASS1 (Bulbul+2024), framework a0 = %.3e m/s^2"%A0_FRAME)
    print("="*92)
    base = load(fstar=0.20)
    print("Clean sample (0<z<1, M500>0, Mgas>0, 0.01<fgas<0.30, fstar=0.20): N = %d"%base["N"])
    z=base["z"]; print("  z: median %.3f  (10-90%%: %.3f - %.3f)"%(np.median(z),np.percentile(z,10),np.percentile(z,90)))
    g=base["gbar"]/A0_FRAME
    print("  g_bar/a0 median %.4f  (%.0f%% deep-MOND g_bar<0.1 a0) -> deep-MOND regime confirmed"%(np.median(g),100*(g<0.1).mean()))

    print("\n-- eta = M_dyn/M_MOND-pred at R500, FRAMEWORK a0, across interpolation functions (fstar=0.20) --")
    print("  %-16s %8s %8s %18s"%("interp fn","median","geomean","[q25,q75]"))
    for name,nu in INTERP.items():
        med,gm,q = eta_stats(base["gobs"],base["gbar"],A0_FRAME,nu)
        print("  %-16s %8.3f %8.3f   [%.2f, %.2f]"%(name,med,gm,q[0],q[1]))

    print("\n-- baryon-budget sweep: stellar fraction fstar (=M_star/M_gas), interp=simple --")
    print("  %-10s %8s %8s"%("fstar","median","geomean"))
    for fstar in (0.0,0.10,0.20,0.30,0.50):
        b=load(fstar=fstar); med,gm,_=eta_stats(b["gobs"],b["gbar"],A0_FRAME,nu_simple)
        print("  %-10.2f %8.3f %8.3f"%(fstar,med,gm))

    print("\n-- framework a0 vs rival regular MOND a0=1.2e-10 (interp=simple, fstar=0.20) --")
    for lab,a0 in (("framework 9.36e-11",A0_FRAME),("regular MOND 1.2e-10",A0_MOND)):
        med,gm,_=eta_stats(base["gobs"],base["gbar"],a0,nu_simple)
        print("  %-22s eta median %.3f  geomean %.3f"%(lab,med,gm))
    print("  ratio sqrt(1.2e-10/9.36e-11) = %.3f  (deep-MOND: lower a0 -> bigger eta)"%np.sqrt(A0_MOND/A0_FRAME))

    print("\n-- significance of the deficit --")
    med,gm,q = eta_stats(base["gobs"],base["gbar"],A0_FRAME,nu_simple)
    logeta = np.log10(base["gobs"]/(nu_simple(base["gbar"]/A0_FRAME)*base["gbar"]))
    N=base["N"]; mean_log=np.mean(logeta); sd_log=np.std(logeta)
    se_log = sd_log/np.sqrt(N)
    print("  mean log10(eta) = %+.4f dex, scatter = %.4f dex, N=%d"%(mean_log,sd_log,N))
    print("  formal SE on the mean = %.5f dex -> %.0f sigma > 0 (statistical only)"%(se_log, mean_log/se_log))
    for floor in (0.10,0.15,0.20):
        print("    vs absolute-scale systematic floor %.2f dex: %.1f sigma"%(floor, mean_log/floor))
    # per-cluster significance using each cluster's own mass error
    sig_each = logeta/ (base["eM"]/np.log(10))   # eM is fractional -> dex via /ln10
    print("  median per-cluster significance (own M500 error): %.1f sigma"%np.median(sig_each))

    print("\n-- eta vs M500 bins (does it worsen with mass? interp=simple, fstar=0.20) --")
    M=base["M500"]; edges=np.percentile(M,[0,20,40,60,80,100])
    gobs,gbar=base["gobs"],base["gbar"]
    print("  %-18s %6s %8s"%("M500 bin [1e13]","N","eta_med"))
    for i in range(5):
        m=(M>=edges[i])&(M<edges[i+1] if i<4 else M<=edges[i+1])
        med,_,_=eta_stats(gobs[m],gbar[m],A0_FRAME,nu_simple)
        print("  %5.1f - %-10.1f %6d %8.3f"%(edges[i],edges[i+1],m.sum(),med))

    print("\n-- how much a0 boost is needed to erase eta? --")
    print("  M_eff prop sqrt(a0) in deep MOND -> need a0 x eta^2.  eta_med=%.2f -> a0 x %.1f (= +%.2f dex)"
          %(med if False else eta_stats(base['gobs'],base['gbar'],A0_FRAME,nu_simple)[0],
            eta_stats(base['gobs'],base['gbar'],A0_FRAME,nu_simple)[0]**2,
            2*np.log10(eta_stats(base['gobs'],base['gbar'],A0_FRAME,nu_simple)[0])))
    print("="*92)

if __name__=="__main__":
    main()
