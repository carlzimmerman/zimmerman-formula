import math, json, numpy as np
from math import pi, sqrt
from scipy.stats import poisson

FIT = dict(canonical=dict(h=0.6740783101172539, ob=0.022356930725653812, oc=0.12094167604861616),
           alt=dict(h=0.6739978899187015, ob=0.0223368383639658, oc=0.12089295824903992))
OMG = 2.47282e-5 * (1 + 0.22711 * 3.046)   # T_cmb 2.7255, N_ur 3.046 (co1_linear.py class_B)
FRAC = 0.012

def cosmo(h, ob, oc):
    Ob, Oc, Or = ob/h**2, oc/h**2, OMG/h**2
    return {'Omega_DE': 1-Ob-Oc-Or, 'Omega_b': Ob, 'Omega_r': Or, '1+z_eq': (ob+oc)/OMG, 'h': h, 'omega_b': ob}

PURE = {'1':1., '2':2., '3':3., '4':4., 'pi':pi, 'Z':2*sqrt(8*pi/3), '8pi/3':8*pi/3, '32pi':32*pi, 'pi^2/3':pi**2/3}
U = {'': lambda x: x, 'sqrt': math.sqrt, 'sq': lambda x: x*x}
UC = dict(U, inv=lambda x: 1/x)
OPS = {'+': lambda a,b: a+b, '-': lambda a,b: a-b, '*': lambda a,b: a*b, '/': lambda a,b: a/b}

def name(u, a): return f"{u}({a})" if u else a
pleaves = {name(u,a): f(v) for a,v in PURE.items() for u,f in U.items()}

def fam1():
    out = dict(pleaves)
    for a,x in pleaves.items():
        for b,y in pleaves.items():
            for o,f in OPS.items(): out[f"{a}{o}{b}"] = f(x,y)
    return {k:v for k,v in out.items() if v > 0}

def fam2(C):
    cl = {name(u,a): f(v) for a,v in C.items() for u,f in UC.items()}
    out = {}
    for a,x in cl.items():
        for b,y in list(pleaves.items()) + list(cl.items()):
            for o,f in OPS.items():
                out[f"{a}{o}{b}"] = f(x,y); out[f"{b}{o}{a}"] = f(y,x)
    return {k:v for k,v in out.items() if v > 0}

def uniq(d):
    seen = {}
    for k,v in sorted(d.items(), key=lambda kv: len(kv[0])):
        key = round(math.log(v), 9)
        if key not in seen: seen[key] = (k, v)
    return list(seen.values())

def count(vals, T, ns):
    return int(np.sum(np.abs(vals - T) <= ns*FRAC*T))

R = {f: FIT[f]['oc']/FIT[f]['ob'] for f in FIT}
f = FIT['canonical']; C0 = cosmo(**f); C1 = cosmo(f['h'], f['ob'], f['oc']*1.05)
F1 = uniq(fam1())
F2raw = fam2(C0); F2p = fam2(C1)
# restatement: d ln E / d ln R  (R scales by 1.05)
resp = {k: math.log(F2p[k]/v)/math.log(1.05) for k,v in F2raw.items() if k in F2p and F2p[k] > 0}
F2 = uniq(F2raw)
F2_rel = [(k,v) for k,v in F2 if abs(resp.get(k, 9)) <= 0.5]
F2_res = [(k,v) for k,v in F2 if abs(resp.get(k, 0)) > 0.5]

T = R['canonical']; ctrl = [4.6, 5.0, 5.8, 6.2]
grid = [t for t in np.arange(4.40, 6.4001, 0.02) if abs(t-5.41) >= 0.15]
res = {'R': R, 'sigma_R': FRAC*T, 'inputs_canonical': C0}
for lab, L in [('fam_i_pure', F1), ('fam_ii_relations', F2_rel), ('fam_ii_restatements', F2_res)]:
    vals = np.array([v for _,v in L]); row = {'N_unique': len(L)}
    for ns in (1,2):
        obs = count(vals, T, ns); g = np.mean([count(vals, t, ns) for t in grid])
        row[f'{ns}s'] = dict(observed=obs, expected_grid=round(float(g),2),
                             controls={str(t): count(vals, t, ns) for t in ctrl},
                             poisson_p=float(poisson.sf(obs-1, g)) if g > 0 else None)
    hits = sorted([(k, v, (v-T)/(FRAC*T)) for k,v in L if abs(v-T) <= 2*FRAC*T], key=lambda x: (len(x[0]), abs(x[2])))
    row['hits'] = [(k, round(v,5), round(z,2)) for k,v,z in hits]
    res[lab] = row
# consistency numbers
Oc = f['oc']/f['h']**2; Ob = f['ob']/f['h']**2
res['consistency'] = dict(Ocold=Oc, Ob=Ob, Ocold_over_ODE=Oc/C0['Omega_DE'],
    z_cold_eq_DE=(C0['Omega_DE']/Oc)**(1/3)-1, z_matter_eq_DE=(C0['Omega_DE']/(Oc+Ob))**(1/3)-1,
    a0_over_cH0=0.5*sqrt(3*C0['Omega_DE']/(8*pi)))
# R implied by an independently measured kappa (0.551 +- 0.043, RETRACTIONS.md:40) with a0 fixed, flatness
for k_, sk in [(0.551, 0.043), (0.465, 0.076)]:
    ODE = C0['Omega_DE']*(0.5/k_)**2; Rk = (1-ODE-C0['Omega_r'])/Ob - 1
    sR = 2*ODE*(sk/k_)/Ob
    res['consistency'][f'R_from_kappa_{k_}'] = (Rk, sR, (Rk-T)/sR)
json.dump(res, open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'hunt.json'),'w'), indent=1, default=float)
for lab in ('fam_i_pure','fam_ii_relations','fam_ii_restatements'):
    r = res[lab]; print(lab, r['N_unique'], {k: r[k] for k in ('1s','2s')}); print('  hits:', r['hits'][:25])
print(json.dumps(res['consistency'], indent=1, default=float)); print(R, C0)
