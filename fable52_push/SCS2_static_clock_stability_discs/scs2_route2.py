"""SCS2 route 2: the constraint-surface eigenproblem of the coupled clock about the solved disc backgrounds.
Criteria FROZEN_CRITERIA.md (158c4cf770), amendments A1 (847f24db0b), A2 (cb6ac0fe9a), A3 (ac13205c89).

At mu_K = 0 the coupled quadratic action reduces (phi eliminated on the constraint surface) to
    L_G zeta = lambda H zeta,   H = (L_chi^-1 - L_phi^-1)^-1,   lambda = omega^2,
with L_phi the GR form (weight 1), L_chi the law's anisotropic form (J''_perp on faces plus the cell term
J''_rr on r-faces and J''_theta-theta on theta-faces, the off-diagonal term dropped, plus the azimuthal m^2 term), and L_G the gradient form with the grid's
G = K D.P / c^2 on faces (plus m^2 G / (r sin theta)^2).  Units kpc, K = 1, c = 1.
- Axisymmetric backgrounds, m = 0, 1, 2 (and plane parity even / odd where the plane symmetry holds), both resolutions:
  the full pencil (dense, n <= 3000) or its lowest eigenvalues by Arnoldi on M L_G with M = L_chi^-1 - L_phi^-1
  (sparse LU) when n is larger.
- Every background, including the 3D in-plane field: Sylvester's law of inertia.  Since H > 0, the pencil has exactly as
  many negative eigenvalues as L_G, so the sign is read from L_G's lowest eigenvalue (sparse, which = 'SA').
Stable iff no lambda below -1e-10 max|lambda| (pencil) and L_G has no negative eigenvalue beyond -1e-10 of its largest.
SCS2_MUTATE in {M1, M2, M3}: M1 G -> -D.P; M2 the planar divergence (the part of div P along the field only);
M3 decoupled (H = L_chi).  Separate outputs.
"""
import os, sys, json, math, time, resource, glob
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
from scipy.linalg import eigh

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scs2_aqual as S

ARM = os.environ.get("SCS2_MUTATE", "")
assert ARM in ("", "M1", "M2", "M3")
CACHE = os.environ.get("SCS2_CACHE", os.path.join(HERE, "_cache"))
OUTL = []
def P_(s=""):
    print(s, flush=True); OUTL.append(str(s))
t0 = time.time()
CK = S.C_KMS
NMASK = 20


def G_field(bg, mode=""):
    """G = K D.P / c^2 per cell (kpc^-2); M1 flips the sign; M2 keeps only d(P . ghat)/ds (planar divergence)."""
    g = bg["g"]; dp = bg["dp"]
    Gc = 4 * np.pi * S.G * dp / CK ** 2
    if mode == "M1":
        return -Gc
    if mode == "M2":
        gr, gt, gp = bg["grads"]; gm = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)
        u = gm / bg["a0"]; p = gm / (1 + u)                     # K |P| (code), along ghat
        # derivative of p along ghat: (ghat . grad) p, by central differences on the grid (axisymmetric part)
        lnr = g.xc
        dp_dr = np.gradient(p, g.rc, axis=0)
        dp_dt = np.gradient(p, g.tc, axis=1) / g.rc[:, None, None]
        Gp = (gr * dp_dr + gt * dp_dt) / np.maximum(gm, 1e-300) / CK ** 2
        Gp[:NMASK] = np.nan
        return Gp
    return Gc


def build_forms(bg, crop, m, parity, Gc, axisym=True):
    """sparse L_phi, L_chi, L_G on the active cells (shells >= NMASK and r <= crop)."""
    g = bg["g"]
    nr, nt, np_ = g.shape
    imax = int(np.searchsorted(g.rc, crop))
    act = np.zeros(g.shape, bool); act[NMASK:imax] = True
    act &= np.isfinite(Gc)
    idx = -np.ones(g.shape, int); idx[act] = np.arange(act.sum())
    n = int(act.sum())
    gr, gt, gp = bg["grads"]; gm = np.sqrt(gr ** 2 + gt ** 2 + gp ** 2)
    u = gm / bg["a0"]
    Jpar = 1 / (1 + u) ** 2; Jperp = 1 / (1 + u)
    F = S.faces(g)
    rows = {k_: [] for k_ in ("phi", "chi", "G")}; cols = {k_: [] for k_ in rows}; vals = {k_: [] for k_ in rows}
    def addface(k1, k2, w, which):
        a = idx.ravel()[k1]; b = idx.ravel()[k2]
        both = (a >= 0) & (b >= 0); one_a = (a >= 0) & (b < 0); one_b = (b >= 0) & (a < 0)
        for key, wk in which.items():
            ww = w * wk
            rows[key] += [a[both], b[both], a[both], b[both]]; cols[key] += [a[both], b[both], b[both], a[both]]
            vals[key] += [ww[both], ww[both], -ww[both], -ww[both]]
            # Dirichlet where the neighbour is masked or cropped (inner annulus edge, crop sphere): ghost = 0 at the face
            rows[key] += [a[one_a], b[one_b]]; cols[key] += [a[one_a], b[one_b]]
            vals[key] += [ww[one_a], ww[one_b]]
    ghr = gr / np.maximum(gm, 1e-300); ght = gt / np.maximum(gm, 1e-300)
    Jrr = Jperp + (Jpar - Jperp) * ghr ** 2; Jtt = Jperp + (Jpar - Jperp) * ght ** 2      # diagonal of J'' in (r, theta)
    Jdir = {"r": Jrr, "t": Jtt, "p": Jperp}
    for key in ("r", "t", "p"):
        if key not in F: continue
        k1, k2, A, d = F[key]
        Gf = 0.5 * (Gc.ravel()[k1] + Gc.ravel()[k2])
        Jf = 0.5 * (Jdir[key].ravel()[k1] + Jdir[key].ravel()[k2])
        addface(k1, k2, A / d, {"phi": np.ones_like(A), "chi": Jf, "G": np.nan_to_num(Gf)})
    # outer sphere r_max (when the crop reaches it): Dirichlet at the face, half distance
    k1o, Ao, do = F["out"]
    ao = idx.ravel()[k1o]; sel = ao >= 0
    for key, wk in (("phi", np.ones(sel.sum())), ("chi", Jperp.ravel()[k1o][sel]), ("G", np.nan_to_num(Gc.ravel()[k1o][sel]))):
        rows[key].append(ao[sel]); cols[key].append(ao[sel]); vals[key].append((Ao / do)[sel] * wk)
    # plane boundary (half mode): odd parity -> Dirichlet at the plane (ghost = -zeta)
    if g.tmode == "half" and parity == "odd":
        j = nt - 1
        dt = g.rc * (0.5 * np.pi - g.tc[j])
        for i in range(nr):
            for l in range(np_):
                a = idx[i, j, l]
                if a < 0: continue
                Ap = ((g.rf[i + 1] ** 2 - g.rf[i] ** 2) / 2) * (g.pf[l + 1] - g.pf[l])
                w = Ap / dt[i]
                for key, wk in (("phi", 1.0), ("chi", Jperp[i, j, l]), ("G", Gc[i, j, l])):
                    rows[key].append(np.array([a])); cols[key].append(np.array([a])); vals[key].append(np.array([w * wk]))
    # azimuthal m^2 terms and the anisotropic cell term of L_chi
    V = g.V; Rs = (g.rc[:, None, None] * np.sin(g.tc)[None, :, None]) ** 2 * np.ones(g.shape)
    cell = idx[act]
    if axisym and m > 0:
        w = (m ** 2) * V[act] / Rs[act]
        for key, wk in (("phi", np.ones(n)), ("chi", Jperp[act]), ("G", Gc[act])):
            rows[key].append(cell); cols[key].append(cell); vals[key].append(w * wk)
    mats = {}
    for key in rows:
        mats[key] = sps.csr_matrix((np.concatenate(vals[key]), (np.concatenate(rows[key]), np.concatenate(cols[key]))), shape=(n, n))
    # the off-diagonal J''_r-theta term is dropped: the form stays positive by construction (J''_rr, J''_tt <= 1 = GR's
    # weight, so H = (L_chi^-1 - L_phi^-1)^-1 > 0); it changes the inertia H only, never the sign of an eigenvalue (inertia)
    return mats, n


def pencil_lowest(mats, n, decoupled=False, k=4):
    Lp, Lc, LG = mats["phi"].tocsc(), mats["chi"].tocsc(), mats["G"].tocsc()
    if n <= 3000:
        Lpd, Lcd, LGd = Lp.toarray(), Lc.toarray(), LG.toarray()
        Mm = np.linalg.inv(Lcd) - (0 if decoupled else np.linalg.inv(Lpd))
        Mm = 0.5 * (Mm + Mm.T)
        mpos = float(np.linalg.eigvalsh(Mm).min())
        H = np.linalg.inv(Mm); H = 0.5 * (H + H.T)
        w = eigh(LGd, H, eigvals_only=True)
        return float(w.min()), float(np.abs(w).max()), mpos, "dense"
    lc = spla.splu(Lc); lp = spla.splu(Lp)
    def mv(x):
        y = LG @ x
        return lc.solve(y) - (0 if decoupled else lp.solve(y))
    T = spla.LinearOperator((n, n), matvec=mv, dtype=float)
    w = spla.eigs(T, k=k, which="SR", return_eigenvectors=False, maxiter=5000, ncv=40, tol=1e-8)
    wl = spla.eigs(T, k=1, which="LM", return_eigenvectors=False, maxiter=5000, tol=1e-6)
    return float(np.real(w).min()), float(np.abs(wl).max()), None, "arnoldi"


def inertia(mats):
    """lowest and highest eigenvalue of L_G (dense; the caller keeps n <= 6000)."""
    w = np.linalg.eigvalsh(mats["G"].toarray())
    return float(w.min()), float(w.max())


def rayleigh_3d(mats, Gc, act_idx, shape):
    """the frozen 3D test: trial zeta = (-1)^(i+j+l) on negative-G cells whose six neighbours are negative too, 0 elsewhere;
    the quotient's numerator zeta.L_G.zeta < 0 certifies an unstable mode (H > 0).  LOBPCG's lowest eigenvalue beside it."""
    LG = mats["G"]; n = LG.shape[0]
    neg = np.isfinite(Gc) & (Gc < 0)
    inner = neg.copy()
    for ax in range(3):
        for sh in (1, -1):
            inner &= np.roll(neg, sh, axis=ax)
    z = np.zeros(n)
    I, J, L = np.indices(shape)
    sign = (-1.0) ** (I + J + L)
    sel = inner & (act_idx >= 0)
    z[act_idx[sel]] = sign[sel]
    num = float(z @ (LG @ z)) if z.any() else 0.0
    x0 = np.random.default_rng(0).normal(size=(n, 3))
    try:
        wl, _ = spla.lobpcg(LG, x0, largest=False, maxiter=2000, tol=1e-8)
        lob = float(np.min(wl))
    except Exception as ex:
        lob = None
    return num, int(sel.sum()), lob


RES = {"lane": "SCS2", "route": 2, "criteria": "158c4cf770", "amendments": ["847f24db0b", "cb6ac0fe9a", "ac13205c89"],
       "mutate_arm": ARM or None, "rows": []}
files = sorted(glob.glob(os.path.join(CACHE, "*.npz")))
PART = os.environ.get("SCS2_PART", "")
if PART:
    files = files[int(PART)::3]
for f in files:
    tag = os.path.basename(f)[:-4]
    bg = S.load_cache(f); g = bg["g"]
    coarse = tag.endswith("_coarse")
    ge = bg["ge"]
    if ge > 0:
        re = math.sqrt(S.G * bg["M"] * bg["a0"]) / (ge * bg["a0"]); crop = max(30 * bg["Rd"], 3 * re)
    else:
        crop = 30 * bg["Rd"]
    axisym = g.np_ == 1
    Gc = G_field(bg, ARM if ARM in ("M1", "M2") else "")
    ms = (0, 1, 2) if axisym else (None,)
    pars = ("even", "odd") if g.tmode == "half" else ("none",)
    for m in ms:
        for par in pars:
            mats, n = build_forms(bg, crop, m if m is not None else 0, par, Gc, axisym=axisym)
            if not axisym:
                imax = int(np.searchsorted(g.rc, crop))
                act = np.zeros(g.shape, bool); act[NMASK:imax] = True; act &= np.isfinite(Gc)
                aidx = -np.ones(g.shape, int); aidx[act] = np.arange(act.sum())
                num, ncells, lob = rayleigh_3d(mats, Gc, aidx, g.shape)
                RES["rows"].append(dict(tag=tag, m=None, parity=par, n=n, rayleigh_numerator=num, trial_cells=ncells,
                                        lobpcg_min=lob, negative_by_inertia=bool(num < 0 or (lob is not None and lob < 0))))
                continue
            if n > 4000 and m != 0:
                RES["rows"].append(dict(tag=tag, m=m, parity=par, n=n, note="fine grid too large for a dense check at m != 0; coarse grid carries it"))
                continue
            wmin, wmax = inertia(mats)
            neg_inertia = wmin < -1e-10 * abs(wmax)
            row = dict(tag=tag, m=m, parity=par, n=n, LG_min=wmin, LG_max=wmax, negative_by_inertia=bool(neg_inertia))
            if axisym and n <= 3000:
                lmin, lmax, mpos, how = pencil_lowest(mats, n, decoupled=(ARM == "M3"))
                row.update(lambda_min=lmin, lambda_absmax=lmax, M_min_eig=mpos, method=how,
                           unstable_pencil=bool(lmin < -1e-10 * lmax))
                if lmin < 0:
                    row["efold_yr"] = float(1 / (math.sqrt(-lmin) * CK / 3.0857e16) / 3.15576e7)    # kpc^-1 * c -> 1/s
            RES["rows"].append(row)
    rs = [r_ for r_ in RES["rows"] if r_["tag"] == tag]
    P_(f"[{tag}] n {rs[0]['n']}; L_G negative (inertia): {any(r_.get('negative_by_inertia', False) for r_ in rs)}; "
       + (f"pencil lambda_min {min(r_['lambda_min'] for r_ in rs if 'lambda_min' in r_):.3e} kpc^-2" if any('lambda_min' in r_ for r_ in rs) else "pencil not run")
       + f"; {time.time()-t0:.0f}s")

RES["seconds"] = round(time.time() - t0, 1)
RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
suffix = (f"_MUTATE_{ARM}" if ARM else "") + (f"_part{PART}" if PART else "")
with open(os.path.join(HERE, f"scs2_route2{suffix}.json"), "w") as fh:
    json.dump(RES, fh, indent=1, default=str)
P_(f"runtime {RES['seconds']} s, peak RSS {RES['peak_rss_GB']} GB")
P_("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
with open(os.path.join(HERE, f"scs2_route2{suffix}.out"), "w") as fh:
    fh.write("\n".join(OUTL) + "\n")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
