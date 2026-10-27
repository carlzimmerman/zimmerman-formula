import argparse,json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from scipy.integrate import quad

sx=np.array([[0,1],[1,0]],complex)
sy=np.array([[0,-1j],[1j,0]],complex)
sz=np.diag([1.,-1.])

def slab(n,e,full):
    z=np.arange(n)-(n-1)/2
    h=np.kron(np.eye(n),sz-.2*e*sx)
    if full: h-=np.diag(np.repeat(e*z,2))
    hop=(-sz-1j*sy)/2
    for i in range(n-1):
        h[2*i:2*i+2,2*i+2:2*i+4]=hop
        h[2*i+2:2*i+4,2*i:2*i+2]=hop.conj().T
    w,v=eigh(h,check_finite=False)
    occ=v[:,:n].reshape(n,2,n)
    density=np.sum(abs(occ)**2,axis=(1,2))
    p_internal=.2*np.einsum('iaj,ab,ibj->',occ.conj(),sx,occ).real
    p_site=float(np.dot(z,density-1))
    return dict(n=n,field=e,full_position=full,energy=float(w[:n].sum()),
                charge_residual=float(density.sum()-n),
                transferred_half_charge=float((density[n//2:]-1).sum()),
                max_local_charge=float(np.max(abs(density-1))),
                internal_dipole=float(p_internal),site_dipole=p_site,
                conjugate_dipole=float(p_internal+(p_site if full else 0)),
                level_gap=float(w[n]-w[n-1]))

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    rows=[]
    for n in [32,64,128]:
        for e in [.01,.03,.1]:
            for full in [False,True]:
                r=slab(n,e,full);delta=1e-6
                numerical=-(slab(n,e+delta,full)['energy']-slab(n,e-delta,full)['energy'])/(2*delta)
                r['energy_derivative_error']=abs(numerical-r['conjugate_dipole'])
                rows.append(r)
    # Hydrogenic radial functions in a_B units; angular integral 1/sqrt(3).
    radial=quad(lambda r: (2*np.exp(-r))*(r*np.exp(-r/2)/(2*np.sqrt(6)))*r**3,0,np.inf)[0]/np.sqrt(3)
    exact=256/(243*np.sqrt(2))
    # Physical symmetries of the constructed Bloch band.
    def h(k):
        return (2-np.cos(k[0])-np.cos(k[1])-np.cos(k[2]))*sz+np.sin(k[2])*sy
    ks=[np.array([.3,.7,1.1]),np.array([1.2,-.4,.2])]
    sym=max(max(np.max(abs(sz@h(k)@sz-h(-k))),np.max(abs(h(k).conj()-h(-k)))) for k in ks)
    result=dict(rows=rows,hydrogenic_position_integral=radial,integral_error=abs(radial-exact),
                zero_field_symmetry_error=float(sym),
                maximum_energy_derivative_error=max(r['energy_derivative_error'] for r in rows),
                statement='Prescribed-field finite slab, no self-consistent screening times or galaxy fractions.')
    assert abs(radial-exact)<1e-12
    assert sym<1e-14
    assert max(abs(r['charge_residual']) for r in rows)<1e-10
    assert result['maximum_energy_derivative_error']<1e-5
    assert max(r['max_local_charge'] for r in rows if not r['full_position'])<1e-9
    Path(a.output).write_text(json.dumps(result,indent=2)+'\n')
    print('radial',radial,'max work derivative error',result['maximum_energy_derivative_error'])
    for r in rows: print(r['n'],r['field'],r['full_position'],r['transferred_half_charge'],r['site_dipole'])
if __name__=='__main__': main()
