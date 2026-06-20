# convergence: does the realistic clmp/smth ratio depend on grid resolution / softening?
import numpy as np, sys, os
sys.path.insert(0,'.')
from two_body_subadditivity import G,Msun,kpc,a0,nu_simple,LocalGrid
from radial_and_intergalaxy import gradN_vectorized
def run(n, soft_kpc, seed=11):
    R500=2100*kpc;Rcore=420*kpc;Mgas500=1.0e14*Msun;fstar=0.18
    rc=0.20*R500;beta=0.65
    def bMenc(R):
        x=np.linspace(1e-3*rc,R,2000);rho=1.0/(1+(x/rc)**2)**(1.5*beta);return np.trapz(4*np.pi*x**2*rho,x)
    rho0=Mgas500/bMenc(R500)
    L=3000*kpc;grid=LocalGrid(L,n);soft=max(soft_kpc*kpc,1.5*L/n)
    r=np.maximum(grid.r,0.5*grid.d)
    rt=np.linspace(grid.d,np.sqrt(3)*L/2,300);Mt=np.array([rho0*bMenc(R) for R in rt])
    Mgr=np.interp(r,rt,Mt,left=0,right=Mt[-1]);g=G*Mgr/r**2
    gxg,gyg,gzg=g*grid.X/r,g*grid.Y/r,g*grid.Z/r
    np.random.seed(seed);rs=R500/4;N=80
    rgr=np.linspace(5*kpc,Rcore,3000);x=rgr/rs;w=rgr**2/(x*(1+x)**2);w/=w.sum()
    rg=np.random.choice(rgr,N,p=w);ct=np.random.uniform(-1,1,N);ph=np.random.uniform(0,2*np.pi,N);st=np.sqrt(1-ct**2)
    P=np.c_[rg*st*np.cos(ph),rg*st*np.sin(ph),rg*ct];P[0]=0
    gm=np.random.gamma(1.2,1.0,N);gm[0]=8.0;gm*=0.5*fstar*Mgas500/gm.sum()
    masses=list(gm);pos=[tuple(p) for p in P]
    def ph_core(mode):
        if mode=='d': gxs,gys,gzs=gradN_vectorized(grid,masses,pos,soft)
        else:
            rgal=np.sqrt((np.array(pos)**2).sum(1));o=np.argsort(rgal);rr=rgal[o];cm=np.cumsum(np.array(masses)[o])
            Mg=np.interp(r,rr,cm,left=0,right=cm[-1]);gg=G*Mg/r**2;gxs,gys,gzs=gg*grid.X/r,gg*grid.Y/r,gg*grid.Z/r
        gx,gy,gz=gxg+gxs,gyg+gys,gzg+gzs;gmag=np.sqrt(gx**2+gy**2+gz**2);nu=nu_simple(gmag/a0)
        S=grid.div(nu*gx,nu*gy,nu*gz);rho_app=S/(4*np.pi*G)
        return grid.Menc(rho_app,Rcore)/Msun
    Mbar=(rho0*bMenc(Rcore)+sum(masses))/Msun
    phd=ph_core('d')-Mbar;phs=ph_core('s')-Mbar
    return phd/phs
print("Convergence of clumpy/smooth core-phantom ratio:")
for n,s in [(160,12),(240,10),(240,18),(320,8)]:
    print(f"  n={n} cell={3000/n:.1f}kpc soft={s}kpc: ratio={run(n,s):.4f}")
print("Seed (realization) scatter at n=240,soft=12:")
rr=[run(240,12,seed=s) for s in [1,11,22,33,44]]
import statistics as S
print(f"  ratios={[f'{x:.4f}' for x in rr]}  mean={S.mean(rr):.4f} +- {S.pstdev(rr):.4f}")
