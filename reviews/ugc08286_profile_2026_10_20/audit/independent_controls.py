"""Independent reconstruction and orthogonal numerical controls; no author edits."""
import argparse
import json
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import quad
from scipy.optimize import linprog

p = argparse.ArgumentParser()
p.add_argument('--output', required=True)
args = p.parse_args()
packet = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(packet))
from kernel.disk_kernel import (build_annular_kernel,
    uniform_disk_v2_per_surface_density, G_KPC_KMS2_MSUN as G)
d = np.loadtxt(packet / 'data/UGC08286_rotmod.dat')
R, V, eV, Vg, Vd, Vb, SB = d[:, :7].T
foot = json.loads((packet.parents[1] / 'real_research/derivation_chain_2026/FP0_core_postulates_results.json').read_text())['numbers']
h = .196 * 1.05**.633
beam = 6500 * np.deg2rad(30 / 3600)
cut = float(np.loadtxt(packet / 'data/UGC08286.dens')[-1, 0])
gas = Vg * np.abs(Vg)

def I(x, kind):
    # Independently locate the interpolation interval, including continuations.
    i = max(0, min(len(R)-2, np.searchsorted(R, x)-1))
    if kind == 'loglinear' or x > R[-1]:
        slope = np.log(SB[i+1]/SB[i])/(R[i+1]-R[i])
        return float(SB[i] * np.exp(slope*(x-R[i])))
    return float(max(SB[i] + (SB[i+1]-SB[i])*(x-R[i])/(R[i+1]-R[i]), 0))

def ring_force_original(r, a, z):
    # Original Newtonian angular integral, with no elliptic boundary identity.
    return G/np.pi*quad(lambda phi: r*(r-a*np.cos(phi))/
        ((r-a)**2+2*r*a*(1-np.cos(phi))+z*z)**1.5,
        0, np.pi, epsabs=2e-11, epsrel=2e-11, limit=180)[0]

def uniform_original(r, a, z):
    return quad(lambda s: 2*np.pi*s*ring_force_original(r, s, z),
        0, a, epsabs=2e-11, epsrel=2e-10, limit=100)[0]

def min_ceiling(B, low, high):
    n = B.shape[1]
    C = np.vstack([np.column_stack([B, np.zeros(len(low))]),
        np.column_stack([-B, np.zeros(len(low))]),
        np.column_stack([np.eye(n), -np.ones(n)])])
    b = np.concatenate([high, -low, np.zeros(n)])
    c = np.append(np.zeros(n), 1)
    q = linprog(c, A_ub=C, b_ub=b, bounds=(0,None), method='highs-ds')
    result = {'success': bool(q.success), 'status': int(q.status)}
    if q.success:
        y = q.ineqlin.marginals
        result.update(ceiling=float(q.x[-1]), primal_violation=float(max(0, np.max(C@q.x-b), -np.min(q.x))),
            dual_violation=float(max(0, np.max(y), np.max(C.T@y-c))),
            primal_objective=float(c@q.x), dual_objective=float(b@y), gap=float(c@q.x-b@y),
            U=q.x[:-1].tolist())
    return result

boundary=[]
for r,a,z in [(0.5,2.,.3),(3.,2.,.2),(1.7,2.,.1),(2.,2.,.25)]:
    direct=uniform_original(r,a,z)
    closed=float(uniform_disk_v2_per_surface_density(r,a,z))
    boundary.append(dict(r=r,a=a,z=z,direct=direct,closed=closed,
        relative_difference=float(abs(direct-closed)/abs(direct))))

light=[]
for kind in ('loglinear','linear'):
    for step in (beam/2,beam/4,beam/8):
        edges=np.unique(np.r_[np.arange(0,cut,step),cut,R])
        edges=edges[(edges>=0)&(edges<=cut)]
        # Direct adaptive radial integration independent of author's Gauss rule.
        L=np.array([2*np.pi*1e6*quad(lambda x: x*I(x,kind),a,b,
            epsabs=1e-8,epsrel=2e-12)[0] for a,b in zip(edges[:-1],edges[1:])])
        K=build_annular_kernel(R,edges,h,order=192)
        # Adaptive integration of the same exact boundary law, independent of
        # the fixed-node vertical integration used in the author's LP.
        Ka=build_annular_kernel(R,edges,h,method='adaptive')
        B=K*L; Ba=Ka*L
        vunit=np.sqrt(B.sum(axis=1))
        controls={}
        for name,a0 in [('canonical',foot['a0_canonical']),('alt',foot['a0_rho_total'])]:
            low=(V-eV)**4/((V-eV)**2+a0*R*3.0857e19/1e6)-gas
            high=(V+eV)**4/((V+eV)**2+a0*R*3.0857e19/1e6)-gas
            q=min_ceiling(B,low,high); qa=min_ceiling(Ba,low,high)
            if q['success']:
                U=np.array(q['U'])
                q['adaptive_prediction_change_max_v2']=float(np.max(np.abs((Ba-B)@U)))
            controls[name]={'fixed192':q,'adaptive':qa}
        light.append(dict(kind=kind,step=float(step),bins=len(L),luminosity=float(L.sum()),
            max_template_delta_v=float(np.max(np.abs(vunit-Vd))),
            rms_template_delta_v=float(np.sqrt(np.mean((vunit-Vd)**2))),
            max_template_fraction=float(np.max(np.abs(vunit/Vd-1))),
            max_abs_kernel_difference=float(np.max(np.abs(Ka-K))),
            max_sum_abs_light_weighted_difference=float(np.max(np.abs((Ka-K)*L).sum(axis=1))),
            unit_disk_adaptive_delta_v=float(np.max(np.abs(np.sqrt(Ba.sum(axis=1))-vunit))),
            ceiling_controls=controls))

# A fixed additive source geometry, independently optimized with adaptive K.
edges=np.r_[np.arange(0,8.07,beam/2),8.07]
K=build_annular_kernel(R,edges,h,order=192)
Ka=build_annular_kernel(R,edges,h,method='adaptive')
a0=foot['a0_canonical']; b=gas+.5*Vd**2
base=(b+np.sqrt(b*b+4*a0*R*3.0857e19/1e6*b))/2
def extra(K):
    C=np.r_[K,-K]*1e9; rhs=np.r_[(V+eV)**2-base,base-(V-eV)**2]
    c=np.ones(K.shape[1]); q=linprog(c,A_ub=C,b_ub=rhs,bounds=(0,None),method='highs-ds')
    result={'success':bool(q.success),'status':int(q.status)}
    if q.success:
        y=q.ineqlin.marginals
        result.update(total_mass=float(q.x.sum()*1e9),max_primal_violation=float(max(0,np.max(C@q.x-rhs),-np.min(q.x))),
            max_dual_violation=float(max(0,np.max(y),np.max(C.T@y-c))),duality_gap=float(c@q.x-rhs@y))
    return result

# Round-trip simple law over the actual observed interval range.
roundtrips=[]
for name,a0 in [('canonical',foot['a0_canonical']),('alt',foot['a0_rho_total'])]:
    for W in ((V-eV)**2,V**2,(V+eV)**2):
        b=W*W/(W+a0*R*3.0857e19/1e6)
        W2=(b+np.sqrt(b*b+4*a0*R*3.0857e19/1e6*b))/2
        roundtrips.append(float(np.max(np.abs(W-W2))))

result={'assertion_tested':'Four direct Newtonian uniform-disk controls, six independently integrated finite light reconstructions with adaptive vertical quadrature, nominal all17 one-sigma min-ceiling LPs under two fixed footings, and one fiducial extra-mass LP.',
    'boundary_controls':boundary,'light_controls':light,
    'additive_primary':{'fixed192':extra(K),'adaptive':extra(Ka),
        'max_abs_kernel_difference':float(np.max(np.abs(Ka-K)))},
    'simple_law_max_roundtrip_error_v2':max(roundtrips),
    'gas_first3_signed_v2':gas[:3].tolist(),
    'non_claims':['No full intrinsic photometric deprojection','No measured intrinsic radial M/L bound',
        'Adaptive and fixed quadrature agreement is numerical evidence, not rigorous interval integration',
        'Floating LP certificates are numerical residual checks, not exact rational proofs']}
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'boundary_relative_max':max(x['relative_difference'] for x in boundary),
    'light_summary':[{k:q[k] for k in ['kind','step','luminosity','max_template_delta_v','max_template_fraction','unit_disk_adaptive_delta_v']} for q in light],
    'additive_primary':result['additive_primary']},indent=2))
