"""DCN1 (reported, not graded; A5's 'null in box' report): for every P1 box, solve once at N_R 162 and locate where g_z
changes sign on the axis (the null of the field on the axis, where g_R = 0 by symmetry), its offset from the box centre in
units of L, and whether it lies in the analysis region (offset <= L/2).  Writes dcn1_nullcheck.json / .out.
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("DCN1_LSET", "P1")
import dcn1_local as D

rows = json.load(open(os.path.join(HERE, "dcn1_global_BC.json")))["rows"]
OUT = {"lane": "DCN1", "script": "dcn1_nullcheck.py", "N_R": 162, "rows": {}}
lines = []
for key, r in rows.items():
    sp = r["spec"]
    if sp["ge"] <= 0:
        continue
    M = 10 ** float(sp["logm"]); a0 = D.S.a0k(sp["foot"]); zn = r["null"]["z_null_kpc"]; L = 0.4 * abs(zn)
    fPhi, _ = D.global_interp(os.path.join(D.CACHE, r["cache"])); frho, rho0, hz = D.thick_rho(M, r["Rd_kpc"])
    b = D.Box(L, zn - L, zn + L, 162, 324)
    PB = {k: fPhi(*v) for k, v in D.boundary_points(b).items()}
    C0 = float(np.mean(np.concatenate([v.ravel() for v in PB.values()]))); PB = {k: v - C0 for k, v in PB.items()}
    Phi, res, nit = D.solve(b, D.cell_average(b, frho), PB, a0, fPhi(b.RR, b.ZZ) - C0)
    gR, gz = D.grad_cells(b, Phi, PB); u = np.sqrt(gR ** 2 + gz ** 2) / a0
    k = np.where(np.diff(np.sign(gz[0])) != 0)[0]
    zs = [float(0.5 * (b.zc[i] + b.zc[i + 1])) for i in k]
    off = [abs(z - zn) / L for z in zs]
    row = dict(spec=sp, L_kpc=L, z_box_centre_kpc=zn, axis_null_z_kpc=zs, offset_over_L=off,
               null_in_analysis_region=bool(any(o <= 0.5 for o in off)), u_min_box=float(u.min()), u_max_box=float(u.max()),
               residual=res, iterations=nit)
    OUT["rows"][key] = row
    s = (f"{key}: axis null at z {['%.6f' % z for z in zs]} kpc, offset/L {['%.3f' % o for o in off]}, in region "
         f"{row['null_in_analysis_region']}; u in box {u.min():.2e}-{u.max():.2f}")
    print(s, flush=True); lines.append(s)
OUT["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
json.dump(OUT, open(os.path.join(HERE, "dcn1_nullcheck.json"), "w"), indent=1)
open(os.path.join(HERE, "dcn1_nullcheck.out"), "w").write("\n".join(lines) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
