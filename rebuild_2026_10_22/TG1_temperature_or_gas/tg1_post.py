#!/usr/bin/env python3
"""TG1 POST-RESULT forecast stress, after K4 and the plant MUTATE failed; written before the split ran on data. No label moves. kappa = 1/2 FITTED; not theory closed."""
from tg1_common import *
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
def fld(a, b):
    d = a.mean(0) - b.mean(0); C = (np.cov(a.T) + np.cov(b.T)) / 2; return float(np.sqrt(d @ np.linalg.solve(C, d)))
P("F_LD: best linear axis in (Z_T, Z_G), post-result; the frozen Delta axis is not monotone in plant size. Line 3 is frozen for F, not F_LD. 'scale' re-deconvolves with KT sigma x scale, so scatter goes to intrinsic.")
for fi, f in enumerate(FEET):
    S0 = sample(f, "h0672"); P(f"{f}: sample sd t {S0['t'].std():.3f}, g {S0['g'].std():.3f}, rho {np.corrcoef(S0['t'], S0['g'])[0,1]:+.3f}; rms catalogue sigma t {np.sqrt((S0['st']**2).mean()):.3f}, g {np.sqrt((S0['sg']**2).mean()):.3f}; quantiles sigma t {np.quantile(S0['st'],[.1,.5,.9]).round(3).tolist()}")
    for k, sc in enumerate((1.0, .75, .5, .25)):
        S = dict(S0); S["st"] = S0["st"] * sc; mk = Mock(S, 0); r = run(mk, 2000 + 100 * fi + k); Ci = mk.Cint
        P(f"  scale {sc}: intrinsic sd t {Ci[0,0]**.5:.3f} g {Ci[1,1]**.5:.3f} rho {Ci[0,1]/(Ci[0,0]*Ci[1,1])**.5:+.2f}; F {r['F']:.2f}, F_LD {fld(r['HTz'], r['HGz']):.2f}, acc {r['acc']['HT']:.3f}, {r['acc']['HG']:.3f}; HT Z {np.round(r['Z_mean']['HT'],2).tolist()}, HG Z {np.round(r['Z_mean']['HG'],2).tolist()}")
    for lab, (a, b) in dict(x3=(3, 3)).items():
        mk = Mock(S0, 0); r = run(mk, 2900 + fi, a=a * mk.alpha, b=b * mk.beta); P(f"  plant {lab}: F {r['F']:.2f}, F_LD {fld(r['HTz'], r['HGz']):.2f}, acc {r['acc']['HT']:.3f}, {r['acc']['HG']:.3f}")
open(os.path.join(HERE, f"tg1_post{TAG}.out"), "w").write("\n".join(OUT) + "\n")
