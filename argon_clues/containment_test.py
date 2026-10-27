import json, math, numpy as np
from scipy.stats import spearmanr
from scipy.optimize import brentq
rows = json.load(open('../campaign_fresh_gravity/CFG624_no_cold_energy/cfg624_static_results.json'))["G2"]["rows"]
G=6.6743e-11; Ms=1.98847e30; kpc=3.0857e19
H0=67.4e3/3.0857e22; rho_c=3*H0**2/(8*math.pi*G)
m=lambda x: math.log(1+x)-x/(1+x)
def nfw_r200(Mhse, rap=1000*kpc):
    # solve M200 such that NFW(c(M200)) enclosed mass at rap equals Mhse (Duffy-like c = 5.71 (M/2e12 Msun h^-1)^-0.084, h=0.674)
    def f(lM):
        M200=10**lM*Ms; r200=(3*M200/(4*math.pi*200*rho_c))**(1/3); c=5.71*(M200/Ms/(2e12/0.674))**-0.084
        return M200*m(c*rap/r200)/m(c)-Mhse*Ms*0+ -Mhse
    lM=brentq(lambda l: f(l), 13.0, 16.0)
    M200=10**lM*Ms; r200=(3*M200/(4*math.pi*200*rho_c))**(1/3); c=5.71*(M200/Ms/(2e12/0.674))**-0.084
    return M200/Ms, r200/kpc, c
for foot in ('canonical','alt'):
    pc = rows[foot+'|nu_mono']['per_cluster']
    resid = np.array([c['resid_Mb'] for c in pc]); fr = np.array([c['frac_R500'] for c in pc])
    print('== %s: resid median %.2f range %.2f-%.2f'%(foot,np.median(resid),resid.min(),resid.max()))
    for R0 in (4.80,5.364):
        for f in (0.85,0.95):
            eps = resid/(f*R0); print('  T1 R0=%.3f f=%.2f: median eps %.3f max %.3f (n>1: %d)'%(R0,f,np.median(eps),eps.max(),(eps>1).sum()))
    rho,p = spearmanr(resid, fr); print('  T2 Spearman(resid, frac_R500) = %.2f (p %.2f)'%(rho,p))
    print('  T3 NFW containment: NOT RUN (superseded: CFG432 already measured the radial shape of the unsettled mass on the same 12 clusters)')
    eps_m = resid/(0.08*4.80)
    print('  MUTATION f_hot=0.08: median eps %.1f (>1 -> T1 fails as required)'%np.median(eps_m))
