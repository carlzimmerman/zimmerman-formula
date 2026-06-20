"""
Both-ways probe of Carl's collective EFE (efficient + flushed).

Compares, at a sequence of integration radii that CUT THROUGH the clump distribution:
  - CLUMPY total phantom inside R: 300 discrete galaxies (exact analytic Newtonian
    field) + QUMOND on a grid.
  - SMOOTH total phantom inside R: the SAME spherical M_bar(<r) as the clumps, via the
    EXACT spherical QUMOND formula M_app(<r)=nu(g_N/a0) g_N r^2/G (no grid needed).

Also reports the sign of the inter-galaxy phantom density (Milgrom-1986 negative-phantom
test) sampled at the midpoints between neighbouring clumps.

EXACT analytic Newtonian field (no grid mass loss). Vectorized over clumps. Flushed.
"""
import numpy as np, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from two_body_subadditivity import G, Msun, kpc, a0, nu_simple, LocalGrid

def log(*a): print(*a); sys.stdout.flush()

def gradN_vectorized(grid, masses, pos, soft):
    masses=np.asarray(masses); pos=np.asarray(pos)
    gx=np.zeros_like(grid.X);gy=np.zeros_like(grid.X);gz=np.zeros_like(grid.X)
    for m,(x0,y0,z0) in zip(masses,pos):
        dx=grid.X-x0;dy=grid.Y-y0;dz=grid.Z-z0
        rr2=dx*dx+dy*dy+dz*dz+soft**2; rr=np.sqrt(rr2)
        f=G*m/(rr2*rr); gx+=f*dx;gy+=f*dy;gz+=f*dz
    return gx,gy,gz

def clumpy_Mapp_radial(grid, masses, pos, soft, Rlist):
    gx,gy,gz=gradN_vectorized(grid,masses,pos,soft)
    gmag=np.sqrt(gx**2+gy**2+gz**2); nu=nu_simple(gmag/a0)
    S=grid.div(nu*gx,nu*gy,nu*gz); rho_app=S/(4*np.pi*G)
    out=[]
    for R in Rlist:
        Mapp=grid.Menc(rho_app,R)/Msun
        Mbar=np.sum([m for m,p in zip(masses,pos) if np.linalg.norm(p)<R])/Msun
        out.append((R,Mapp,Mbar))
    return out, rho_app

def smooth_Mapp_spherical(Mbar_of_R, Rlist):
    """EXACT spherical QUMOND: M_app(<R)=nu(gN/a0) gN R^2/G, gN=G Mbar(<R)/R^2."""
    out=[]
    for R in Rlist:
        Mb=Mbar_of_R(R)
        gN=G*Mb/R**2
        Mapp=nu_simple(gN/a0)*gN*R**2/G
        out.append((R,Mapp/Msun,Mb/Msun))
    return out

def main():
    log("="*78)
    log("CLUMPY-vs-SMOOTH total phantom inside radii that CUT the distribution")
    log("(smooth = identical spherical M_bar(<r); both at framework a0=9.36e-11)")
    log("="*78)
    M_tot=1e13*Msun; D=200*kpc; soft=15*kpc
    L=4000*kpc; n=240; soft=max(soft,1.5*L/n)
    rM=np.sqrt(G*M_tot/a0)
    log(f"M_tot={M_tot/Msun:.2e}, clumps within sphere r<{D/kpc:.0f}kpc, r_M={rM/kpc:.0f}kpc, "
        f"cell={L/n/kpc:.1f}kpc, soft={soft/kpc:.1f}kpc")
    grid=LocalGrid(L,n)
    np.random.seed(7)
    Nc=300
    p=np.random.uniform(-D,D,(Nc*3,3)); rr=np.sqrt((p**2).sum(1)); p=p[rr<D][:Nc]; p-=p.mean(0)
    masses=[M_tot/len(p)]*len(p); pos=[tuple(x) for x in p]
    rgal=np.sqrt((np.array(pos)**2).sum(1))
    log(f"placed {len(p)} clumps; clump radii: median {np.median(rgal)/kpc:.0f}kpc, "
        f"90th {np.percentile(rgal,90)/kpc:.0f}kpc")

    Rlist=np.array([50,100,150,200,250,300,420,600,1000,1500])*kpc
    resC,rho_app=clumpy_Mapp_radial(grid,masses,pos,soft,Rlist)

    # smooth spherical M_bar(<R) of the clump ensemble
    sr=np.sort(rgal); cm=np.arange(1,len(sr)+1)*(M_tot/len(p))
    def Mbar_of_R(R):
        return np.interp(R, sr, cm, left=0.0, right=M_tot)
    resS=smooth_Mapp_spherical(Mbar_of_R, Rlist)

    log(f"\n  {'R[kpc]':>7} {'Mbar(<R)':>10} {'ph_clumpy':>11} {'ph_smooth':>11} {'clmp/smth':>9} {'delta1e12':>10}")
    for (R,MaC,MbC),(R2,MaS,MbS) in zip(resC,resS):
        phC=MaC-MbC; phS=MaS-MbS
        ratio=phC/phS if phS!=0 else float('nan')
        log(f"  {R/kpc:7.0f} {MbC/1e12:10.3f} {phC/1e12:11.3f} {phS/1e12:11.3f} {ratio:9.4f} {(phC-phS)/1e12:10.4f}")
    log("\n  (Mbar(<R) is the SAME for clumpy & smooth by construction. ph in 1e12 Msun.)")
    log("  clmp/smth > 1 at core radius (420 kpc) => Carl's collective ADD;")
    log("  ~1 / <1 => redistribute-only / sub-additive (enclosed-mass theorem holds).")

    # inter-galaxy phantom sign: sample rho_app - rho_bar at midpoints between nearest pairs
    log("\n" + "="*78)
    log("INTER-GALAXY PHANTOM SIGN (Milgrom-1986: negative between masses?)")
    log("="*78)
    P=np.array(pos)
    # nearest-neighbour midpoints (a sample)
    mids=[]
    for i in range(0,len(P),7):
        d=np.linalg.norm(P-P[i],axis=1); d[i]=1e30; j=d.argmin()
        mids.append(0.5*(P[i]+P[j]))
    mids=np.array(mids)
    # rho_app on the grid -> interpolate nearest cell; rho_bar ~0 between clumps (vacuum)
    ix=np.clip(((mids[:,0]+L/2)/grid.d).astype(int),0,n-1)
    iy=np.clip(((mids[:,1]+L/2)/grid.d).astype(int),0,n-1)
    iz=np.clip(((mids[:,2]+L/2)/grid.d).astype(int),0,n-1)
    rho_mid=rho_app[ix,iy,iz]   # baryon ~0 here -> this is essentially the phantom density
    frac_neg=np.mean(rho_mid<0)
    log(f"  sampled {len(mids)} inter-galaxy midpoints; fraction with NEGATIVE apparent")
    log(f"  (phantom) density = {100*frac_neg:.0f}%  (median rho_app={np.median(rho_mid):.2e})")
    log("  Negative inter-galaxy phantom (Milgrom 1986) is the sub-additivity signature:")
    log("  the overlapping fields partially CANCEL between galaxies, they do NOT add mass.")

if __name__=="__main__":
    main()
