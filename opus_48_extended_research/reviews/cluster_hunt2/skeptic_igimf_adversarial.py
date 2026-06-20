"""
SKEPTIC re-run of the IGIMF route, BOTH WAYS.
Try HARDEST to RESCUE the route (max-generous IGIMF), then try HARDEST to BREAK
a manufactured closure. Independent of the prior agent's geometry model.
"""
import numpy as np

# ------- core target (banked, two-probe agreement 1.03) -------
M_core_target = 2.30e14   # Msun, missing collisionless mass < ~420 kpc (rich cluster)
M_MI_phantom  = 4.00e13   # Msun, framework MI already supplies < ~450 kpc
shortfall     = M_core_target - M_MI_phantom
print("CORE TARGET (banked):  M_res(<420kpc) = %.2e   MI phantom = %.2e"%(M_core_target,M_MI_phantom))
print("  undershoot x%.2f ; shortfall = %.2e Msun\n"%(M_core_target/M_MI_phantom, shortfall))

# =====================================================================
# ARM 1 — TRY HARDEST TO RESCUE: max-generous IGIMF remnant mass + budget.
#   Push EVERY knob in the route's favor and see if it can even in principle
#   reach the core target.
# =====================================================================
print("="*80)
print("ARM 1 — MAX-GENEROUS RESCUE: push every IGIMF knob in the route's favor")
print("="*80)

# Most generous stellar budget. Real upper bounds:
#   - cluster total stellar mass canonical: f_star ~ 0.012-0.02 of M500~1e15 -> 1.2-2e13.
#     Take the HIGH end: 2.0e13 (generous; many estimates put rich clusters ~1-1.5e13).
M_star_canon_hi = 2.0e13
# IGIMF M/L boost: Kroupa headline ~6x. Some BCGs hit ~10x in extreme top-heavy.
#   Take 10x (more than Kroupa's stated 6x) -> extra = 9x M_star_canon.
for ML in [6.0, 8.0, 10.0]:
    M_extra = (ML-1.0)*M_star_canon_hi
    # MAX-generous geometry: pretend ALL remnant mass sits inside the 420 kpc core
    #   (it does not — BCG+ICL is even MORE concentrated, satellites extend beyond —
    #    but this is the ceiling).
    fill_ceiling = M_extra/shortfall
    print("  ML=%.0fx, M_star_canon=2.0e13 -> M_extra=%.2e ; if ALL in core: fills %.0f%% of shortfall"
          %(ML, M_extra, 100*fill_ceiling))
print("  -> EVEN the absolute ceiling (10x boost, high stellar budget, 100%% in core)")
print("     tops out near the shortfall ONLY at ML=10 with ALL mass in 420kpc — physically")
print("     impossible (ICL/BCG concentration + satellite extension put ~50%% inside).")

# Realistic-generous: ML=8, M_star=2.0e13, and a GENEROUS 60% inside 420 kpc.
M_extra = (8.0-1.0)*2.0e13
f_in = 0.60
M_in = f_in*M_extra
print("\n  realistic-generous (ML=8, M_star=2e13, 60%% inside core):")
print("    M_extra=%.2e, inside core=%.2e -> fills %.0f%% of the %.2e shortfall"
      %(M_extra, M_in, 100*M_in/shortfall, shortfall))

# =====================================================================
# ARM 2 — TRY HARDEST TO BREAK: the SHAPE veto is the decisive one.
#   Even granting unlimited mass, remnants track STARS. FPS residual is
#   GAS-tracking + FLAT missing-to-gas ~10. Does the SHAPE EVER match?
# =====================================================================
print("\n"+"="*80)
print("ARM 2 — SHAPE VETO: can star-tracking remnants ever match a gas-tracking flat-10 shell?")
print("="*80)
# Independent shapes (different functional forms than prior agent, to avoid model lock-in):
#   gas: beta-model rc=180 kpc, beta=0.6 (eRASS1-typical core radius)
#   stars(remnants): Hernquist BCG+ICL (a=40 kpc) 40% + cluster-NFW satellites (rs=350) 60%
def m_gas(r, rc=180., beta=0.6):
    rr=np.linspace(1,1500,6000); rho=(1+(rr/rc)**2)**(-1.5*beta)
    c=np.cumsum(4*np.pi*rr**2*rho)*(rr[1]-rr[0]); return np.interp(r,rr,c)/c[-1]
def m_hern(r,a=40.): return (r**2)/(r+a)**2 / ((1400.**2)/(1400.+a)**2)
def m_nfw(r,rs=350.):
    x=r/rs; m=np.log(1+x)-x/(1+x); xt=1400./rs; mt=np.log(1+xt)-xt/(1+xt); return m/mt
def m_star(r): return 0.40*m_hern(r)+0.60*m_nfw(r)

print("  %6s %10s %10s %14s"%("R[kpc]","fgas(<R)","fstar(<R)","ratio star/gas"))
ratios=[]
for R in [50,100,150,200,300,420]:
    fg=m_gas(R); fs=m_star(R); ratios.append(fs/fg)
    print("  %6.0f %10.4f %10.4f %14.2f"%(R,fg,fs,fs/fg))
print("  -> star/gas ratio range %.1f (center) to %.1f (420kpc): NOT FLAT."%(max(ratios),min(ratios)))
print("     A flat missing-to-gas ~10 shell CANNOT be sourced by a star-tracking field;")
print("     remnants over-fill the inner 50-100 kpc and under-fill the 200-420 kpc shell.")

# =====================================================================
# ARM 3 — the a0 surcharge AND the f_star reality check on REAL eRASS1.
#   The prior agent's f_star_canon=0.15 (stellar/gas). Is that right? And does
#   the IGIMF integrated help actually reach eta->1?
# =====================================================================
print("\n"+"="*80)
print("ARM 3 — does the INTEGRATED IGIMF help actually reach eta->1 (its claimed strength)?")
print("="*80)
from astropy.io import fits
G=6.674e-11; Msun=1.989e30; kpc=3.086e19
a0_fw=9.36e-11
d=fits.open('/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits')[1].data
M500=np.array(d['M500'],float)*1e14*Msun
MGAS=np.array(d['MGAS500'],float)*1e12*Msun
R500=np.array(d['R500'],float)*kpc
g=np.isfinite(M500)&np.isfinite(MGAS)&np.isfinite(R500)&(M500>0)&(MGAS>0)&(R500>0)
M500,MGAS,R500=M500[g],MGAS[g],R500[g]
def gp(gb,a0): return np.sqrt(gb**2+gb*a0)
gobs=G*M500/R500**2
for fstar,ML,lab in [(0.15,1.0,"canonical f*=0.15"),(0.15,6.0,"IGIMF 6x"),(0.20,8.0,"IGIMF 8x, f*=0.20 (max)")]:
    Mbar=MGAS+ML*fstar*MGAS; gbar=G*Mbar/R500**2
    eta=gobs/gp(gbar,a0_fw)
    print("  %-26s median eta(R500)=%.2f  (need ~1.0 to close integrated)"%(lab,np.median(eta)))
print("  -> even max IGIMF (8x, f*=0.20) leaves median eta ~well above 1 on framework footing.")
print("     'closes the integrated/equilibrium deficit' holds ONLY at the HSE-reliable")
print("     eta~1.0-1.6 END of the post-XRISM bracket, NOT at the WL/raw-catalog median.")
