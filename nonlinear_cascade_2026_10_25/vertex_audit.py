"""Independent automatic third derivative of the full local density action."""
import argparse,json
from pathlib import Path
import numpy as np,torch
from vertex import vertex
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();torch.set_num_threads(1);rho=.09478717830483639;u=.2659697829626922;kappa=.0006995338357181399;L=2*np.pi;vol=L**3;xx=np.stack(np.meshgrid(*[np.arange(32)*L/32]*3,indexing='ij'),axis=-1);rows=[]
for k1,k2,phase in [(np.array([3.,0.,0.]),np.array([0.,4.,0.]),1.),(np.array([1.,0.,1.]),np.array([0.,1.,1.]),1j)]:
 ks=[k1,k2,k1+k2];z=vertex(k1,k2,rho,u,kappa,vol);ns=[];vs=[];gs=[];dns=[]
 for k,A in zip(ks,z['A']):
  j=len(ns);b=phase if j==2 else 1.;wave=b*np.exp(1j*(xx@k));B=1/(2*A);ns.append(2*np.real(A*wave)/np.sqrt(vol));vs.append(2*np.real(wave[...,None]*k*B)/np.sqrt(vol));gs.append(2*np.real(-1j*wave[...,None]*k*A/(k@k))/np.sqrt(vol));dns.append(2*np.real(1j*wave[...,None]*k*A)/np.sqrt(vol))
 ns=torch.tensor(np.array(ns));vs=torch.tensor(np.array(vs));gs=torch.tensor(np.array(gs));dns=torch.tensor(np.array(dns));eps=torch.zeros(3,dtype=torch.float64,requires_grad=True);n=torch.einsum('i,ixyz->xyz',eps,ns);vel=torch.einsum('i,ixyza->xyza',eps,vs);dg=torch.einsum('i,ixyza->xyza',eps,gs);dn=torch.einsum('i,ixyza->xyza',eps,dns);g0=torch.tensor([0.,0.,u]);uu=torch.linalg.vector_norm(g0+dg,dim=-1);E=vol*torch.mean(.5*(rho+n)*torch.sum(vel**2,dim=-1)+kappa/(8*(rho+n))*torch.sum(dn**2,dim=-1)-torch.log1p(-uu)-uu-.5*torch.sum(dg**2,dim=-1));d1=torch.autograd.grad(E,eps,create_graph=True)[0][0];d2=torch.autograd.grad(d1,eps,create_graph=True)[0][1];third=float(torch.autograd.grad(d2,eps)[0][2]);pred=2*np.real(z['V']*np.conj(phase));error=abs(third-pred)/max(abs(pred),1e-12);assert error<1e-9;rows.append({'k1':k1.tolist(),'k2':k2.tolist(),'b3_phase':str(phase),'automatic_mixed_third_derivative':third,'vertex_prediction':float(pred),'relative_error':float(error)})
out={'checks':rows,'scope':'Independent exact automatic third derivative on32^3 Fourier quadrature of full pureT local density/phase/nonlocal-response energy, compared to derived complex cubic vertex. Not a global nonlinear model.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
