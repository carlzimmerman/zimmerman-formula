#!/usr/bin/env python3
"""
PILOT on REAL DATA -- SDSS DR17 member internal velocity dispersion vs cluster-centric radius (Coma).
=====================================================================================================
Tests the EFE sign prediction on real public data: do member galaxies' INTERNAL stellar velocity
dispersions (SDSS velDisp) DECREASE toward the cluster center (stronger external field -> MOND/MI/MG
EFE suppression) or stay FLAT/UP (CDM)?

DATA: SDSS DR17 SpecObj velDisp (per-galaxy stellar sigma_int) for galaxies within 3 deg of Coma
(RA=194.953, Dec=27.981, z=0.0231), cluster members by |dz| consistent with sigma_cluster~1000 km/s.

CAVEAT (honest): SDSS velDisp is a 3-arcsec-fiber central sigma, strongly correlated with galaxy
LUMINOSITY/MASS (Faber-Jackson). A raw sigma-vs-R trend is CONFOUNDED by morphology-density (brighter,
higher-sigma ellipticals concentrate toward cluster centers -> sigma UP toward center for a CDM+FJ
reason that has NOTHING to do with the EFE). The CLEAN EFE test must CONTROL for stellar mass / luminosity
(compare sigma at FIXED M*). This pilot does the raw trend AND a luminosity-controlled (residual) trend.
"""
import numpy as np, warnings, sys
warnings.filterwarnings('ignore')
from astroquery.sdss import SDSS

# Coma
RA0, DEC0, Z0 = 194.953, 27.981, 0.0231
c_kms = 299792.458
def angsep(ra,dec):
    r1,d1,r2,d2=map(np.radians,[RA0,DEC0,ra,dec])
    return np.degrees(np.arccos(np.clip(np.sin(d1)*np.sin(d2)+np.cos(d1)*np.cos(d2)*np.cos(r1-r2),-1,1)))

def fetch():
    sql=f"""SELECT s.ra,s.dec,s.z,s.velDisp,s.velDispErr,
                   p.modelMag_r, p.modelMag_g
            FROM SpecObj AS s JOIN PhotoObj AS p ON s.bestObjID=p.objID
            WHERE s.class='GALAXY' AND s.zWarning=0
              AND s.velDisp>60 AND s.velDispErr>0 AND s.velDispErr<30
              AND s.z BETWEEN 0.010 AND 0.040
              AND s.ra BETWEEN {RA0-3.5} AND {RA0+3.5}
              AND s.dec BETWEEN {DEC0-3.0} AND {DEC0+3.0}"""
    r=SDSS.query_sql(sql, data_release=17)
    return r

def main():
    print("="*92); print(" SDSS DR17 PILOT -- Coma member internal sigma vs cluster-centric radius"); print("="*92)
    try:
        t=fetch()
    except Exception as e:
        print("DATA PULL FAILED:",repr(e)[:160]); sys.exit(2)
    if t is None or len(t)==0:
        print("DATA PULL returned 0 rows."); sys.exit(2)
    ra=np.array(t['ra']); dec=np.array(t['dec']); z=np.array(t['z'])
    sig=np.array(t['velDisp']); sigE=np.array(t['velDispErr'])
    Mr=np.array(t['modelMag_r']); Mg=np.array(t['modelMag_g'])
    print(f" pulled {len(z)} SDSS galaxies near Coma with velDisp")

    # membership: peculiar velocity within ~3 sigma_cluster (Coma sigma~1000 km/s)
    vpec = c_kms*(z-Z0)/(1+Z0)
    sig_cl=1000.0
    mem = np.abs(vpec) < 3*sig_cl
    sep = angsep(ra,dec)                       # deg
    # projected radius: Coma D_A ~ 99 Mpc -> 1 deg ~ 1.73 Mpc
    DA_Mpc = 99.0
    Rproj = np.radians(sep)*DA_Mpc            # Mpc
    inR = Rproj < 3.0
    keep = mem & inR & np.isfinite(sig) & (sig>60) & (sig<420)
    ra,dec,z,sig,sigE,Mr,Mg,vpec,Rproj = [a[keep] for a in (ra,dec,z,sig,sigE,Mr,Mg,vpec,Rproj)]
    N=len(sig)
    print(f" {N} confirmed Coma members (|vpec|<3000 km/s, R<3 Mpc, valid sigma)")
    if N<40:
        print(" too few members for a trend; reporting counts only.");
    # absolute r-band magnitude (k-correction negligible at z~0.023)
    DL = (c_kms*Z0/70.0)  # crude Mpc
    Mabs = Mr - 5*np.log10(DL*1e6/10.0)

    # ---- RAW trend: sigma vs Rproj ----
    print("-"*92); print(" RAW member sigma_int vs projected radius (NOT luminosity-controlled)"); print("-"*92)
    edges=np.array([0,0.25,0.5,0.75,1.0,1.5,2.0,3.0])
    print(f"  {'R[Mpc]':>10} {'N':>4} {'<sigma>[km/s]':>13} {'err':>6} {'<M_r>':>7}")
    binc=[]; binsig=[]; binerr=[]
    for i in range(len(edges)-1):
        m=(Rproj>=edges[i])&(Rproj<edges[i+1])
        if m.sum()>=5:
            ms=np.average(sig[m],weights=1/sigE[m]**2); me=ms/np.sqrt(m.sum())
            binc.append(0.5*(edges[i]+edges[i+1])); binsig.append(ms); binerr.append(me)
            print(f"  {edges[i]:.2f}-{edges[i+1]:.2f}  {m.sum():>4} {ms:>13.1f} {me:>6.1f} {np.median(Mabs[m]):>7.2f}")
    binc=np.array(binc); binsig=np.array(binsig); binerr=np.array(binerr)
    if len(binc)>=3:
        # linear fit sigma vs R
        A=np.vstack([binc,np.ones_like(binc)]).T
        W=np.diag(1/binerr**2)
        cov=np.linalg.inv(A.T@W@A); beta=cov@A.T@W@binsig
        slope,icpt=beta; sl_err=np.sqrt(cov[0,0])
        print(f"\n  RAW slope d<sigma>/dR = {slope:+.1f} +- {sl_err:.1f} km/s/Mpc "
              f"({'sigma rises toward center' if slope<0 else 'sigma falls toward center'}, {abs(slope/sl_err):.1f} sigma)")

    # ---- LUMINOSITY-CONTROLLED trend (the CLEAN EFE test): Faber-Jackson residual vs R ----
    print("-"*92); print(" LUMINOSITY-CONTROLLED: Faber-Jackson residual log(sigma) vs R (the CLEAN EFE test)"); print("-"*92)
    # fit log sigma = a + b*M_r globally, take residuals, then residual-vs-R
    good=np.isfinite(Mabs)&np.isfinite(sig)&(sig>0)
    x=Mabs[good]; y=np.log10(sig[good]); Rg=Rproj[good]
    A=np.vstack([x,np.ones_like(x)]).T; b=np.linalg.lstsq(A,y,rcond=None)[0]
    resid = y - A@b
    print(f"  global Faber-Jackson: log10(sigma) = {b[0]:.3f}*M_r + {b[1]:.3f}")
    print(f"  {'R[Mpc]':>10} {'N':>4} {'<dlog sigma>':>13} {'err':>7}")
    rc=[]; rr=[]; re=[]
    for i in range(len(edges)-1):
        m=(Rg>=edges[i])&(Rg<edges[i+1])
        if m.sum()>=5:
            mr=resid[m].mean(); mer=resid[m].std()/np.sqrt(m.sum())
            rc.append(0.5*(edges[i]+edges[i+1])); rr.append(mr); re.append(mer)
            print(f"  {edges[i]:.2f}-{edges[i+1]:.2f}  {m.sum():>4} {mr:>+13.4f} {mer:>7.4f}")
    rc=np.array(rc); rr=np.array(rr); re=np.array(re)
    if len(rc)>=3:
        A2=np.vstack([rc,np.ones_like(rc)]).T; W=np.diag(1/re**2)
        cov=np.linalg.inv(A2.T@W@A2); beta=cov@A2.T@W@rr
        sl=beta[0]; sle=np.sqrt(cov[0,0])
        # convert dlog sigma per Mpc to % at center vs R=2 Mpc
        d_center = (beta[0]*0.25+beta[1]) - (beta[0]*2.0+beta[1])   # log10 diff center-minus-outer
        pct = (10**d_center-1)*100
        print(f"\n  CONTROLLED slope d<dlog sigma>/dR = {sl:+.4f} +- {sle:.4f} dex/Mpc ({abs(sl/sle):.1f} sigma)")
        print(f"  At fixed luminosity, center(0.25Mpc) vs outer(2Mpc): {pct:+.1f}% in sigma "
              f"({'DOWN toward center = MOND/MI/MG EFE sign' if pct<0 else 'UP toward center = CDM/FJ-residual sign'})")
    print("="*92)
    print(" INTERPRETATION:")
    print("  * If the LUMINOSITY-CONTROLLED residual sigma DROPS toward the center (negative %) -> consistent")
    print("    with the MOND/MI/MG EFE sign (member internal dynamics quenched by the cluster field).")
    print("  * If it RISES or is FLAT -> consistent with CDM (no EFE; tidal/FJ effects).")
    print("  * SDSS velDisp is a 3-arcsec central sigma (luminosity-dominated) -> the RAW trend is FJ-confounded;")
    print("    only the controlled residual is EFE-diagnostic, and even it is weak (the bright SDSS members have")
    print("    g_in>~a0 so the predicted EFE suppression is only a few %). This is a PILOT/feasibility check,")
    print("    not the decisive sample -- the decisive test needs DIFFUSE members (g_in<<a0) where the EFE bites.")
    print("="*92)

if __name__=="__main__":
    main()
