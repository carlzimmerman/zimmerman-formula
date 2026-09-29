# POST-HOC (after frozen runs, after reading CFG53's docstring): inverse-variance weighting of the per-galaxy slope differences, as CFG53's docstring states.
import io, contextlib, numpy as np
src=open("cfg97_massive_spirals_hi.py").read()
pre=src.split("# ---------------- CFG53 law-side shapes ----------------")[0].replace("rel.append(abs(g_num / g_cf - 1))","rel.append(0.0)")
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(pre,"x","exec"),g)
names,curves,S0,vlaw,Mstar,Mgas=[g[k] for k in ("names","curves","S0","vlaw","Mstar","Mgas")]
def slope(R,V,dV,wts=None):
    x=np.log(R);y=np.log(V);w=(V/dV)**2 if wts is None else wts
    xb=(w*x).sum()/w.sum();yb=(w*y).sum()/w.sum();sxx=(w*(x-xb)**2).sum()
    return (w*(x-xb)*(y-yb)).sum()/sxx,1/np.sqrt(sxx)
rows=[]
for i,n in enumerate(names):
    c=curves[n];keep=c[:,0]>=c[:,0].max()/2;R,V,dV=c[keep,0],c[keep,1],c[keep,2]
    so,se=slope(R,V,dV);w=(V/dV)**2;sl,_=slope(R,vlaw("point",Mstar()[i]+Mgas()[i],R),dV,wts=w)
    rows.append((so-sl,se*np.sqrt(2)));print(f"{n:9s} {'red ' if S0[i] else 'blue'} {len(R):2d} pts {R.min():5.1f}-{R.max():5.1f} obs {so:+.3f} law {sl:+.3f} diff {so-sl:+.3f}")
r=np.array([x[0] for x in rows]);s=np.array([x[1] for x in rows])
for lab,m in (("red",S0),("blue",~S0)):
    w=1/s[m]**2;mu=(r[m]*w).sum()/w.sum();e=1/np.sqrt(w.sum());chi2=((r[m]-mu)**2*w).sum();sc=max(1,np.sqrt(chi2/(m.sum()-1)))
    print(lab,"ivw mean %+.4f +- %.4f (chi2 %.1f/%d)"%(mu,e*sc,chi2,m.sum()-1))
