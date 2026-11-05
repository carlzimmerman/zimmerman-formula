#!/usr/bin/env python3
"""AZ46 model parameters and dense-Jacobian fits; no data verdict here."""
import math
import numpy as np
from scipy import ndimage
from scipy.optimize import least_squares
import model as M

class YieldRequested(Exception):pass

def smooth_physical(values,pixel,width=30.):
    """Cell-integrated centred top-hat, half-sample symmetric extension."""
    if pixel<=0 or width<=0:raise ValueError('Positive scales required')
    radius=int(math.ceil(width/(2*pixel)+.5))
    offsets=np.arange(-radius,radius+1,dtype=float)
    overlap=np.maximum(0,np.minimum((offsets+.5)*pixel,width/2)-np.maximum((offsets-.5)*pixel,-width/2))
    return ndimage.convolve1d(np.asarray(values,float),overlap/width,mode='reflect')

class Base:
    def __init__(self,cube,prepared,stop=None):
        self.c=cube;self.P=prepared;self.stop=stop or (lambda:False)
        self.nr=int(prepared['nring']);self.rc=(np.arange(self.nr)+.5)*prepared['ring_width']
        self.nodes=np.linspace(0,float(prepared['R_out']),6);self.calls=0
    def check_stop(self):
        if self.stop():raise YieldRequested('Fit interrupted at residual boundary')
        self.calls+=1
    def sfun(self,values):return M.C.interp_nodes(self.nodes,values)
    def optimize(self,fun,start,lo,hi,scale,budget):
        if budget not in (100,200) and budget!=2:raise ValueError('Only frozen budgets or ungraded 2-evaluation pilot')
        return least_squares(fun,np.clip(start,lo+1e-6,hi-1e-6),bounds=(lo,hi),x_scale=scale,
                             method='trf',max_nfev=budget,diff_step=1e-3)

class Free(Base):
    def start(self,inc=48.):
        initial=np.interp(self.rc,self.P['initial_ring_R'],self.P['initial_ring_V'])
        initial=np.nan_to_num(initial,nan=10.,posinf=60.,neginf=1.)
        return np.r_[0.,0.,73.7,inc,-232.2,np.clip(initial,1,60),np.full(6,9.)]
    def fields(self,p):
        x,y,pa,inc,vs=p[:5];rotation=M.C.interp_nodes(np.r_[0.,self.rc],np.r_[0.,p[5:5+self.nr]])
        return M.C.vfield(self.c,x,y,pa,inc,vs,rotation,self.sfun(p[5+self.nr:11+self.nr]))
    def residual(self,p):
        self.check_stop();vl,sg,_=self.fields(p);return self.c.residual(vl,sg)
    def fit(self,start,budget=100):
        lo=np.r_[-60,-60,40,15,-250,np.zeros(self.nr),np.full(6,2.)]
        hi=np.r_[60,60,110,60,-215,np.full(self.nr,80.),np.full(6,25.)]
        scale=np.r_[5,5,3,3,1,np.full(self.nr,2.),np.ones(6)]
        return self.optimize(self.residual,start,lo,hi,scale,budget)

class Law(Base):
    def __init__(self,cube,prepared,baryons,a0,modified=True,nc=False,thickness=200.,stop=None):
        super().__init__(cube,prepared,stop);self.b=baryons;self.a0=a0;self.modified=modified;self.nc=nc;self.thickness=thickness
    def start(self,inc=None):
        p=np.r_[0.,0.,73.7,-232.2,np.full(6,9.),np.zeros(18 if self.nc else 0)]
        return p if inc is None else np.r_[inc,p]
    def rotation(self,x,y,pa,inc,sg):
        radii,v2,gas=self.b.vc2(x,y,pa,inc,self.a0,modified=self.modified,thickness=self.thickness)
        sigma=self.sfun(sg)(radii);q=np.log(np.maximum(gas,1e-30)*sigma**2)
        derivative=np.gradient(smooth_physical(q,self.b.pixel),np.log(radii))
        return M.C.interp_nodes(radii,np.sqrt(np.maximum(v2+sigma**2*derivative,0))),radii,np.sqrt(np.maximum(v2,0))
    def fields(self,p,inc):
        x,y,pa,vs=p[:4];sg=p[4:10];rotation,_,_=self.rotation(x,y,pa,inc,sg)
        nc=None
        if self.nc:nc=lambda r:tuple(np.interp(r,self.nodes,p[i:i+6]) for i in (10,16,22))
        return M.C.vfield(self.c,x,y,pa,inc,vs,rotation,self.sfun(sg),nc=nc)
    def residual_at(self,p,inc):
        self.check_stop();vl,sg,_=self.fields(p,inc);return self.c.residual(vl,sg)
    def fit(self,start,inc=None,budget=100):
        count=18 if self.nc else 0
        lo=np.r_[-60,-60,40,-250,np.full(6,2.),np.full(count,-20.)]
        hi=np.r_[60,60,110,-215,np.full(6,25.),np.full(count,20.)]
        scale=np.r_[5,5,3,1,np.ones(6),np.full(count,2.)]
        if inc is None:
            lo=np.r_[15.,lo];hi=np.r_[60.,hi];scale=np.r_[3.,scale]
            fun=lambda p:self.residual_at(p[1:],p[0])
        else:fun=lambda p:self.residual_at(p,inc)
        return self.optimize(fun,start,lo,hi,scale,budget)

def summarize(result,cube,model,budget):
    chi=float(np.sum(result.fun**2));npar=len(result.x);dof=cube.ndat-npar
    return dict(parameters=result.x.tolist(),chi2=chi,ndat=cube.ndat,npar=npar,dof=dof,
                chi2_red=chi/dof if dof>0 else None,status=int(result.status),nfev=int(result.nfev),
                njev=int(result.njev or 0),residual_calls=model.calls,optimality=float(result.optimality),
                success=bool(result.success),message=result.message,budget=budget,
                optimizer_accepted=bool(result.status>0 and dof>0 and budget in (100,200)),
                scope='UNGRADED implementation pilot' if budget==2 else 'Optimizer result only; all other gates separate',
                fallback_max_pixels=cube.fallback_max,fallback_total_pixels=cube.fallback_total)
