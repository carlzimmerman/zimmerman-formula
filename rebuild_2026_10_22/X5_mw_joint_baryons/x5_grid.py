#!/usr/bin/env python3
"""X5_mw_joint_baryons question (i): the frozen prior box of published Milky Way baryons on P4's AQUAL solver.

Criteria FROZEN_CRITERIA.md (8e5b65bca5) §2.  175 cells per footing: Sigma_b(R0) (McKee+15 +-2 sigma) x M_bb (Portail+17
+-2 sigma, PROVISIONAL) x R_d (BH&G16 +-2 sigma).  Each cell: P4's grid / quadrature / Problem; AQUAL (L* = 0) recorded,
then the stiffened L* = 24 pc solve (the scored cell); P4's mw_obs.  Nothing is fitted; no grid refinement after results.
Run:  OMP_NUM_THREADS=1 nice -n 15 python3 x5_grid.py --foot canonical     (and --foot alt)
Outputs: x5_grid_<foot>.out, x5_grid_<foot>.json.  kappa = 1/2 FITTED; footings never pooled; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys
import json
import time
import itertools
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import x5_lib as L  # noqa: E402

foot = sys.argv[sys.argv.index("--foot") + 1]
assert foot in L.FOOTS
T0 = time.time()
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


ns = L.load_p4()
F = L.Family(ns)
vE, eE = L.eilers_target(ns)
P(f"X5 grid, footing {foot} (a0 {L.A0_SI[foot]:.4e} m/s^2); criteria {L.CRITERIA}; kappa = 1/2 FITTED")
P(f"McMillan17 at R0 {F.R0}: thin share {F.f_thin:.6f}; gas column {F.sig_gas_R0 / 1e6:.4f}; discs + gas column {F.sig_b_mcm:.4f} Msun/pc^2; "
  f"bulge-shape mass {F.M_bulge_mcm:.5e} Msun")
P(f"lines: chi2_Kz <= {L.LINE_CHI2:.3f}; |v_c - {L.VC_BRIEF}| <= {L.VC_BRIEF_LINE} and |v_c - {vE:.3f}| <= {2 * eE:.3f} km/s")
Mgas = F.gas_mass()
cells = []
P(f"\n{'Sig_b':>6} {'M_bb':>6} {'R_d':>6} | {'M*':>7} {'S11':>6} | {'K(R0)':>6} {'h':>5} {'chi2Kz':>8} {'vc(R0)':>7} {'D':>6} pass | L0 chi2 vc | res it s")
for sb, mbb, rd in itertools.product(L.SIG_B_GRID, L.MBB_GRID, L.RD_GRID):
    rhof, p = F.rho(sb, mbb, rd)
    s_all, s11 = L.columns(rhof, F.R0)
    o0, oL, info = L.solve_cell(ns, rhof, foot)
    ok, D = L.cell_pass(oL["chi2_kz"], oL["vc_R0"], vE, eE)
    Mana = p["M_thin"] + p["M_thick"] + p["M_bb"] + Mgas
    c = dict(sig_b=sb, M_bb=mbb, R_d=rd, params={k: v for k, v in p.items() if k not in ("st", "sk")},
             Sigma_b_R0_quad=s_all, Sigma_11_R0_quad=s11, M_analytic=Mana, mass_rel_err=info["Mb_Msun"] / Mana - 1,
             tag_Mstar_IN=bool(L.MSTAR_TAG[0] <= p["Mstar"] <= L.MSTAR_TAG[1]), tag_Rd_IN=bool(L.RD_TAG[0] <= rd <= L.RD_TAG[1]),
             L0=L.slim(o0), L24=oL, info=info, passes=ok, D=D)
    cells.append(c)
    P(f"{sb:6.1f} {mbb / 1e10:6.2f} {rd:6.3f} | {p['Mstar'] / 1e10:7.3f} {s11:6.2f} | {oL['K_R0']:6.2f} {oL['h']:5.2f} {oL['chi2_kz']:8.2f} "
      f"{oL['vc_R0']:7.2f} {D:6.3f} {'PASS' if ok else '  - '} | {o0['chi2_kz']:7.2f} {o0['vc_R0']:6.2f} | {max(info['res_L0'], info['res_L']):.0e} "
      f"{info['it_L0']}+{info['it_L']} {info['solve_s']}")

npass = sum(c["passes"] for c in cells)
best = min(cells, key=lambda c: c["D"])
P(f"\n{foot}: {len(cells)} cells; passing {npass}; best D {best['D']:.3f} at Sig_b {best['sig_b']}, M_bb {best['M_bb']:.3g}, R_d {best['R_d']:.4f} "
  f"(chi2_Kz {best['L24']['chi2_kz']:.2f}, v_c {best['L24']['vc_R0']:.2f})")
RES = dict(lane="X5_mw_joint_baryons", part="grid", foot=foot, criteria=L.CRITERIA, a0=L.A0_SI[foot], line_chi2=L.LINE_CHI2,
           vc_target=[vE, eE], vc_brief=[L.VC_BRIEF, L.VC_BRIEF_LINE], family=dict(f_thin=F.f_thin, sig_gas_R0=F.sig_gas_R0 / 1e6,
           sig_b_mcm=F.sig_b_mcm, M_bulge_shape=F.M_bulge_mcm, M_gas=Mgas), grid=dict(sig_b=L.SIG_B_GRID, M_bb=L.MBB_GRID, R_d=L.RD_GRID),
           n_cells=len(cells), n_pass=npass, cells=cells, runtime_s=round(time.time() - T0, 1), peak_rss_MB=round(L.rss_mb(), 1))
json.dump(RES, open(os.path.join(L.HERE, f"x5_grid_{foot}.json"), "w"), indent=1)
P(f"X5_GRID {foot} done: runtime {RES['runtime_s']} s, peak RSS {RES['peak_rss_MB']} MB")
open(os.path.join(L.HERE, f"x5_grid_{foot}.out"), "w").write("\n".join(OUT) + "\n")
