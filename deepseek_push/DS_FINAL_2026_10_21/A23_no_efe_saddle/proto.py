import numpy as np, math, scipy.sparse as sps, scipy.sparse.linalg as spla

XMAX=6.0; RATE=0.05; BFAC=0.01; H0F=0.001

def make_faces(xmax, refs):
    xs=[0.0]
    while xs[-1]<xmax:
        x=xs[-1]
        h=min(hk+RATE*abs(x-ck) for ck,hk in refs)
        xs.append(min(x+h,xmax))
    return np.array(xs)

class Grid:
    def __init__(self,Rf,zf):
        self.Rf,self.zf=Rf,zf
        self.Rc=0.5*(Rf[1:]+Rf[:-1]); self.zc=0.5*(zf[1:]+zf[:-1])
        self.NR,self.NZ=len(self.Rc),len(self.zc); self.N=self.NR*self.NZ
        self.RR,self.ZZ=np.meshgrid(self.Rc,self.zc,indexing="ij")
        self.V=np.outer(np.pi*(Rf[1:]**2-Rf[:-1]**2),np.diff(zf))
        self.idx=np.arange(self.N).reshape(self.NR,self.NZ)

def plummer(g,b,mtot=1.0,centres=(0.5,-0.5)):
    rho=np.zeros((g.NR,g.NZ))
    for zp in centres:
        r2=g.RR**2+(g.ZZ-zp)**2
        rho+=(3/(4*math.pi*b**3))*(1+r2/b**2)**(-2.5)
    m=rho*g.V
    return m*(mtot/m.sum())

def coeffs(g,Phi,pbR,pbZ,mufun,e=0.0):
    dR=np.zeros_like(Phi); dZ=np.zeros_like(Phi)
    dR[1:-1,:]=(Phi[2:,:]-Phi[:-2,:])/(g.Rc[2:,None]-g.Rc[:-2,None])
    dR[0,:]=(Phi[1,:]-Phi[0,:])/(g.Rc[1]+g.Rc[0])
    dR[-1,:]=(pbR-Phi[-2,:])/(g.Rf[-1]-g.Rc[-2])
    dZ[:,1:-1]=(Phi[:,2:]-Phi[:,:-2])/(g.zc[None,2:]-g.zc[None,:-2])
    dZ[:,0]=(Phi[:,1]-Phi[:,0])/(g.zc[1]+g.zc[0])
    dZ[:,-1]=(pbZ-Phi[:,-2])/(g.zf[-1]-g.zc[-2])
    nR=(Phi[1:,:]-Phi[:-1,:])/(g.Rc[1:,None]-g.Rc[:-1,None])
    tR=0.5*(dZ[1:,:]+dZ[:-1,:])-e
    muR=mufun(np.hypot(nR,tR))
    nRo=(pbR-Phi[-1,:])/(g.Rf[-1]-g.Rc[-1])
    muRo=mufun(np.hypot(nRo,dZ[-1,:]-e))
    nz=(Phi[:,1:]-Phi[:,:-1])/(g.zc[None,1:]-g.zc[None,:-1])-e
    tz=0.5*(dR[:,1:]+dR[:,:-1])
    muz=mufun(np.hypot(nz,tz))
    nzo=(pbZ-Phi[:,-1])/(g.zf[-1]-g.zc[-1])-e
    muzo=mufun(np.hypot(nzo,dR[:,-1]))
    return muR,muRo,muz,muzo

def assemble(g,muR,muRo,muz,muzo,pbR,pbZ):
    I=g.idx; b=np.zeros(g.N); diag=np.zeros(g.N)
    rows,cols,vals=[],[],[]
    AR=2*math.pi*g.Rf[1:-1,None]*np.diff(g.zf)[None,:]
    cR=(muR*AR/(g.Rc[1:,None]-g.Rc[:-1,None])).ravel()
    a,bb=I[:-1,:].ravel(),I[1:,:].ravel()
    rows+=[a,bb]; cols+=[bb,a]; vals+=[cR,cR]
    np.add.at(diag,a,-cR); np.add.at(diag,bb,-cR)
    ARo=2*math.pi*g.Rf[-1]*np.diff(g.zf)
    cRo=(muRo*ARo/(g.Rf[-1]-g.Rc[-1])).ravel()
    ii=I[-1,:].ravel(); np.add.at(diag,ii,-cRo); b[ii]-=cRo*pbR
    Az=np.pi*(g.Rf[1:]**2-g.Rf[:-1]**2)[:,None]*np.ones((1,g.NZ-1))
    cz=(muz*Az/(g.zc[None,1:]-g.zc[None,:-1])).ravel()
    a,bb=I[:,:-1].ravel(),I[:,1:].ravel()
    rows+=[a,bb]; cols+=[bb,a]; vals+=[cz,cz]
    np.add.at(diag,a,-cz); np.add.at(diag,bb,-cz)
    Azo=np.pi*(g.Rf[1:]**2-g.Rf[:-1]**2)
    czo=(muzo*Azo/(g.zf[-1]-g.zc[-1])).ravel()
    ii=I[:,-1].ravel(); np.add.at(diag,ii,-czo); b[ii]-=czo*pbZ
    rows.append(np.arange(g.N)); cols.append(np.arange(g.N)); vals.append(diag)
    A=sps.csr_matrix((np.concatenate(vals),(np.concatenate(rows),np.concatenate(cols))),shape=(g.N,g.N))
    return A,b

def solve(g,m,mufun,phif,e=0.0,alpha=1.0,itmax=500,tol=1e-10,Phi0=None):
    Rb=np.hypot(g.Rf[-1],g.zc); Zb=np.hypot(g.Rc,g.zf[-1])
    pbR,pbZ=phif(Rb),phif(Zb)
    rhs=4*math.pi*m.ravel()
    Phi=phif(np.hypot(g.RR,g.ZZ)+1e-3) if Phi0 is None else Phi0.copy()
    mu=coeffs(g,Phi,pbR,pbZ,mufun,e)
    it=0
    for it in range(itmax):
        A,b=assemble(g,*mu,pbR,pbZ)
        Pn=spla.spsolve(A.tocsc(),rhs+b).reshape(g.NR,g.NZ)
        if alpha!=1.0: Pn=Phi+alpha*(Pn-Phi)
        d=np.max(np.abs(Pn-Phi))/(np.max(Pn)-np.min(Pn))
        Phi=Pn
        mu_new=coeffs(g,Phi,pbR,pbZ,mufun,e)
        mu=tuple(np.sqrt(a*b) for a,b in zip(mu,mu_new))
        if d<tol and it>3: break
    mu=coeffs(g,Phi,pbR,pbZ,mufun,e)
    A,b=assemble(g,*mu,pbR,pbZ)
    res=np.max(np.abs(A@Phi.ravel()-b-rhs))/np.max(np.abs(rhs))
    return Phi,pbR,pbZ,res,it+1,d

def laplacian(g,Phi,pbR,pbZ):
    one=lambda x: np.ones_like(x)
    mu=coeffs(g,Phi,pbR,pbZ,one,0.0)
    A,b=assemble(g,*mu,pbR,pbZ)
    return (A@Phi.ravel()-b).reshape(g.NR,g.NZ)/g.V

DEEP=lambda x: np.maximum(x,1e-14)
PHI1=lambda r: np.log(r)
PHI2=lambda r: math.sqrt(2.0)*np.log(r)

# control: one mass, total 1 (mtot=1), BC log r
Rf=make_faces(XMAX,[(0.0,H0F)]); zf=make_faces(XMAX,[(0.0,H0F)])
g=Grid(Rf,zf); m=plummer(g,BFAC,1.0,(0.0,))
Phi,pR,pZ,res,it,d=solve(g,m,DEEP,PHI1)
dR=np.zeros_like(Phi); dZ=np.zeros_like(Phi)
dR[1:-1,:]=(Phi[2:,:]-Phi[:-2,:])/(g.Rc[2:,None]-g.Rc[:-2,None])
dR[0,:]=(Phi[1,:]-Phi[0,:])/(g.Rc[1]+g.Rc[0])
dZ[:,1:-1]=(Phi[:,2:]-Phi[:,:-2])/(g.zc[None,2:]-g.zc[None,:-2])
dZ[:,0]=(Phi[:,1]-Phi[:,0])/(g.zc[1]+g.zc[0])
rc=np.hypot(g.RR,g.ZZ); gm=np.hypot(dR,dZ)
sel=(rc>0.3)&(rc<4.0)
print("M=1 BC=log r: max|gr-1| =",np.max(np.abs(gm[sel]*rc[sel]-1)), "it",it,"res",res)
C=laplacian(g,Phi,pR,pZ)/(4*math.pi)-m/g.V
selc=(rc>0.4)&(rc<2.0)
print("rho_ph check 4pi r^2 C: ",np.max(np.abs(C[selc]*4*math.pi*rc[selc]**2-1)))

# control: one mass, total 0.5 (as A13), BC log r
m05=plummer(g,BFAC,0.5,(0.0,))
Phi5,pR5,pZ5,res5,it5,d5=solve(g,m05,DEEP,PHI1)
dR=np.zeros_like(Phi5); dZ=np.zeros_like(Phi5)
dR[1:-1,:]=(Phi5[2:,:]-Phi5[:-2,:])/(g.Rc[2:,None]-g.Rc[:-2,None])
dR[0,:]=(Phi5[1,:]-Phi5[0,:])/(g.Rc[1]+g.Rc[0])
dZ[:,1:-1]=(Phi5[:,2:]-Phi5[:,:-2])/(g.zc[None,2:]-g.zc[None,:-2])
dZ[:,0]=(Phi5[:,1]-Phi5[:,0])/(g.zc[1]+g.zc[0])
gm5=np.hypot(dR,dZ)
print("M=0.5 BC=log r: max|gr-1| =",np.max(np.abs(gm5[sel]*rc[sel]-1)), "it",it5)
print("   mean gr at r=1..4:", np.mean((gm5*rc)[sel]))

# two masses total 1, BC sqrt2 log r
Rf2=make_faces(XMAX,[(0.0,0.002),(0.5,0.002)]); zf2=make_faces(XMAX,[(0.0,0.002),(0.5,0.002)])
g2=Grid(Rf2,zf2); m2=plummer(g2,BFAC,1.0)
Phi2,pR2,pZ2,res2,it2,d2=solve(g2,m2,DEEP,PHI2)
C2=laplacian(g2,Phi2,pR2,pZ2)/(4*math.pi)-m2/g2.V
row=C2[:,0]
S=float(2*np.sum(np.minimum(row,0)*np.diff(g2.Rf)))
print("two-body h=0.002: C(0.2)=",np.interp(0.2,g2.Rc,row),"S=",S,"it",it2,"res",res2)
print("C profile:", [(round(x,3),round(float(np.interp(x,g2.Rc,row)),4)) for x in (0.02,0.05,0.1,0.2,0.3,0.5,1.0)])
print("far flux: at r=5, |grad|*r =", end=" ")
dR=np.zeros_like(Phi2); dZ=np.zeros_like(Phi2)
dR[1:-1,:]=(Phi2[2:,:]-Phi2[:-2,:])/(g2.Rc[2:,None]-g2.Rc[:-2,None])
dR[0,:]=(Phi2[1,:]-Phi2[0,:])/(g2.Rc[1]+g2.Rc[0])
dZ[:,1:-1]=(Phi2[:,2:]-Phi2[:,:-2])/(g2.zc[None,2:]-g2.zc[None,:-2])
dZ[:,0]=(Phi2[:,1]-Phi2[:,0])/(g2.zc[1]+g2.zc[0])
rc2=np.hypot(g2.RR,g2.ZZ); gm2=np.hypot(dR,dZ)
sel3=(rc2>4.5)&(rc2<5.5)
print(np.mean((gm2*rc2)[sel3]))
print("total mass:", m2.sum())
