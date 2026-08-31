#!/usr/bin/env python3
"""phase10_constraints.py -- observational-constraint overlay at benchmark P1.
Confirms FC-KH PASSES GW170817, solar-PPN alpha1, 1PN strong-coupling floor, G_N/G_C ~ 1,
so the KILL is a purely INTERNAL (transition-stability) failure, not an observational one."""
import numpy as np
def overlay(alpha,beta,lam,G=1.0):
    cT2=1/(1-beta); a1=4*(alpha-2*beta)/(beta-1)
    GN=2*G/(2-alpha); GC=2*G/(2+beta+3*lam)
    return dict(cT2=cT2, cT_minus_1=np.sqrt(cT2)-1, alpha1=a1, GN=GN, GC=GC, GN_over_GC=GN/GC,
                beta_plus_lam=beta+lam)
for name,(al,be,la) in [('P1 benchmark',(2e-15,1e-15,1e-3)),
                        ('small-lambda',(2e-15,1e-15,1e-7)),
                        ('large-lambda',(2e-14,1e-14,1e-1))]:
    d=overlay(al,be,la)
    print(f"\n{name}: (alpha,beta,lambda)=({al:.0e},{be:.0e},{la:.0e})")
    print(f"  c_T-1        = {d['cT_minus_1']:+.2e}   (GW170817 |c_T-1|<~1e-15) -> {'PASS' if abs(d['cT_minus_1'])<1e-15 else 'CHECK'}")
    print(f"  alpha1_PPN   = {d['alpha1']:+.2e}   (solar |alpha1|<~1e-5)     -> {'PASS' if abs(d['alpha1'])<1e-5 else 'FAIL'}")
    print(f"  beta+lambda  = {d['beta_plus_lam']:.2e}   (BB 1PN floor >~2.5e-7)   -> {'PASS' if d['beta_plus_lam']>2.5e-7 else 'FAIL'}")
    print(f"  G_N/G_C      = {d['GN_over_GC']:.6f}  (~1)")
print("\n=> FC-KH v1.0 (alpha=2beta) passes GW/PPN/1PN gates. The failure is INTERNAL:")
print("   the radial khronon gradient speed c_par^2<0 through the MOND transition (see PASS_KILL.md).")
# growth timescale at central worst point y0~2, |c_par^2|~4e-3, k~1/kpc
kpc=3.086e19; c=3e8; yr=3.15e7
for cc,kk_desc,kk in [(4.2e-3,'k~1/kpc',1/kpc),(4.2e-3,'k~1/(100pc)',1/(kpc/10))]:
    gamma=np.sqrt(cc)*c*kk; tau=1/gamma/yr
    print(f"   central y0~2 |c_par^2|={cc:.1e}, {kk_desc}: growth time tau ~ {tau:.1e} yr")
