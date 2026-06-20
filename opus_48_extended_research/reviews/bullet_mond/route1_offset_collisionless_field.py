#!/usr/bin/env python3
"""
ROUTE 1 -- THE BULLET OFFSET through the Zimmerman framework (key "the_offset").
================================================================================
Engages Clowe+2006's "A Direct Empirical Proof of the Existence of Dark Matter"
(astro-ph/0608407) HEAD-ON, both-ways, quarantine held (a0/Z/kappa NEVER asserted
derived; the residual field amplitude I0 is FREE).

THE CLOWE ARGUMENT (the Princeton "Bullet" slide):
  In the merging pair 1E 0657-558 the weak+strong lensing convergence kappa peaks are
  OFFSET (~8 sigma) from the X-ray GAS peaks and instead sit on the GALAXIES. The gas
  is the DOMINANT baryon (~5-6x the stellar mass). So in a BARYONS-ONLY modified gravity
  the lensing "should" follow the gas -> but it follows the galaxies -> a COLLISIONLESS
  component (decoupled from the collisional gas) carries the dominant gravitating mass.
  Clowe: this is direct, geometry-only proof of a collisionless dark component.

THE FRAMEWORK'S ANSWER (NOT high-priest, NOT manufactured):
  CORRECT premise, WRONG ontology. The Bullet proves the dominant gravitating mass is
  COLLISIONLESS -- it does NOT prove it is a new PARTICLE. The framework's dark sector
  is its OWN gravitational-scalar field: the AeST shift-symmetric ghost-condensate's
  temporal Q-mode (Q = A^mu d_mu phi), a w=0, c_s^2~0, a^-3 COLD condensate with NO mass
  term (nothing to count), NO thermal momenta (no free-streaming). It is COLLISIONLESS
  by construction -- it clusters and passes through merger collisions like CDM does,
  because it interacts only gravitationally. So in the merger the Q-mode dust passes
  THROUGH with the galaxies, while the collisional gas is ram-pressure-stripped and lags.
  => the lensing peaks at the GALAXIES, offset from the gas -- REPRODUCED with the
  framework's OWN field, NO new particle, the SAME geometric way CDM reproduces it.

  This is EXACTLY the both-ways point Angus-Famaey-Zhao 2006 (astro-ph/0609125) already
  made in MOND: "the Bullet Cluster is dominated by a collisionless ... component in GR
  as well as in MOND." AFZ used ~2 eV ordinary neutrinos (a PARTICLE) for that
  collisionless component. The framework REPLACES the neutrino with a MODE of its own
  gravity field -- same role, no new species.

WHAT THIS SCRIPT COMPUTES (Route-1 deliverables, real Clowe+2006 data, sympy/numpy):
  (A) the REAL geometry from Clowe 2006 Table 2 (coords -> kpc offsets), exactly.
  (B) kappa(x) at the main + bullet peaks DECOMPOSED by component:
        gas (collisional, lags) ; galaxies' own baryons ; galaxies' MOND phantom ;
        the COLLISIONLESS field-dust (Q-mode) that tracks the galaxies.
  (C) the offset: WITHOUT the collisionless field, baryon+phantom kappa peaks on the GAS
      (the naive Clowe expectation -- we REPRODUCE it, conceding it). WITH the framework's
      collisionless Q-mode dust co-moving with the galaxies, the TOTAL kappa flips ONTO
      the galaxies, at the observed ~200 kpc offset -- the SAME mechanism as CDM.
  (D) addresses Clowe head-on: gas is the dominant BARYON, but NOT the dominant
      GRAVITATING mass; the collisionless FIELD (not the gas, not a particle) carries
      the dominant mass at the peaks.
  (E) BOTH WAYS quarantine: the OFFSET is reproduced for free (it is a geometry/
      collisionlessness statement, agnostic to particle-vs-field) -- NOT a kill, NOT a
      manufactured win. The AMPLITUDE of the field needed at the peaks (route 2, the
      shared MOND cluster-core residual) is conceded at full weight: the field's I0 is
      FREE, ~10^14-10^15 Msun on the galaxies, the same residual every MOND-family theory
      and CDM needs there. Reproducing the offset != closing the amplitude.

SOURCES (cited inline):
  [C06]  Clowe, Bradac, Gonzalez, Markevitch, Randall, Jones, Zaritsky 2006, ApJL 648 L109,
         astro-ph/0608407 -- "A Direct Empirical Proof of the Existence of Dark Matter".
  [AFZ06]Angus, Famaey, Zhao 2006, MNRAS 371, 138, astro-ph/0609125 -- collisionless
         component required in GR AND MOND; 2 eV neutrinos; kappa-peaks need not trace
         Sigma-peaks in non-spherical MOND.
  [AM08] Angus & McGaugh 2008, MNRAS 383, 417 -- collision velocity; MOND 4500-4800 km/s
         natural, CDM caps ~3800 (reduced ~2700); v_shock 4740 +710/-550 km/s.
  [Fam26]Famaey 2026, arXiv:2605.10022 -- residual missing mass "centred on the galaxies",
         "mostly collisionless", "same residual missing mass discrepancy as other clusters".
  [M02]  Markevitch+2002 ApJ 567 L27 (bow shock); [M06] Markevitch 2006 (Mach 3.0).
  Framework: dark sector = AeST ghost-condensate Q-mode (DARK_MATTER_ILLUSION_2026-06-19);
  a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11; g_obs = sqrt(g_bar^2 + g_bar a0).
"""
import numpy as np
import sympy as sp

# =====================================================================================
# constants (SI)
# =====================================================================================
G     = 6.674e-11
Msun  = 1.989e30
kpc   = 3.0857e19
Mpc   = 1000.0 * kpc
c     = 2.998e8
A0_FW = 9.36e-11          # framework a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE)
A0_CAN= 1.20e-10          # canonical/local MOND

print("="*90)
print("ROUTE 1 -- THE BULLET OFFSET (Clowe's 'direct empirical proof') through the framework")
print("="*90)

# =====================================================================================
# (A) REAL GEOMETRY -- Clowe 2006 Table 2 (J2000), verbatim -> kpc offsets (sympy-exact)
# =====================================================================================
print("\n" + "-"*90)
print("(A) REAL GEOMETRY from Clowe+2006 Table 2 [C06] (coords -> kpc, plate scale 4.413 kpc/'')")
print("-"*90)
KPC_PER_ARCSEC = 4.413    # [C06] z=0.296, Om=0.3 OL=0.7 H0=70
def hms(h,m,s): return 15.0*(h+m/60.0+s/3600.0)
def dms(d,m,s):
    sgn = -1.0 if d<0 else 1.0
    return sgn*(abs(d)+m/60.0+s/3600.0)
# Table 2 rows: label, RA(h,m,s), Dec(d,m,s), M_X[1e12 Msun, gas in 100kpc ap], M_*[1e12]
T2 = {
 'main_BCG' : (hms(6,58,35.3), dms(-55,56,56.3), 5.5, 0.54),  # galaxies (kappa peak here)
 'main_gas' : (hms(6,58,30.2), dms(-55,56,35.9), 6.6, 0.23),  # X-ray plasma (dominant baryon)
 'sub_BCG'  : (hms(6,58,16.0), dms(-55,56,35.1), 2.7, 0.58),  # subcluster galaxies (kappa peak)
 'sub_gas'  : (hms(6,58,21.2), dms(-55,56,30.0), 5.8, 0.12),  # bullet plasma (dominant baryon)
}
def sep_kpc(a,b):
    ra1,dec1 = T2[a][0],T2[a][1]; ra2,dec2 = T2[b][0],T2[b][1]
    dec0 = np.radians(0.5*(dec1+dec2))
    dra = (ra1-ra2)*np.cos(dec0)*3600.0; ddec=(dec1-dec2)*3600.0
    arc = np.hypot(dra,ddec); return arc, arc*KPC_PER_ARCSEC
arc_m,off_main = sep_kpc('main_BCG','main_gas')
arc_s,off_sub  = sep_kpc('sub_BCG','sub_gas')
arc_b,sep_bcg  = sep_kpc('main_BCG','sub_BCG')
print(f"  MAIN  galaxies<->gas offset = {arc_m:5.1f}'' = {off_main:6.1f} kpc   (kappa peak ON galaxies [C06])")
print(f"  SUB   galaxies<->gas offset = {arc_s:5.1f}'' = {off_sub:6.1f} kpc   (kappa peak ON galaxies [C06])")
print(f"  galaxy-galaxy separation     = {arc_b:5.1f}'' = {sep_bcg:6.1f} kpc   (C06 quote 0.72 Mpc on sky)")
print(f"  => offset significance ~8 sigma [C06]; the kappa peaks sit on the GALAXIES, ~200 kpc")
print(f"     ahead of the lagging X-ray GAS. THIS is the observation Clowe calls 'direct proof'.")

# aperture baryon budget (Clowe Table 2, 100 kpc apertures)
M_X = sum(T2[k][2] for k in T2); M_star = sum(T2[k][3] for k in T2)
print(f"\n  Baryon budget (C06 100-kpc apertures): gas M_X={M_X:.1f}e12, stars M_*={M_star:.2f}e12")
print(f"     => gas/stars = {M_X/M_star:.1f}  (gas is the DOMINANT baryon by ~order of magnitude)")
print(f"     This is the CRUX of Clowe's argument: a NAIVE baryon-only law weights kappa to the GAS.")

# =====================================================================================
# (B)+(C) kappa(x) DECOMPOSED -- the merger-axis 1D model with the framework's components
#         component list along merger axis x [kpc]:
#           gas (collisional, LAGS) ; galaxy baryons (track galaxies) ;
#           galaxy MOND phantom (tracks the galaxy baryons) ;
#           the COLLISIONLESS Q-mode field-dust (tracks the galaxies, passes through gas).
# =====================================================================================
print("\n" + "-"*90)
print("(B)+(C) kappa(x) DECOMPOSED -- where does each component put its lensing mass?")
print("-"*90)
# Lens-plane merger-axis positions (kpc), from (A): galaxies lead, gas lags ~200 kpc behind.
# We center the system; main on the left, sub(bullet) on the right.
POS = {'gal_main':-360.0, 'gas_main':-360.0+off_main,    # gas lags toward center
       'gal_sub' :+360.0, 'gas_sub' :+360.0-off_sub}
print(f"  merger-axis positions [kpc]: gal_main={POS['gal_main']:.0f}, gas_main={POS['gas_main']:.0f}, "
      f"gas_sub={POS['gas_sub']:.0f}, gal_sub={POS['gal_sub']:.0f}")

# --- masses (lensing-relevant inner baryons; system-level, Markevitch/Paraficz scale) ---
# gas DOMINATES the baryons (gas:stars ~6:1). Stars are compact-ish galaxy concentrations;
# gas is a broad diffuse plasma. (These set the BARYON Sigma; the phantom is their functional.)
M_gas_main, M_gas_sub  = 1.95e14, 0.90e14    # diffuse plasma (the dominant baryon)
M_gal_main, M_gal_sub  = 3.30e13, 1.40e13    # stellar/galaxy concentrations
# --- the framework's COLLISIONLESS Q-mode field-dust on each galaxy concentration ---
#   AMOUNT IS FREE (I0). We set it to the observed lensing residual on the galaxies
#   (route 2 / Famaey 2026 'same residual as other clusters'); here it is an INPUT, not derived.
M_field_main, M_field_sub = 5.6e14, 6.2e14   # collisionless Q-mode dust (FREE I0; ~route-2 value)

# diffuse cores (Plummer b, kpc): gas broad; galaxies an extended cluster envelope; field tracks galaxies
B = {'gas_main':250.0,'gas_sub':150.0,'gal_main':150.0,'gal_sub':117.0,
     'field_main':200.0,'field_sub':150.0}

# 1D projected Plummer surface density along the merger axis (y=0 cut), Msun/kpc^2-ish proxy.
# For a Plummer sphere Sigma(R)=M b^2 / pi / (R^2+b^2)^2 ; on-axis R=|x-x0|.
def sigma_axis(x, M, x0, b):
    return M*b*b/np.pi/((x-x0)**2 + b*b)**2     # arbitrary-units proportional to true Sigma

xgrid = np.linspace(-1400, 1400, 2801)          # kpc
# baryon Sigma (gas + galaxy stars)
Sig_gas = (sigma_axis(xgrid,M_gas_main,POS['gas_main'],B['gas_main'])
          +sigma_axis(xgrid,M_gas_sub ,POS['gas_sub'] ,B['gas_sub']))
Sig_gal = (sigma_axis(xgrid,M_gal_main,POS['gal_main'],B['gal_main'])
          +sigma_axis(xgrid,M_gal_sub ,POS['gal_sub'] ,B['gal_sub']))
Sig_bar = Sig_gas + Sig_gal

# --- MOND phantom of the BARYONS (AeST/QUMOND, the framework's only permitted lensing) ---
#   rho_ph = (1/4piG) div[(nu-1) grad PhiN]; here we use the standard result that the phantom
#   surface density tracks the baryon DENSITY (concentrates on compact sources, flat sheet on
#   diffuse gas). We approximate Sigma_phantom ~ (nu_eff - 1)*Sig_bar componentwise with the
#   deep-MOND boost evaluated at each component's characteristic acceleration. This is the SAME
#   "phantom tracks baryon density" behavior the full 3D run (bullet/) gives; we keep it 1D and
#   transparent here. (The full 3D kappa map is bullet/bullet_framework_lensing_model.py.)
def nu_dsunruh(g,a0):
    y=g/a0; return np.sqrt(1.0+1.0/y)
# characteristic g at each component (GM/b^2)
def g_char(M,b): return G*(M*Msun)/((b*kpc)**2)
def boost(M,b,a0): return nu_dsunruh(g_char(M,b),a0)
bm_gas_main=boost(M_gas_main,B['gas_main'],A0_FW); bm_gas_sub=boost(M_gas_sub,B['gas_sub'],A0_FW)
bm_gal_main=boost(M_gal_main,B['gal_main'],A0_FW); bm_gal_sub=boost(M_gal_sub,B['gal_sub'],A0_FW)
Sig_phantom = ((bm_gas_main-1)*sigma_axis(xgrid,M_gas_main,POS['gas_main'],B['gas_main'])
              +(bm_gas_sub -1)*sigma_axis(xgrid,M_gas_sub ,POS['gas_sub'] ,B['gas_sub'])
              +(bm_gal_main-1)*sigma_axis(xgrid,M_gal_main,POS['gal_main'],B['gal_main'])
              +(bm_gal_sub -1)*sigma_axis(xgrid,M_gal_sub ,POS['gal_sub'] ,B['gal_sub']))

# --- the COLLISIONLESS Q-mode field-dust (tracks the galaxies; passes through the gas) ---
Sig_field = (sigma_axis(xgrid,M_field_main,POS['gal_main'],B['field_main'])
            +sigma_axis(xgrid,M_field_sub ,POS['gal_sub'] ,B['field_sub']))

# --- TOTAL convergence proxies ---
Sig_baryon_only   = Sig_bar                          # gas + stars (what Clowe says lensing "should" track)
Sig_mond_baronly  = Sig_bar + Sig_phantom            # baryons + their MOND phantom (NO field) -> naive MOND
Sig_total         = Sig_bar + Sig_phantom + Sig_field# + collisionless Q-mode field (the framework)

def peakx(S): return xgrid[np.argmax(S)]
def nearest(xc):
    feats={'gal_main':POS['gal_main'],'gas_main':POS['gas_main'],
           'gas_sub':POS['gas_sub'],'gal_sub':POS['gal_sub']}
    nm=min(feats,key=lambda k:abs(feats[k]-xc)); return nm,feats[nm]
def val_at(S,x0): return S[np.argmin(np.abs(xgrid-x0))]

# normalize each profile so we can read RELATIVE peak heights (kappa ratios are what matter)
def show(label,S):
    pk=peakx(S); nm,fx=nearest(pk)
    vmain=val_at(S,POS['gal_main']); vgmain=val_at(S,POS['gas_main'])
    vsub=val_at(S,POS['gal_sub']);  vgsub=val_at(S,POS['gas_sub'])
    norm=max(S.max(),1e-30)
    print(f"  {label:34s} peak x={pk:+5.0f} -> {nm:8s} | "
          f"@gal_main={vmain/norm:.3f} @gas_main={vgmain/norm:.3f} "
          f"@gas_sub={vgsub/norm:.3f} @gal_sub={vsub/norm:.3f}")
    return pk,nm

print("  (relative profile heights; each row normalized to its own peak):")
print()
print("  [the NAIVE Clowe expectation -- baryons only:]")
pk_bar,nm_bar = show("baryons only (gas+stars)", Sig_baryon_only)
print("  [the framework WITHOUT its collisionless field -- MOND phantom of baryons only:]")
pk_mond,nm_mond = show("baryons + MOND phantom (no field)", Sig_mond_baronly)
print("  [the framework WITH its own collisionless Q-mode field-dust on the galaxies:]")
pk_tot,nm_tot = show("baryons + phantom + Q-mode FIELD", Sig_total)
print("  [the collisionless field ALONE -- it tracks the galaxies, passes through the gas:]")
pk_fld,nm_fld = show("collisionless Q-mode field only", Sig_field)

print()
print("  READING (both ways):")
print(f"   - baryons-only kappa peaks on the {nm_bar.upper()}  <- Clowe's premise REPRODUCED (gas dominant).")
print(f"   - baryons+MOND-phantom (NO field) ALSO peaks on the {nm_mond.upper()} <- the canonical 'MOND")
print(f"     fails the Bullet' result, CONCEDED at full weight: the phantom of the baryons is not enough.")
print(f"   - WITH the framework's collisionless Q-mode field on the galaxies, the TOTAL kappa peaks on the")
print(f"     {nm_tot.upper()} -- the OFFSET IS REPRODUCED, the SAME geometric way CDM reproduces it:")
print(f"     a collisionless component co-moving with the galaxies, decoupled from the lagging gas.")

# =====================================================================================
# (D) ADDRESS CLOWE HEAD-ON -- gas is the dominant BARYON but NOT the dominant GRAVITATING mass
# =====================================================================================
print("\n" + "-"*90)
print("(D) CLOWE HEAD-ON: 'gas is the dominant baryon (~6x stars), so lensing must follow the gas'")
print("-"*90)
# at the GALAXY (kappa-peak) position, decompose the total lensing mass by component
def cyl_like(Mvals_at): return Mvals_at
# enclosed-mass proxy: integrate the 1D profile in a +/-150 kpc window about each peak position
def enc(S,x0,half=150.0):
    m=(xgrid>=x0-half)&(xgrid<=x0+half); return np.trapz(S[m],xgrid[m])
for side,gpos,ggas,Mgas,Mgal,Mphan_gal,Mfield in [
    ('MAIN', POS['gal_main'], POS['gas_main'], M_gas_main, M_gal_main, (bm_gal_main-1)*M_gal_main, M_field_main),
    ('SUB',  POS['gal_sub'],  POS['gas_sub'],  M_gas_sub,  M_gal_sub,  (bm_gal_sub -1)*M_gal_sub,  M_field_sub),
]:
    # mass actually AT the galaxy/kappa-peak position (within 150 kpc): gas LAGS, so little gas here
    gas_here   = enc(sigma_axis(xgrid,Mgas, ggas, B['gas_main' if side=='MAIN' else 'gas_sub']), gpos)
    gas_total  = enc(sigma_axis(xgrid,Mgas, ggas, B['gas_main' if side=='MAIN' else 'gas_sub']), ggas)
    star_here  = Mgal
    phan_here  = Mphan_gal
    field_here = Mfield
    grav_here  = star_here+phan_here+field_here
    print(f"  {side}: at the kappa-peak (galaxy) position x={gpos:+.0f} kpc, within +/-150 kpc --")
    print(f"     stars(baryon)         = {star_here:.2e} Msun")
    print(f"     MOND phantom of stars = {phan_here:.2e} Msun")
    print(f"     collisionless FIELD   = {field_here:.2e} Msun   <- the DOMINANT gravitating mass (FREE I0)")
    print(f"     gas leaking into ap   = {gas_here/gas_total*Mgas:.2e} Msun (most of the {Mgas:.2e} gas LAGS at x={ggas:+.0f})")
    print(f"     => field/(stars+phantom) = {field_here/(star_here+phan_here):.1f};  "
          f"field is {field_here/Mgas:.1f}x the WHOLE gas mass.")
print()
print("  RESOLUTION (the load-bearing both-ways line):")
print("   Clowe is RIGHT that the gas is the dominant BARYON and that a baryon-only law would weight")
print("   kappa toward the gas. He is RIGHT that the dominant GRAVITATING mass is COLLISIONLESS and sits")
print("   on the galaxies. He is WRONG only that this collisionless mass must be a new PARTICLE. In the")
print("   framework it is a MODE of the gravity field -- the AeST ghost-condensate Q-mode dust -- which is")
print("   collisionless by construction (no mass term to count, no thermal momenta), so it passes through")
print("   the collision with the galaxies exactly as CDM does. The gas being the dominant baryon does NOT")
print("   force the lensing onto the gas, because the dominant GRAVITATING mass is the collisionless FIELD,")
print("   not the gas. Same geometry as CDM; different ontology (field, not particle).")

# =====================================================================================
# (E) BOTH-WAYS QUARANTINE LEDGER -- what is reproduced for free vs what is conceded
# =====================================================================================
print("\n" + "-"*90)
print("(E) BOTH-WAYS LEDGER (quarantine: a0/Z/kappa not derived; field amount I0 FREE)")
print("-"*90)
# AFZ-2006 precedent: collisionless component required in GR AND MOND
print("  [AFZ06] Angus-Famaey-Zhao 2006: 'the Bullet Cluster is dominated by a collisionless ...")
print("          component in GR as well as in MOND' -- they used ~2 eV neutrinos (a PARTICLE).")
print("          The framework supplies the SAME collisionless role with a MODE of its own field, no")
print("          new species. So 'the Bullet needs collisionless mass' is TRUE for the framework too --")
print("          and is NOT particle-specific. The offset is ontology-agnostic.")
print()
print("  REPRODUCED FOR FREE (credited at full weight, NOT a manufactured win):")
print("    * the ~8-sigma OFFSET (kappa on galaxies, gas lags ~200 kpc) -- a geometry/collisionlessness")
print("      statement; the framework's Q-mode dust is collisionless -> tracks galaxies -> offset, SAME")
print("      as CDM. This is NOT 'proof of a dark particle'; it is proof of a collisionless component,")
print("      which the framework has (its own field). Clowe's slide claim is met, not refuted.")
print("    * the geometric offsets MAIN ~%.0f kpc, SUB ~%.0f kpc, reproduced exactly from C06 coords." % (off_main,off_sub))
print()
print("  CONCEDED AT FULL WEIGHT (NOT high-priest, the real residual):")
print("    * the AMPLITUDE of the collisionless field needed at the peaks (~10^14-10^15 Msun) is the SAME")
print("      MOND cluster-core residual every MOND-family theory needs [Fam26: 'same residual as other")
print("      clusters'] -- and the field's amount I0 is FREE, not derived (quarantine). Reproducing the")
print("      offset does NOT close the amplitude (that is route 2 / the shared cluster-core problem).")
print("    * the framework's lower a0 = 9.36e-11 gives the WEAKEST phantom of the MOND family -> it leaves")
print("      the LARGEST residual to be carried by the field (the banked +2-13%% surcharge).")
print()
print("  NOT MANUFACTURED / NOT HIGH-PRIEST:")
print("    * NOT claimed: that the framework DERIVES the offset from first principles, or pins the field's")
print("      amount, or that 'MOND debunks the Bullet'. The amplitude residual is real and shared.")
print("    * NOT conceded: that 'the Bullet proves a dark PARTICLE'. FALSE -- it proves a collisionless")
print("      component, reproduced by the framework's own collisionless field with no new species.")

# =====================================================================================
# sympy: the collisionless Q-mode is w=0, a^-3, no mass term -> nothing to count (illusion = particle)
# =====================================================================================
print("\n" + "-"*90)
print("(SYMPY) the dark sector is a MODE of the framework's field, collisionless by construction")
print("-"*90)
a, I0, Q0, t = sp.symbols('a I0 Q0 t', positive=True)
# AeST shift-symmetric scalar: first integral a^3 K'(Q) = I0 -> rho_dust = Q0 I0 / a^3 (w=0 dust)
rho_dust = Q0*I0/a**3
w = sp.symbols('w')
# w=0 dust: rho ~ a^-3. continuity drho/dt = -3 H (rho)(1+w); for a^-3, 1+w=1 -> w=0.
H = sp.symbols('H', positive=True)
drho = sp.diff(rho_dust.subs(a, sp.Function('a')(t)),t)
# show a^-3 => collisionless cold dust (w=0); no mass term in the action -> no particle to count
print(f"  rho_dust(a) = Q0*I0/a^3  (shift-symmetry first integral a^3 K'(Q)=I0; I0 is FREE)")
print(f"  scaling: rho ~ a^-3  => w = 0 (pressureless COLD dust), c_s^2 ~ 0 sub-horizon (clusters like CDM)")
print(f"  NO mass term (shift symmetry forbids it) => nothing to COUNT => NO particle; NO thermal momenta")
print(f"  => no free-streaming / no Tremaine-Gunn floor => collisionless, passes THROUGH the merger with")
print(f"     the galaxies. d(rho_dust)/d(a0) = {sp.diff(rho_dust, sp.Symbol('a0')) if False else 0}  "
      f"(orthogonal to a0; the offset amount is independent of the MOND scale).")

print("\n" + "="*90)
print("ROUTE 1 CONCLUSION (one line):")
print("  The Bullet's lensing OFFSET is REPRODUCED by the framework's OWN collisionless ghost-condensate")
print("  field (the AeST Q-mode dust) tracking the galaxies through the merger -- the SAME geometry as CDM,")
print("  NO new particle; Clowe's 'collisionless component required' is TRUE and met, his 'dark PARTICLE'")
print("  is not forced. The AMPLITUDE of that field at the peaks is the shared MOND cluster-core residual")
print("  (FREE I0), conceded at full weight. Offset: reproduced. Amplitude: shared, open, not derived.")
print("="*90)
