#!/usr/bin/env python3
"""TS1 (FROZEN_CRITERIA.md 4b352f2a37) cosmology: WM1's scripts executed read-only from origin's WM1 dir with in-process patches:
nu -> 1 + (nu - 1) <s>_w (T6, <s>_w from parts/core.json), and for M-split two ncdm species (188.7 eV and 18.87 eV, omega/2 each;
seeding uses the mean of the two species' transfers). Outputs go to TS1's parts/ with a variant suffix.
    python3 ts1_cosmo.py <cosmo|seed|hc1|cmb> <MW|MSPLIT> [footing]
kappa = 1/2 FITTED; not theory closed; adopts nothing."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WM1 = os.path.join(REPO, "closure_2026_11_09", "WM1_warm_component_law_baryons")
W, VAR = sys.argv[1], sys.argv[2]; FOOT = sys.argv[3] if len(sys.argv) > 3 else "canonical"; os.environ["SS1_FOOT"] = FOOT; os.environ["WM1_V"] = "W"
SW = json.load(open(os.path.join(HERE, "parts", "core.json")))["T6_ensemble"]["s_w_delta2"]; SPLIT = (VAR == "MSPLIT"); SUF = "_" + VAR
def sub(src, old, new, n=1):
    assert src.count(old) == n, (old, src.count(old)); return src.replace(old, new)
fn = {"cosmo": "wm1_cosmo.py", "seed": "wm1_seed.py", "hc1": "wm1_hc1.py", "cmb": "wm1_cmb.py"}[W]
src = open(os.path.join(WM1, fn)).read()
pre = f"TS1_SW = {SW!r}\nTS1_SPLIT = {SPLIT!r}\n"
if W == "cosmo":
    src = sub(src, "y = np.maximum(y, 1e-30); return 0.5 + np.sqrt(0.25 + 1.0 / y)", "y = np.maximum(y, 1e-30); return 1 + (0.5 + np.sqrt(0.25 + 1.0 / y) - 1) * TS1_SW")
    src = sub(src, 'if V == "W":\n    s5 = open', 'if False:   # TS1: KA-W2 passed in WM1 with this code unchanged; skipped (nu is patched)\n    s5 = open')
    if SPLIT: src = sub(src, "WP = dict(BASE, omega_cdm=1e-7, N_ncdm=1, m_ncdm=M_EV, T_ncdm=TNCDM, deg_ncdm=1.0, tol_ncdm_bg=1e-10)",
                        "WP = dict(BASE, omega_cdm=1e-7, N_ncdm=2, m_ncdm=f'{M_EV},{M_EV/10}', T_ncdm=f'{0.71611 * (0.5 * OD * 93.14 / M_EV) ** (1 / 3)},{0.71611 * (0.5 * OD * 93.14 / (M_EV / 10)) ** (1 / 3)}', deg_ncdm='1,1', tol_ncdm_bg=1e-10)")
    src = sub(src, 'f"cosmo_{V}_{FOOT}.json"', 'f"cosmo{SUF}_{FOOT}.json"')
elif W == "seed":
    src = sub(src, "1e-30); return 0.5 + np.sqrt(0.25 + 1 / y)", "1e-30); return 1 + (0.5 + np.sqrt(0.25 + 1 / y) - 1) * TS1_SW")
    src = sub(src, 'RELICS = {"W": m_for(MHM0), "MW1": m_for(10 * MHM0), "MW2": m_for(MHM0 / 10), "SRC107.5": 107.5}', 'RELICS = {"W": m_for(MHM0)}')
    if SPLIT:
        src = sub(src, "    else: p.update({'omega_cdm': 1e-7, 'N_ncdm': 1, 'm_ncdm': m_ev, 'T_ncdm': 0.71611 * (OD * 93.14 / m_ev) ** (1 / 3), 'deg_ncdm': 1.0, 'tol_ncdm_bg': 1e-10})",
                  "    else: p.update({'omega_cdm': 1e-7, 'N_ncdm': 2, 'm_ncdm': f'{m_ev},{m_ev/10}', 'T_ncdm': f'{0.71611 * (0.5 * OD * 93.14 / m_ev) ** (1 / 3)},{0.71611 * (0.5 * OD * 93.14 / (m_ev / 10)) ** (1 / 3)}', 'deg_ncdm': '1,1', 'tol_ncdm_bg': 1e-10})")
        src = sub(src, "dc = t['d_ncdm[0]'] if warm else t['d_cdm']", "dc = (0.5 * (t['d_ncdm[0]'] + t['d_ncdm[1]'])) if warm else t['d_cdm']")
    src = sub(src, "Mc.struct_cleanup(); Mc_cl.struct_cleanup()", "Mc.struct_cleanup()")
    src = sub(src, 'f"seed_{FOOT}.json"', 'f"seed{SUF}_{FOOT}.json"')
elif W == "hc1":
    assert SPLIT
    src = sub(src, "    om = 0.11958060485606123 if MODE == \"hc1\" else 5.41 * ob; T = 0.71611 if MODE == \"hc1\" else 0.71611 * (om * 93.14 / MEV) ** (1 / 3)",
              "    om = 5.41 * ob; T = f'{0.71611 * (0.5 * om * 93.14 / MEV) ** (1 / 3)},{0.71611 * (0.5 * om * 93.14 / (MEV / 10)) ** (1 / 3)}'")
    src = sub(src, "'omega_cdm': 1e-7, 'N_ncdm': 1, 'm_ncdm': MEV, 'T_ncdm': T, 'deg_ncdm': 1.0,", "'omega_cdm': 1e-7, 'N_ncdm': 2, 'm_ncdm': f'{MEV},{MEV/10}', 'T_ncdm': T, 'deg_ncdm': '1,1',")
    src = sub(src, 'REL = json.load(open(os.path.join(HERE, "parts", "cosmo_W_canonical.json")))["relic"]', 'REL = json.load(open(os.path.join(HERE, "parts", "cosmo_MW_canonical.json")))["relic"]')
    src = sub(src, 'f"g9_{MODE}.json"', 'f"g9{SUF}.json"')
elif W == "cmb":
    assert SPLIT
    src = sub(src, "        mev, T = relic(V); p.update({'omega_cdm': 1e-7, 'N_ncdm': 1, 'm_ncdm': mev, 'T_ncdm': T, 'deg_ncdm': 1.0, 'tol_ncdm_bg': 1e-10})",
              "        mev, T = relic(V); p.update({'omega_cdm': 1e-7, 'N_ncdm': 2, 'm_ncdm': f'{mev},{mev/10}', 'T_ncdm': f'{0.71611 * (0.5 * OD * 93.14 / mev) ** (1 / 3)},{0.71611 * (0.5 * OD * 93.14 / (mev / 10)) ** (1 / 3)}', 'deg_ncdm': '1,1', 'tol_ncdm_bg': 1e-10})")
    src = sub(src, 'for V in ("W", "MW1", "MW2", "W3", "Wthird"):', 'for V in ("W",):')
    src = sub(src, 'f"cmb7a_{FOOT}.json"', 'f"cmb7a{SUF}_{FOOT}.json"')
if W == "hc1": sys.argv = [os.path.join(HERE, fn), "W"]
ns = {"__file__": os.path.join(HERE, fn), "__name__": "__main__", "SUF": SUF}
exec(compile(pre + src, f"ts1_patched_{fn}", "exec"), ns)
