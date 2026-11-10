"""DCN1 B2 (FROZEN_CRITERIA.md d603f1703c, sections 2, 4, 5): resolved local solves of the law around a null.

Axisymmetric finite volume on a uniform cylindrical (R, z) grid: div[mu(|grad Phi|/a0) grad Phi] = 4 pi G rho_b,
mu = x/(1+x), face mu from the normal difference and the averaged tangential cell gradients (SCS2's rule), R = 0 a symmetry
axis (faces of zero area), Dirichlet data on the outer faces, z = 0 a mirror for P2.  Picard (relaxation 0.7) to relative
residual 1e-10.  Per resolution N_R in 48, 72, 108, 162, 243: route L (SCS3's formula on the FV D.P and the cell u) maximised
over the analysis region (cell centres within L/2 of the null), the A1 identity with FD Hessians (reported), counts, scalings,
and the MUTATE M1 / M2 values.

Sets (DCN1_LSET):
  KA4   uniform sphere, exact Dirichlet data, P1 geometry (null at the box centre) and P2 geometry (null at the corner).
  KA5   manufactured saddle Phi = (c/2) z^2 - (a/4) R^2 (+ b z), rho_b from the law, exact data; P1 geometry.
  P1    the thick twin's external-field null (16 backgrounds), boundary data from dcn1_global.py's variant-C R4 caches.
  P2    the isolated thick-disc centres (8 backgrounds), same source.
Writes dcn1_local_<SET>.json (partial json after every row; SIGTERM writes and exits).
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import os, sys, json, math, time, resource, signal
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla
from scipy.interpolate import RegularGridInterpolator
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scs2_aqual as S

G = S.G
KPCKMS_TO_S = 3.0857e16
MYR = 3.15576e13
NRS = [48, 72, 108, 162, 243]
LSET = os.environ.get("DCN1_LSET", "KA4")
CACHE = os.environ.get("DCN1_CACHE", os.path.join(HERE, "_cache"))
TOL, MAXIT, OMEGA = 1e-10, 800, 0.7
LAST = {"update": None}


class Box:
    def __init__(self, L, z_lo, z_hi, NR, NZ, mirror_z0=False):
        self.L, self.z_lo, self.z_hi, self.NR, self.NZ = L, z_lo, z_hi, NR, NZ
        self.Rf = np.linspace(0, L, NR + 1); self.zf = np.linspace(z_lo, z_hi, NZ + 1)
        self.Rc = 0.5 * (self.Rf[1:] + self.Rf[:-1]); self.zc = 0.5 * (self.zf[1:] + self.zf[:-1])
        self.hR = L / NR; self.hz = (z_hi - z_lo) / NZ
        self.mirror = mirror_z0
        self.shape = (NR, NZ); self.n = NR * NZ
        self.Ring = np.pi * (self.Rf[1:] ** 2 - self.Rf[:-1] ** 2)
        self.V = self.Ring[:, None] * self.hz * np.ones((1, NZ))
        self.RR, self.ZZ = np.meshgrid(self.Rc, self.zc, indexing="ij")


def boundary_points(b):
    """Dirichlet face centres: outer R (per z cell), bottom (per R cell, unless mirror), top (per R cell)."""
    pts = {"R": (np.full(b.NZ, b.L), b.zc.copy()), "top": (b.Rc.copy(), np.full(b.NR, b.z_hi))}
    if not b.mirror:
        pts["bot"] = (b.Rc.copy(), np.full(b.NR, b.z_lo))
    return pts


def grad_cells(b, Phi, PB):
    """cell-centred gradient with ghosts: mirror at R = 0 (and z = 0 for P2), Dirichlet ghost 2 Phi_b - Phi at the faces."""
    gR = np.empty_like(Phi); gz = np.empty_like(Phi)
    gR[1:-1] = (Phi[2:] - Phi[:-2]) / (2 * b.hR)
    gR[0] = (Phi[1] - Phi[0]) / (2 * b.hR)
    gR[-1] = (2 * PB["R"] - Phi[-1] - Phi[-2]) / (2 * b.hR)
    gz[:, 1:-1] = (Phi[:, 2:] - Phi[:, :-2]) / (2 * b.hz)
    gz[:, -1] = (2 * PB["top"] - Phi[:, -1] - Phi[:, -2]) / (2 * b.hz)
    if b.mirror:
        gz[:, 0] = (Phi[:, 1] - Phi[:, 0]) / (2 * b.hz)
    else:
        gz[:, 0] = (Phi[:, 1] - (2 * PB["bot"] - Phi[:, 0])) / (2 * b.hz)
    return gR, gz


def face_coefs(b, Phi, PB, a0, gR, gz, fun):
    """fun(x) at every face: x = |grad Phi|/a0 from the normal difference and the averaged tangential cell gradient."""
    out = {}
    gn = (Phi[1:] - Phi[:-1]) / b.hR; gt = 0.5 * (gz[1:] + gz[:-1])
    out["R"] = fun(np.sqrt(gn ** 2 + gt ** 2) / a0)
    gn = (Phi[:, 1:] - Phi[:, :-1]) / b.hz; gt = 0.5 * (gR[:, 1:] + gR[:, :-1])
    out["z"] = fun(np.sqrt(gn ** 2 + gt ** 2) / a0)
    gn = (PB["R"] - Phi[-1]) / (b.hR / 2); out["Rout"] = fun(np.sqrt(gn ** 2 + gz[-1] ** 2) / a0)
    gn = (PB["top"] - Phi[:, -1]) / (b.hz / 2); out["top"] = fun(np.sqrt(gn ** 2 + gR[:, -1] ** 2) / a0)
    if not b.mirror:
        gn = (Phi[:, 0] - PB["bot"]) / (b.hz / 2); out["bot"] = fun(np.sqrt(gn ** 2 + gR[:, 0] ** 2) / a0)
    return out


def assemble(b, coef, PB):
    """(A Phi)_k = sum over faces coef A/d (Phi_nb - Phi_k); Dirichlet parts go to rhs: returns A, rhs_add."""
    NR, NZ = b.shape; idx = np.arange(b.n).reshape(b.shape)
    rows, cols, vals = [], [], []
    diag = np.zeros(b.shape); rhs = np.zeros(b.shape)
    AR = 2 * np.pi * b.Rf[1:-1, None] * b.hz * np.ones((1, NZ)); c = coef["R"] * AR / b.hR
    k1, k2 = idx[:-1].ravel(), idx[1:].ravel(); c = c.ravel()
    rows += [k1, k2]; cols += [k2, k1]; vals += [c, c]
    np.add.at(diag.ravel(), k1, -c); np.add.at(diag.ravel(), k2, -c)
    Az = b.Ring[:, None] * np.ones((1, NZ - 1)); c = (coef["z"] * Az / b.hz).ravel()
    k1, k2 = idx[:, :-1].ravel(), idx[:, 1:].ravel()
    rows += [k1, k2]; cols += [k2, k1]; vals += [c, c]
    np.add.at(diag.ravel(), k1, -c); np.add.at(diag.ravel(), k2, -c)
    cR = coef["Rout"] * 2 * np.pi * b.L * b.hz / (b.hR / 2)
    diag[-1] -= cR; rhs[-1] -= cR * PB["R"]
    ct = coef["top"] * b.Ring / (b.hz / 2)
    diag[:, -1] -= ct; rhs[:, -1] -= ct * PB["top"]
    if not b.mirror:
        cb = coef["bot"] * b.Ring / (b.hz / 2)
        diag[:, 0] -= cb; rhs[:, 0] -= cb * PB["bot"]
    A = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(b.n, b.n)) + sps.diags(diag.ravel())
    return A, rhs.ravel()


def solve(b, rho, PB, a0, Phi0):
    src = (4 * np.pi * G * rho * b.V).ravel()
    Phi = Phi0.copy(); res = None
    LAST["update"] = np.inf
    prange = float(max(np.ptp(v) for v in PB.values()))
    mu = lambda x: x / (1 + x)
    for it in range(MAXIT):
        gR, gz = grad_cells(b, Phi, PB)
        A, radd = assemble(b, face_coefs(b, Phi, PB, a0, gR, gz, mu), PB)
        rhs = src + radd                       # amendment A2: was src - radd (imposed -Phi_b)
        res = float(np.linalg.norm(A @ Phi.ravel() - rhs) / np.linalg.norm(src))      # amendment A4: was / ||rhs||
        if it >= 10 and res < TOL and LAST["update"] < 1e-10 * prange:
            break
        new = spla.spsolve(A.tocsc(), rhs).reshape(b.shape)
        LAST["update"] = float(np.max(np.abs(OMEGA * (new - Phi))))
        Phi = Phi + OMEGA * (new - Phi)
    return Phi, res, it + 1


def diagnostics(b, Phi, PB, a0, rho, null, Gam2_exact=None, m2_ref=None):
    gR, gz = grad_cells(b, Phi, PB)
    A, radd = assemble(b, face_coefs(b, Phi, PB, a0, gR, gz, lambda x: 1 / (1 + x)), PB)
    dp = ((A @ Phi.ravel() - radd).reshape(b.shape)) / (4 * np.pi * G * b.V)          # D.P, Msun/kpc^3
    gm = np.sqrt(gR ** 2 + gz ** 2); u = gm / a0
    Gam2 = -4 * np.pi * G * dp * u * (2 + u) / KPCKMS_TO_S ** 2                        # s^-2
    # A1 identity with FD Hessians of the cell gradient (reported)
    HRR = np.gradient(gR, b.hR, axis=0); Hzz = np.gradient(gz, b.hz, axis=1)
    HRz = 0.5 * (np.gradient(gR, b.hz, axis=1) + np.gradient(gz, b.hR, axis=0))
    nR = gR / np.maximum(gm, 1e-300); nz = gz / np.maximum(gm, 1e-300)
    Pnn = nR * nR * HRR + 2 * nR * nz * HRz + nz * nz * Hzz
    Gid = (2 + u) * (u * Pnn / (1 + u) - 4 * np.pi * G * rho) / KPCKMS_TO_S ** 2
    s = np.sqrt(b.RR ** 2 + (b.ZZ - null) ** 2)
    reg = s <= b.L / 2
    def mx(F):
        Fm = np.where(reg, F, -np.inf); k = int(np.argmax(Fm)); i, j = np.unravel_index(k, b.shape)
        return float(Fm[i, j]), int(i), int(j)
    Q, i, j = mx(Gam2)
    Qid, _, _ = mx(np.where(reg, Gid, -np.inf))
    h8 = max(b.hR, b.hz)
    Q8 = float(np.max(np.where(reg & (s >= 8 * h8), Gam2, -np.inf)))          # amendment A1: reported
    out = dict(Q=Q, Q_efold_myr=(1 / math.sqrt(Q) / MYR) if Q > 0 else None, at_R=float(b.Rc[i]), at_z=float(b.zc[j]),
               at_s_over_L=float(s[i, j] / b.L), at_R_cells=int(i), u_there=float(u[i, j]), dp_there=float(dp[i, j]),
               rho_there=float(rho[i, j]), Q_identity=Qid, Q8=Q8,
               n_neg=int(np.sum(reg & (dp < 0))), n_region=int(reg.sum()), min_dp=float(np.min(dp[reg])),
               max_abs_dp=float(np.max(np.abs(dp[reg]))))
    # scalings of |D.P| and u with the distance s to the null (fits over s in [4 h, L/4])
    h = max(b.hR, b.hz)
    sel = reg & (s >= 4 * h) & (s <= b.L / 4) & (np.abs(dp) > 0) & (u > 0)
    if sel.sum() > 10:
        out["slope_absdp_vs_s"] = float(np.polyfit(np.log(s[sel]), np.log(np.abs(dp[sel])), 1)[0])
        out["slope_u_vs_s"] = float(np.polyfit(np.log(s[sel]), np.log(u[sel]), 1)[0])
    # MUTATE M1: G -> -D.P
    out["M1_Q"] = mx(-Gam2)[0]
    # MUTATE M2: spike at the analysis cell nearest the null
    sn = np.where(reg, s, np.inf); k = int(np.argmin(sn)); i2, j2 = np.unravel_index(k, b.shape)
    if m2_ref is not None:
        dpm = dp.copy(); dpm[i2, j2] -= (b.NR / 48.0) ** 2 * abs(m2_ref)       # (h_0/h)^2 (A1 corrects a (48/N)^2 slip)
        G2m = -4 * np.pi * G * dpm * u * (2 + u) / KPCKMS_TO_S ** 2
        out["M2_Q"] = mx(G2m)[0]
    # ---- amendment A3: the fixed annulus L/8 <= s <= L/2 and the shell maxima (inner radius >= 8h)
    ann = reg & (s >= b.L / 8)
    def shells(F):
        out_, k_ = [], 1
        while True:
            lo, hi = b.L / 2 ** (k_ + 1), b.L / 2 ** k_
            if lo < 8 * h8:
                break
            sel_ = reg & (s >= lo) & (s < hi)
            out_.append(dict(k=k_, s_lo_over_L=lo / b.L, s_hi_over_L=hi / b.L, M=float(np.max(F[sel_])) if sel_.any() else None))
            k_ += 1
        return out_
    def amax(F):
        return float(np.max(np.where(ann, F, -np.inf)))
    out["QA"] = amax(Gam2); out["QA_identity"] = amax(np.where(ann, Gid, -np.inf))
    out["shells"] = shells(Gam2)
    out["M1_QA"] = amax(-Gam2); out["M1_shells"] = shells(-Gam2)
    if m2_ref is not None:
        dpm3 = dp - abs(m2_ref) * (np.maximum(s, 1e-300) / b.L) ** -1
        G2m3 = -4 * np.pi * G * dpm3 * u * (2 + u) / KPCKMS_TO_S ** 2
        out["M2A3_QA"] = amax(G2m3); out["M2A3_shells"] = shells(G2m3)
    if Gam2_exact is not None:
        ex = Gam2_exact(b.RR, b.ZZ)
        out["exact_at_cells_annulus_max"] = float(np.max(np.where(ann, ex, -np.inf)))
        out["exact_at_cells_max"] = float(np.max(np.where(reg, ex, -np.inf)))
        err = np.abs(Gam2 - ex)[reg & (s > 4 * h)]
        out["cellwise_max_abs_err_over_4piGrho"] = float(np.max(err) / (4 * np.pi * G * np.max(rho) / KPCKMS_TO_S ** 2)) if np.max(rho) > 0 else float(np.max(err))
    return out


# ------------------------------------------------------------------ exact backgrounds for KA4 / KA5
def sphere_case(rho0, a0):
    s4 = 4 * np.pi * G * rho0; k = s4 / 3
    g = lambda r: (k * r + np.sqrt((k * r) ** 2 + 4 * a0 * k * r)) / 2
    dg = lambda r: (k + (2 * k * k * r + 4 * a0 * k) / (2 * np.sqrt((k * r) ** 2 + 4 * a0 * k * r))) / 2
    Phi = np.vectorize(lambda r: quad(g, 0, r, epsabs=0, epsrel=1e-13, limit=200)[0])
    def Gam2(R, z):
        r = np.sqrt(R ** 2 + z ** 2); r = np.maximum(r, 1e-300); u = g(r) / a0
        return (2 + u) * (u * dg(r) / (1 + u) - s4) / KPCKMS_TO_S ** 2
    def sup(Lh, lo=1e-12):
        rr = np.logspace(math.log10(lo), 0, 20000) * Lh
        return float(np.max(Gam2(rr, 0 * rr)))
    return (lambda R, z: Phi(np.sqrt(R ** 2 + z ** 2))), (lambda R, z: rho0 + 0 * R), Gam2, sup


def saddle_case(c, a, a0):
    import sympy as sp
    R_, z_ = sp.symbols("R z", real=True)
    Phi = c / 2 * z_ ** 2 - a / 4 * R_ ** 2
    gR_, gz_ = sp.diff(Phi, R_), sp.diff(Phi, z_)
    w = sp.sqrt(gR_ ** 2 + gz_ ** 2); u = w / a0; mu = u / (1 + u)
    rho4 = sp.diff(R_ * mu * gR_, R_) / R_ + sp.diff(mu * gz_, z_)
    lap = sp.diff(R_ * gR_, R_) / R_ + sp.diff(gz_, z_)
    G2 = -(lap - rho4) * u * (2 + u)
    fPhi = sp.lambdify((R_, z_), Phi, "numpy"); frho = sp.lambdify((R_, z_), rho4 / (4 * sp.pi * G), "numpy")
    fG2 = sp.lambdify((R_, z_), G2, "numpy")
    def Gam2(R, z):
        with np.errstate(all="ignore"):
            v = fG2(np.maximum(R, 1e-300), z) / KPCKMS_TO_S ** 2
        return np.nan_to_num(v, nan=0.0)
    def rho(R, z):
        with np.errstate(all="ignore"):
            return np.nan_to_num(frho(np.maximum(R, 1e-300), z), nan=0.0)
    def sup(Lh, lo=1e-8):
        th = np.linspace(0, np.pi, 4001); rr = np.logspace(math.log10(lo), 0, 3001) * Lh
        TT, RRr = np.meshgrid(th, rr)
        return float(np.max(Gam2(RRr * np.sin(TT), RRr * np.cos(TT))))
    return fPhi, rho, Gam2, sup


def cell_average(b, f, nsub=4):
    acc = np.zeros(b.shape); wsum = np.zeros(b.shape)
    for a_ in (np.arange(nsub) + 0.5) / nsub:
        for c_ in (np.arange(nsub) + 0.5) / nsub:
            R = b.Rf[:-1, None] + a_ * b.hR; z = b.zf[None, :-1] + c_ * b.hz
            w = R * np.ones_like(z)
            acc += f(R * np.ones_like(z), z * np.ones_like(R)) * w; wsum += w
    return acc / wsum


# ------------------------------------------------------------------ global boundary data
def global_interp(cpath):
    bg = S.load_cache(cpath); g = bg["g"]
    full = g.tmode == "full"
    tc = np.concatenate([[-g.tc[0]], g.tc, [(2 * np.pi - g.tc[-1]) if full else (np.pi - g.tc[-1])]])
    Ph = bg["Phi"][:, :, 0]
    Ph = np.concatenate([Ph[:, :1], Ph, Ph[:, -1:]], axis=1)
    it = RegularGridInterpolator((g.xc, tc), Ph, method="linear", bounds_error=True)
    def f(R, z):
        r = np.maximum(np.sqrt(R ** 2 + z ** 2), math.exp(g.xc[0])); th = np.arctan2(R, z)   # A4: clamp (initial guess only)
        if not full:
            th = np.minimum(th, np.pi / 2)
        return it(np.stack([np.log(r).ravel(), th.ravel()], -1)).reshape(np.shape(R))
    return f, bg


def thick_rho(M, Rd):
    hz = S.h_z_bershady(Rd); rho0 = M / (4 * np.pi * Rd ** 2 * hz)
    return (lambda R, z: rho0 * np.exp(-R / Rd - np.abs(z) / hz)), rho0, hz


# ------------------------------------------------------------------ cases
def cases():
    L_ = []
    a0c = S.a0k("canonical"); M = 10 ** 9.4; Rd = S.R_d_shen(M)
    _, rho0, hz = thick_rho(M, Rd)
    zn = -0.0131                          # P1 null scale (kpc), the canonical 9.4 / 0.1 a0 thick twin (R4, frozen); L = 0.4 |z_n|
    if LSET == "KA4":
        for geo in ("P1", "P2"):
            Lb = 0.4 * abs(zn) if geo == "P1" else min(0.5 * hz, 0.5 * a0c / (4 * np.pi * G * rho0))
            L_.append(dict(name=f"KA4_sphere_{geo}", kind="sphere", geo=geo, L=Lb, z_null=0.0, rho0=rho0, a0=a0c))
    elif LSET == "KA5":
        c = 4 * np.pi * G * rho0
        L_.append(dict(name="KA5_saddle_P1", kind="saddle", geo="P1", L=0.4 * abs(zn), z_null=0.0, c=c, a=2 * c, a0=a0c, rho0=rho0))
    elif LSET in ("P1", "P2"):
        gl = json.load(open(os.path.join(HERE, "dcn1_global_BC.json")))["rows"]
        for key, r in gl.items():
            sp_ = r["spec"]
            if (LSET == "P1") != (sp_["ge"] > 0):
                continue
            Mx = 10 ** float(sp_["logm"]); Rdx = r["Rd_kpc"]
            _, rho0x, hzx = thick_rho(Mx, Rdx)
            a0x = S.a0k(sp_["foot"])
            if LSET == "P1":
                zx = r["null"]["z_null_kpc"]
                L_.append(dict(name=key, kind="global", geo="P1", L=0.4 * abs(zx), z_null=zx, cache=r["cache"], M=Mx, Rd=Rdx,
                               a0=a0x, rho0=rho0x, spec=sp_))
            else:
                L_.append(dict(name=key, kind="global", geo="P2", L=min(0.5 * hzx, 0.5 * a0x / (4 * np.pi * G * rho0x)), z_null=0.0,
                               cache=r["cache"], M=Mx, Rd=Rdx, a0=a0x, rho0=rho0x, spec=sp_))
    return L_


OUTNAME = os.path.join(HERE, f"dcn1_local_{LSET}.json")
PARTIAL = OUTNAME.replace(".json", "_partial.json")
RES = {"lane": "DCN1", "script": "dcn1_local.py", "criteria": "d603f1703c", "set": LSET, "rows": {}}
if os.path.exists(PARTIAL):
    RES = json.load(open(PARTIAL))


def dump(path):
    RES["peak_rss_GB"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 3)
    RES["footer"] = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."
    tmp = path + ".tmp"; json.dump(RES, open(tmp, "w"), indent=1, default=str); os.replace(tmp, path)


def on_term(sig, frm):
    dump(PARTIAL); print("SIGTERM: partial written", flush=True); sys.exit(0)


signal.signal(signal.SIGTERM, on_term)

if __name__ == "__main__":
    t0 = time.time()
    for cs in cases():
        a0 = cs["a0"]; Lb = cs["L"]; zn = cs["z_null"]
        if cs["kind"] == "sphere":
            fPhi, frho, fG2, fsup = sphere_case(cs["rho0"], a0)
        elif cs["kind"] == "saddle":
            fPhi, frho, fG2, fsup = saddle_case(cs["c"], cs["a"], a0)
        else:
            fPhi, bgg = global_interp(os.path.join(CACHE, cs["cache"]))
            frho, _, _ = thick_rho(cs["M"], cs["Rd"]); fG2 = None; fsup = None
        row = RES["rows"].get(cs["name"], dict(case={k: v for k, v in cs.items()}, res={}))
        if fsup is not None:
            row["exact_sup_region"] = fsup(Lb / 2)
            row["exact_sup_annulus"] = fsup(Lb / 2, lo=0.25)          # A3: s in [L/8, L/2]
        m2_ref = None
        for NR in NRS:
            if str(NR) in row["res"]:
                m2_ref = row["res"][str(48)]["min_dp"] if "48" in row["res"] else m2_ref
                continue
            t1 = time.time()
            if cs["geo"] == "P1":
                b = Box(Lb, zn - Lb, zn + Lb, NR, 2 * NR)
            else:
                b = Box(Lb, 0.0, Lb, NR, NR, mirror_z0=True)
            PB = {k: fPhi(*v) for k, v in boundary_points(b).items()}
            C0 = float(np.mean(np.concatenate([v.ravel() for v in PB.values()])))          # amendment A4: gauge shift
            PB = {k: v - C0 for k, v in PB.items()}
            rho = cell_average(b, frho)
            Phi0 = fPhi(b.RR, b.ZZ) - C0
            Phi, resid, nit = solve(b, rho, PB, a0, Phi0)
            if NR == 48:
                tmpd = diagnostics(b, Phi, PB, a0, rho, zn)
                m2_ref = tmpd["min_dp"]
            d = diagnostics(b, Phi, PB, a0, rho, zn, Gam2_exact=fG2, m2_ref=m2_ref)
            d.update(residual=resid, iterations=nit, last_update=LAST["update"], seconds=round(time.time() - t1, 1), h_R=b.hR, h_z=b.hz)
            row["res"][str(NR)] = d
            RES["rows"][cs["name"]] = row
            dump(PARTIAL)
            print(f"[{cs['name']} N{NR}] res {resid:.1e} it {nit} upd {LAST['update']:.1e} {d['seconds']}s; Q {d['Q']:.4e} (e-fold {d['Q_efold_myr']} Myr) "
                  f"at s/L {d['at_s_over_L']:.3f} Rcell {d['at_R_cells']} u {d['u_there']:.3g}; Q_id {d['Q_identity']:.4e}; "
                  f"neg {d['n_neg']}/{d['n_region']}; minDP {d['min_dp']:.3e}; slopes dp {d.get('slope_absdp_vs_s')} u {d.get('slope_u_vs_s')}; "
                  f"QA {d['QA']:.4e} shells {[None if x['M'] is None else float('%.3e' % x['M']) for x in d['shells']]}; Q8 {d['Q8']:.3e}; M1 {d['M1_Q']:.3e} M2 {d.get('M2_Q')}" + (f"; exact sup {row.get('exact_sup_region'):.4e} cells-exact max {d.get('exact_at_cells_max'):.4e} annulus exact {row.get('exact_sup_annulus'):.4e}" if fsup else ""),
                  flush=True)
    RES["seconds_total"] = round(time.time() - t0, 1)
    dump(OUTNAME)
    if os.path.exists(PARTIAL):
        os.remove(PARTIAL)
    print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
