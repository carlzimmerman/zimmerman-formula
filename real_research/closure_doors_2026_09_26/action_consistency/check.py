#!/usr/bin/env python3
"""Action-level static, ADM and Ward identities with explicit scope."""
import argparse,json
from pathlib import Path
import sympy as s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
    checks={}
    def exact(name,r):
        v=s.simplify(r);assert v==0,(name,v);checks[name]={'passed':True,'residual':str(v)}
    x,y=s.symbols('x y',positive=True)
    Phi=(x*x+2*y*y)/2
    g=s.Matrix([s.diff(Phi,x),s.diff(Phi,y)])
    r=s.sqrt(g.dot(g));mu=1-s.exp(-r)
    curl=s.simplify(s.diff(mu*g[1],x)-s.diff(mu*g[0],y))
    exact('AQUAL_flux_curl',curl+2*x*y*s.exp(-r)/r)
    control=curl.subs({x:1,y:1})
    assert control.is_negative
    checks['non_spherical_algebraic_Newtonian_field_control']={'passed':True,'curl_at_1_1':str(control)}

    # Pointwise ADM Legendre transform, h_ij=delta_ij, N=sqrt(h)=1,
    # common positive action prefactor suppressed. Six independent symmetric jets.
    lam=s.symbols('lambda',real=True)
    aa,bb,cc,dd,ee,ff=s.symbols('a b c d e f',real=True)
    K=s.Matrix([[aa,dd,ee],[dd,bb,ff],[ee,ff,cc]])
    tr=s.trace(K);L=s.trace(K*K)-lam*tr**2
    P=K-lam*tr*s.eye(3) # pi for hdot=2K, with appropriate symmetric pairing
    reconstructed=P-lam/(3*lam-1)*s.trace(P)*s.eye(3)
    for i in range(3):
        for j in range(i,3):exact(f'ADM_velocity_inverse_{i}{j}',reconstructed[i,j]-K[i,j])
    H=2*s.trace(P*K)-L
    Htarget=s.trace(P*P)-lam/(3*lam-1)*s.trace(P)**2
    exact('ADM_Legendre_Hamiltonian',H-Htarget)
    exact('ADM_trace_degeneracy',s.trace(P)-(1-3*lam)*tr)
    exact('ADM_conformal_Hessian',s.diff(L.subs({aa:aa,bb:aa,cc:aa,dd:0,ee:0,ff:0}),aa,2)-6*(1-3*lam))

    # Explicit covariant scalar toy: omitted gate equation leaves energy exchange.
    # Flat signature(-,+), L=+1/2 q_t²−1/2 q_x²−F(z)V(q)
    #                         +1/2 z_t²−1/2 z_x².
    t,zx=s.symbols('t x',real=True)
    q=s.Function('q')(t,zx);z=s.Function('z')(t,zx)
    F=s.Function('F');V=s.Function('V')
    qt,qx,zt,zz=s.diff(q,t),s.diff(q,zx),s.diff(z,t),s.diff(z,zx)
    E_q=s.diff(q,t,2)-s.diff(q,zx,2)+F(z)*s.diff(V(q),q)
    E_z=s.diff(z,t,2)-s.diff(z,zx,2)+s.diff(F(z),z)*V(q)
    energy=(qt**2+qx**2+zt**2+zz**2)/2+F(z)*V(q)
    flux=-qt*qx-zt*zz
    exact('total_energy_Ward_identity',s.diff(energy,t)+s.diff(flux,zx)-qt*E_q-zt*E_z)
    sector_energy=(qt**2+qx**2)/2+F(z)*V(q)
    sector_flux=-qt*qx
    exact('external_gate_energy_exchange',s.diff(sector_energy,t)+s.diff(sector_flux,zx)-qt*E_q-V(q)*s.diff(F(z),z)*zt)
    # Negative control: pretending z has its free equation omits a source.
    free_z=s.diff(z,t,2)-s.diff(z,zx,2)
    residual=s.simplify(s.diff(energy,t)+s.diff(flux,zx)-qt*E_q-zt*free_z)
    exact('omitted_gate_variation_residual',residual-V(q)*s.diff(F(z),z)*zt)

    output={'result':'exact static, ADM Legendre and gate-Ward identities verified',
            'checks':checks,'expressions':{'flux_curl':str(curl),'ADM_Hamiltonian':str(Htarget),
                                          'gate_exchange':str(residual)},
            'scope':['ADM lambda!=1/3, positive common prefactor; no full functional constraint algebra derived',
                     'Off-shell two-scalar toy demonstrates exchange mechanism; it is not the gravity completion',
                     'Nonzero curl rules out an algebraic gradient identification, not all QUMOND/AQUAL relations'],
            'non_claims':['No GR degree-of-freedom count from appearance','No matter-conservation failure claimed for minimally coupled covariant matter','No observational fit']}
    p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
if __name__=='__main__':main()
