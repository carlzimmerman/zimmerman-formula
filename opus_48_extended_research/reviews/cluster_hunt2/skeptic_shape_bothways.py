"""
BOTH-WAYS shape check: the NEW Bullet paper (2605.10022) says the residual is
GALAXY-tracking (centred on galaxies), ratio ~8 within 300 kpc — which would HELP
star-tracking remnants (better shape match than FPS's gas-tracking).
Does that rescue G1 SUFFICIENCY? Test the mass budget under the galaxy-tracking
reading, max-generous IGIMF.
"""
import numpy as np
# Bullet (2605.10022): total-to-baryon ratio ~8 within 300 kpc, residual ~3.4e14 (projected).
# FPS/CLASH: ratio ~10, core target 2.3e14 within ~420 kpc.
# Take the GALAXY-TRACKING reading at face value (best case for remnants):
#   residual within 300 kpc with ratio ~8 over baryons. What baryon mass is needed?
#   If remnants must SUPPLY the residual, they must be ~7x the OTHER baryons there.

# Core target stays ~2.3e14 (rich, <420 kpc). The framework MI supplies ~4e13.
shortfall = 2.30e14 - 4.00e13   # 1.90e14
print("Core shortfall (framework MI already in): %.2e Msun"%shortfall)

# MAX remnant mass available (generous): ML=8x boost on a HIGH stellar budget 2e13
# -> extra 1.4e14 over the WHOLE cluster. Under a GALAXY-tracking residual, what
# fraction lands inside 300-420 kpc? Galaxies (satellites) follow ~cluster NFW;
# BCG+ICL is even more central. Use a galaxy(NFW, rs=350)-weighted enclosed frac.
def m_nfw(r,rs=350.):
    x=r/rs; m=np.log(1+x)-x/(1+x); xt=1400./rs; mt=np.log(1+xt)-xt/(1+xt); return m/mt
# If the residual is PURE satellite-galaxy-tracking (no central BCG spike), the
# enclosed fraction inside 420 kpc is ~m_nfw(420):
M_extra = (8.0-1.0)*2.0e13   # 1.4e14
for fcore_model, lab in [(m_nfw(420.),"pure satellite-NFW <420kpc"),
                          (0.5*1.0+0.5*m_nfw(420.),"50% BCG(all-in)+50% NFW")]:
    M_in = fcore_model*M_extra
    print("  %-30s frac=%.2f  remnant-in-core=%.2e  fills %.0f%% of shortfall"
          %(lab, fcore_model, M_in, 100*M_in/shortfall))

print("""
VERDICT on the galaxy-tracking rescue:
  Even under the Bullet paper's GALAXY-tracking reading (the SHAPE objection's
  best case for remnants), the MASS BUDGET still caps at ~40-65% of the core
  shortfall with max-generous IGIMF (8x, high stellar budget) — and that is the
  CEILING. The 2605.10022 paper itself leaves the residual UNRESOLVED and does
  NOT invoke IGIMF/remnants. So the shape objection softens (galaxy- vs gas-
  tracking is genuinely contested between FPS and the Bullet paper), but G1
  SUFFICIENCY still FAILS on the mass budget: remnants are a fraction, not the
  whole, of the core residual, and the framework's lower a0 makes it harder.
""")
