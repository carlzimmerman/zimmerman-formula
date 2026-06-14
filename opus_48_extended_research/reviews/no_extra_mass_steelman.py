#!/usr/bin/env python3
"""
STEELMAN forensic: can clusters avoid a second mass component? -- on real eRASS1.
=================================================================================
Carl's hypothesis: the eta~2 cluster deficit is a methodology/footing artifact,
NOT evidence for a second (dark) mass component. We give that its STRONGEST honest
defense and report where it runs out. Reducers/inflaters applied to the REAL eRASS1
(Bulbul+2024) clean sample (N=9830, WL-calibrated M500), framework a0=9.36e-11 + the
framework's own dS-Unruh interpolation g_obs=sqrt(gbar^2 + gbar a0).

eta == M_dyn / M_MOND-predicted at R500  (= 1 means no second component needed).
In deep MOND, M_MOND-pred ~ sqrt(M_bar) * const, so M_eff ~ sqrt(a0 * M_bar) and
eta scales as 1/sqrt(a0 * M_bar) at fixed M_dyn -> doubling baryons cuts eta by sqrt(2).

KEY PROVENANCE FACT (verified against Bulbul+2024 / Ghirardini+2024 / Kleinebreil+2024):
  eRASS1 M500 is a WEAK-LENSING-calibrated mass (count-rate<->mass<->shear scaling),
  NOT a hydrostatic mass. So the M_dyn here is already the true (lensing) mass:
  a 'hydrostatic-bias' correction does NOT reduce eta on THIS catalog (it would only
  help analyses that start from hydrostatic mass, e.g. Zhang+2026 / Brownstein-Moffat).
"""
import numpy as np
from astropy.io import fits

c, G, Msun, kpc, Mpc = 2.99792458e8, 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
H0 = 2.184e-18                       # 67.4 km/s/Mpc
Om, OmL, Ob = 0.315, 0.685, 0.0493
RHO_CRIT0 = 3*H0**2/(8*np.pi*G)
A0_FRAME = 0.5*c*np.sqrt(G*OmL*RHO_CRIT0)   # 9.36e-11  (pure dark-energy footing)
A0_MOND  = 1.2e-10
FB_COSMIC = Ob/Om                            # 0.1565 cosmic baryon fraction

FITS = "/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/data/erass1cl_primary_v3.2.fits"

# framework's OWN interpolation: g_obs = sqrt(gbar^2 + gbar a0) -> nu = sqrt(1 + 1/y), y=gbar/a0
def nu_frame(y): return np.sqrt(1.0 + 1.0/y)
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1.0/y)   # for cross-check

def load(fstar=0.20, fgas_lo=0.01, fgas_hi=0.30, zmax=1.0):
    d = fits.open(FITS)[1].data
    f = lambda col: np.array([float(v) if str(v).strip() not in ("","--") else np.nan for v in d[col]], float)
    z,M500,Mgas,fgas,R500 = f("BEST_Z"),f("M500"),f("MGAS500"),f("FGAS500"),f("R500")
    M500H,M500L = f("M500_H"),f("M500_L")
    ok = ((z>0)&(z<zmax)&np.isfinite(z)&(M500>0)&(Mgas>0)&(R500>0)&(fgas>fgas_lo)&(fgas<fgas_hi))
    M500_kg = M500[ok]*1e13*Msun
    Mgas_kg = Mgas[ok]*1e11*Msun
    R_m = R500[ok]*kpc
    eM = np.clip(np.nan_to_num((M500H[ok]-M500L[ok])/(2*np.maximum(M500[ok],1e-6)),nan=0.25),0.05,1.0)
    return dict(z=z[ok],M500=M500[ok],Mgas_kg=Mgas_kg,M500_kg=M500_kg,fgas=fgas[ok],
                R_m=R_m,eM=eM,N=int(ok.sum()))

def eta_of(M500_kg, Mbar_kg, R_m, a0, nu):
    gobs = G*M500_kg/R_m**2
    gbar = G*Mbar_kg/R_m**2
    y = gbar/a0
    return gobs/(nu(y)*gbar)

def stat(eta): return np.median(eta), 10**np.mean(np.log10(eta)), np.percentile(eta,[25,75])

b = load()
print("="*100)
print("STEELMAN: do clusters need a SECOND mass component?  eRASS1 N=%d, a0_frame=%.3e, frame interp"%(b["N"],A0_FRAME))
print("="*100)

# ---- 0. Banked baseline (framework a0, framework interp, ICM gas + fstar=0.2 stars) ----
Mbar0 = (1+0.20)*b["Mgas_kg"]
e0 = eta_of(b["M500_kg"], Mbar0, b["R_m"], A0_FRAME, nu_frame)
m,gm,q = stat(e0)
print("\n0. BANKED BASELINE (a0_frame, frame interp, gas + 0.20*gas stars):  eta med=%.3f geomean=%.3f [%.2f,%.2f]"%(m,gm,q[0],q[1]))
print("   median fgas(=Mgas/M500)=%.4f   vs cosmic fb=%.4f -> ICM is %.0f%% of cosmic baryons"
      %(np.median(b["fgas"]), FB_COSMIC, 100*np.median(b["fgas"])/FB_COSMIC))

# ---- REDUCERS (each applied alone, then stacked) ----
print("\n--- REDUCERS (each ALONE vs the baseline above), framework a0 ---")
rows = []

# R1: framework a0 already (vs McGaugh 1.2e-10 which is an INFLATER of eta -- lower a0 -> higher eta)
eMcG = eta_of(b["M500_kg"], Mbar0, b["R_m"], A0_MOND, nu_frame)
print("  [a0 footing] McGaugh a0=1.2e-10 -> eta med=%.3f ; framework a0=9.36e-11 -> %.3f"
      %(np.median(eMcG), m))
print("               => the framework a0 is an INFLATER vs McGaugh: lower a0 RAISES eta by sqrt(1.2/0.936)=%.3f"%np.sqrt(A0_MOND/A0_FRAME))

# R2: IGIMF stellar remnants (Zhang+2026): ICM-only baryons are 52% of M_dyn; +stars/remnants/ICL -> 88%.
#     i.e. their total-baryon/ICM ratio = 88/52 = 1.69x the ICM mass.  Apply that multiplier to OUR ICM gas.
igimf_mult = 88.0/52.0     # 1.692
Mbar_igimf = igimf_mult * b["Mgas_kg"]
e_igimf = eta_of(b["M500_kg"], Mbar_igimf, b["R_m"], A0_FRAME, nu_frame)
print("  [R2 IGIMF stars+remnants, Zhang+2026 88/52=%.2fx ICM]                eta med=%.3f"%(igimf_mult, np.median(e_igimf)))

# R3: full cosmic baryon budget within R500 (cap baryons at fb_cosmic*M500) -- an UPPER bound on baryons
Mbar_cosmic = FB_COSMIC * b["M500_kg"]
e_cosmic = eta_of(b["M500_kg"], Mbar_cosmic, b["R_m"], A0_FRAME, nu_frame)
print("  [R3 FULL cosmic fb=%.3f * M500 (upper bound on baryons)]            eta med=%.3f"%(FB_COSMIC, np.median(e_cosmic)))

# R4: clumping / missing-gas: assume true gas is 1.15x the inferred (clumping bias ~10-20% on gas mass)
Mbar_clump = 1.15*(1+0.20)*b["Mgas_kg"]
e_clump = eta_of(b["M500_kg"], Mbar_clump, b["R_m"], A0_FRAME, nu_frame)
print("  [R4 gas clumping +15%% on Mgas]                                      eta med=%.3f"%np.median(e_clump))

# R5: non-equilibrium / merger boost -- on a WL mass this does NOT help (WL doesn't assume equilibrium).
#     We note it but do not credit it (M_dyn is WL, not hydrostatic).

# ---- STACKED STEELMAN (defensible, non-cherry-picked): IGIMF baryons + clumping, framework a0 ----
Mbar_steel = 1.15*igimf_mult*b["Mgas_kg"]
e_steel = eta_of(b["M500_kg"], Mbar_steel, b["R_m"], A0_FRAME, nu_frame)
ms,gms,qs = stat(e_steel)
print("\n--- STACKED STEELMAN (IGIMF 1.69x ICM + 15%% clumping, framework a0, frame interp) ---")
print("   eta med=%.3f geomean=%.3f [%.2f,%.2f]   (resulting baryon fraction med=%.3f vs cosmic %.3f)"
      %(ms,gms,qs[0],qs[1], np.median(Mbar_steel/b["M500_kg"]), FB_COSMIC))

# steelman but CAPPED at cosmic (can't have more baryons than cosmic fb within R500)
Mbar_steel_cap = np.minimum(Mbar_steel, FB_COSMIC*b["M500_kg"])
e_steel_cap = eta_of(b["M500_kg"], Mbar_steel_cap, b["R_m"], A0_FRAME, nu_frame)
mc,gmc,qc = stat(e_steel_cap)
print("   same but baryons CAPPED at cosmic fb (physical ceiling): eta med=%.3f geomean=%.3f"%(mc,gmc))

# McGaugh a0 version of the capped steelman (regular-MOND baseline, to show convention spread)
e_steel_cap_McG = eta_of(b["M500_kg"], Mbar_steel_cap, b["R_m"], A0_MOND, nu_frame)
print("   same capped steelman but McGaugh a0=1.2e-10:              eta med=%.3f"%np.median(e_steel_cap_McG))

# ---- absolute floor: if ALL baryons were exactly cosmic fb (the most generous physical case) ----
print("\n--- ABSOLUTE PHYSICAL FLOOR: baryons = cosmic fb (no second component possible beyond this) ---")
for a0,lab in ((A0_FRAME,"frame 9.36e-11"),(A0_MOND,"McGaugh 1.2e-10")):
    e = eta_of(b["M500_kg"], FB_COSMIC*b["M500_kg"], b["R_m"], a0, nu_frame)
    print("   baryons=cosmic fb, a0=%s -> eta med=%.3f geomean=%.3f"%(lab, np.median(e), 10**np.mean(np.log10(e))))

# ---- mass trend of the residual (does the steelman work better for massive clusters?) ----
print("\n--- steelman eta vs M500 (massive clusters have fgas closer to cosmic) ---")
M = b["M500"]; edges = np.percentile(M,[0,50,80,95,100])
for i in range(len(edges)-1):
    sel=(M>=edges[i])&(M<edges[i+1] if i<len(edges)-2 else M<=edges[i+1])
    print("   M500 %.1f-%.1f [1e13] N=%4d: baseline eta=%.2f  steelman-capped eta=%.2f"
          %(edges[i],edges[i+1],sel.sum(),np.median(e0[sel]),np.median(e_steel_cap[sel])))

# ---- how much baryon (or a0) would eta=1 require? ----
print("\n--- what eta=1 would require ---")
print("   baseline eta_med=%.2f -> need baryons x %.2f (M_MOND~sqrt(Mbar)) i.e. baryon fraction %.3f (cosmic=%.3f)"
      %(m, m**2, m**2*np.median(b["fgas"])*1.2, FB_COSMIC))
print("   steelman-capped eta_med=%.2f -> residual second-component fraction = 1 - 1/eta^2 = %.0f%% of M_dyn"
      %(mc, 100*(1-1/mc**2)))
print("="*100)
