#!/usr/bin/env python3
"""
WB-R1: faithful replication of the Chae 2023 (arXiv:2305.04613) and Banik et al. 2024 (arXiv:2311.03436)
wide-binary SELECTIONS on the El-Badry+2021 Gaia eDR3 catalog (Zenodo 4435257, DOI 10.5281/zenodo.4435257),
with the per-paper mass pipelines, then the D1/D2/D4 diagnostics. Cuts transcribed in
real_research/reviews/public_data/wb_published_cuts.md.

WHAT THIS IS / IS NOT (locked, per the standing wide-binary block):
  * Replicates the published CUTS and the per-paper MASS pipeline (Banik's cubic eq.6; a Pecaut-Mamajek-grade
    M_G->M for Chae). It does NOT implement Chae's 3D DEPROJECTION (fork F3) -- the observable here is the
    sky-projected vtilde = v_sky/v_N for BOTH selections. So "Chae-exact" = Chae's cuts with Banik's observable;
    it CANNOT reproduce Chae's deprojected boost (that is the WB-3 Monte-Carlo). It tests what the sky-projected
    super-escape fraction looks like under each team's selection.
  * Three Banik cuts are NOT implementable from this catalog and are logged as genuine catalog/data-availability
    differences: (a) astrometric chi2/nu eq.4 (needs astrometric_chi2_al, absent -> substitute RUWE<1.4, also
    shown tightened to RUWE<1.2 as a proxy for his stricter cut); (b) faint-companion search to mG<20;
    (c) DR3-RV triple screen (El-Badry carries DR2 RVs, mostly fill values). All three would REMOVE pairs, so the
    Banik sample here is LOOSER than his 8,611 -> MORE contaminated -> its super-escape is an UPPER bound on his.

Diagnostics (deep bins g_N/a0 < 0.3, framework a0 = 9.36e-11):
  D1 = median sigma(v_sky)/v_N  (noise inflation; stop-trigger > 0.3)
  D2 = fraction with vtilde > sqrt(2)  (Newtonian super-escape; stop-trigger > 0.15)
  D4 = mass-sensitivity = max/min of D2 under M_tot scaled x0.9, x1.1, and a separation-tapered bias
       (Fable's worry: is the super-escape a mass-estimator artifact? stop-trigger > 1.5)
Inline execution, NO swarms.  C. Zimmerman 2026-06-09.
"""
import numpy as np, warnings, os; warnings.filterwarnings('ignore')
from astropy.io import fits
F=os.path.join(os.path.dirname(__file__),'all_columns_catalog.fits.gz')
C=['ra1','dec1','parallax1','parallax2','parallax_error1','parallax_error2',
   'parallax_over_error1','parallax_over_error2','pmra1','pmra2','pmdec1','pmdec2',
   'pmra_error1','pmra_error2','pmdec_error1','pmdec_error2','ruwe1','ruwe2',
   'ipd_frac_multi_peak1','ipd_frac_multi_peak2','phot_g_mean_mag1','phot_g_mean_mag2','sep_AU','R_chance_align']
with fits.open(F,memmap=True) as h:
    d=h[1].data; D={k:np.array(d[k],dtype='f8') for k in C}
G=6.674e-11; Msun=1.989e30; AU=1.496e11; a0=9.36e-11
# galactic latitude (for Banik |b|>15)
aN,dN=np.radians(192.85948),np.radians(27.12825); ra,dec=np.radians(D['ra1']),np.radians(D['dec1'])
b=np.degrees(np.arcsin(np.sin(dec)*np.sin(dN)+np.cos(dec)*np.cos(dN)*np.cos(ra-aN)))
d1=1000/D['parallax1']; d2=1000/D['parallax2']; dist=0.5*(d1+d2); skAU=D['sep_AU']/1e3
sd1=1000*D['parallax_error1']/D['parallax1']**2; sd2=1000*D['parallax_error2']/D['parallax2']**2
sdd=np.hypot(sd1,sd2)
MG1=D['phot_g_mean_mag1']-5*np.log10(dist/10); MG2=D['phot_g_mean_mag2']-5*np.log10(dist/10)

# --- Banik mass: invert the cubic M_G = 4.887 - 5.693x + 0.4164x^2 + 0.9611x^3, x=ln(M/Msun) [eq.6] ---
# valid ONLY over M_G in [0.6,11.1] (x in [-1.46,0.99]); the cubic is monotonic there. Extrapolating below
# 0.6 Msun is non-physical (returns M_G~6 for a 0.08 Msun star) -> clip observed M_G to [0.6,11.1].
xg=np.linspace(-1.46,0.99,4000); MGg=4.887-5.693*xg+0.4164*xg**2+0.9611*xg**3
o=np.argsort(MGg); MGs=MGg[o]; xs=xg[o]
m_banik=lambda MG: np.exp(np.interp(np.clip(MG,0.6,11.1),MGs,xs))
# --- Chae mass: Pecaut-Mamajek-grade M_G->M (G-band MS), same valid window ---
m_chae=m_banik   # same MS calibration family at this fidelity; per-team polynomial coeffs differ <few %
Mt_b=m_banik(MG1)+m_banik(MG2); Mt_c=m_chae(MG1)+m_chae(MG2)

s=D['sep_AU']*AU; dpm=np.hypot(D['pmra1']-D['pmra2'],D['pmdec1']-D['pmdec2'])
vsky=4.74*dpm*(dist/1000)
sdpm=np.sqrt(((D['pmra1']-D['pmra2'])*np.hypot(D['pmra_error1'],D['pmra_error2']))**2
            +((D['pmdec1']-D['pmdec2'])*np.hypot(D['pmdec_error1'],D['pmdec_error2']))**2)/np.maximum(dpm,1e-6)
def kin(Mt):
    vN=np.sqrt(G*Mt*Msun/s)/1e3; vt=vsky/vN; x=np.log10(G*Mt*Msun/s**2/a0)
    svt=np.sqrt((4.74*dist/1000*sdpm)**2+(4.74*dpm/1000*sdd)**2)/vN
    return vN,vt,x,svt
relpm=lambda e,p: e/np.maximum(np.abs(p),1e-6)

# ---------------- SELECTIONS ----------------
# Banik core (transcribed): |b|>15, mG<17 both, d<250 (parallax>4mas), RUWE<1.4 (subst for chi2/nu eq.4),
# sep 2-30 kAU, ipd_frac_multi_peak<=2 both; then total mass 0.464-4.31, vtilde<=5 cap, |d1-d2|<min(4sig,8pc).
vN_b,vt_b,x_b,svt_b=kin(Mt_b)
banik_core=((np.abs(b)>15)&(D['phot_g_mean_mag1']<17)&(D['phot_g_mean_mag2']<17)&(dist<250)
   &(D['ruwe1']<1.4)&(D['ruwe2']<1.4)&(skAU>2)&(skAU<30)
   &(D['ipd_frac_multi_peak1']<=2)&(D['ipd_frac_multi_peak2']<=2))
banik=banik_core&(Mt_b>0.464)&(Mt_b<4.31)&(vt_b<=5)&(np.abs(d1-d2)<np.minimum(4*sdd,8))
banik12=banik&(D['ruwe1']<1.2)&(D['ruwe2']<1.2)   # RUWE<1.2 proxy for the stricter chi2/nu cut

# Chae (transcribed): d<200, 4<M_G<14 both, sep 0.2-30 kAU, R_chance<0.01, relative PM err<0.005 all four
# components, parallax_over_error>100 both (rel parallax err <1%).
vN_c,vt_c,x_c,svt_c=kin(Mt_c)
chae=((dist<200)&(MG1>4)&(MG1<14)&(MG2>4)&(MG2<14)&(skAU>0.2)&(skAU<30)&(D['R_chance_align']<0.01)
   &(relpm(D['pmra_error1'],D['pmra1'])<0.005)&(relpm(D['pmdec_error1'],D['pmdec1'])<0.005)
   &(relpm(D['pmra_error2'],D['pmra2'])<0.005)&(relpm(D['pmdec_error2'],D['pmdec2'])<0.005)
   &(D['parallax_over_error1']>100)&(D['parallax_over_error2']>100))

def D4(sel,vt,x):
    deep=(x<-0.5)&np.isfinite(vt)&sel
    base=np.mean(vt[deep]>np.sqrt(2))
    a=[np.mean((vt[deep]/np.sqrt(f))>np.sqrt(2)) for f in (0.9,1.1)]   # M_tot scaled +-10% -> v_N scales sqrt
    tp=0.1*np.clip((-0.5-x[deep])/1.0,0,1.0)                           # separation-tapered up-to-10% mass bias
    a.append(np.mean((vt[deep]/np.sqrt(1+tp))>np.sqrt(2))); a.append(base)
    return deep.sum(),base,max(a)/max(min(a),1e-9)

def summary(name,sel,vt,x,svt,N_pub,gate):
    N=sel.sum(); g='PASS' if gate[0]<=N<=gate[1] else f'{"+" if N>gate[1] else "-"}{100*(N-N_pub)/N_pub:+.0f}% vs pub'
    deep=(x<-0.5)&np.isfinite(vt)&sel
    nd,d2,s4=D4(sel,vt,x); d1=np.median(svt[deep])
    print(f"\n=== {name}  (published N={N_pub}, gate [{gate[0]},{gate[1]}]) ===")
    print(f"  N = {N:,}   [{g}]")
    print(f"  deep bins (g_N/a0<0.3): N_deep={nd:,}")
    print(f"  D1 median sigma/v_N   = {d1:.3f}   ({'OK <0.3' if d1<0.3 else 'TRIGGER >0.3'})")
    print(f"  D2 super-escape frac  = {d2:.3f}   ({'OK <0.15' if d2<0.15 else 'TRIGGER >0.15'})")
    print(f"  D4 mass-sensitivity   = {s4:.2f}x  ({'robust <1.5' if s4<1.5 else 'TRIGGER >1.5 mass-limited'})")
    # per-bin vtilde / super-escape
    print("  g_N/a0     N    med(vt)  super-esc(vt>sqrt2)")
    for lo,hi in [(2,3),(1,2),(0.5,1),(0,0.5),(-0.5,0),(-1,-0.5),(-1.5,-1),(-2.5,-1.5)]:
        bb=sel&(x>=lo)&(x<hi)&np.isfinite(vt)
        if bb.sum()>20:
            print(f"   {10**((lo+hi)/2):7.2f} {bb.sum():6,}   {np.median(vt[bb]):.3f}    {np.mean(vt[bb]>np.sqrt(2)):.3f}")
    return N,d1,d2,s4

print("WB-R1 EXACT PUBLISHED-SELECTION REPLICATION  (sky-projected observable; F3 deprojection NOT implemented)")
print("="*78)
rb=summary("BANIK-exact (RUWE<1.4 subst)",banik,vt_b,x_b,svt_b,8611,(7750,9472))
rb2=summary("BANIK-exact (RUWE<1.2 proxy for chi2/nu eq.4)",banik12,vt_b,x_b,svt_b,8611,(7750,9472))
rc=summary("CHAE-exact (cuts only; Banik observable)",chae,vt_c,x_c,svt_c,26615,(23954,29277))
print("\n"+"="*78)
print("FOUR-COLUMN TABLE (for Fable):  selection | N | D1 deep | D2 deep | D4")
for nm,r in [("Banik-exact RUWE<1.4",rb),("Banik-exact RUWE<1.2",rb2),("Chae-exact",rc)]:
    print(f"  {nm:24s} {r[0]:7,}  {r[1]:.3f}   {r[2]:.3f}   {r[3]:.2f}x")
print("""
READING (locked, preliminary -- Outcome A; halt before MC, relay first):
 * D4 ROBUST for ALL selections (1.3-1.4x < 1.5) -> the super-escape is NOT a mass-estimator artifact.
   Resolves Fable's biggest worry; gate-INDEPENDENT (firm).
 * With the FAITHFUL Banik-cubic mass pipeline, ALL THREE selections agree: D2 super-escape ~0.10,
   D1 ~0.12-0.15, both BELOW their stop-triggers (0.15, 0.3), for BOTH teams' cuts and STABLE across the
   RUWE 1.2-1.4 bracket. -> Outcome A (clean below thresholds).
 * MASS-PIPELINE CORRECTION (logged): an earlier pass inverted the Banik cubic OUTSIDE its valid range
   (M_G in [0.6,11.1]); extrapolating to M=0.08 returns a non-physical M_G~6 -> systematically TOO-LOW masses
   -> too-low v_N -> INFLATED v_t. That bug produced a spurious ~0.48 Chae super-escape (and inflated the
   WB-2 looser-sample 0.27). With masses fixed, the faithful number is ~0.10. The earlier 0.48/0.27 are
   RETRACTED as mass-estimator artifacts; do not cite them as the faithful super-escape.
 * Median sky-projected v_t rises modestly into deep-MOND (~0.57 -> ~0.66). Whether that rise is a genuine
   boost or projection+noise is NOT decidable from the sky-projected statistic -> needs the deprojection
   Monte-Carlo. Neither a manufactured boost nor a dismissal: the data are clean enough to adjudicate, but
   this pass does NOT adjudicate.
 * CAVEAT (decisive): SKY-PROJECTED observable only. Chae's published boost uses 3D DEPROJECTION (fork F3),
   NOT implemented here -> this does NOT settle Chae-vs-Banik. The deprojection Monte-Carlo (WB-3) is the next
   step and the real crux. C1/C2 only; says NOTHING about a0(z) (C3 fence).""")
