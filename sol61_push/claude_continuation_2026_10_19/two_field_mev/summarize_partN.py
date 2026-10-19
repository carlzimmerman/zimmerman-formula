"""Evaluate the PLAN N2 acceptance criteria C1-C5, GR calibration and transfer criterion."""
import glob, json, math, os, sys
import numpy as np
from common import dump

D = 'results/partN'
GR_SIGMA0 = 2.303832927e-6          # stability/run_018 lowest radial angular frequency (full GR)
runs = {}
for fn in sorted(glob.glob(f'{D}/*.json')):
    tag = os.path.basename(fn)[:-5]
    if tag.startswith('summary'):
        continue
    runs[tag] = json.load(open(fn))

# merge split runs (_a, _b) into one record per discretization
merged = {}
for tag, r in runs.items():
    base = tag[:-2] if tag.endswith(('_a', '_b')) else tag
    m = merged.setdefault(base, dict(sectors={}, background=r['background'], newton=r['newton'],
                                     dr=r['dr'], disc=r['disc'], rbox=r['rbox'], N=r['N'],
                                     vk=r.get('vakhitov_kolokolov'), coercivity=r.get('coercivity')))
    for s in r['sectors']:
        m['sectors'][s['l']] = s

ls = sorted(set().union(*[set(m['sectors']) for m in merged.values()]))
table = {}
for base, m in merged.items():
    table[base] = {l: dict(sigma=m['sectors'][l]['sigma_lowest'][:4], Splus=m['sectors'][l]['Splus_lowest'][:3],
                           Sminus=m['sectors'][l]['Sminus_lowest'][:2],
                           Splus_constrained=m['sectors'][l].get('Splus_constrained_lowest', [None])[:2],
                           translation_ratio=m['sectors'][l].get('translation_eig_over_next'),
                           translation_overlap=m['sectors'][l].get('translation_overlap'),
                           phase_res=m['sectors'][l].get('phase_kernel_rel_residual'),
                           n_neg_Splus=m['sectors'][l]['Splus_negative_count'],
                           s2_natural=m['sectors'][l]['s2_natural'][:3])
                   for l in m['sectors']}


def nontrivial_sigma2(sec, l):
    s2 = sec['sigma2_lowest']
    return s2[1:] if l == 1 else s2


crit = {}
# C1 signs
signs_ok = True
sign_detail = {}
for l in ls:
    sg = {b: [int(np.sign(x)) for x in nontrivial_sigma2(m['sectors'][l], l)[:3]] for b, m in merged.items() if l in m['sectors']}
    sp = {b: [int(np.sign(x)) for x in (m['sectors'][l].get('Splus_constrained_lowest') or m['sectors'][l]['Splus_lowest'])[(1 if l == 1 else 0):3]] for b, m in merged.items() if l in m['sectors']}
    allsg = set(tuple(v) for v in sg.values()) | set()
    ok = len(set(tuple(v) for v in sg.values())) == 1 and len(set(tuple(v) for v in sp.values())) == 1
    sign_detail[l] = dict(sigma2_signs=sg, energy_signs=sp, identical=ok)
    signs_ok &= ok
crit['C1_signs_identical'] = signs_ok
crit['C1_detail'] = sign_detail
# C2 finest D1 vs finest D2
d1 = 'fd_R8000_N2000'
d2 = 'dvr_R8000_N1500'
c2 = {}
c2ok = True
for l in ls:
    if l in merged[d1]['sectors'] and l in merged[d2]['sectors']:
        a = np.array(nontrivial_sigma2(merged[d1]['sectors'][l], l)[:3])
        b = np.array(nontrivial_sigma2(merged[d2]['sectors'][l], l)[:3])
        rel = np.abs(np.sqrt(np.abs(a)) / np.sqrt(np.abs(b)) - 1)
        c2[l] = rel.tolist()
        c2ok &= bool(np.all(rel <= 1e-3))
crit['C2_D1_vs_D2_freq_rel'] = c2
crit['C2_pass'] = c2ok
# C3 translation
c3 = {b: dict(ratio=m['sectors'][1].get('translation_eig_over_next'), overlap=m['sectors'][1].get('translation_overlap'),
              Splus_l1=m['sectors'][1]['Splus_lowest'][0], dr=m['dr'], disc=m['disc'])
      for b, m in merged.items() if 1 in m['sectors']}
crit['C3_translation'] = c3
crit['C3_pass'] = all(abs(v['ratio']) <= 1e-2 for v in c3.values())
# C4 stationarity, phase
crit['C4_newton_rel'] = {b: m['newton']['rel'] for b, m in merged.items()}
crit['C4_phase_kernel'] = {b: m['sectors'][0].get('phase_kernel_rel_residual') for b, m in merged.items() if 0 in m['sectors']}
crit['C4_pass'] = all(v <= 1e-10 for v in crit['C4_newton_rel'].values())
# C5 H1
crit['C5_H1'] = {b: m['background']['H1'] for b, m in merged.items()}
crit['C5_pass'] = all(h['f_positive'] and h['x_positive'] and h['f_decreasing'] and h['x_decreasing'] for h in crit['C5_H1'].values())
# GR calibration
cal = {}
for b, m in merged.items():
    if 0 in m['sectors']:
        s0 = m['sectors'][0]['sigma_lowest'][0]
        cal[b] = dict(sigma0_NR=s0, rel_diff_vs_GR=s0 / GR_SIGMA0 - 1)
crit['GR_calibration'] = cal
crit['GR_calibration_pass'] = all(abs(v['rel_diff_vs_GR']) <= 1e-2 for v in cal.values())
# transfer criterion
prof = np.load('../../full_two_field_2026_10_19/equilibria/mixed_G1em8_x04.npz')
z, v = prof['z'], prof['v']
eps = max(1 - float(prof['omega']), float(np.max(2 * v[1:] / z[1:])), float(abs(1 - prof['alpha'][0])))
bg = merged[d1]['background']
G = 1e-8
scale = 4 * math.pi * G * bg['q_c']
tr = {}
for l in ls:
    s2min = min(nontrivial_sigma2(merged[d1]['sectors'][l], l))
    tr[l] = dict(lowest_nonsymmetry_sigma2=s2min, threshold=100 * eps * scale, margin=s2min / (100 * eps * scale))
crit['transfer'] = dict(eps=eps, eps_parts=dict(one_minus_omega=1 - float(prof['omega']), max_2GM_over_r=float(np.max(2 * v[1:] / z[1:])),
                                                 one_minus_alpha_c=float(1 - prof['alpha'][0])), per_l=tr,
                        pass_l_ge_1=all(tr[l]['margin'] > 1 for l in ls if l >= 1))
# thresholds (continuum)
crit['continuum'] = {b: dict(threshold_sigma_Phi=m['background']['threshold_sigma_Phi'],
                             threshold_sigma_X=m['background']['threshold_sigma_X'],
                             max_reported_sigma=max(max(m['sectors'][l]['sigma_lowest']) for l in m['sectors']),
                             coercivity=m['coercivity'], vk=m['vk']) for b, m in merged.items()}
out = dict(table=table, criteria=crit, runs=list(merged))
dump(f'{D}/summary_partN.json', out)
print(json.dumps({k: v for k, v in crit.items() if k.endswith('pass') or k in ('C1_signs_identical',)}, indent=1))
print(json.dumps(crit['GR_calibration'], indent=1))
print(json.dumps(crit['transfer'], indent=1, default=float))
print(json.dumps(crit['C2_D1_vs_D2_freq_rel'], indent=1))
for b in merged:
    print(b, {l: [round(x, 4) for x in table[b][l]['s2_natural']] for l in sorted(table[b])})
