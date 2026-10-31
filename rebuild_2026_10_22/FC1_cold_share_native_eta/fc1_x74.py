#!/usr/bin/env python3
"""FC1_cold_share_native_eta: X74's grader text with the cold-share conversion (criteria 061b2e2a1a). Called by fc1_grade.py.
    FC1_MODE=cold|sonly|none|mut X74_CF=<table> X73_FSTAR=.. X73_SLOPE=.. python3 fc1_x74.py
cold: S x f_c, mass argument M/f_c on SPARC and groups; sonly: S x f_c only; none: X74 unchanged; mut: factor 0.5. kappa = 1/2 FITTED; not theory closed."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)
X74F = os.path.join(REB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
INJ = r'''
_cf_line = "def cf_of(M): return float(np.interp(math.log10(M), CFLM, CFV))\n"
sub(_cf_line, _cf_line + """_FCN = NAT_RRAT / (1 + NAT_RRAT); _FM = os.environ.get("FC1_MODE", "cold")
FC1_F = {"cold": _FCN, "sonly": _FCN, "none": 1.0, "mut": 0.5}[_FM]; FC1_MC = {"cold": _FCN, "sonly": 1.0, "none": 1.0, "mut": 0.5}[_FM]
""")
sub('    sc = (eta_of(cf_of(M)) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2',
    '    sc = (FC1_F * eta_of(cf_of(M)) if ETA_USE["v"] == ETA else ETA_USE["v"]) * sigma_coll(tag, M)[0] * MSUNE / PC2')
sub('s, a_ = sig_core(f, tag, M200, rule); act += a_', 's, a_ = sig_core(f, tag, M200 / (FC1_MC if ETA_USE["v"] == ETA else 1.0), rule); act += a_')
sub('sc, act = sig_core(foot, "A_c2b_refit", M200 / MSUNE)', 'sc, act = sig_core(foot, "A_c2b_refit", M200 / MSUNE / (FC1_MC if ETA_USE["v"] == ETA else 1.0))')
sub("x74ok = k2x\n", """x74ok = k2x
_fb = lambda t: F3[t]["params"]["omega_cdm"] / (F3[t]["params"]["omega_b"] + F3[t]["params"]["omega_cdm"])
_n = {l: sig_core("canonical", "A_c2b_refit", 10.0 ** l)[0] / (MSUNE / PC2) / sigma_coll("A_c2b_refit", 10.0 ** l)[0] for l in (12, 13, 14)}
_k2 = [abs(solve_r0(_FCN * m * MSUNE, r, _FCN * s_) / solve_r0(m * MSUNE, r, s_) - 1) for m, r, s_ in ((1e12, 6e21, 2.0e0), (1e13, 1.2e22, 2.5e0), (1e14, 2.6e22, 5.0e0))]
RES["x74"]["fc1"] = dict(mode=_FM, F=FC1_F, MC=FC1_MC, f_c=_FCN, f_c_bgA=_fb("A_c2b_refit"), f_c_bgB=_fb("B_cfg886_bg"), S_over_Scoll=_n, k2=_k2)
P(f"FC1 mode {_FM}: F {FC1_F:.5f}, MC {FC1_MC:.5f}; f_c {_FCN:.5f}; bg A/B 1-fb {_fb('A_c2b_refit'):.5f}/{_fb('B_cfg886_bg'):.5f}; S/Sigma_coll at 1e12/13/14 {_n[12]:.3f}/{_n[13]:.3f}/{_n[14]:.3f}; solve_r0 scale identity max {max(_k2):.1e}")
""")
'''
A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + A)
exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(HERE, "x74_native_cf.py"), "__name__": "__main__"})
