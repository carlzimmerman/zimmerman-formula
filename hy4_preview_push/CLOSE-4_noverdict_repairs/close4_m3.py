#!/usr/bin/env python3
"""CLOSE-4 R2 (FROZEN_CRITERIA.md, committed alone before this file ran): DCN1's MUTATE M3 numerical half.

The frozen clause (DCN1 FROZEN_CRITERIA.md d603f1703c section 5): "drop the 1/(1+u) in A1: the sympy check must fail,
and Gamma_id^2 must disagree with route L on the KA4 sphere by more than 5 %."
Landed: sympy BITES; numerical half 2.13 % against the 5 % line -> DOES NOT BITE.

Why the line is unattainable: the mutation replaces u Phi_nn/(1+u) by u Phi_nn, so the change it can produce is capped
by u_max/(1 + u_max) over the analysis region. On the KA4 sphere u_max = 0.101, so the cap is 0.0917 of the u Phi_nn
share of Gamma_id^2 -- and the realised value is 2.13 % against the identity's own 0.036 % agreement with route L.
The 5 % line demands more than the testbed's own u allows. It is a mis-scaled line, not a failing pipeline.

R2-a (graded): on DCN1's own KA4 sphere the arm BITES iff  d1 >= 10 d0  AND  0.5 dp <= d1 <= 2 dp, with
  d0 = max_ann |Gid/GL - 1|   (the identity's own agreement with route L)
  d1 = max_ann |Gmut/GL - 1|  (the mutated identity's disagreement)
  dp = max_ann |Gmut - Gid| / |GL|  (the change the algebra predicts).
R2-b (graded): the frozen 5 % line, on the first rho_0 scale factor in {1, 3, 10, 30, 100, 300} whose KA4-sphere
  analysis annulus has sup(u) >= 1.0, where the line is attainable.

  OMP_NUM_THREADS=1 nice -n 10 python3 close4_m3.py    -> parts/m3_repaired.json, parts/m3_repaired.out

Runs DCN1's own dcn1_local.py from DCN1's folder (read-only import). Nothing in DCN1 is edited.
kappa = 1/2 FITTED; footings never pooled (the canonical footing carries the graded M3, as DCN1 ran it; the alt is
reported beside it); not theory closed; adopts nothing."""
import os, sys, json, math, warnings
warnings.filterwarnings("ignore")
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DCN1 = os.path.join(ROOT, "fable52_push", "DCN1_disc_centre_null")
sys.path.insert(0, DCN1)
import numpy as np
import dcn1_local as DL
S = DL.S
G = DL.G
KPCKMS_TO_S = 3.0857e16
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

LADDER = [1, 3, 10, 30, 100, 300]
NR = 108

def run_sphere(ft, scale):
    """One KA4 uniform sphere at N_R = 108, rho_0 scaled by `scale`. Returns every number R2 needs."""
    a0 = S.a0k(ft)
    M = 10 ** 9.4
    Rd = S.R_d_shen(M)
    _, rho0, hz = DL.thick_rho(M, Rd)
    rho0 = rho0 * scale
    fPhi, frho, fG2, fsup = DL.sphere_case(rho0, a0)
    Lb = 0.4 * 0.0131
    b = DL.Box(Lb, -Lb, Lb, NR, 2 * NR)
    PB = {k: fPhi(*v) for k, v in DL.boundary_points(b).items()}
    C0 = float(np.mean(np.concatenate([v.ravel() for v in PB.values()])))
    PB = {k: v - C0 for k, v in PB.items()}
    rho = DL.cell_average(b, frho)
    Phi, _, _ = DL.solve(b, rho, PB, a0, fPhi(b.RR, b.ZZ) - C0)
    gR, gz = DL.grad_cells(b, Phi, PB)
    A_, radd = DL.assemble(b, DL.face_coefs(b, Phi, PB, a0, gR, gz, lambda x: 1 / (1 + x)), PB)
    dp = ((A_ @ Phi.ravel() - radd).reshape(b.shape)) / (4 * np.pi * G * b.V)
    gm = np.sqrt(gR ** 2 + gz ** 2); u = gm / a0
    GL = -4 * np.pi * G * dp * u * (2 + u)                     # route L, DCN1's formula
    HRR = np.gradient(gR, b.hR, axis=0); Hzz = np.gradient(gz, b.hz, axis=1)
    HRz = 0.5 * (np.gradient(gR, b.hz, axis=1) + np.gradient(gz, b.hR, axis=0))
    nR = gR / np.maximum(gm, 1e-300); nz = gz / np.maximum(gm, 1e-300)
    Pnn = nR * nR * HRR + 2 * nR * nz * HRz + nz * nz * Hzz
    s4 = 4 * np.pi * G * rho
    Gid = (2 + u) * (u * Pnn / (1 + u) - s4)                   # the A1 identity, as frozen
    Gmut = (2 + u) * (u * Pnn - s4)                            # M3: the 1/(1+u) dropped
    ss = np.sqrt(b.RR ** 2 + b.ZZ ** 2)
    ann = (ss >= Lb / 8) & (ss <= Lb / 2)                      # DCN1's analysis annulus, unchanged
    d0 = float(np.max(np.abs(Gid[ann] / GL[ann] - 1)))
    d1 = float(np.max(np.abs(Gmut[ann] / GL[ann] - 1)))
    dpn = float(np.max(np.abs(Gmut[ann] - Gid[ann]) / np.abs(GL[ann])))
    return dict(foot=ft, scale=scale, rho0=float(rho0), u_max_annulus=float(np.max(u[ann])),
                u_cap=float(np.max(u[ann]) / (1 + np.max(u[ann]))),
                d0_identity_vs_routeL=d0, d1_mutated_vs_routeL=d1, dp_predicted=dpn,
                ratio_d1_over_d0=(d1 / d0) if d0 > 0 else None,
                ratio_d1_over_dp=(d1 / dpn) if dpn > 0 else None,
                frozen_line_5pct=bool(d1 > 0.05),
                R2a_bites=bool(d1 >= 10 * d0 and 0.5 * dpn <= d1 <= 2 * dpn))

RES = dict(lane="CLOSE-4 R2", target="DCN1 MUTATE M3, numerical half",
           frozen_clause="Gamma_id^2 must disagree with route L on the KA4 sphere by more than 5 %",
           frozen_landed="2.13 % against the 5 % line; u_max on the annulus 0.101; identity's own agreement 0.036 %",
           note="post hoc amendment to DCN1; kappa = 1/2 FITTED; not theory closed; adopts nothing",
           ladder=LADDER, N_R=NR, rows={})
for ft in ("canonical", "alt"):
    # ---- R2-a: DCN1's own KA4 sphere, unscaled
    a = run_sphere(ft, 1)
    RES["rows"].setdefault(ft, {})["R2a_KA4_sphere"] = a
    P(f"[{ft}] R2-a  KA4 sphere (scale 1): sup_ann u {a['u_max_annulus']:.4f} (cap u/(1+u) = {a['u_cap']:.4f})")
    P(f"        d0 identity vs route L {a['d0_identity_vs_routeL']:.5f}; d1 mutated vs route L {a['d1_mutated_vs_routeL']:.5f}; "
      f"dp predicted {a['dp_predicted']:.5f}")
    P(f"        d1/d0 = {a['ratio_d1_over_d0']:.1f} (line 10); d1/dp = {a['ratio_d1_over_dp']:.3f} (band 0.5 to 2) "
      f"=> R2-a {'BITES' if a['R2a_bites'] else 'DOES NOT BITE'}   (frozen 5 % line: {a['frozen_line_5pct']})")
    # ---- R2-b: the first scale factor whose annulus has sup(u) >= 1
    chosen = None
    for sc in LADDER:
        if sc == 1: continue
        r = run_sphere(ft, sc)
        P(f"        ladder x{sc}: sup_ann u {r['u_max_annulus']:.4f}")
        if r["u_max_annulus"] >= 1.0:
            chosen = r; break
    if chosen is None:
        r = run_sphere(ft, LADDER[-1])
        RES["rows"][ft]["R2b_ladder"] = dict(chosen=None, last=r, note="no ladder factor reached sup_ann u >= 1")
        P(f"[{ft}] R2-b  NO ladder factor in {LADDER} reached sup_ann u >= 1; last x{LADDER[-1]} gives "
          f"{r['u_max_annulus']:.4f}. R2-b NOT EVALUABLE.")
    else:
        RES["rows"][ft]["R2b_ladder"] = dict(chosen=chosen)
        P(f"[{ft}] R2-b  first factor with sup_ann u >= 1: x{chosen['scale']} (sup_ann u {chosen['u_max_annulus']:.4f}): "
          f"d0 {chosen['d0_identity_vs_routeL']:.5f}, d1 {chosen['d1_mutated_vs_routeL']:.5f}, dp {chosen['dp_predicted']:.5f} "
          f"=> frozen 5 % line {'MET, BITES' if chosen['frozen_line_5pct'] else 'NOT MET, DOES NOT BITE'}")
os.makedirs(os.path.join(HERE, "parts"), exist_ok=True)
json.dump(RES, open(os.path.join(HERE, "parts", "m3_repaired.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "parts", "m3_repaired.out"), "w").write("\n".join(OUT) + "\n")
