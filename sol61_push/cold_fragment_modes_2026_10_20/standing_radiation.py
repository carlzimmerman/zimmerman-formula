"""Natural scalar loss of a normalized real standing quadrupole, not a merger.

Compute only new ell=0,2 responses. Reuse the pinned completed ell=4 source
response by exact linear amplitude scaling, with both opposite chiralities.
"""
from pathlib import Path
import json, sys, math, time, resource, hashlib
import numpy as np
from scipy.sparse import diags
from radial_tools import operators, P
from outgoing_library import outgoing_solve

mode_dir, profiles, prior_file, out = map(Path, sys.argv[1:5])
start = time.monotonic()
prior = json.loads(prior_file.read_text())
rows, checks = [], []
def ck(name, value):
    checks.append({'name': name, 'pass': bool(value)})

C44 = math.sqrt(5/(14*math.pi))
C0 = 1/math.sqrt(4*math.pi)
C2 = -math.sqrt(5)/(7*math.sqrt(math.pi))
C4 = 1/(14*math.sqrt(math.pi))

# Independent deterministic angular quadrature of all five projected terms.
x, wx = np.polynomial.legendre.leggauss(64)
phi = np.arange(64)*2*math.pi/64
xx = x[:, None]
e2 = np.exp(-2j*phi)[None, :]
y22 = math.sqrt(15/(32*math.pi))*(1-xx*xx)*e2
y2m2 = y22.conj()
H = (y22+y2m2)/math.sqrt(2)
y00 = np.ones_like(H)/math.sqrt(4*math.pi)
y20 = math.sqrt(5/(16*math.pi))*(3*xx*xx-1)*np.ones_like(H)
y40 = 3/(16*math.sqrt(math.pi))*(35*xx**4-30*xx**2+3)*np.ones_like(H)
y44 = 3/16*math.sqrt(35/(2*math.pi))*(1-xx*xx)**2*np.exp(-4j*phi)[None, :]
y4m4 = y44.conj()
def angular_integral(a):
    return np.sum(wx[:, None]*a)*2*math.pi/len(phi)
reconstructed = C0*y00+C2*y20+C4*y40+C44*(y44+y4m4)/2
angular_error = float(np.max(abs(H*H-reconstructed)))
ck('standing angular norm one', abs(angular_integral(abs(H)**2)-1)<1e-13)
ck('standing H is real', np.max(abs(H.imag))<1e-14)
ck('all five H squared coefficients reconstruct pointwise', angular_error<1e-13)
for label, yy, expected in [('00',y00,C0),('20',y20,C2),('40',y40,C4),('44',y44,C44/2),('4-4',y4m4,C44/2)]:
    ck('quadrature coefficient '+label,abs(angular_integral(H*H*yy.conj())-expected)<1e-13)
dH = (-2j*y22+2j*y2m2)/math.sqrt(2)
ck('zero integrated standing angular momentum factor',abs(angular_integral(H*dH))<1e-13)
ck('angular negative control detects wrong C2 sign',np.max(abs(H*H-(reconstructed-2*C2*y20)))>.01)
ck('ell4 total standing weight 18/35',abs((C4/C44)**2+.5-18/35)<1e-15)

def scaled_cached(summary, factor, m):
    v = {}
    for name in ['Omega','omega','ell','Q','L','N','dr']:
        v[name] = summary[name]
    v['m'] = m
    for name in ['K_edge_total','K_continuum_total','K_source_work','force_radial_L2_squared','response_radial_L2_squared','E_edge_total','Q_edge_total']:
        v[name] = summary[name]*factor*factor
    v['Jz_edge_total'] = m/v['Omega']*v['K_edge_total']
    v['source_work_relative_difference'] = summary['source_work_relative_difference']
    v['linear_relative_residual'] = summary['linear_relative_residual']
    v['channels'] = []
    for old in summary['channels']:
        c = dict(old)
        for name in ['K_edge','K_continuum_amplitude','E_edge','Q_edge']:
            c[name] *= factor*factor
        c['Jz_edge'] = m/v['Omega']*c['K_edge']
        v['channels'].append(c)
    v['provenance'] = 'exact linear source scaling of pinned prior ell4 response; no repeated solve'
    v['source_factor_relative_to_chiral_44'] = factor
    return v

for Q in [80000,160000]:
    for L,N in [(40.,399),(60.,599),(60.,1199)]:
        tag = f'Q{Q}_L{int(L)}_N{N}'
        cache = np.load(mode_dir/(tag+'.npz'))
        base = operators(profiles/f'Q{Q}.npz',Q,L,N,0)
        r, dr = base['r'], base['dr']
        W2 = base['W']+diags(np.tile(6/r**2,5))
        z = cache['mode'].reshape(-1)
        Om, om = float(cache['Omega']), float(cache['omega'])
        ck(tag+' matched grid',np.max(abs(r-cache['r']))<1e-13)
        ck(tag+' matched background omega',abs(base['record']['omega']-om)<1e-13)
        ck(tag+' matched relaxed fields',np.max(abs(np.array(base['fields'])-cache['background_fields']))<1e-12)
        kappa = float(dr*np.real(Om*Om*np.vdot(z,z)+np.vdot(z,W2@z)))
        oscillatory = dr*(np.dot(z,W2@z)-Om*Om*np.dot(z,z))
        ck(tag+' unit K for standing angular norm',abs(kappa-1)<1e-8)
        ck(tag+' no spurious oscillating K term',abs(oscillatory)<1e-7)
        f,b,h = base['fields']
        u,s,xi,v,t = cache['mode']/r
        F = math.sqrt(2)*f
        g,a,M,lam = P['g'],P['a'],P['M_chi'],P['lambda']
        Nquad = np.array([
            lam*F*(3*u*u+v*v)+math.sqrt(2)*g*(s*u+t*v)+a*xi*u,
            g/math.sqrt(2)*(u*u-v*v),
            .5*(-.75*M+6*h)*xi*xi+.5*a*(u*u+v*v),
            2*lam*F*u*v+math.sqrt(2)*g*(-s*v+t*u)+a*xi*v,
            math.sqrt(2)*g*u*v])
        source = -C44*r*Nquad
        ck(tag+' action source equals normalized cached source',np.linalg.norm(source-cache['source'])/np.linalg.norm(source)<1e-13)
        comps = {}
        for ell, coefficient in [(0,C0),(2,C2)]:
            op = dict(base)
            op['ell'] = ell
            op['W'] = base['W']+diags(np.tile(ell*(ell+1)/r**2,5))
            force = (source*(coefficient/C44)).reshape(-1)
            response = outgoing_solve(op,2*Om,force,P,m=0)
            val = response['summary']
            ck(tag+f' ell{ell} positive natural power',val['K_continuum_total']>0)
            ck(tag+f' ell{ell} only positive Psi open',[x['name'] for x in val['channels'] if x['open']]==['Psi+'])
            ck(tag+f' ell{ell} source-work balance',val['source_work_relative_difference']<1e-6)
            ck(tag+f' ell{ell} linear residual',val['linear_relative_residual']<1e-8)
            ck(tag+f' ell{ell} zero intrinsic J',abs(val['Jz_edge_total'])<1e-20)
            half = outgoing_solve(op,2*Om,.25*force,P,m=0)['summary']
            ck(tag+f' ell{ell} half parent amplitude fourth-power flux',abs(half['K_edge_total']/val['K_edge_total']-1/16)<1e-10)
            comps[f'ell{ell}_m0'] = val
            np.savez_compressed(out/f'response_{tag}_ell{ell}.npz',r=r,y=response['y'].reshape(5,N),force=force.reshape(5,N),Omega=2*Om)
        old = next(x for x in prior['rows'] if x['Q_target']==Q and x['L']==L and x['N']==N)
        ck(tag+' cached harmonic frequency matches',abs(old['Omega']-2*Om)<1e-13)
        ck(tag+' cached parent mode frequency matches',abs(old['Omega_parent']-Om)<1e-13)
        ck(tag+' cached source norm matches',abs(old['force_radial_L2_squared']/(dr*np.sum(abs(source)**2))-1)<1e-12)
        comps['ell4_m0'] = scaled_cached(old,C4/C44,0)
        comps['ell4_m+4'] = scaled_cached(old,.5,4)
        comps['ell4_m-4'] = scaled_cached(old,.5,-4)
        totals = {key:float(sum(c[key] for c in comps.values())) for key in ['K_edge_total','K_continuum_total','K_source_work','E_edge_total','Q_edge_total','Jz_edge_total']}
        gamma = totals['K_continuum_total']
        ck(tag+' total source-work balance',abs(totals['K_edge_total']-totals['K_source_work'])/totals['K_edge_total']<1e-6)
        ck(tag+' net outgoing intrinsic J cancels',abs(totals['Jz_edge_total'])<1e-20)
        ck(tag+' total charge over K ratio',abs(totals['Q_edge_total']/totals['K_edge_total']*(2*Om)-1)<1e-8)
        ck(tag+' total lab E over K ratio',abs(totals['E_edge_total']/totals['K_edge_total']/(1+om/(2*Om))-1)<1e-8)
        gamma4 = old['gamma_for_unit_K_mode']
        ck(tag+' reused ell4 contribution exact',abs(sum(comps[x]['K_continuum_total'] for x in ['ell4_m0','ell4_m+4','ell4_m-4'])/gamma4-18/35)<1e-13)
        row = {'Q_target':Q,'L':L,'N':N,'omega':om,'Omega_parent':Om,'K_normalization':kappa,'oscillatory_K_coefficient_abs':float(abs(oscillatory)),
               'source_tag':tag+'.npz','components':comps,**totals,'gamma_for_unit_K_standing_mode':gamma,
               'gamma_relative_to_pure_chiral':gamma/gamma4,'half_time_for_K0_1':1/gamma,
               'weak_rate_ratio_for_K0_1':gamma/Om,
               'ell0_fraction':comps['ell0_m0']['K_continuum_total']/gamma,
               'ell2_fraction':comps['ell2_m0']['K_continuum_total']/gamma,
               'ell4_fraction':(18/35)*gamma4/gamma}
        rows.append(row)
        print(json.dumps({k:row[k] for k in ['Q_target','L','N','gamma_for_unit_K_standing_mode','gamma_relative_to_pure_chiral','half_time_for_K0_1','Jz_edge_total']}),flush=True)

for Q in [80000,160000]:
    a,b,c = [next(x for x in rows if x['Q_target']==Q and x['L']==L and x['N']==N) for L,N in [(40.,399),(60.,599),(60.,1199)]]
    ck(f'Q{Q} standing total box convergence',abs(a['gamma_for_unit_K_standing_mode']/b['gamma_for_unit_K_standing_mode']-1)<.05)
    ck(f'Q{Q} standing total mesh convergence',abs(b['gamma_for_unit_K_standing_mode']/c['gamma_for_unit_K_standing_mode']-1)<.05)
rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
ck('measured RSS below 1GB',rss<1_000_000_000)
result = {'scope':'Natural scalar second-harmonic loss coefficient for the specified unit-K standing quadrupole with zero net intrinsic angular momentum.',
          'conventions':{'parent':'z=A[Z H exp(+iOmega t)+c.c.]/r; H=(Y22+Y2-2)/sqrt2, unit angular norm, dphiY=-imY',
                         'normalization':'K_parent=A^2, same normalized radial Z as cached chiral mode; cross-time energy coefficient vanishes by skew G',
                         'squared_angular_coefficients':{'ell0_m0':C0,'ell2_m0':C2,'ell4_m0':C4,'ell4_m+4':C44/2,'ell4_m-4':C44/2},
                         'loss':'dK/dt=-gamma K^2 to leading weak, slowly varying single-standing-pattern approximation; no fixed-Q remnant'},
          'angular_reconstruction_max_error':angular_error,'new_response_solves':'ell0 and ell2 plus half-amplitude controls only; ell4 reused by exact amplitude scaling',
          'cached_ell4_results_sha256':hashlib.sha256(prior_file.read_bytes()).hexdigest(),'rows':rows,'checks':checks,'n_checks':len(checks),
          'all_checks_pass':all(x['pass'] for x in checks),'peak_rss_bytes_macos':rss,'runtime_seconds':time.monotonic()-start,
          'limits':['No actual merger mode excitation, capture probability or partition of the stationary binding gap',
                    'No complete nonlinear time-domain decay or proof of a stable invariant one-mode standing subspace',
                    'No galactic orbital angular momentum export or four-dwarf mass-budget closure',
                    'Outgoing positive charge requires slow background/remnant charge adjustment',
                    'Finite box/mesh controls are not an interval-certified continuum bound; physical unit scale not fixed']}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
raise SystemExit(0 if result['all_checks_pass'] else 1)
