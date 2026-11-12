"""LWB1R grade: reads lwb1r.json and lwb1r_MUTATE_MU1.json, applies LWB1's frozen lines, writes lwb1r_grade.json/.out.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'lwb1r.json'))); M = json.load(open(os.path.join(HERE, 'lwb1r_MUTATE_MU1.json')))
V = ['J', 'KiDS', 'DES', 'HSCY3', 'K+D']
BR = ['pimax_80', 'pimax_100', 'pimax_inf', 'pointmass', 'wpcorr0.5', 'rp_column', 'Rmin_5', 'Rmin_12', 'cut_edges', 'no_magnification', 'N1', 'Ntail0', 'camb_halofit']
def base(lab): return lab.split(' (')[0]
lines, g = [], dict(gating={}, foot={})
ka = dict(V1=R['V1']['pass_'], V2=R['V2']['pass_'], V3=R['V3']['pass_'], V4=R['V4']['pass_'])
g['gating'] = ka; lines.append(f"gating known answers: {ka}; V1b xi vs brute force max |rel| {max(abs(v) for v in R['V1b_xi_vs_bruteforce_rel'].values()):.4f}")
v5 = R['V5']['rows']; S8pub = 0.794
for foot in ('canonical', 'alt'):
    F = R['foot'][foot]; t = F['target_s8']; Om = F['Omega_m']; out = {}
    pim = {k: base(F[k]['J']['label']) for k in ('primary', 'pimax_80', 'pimax_100')}
    stable = len(set(pim.values())) == 1
    lines.append(f"\n== {foot}: target sigma8 {t:.4f}, Omega_m {Om:.5f}; J label at pi_max 40/80/100: {list(pim.values())} stable={stable}")
    lines.append("vector | sigma8_best +- width | gap | chi2/dof p | label (exact profile best, half-width)")
    for v in V:
        r = F['primary'][v]
        lab = r['label'] if (all(ka.values()) and stable) else 'NO VERDICT (gate)'
        flips = [b for b in BR if base(F[b][v]['label']) != base(r['label'])]
        # reference-offset row: theory S8 reading shifted by the pipeline's own Planck offset on the same vector
        off = S8pub - v5[v]['S8']                                  # how far this pipeline reads the Planck spectrum below 0.794
        S8b = r['best'] * math.sqrt(Om / 0.3); wS = r['width'] * math.sqrt(Om / 0.3); S8t = t * math.sqrt(Om / 0.3)
        g_off = (S8t - (S8b + off)) / wS
        out[v] = dict(best=r['best'], width=r['width'], gap=r['gap'], p=r['p'], chi2=r['chi2'], dof=r['dof'], label=lab,
                      exact=(r['exact_best'], r['exact_width']), fragile_under=flips, gap_after_reference_offset=g_off,
                      brackets={b: (round(F[b][v]['best'], 4), round(F[b][v]['width'], 4), round(F[b][v]['gap'], 2), F[b][v]['label']) for b in BR})
        lines.append(f"{v:6s} | {r['best']:.4f} +- {r['width']:.4f} | {r['gap']:+.2f} | {r['chi2']:.1f}/{r['dof']} p {r['p']:.3f} | "
                     f"{lab}{' FRAGILE' if flips else ''} ({r['exact_best']:.4f}, {r['exact_width']:.4f}); offset-shifted gap {g_off:+.2f}")
        if flips: lines.append(f"         label moves under: " + ', '.join(f"{b} -> {F[b][v]['label']} (g {F[b][v]['gap']:+.2f})" for b in flips))
    m = M['foot'][foot]['primary']['J']['best'] / F['primary']['J']['best']
    out['MU1_J_ratio'] = m; out['MU1_bites'] = abs(m - 0.85) <= 0.02 and base(M['foot'][foot]['primary']['J']['label']) != base(F['primary']['J']['label'])
    lines.append(f"MU1 (every Delta Sigma x 0.85): J sigma8 ratio {m:.4f} (line 0.85 +- 0.02); J label -> {M['foot'][foot]['primary']['J']['label']}; bites={out['MU1_bites']}")
    lines.append("brackets on J: " + '; '.join(f"{b} {F[b]['J']['best']:.4f}+-{F[b]['J']['width']:.4f} g {F[b]['J']['gap']:+.2f}" for b in BR))
    g['foot'][foot] = out
lines.append("\nV5 reference (Planck 2018 CAMB halofit, same pipeline): " + '; '.join(f"{v} S8 {v5[v]['S8']:.3f} +- {v5[v]['S8_width']:.3f} ({v5[v]['n_comb_widths_vs_0794']:+.2f} comb. widths vs 0.794)" for v in V))
lines.append(f"V5 sigma8 ratio best/Planck: " + '; '.join(f"{v} {v5[v]['sigma8'] / R['V5']['sigma8_planck']:.3f}" for v in V))
lines.append(f"V4 pooled slope c {R['V4']['pooled_c']:.4f} +- {R['V4']['sigma']:.4f} ({R['V4']['nsig']:.2f} sigma); V3 null n-sigma " + ', '.join(f"{k} {R['V3'][k]['nsig']:+.2f}" for k in ('KiDS', 'DES', 'HSCY3', 'J')))
lines.append(f"V2 sigma8 of P_lin0 on an independent grid {R['V2']['sigma8_independent_grid']:.5f}; lens z {R['zL']}; n_DS {R['n_ds']}, n_wp {R['n_wp']}")
txt = '\n'.join(lines); print(txt)
open(os.path.join(HERE, 'lwb1r_grade.out'), 'w').write(txt + '\n')
json.dump(g, open(os.path.join(HERE, 'lwb1r_grade.json'), 'w'), indent=1, default=float)
