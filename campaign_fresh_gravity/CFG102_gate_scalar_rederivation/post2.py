"""POST-HOC (not in the frozen doc; labelled as such): why is the Sun potential so different from a slaved chi0 = t estimate?
(a) inner-boundary sensitivity: restrict the domain to r >= r0 (Dirichlet chi = t), r0 in {1, 2, 4} kpc, (b) the slaved evaluation mu lap t at the same mu,
(c) the local ratio lap(chi0)/lap(t) at 8 kpc."""
from cfg102_common import *
GS=cost_setup(SUN[0],SUN[1],SUN[2])
def cut(Gd, r0):
    m = Gd.r >= r0*KPC
    return Grid({k:(v[m] if isinstance(v,np.ndarray) and v.shape==Gd.r.shape else v) for k,v in Gd.tr.items()})
for m2,mu in ((1e-12,1.4736e28),(1e-10,3.8e28)):
    print(f"m2={m2:.0e} mu={mu:.4e}")
    ph_inf=phi_inf(GS,mu); print("   slaved (chi0=t) Sun:", sun_cost(GS,ph_inf))
    for r0 in (1,2,4,8/2):
        Gd=cut(GS,r0)
        for free in (False,True):
            chi,info=solve_chi0(Gd,mu,m2,free=free)
            ph=phi_chi(Gd,info,m2)
            print(f"   r0={r0} kpc {'Neumann ' if free else 'Dirichlet'}: Sun {sun_cost(Gd,ph):+.4g} conv {info['converged']}")
