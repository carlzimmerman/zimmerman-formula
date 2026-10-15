import sys,json
from pathlib import Path
import numpy as np
from scipy.special import expit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
def current(S,Z):
 r=np.hypot(S,Z);u=2*r-1;f=np.zeros_like(r);fp=f.copy();fpp=f.copy();f[u>=1]=1
 mask=(u>0)&(u<1);v=u[mask];L=-1/v+1/(1-v);Lp=1/v**2+1/(1-v)**2;Lpp=-2/v**3+2/(1-v)**3
 ff=expit(L);f[mask]=ff;fp[mask]=2*ff*(1-ff)*Lp;fpp[mask]=4*ff*(1-ff)*((1-2*ff)*Lp**2+Lpp)
 b=.1*f;bp=.1*fp;bpp=.1*fpp;psip=(1+b*b)*bp;psipp=(1+b*b)*bpp+2*b*bp*bp
 rr=np.where(r>0,r,1)
 Ws=.5*S*Z/(rr*rr)*(psipp-psip/rr)
 Wz=-.5*(psipp*S*S/(rr*rr)+psip*(2/rr-S*S/(rr**3)))
 chi=-.5*S*S*psip/rr
 return Ws,Wz,chi
s=np.linspace(0,1.18,301);z=np.linspace(-1.18,1.18,501);S,Z=np.meshgrid(s,z);Ws,Wz,chi=current(S,Z);mag=np.hypot(Ws,Wz);scale=mag.max()
fig,ax=plt.subplots(figsize=(6.4,8.0),dpi=180)
im=ax.pcolormesh(S,Z,mag/scale,cmap='Blues',vmin=0,vmax=1,shading='auto',rasterized=True)
ax.contour(S,Z,chi/(-chi.min()),levels=np.linspace(-.95,-.08,10),colors='#164a73',linewidths=.75)
Ss,Zz=np.meshgrid(np.linspace(.04,1.1,17),np.linspace(-1.1,1.1,33));wx,wz,_=current(Ss,Zz);mm=np.hypot(wx,wz);valid=mm>.03*scale
ax.quiver(Ss[valid],Zz[valid],wx[valid]/mm[valid],wz[valid]/mm[valid],color='#102a43',angles='xy',scale_units='xy',scale=21,width=.003)
t=np.linspace(-np.pi/2,np.pi/2,300)
for r in [.5,1.]:ax.plot(r*np.cos(t),r*np.sin(t),'--',color='#6b7280',lw=.9)
ax.text(.08,.04,'Flat cabin',fontsize=10,color='#475569')
ax.text(.78,.82,'Wall',fontsize=10,color='#475569')
ax.set(xlim=(0,1.18),ylim=(-1.18,1.18),xlabel='Cylindrical radius s / R',ylabel='Axial position z / R')
ax.set_aspect('equal');ax.spines[['top','right']].set_visible(False)
ax.set_title('Clock current required by the assigned wall',loc='left',fontsize=13,pad=17)
fig.colorbar(im,ax=ax,shrink=.72,pad=.04,label='Relative current magnitude')
fig.text(.1,.035,'V = 0.1; arrows show normalized directions. W = Tⁱ₀.\nThis is a stress-energy current, not particle velocity or thrust.',fontsize=9,color='#475569')
fig.subplots_adjust(bottom=.14,left=.12,right=.86,top=.92)
fig.savefig(out/'clock_current.png',dpi=180)
res={'claim_id':'CLA-003','grid':[301,501],'V':.1,'profile':'sigma=expit(-1/u+1/(1-u)), u=2r/R-1 for0<u<1, extended0/1','max_current_dimensionless':float(scale),'streamfunction':'-s Psi_s/2, Psi=b+b^3/3, Mp=R=1','scope':'Illustration of exact assigned stationary current; no stability, material velocity, propulsion or horizon inference.'}
(out/'results.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
