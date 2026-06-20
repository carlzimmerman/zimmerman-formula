"""
INDEPENDENT SKEPTIC CHECK of the clumpy_vs_smooth verdict.

I attack the verdict's escape hatch from BOTH sides:

(I)   RESCUE attempt for Carl: the sharpest pro-Carl configuration the banked
      scripts may UNDER-test. A real cluster has member galaxies all the way out
      to ~R200 (2-3 Mpc), NOT confined to the 420 kpc core. When we measure the
      residual INSIDE the core, the galaxies OUTSIDE the core still source a
      long-range 1/r deep-MOND field reaching INTO the core. Plus QUMOND is
      NONLINEAR: the cross-term nu(|g_gas + g_gal|) is not nu(g_gas)+nu(g_gal).
      Does the FULL discrete realization (galaxies to R200 + gas) give MORE core
      phantom than the smooth-baryon estimate that the standard calc uses?
      This is the steelman: the boundary does NOT enclose all baryons, so the
      enclosed-mass theorem does NOT directly apply -> Carl's effect has room.

(II)  BREAK attempt: is the sign of the QUMOND nonlinear cross-term such that a
      clumpy/external field ADDS or SUBTRACTS core phantom? Compute it directly.

Method: full 3D QUMOND on a grid large enough to hold R200, EXACT analytic
Newtonian field for gas (beta-model, spherical) + galaxies (softened points to
R200). Compare core (<420 kpc) phantom: discrete-galaxies-to-R200 vs the SAME
spherical M_gal(<r) smeared. a0=9.36e-11 (framework input).
"""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from two_body_subadditivity import G, Msun, kpc, a0, nu_simple, LocalGrid
from radial_and_intergalaxy import gradN_vectorized
from realistic_cluster_with_gas import beta_Menc, beta_grad

def log(*a): print(*a); sys.stdout.flush()

def main():
    log("="*80)
    log("SKEPTIC INDEPENDENT: galaxies to R200 (NOT core-confined) + gas, core phantom")
    log("="*80)
    R500=2100*kpc; R200=1.5*R500; Rcore=420*kpc
    Mgas500=1.0e14*Msun; fstar=0.18; Mstar_tot=fstar*Mgas500
    rc_gas=0.20*R500; beta_gas=0.65
    rho0_gas=Mgas500/beta_Menc(R500,1.0,rc_gas,beta_gas)
    Mgas_core=beta_Menc(Rcore,rho0_gas,rc_gas,beta_gas)

    # BIG grid to hold galaxies out to R200 (~3.15 Mpc); core measured at 420 kpc
    L=9000*kpc; n=200; soft=max(8*kpc, 1.5*L/n)
    grid=LocalGrid(L,n)
    log(f"R200={R200/kpc:.0f}kpc, Rcore={Rcore/kpc:.0f}kpc, grid L={L/kpc:.0f}kpc "
        f"n={n} cell={L/n/kpc:.1f}kpc soft={soft/kpc:.1f}kpc")
    log(f"gas Mgas(<R500)={Mgas500/Msun:.2e}, Mgas(<core)={Mgas_core/Msun:.3e}; "
        f"Mstar_tot={Mstar_tot/Msun:.2e}")

    gxg,gyg,gzg,Mgas_of_r = beta_grad(grid,rho0_gas,rc_gas,beta_gas)

    ratios=[]; deltas=[]; phDs=[]; phSs=[]
    NSEED=3
    for seed in range(NSEED):
        np.random.seed(100+seed)
        # ~200 member galaxies distributed NFW c=4 out to R200 (whole cluster)
        Ngal=200; rs=R500/4
        rgrid=np.linspace(5*kpc,R200,6000); x=rgrid/rs
        w=rgrid**2/(x*(1+x)**2); w/=w.sum()
        rg=np.random.choice(rgrid,Ngal,p=w)
        ct=np.random.uniform(-1,1,Ngal);ph=np.random.uniform(0,2*np.pi,Ngal)
        st=np.sqrt(1-ct**2)
        P=np.c_[rg*st*np.cos(ph),rg*st*np.sin(ph),rg*ct]; P[0]=0
        gm=np.random.gamma(1.2,1.0,Ngal); gm[0]=8.0
        gm*=Mstar_tot/gm.sum()
        masses=list(gm); pos=[tuple(p) for p in P]

        def core_phantom(mode):
            if mode=='discrete':
                gxs,gys,gzs=gradN_vectorized(grid,masses,pos,soft)
            else:
                rgal=np.sqrt((np.array(pos)**2).sum(1)); sr=np.argsort(rgal)
                rr=rgal[sr]; mm=np.array(masses)[sr]; cm=np.cumsum(mm)
                r=np.maximum(grid.r,0.5*grid.d)
                Mg=np.interp(r, rr, cm, left=0.0, right=cm[-1])
                g=G*Mg/r**2; gxs=g*grid.X/r; gys=g*grid.Y/r; gzs=g*grid.Z/r
            gx=gxg+gxs; gy=gyg+gys; gz=gzg+gzs
            gmag=np.sqrt(gx**2+gy**2+gz**2); nu=nu_simple(gmag/a0)
            S=grid.div(nu*gx,nu*gy,nu*gz); rho_app=S/(4*np.pi*G)
            return grid.Menc(rho_app,Rcore)/Msun

        Md=core_phantom('discrete'); Ms=core_phantom('smeared')
        # in-core baryon (same both ways): gas + stars within core
        rgal=np.sqrt((np.array(pos)**2).sum(1))
        Mstar_core=np.sum(np.array(masses)[rgal<Rcore])/Msun
        Mbar_core=Mgas_core/Msun+Mstar_core
        phD=Md-Mbar_core; phS=Ms-Mbar_core
        ratios.append(phD/phS); deltas.append(phD-phS); phDs.append(phD); phSs.append(phS)
        log(f"  seed {seed}: Mstar(<core)={Mstar_core:.3e}  ph_disc={phD:.4e}  "
            f"ph_smear={phS:.4e}  ratio={phD/phS:.4f}  d={phD-phS:+.3e}")

    ratios=np.array(ratios); deltas=np.array(deltas)
    log(f"\n  MEAN clumpy/smooth core-phantom ratio = {ratios.mean():.4f} "
        f"+/- {ratios.std():.4f}  (N={NSEED} seeds, galaxies to R200)")
    log(f"  MEAN delta = {deltas.mean():+.3e} Msun = "
        f"{100*deltas.mean()/1.357e14:+.2f}% of 1.357e14 residual target")
    log(f"  ratio>1 => Carl's collective ADD survives the steelman; <=1 => sub-additive null")

if __name__=="__main__":
    main()
