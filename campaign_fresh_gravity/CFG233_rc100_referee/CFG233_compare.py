"""CFG233 COMMITTED vs CORRECTED comparison table (reads the saved results JSONs; post-run, labelled)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["DATA"] = "committed"
from CFG233_common import HERE
import CFG233_common as C
C.SUF = ""
sys.stdout = C.Tee(os.path.join(HERE, "CFG233_compare.out"))
def J(name, D): return json.load(open(os.path.join(HERE, f"{name}__{D}_results.json")))
out = {}
def row(label, fn):
    vals = []
    for D in ("COMMITTED", "CORRECTED"):
        try: vals.append(fn(D))
        except Exception as e: vals.append(f"n/a({type(e).__name__})")
    print(f"| {label} | {vals[0]} | {vals[1]} |")
print("| quantity | COMMITTED | CORRECTED |\n|---|---|---|")
m = lambda D: J("CFG233_main", D)
c = lambda D: m(D)["cells"]["canonical/nu_mono"]
row("n / RC41 matched", lambda D: f"100 / {len(m(D)['rc41_unmatched'])} unmatched of 41 -> {41-len(m(D)['rc41_unmatched'])} matched")
row("delta_flat slope [CI] (nu_mono, canonical)", lambda D: f"{c(D)['slope_flat']:+.4f} [{c(D)['ci_flat'][0]:+.4f},{c(D)['ci_flat'][1]:+.4f}]")
row("delta_rival slope [CI]", lambda D: f"{c(D)['slope_rival']:+.4f} [{c(D)['ci_rival'][0]:+.4f},{c(D)['ci_rival'][1]:+.4f}]")
row("bootstrap SD flat / rival", lambda D: f"{c(D)['sd'][0]:.4f} / {c(D)['sd'][1]:.4f}")
row("expected: rival-true delta_flat / flat-true delta_rival", lambda D: f"{c(D)['exp_rival_true_flat']:+.4f} / {c(D)['exp_flat_true_rival']:+.4f}")
row("z-scores: flat vs flat / flat vs rival / rival vs flat / rival vs rival", lambda D: f"{c(D)['z_flat_vs_flat']:+.2f} / {c(D)['z_flat_vs_rival']:+.2f} / {c(D)['z_rival_vs_flat']:+.2f} / {c(D)['z_rival_vs_rival']:+.2f}")
row("classes in the 4 cells", lambda D: ", ".join(f"{k}:{v['cls']}" for k, v in m(D)["cells"].items()))
row("levels flat / rival (median [CI])", lambda D: f"{m(D)['levels']['flat'][0]:+.3f} [{m(D)['levels']['flat'][1][0]:+.3f},{m(D)['levels']['flat'][1][1]:+.3f}] / {m(D)['levels']['rival'][0]:+.3f} [{m(D)['levels']['rival'][1][0]:+.3f},{m(D)['levels']['rival'][1][1]:+.3f}]")
row("low-z half flat median", lambda D: f"{m(D)['halves']['low']['flat'][0]:+.3f}")
for k, lab in (("a_RC41", "(a) RC41"), ("b_other", "(b) other"), ("c_gbar<3a0", "(c) g_bar<3a0"), ("d_thin_disc_Mbar", "(d) thin-disc M_bar")):
    row(f"{lab}: n; flat med, slope [CI]; rival slope; class", lambda D, k=k: (lambda s: f"{s['n']}; {s['med_flat']:+.3f}, {s['slope_flat']:+.3f} [{s['ci_flat'][0]:+.3f},{s['ci_flat'][1]:+.3f}]; {s['slope_rival']:+.3f}; {s['cls']}")(m(D)["sens"][k]))
a = lambda D: J("CFG233_attack_a", D)
row("a1: residual SD of log g_bar(f) on log g_bar(Freeman M_bar), corr", lambda D: f"{a(D)['a1']['resid_sd']:.3f} dex, {a(D)['a1']['corr']:.3f}")
row("a1: z-slope of log g_bar(f) - log g_geom [CI]", lambda D: f"{a(D)['a1']['ts_slope']:+.4f} [{a(D)['a1']['ts_ci'][0]:+.3f},{a(D)['a1']['ts_ci'][1]:+.3f}]")
row("G1 gas slope b (dex/z) and n", lambda D: f"{a(D)['G1']['b']:+.3f} (n={a(D)['G1']['n']})")
row("t_data (PHIBSS - authors)", lambda D: f"{a(D)['phibss']['t_data']:+.3f} +/- {a(D)['phibss']['se_t']:.3f}")
row("gas-grid plausible band: cells with both tensions >= 3 sigma (G1 / G2)", lambda D: f"{a(D)['band_G1']['surv']}/9 / {a(D)['band_G2']['surv']}/9")
row("data-informed t_data row: flat, rival slope; class", lambda D: f"{a(D)['data_t_data']['slope_flat']:+.3f}, {a(D)['data_t_data']['slope_rival']:+.3f}; {a(D)['data_t_data']['cls']} (tensions {abs(a(D)['data_t_data']['T_flat_vs_rival']):.1f}/{abs(a(D)['data_t_data']['T_rival_vs_rival']):.1f})")
row("break-even gas tilt t* (G1); zero-gas flat slope shift; M_bar tilt tau* total dex; V_c tilt q* total dex", lambda D: f"{a(D)['breakeven']['gas_t_G1'][0]:+.3f}; {a(D)['breakeven']['zero_gas_G1'][0]-a(D)['base']['slope_flat']:+.3f} (needed {a(D)['base']['exp_R_flat']-a(D)['base']['slope_flat']:+.3f}); {a(D)['breakeven']['tau'][0]*1.91:.3f}; {a(D)['breakeven']['q'][0]*1.91:.3f}")
for tot in ("0.15", "0.2", "0.25", "0.26", "0.3"):
    row(f"M_bar tilt total {tot} dex: flat slope; tension flat-vs-0 / rival-vs-flat-exp; class", lambda D, tot=tot: (lambda o: f"{o['slope_flat']:+.3f}; {o['T_flat_vs_flat']:+.1f} / {o['T_rival_vs_flat']:+.1f}; {o['cls']}")(a(D)["tau_scan"][tot]))
row("pressure s=1: flat slope; s=3", lambda D: f"{a(D)['pressure']['1.0']['slope_flat']:+.3f}; {a(D)['pressure']['3.0']['slope_flat']:+.3f}")
for seed, tag in ((233, ""), (234, "_seed234")):
    b = lambda D, tag=tag: J("CFG233_attack_b" + tag, D)
    row(f"b seed {seed}: c=1,t=0: P(flat-truth slope<=obs) / P(rival-truth ...)", lambda D: f"{b(D)['grid']['c1.0/t0.0']['flat']['p_flat_le_obs']:.3f} / {b(D)['grid']['c1.0/t0.0']['rival']['p_flat_le_obs']:.4f}")
    row(f"b seed {seed}: plausible-band Gaussian LR (rival/flat) max, cells >=1/3", lambda D: f"{max(v[0] for v in b(D)['lrs'].values()):.2f}, {sum(v[0]>=1/3 for v in b(D)['lrs'].values())}/9 (worst cell {max(b(D)['lrs'], key=lambda k: b(D)['lrs'][k][0])})")
    row(f"b seed {seed}: post-freeze tau_total=0.26: rival-truth mean slopes; box-frac rival / flat", lambda D: f"{b(D)['postfreeze']['0.26']['rival']['mean'][0]:+.3f}/{b(D)['postfreeze']['0.26']['rival']['mean'][1]:+.3f}; {b(D)['postfreeze']['0.26']['rival']['box']:.2f} / {b(D)['postfreeze']['0.26']['flat']['box']:.2f}")
    row(f"b seed {seed}: marginal LR(rival/flat), tilt prior sd 0.05 / 0.10 / 0.20 / 0.40", lambda D: " / ".join(f"{b(D)['postfreeze']['marginal_LR'][k]:.3g}" for k in ("0.05", "0.1", "0.2", "0.4")))
cc = lambda D: J("CFG233_attack_c", D)
row("c: s_R by kernel (mono, P2, simple; canonical)", lambda D: " / ".join(f"{cc(D)['kernels']['canonical/'+k]['s_R']:+.4f}" for k in ("nu_mono", "P2", "simple")))
row("c: worst change of a rival tension (line 1 sigma)", lambda D: f"{cc(D)['worst_tension_change']:.2f}")
row("c: joint-bootstrap flat-vs-rival sigma (const / joint) and z", lambda D: f"{cc(D)['joint']['sd_const1']:.4f} / {cc(D)['joint']['sd_joint1']:.4f}; {cc(D)['joint']['obs1']/cc(D)['joint']['sd_const1']:+.2f} / {cc(D)['joint']['obs1']/cc(D)['joint']['sd_joint1']:+.2f}")
d = lambda D: J("CFG233_attack_d", D)
row("d1: non-RC41 flat slope [CI]; class", lambda D: f"n={d(D)['d1']['n']}: {d(D)['d1']['flat']:+.3f} [{d(D)['d1']['ci_flat'][0]:+.3f},{d(D)['d1']['ci_flat'][1]:+.3f}]; {d(D)['d1']['cls']}")
row("d4ii: flat-truth mock slope mean (none / gbar range / drop f<0.01), seed 233; P(<=-0.027)", lambda D: " / ".join(f"{d(D)['d4ii'][k+'/seed233']['mean']:+.4f}" for k in ("none", "gbar_in_range", "drop_f<0.01")) + f"; {d(D)['d4ii']['none/seed233']['p_le_027']:.3f}")
row("d4i: OLS z-slope alone / with log g_bar in the model (all 100)", lambda D: f"{d(D)['d4i_all 100']['ols_z_alone']:+.3f} / {d(D)['d4i_all 100']['ols_z_partial']:+.3f}")
e = lambda D: J("CFG233_attack_e", D)
row("e1 map: usable cells; W-flat / W-none / W-mixed / W-rival", lambda D: f"{e(D)['map']['usable']}; " + " / ".join(str(e(D)['map']['counts'].get(k, 0)) for k in ("W-flat", "W-none", "W-mixed", "W-rival")))
row("e2 LOO: flat slope range; classes", lambda D: f"{e(D)['loo']['min']:+.4f}..{e(D)['loo']['max']:+.4f}; {e(D)['loo']['classes']}")
row("e3 boot seeds 233/234: share flat>0", lambda D: f"{e(D)['boot233']['share_pos']:.4f} / {e(D)['boot234']['share_pos']:.4f}; class {e(D)['boot233']['cls']}/{e(D)['boot234']['cls']}")
row("e4 permutation p: flat; rival (axis / full)", lambda D: f"{e(D)['perm']['p_flat']:.3f}; {e(D)['perm']['p_rival_axis']:.5f} / {e(D)['perm']['p_rival_full']:.3f}")
row("e5 honest total tension (sigma_t 0.05/0.10/0.20): flat-side / rival-side", lambda D: " | ".join(f"{e(D)['honest'][k]['tot_f']:.2f}/{e(D)['honest'][k]['tot_r']:.2f}" for k in ("0.05", "0.1", "0.2")))
row("e5 decomposition SD of modified flat slope: gas t / V_c q / M* tau / pressure", lambda D: " / ".join(f"{v['sd']:.4f}" for v in e(D)['honest_decomp'].values()))
row("62-vs-38 flat slope difference (sigma)", lambda D: f"{e(D)['diff62_38']['obs']:+.4f} ({e(D)['diff62_38']['obs']/e(D)['diff62_38']['sd']:+.2f})")
