"""Independent species-direction and endpoint curvature diagnostics."""
import numpy as np,torch,json,argparse
from pathlib import Path
from carrier_checked import Carrier
from joint import T,RESERVOIR

def audit(r):
 m=Carrier(n=r['n'],domain=4,beta=r['beta'],K=r['K'],charge=r['charge'],rhos=r['rhos'])
 # Reconstruct exact extent, not a rounded physical reference.
 from joint import outer
 m=Carrier(n=r['n'],domain=r['R_kpc']/(m.rm*outer(m.b)),beta=r['beta'],K=r['K'],charge=r['charge'],rhos=r['rhos']);m.ell2=(r.get('ell_kpc',30)/m.rm)**2
 mass=np.array(r['mass']);x=np.array(r['v'][m.n:]);v=np.r_[mass,x];a=T(v).requires_grad_(True)
 H=torch.autograd.functional.hessian(lambda aa:m.energy(torch.log(aa[:m.n]),aa[m.n:]),a).detach().numpy();E,g=m.direct(v)
 # Tangent space for occupied material cells and interior phase coordinates.
 im=np.where(mass>1e-7)[0];ix=np.where((x>1e-5)&(x<1-1e-5))[0]+m.n
 Z=np.zeros((2*m.n,max(0,len(im)-1)+len(ix)))
 for j,i in enumerate(im[:-1]):Z[i,j]=1;Z[im[-1],j]=-1
 for j,i in enumerate(ix):Z[i,len(im)-1+j]=1
 Q=np.linalg.qr(Z)[0];eig=np.linalg.eigvalsh(Q.T@H@Q)
 end=np.where((x<1e-5)|(x>1-1e-5))[0]
 return {'energy':E,'interior_tangent_H_min':float(eig[0]),'endpoint_H_min':float(min(np.diag(H)[m.n:][end])) if len(end) else None,'negative_endpoint_radii_kpc':(m.r.numpy()[end[np.diag(H)[m.n:][end]<-1e-7]]*m.rm).tolist(),'qualified':'Finite-grid diagnostics; small residuals required before eigenvalues certify stationarity.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();data=json.loads(Path(args.input).read_text());out=[]
 for i,r in enumerate(data['runs']):
  a=audit(r);a['index']=i;out.append(a)
 Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
