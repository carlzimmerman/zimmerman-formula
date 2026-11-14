#!/usr/bin/env python3
"""CSD1 supply S-ref (FROZEN_CRITERIA.md section 2): the cosmological reference layout as the delivered charge.
For each footing and z in (0, 2.2, 3.0, 4.4): over FRZ1's halo grid (galaxy regime, v_vir <= v*(z)), M_b = Mb_fold / h
(FZS1's rule), R_k from XJ1's shell files (k = 1, 2, 3 and 0.5 R_fold, comoving as FZS1 converts), and
D_k = C_R(R_k) / C_B(R_k) = s, N_in / N_out = C_B'(R_k) / C_R'(R_k), the equal-charge radius (largest r <= r_ta with
C_R >= C_B) over R_fold, and D against the pure phantom. Interpolated in log M_b to the nine masses.
KA5: XJ1's stored s (min, max) for Ec2 / Ec3 at z 2.2 / 3.0 / 4.4 reproduced (a) by XJ1's own exact_fn, read-only, and
(b) by this lane's evaluation of C_R and C_B from FRZ1's primitives (M_L, phantom), not through layout().
TW4 (argument 'mutate'): R_2 used where R_3 is asked; KA5's Ec3 reproduction must fail.
  nice -n 19 python3 -I -B csd1_ref.py [mutate] -> csd1_ref.json / .out (csd1_ref_MUTATE.*)
Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
XJ1 = os.path.join(REPO, "closure_2026_11_14", "XJ1_exact_junction_zero_velocity_surface")
sys.path.insert(0, XJ1)
import xj1_lib2 as XL                                            # read-only
MUT = len(sys.argv) > 1 and sys.argv[1] == "mutate"
OUT = []
def P(*x):
    s = " ".join(str(y) for y in x); print(s, flush=True); OUT.append(s)

X = XL.X; Z = X.rec(); F = Z["F"]; Lb = Z["L"]
XL.install()
FB, h = F["FB"], F["h"]; M_L, phantom, a0c, Xsh, v_vir = F["M_L"], F["phantom"], F["a0c"], F["Xsh"], F["v_vir"]
COL = {1: 5, 2: 6, 3: 7, "half": 2}
MASSES = [8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5]

def own_C(hb, foot, r):
    """C_R and C_B of FRZ1's galaxy layouts ('Rb', 'B'; gal_scope lag) from the primitives, for r <= r_ta."""
    a0 = a0c(foot); Xs = Xsh(foot); Rs, Ms = hb["rta"], hb["Mta"]
    Mcold = (1 - FB) * Ms; Mb = Mcold / Xs
    rin = np.minimum(np.asarray(r, float), Rs)
    CR = Mcold * M_L(hb, rin) / Ms
    ph = np.minimum(phantom(np.full_like(rin, Mb), rin, a0), Mcold)
    rem = max(Mcold - float(min(phantom(np.array([Mb]), np.array([Rs]), a0)[0], Mcold)), 0.0)
    CB = ph + rem * rin / Rs
    return CR, CB, ph

def rk_com(hb, foot, z, k):
    col = COL[3 if (MUT and k == 3) else k]
    mult = 0.5 if k == "half" else 1.0
    return XL.rsurf_com(hb, foot, z, col, mult)

RES = dict(lane="CSD1", supply="S-ref", mutate=MUT, ka5={}, table={})
# ---------------------------------------------------------------- KA5
stored = {}
for line in open(os.path.join(XJ1, "xj1b2_grade.out")):
    m = re.match(r"\[(canonical|alt)\] (Ec2|Ec3)\s+t \(min, max\) / s \(min, max\).*", line)
    if m:
        for zz, s1, s2 in re.findall(r"z (\d\.\d): t \[[^\]]*\], s \[([0-9.e-]+), ([0-9.e-]+)\]", line):
            stored[(m.group(1), m.group(2), float(zz))] = (float(s1), float(s2))
ka5 = True; worst = 0.0
for z in (2.2, 3.0, 4.4):
    Z["set_z"](z)
    for ft in ("canonical", "alt"):
        vs = X.vstar(ft, z)
        for case, k in (("Ec2", 2), ("Ec3", 3)):
            kk = 2 if (MUT and k == 3) else k
            fn = XL.exact_fn(ft, z, vs, XL.COL_K[kk], 1.0)
            sa, sb = [], []
            for hb in Lb["HB"]:
                _, _, inf = fn(hb)
                if isinstance(inf, dict) and "s" in inf:
                    sa.append(inf["s"])
                    R = XL.rsurf_com(hb, ft, z, XL.COL_K[kk], 1.0)
                    CR, CB, _ = own_C(hb, ft, np.array([R])); sb.append(float(CR[0] / CB[0]))
            Z["CUR"][0] = 0.0
            st = stored[(ft, case, z)]
            da = max(abs(min(sa) / st[0] - 1), abs(max(sa) / st[1] - 1)); db = max(abs(min(sb) / st[0] - 1), abs(max(sb) / st[1] - 1))
            worst = max(worst, da, db); okk = da <= 1e-9 and db <= 1e-9; ka5 = ka5 and okk
            P(f"KA5 [{ft}] {case} z {z}: stored s [{st[0]:.10f}, {st[1]:.10f}]; exact_fn [{min(sa):.10f}, {max(sa):.10f}] (rel {da:.1e}); "
              f"own [{min(sb):.10f}, {max(sb):.10f}] (rel {db:.1e}) -> {'PASS' if okk else 'FAIL'}")
            RES["ka5"][f"{ft}_{case}_z{z}"] = dict(stored=st, exact_fn=[min(sa), max(sa)], own=[min(sb), max(sb)], n=len(sa))
P(f"KA5 (XJ1's s range, both routes, line 1e-9): {'PASS' if ka5 else 'FAIL'} (worst {worst:.1e})")
RES["KA5"] = bool(ka5)

# ---------------------------------------------------------------- the table at the nine masses
for z in (0.0, 2.2, 3.0, 4.4):
    Z["set_z"](z)
    for ft in ("canonical", "alt"):
        vs = X.vstar(ft, z)
        rows = []
        for hb in Lb["HB"]:
            if v_vir(hb) > vs: continue
            lMb = math.log10(Z["Mb_fold"](hb, ft) / h)
            row = dict(lMb=lMb, lM200=math.log10(hb["M"]), v_vir=v_vir(hb))
            Rf = rk_com(hb, ft, z, 1)
            for k in (1, 2, 3, "half"):
                R = rk_com(hb, ft, z, k)
                if R <= 0 or R >= hb["rta"]:
                    row[f"D_{k}"] = float("nan"); row[f"NinNout_{k}"] = float("nan"); row[f"Dph_{k}"] = float("nan"); continue
                e = 1e-5
                CR, CB, ph = own_C(hb, ft, np.array([R, R * (1 + e), R * (1 - e)]))
                row[f"D_{k}"] = float(CR[0] / CB[0]); row[f"Dph_{k}"] = float(CR[0] / ph[0])
                row[f"NinNout_{k}"] = float((CB[1] - CB[2]) / (CR[1] - CR[2]))
            # AMENDMENT A1: C_R = C_B = (1 - f_b) M_ta at r_ta by construction, so the equal-charge radius is the outermost
            # sign change of C_R - C_B strictly inside 0.999 r_ta (0 if none)
            rr = np.geomspace(1e-4 * hb["rta"], 0.999 * hb["rta"], 4000)
            CR, CB, _ = own_C(hb, ft, rr); sg = np.sign(CR - CB); ch = np.where(sg[1:] != sg[:-1])[0]
            row["R_eq_over_Rfold"] = float(rr[ch.max() + 1] / Rf) if (len(ch) and Rf > 0) else 0.0
            row["CR_over_CB_at_0.999rta"] = float(CR[-1] / CB[-1])
            rows.append(row)
        lm = np.array([q["lMb"] for q in rows]); o = np.argsort(lm); lm = lm[o]; rows = [rows[i] for i in o]
        tab = {}
        for M in MASSES:
            ent = {}
            if len(lm) == 0 or M < lm[0] or M > lm[-1]:
                ent = dict(status="outside the settled haloes (reference throughout or off the grid)")
            else:
                for key in rows[0]:
                    if key == "lMb": continue
                    vals = np.array([q[key] for q in rows], float)
                    if key.startswith("D") or key.startswith("NinNout"):
                        ok = np.isfinite(vals) & (vals > 0)
                        ent[key] = float(10 ** np.interp(M, lm[ok], np.log10(vals[ok]))) if ok.sum() >= 2 else float("nan")
                    else:
                        ent[key] = float(np.interp(M, lm, vals))
                ent["status"] = "settled"
            tab[f"{M:g}"] = ent
        RES["table"][f"{ft}_z{z:g}"] = dict(vstar=vs, n_settled=len(rows), lMb_range=[float(lm[0]), float(lm[-1])] if len(lm) else None, rows=tab)
        P(f"[{ft}] z {z:g}: settled haloes {len(rows)}, log M_b {lm[0]:.2f} to {lm[-1]:.2f}; v* {vs:.1f} km/s")
        for M in MASSES:
            e_ = tab[f"{M:g}"]
            if e_["status"] != "settled":
                P(f"   log M_b {M:5.2f}: {e_['status']}"); continue
            P(f"   log M_b {M:5.2f}: D_1 / D_2 / D_3 / D_half = {e_['D_1']:.3f} / {e_['D_2']:.3f} / {e_['D_3']:.3f} / {e_['D_half']:.3f}; "
              f"N_in/N_out k3 {e_['NinNout_3']:.3f}; R_eq/R_fold {e_['R_eq_over_Rfold']:.3f}; D_3 vs phantom only {e_['Dph_3']:.3f}")
Z["CUR"][0] = 0.0
name = "csd1_ref" + ("_MUTATE" if MUT else "")
RES["note"] = "Adopts nothing. kappa = 1/2 FITTED; not theory closed."
json.dump(RES, open(os.path.join(HERE, name + ".json"), "w"), indent=1)
OUT.append("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
open(os.path.join(HERE, name + ".out"), "w").write("\n".join(OUT) + "\n")
