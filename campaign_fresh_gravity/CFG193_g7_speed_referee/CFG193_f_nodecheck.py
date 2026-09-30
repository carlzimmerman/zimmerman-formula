#!/usr/bin/env python3
# CFG193_f_nodecheck -- answers the CFG186 owner's questions about the NGC2403 / F571-8 / UGC05764 / UGC00731 cells (reads CFG186's .npz, my curves).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CFG193_common import *
T = Tee(os.path.join(HERE, "CFG193_f_nodecheck.out")); P = T.p
LANE=os.path.join(REPO,"campaign_fresh_gravity","CFG186_a0_vs_cmb_speed")
th=np.load(os.path.join(LANE,"cfg186_a_curves.npz"),allow_pickle=True); tn=[str(x) for x in th['names']]
cn=np.load(os.path.join(HERE,'CFG193_curves.npz')); cnn=[str(x) for x in cn['names']]
gb={g['name']:g for g in load_sparc()}; nu=get_kernel('mono')
P("grids identical: xgrid",np.allclose(th['xgrid'],XG),"tgrid",np.allclose(th['tgrid'],TG))
def tab(nm):
    return cn['C'][cnn.index(nm)]+(TG**2)[:,None], th['chi'][tn.index(nm)].astype(float)
nm='NGC2403'; a,b=tab(nm); j=int(round((-9.04-XG[0])/0.02))
P("(1)(2) t=-4.00 is TGRID[0]; log a0=-9.04 is XGRID[%d] (%.2f): a node. CFG186 value = cfg186_a_curves.npz['chi'][%d, 0, %d] (float32) = %.4f; mine = my CFG193_curves.npz['C'][%d,0,%d] + t^2 = %.4f. Direct stored-grid reads; no spline, no interpolation, no CFG186 code run."%(j,XG[j],tn.index(nm),j,b[0,j],cnn.index(nm),j,a[0,j]))
P("(3) table, NGC2403 (theirs / mine / mine-theirs):")
for ti in (0,1,2):
    ks=[k for k in range(j-3,j+3) if 0<=k<116]
    P("  t=%+.2f  x:"%TG[ti]," ".join("%8.2f"%XG[k] for k in ks))
    P("     theirs  "," ".join("%8.2f"%b[ti,k] for k in ks)); P("     mine    "," ".join("%8.2f"%a[ti,k] for k in ks)); P("     diff    "," ".join("%8.2f"%(a[ti,k]-b[ti,k]) for k in ks))
d=a-b; s=np.isfinite(d)
P("(4) NGC2403 whole grid: cells with theirs>mine by >0.1: %d, by >1: %d, by >10: %d, of %d feasible; mine>theirs by >0.1: %d"%(int(np.sum(d[s]<-0.1)),int(np.sum(d[s]<-1)),int(np.sum(d[s]<-10)),int(s.sum()),int(np.sum(d[s]>0.1))))
g=np.argwhere(s&(d<-0.1)); P("   flagged t index range %d..%d, x index range %d..%d (x %.2f..%.2f)"%(g[:,0].min(),g[:,0].max(),g[:,1].min(),g[:,1].max(),XG[g[:,1].min()],XG[g[:,1].max()]))
for ti in (0,4,8,12,16,20):
    r=-d[ti]; P("   t=%+.2f: max(theirs-mine) = %.3f at x=%.2f; number of x cells > 0.1: %d"%(TG[ti],np.nanmax(r),XG[int(np.nanargmax(r))],int(np.sum(r>0.1))))
P("   owner's set (every 5th x, x idx multiple of 5): min(mine-theirs) = %.4f (max excess of theirs); on the other x cells: %.3f;  x idx of the stated cell = %d, mod 5 = %d"%(np.nanmin(d[:,::5]),np.nanmin(np.delete(d,np.arange(0,116,5),axis=1)),j,j%5))
gx=sorted(set(g[:,1])); P("   flagged x indices: %s; multiples of 5 among them: %s"%(gx,[k for k in gx if k%5==0]))
P("   the anchor x of CFG186's warm start (-9.92) is index %d"%int(np.argmin(abs(XG+9.92))))
for nm2 in ('F571-8','UGC05764','UGC00731'):
    a2,b2=tab(nm2); d2=a2-b2; s2=np.isfinite(d2); g2=np.argwhere(s2&(d2<-0.1)); ii,jj=np.unravel_index(np.nanargmin(d2),d2.shape)
    P("   %s: theirs>mine by >0.1 in %d cells (>1: %d) of %d; t idx %d..%d, x idx %d..%d; flagged x idx multiples of 5: %d of %d; worst node t=%+.2f (idx %d) x=%.2f (idx %d): theirs %.3f mine %.3f; max(mine-theirs) anywhere %.3f"%(
      nm2,len(g2),int(np.sum(d2[s2]<-1)),int(s2.sum()),g2[:,0].min(),g2[:,0].max(),g2[:,1].min(),g2[:,1].max(),sum(1 for k in set(g2[:,1]) if k%5==0),len(set(g2[:,1])),TG[ii],ii,XG[jj],jj,b2[ii,jj],a2[ii,jj],np.nanmax(d2)))
    lo=max(min(jj-2,111),0); P("      row t idx %d, x idx %d..%d: theirs %s | mine %s"%(ii,lo,lo+4,[round(b2[ii,k],2) for k in range(lo,lo+5)],[round(a2[ii,k],2) for k in range(lo,lo+5)]))
    if 0<ii<32: P("      column x idx %d, t idx %d..%d: theirs %s | mine %s"%(jj,ii-1,ii+1,[round(b2[k,jj],2) for k in (ii-1,ii,ii+1)],[round(a2[k,jj],2) for k in (ii-1,ii,ii+1)]))
# my own cold-start check with parameters at the NGC2403 node, and bounds check against CFG186-style bounds
from scipy.optimize import least_squares
G=Gal(gb[nm]); a0=10**XG[j]; scl=math.sqrt((G.D+G.eD*TG[0])/G.D)
lo_,hi_=np.array([-1.6,-1.6,5.0]),np.array([0.8,0.8,89.0]); rng=np.random.RandomState(11); best=(1e9,None)
for s_ in range(60):
    p0=np.clip([math.log10(.5)+rng.uniform(-.4,.4),math.log10(.7)+rng.uniform(-.4,.4),G.inc+rng.uniform(-3,3)*G.einc],lo_+1e-6,hi_-1e-6)
    sol=least_squares(lambda p: resid(G,np.array([p]),np.array([a0]),np.array([scl]),nu,True)[0],p0,bounds=(lo_,hi_),xtol=1e-12,ftol=1e-12,gtol=1e-12)
    if 2*sol.cost<best[0]: best=(2*sol.cost,sol.x)
p=best[1]; P("   my 60-start minimum at the NGC2403 node (data+priors, t^2 added): %.4f; parameters: log10 Ups_d = %.3f (prior sigma units %.2f), log10 Ups_b = %.3f, inclination %.2f deg (catalogue %.1f +- %.1f, i.e. %.2f sigma)"%(best[0]+TG[0]**2,p[0],(p[0]-math.log10(.5))/.1,p[1],p[2],G.inc,G.einc,(p[2]-G.inc)/G.einc))
P("   CFG186-style bounds (from its README/FROZEN only, not its code): none read here; NGC2403 has bulge flag %s"%G.hasb)
# (5) swap test variants
def fit_on(C,N,names,Zm,mask_nodes=False):
    cv=Curves(names,C,meta=dict(N=N)); sg,xh,_=cv.sigma_i(); L0,tau=cv.tau_ml(sg,xh); ce=cv.ceff_fast(tau)
    if mask_nodes:
        keep=np.zeros(len(TF),bool); keep[::5]=True; ce=ce.copy(); ce[:,~keep,:]=1e6
    st=Stat(ce); return fit_LB(st,Zm,L0=L0), tau
ut=np.load(os.path.join(HERE,'CFG193_utable.npz')); un=[str(x) for x in ut['names']]
prim=[n for n,ip in zip(tn,th['isprim']) if ip]
Zm=[]; 
for n in prim:
    k=tn.index(n); zc=cmb_convert(th['cz_hel'][k],th['l'][k],th['b'][k]); Dt=np.maximum(th['D'][k]+th['eD'][k]*TF,0.3*th['D'][k]); u0=float(u_los(zc,th['D'][k]))
    Zm.append(((u0+u_los(zc,Dt)-u0)/W_REF)**2)
Zm=np.array(Zm)
ip=[tn.index(n) for n in prim]; Ct=th['chi'][ip].astype(float)-(TG**2)[None,:,None]; Nt=th['npt'][ip]
Cm=np.array([cn['C'][cnn.index(n)] for n in prim]); Nm=np.array([cn['N'][cnn.index(n)] for n in prim])
Cs=Ct.copy(); Cs[prim.index(nm)]=Cm[prim.index(nm)]; Cr=Cm.copy(); Cr[prim.index(nm)]=Ct[prim.index(nm)]
P("(5) swap tests use CFG186's stored chi grid nodes (33 t x 116 x) and my stored grid nodes; both are then spline-interpolated in t onto TFINE by MY Curves class (cubic spline along t, same as the main fits).")
for lab,C,N in (("CFG186 curves",Ct,Nt),("CFG186 curves with my NGC2403",Cs,Nt),("my curves",Cm,Nm),("my curves with CFG186's NGC2403",Cr,Nm)):
    (L,bb),tau=fit_on(C,N,prim,Zm); (L2,b2),tau2=fit_on(C,N,prim,Zm,mask_nodes=True)
    P("   %-34s spline-refined t: beta_hat %+.3f ;  restricted to the 33 grid-node t values only (no spline between nodes): beta_hat %+.3f"%(lab,bb,b2))
P("   (x is always interpolated cubically between the 0.02-dex nodes in the fit; at the fit minimum the stated NGC2403 cell is a node in both x and t.)")

# ---------------------------------------------------------------------------------------------------------------
# (6) Is the difference the OPTIMISER, or the BOUNDS?  My optimum at the NGC2403 node has inclination 38.2 deg = -8.26 sigma from the catalogue
# (63.0 +- 3.0).  CFG186's _bounds (read in phase 2) limit inclination to Inc +- 8 sigma (>= 5 deg, <= 90) and log Upsilon to +-1.0 dex
# (u = +-10 in 0.1-dex units); my LM bounds are [-1.6, 0.8] (log10 Upsilon) and [5, 89] deg.  Recompute the four galaxies with CFG186-style bounds.
import CFG193_common as cc
P("(6) recomputing NGC2403, F571-8, UGC05764, UGC00731 with CFG186-style bounds (inclination Inc +- 8 sigma, log10 Upsilon = log10 Upsilon0 +- 1.0) and comparing with its stored grid")
res6={}
for nm2 in ('NGC2403','F571-8','UGC05764','UGC00731'):
    G=Gal(gb[nm2])
    ilo=max(G.inc-8*G.einc,5.0); ihi=min(G.inc+8*G.einc,90.0)
    cc.LO[:]=[math.log10(.5)-1.0, math.log10(.7)-1.0, ilo]; cc.HI[:]=[math.log10(.5)+1.0, math.log10(.7)+1.0, ihi]
    Cb=profile_grid(G,nu,nstart=3)+(TG**2)[:,None]
    cc.LO[:]=[-1.6,-1.6,5.0]; cc.HI[:]=[0.8,0.8,89.0]
    b2=th['chi'][tn.index(nm2)].astype(float); a2=cn['C'][cnn.index(nm2)]+(TG**2)[:,None]
    dd=Cb-b2; ss=np.isfinite(dd); near=ss&(b2-np.nanmin(b2)<=25)
    d_unb=a2-b2; su=np.isfinite(d_unb)
    P("   %-9s bounded-recompute minus CFG186 stored: all %d cells max|d| = %.4f, 95%% |d| = %.4f, cells |d|>0.1: %d;  (my unbounded minus stored: cells theirs>mine by >0.1: %d)"%(nm2,int(ss.sum()),np.nanmax(np.abs(dd)),np.percentile(np.abs(dd[ss]),95),int(np.sum(np.abs(dd[ss])>0.1)),int(np.sum(d_unb[su]<-0.1))))
    res6[nm2]=Cb
    if nm2=='NGC2403':
        P("      node t=-4.00, x=-9.04: bounded recompute %.3f | CFG186 stored %.3f | unbounded %.3f ; inclination bounds used [%.1f, %.1f] deg"%(Cb[0,113],b2[0,113],a2[0,113],ilo,ihi))
# beta_hat with my curves but the four galaxies replaced by the bounded recomputation
Cbd=Cm.copy()
for nm2,Cb in res6.items():
    if nm2 in prim: Cbd[prim.index(nm2)]=Cb-(TG**2)[:,None]
(L,bb),tau=fit_on(Cbd,Nm,prim,Zm); (L2,b2_),_=fit_on(Cbd,Nm,prim,Zm,mask_nodes=True)
P("   my curves, primary members of the four (NGC2403 only) recomputed with CFG186-style bounds: beta_hat %+.3f (spline-refined t), %+.3f (nodes only); CFG186's own +0.887"%(bb,b2_))

# ---------------------------------------------------------------------------------------------------------------
# (7) parameters at the cells in question, box membership, chi2 inside CFG186's box (scipy bounded least squares, 60 starts), point sets
from scipy.optimize import least_squares
def solve(G, xj, ti_val, lo, hi, nst=60, seed=5):
    a0=10**XG[xj]; scl=math.sqrt(max(G.D+G.eD*ti_val,0.3*G.D)/G.D); rng=np.random.RandomState(seed); best=(1e18,None)
    for s_ in range(nst):
        p0=np.clip([math.log10(.5)+rng.uniform(-.4,.4),math.log10(.7)+rng.uniform(-.4,.4),G.inc+rng.uniform(-3,3)*G.einc],lo+1e-6,hi-1e-6)
        sol=least_squares(lambda p: resid(G,np.array([p]),np.array([a0]),np.array([scl]),nu,True)[0],p0,bounds=(lo,hi),xtol=1e-12,ftol=1e-12,gtol=1e-12)
        if 2*sol.cost<best[0]: best=(2*sol.cost,sol.x)
    return best[0]+ti_val**2, best[1]
cells=[('NGC2403',0,113),('F571-8',30,113),('F571-8',32,115),('UGC05764',26,6),('UGC05764',8,0),('UGC00731',27,0),('UGC00731',32,115)]
P("(7) per-cell solutions (log10 Upsilon0: disk %.3f, bulge %.3f; prior sigma 0.1 dex; inclination prior sigma = e_Inc):"%(math.log10(.5),math.log10(.7)))
for nm2,ti,xj in cells:
    G=Gal(gb[nm2]); b2=th['chi'][tn.index(nm2)].astype(float)
    lo_m,hi_m=np.array([-1.6,-1.6,5.0]),np.array([0.8,0.8,89.0])
    ilo=max(G.inc-8*G.einc,5.0); ihi=min(G.inc+8*G.einc,90.0)
    lo_c,hi_c=np.array([math.log10(.5)-1.0,math.log10(.7)-1.0,ilo]),np.array([math.log10(.5)+1.0,math.log10(.7)+1.0,ihi])
    chi_m,pm=solve(G,xj,TG[ti],lo_m,hi_m); chi_c,pc=solve(G,xj,TG[ti],lo_c,hi_c)
    inbox=bool(np.all(pm>=lo_c-1e-6) and np.all(pm<=hi_c+1e-6))
    P("   %-9s t=%+.2f (idx %d) x=%.2f (idx %d): stored %.3f | mine (my bounds) %.3f | mine in CFG186's box %.3f | grid value of mine %.3f"%(nm2,TG[ti],ti,XG[xj],xj,b2[ti,xj],chi_m,chi_c,cn['C'][cnn.index(nm2)][ti,xj]+TG[ti]**2))
    P("      my solution: log10 Ups_d %.3f (u_d = %+.2f in 0.1-dex units), log10 Ups_b %.3f (u_b = %+.2f), inclination %.2f deg = %+.2f sigma_Inc (catalogue %.1f +- %.1f), t = %+.2f (D' = %.3f Mpc; not a free parameter: fixed by the grid node; prior t^2 = %.2f)"%(
        pm[0],(pm[0]-math.log10(.5))/.1,pm[1],(pm[1]-math.log10(.7))/.1,pm[2],(pm[2]-G.inc)/G.einc,G.inc,G.einc,TG[ti],G.D+G.eD*TG[ti],TG[ti]**2))
    P("      CFG186-box solution: log10 Ups_d %.3f (u_d %+.2f), inclination %.2f deg (%+.2f sigma); CFG186 box inclination [%.1f, %.1f], Ups u in [-10,10] i.e. log10 Ups_d in [%.3f, %.3f]; my solution inside CFG186's box: %s"%(
        pc[0],(pc[0]-math.log10(.5))/.1,pc[2],(pc[2]-G.inc)/G.einc,ilo,ihi,lo_c[0],hi_c[0],inbox))
P("(5) data points / weights / mask for the four galaxies (mine U1 = the main run; U2 = CFG186-style mask):")
for nm2 in ('NGC2403','F571-8','UGC05764','UGC00731'):
    g=gb[nm2]; m1=usable_mask(g,'U1'); m2=usable_mask(g,'U2')
    P("   %-9s CFG186 npt %d | my U1 N %d | my U2 N %d | points with Vdisk<0 or Vbul<0 among U1: %d | points with fiducial baryonic V^2<=0 among U1: %d | raw file points %d | eV min %.2f"%(nm2,th['npt'][tn.index(nm2)],int(m1.sum()),int(m2.sum()),int(np.sum((g['Vd'][m1]<0)|(g['Vb'][m1]<0))),int(np.sum((g['Vg'][m1]*np.abs(g['Vg'][m1])+.5*g['Vd'][m1]**2+.7*g['Vb'][m1]**2)<=0)),len(g['R']),g['eV'][m1].min()))
P("    weights: both use chi2 = sum((V_obs - V_model)/eV)^2 with the published eV, unscaled inside the profile (Birge scaling is applied afterwards, in the statistic); priors: identical form (Upsilon: (log10 Ups - log10 Ups0)/0.1, inclination: (i' - i)/e_Inc, t^2).")
P("    model differences: mine signed V_disk|V_disk|, V_bul|V_bul| vs CFG186 V^2 (identical when V >= 0); g_bar floor 1e-16 m/s^2 vs S >= 1e-6 (km/s)^2; kpc = 3.0856776e19 vs 3.0857e19 m (7e-6 relative).")

# ---------------------------------------------------------------------------------------------------------------
# (8) the exact cells quoted in README.md, and the extent of the NGC2403 region near its minimum
P("(8) the cells quoted in the README, solved unbounded (my bounds) and inside CFG186's box:")
for nm2,tv,xv in (('NGC2403',-4.0,-9.04),('F571-8',3.0,-9.00),('UGC05764',1.5,-10.98),('UGC00731',1.75,-11.28)):
    ti=int(round((tv+4)/0.25)); xj=int(round((xv-XG[0])/0.02)); G=Gal(gb[nm2]); b2=th['chi'][tn.index(nm2)].astype(float)
    ilo=max(G.inc-8*G.einc,5.0); ihi=min(G.inc+8*G.einc,90.0)
    lo_m,hi_m=np.array([-1.6,-1.6,5.0]),np.array([0.8,0.8,89.0]); lo_c,hi_c=np.array([math.log10(.5)-1.0,math.log10(.7)-1.0,ilo]),np.array([math.log10(.5)+1.0,math.log10(.7)+1.0,ihi])
    cm,pm=solve(G,xj,tv,lo_m,hi_m); cc_,pc=solve(G,xj,tv,lo_c,hi_c); inb=bool(np.all(pm>=lo_c-1e-6) and np.all(pm<=hi_c+1e-6))
    P("   %-9s node t idx %d x idx %d: stored %.3f | mine unbounded %.3f (log10 Ups_d %.3f = u %+.1f; inclination %.2f = %+.2f sigma; inside CFG186 box: %s) | mine in CFG186 box %.3f"%(nm2,ti,xj,b2[ti,xj],cm,pm[0],(pm[0]-math.log10(.5))/.1,pm[2],(pm[2]-G.inc)/G.einc,inb,cc_))
a,b=tab('NGC2403'); d=a-b; s=np.isfinite(d); near=s&(b-np.nanmin(b)<=25.0)
g=np.argwhere(near&(d<-0.1)); P("   NGC2403: cells within Delta chi2 <= 25 of CFG186's minimum: %d; of those theirs>mine by >0.1: %d (t idx %d..%d, x idx %d..%d); the neighbours of the stated node on the grid (x idx 111..115 at t idx 0) are: theirs %s"%(int(near.sum()),len(g),g[:,0].min(),g[:,0].max(),g[:,1].min(),g[:,1].max(),[round(b[0,k],2) for k in range(111,116)]))
inc_sig=[]
for ti,xj in g[::max(1,len(g)//12)]:
    G=Gal(gb['NGC2403']); c_,p_=solve(G,int(xj),TG[int(ti)],np.array([-1.6,-1.6,5.0]),np.array([0.8,0.8,89.0]),nst=30); inc_sig.append(round(float((p_[2]-G.inc)/G.einc),2))
P("   my unbounded inclination offsets (sigma_Inc units) at a sample of those flagged cells: %s"%inc_sig)
