import sys,json,time,math;sys.dont_write_bytecode=True
import numpy as np,dr8_ic as I
S=I.setup();O={}
for k in ("core","nfw"):
  for rd in (0.1,0.2,0.3):
    x,v,m,Ms,Mo=I.build(k,S,60000,1,rd)
    sel=(Mo.E>1e-4*Mo.pa[-1])
    nneg=int((Mo.f<=0).sum());nneg_sel=int((Mo.f[sel]<=0).sum())
    psi=Mo.Psi[::400][1:-2];err=np.abs(Mo.rho_from_f(psi)/Mo.rho[::400][1:-2]-1)
    r=np.sqrt((x*x).sum(1));rr=np.array([.25,.5,1,2,5])*S["r0"];Na=np.interp(np.log(rr),np.log(Mo.r),Mo.M)/m;Nm=np.searchsorted(np.sort(r),rr)
    T=.5*m*(v*v).sum()
    W=-m*np.trapz(I.G*Mo.M/Mo.r*Mo.M/Ms*0+0*Mo.M,Mo.r) if False else -np.trapz(I.G*Mo.M/Mo.r*np.gradient(Mo.M,Mo.r),Mo.r)
    O[f"{k}_{rd}"]=dict(N_neg=nneg,N_neg_sel=nneg_sel,fminrel=Mo.fmin_rel,rho_err_max=float(err.max()),rho_err_med=float(np.median(err)),Ms=Ms,m=m,Mcut=Mo.Mtot,N_an=Na.round(1).tolist(),N_meas=Nm.tolist(),virial=float(2*T/abs(W)))
    print(k,rd,O[f"{k}_{rd}"],flush=True)
    if nneg_sel==0:break
json.dump(O,open("dr8_precheck.json","w"),indent=1)
