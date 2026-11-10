"""SCS3 route 2: SCS2's constraint-surface pencil L_G zeta = lambda H zeta on the multi-resolution backgrounds of scs3_maps.py.
Criteria FROZEN_CRITERIA.md (eff0ae1861) section 2; amendment A1 (f51866c8d4) when SCS3_A1=1.

The forms (L_phi, L_chi, L_G) are built by SCS2's own functions, taken verbatim from scs2_route2_copy.py (the part before its
main loop is executed here; nothing is edited).  Lowest eigenvalue:
  - n <= 3000: SCS2's dense pencil (pencil_lowest), as SCS2 ran it (KA1 / KA2 reproduce SCS2's rows);
  - otherwise: shift-invert Arnoldi on T = M L_G, M = L_chi^-1 - L_phi^-1, through the sparse 3n block system
        L_chi a = L_G x,  L_phi c = L_G x,  a - c - sigma x = b   (so (T - sigma) x = b),
    stage 1 at sigma_0 = 1.02 c_lb, where c_lb = min over cells of G/J_dir <= lambda_min (H >= L_chi; the face ratio
    (G1+G2)/(J1+J2) is a mediant of the cell ratios), so no eigenvalue lies below sigma_0 and the eigenvalue nearest it is
    the lowest; stage 2 refines at sigma_1 = lambda_1 - 0.1 |lambda_1|.  The reported lambda_min is the lower of the two.
  - 3D (PL): SCS2's Rayleigh certificate (sign) and, if SCS3_PL_PENCIL=1, the same shift-invert pencil.
SCS3_SET in {AX, AXKA, PL, THICK_AX, THICK_PL}; SCS3_RES = comma list of resolutions; SCS3_PART k/n.  Preemptible (partial
json per background; SIGTERM writes and exits).  TEST lane.  Adopts nothing.  kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, time, resource, signal, glob
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("SCS2_MUTATE", "")
_src = open(os.path.join(HERE, "scs2_route2_copy.py")).read().split("\nRES = {")[0]
R2 = {"__file__": os.path.join(HERE, "scs2_route2_copy.py"), "__name__": "scs2_route2_copy"}
exec(compile(_src, "scs2_route2_copy.py", "exec"), R2)
import scs3_maps as SM          # make_grid_res is installed into scs2_aqual on import
S = SM.S

CK = S.C_KMS
A1 = os.environ.get("SCS3_A1") == "1"
SET = os.environ.get("SCS3_SET", "AX")
CACHE = os.environ.get("SCS3_CACHE", os.path.join(HERE, "_cache"))
RESL = tuple(int(x) for x in os.environ.get("SCS3_RES", "0,1,2,3").split(","))
PART = os.environ.get("SCS3_PART", "")
OUT = os.path.join(HERE, f"scs3_route2_{SET}" + ("_A1" if A1 else "") + f"_R{''.join(map(str, RESL))}"
                   + (f"_p{PART.split('/')[0]}" if PART else "") + ".json")
PARTIAL = OUT.replace(".json", "_partial.json")
RES = {"lane": "SCS3", "script": "scs3_route2.py", "criteria": "eff0ae1861", "amendment_A1": "f51866c8d4" if A1 else None,
       "set": SET, "resolutions": RESL, "rows": []}
if os.path.exists(PARTIAL):
    RES = json.load(open(PARTIAL))
DONE = {(r_["tag"], r_["m"], r_["parity"]) for r_ in RES["rows"]}


def dump(path):
    RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
    RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
    with open(path + ".tmp", "w") as fh:
        json.dump(RES, fh, indent=1, default=str)
    os.replace(path + ".tmp", path)


signal.signal(signal.SIGTERM, lambda s, f: (dump(PARTIAL), print("SIGTERM: partial written", flush=True), sys.exit(0)))


def lower_bound(bg, Gc):
    gr, gt, gp = bg["grads"]; gm = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)
    u = gm / bg["a0"]; Jpar = 1 / (1 + u) ** 2; Jperp = 1 / (1 + u)
    ghr = gr / np.maximum(gm, 1e-300); ght = gt / np.maximum(gm, 1e-300)
    Jrr = Jperp + (Jpar - Jperp) * ghr ** 2; Jtt = Jperp + (Jpar - Jperp) * ght ** 2
    ok = np.isfinite(Gc)
    c = min(np.min(Gc[ok] / Jrr[ok]), np.min(Gc[ok] / Jtt[ok]), np.min(Gc[ok] / Jperp[ok]))
    return float(c)


def pencil_si(mats, n, c_lb, k=6):
    Lp, Lc, LG = mats["phi"].tocsc(), mats["chi"].tocsc(), mats["G"].tocsc()
    lc = spla.splu(Lc); lp = spla.splu(Lp)
    def Tmv(x):
        y = LG @ x
        return lc.solve(y) - lp.solve(y)
    T = spla.LinearOperator((n, n), matvec=Tmv, dtype=float)
    I = sps.identity(n, format="csc")
    out = {}
    def stage(sigma, tag):
        B = sps.bmat([[-LG, Lc, None], [-LG, None, Lp], [-sigma * I, I, -I]], format="csc")
        t1 = time.time()
        lu = spla.splu(B, permc_spec="COLAMD")
        def opinv(b):
            return lu.solve(np.concatenate([np.zeros(2 * n), b]))[:n]
        OP = spla.LinearOperator((n, n), matvec=opinv, dtype=float)
        w = spla.eigs(T, k=k, sigma=sigma, OPinv=OP, which="LM", return_eigenvectors=False, maxiter=20000, ncv=min(n - 1, 60),
                      tol=1e-10)
        out[tag] = dict(sigma=sigma, eigs=sorted(float(x) for x in np.real(w)), max_imag=float(np.max(np.abs(np.imag(w)))),
                        lu_nnz=int(lu.L.nnz + lu.U.nnz), seconds=round(time.time() - t1, 1))
        return min(np.real(w))
    if c_lb >= 0:
        return dict(lambda_min=None, note="c_lb >= 0: no negative eigenvalue possible", c_lb=c_lb)
    l1 = stage(1.02 * c_lb, "stage1")
    l2 = stage(l1 - 0.1 * abs(l1), "stage2") if l1 < 0 else l1
    out.update(lambda_min=float(min(l1, l2)), c_lb=c_lb, method="shift-invert block")
    return out


def bg_list():
    rows = []
    if SET in ("AX", "AXKA", "THICK_AX"):
        for foot in ("canonical", "alt"):
            for lm in S.LOGM:
                if SET == "THICK_AX":
                    for ge in (0.01, 0.1):
                        rows.append(dict(group="THICK_AX", foot=foot, kind="thick", logm=lm, ge=ge, axis="z"))
                    continue
                for kind in ("expo", "kuzmin"):
                    if SET == "AXKA" and lm == "10.45":
                        rows.append(dict(group="primary", foot=foot, kind=kind, logm=lm, ge=0.0, axis="z"))
                    if SET == "AX":
                        for ge in (0.01, 0.1):
                            rows.append(dict(group="AX", foot=foot, kind=kind, logm=lm, ge=ge, axis="z"))
    elif SET in ("PL", "THICK_PL"):
        for foot in ("canonical", "alt"):
            for lm in ("9.4", "10.9"):
                for kind in (("expo", "kuzmin") if SET == "PL" else ("thick",)):
                    for ge in (0.01, 0.1):
                        rows.append(dict(group=SET, foot=foot, kind=kind, logm=lm, ge=ge, axis="x"))
    return rows


if __name__ == "__main__":
    t0 = time.time()
    todo = bg_list()
    if PART:
        kk, nn = map(int, PART.split("/")); todo = todo[kk::nn]
    for d in todo:
        for res in RESL:
            tg = SM.tag_of(d, res)
            cpath = os.path.join(CACHE, tg + os.environ.get("SCS3_CACHE_SUFFIX", "") + ".npz")
            if not os.path.exists(cpath):
                bg = S.background(d["foot"], d["kind"], d["logm"], ge=d["ge"], axis=d["axis"], res=res)
                S.save_cache(bg, cpath)
            bg = S.load_cache(cpath)
            if A1:
                SM.a1_mask(bg, d)
            g = bg["g"]
            if d["ge"] > 0:
                re = math.sqrt(S.G * bg["M"] * bg["a0"]) / (d["ge"] * bg["a0"]); crop = max(30 * bg["Rd"], 3 * re)
            else:
                crop = 30 * bg["Rd"]
            Gc = R2["G_field"](bg, "")
            axisym = g.np_ == 1
            c_lb = lower_bound(bg, Gc)
            ms = ((0, 1, 2) if res <= 1 else (0,)) if axisym else (None,)
            pars = ("even", "odd") if (g.tmode == "half" and axisym) else ("none",)
            for m in ms:
                for par in pars:
                    if (tg, m, par) in DONE:
                        continue
                    t1 = time.time()
                    mats, n = R2["build_forms"](bg, crop, m if m is not None else 0, par, Gc, axisym=axisym)
                    row = dict(tag=tg, spec=d, res=res, m=m, parity=par, n=n, c_lb=c_lb)
                    if not axisym:
                        imax = int(np.searchsorted(g.rc, crop))
                        act = np.zeros(g.shape, bool); act[R2["NMASK"]:imax] = True; act &= np.isfinite(Gc)
                        aidx = -np.ones(g.shape, int); aidx[act] = np.arange(act.sum())
                        num, ncells, lob = R2["rayleigh_3d"](mats, Gc, aidx, g.shape)
                        row.update(rayleigh_numerator=num, trial_cells=ncells, lobpcg_min=lob, negative=bool(num < 0))
                        if os.environ.get("SCS3_PL_PENCIL") == "1":
                            row["pencil"] = pencil_si(mats, n, c_lb)
                            row["lambda_min"] = row["pencil"].get("lambda_min")
                    elif n <= 3000:
                        lmin, lmax, mpos, how = R2["pencil_lowest"](mats, n)
                        row.update(lambda_min=lmin, lambda_absmax=lmax, M_min_eig=mpos, method=how)
                        if os.environ.get("SCS3_CROSSCHECK") == "1" and m == 0:
                            row["si_crosscheck"] = pencil_si(mats, n, c_lb)
                    else:
                        row.update(pencil_si(mats, n, c_lb))
                    lm_ = row.get("lambda_min")
                    if lm_ is not None and lm_ < 0:
                        row["Gamma2_s2"] = float(-lm_ * (CK / 3.0857e16) ** 2)
                        row["efold_gyr"] = float(1 / (math.sqrt(-lm_) * CK / 3.0857e16) / 3.15576e16)
                    row["seconds"] = round(time.time() - t1, 1)
                    RES["rows"].append(row); DONE.add((tg, m, par))
                    dump(PARTIAL)
                    print(f"[{tg} m {m} {par}] n {n}; lambda_min {row.get('lambda_min')}; e-fold {row.get('efold_gyr')} Gyr; "
                          f"c_lb {c_lb:.3e}; {row['seconds']}s; rss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB",
                          flush=True)
    RES["seconds_total"] = round(time.time() - t0, 1)
    dump(OUT)
    if os.path.exists(PARTIAL):
        os.remove(PARTIAL)
    print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
