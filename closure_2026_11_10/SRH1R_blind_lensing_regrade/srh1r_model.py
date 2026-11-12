"""SRH1R model side (own code): the settled layout of SRH1's family, its exact projection, and the tables used for a
lens's own halo and for offset neighbour halos.  Nothing is imported from SRH1 or ONE1.

Run as a script: known answers KA1-KA5 and the kernel part of KA7 -> srh1r_model_ka.json / .out.
Units: Msun, kpc (physical).  kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FLD = os.path.join(REPO, "fable52_push", "FLD1_fold_reach", "runs")
G_SI, MSUN, MPC = 6.674e-11, 1.989e30, 3.0857e22; KPC = MPC / 1e3          # the record's constants
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
XSH = {"canonical": 59.4861237154402, "alt": 59.502850378209175}           # PD1's share (pd1.json, z 0 table median)
FOOTS = ("canonical", "alt")
h = 0.6736; OMB, OMC = 0.02237, 0.1200
Om = (OMB + OMC) / h ** 2; FB = OMB / (OMB + OMC); RHO_M = Om * 2.77536627e11      # Msun/h per (Mpc/h)^3 comoving
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]

def m_nfw(x): return np.log1p(x) - x / (1 + x)
def r_M(Mb, foot): return np.sqrt(G_SI * Mb * MSUN / A0[foot]) / KPC

# ---------------------------------------------------------------- R_fold (FLD1's primary runs; FZS1's rule, re-written)
_FT = {}
def _series(foot):
    if foot not in _FT:
        _FT[foot] = []
        for M in MASSES:
            S = np.array(json.load(open(os.path.join(FLD, f"hubble_{foot}_M{M:g}_zi10_N2400.json")))["series"])
            o = np.argsort(S[:, 1]); _FT[foot].append((S[o, 1], S[o, 2]))
    return _FT[foot]
def rfold_kpc(foot, z, lM):
    """R_fold(z, M_b) in physical kpc; lM = log10 M_b (array), z scalar."""
    R = np.array([np.interp(z, zs, rs) for zs, rs in _series(foot)]); lM = np.atleast_1d(np.asarray(lM, float))
    out = 10 ** np.interp(lM, MASSES, np.log10(R)) if np.all(R > 0) else np.interp(lM, MASSES, R)
    lo, hi = lM < MASSES[0], lM > MASSES[-1]
    out = np.where(lo, R[0] * 10 ** ((lM - MASSES[0]) / 3), out); out = np.where(hi, R[-1] * 10 ** ((lM - MASSES[-1]) / 3), out)
    return out

# ---------------------------------------------------------------- the cold reference halo (FRZ1's rule, re-written)
def Omz(z): return Om * (1 + z) ** 3 / (Om * (1 + z) ** 3 + 1 - Om)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz(z)) / (1 - Om)
_REF = {}
def ref_halo(Mta, z):
    """NFW reference with turnaround mass Mta (Msun) at z: returns r_s, r_ta in physical kpc (arrays)."""
    key = round(float(z), 6)
    if key not in _REF:
        lM = np.arange(6.0, 17.0001, 0.01); M = 10 ** lM                    # Msun/h, 200 x mean
        c = 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01
        r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3)               # comoving Mpc/h
        tgt = dta_of(z) / 200.0; xl, xh = np.full(len(M), 1.0), np.full(len(M), 200.0)
        for _ in range(80):                                                 # bisection: m(c x) / m(c) / x^3 = Delta_ta / 200
            xm = 0.5 * (xl + xh); big = m_nfw(c * xm) / m_nfw(c) / xm ** 3 > tgt
            xl = np.where(big, xm, xl); xh = np.where(big, xh, xm)
        xta = 0.5 * (xl + xh); MtaG = M * m_nfw(c * xta) / m_nfw(c) / h     # Msun
        f = 1e3 / (h * (1 + z)); _REF[key] = (np.log10(MtaG), np.log10(r2 / c * f), np.log10(xta * r2 * f))
    a, b, d = _REF[key]; l = np.log10(np.asarray(Mta, float))
    return 10 ** np.interp(l, a, b), 10 ** np.interp(l, a, d)

# ---------------------------------------------------------------- one halo's layout
def layout(Mb, z, foot, case):
    """case: ("set", f) | ("ref",) | ("inf",) | ("one1", X) | ("mu1", f) share x 0.1 | ("mu2", f) no reference outside.
    Returns dict(segs=[(ra, rb, kind, amp)], Mc = total cold mass, edge, Rset, s, rta, rs, rt, X, rM)."""
    X = XSH[foot] * (0.1 if case[0] == "mu1" else 1.0)
    if case[0] == "one1": X = case[1]
    rM = float(r_M(Mb, foot)); rt = math.sqrt(X * (X + 1)) * rM
    rs, rta = (float(v) for v in ref_halo(X * Mb / (1 - FB), z)); An = X * Mb / m_nfw(rta / rs)
    CB = lambda r: min(Mb * (math.sqrt(0.25 + (r / rM) ** 2) - 0.5), X * Mb)
    CR = lambda r: An * m_nfw(min(r, rta) / rs)
    if case[0] == "one1":
        return dict(segs=[(0.0, rt, "ph", 1.0)], Mc=X * Mb, edge=rt, Rset=rt, s=1.0, rta=rta, rs=rs, rt=rt, X=X, rM=rM, Mb=Mb)
    if case[0] == "ref":
        return dict(segs=[(0.0, rta, "nfw", An)], Mc=X * Mb, edge=rta, Rset=0.0, s=float("nan"), rta=rta, rs=rs, rt=rt, X=X, rM=rM, Mb=Mb)
    f = float("inf") if case[0] == "inf" else case[1]
    Rset = rta if f == float("inf") else min(f * float(rfold_kpc(foot, z, math.log10(Mb))[0]), rta)
    s = CR(Rset) / CB(Rset); segs = [(0.0, min(Rset, rt), "ph", s)]
    if case[0] == "mu2": return dict(segs=segs, Mc=CR(Rset), edge=Rset, Rset=Rset, s=s, rta=rta, rs=rs, rt=rt, X=X, rM=rM, Mb=Mb)
    if Rset < rta: segs.append((Rset, rta, "nfw", An))
    return dict(segs=segs, Mc=X * Mb, edge=rta, Rset=Rset, s=s, rta=rta, rs=rs, rt=rt, X=X, rM=rM, Mb=Mb)

def dens(L, kind, amp, r):
    """dM/dr of one piece."""
    if kind == "ph":
        x = r / L["rM"]; return amp * L["Mb"] * x / (L["rM"] * np.sqrt(0.25 + x * x))
    x = r / L["rs"]; return amp * x / (1 + x) ** 2 / L["rs"]
def cold_mass(L, r):
    """Enclosed cold mass at r (array)."""
    r = np.asarray(r, float); out = np.zeros_like(r)
    for ra, rb, kind, amp in L["segs"]:
        rr = np.clip(r, ra, rb)
        if kind == "ph":
            out += amp * L["Mb"] * (np.sqrt(0.25 + (rr / L["rM"]) ** 2) - math.sqrt(0.25 + (ra / L["rM"]) ** 2))
        else: out += amp * (m_nfw(rr / L["rs"]) - m_nfw(ra / L["rs"]))
    return out

# ---------------------------------------------------------------- exact projection (r = R cosh t on each piece)
_GL = {}
def gl(n):
    if n not in _GL: _GL[n] = np.polynomial.legendre.leggauss(n)
    return _GL[n]
def project(L, R, n=64):
    """Sigma_cold(R) [Msun/kpc^2] and projected cold mass inside R [Msun]."""
    R = np.asarray(R, float); x, w = gl(n); Sig = np.zeros_like(R); I = np.zeros_like(R)
    for ra, rb, kind, amp in L["segs"]:
        ok = rb > R
        if not ok.any(): continue
        Rk = R[ok]; t0 = np.arccosh(np.maximum(ra, Rk) / Rk); t1 = np.arccosh(rb / Rk); hw = 0.5 * (t1 - t0)
        t = t0[:, None] + hw[:, None] * (x[None, :] + 1); r = Rk[:, None] * np.cosh(t); dm = dens(L, kind, amp, r)
        Sig[ok] += (dm / (2 * math.pi * r) * w).sum(1) * hw
        I[ok] += (dm * np.tanh(t) * Rk[:, None] * np.sinh(t) * w).sum(1) * hw
    return Sig, L["Mc"] - I
def dsig_exact(L, R, n=64):
    """DeltaSigma(R) of the whole halo (central baryon point + cold), Msun/kpc^2."""
    Sig, M2 = project(L, R, n); return (L["Mb"] + M2) / (math.pi * np.asarray(R) ** 2) - Sig

# ---------------------------------------------------------------- offset halo: projected cold mass inside a circle
def mdisk_frac(L, d, R, nq=48, rho=None, rS=None, M2=None):
    """Fraction of the halo's cold mass projected inside the circle of radius R centred a distance d from the halo (arrays)."""
    d, R = np.broadcast_arrays(np.asarray(d, float), np.asarray(R, float)); E = L["edge"]
    if rho is None:
        rho = E * np.logspace(-5, 0, 400); S, M2 = project(L, rho); rS = rho * S
    lr = np.log(rho)
    m2 = lambda q: np.where(q <= rho[0], 0.0, np.interp(np.log(np.maximum(q, rho[0])), lr, M2))
    rs_ = lambda q: np.where(q >= E, 0.0, np.interp(np.log(np.maximum(q, rho[0])), lr, rS))
    out = np.where(R > d, m2(np.minimum(R - d, E)), 0.0)
    lo = np.abs(R - d); hi = np.minimum(R + d, E); ok = (hi > lo) & (d > 0)
    if ok.any():
        x, w = gl(nq); th = 0.5 * math.pi * (x + 1); c = 0.5 * (lo[ok] + hi[ok]); hh = 0.5 * (hi[ok] - lo[ok])
        q = c[:, None] - hh[:, None] * np.cos(th)[None, :]; dd, RR = d[ok][:, None], R[ok][:, None]
        a = np.arccos(np.clip((q * q + dd * dd - RR * RR) / (2 * q * dd), -1.0, 1.0)) / math.pi
        add = (2 * math.pi * rs_(q) * a * np.sin(th)[None, :] * w).sum(1) * hh * 0.5 * math.pi
        o2 = out.copy(); o2[ok] += add; out = o2
    return np.clip(out / L["Mc"], 0.0, 1.0)

# ---------------------------------------------------------------- tables
LMG = np.round(np.arange(6.6, 13.9001, 0.1), 3); ZG = np.round(np.arange(0.0, 0.6001, 0.1), 3)
NRO = 260; LRO = np.linspace(-0.3, 3.9, NRO)                    # own halo: log10 R kpc
UG = np.concatenate([[-3.0], np.linspace(-2.5, -0.5, 9), np.round(np.linspace(-0.45, 0.6, 43), 4), np.linspace(0.7, 1.5, 9)])   # first row: d = 0
WG_ = np.linspace(0.0, 1.0, 257)      # offset halo: log10(d / edge), w'
def wmap_R(d, E, w):
    return np.where(w < 0.5, d - np.minimum(d, E) * (1 - 2 * w) ** 2, d + E * (2 * w - 1) ** 2)
def build(foot, case):
    """Tables for one footing and layout: OWN[iM, iz, iR] = projected total mass inside R / total mass; EDGE, MTOT, BFR
    [iM, iz]; NB[iM, iz, iu, iw] = cold fraction inside the circle R(w'), d = edge 10^u, with the circle through the halo centre
    (R = d) pinned at w' = 1/2: R = d - min(d, edge) (1 - 2 w')^2 below, R = d + edge (2 w' - 1)^2 above."""
    nM, nz = len(LMG), len(ZG)
    OWN = np.zeros((nM, nz, NRO)); EDGE = np.zeros((nM, nz)); MTOT = np.zeros((nM, nz)); BFR = np.zeros((nM, nz))
    NB = np.zeros((nM, nz, len(UG), len(WG_))); Ro = 10 ** LRO
    for i, lM in enumerate(LMG):
        for j, z in enumerate(ZG):
            L = layout(10 ** lM, z, foot, case); E = L["edge"]; Mt = L["Mb"] + L["Mc"]
            _, M2 = project(L, np.minimum(Ro, E)); OWN[i, j] = (L["Mb"] + M2) / Mt
            EDGE[i, j], MTOT[i, j], BFR[i, j] = E, Mt, L["Mb"] / Mt
            rho = E * np.logspace(-5, 0, 400); S, M2r = project(L, rho); d = E * 10 ** UG[:, None]; d[0] = 0.0
            Rr = wmap_R(d, E, WG_[None, :])
            NB[i, j] = mdisk_frac(L, d, Rr, rho=rho, rS=rho * S, M2=M2r)
    return dict(OWN=OWN, EDGE=EDGE, MTOT=MTOT, BFR=BFR, NB=NB.astype(np.float32))

def _mz(lM, z):
    a = np.clip((lM - LMG[0]) / 0.1, 0, len(LMG) - 1.000001); i = a.astype(int); fa = a - i
    b = np.clip((z - ZG[0]) / 0.1, 0, len(ZG) - 1.000001); j = b.astype(int); fb = b - j
    return i, fa, j, fb
def _bil(T, i, fa, j, fb):
    return (T[i, j] * (1 - fa) * (1 - fb) + T[i + 1, j] * fa * (1 - fb) + T[i, j + 1] * (1 - fa) * fb + T[i + 1, j + 1] * fa * fb)
def halo_scalars(T, lM, z):
    """edge [kpc], total mass [Msun], baryon fraction, interpolated in (log M_b, z) (log for edge and mass)."""
    i, fa, j, fb = _mz(lM, z)
    return 10 ** _bil(np.log10(T["EDGE"]), i, fa, j, fb), 10 ** _bil(np.log10(T["MTOT"]), i, fa, j, fb), _bil(T["BFR"], i, fa, j, fb)
def own_m2d(T, lM, z, R):
    """Projected total mass inside R for halos (lM, z) [n] at radii R [n, m] (Msun)."""
    i, fa, j, fb = _mz(lM, z); _, Mt, _ = halo_scalars(T, lM, z)
    c = np.clip((np.log10(R) - LRO[0]) / (LRO[1] - LRO[0]), 0, NRO - 1.000001); k = c.astype(int); fc = c - k
    O = T["OWN"]; out = 0.0
    for di, wi in ((0, 1 - fa), (1, fa)):
        for dj, wj in ((0, 1 - fb), (1, fb)):
            ii, jj = (i + di)[:, None], (j + dj)[:, None]
            out = out + (wi * wj)[:, None] * (O[ii, jj, k] * (1 - fc) + O[ii, jj, k + 1] * fc)
    E = halo_scalars(T, lM, z)[0]
    return np.where(R >= E[:, None], 1.0, out) * Mt[:, None]
def nb_cold(T, lM, z, d, R):
    """Projected COLD mass of offset halos (lM, z, d) [n] inside circles R [n, m] (Msun); the baryon point is separate."""
    i, fa, j, fb = _mz(lM, z); E, Mt, bf = halo_scalars(T, lM, z); E = E[:, None]; d = d[:, None]
    lu = np.clip(np.log10(np.maximum(d, 1e-12) / E), UG[0], UG[-1]); iu0 = np.clip(np.searchsorted(UG, lu, side='right') - 1, 0, len(UG) - 2)
    u = (iu0 + (lu - UG[iu0]) / (UG[iu0 + 1] - UG[iu0])) * np.ones_like(R); u = np.minimum(u, len(UG) - 1.000001)
    Llo = np.maximum(np.minimum(d, E), 1e-12)
    w = np.where(R < d, 0.5 * (1 - np.sqrt(np.clip((d - R) / Llo, 0.0, 1.0))), 0.5 * (1 + np.sqrt(np.clip((R - d) / E, 0.0, 1.0)))) * (len(WG_) - 1)
    w = np.minimum(w, len(WG_) - 1.000001); iu = u.astype(int); fu = u - iu; iw = w.astype(int); fw = w - iw
    N = T["NB"]; out = 0.0
    for di, wi in ((0, 1 - fa), (1, fa)):
        for dj, wj in ((0, 1 - fb), (1, fb)):
            ii, jj = (i + di)[:, None], (j + dj)[:, None]
            v = (N[ii, jj, iu, iw] * (1 - fu) * (1 - fw) + N[ii, jj, iu + 1, iw] * fu * (1 - fw)
                 + N[ii, jj, iu, iw + 1] * (1 - fu) * fw + N[ii, jj, iu + 1, iw + 1] * fu * fw)
            out = out + (wi * wj)[:, None] * v
    return out * (Mt * (1 - bf))[:, None]

NGL = 5
def cell_mean(Mfun, R1, R2, lo, hi, Msat, brk, d=None, Mbar=None):
    """Area mean of DeltaSigma over annuli [R1, R2] ([n, m] arrays) for a mass-inside-circle function Mfun(R) that is 0
    below lo [n], Msat [n] above hi [n] and smooth between except at brk [n] (the quadrature is split there), plus a
    point Mbar [n] at offset d [n] (closed form).  Exact identity: <DS> = [2 int M dlnR - (M(R2) - M(R1))] /
    (pi (R2^2 - R1^2)).  Cells with R2 <= R1 return 0."""
    ok = R2 > R1; R2s = np.where(ok, R2, R1 * 1.0001); x, w = gl(NGL); n, m = R1.shape
    a = np.maximum(R1, lo[:, None]); b = np.minimum(R2s, hi[:, None]); b = np.maximum(b, a); c = np.clip(brk[:, None], a, b)
    la, lc, lb = np.log(a), np.log(c), np.log(b); h1, h2 = 0.5 * (lc - la), 0.5 * (lb - lc)
    n1 = np.exp(la[:, :, None] + h1[:, :, None] * (x[None, None, :] + 1)); n2 = np.exp(lc[:, :, None] + h2[:, :, None] * (x[None, None, :] + 1))
    q = m * NGL; allR = np.concatenate([n1.reshape(n, q), n2.reshape(n, q), R1, R2s], axis=1); Mv = Mfun(allR)
    I = (Mv[:, :q].reshape(n, m, NGL) * w).sum(2) * h1 + (Mv[:, q:2 * q].reshape(n, m, NGL) * w).sum(2) * h2
    M1, M2 = Mv[:, 2 * q:2 * q + m], Mv[:, 2 * q + m:]
    top = np.maximum(R1, hi[:, None]); I = I + np.where(R2s > top, Msat[:, None] * np.log(R2s / top), 0.0)
    num = 2 * I - (M2 - M1)
    if Mbar is not None:
        dd = d[:, None]; lob = np.maximum(R1, dd)
        num = num + Mbar[:, None] * np.where(R2s > dd, 2 * np.log(R2s / lob) - (R1 <= dd), 0.0)
    return np.where(ok, num / (math.pi * (R2s ** 2 - R1 ** 2)), 0.0)
def own_cells(T, lM, z, R1, R2):
    """Own-halo cell means of DeltaSigma [Msun/kpc^2] for lenses (log M_b, z) [n] and cells R1, R2 [n, m] kpc."""
    E, Mt, _ = halo_scalars(T, lM, z)
    return cell_mean(lambda R: own_m2d(T, lM, z, R), R1, R2, np.zeros_like(E), E, Mt, np.zeros_like(E))
def nb_cells(T, lMj, z, d, R1, R2):
    """Neighbour cell means: halos (log M_b,j, z) at projected offset d [n] about the lens whose cells are R1, R2 [n, m]."""
    E, Mt, bf = halo_scalars(T, lMj, z)
    return cell_mean(lambda R: nb_cold(T, lMj, z, d, R), R1, R2, np.maximum(d - E, 0.0), d + E, Mt * (1 - bf), d, d=d, Mbar=Mt * bf)
DCONV = 4 * G_SI * MSUN / KPC ** 2                                # DeltaSigma [Msun/kpc^2] -> 4 G DeltaSigma [m/s^2]
CASES = {"f0.40": ("set", 0.40), "f0.50": ("set", 0.50), "f0.60": ("set", 0.60), "f0.70": ("set", 0.70), "ref": ("ref",),
         "inf": ("inf",), "one1": ("one1", None), "mu1": ("mu1", 0.50), "mu2": ("mu2", 0.50), "mu3": ("set", 0.05)}
def case_of(name, foot):
    c = CASES[name]; return ("one1", XSH[foot]) if c[0] == "one1" else c
def table(foot, name, cache=None):
    cache = cache or os.path.join(HERE, "_tables"); os.makedirs(cache, exist_ok=True); p = os.path.join(cache, f"{foot}_{name}.npz")
    if os.path.exists(p): return dict(np.load(p))
    T = build(foot, case_of(name, foot)); np.savez(p + ".tmp.npz", **T); os.replace(p + ".tmp.npz", p); return T

# ================================================================ known answers
if __name__ == "__main__":
    OUT = []; KA = {}
    def P(*a):
        s = " ".join(str(v) for v in a); print(s, flush=True); OUT.append(s)
    def rec(name, ok, **kw):
        KA[name] = dict(pass_=bool(ok), **kw); P(f"{name}: {'PASS' if ok else 'FAIL'}  {kw}")
    rng = np.random.default_rng(52)
    # KA1 point mass through the projection: a halo with no cold mass
    L = layout(1e11, 0.3, "canonical", ("one1", 1e-12)); R = np.logspace(0, 4, 60)
    e1 = float(np.max(np.abs(dsig_exact(L, R) * math.pi * R ** 2 / 1e11 - 1)))
    Tp = dict(OWN=np.ones((len(LMG), len(ZG), NRO)), EDGE=np.ones((len(LMG), len(ZG))), MTOT=np.tile((10 ** LMG)[:, None], (1, len(ZG))), BFR=np.ones((len(LMG), len(ZG))))
    R1 = np.array([[100.0, 300.0]]); R2 = np.array([[133.0, 420.0]])
    cm = own_cells(Tp, np.array([11.0]), np.array([0.3]), R1, R2); ex = 2e11 * np.log(R2 / R1) / (math.pi * (R2 ** 2 - R1 ** 2))
    e1b = float(np.max(np.abs(cm / ex - 1)))
    rec("KA1_point_mass", e1 < 1e-6 and e1b < 1e-6, max_dev_projection=e1, max_dev_cell_mean=e1b)
    # KA2 the law's untruncated halo
    r2 = {}
    for foot in FOOTS:
        L = layout(1e11, 0.3, foot, ("one1", 1e8)); u = np.logspace(math.log10(30), 3, 40); R = u * L["rM"]
        g = DCONV * dsig_exact(L, R); iso = math.sqrt(G_SI * 1e11 * MSUN * A0[foot]) / (R * KPC); r2[foot] = float(np.max(np.abs(g / iso - 1))); r2[foot + '_after_next_term'] = float(np.max(np.abs(g / iso - 1 - (2 / math.pi) / u)))
    rec("KA2_law_untruncated", max(r2[f + "_after_next_term"] for f in FOOTS) < 1e-3, as_frozen_pass=bool(max(r2[f] for f in FOOTS) < 1e-3), max_dev=r2)
    # KA3 far field
    dev = 0.0
    for foot in FOOTS:
        for name in CASES:
            for lM in (9.5, 10.5, 11.5):
                L = layout(10 ** lM, 0.3, foot, case_of(name, foot)); R = L["edge"] * np.array([1.0, 1.5, 4.0])
                dev = max(dev, float(np.max(np.abs(dsig_exact(L, R) * math.pi * R ** 2 / (L["Mb"] + L["Mc"]) - 1))))
    L = layout(1e11, 0.3, "canonical", ("one1", 53.64)); Li = layout(1e11, 0.3, "canonical", ("one1", 1e8)); R = np.array([2000.0 * L["rM"]])
    rat = float(dsig_exact(L, R)[0] / dsig_exact(Li, R)[0]); want = 4 * 54.64 / (math.pi * 2000)
    rec("KA3_far_field", dev < 1e-6 and abs(rat / want - 1) < 1e-3, max_dev=dev, ratio=rat, expected=want)
    # KA4 mass: continuous at R_set, non-decreasing, X M_b at r_ta
    worst = dict(cont=0.0, tot=0.0, mono=True, proj=0.0)
    for foot in FOOTS:
        for f in (0.05, 0.4, 0.5, 0.6, 0.7):
            for lM in (8.0, 9.5, 10.5, 11.5, 12.5):
                for z in (0.1, 0.3, 0.5):
                    L = layout(10 ** lM, z, foot, ("set", f)); Rs = L["Rset"]
                    a, b = cold_mass(L, np.array([Rs * (1 - 1e-12), Rs * (1 + 1e-12)]))
                    An = L["X"] * L["Mb"] / m_nfw(L["rta"] / L["rs"]); cr = An * m_nfw(Rs / L["rs"])
                    worst["cont"] = max(worst["cont"], abs(a / cr - 1), abs(b / cr - 1))
                    worst["tot"] = max(worst["tot"], abs(float(cold_mass(L, np.array([L["rta"]]))[0]) / (L["X"] * L["Mb"]) - 1))
                    rr = np.logspace(-1, math.log10(L["rta"] * 2), 400); worst["mono"] &= bool(np.all(np.diff(cold_mass(L, rr)) >= -1e-9 * L["Mb"]))
                    _, M2 = project(L, np.array([L["rta"] * 0.999999])); worst["proj"] = max(worst["proj"], abs(float(M2[0]) / L["Mc"] - 1))
    rec("KA4_mass", worst["cont"] < 1e-9 and worst["tot"] < 1e-9 and worst["mono"] and worst["proj"] < 1e-5, **worst)
    # KA5 R_fold
    st = json.load(open(os.path.join(FLD, "hubble_canonical_M10.45_zi10_N2400.json")))["R_fold_end_kpc"]; got = float(rfold_kpc("canonical", 0.0, 10.45)[0])
    rec("KA5_rfold", abs(got / st - 1) < 1e-6, got=got, stored=st)
    # quadrature convergence (reported)
    L = layout(10 ** 10.9, 0.3, "canonical", ("set", 0.5)); R = np.logspace(0, math.log10(L["edge"] * 0.999), 80)
    P("projection 64 vs 160 nodes, max rel dev of DeltaSigma:", float(np.max(np.abs(dsig_exact(L, R, 64) / dsig_exact(L, R, 160) - 1))))
    P(f"example halo log M_b 10.9 z 0.3 canonical f 0.5: r_M {L['rM']:.2f} R_set {L['Rset']:.1f} r_ta {L['rta']:.1f} r_s {L['rs']:.1f} r_t {L['rt']:.1f} kpc, s {L['s']:.4f}")
    # KA7 kernel: tables against direct integration
    T = table("canonical", "f0.50"); k7 = {}
    # (b) d = 0 equals the own projection
    lM = np.array([10.3, 11.0, 11.7]); z = np.array([0.15, 0.3, 0.45]); R1 = np.tile(np.array([[30.0, 80.0, 200.0, 500.0, 1200.0]]), (3, 1)); R2 = R1 * 1.33
    own = own_cells(T, lM, z, R1, R2); nb0 = nb_cells(T, lM, z, np.full(3, 1e-6), R1, R2)
    ex = np.zeros_like(own)
    for a in range(3):
        L = layout(10 ** lM[a], z[a], "canonical", ("set", 0.5))
        for b in range(5):
            rr = np.exp(np.linspace(math.log(R1[a, b]), math.log(R2[a, b]), 2001)); ds = dsig_exact(L, rr)
            ex[a, b] = np.trapz(ds * rr * rr, np.log(rr)) / np.trapz(rr * rr, np.log(rr))
    k7["own_table_vs_exact"] = float(np.max(np.abs(own / ex - 1))); k7["centred_nb_vs_own"] = float(np.max(np.abs(nb0 / own - 1)))
    # (c) wholly inside / outside
    L = layout(10 ** 10.5, 0.3, "canonical", ("set", 0.5)); E = L["edge"]; Mt = L["Mb"] + L["Mc"]
    R1 = np.array([[3 * E, 6 * E]]); R2 = R1 * 1.33
    ins = nb_cells(T, np.array([10.5]), np.array([0.3]), np.array([1.5 * E]), R1, R2); pm = 2 * Mt * np.log(R2 / R1) / (math.pi * (R2 ** 2 - R1 ** 2))
    outs = nb_cells(T, np.array([10.5]), np.array([0.3]), np.array([12 * E]), R1, R2)
    k7["inside_vs_point"] = float(np.max(np.abs(ins / pm - 1))); k7["outside_abs_over_point"] = float(np.max(np.abs(outs / pm)))
    # (a) point step in closed form: baryon-only table
    Tb = dict(T); Tb["BFR"] = np.ones_like(T["BFR"]); R1 = np.array([[100.0, 300.0, 900.0]]); R2 = R1 * 1.33; d = np.array([350.0])
    st_ = nb_cells(Tb, np.array([10.5]), np.array([0.3]), d, R1, R2); Mt_ = halo_scalars(T, np.array([10.5]), np.array([0.3]))[1][0]
    exs = np.array([[0.0, (2 * Mt_ * math.log(399.0 / 350.0) - Mt_) / (math.pi * (399.0 ** 2 - 300.0 ** 2)), 2 * Mt_ * math.log(1.33) / (math.pi * (1197.0 ** 2 - 900.0 ** 2))]])
    k7["point_step"] = float(np.max(np.abs(st_ - exs)) / np.abs(exs).max())
    # (d) 200 random pairs: table against direct integration of the offset halo
    n = 200; lMj = rng.uniform(8.5, 12.5, n); zz = rng.uniform(0.1, 0.5, n); Rc = 10 ** rng.uniform(1.8, 3.4, n); dq = Rc * 10 ** rng.uniform(-0.5, 0.5, n)
    R1 = Rc[:, None]; R2 = R1 * 1.33; tb = nb_cells(T, lMj, zz, dq, R1, R2)[:, 0]; ex = np.zeros(n); sc = np.zeros(n)
    for a in range(n):
        L = layout(10 ** lMj[a], zz[a], "canonical", ("set", 0.5)); rr = np.exp(np.linspace(math.log(Rc[a]), math.log(1.33 * Rc[a]), 801))
        Md = mdisk_frac(L, np.full(801, dq[a]), rr, nq=96) * L["Mc"] + L["Mb"] * (rr > dq[a])
        ex[a] = (2 * np.trapz(Md, np.log(rr)) - (Md[-1] - Md[0])) / (math.pi * (rr[-1] ** 2 - rr[0] ** 2))
        sc[a] = (L["Mb"] + L["Mc"]) / (math.pi * rr[-1] ** 2)
    dv = np.abs(tb - ex) / sc; k7["random_pairs_abs_dev_over_point_scale"] = dict(max=float(dv.max()), median=float(np.median(dv)), mean_signed=float(np.mean((tb - ex) / sc)))
    ok7 = (k7["point_step"] < 1e-6 and k7["centred_nb_vs_own"] < 1e-3 and k7["own_table_vs_exact"] < 1e-3 and k7["inside_vs_point"] < 1e-4
           and k7["outside_abs_over_point"] < 1e-4 and dv.max() < 0.01)
    rec("KA7_kernel", ok7, **k7)
    json.dump(dict(lane="SRH1R", KA=KA, note="kappa = 1/2 FITTED; not theory closed; adopts nothing"), open(os.path.join(HERE, "srh1r_model_ka.json"), "w"), indent=1)
    open(os.path.join(HERE, "srh1r_model_ka.out"), "w").write("\n".join(OUT) + "\n")
