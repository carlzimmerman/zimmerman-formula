"""Literal frozen-source, resolution and domain checks of selected KT39 rows."""
import argparse
import json
import math
import time
from pathlib import Path
import power_model as J

M, E, np = J.M, J.E, J.np


def grid(foot, refine, rmin, outer):
    a0 = M.C.A0[foot]
    mu = M.C.PS.mass_unit(a0)
    re = M.C.PS.log_edges(rmin, outer*300*max(60, math.sqrt(6.6e10/mu)), 30*refine)
    return M.C.PS.Grid(re, M.C.PS.theta_edges(48*refine, full=False, stretch_min=.002/refine)), mu


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selection', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    selected = json.loads(args.selection.read_text())
    cells = E.population()
    out = dict(selection=selected, rows=[], complete=False)
    started = time.monotonic()
    def save():
        args.output.write_text(json.dumps(out, indent=2, allow_nan=False)+'\n')
    for foot in ('canonical', 'alt'):
        cases = [c for c in selected['cases'] if c['footing'] == foot]
        for ref, rmin, outer in [(2,.005,1), (3,.005,1), (4,.005,1),
                                  (5,.005,1), (3,.0025,1), (3,.005,2)]:
            g, mu = grid(foot, ref, rmin, outer)
            sol = M.Solver(g, mu, M.C.A0[foot])
            model = J.Generalized(sol)
            for c in cases:
                J.set_power(c['power'])
                rho_fun, _ = M.rho_cell(cells[c['index']])
                rho = g.rho_axisym(lambda R,z: rho_fun(R,z)/mu, nq=4)
                psi = sol.LU.newton(rho)
                ph, stats = model.phantom(psi, c['ell_kpc'])
                q = sol.evaluate(psi+ph)
                recomputed = M.C.lines(q['vc'], q['K'], q['K0'], q['vc_Ou'])
                assert all(q[k] == recomputed[k] for k in (*M.GATE, 'Lh'))
                if ref == 2 and rmin == .005 and outer == 1:
                    original = c['production_score']
                    assert max(abs(q[k]-original[k])/max(abs(original[k]),1)
                               for k in ['vc','K0','cK','cO','D']) < 1e-7
                if not math.isfinite(q['h']):
                    assert q['h'] == float('inf') and not q['Lh']
                    q['h'] = None
                    q['h_status'] = 'positive infinity: fitted log-K slope is nonnegative'
                row = dict(footing=foot, power=c['power'], ell_kpc=c['ell_kpc'],
                           index=c['index'], cell=cells[c['index']], refine=ref,
                           rmin=rmin, outer=outer, score=q, source_stats=stats)
                out['rows'].append(row)
                print(foot, c['power'], c['ell_kpc'], c['index'], ref, rmin, outer,
                      {k:q[k] for k in ['vc','K0','cK','cO','D','all_four','Lh']}, flush=True)
            save()
    out['complete'] = True
    out['runtime_seconds'] = time.monotonic()-started
    save()


if __name__ == '__main__':
    main()
