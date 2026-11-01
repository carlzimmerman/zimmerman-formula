"""Tier B: Ln, KiDS isolated lensing. Section 5. Set L."""
from crg1_core import *
from crg1_zoom import get_nr
from scipy.optimize import lsq_linear
from scipy.integrate import quad
from scipy.linalg import cholesky, solve_triangular

Gpc = 4.30091e-3
HN, ON, TT = 0.679, 0.3085, 1.0128
FF = (HN / 0.70) * TT
LMG = np.round(np.arange(6.8, 11.8 + 1e-9, 0.02), 2)
RGRID = np.logspace(1, 10, 3601); LR = np.log(RGRID)
TG = np.linspace(0, 12, 2401); WT = np.full(2401, TG[1] - TG[0]); WT[[0, -1]] *= 0.5
PL = os.path.join(INP, "lensing")

_zg = np.linspace(0, 1, 4001)
def chi_fn(Om):
    i = 1 / np.sqrt(Om * (1 + _zg) ** 3 + 1 - Om); c = np.zeros_like(_zg)
    c[1:] = np.cumsum(0.5 * (i[1:] + i[:-1]) * np.diff(_zg))
    return lambda z: np.interp(z, _zg, c)

def load():
    Rs, Ys = [], []
    for b in range(1, 5):
        a = np.loadtxt(os.path.join(PL, "Fig-3_Lensing-rotation-curves_Massbin-%d.txt" % b), comments="#")
        Rs.append(a[:, 0]); Ys.append(a[:, 1] / a[:, 4])
    R, Y = np.array(Rs), np.array(Ys)
    c = np.loadtxt(os.path.join(PL, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
    u0 = np.unique(c[:, 0]); u1 = np.unique(c[:, 1]); C = np.zeros((60, 60))
    mm = np.searchsorted(u0, c[:, 0]); nn = np.searchsorted(u1, c[:, 1])
    ii = np.abs(R[0][None, :] - c[:, 2][:, None]).argmin(1); jj = np.abs(R[0][None, :] - c[:, 3][:, None]).argmin(1)
    C[15 * mm + ii, 15 * nn + jj] = c[:, 4] / c[:, 6]
    d = np.load(os.path.join(PL, "lens_inventory.npz")); lm = d["logM"]; z = d["z"]; w = d["WLENS"]
    bins = np.digitize(lm, [8.5, 10.3, 10.6, 10.8, 11.0001]) - 1
    chiN, chi3, chiF = chi_fn(ON), chi_fn(0.3), chi_fn(0.2793)
    q = chiN(z) / chi3(z)
    out = dict(R=R, Y=Y, C=C, Yn=Y * FF, Cn=C * FF ** 2)
    Rn = np.zeros_like(R); zeff = []; Wg = np.zeros((4, len(LMG))); lens = []
    dl = LMG[1] - LMG[0]
    for b in range(4):
        s = bins == b; wb = w[s]; zb = z[s]; ze = (wb * zb).sum() / wb.sum(); zeff.append(ze)
        Rn[b] = R[b] * (0.70 / HN) * chiN(ze) / chiF(ze)
        li = lm[s] + 2 * math.log10(0.70 / HN) + 2 * np.log10(q[s])
        t = np.clip((li - LMG[0]) / dl, 0, len(LMG) - 1 - 1e-12); k = t.astype(int); fr = t - k
        np.add.at(Wg[b], k, wb * (1 - fr)); np.add.at(Wg[b], k + 1, wb * fr)
        Wg[b] /= wb.sum(); lens.append((li, wb))
    out.update(Rn=Rn, zeff=zeff, Wg=Wg, lens=lens)
    return out

class Stencil:
    def __init__(s, Rpc):
        s.R = Rpc.ravel(); lRc = np.log(s.R[:, None] * np.cosh(TG)[None, :])
        s.hi = lRc > LR[-1]; s.ix = np.clip(np.searchsorted(LR, lRc, side="right") - 1, 0, len(LR) - 2)
        s.fr = np.clip((lRc - LR[s.ix]) / (LR[s.ix + 1] - LR[s.ix]), 0, 1)
        s.a = (1 - np.tanh(TG))[None, :] * s.R[:, None] * np.sinh(TG)[None, :] * WT[None, :]
        s.b = (1 / np.cosh(TG))[None, :] * WT[None, :] / (2 * math.pi * s.R[:, None])
    def dsig(s, M, tail):
        dMdr = np.gradient(M, LR) / RGRID
        tv = dMdr[-1] if tail == "linear" else 0.0
        f = dMdr[s.ix] * (1 - s.fr) + dMdr[s.ix + 1] * s.fr; f[s.hi] = tv
        Mcyl = np.interp(np.log(s.R), LR, M) + (f * s.a).sum(1)
        return Mcyl / (math.pi * s.R ** 2) - (f * s.b).sum(1)

def baryon(lm):
    lm70 = lm - 2 * math.log10(0.70 / HN); lmc = lm + (-0.69 * lm70 + 6.63)
    Ms, Mcg = 10 ** lm, 10 ** lmc
    return Ms + Mcg + 0.5 * Ms * np.minimum(1, (RGRID / 1e5) ** 3), Ms + Mcg

class Sig5:
    def __init__(s, b):
        s.nodes = np.array([11., 12, 13, 14, 15]); s.v = np.log10([float(b.sigcoll(10 ** m)) for m in s.nodes])
    def __call__(s, M):
        l = math.log10(M); n, v = s.nodes, s.v
        if l <= n[0]: return 10 ** (v[0] + (l - n[0]) * (v[1] - v[0]) / (n[1] - n[0]))
        if l >= n[-1]: return 10 ** (v[-1] + (l - n[-1]) * (v[-1] - v[-2]) / (n[-1] - n[-2]))
        return 10 ** float(np.interp(l, n, v))

def tables(foot, L, st, nr):
    a0L = A0[foot] * 3.0857e16 / 1e6
    b = bg(BGS[0]); s5 = Sig5(b); shp = (len(LMG), 60)
    rc = 2.775e11 * b.h ** 2 / 1e18
    T = {k: np.zeros(shp) for k in ("L", "H_C3", "H_C4", "H_C3_A11b", "H_C4_A11b", "H_C1", "H_C1_A12b")}
    M200v = np.zeros(len(LMG)); R200v = np.zeros(len(LMG))
    floor = a0L / (2 * math.pi * Gpc)
    et3 = SC["ce1_a3_eta_med"]; 
    for i, lm in enumerate(LMG):
        MB, Mbm = baryon(float(lm))
        lgM2 = float(b.lgM200(math.log10(Mbm))); M2 = 10 ** lgM2; M200v[i] = M2
        R2 = (3 * M2 / (4 * math.pi * 200 * rc)) ** (1.0 / 3); R200v[i] = R2
        T["L"][i] = st.dsig(MB * nu(Gpc * MB / RGRID ** 2 / a0L), "linear")
        def H(S, B):
            r0 = solve_r0(M2, R2, S, B)
            return st.dsig(MB + math.pi * S * r0 ** 2 * B(np.minimum(RGRID, R2) / r0), "const")
        T["H_C3"][i] = H(max(floor, float(eta_C3(M2)) * s5(M2)), B_B)
        T["H_C4"][i] = H(max(floor, float(eta_A2(M2)) * s5(M2)), B_B)
        T["H_C3_A11b"][i] = H(max(floor, float(eta_C3(M2)) * float(b.sigcoll(M2))), B_B)
        T["H_C4_A11b"][i] = H(max(floor, float(eta_A2(M2)) * float(b.sigcoll(M2))), B_B)
        e = f_c * float(np.interp(lgM2, [12, 13, 14], [et3["12"], et3["13"], et3["14"]]))
        T["H_C1"][i] = H(max(floor, e * s5(M2)), B_S)
        Mt = M2 / f_c
        T["H_C1_A12b"][i] = H(f_c * float(nr.eta(Mt)) * s5(Mt) * float(nr.lowfac(Mt)), B_S)
    return T, M200v, R200v

class TwoHalo:
    def __init__(s, L):
        d = json.load(open(os.path.join(PL, "t1x_pgrav_x0.2562.json")))
        k = np.array(d["k_h_Mpc"], float); P_ = np.array(d["P_grav"], float); ok = (k > 0) & np.isfinite(P_) & (P_ > 0); k, P_ = k[ok], P_[ok]
        s.ht = 0.6736; s.Ot = (0.02237 + 0.1200) / s.ht ** 2; s.a = 1 / (1 + float(d["z"])); rs = 0.05
        rg = np.logspace(-2.5, 2, 900)
        s.lr = np.log(rg)
        s.xi = np.array([np.trapz(k ** 2 * P_ * np.sinc(k * r / math.pi) * np.exp(-(k * rs) ** 2), k) / (2 * math.pi ** 2) for r in rg])
        s.rho = s.Ot * 2.775e11
    def xif(s, r): return float(np.interp(math.log(r), s.lr, s.xi, left=s.xi[0], right=0.0))
    def esd2h(s, R, rex):
        Rc = R * s.ht / s.a; rc = rex * s.ht / s.a
        Rg = np.logspace(-3, math.log10(1.01 * Rc.max()), 220); Sg = np.zeros(220)
        for i, Rv in enumerate(Rg):
            t0 = math.sqrt(max(rc * rc - Rv * Rv, 0.0))
            if t0 >= 80: continue
            Sg[i] = 2 * s.rho * quad(lambda t: s.xif(math.sqrt(Rv * Rv + t * t)), t0, 80, limit=400)[0]
        c = np.zeros(220); c[1:] = np.cumsum(0.5 * (2 * math.pi * Rg[1:] * Sg[1:] + 2 * math.pi * Rg[:-1] * Sg[:-1]) * np.diff(Rg))
        return np.interp(Rc, Rg, c / (math.pi * Rg ** 2) - Sg) * s.ht / 1e12 / s.a ** 2

def sel(idx): return np.concatenate([15 * b + np.array(idx) for b in range(4)])

def fit(L, m, idx, T, bmax=np.inf):
    s = sel(idx); Cs = L["Cn"][np.ix_(s, s)]; Lc = cholesky(Cs, lower=True)
    res = (L["Yn"].ravel() - m)[s]; r0 = solve_triangular(Lc, res, lower=True)
    Afull = np.zeros((60, 4))
    for b in range(4): Afull[15 * b:15 * (b + 1), b] = T[b]
    A = solve_triangular(Lc, Afull[s], lower=True)
    bb = lsq_linear(A, r0, bounds=(0, bmax)).x
    mf = m + Afull @ bb; r = (L["Yn"].ravel() - mf)[s]
    return float(r @ np.linalg.solve(Cs, r)), bb

def stack(L, table):
    t = table.reshape(len(LMG), 4, 15)
    return np.concatenate([np.dot(L["Wg"][b], t[:, b, :]) for b in range(4)])

def main():
    if have_part("Ln"): return
    L = load(); st = Stencil(L["Rn"] * 1e6); nr = get_nr("a")
    TH = TwoHalo(L); rex = [0.343, 0.442, 0.433, 0.429]
    T0 = np.array([TH.esd2h(L["R"][b], rex[b]) * FF for b in range(4)])
    log("two-halo template done")
    IDX_ALL = list(range(15)); IDX_PRIM = [j for j in range(15) if L["R"][0][j] <= 0.31]
    out = {"n_prim_per_bin": len(IDX_PRIM), "zeff": L["zeff"]}
    T1 = None
    for foot in ("canonical", "alt"):
        Tb, M2v, R2v = tables(foot, L, st, nr); log("tables %s mem %.0fMB" % (foot, peak_mb()))
        above = M2v > 10 ** 12.3
        ENV3 = np.where(above[:, None], Tb["H_C3"], Tb["L"]); ENV3b = np.where(above[:, None], Tb["H_C3_A11b"], Tb["L"])
        mL = stack(L, Tb["L"]); ms = {k: stack(L, Tb[k]) for k in Tb}; mE3, mE3b = stack(L, ENV3), stack(L, ENV3b)
        def row(mH, mE, tag):
            r = {}
            for lab, idx in (("all", IDX_ALL), ("prim", IDX_PRIM)):
                cL, bL = fit(L, mL, idx, T0); cE, bE = fit(L, mE, idx, T0); cH, bH = fit(L, mH, idx, T0)
                r[lab] = dict(chi2_L2H=cL, chi2_ENV2H=cE, chi2_H2H=cH, d_ENV_L=cE - cL, d_ENV_H=cE - cH, b_L2H=bL, b_ENV2H=bE, b_H2H=bH)
            r["passed"] = bool(r["all"]["d_ENV_L"] <= 9 and r["all"]["d_ENV_H"] < 0)
            r["tag"] = tag
            return r
        C3 = row(ms["H_C3"], mE3, "[recomputed]"); C3["A11b"] = row(ms["H_C3_A11b"], mE3b, "A11b direct Sigma_coll")
        C4 = row(ms["H_C4"], mL, "[recomputed]"); C4["A11b"] = row(ms["H_C4_A11b"], mL, "A11b direct Sigma_coll")
        C3["share_lens_grid_above_T"] = float(above.mean())
        # C1 class
        if T1 is None:
            T1 = []
            for b in range(4):
                li, w = L["lens"][b]; r = np.interp(li, LMG, R2v); o = np.argsort(r, kind="stable"); cw = np.cumsum(w[o])
                mR = r[o][np.searchsorted(cw, 0.5 * w.sum(), side="left")]
                T1.append(TH.esd2h(L["R"][b], mR / 1e6) * FF)
            T1 = np.array(T1)
        def cls(d): return "LAW" if d >= 9 else ("HALOS" if d <= -9 else "NOT DIAGNOSTIC")
        def fc1(mH):
            d0 = fit(L, mH, IDX_ALL, T0)[0] - fit(L, mL, IDX_ALL, T0)[0]
            d1 = fit(L, mH, IDX_ALL, T1)[0] - fit(L, mL, IDX_ALL, T1)[0]
            d2 = fit(L, mH, IDX_ALL, T0, 1.0)[0] - fit(L, mL, IDX_ALL, T0, 1.0)[0]
            v = cls(d0)
            if v == "NOT DIAGNOSTIC" or cls(d1) != v or cls(d2) != v: v = "NOT DIAGNOSTIC"
            return dict(D0=d0, D1=d1, D2=d2, cls0=cls(d0), cls1=cls(d1), cls2=cls(d2), verdict=v, passed=v != "LAW")
        out[foot] = dict(C3=C3, C4=C4, C1=fc1(ms["H_C1"]), C1_A12b=fc1(ms["H_C1_A12b"]))
    save_part("Ln", out); log("Ln done")

if __name__ == "__main__": main()
