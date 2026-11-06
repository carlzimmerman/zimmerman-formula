#!/usr/bin/env python3
"""QX10 iter_3 (FROZEN_CRITERIA.md c1f0cadb7a): the flagship SPARC grade (QX8 pipeline and its committed exact-field
corrections T, imported read-only) with each galaxy's sector profile (iter_2 method A, a0 law on) added.
  python3 qx10_i3.py <cell|K1|MUTATE>   -> part_<cell>.json   (cells C1..C4; K1 = zero sector; MUTATE = lambda_0 1e-3 Mpc)
  python3 qx10_i3.py grade              -> qx10_i3.json/.out, qx10_i3_MUTATE.json/.out
kappa = 1/2 FITTED; not theory closed. Footings never pooled."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field"))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_06", "QX10_window_hardening", "iter_2_capture_dynamics"))
argv0 = sys.argv; sys.argv = [argv0[0]]
import qx8 as Q8                     # read-only: loader, mask, weights, fit_one, pooled, line, nu, UPS, NODES, PARTS
import qx10_i2 as S                  # iter_2 static solver (method A), constants
sys.argv = argv0
KPC_S = Q8.KPC_S; GK = S.GK; ACC = S.ACC


def galaxy_Md(q, U, lam0_kpc, a0k):
    """sector M_d(<R) at the data radii for one galaxy at mass-to-light U (method A, host = sphericalised V_bar)."""
    R = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + U * q["Vdisk"] ** 2 + 1.4 * U * q["Vbul"] ** 2
    Mr = np.maximum.accumulate(np.clip(VB2 * R / GK, 0, None))
    m = q["meta"]; Mtot = max(float(Mr[-1]), U * m["L36"] * 1e9 + 1.33 * m["MHI"] * 1e9)
    if Mtot <= 0: return np.zeros(len(R)), 0.0
    good = Mr > 0
    rk = R[good] if good.any() else R[-1:]; mk = Mr[good] if good.any() else np.array([Mtot])
    host = S.profile_from(list(rk), list(mk), Mtot, float(R[-1]) * 1.0001 if Mtot > mk[-1] else float(R[-1]) * 1.0001)
    sol = S.solve_static(host, S.FCAP * S.R * Mtot, S.K_of(lam0_kpc), S.r_ta(Mtot), a0k)
    return np.array([S.Mdust_at(sol, x) for x in R]), sol["retained"]


def part(which):
    GALS = Q8.load_sparc(); out = {}
    lam = {"K1": None, "MUTATE": 1.0}.get(which, S.CELLS.get(which, (None,))[0])
    if which.startswith("C"): lam = S.CELLS[which][0] * 1e3
    for foot, a0 in Q8.FOOT.items():
        a0k = a0 / ACC; rows = []
        for q in GALS:
            if lam is None:
                rows.append(dict(name=q["name"], Md=[[0.0] * len(q["R"]) for _ in Q8.NODES], kept=[0.0] * len(Q8.NODES))); continue
            Ms, kept = [], []
            for U in Q8.NODES:
                md, ret = galaxy_Md(q, float(U), lam, a0k); Ms.append([float(x) for x in md]); kept.append(float(ret))
            rows.append(dict(name=q["name"], Md=Ms, kept=kept))
        out[foot] = rows
        print(which, foot, "done", flush=True)
    json.dump(out, open(os.path.join(HERE, f"part_{which}.json"), "w"))


def grade_one(which, GALS):
    P = json.load(open(os.path.join(HERE, f"part_{which}.json"))); res = {}
    lU = np.log(Q8.UPS); lN = np.log(Q8.NODES)
    for foot, a0 in Q8.FOOT.items():
        parts = [dict(np.load(os.path.join(Q8.PARTS, foot, f"{i:03d}.npz"), allow_pickle=False)) for i in range(len(GALS))]
        rows = []; nkeep = 0
        for q, pt, pr in zip(GALS, parts, P[foot]):
            assert pr["name"] == q["name"]
            Tn = pt["T"]; Tf = np.array([np.interp(lU, lN, Tn[:, j]) for j in range(Tn.shape[1])])     # (npts, nups)
            Mn = np.array(pr["Md"])                                                                     # (nodes, npts)
            Mf = np.array([np.interp(lU, lN, Mn[:, j]) for j in range(Mn.shape[1])])                   # (npts, nups)
            gd = GK * Mf / (q["R"][:, None] ** 2) * ACC                                                # m/s^2
            gN = q["GB"] + gd
            lg = np.log10(np.maximum(Q8.nu(gN / a0) * gN, 1e-300)) + Tf
            rows.append(Q8.fit_one(q, lg)); nkeep += int(max(pr["kept"]) > 1e-3 * 1e9)
        st = Q8.pooled(rows); res[foot] = dict(rms=st["rms"], U_median=st["U_median"], line=Q8.line(st), n_galaxies_keep_sector=nkeep)
    return res


def grade():
    OUT = []; Pp = lambda s="": (print(s, flush=True), OUT.append(str(s)))
    GALS = Q8.load_sparc(); qx8 = json.load(open(os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "qx8.json")))
    Pp("QX10 iter_3: flagship SPARC grade (QX8 pipeline + its exact-field T) with the sector's galaxy profiles (iter_2 method A).")
    Pp("kappa = 1/2 FITTED; not theory closed. Footings never pooled. Line: rms <= 0.110 and 0.50 <= median U <= 0.80.")
    RES = dict(lane="QX10 iter_3", criteria="c1f0cadb7a", note="kappa = 1/2 FITTED; not theory closed")
    k1 = grade_one("K1", GALS); RES["K1"] = k1; ok1 = True
    for foot in Q8.FOOT:
        ref = qx8["footings"][foot]
        rx = ref.get("exact", ref.get("st_ex", {})); rr, ru = rx.get("rms"), rx.get("U_median")
        d = abs(k1[foot]["rms"] - rr) if rr is not None else float("nan"); du = abs(k1[foot]["U_median"] - ru) if ru is not None else float("nan")
        ok = (d <= 1e-4) and (du <= 1e-4); ok1 &= bool(ok)
        Pp(f"K1 {foot}: zero sector rms {k1[foot]['rms']:.5f} @ {k1[foot]['U_median']:.2f} vs QX8 exact {rr} @ {ru} -> {'PASS' if ok else 'FAIL'}")
    RES["K1_pass"] = bool(ok1); RES["cells"] = {}
    for c in S.CELLS:
        r = grade_one(c, GALS); RES["cells"][c] = r; r["pass_"] = bool(all(r[f]["line"] for f in Q8.FOOT))
        Pp(f"{c}: " + "; ".join(f"{f} rms {r[f]['rms']:.4f} @ U {r[f]['U_median']:.2f} ({r[f]['n_galaxies_keep_sector']} galaxies keep sector mass) -> {'PASS' if r[f]['line'] else 'FAIL'}" for f in Q8.FOOT))
    m = grade_one("MUTATE", GALS); mb = bool(all(not m[f]["line"] for f in Q8.FOOT))
    json.dump(dict(MUTATE=m, bites=mb, note="kappa = 1/2 FITTED; not theory closed"), open(os.path.join(HERE, "qx10_i3_MUTATE.json"), "w"), indent=1)
    mo = "; ".join(f"{f} rms {m[f]['rms']:.4f} @ U {m[f]['U_median']:.2f} -> {'PASS' if m[f]['line'] else 'FAIL'}" for f in Q8.FOOT) + f" -> {'BITES' if mb else 'DOES NOT BITE'}"
    open(os.path.join(HERE, "qx10_i3_MUTATE.out"), "w").write("MUTATE (lambda_0 1e-3 Mpc, sector in every galaxy): " + mo + "\n")
    Pp("MUTATE (lambda_0 1e-3 Mpc): " + mo)
    RES["MUTATE_bites"] = mb
    RES["labels"] = {c: ("NO VERDICT" if not (ok1 and mb) else ("PASS" if RES["cells"][c]["pass_"] else "FAIL")) for c in S.CELLS}
    Pp("Labels: " + "; ".join(f"{c} {l}" for c, l in RES["labels"].items()))
    json.dump(RES, open(os.path.join(HERE, "qx10_i3.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "qx10_i3.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    if sys.argv[1] == "grade": grade()
    else: part(sys.argv[1])
