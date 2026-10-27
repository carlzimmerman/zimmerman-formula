#!/usr/bin/env python3
"""X55_one_halo_mass_for_both: is there ONE route-E halo-mass relation log M200 = a + b (log M_b - 10.5) that fits both
SPARC (a0-floor Burkert, X38 machinery and line, galaxy bootstrap) and the B21 KiDS isolated lenses (X53's (H2H))?

Criteria: FROZEN_CRITERIA.md + ASSUMPTION_LEDGER.md (32f994b55e, committed alone before any script or number).
X53's code (up to its scoring loop; it loads F2 and CFG805 read-only) and EM1's SPARC code (up to its backgrounds block)
are executed read-only in namespaces.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x55_one_halo.py               -> x55_one_halo.out, _results.json
    X55_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x55_one_halo.py  -> _MUTATE (lens M* +1 dex; K0_X53, K0_A1 must FAIL)
kappa = 1/2 FITTED; footings never pooled; cold dark energy is not matter; no dark-matter particle; not theory closed.
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
os.environ.pop("X53_MUTATE", None)
import io, json, math, time, resource, contextlib, itertools
import numpy as np
from scipy import stats

T0 = time.time()
MUT = os.environ.get("X55_MUTATE") == "1"
SFX = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
REB = os.path.dirname(HERE)
OUT, CHK = [], {}
RES = dict(lane="X55_one_halo_mass_for_both", criteria="32f994b55e", mutate=MUT)
np.seterr(all="ignore")
PIV = 10.5


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def check(name, ok, val):
    CHK[name] = bool(ok); P(f"  {name}: {'PASS' if ok else 'FAIL'}  ({val})")


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1e9 if sys.platform == "darwin" else 1e6)


# ============================================================ X53 machinery (read-only, up to its scoring loop)
X53D = os.path.join(REB, "X53_outer_lensing_law_vs_halos")
SRC = os.path.join(X53D, "x53_outer_lensing.py")
TX = open(SRC).read()
code = TX[:TX.index("for foot in FOOTS:\n    P(f\"\\n=== [{foot}]")]
NS = {"__file__": SRC, "__name__": "x53_ro"}
argv0 = sys.argv; sys.argv = [SRC]
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    exec(compile(code, SRC, "exec"), NS)
sys.argv = argv0
FOOTS = ("canonical", "alt")
INV, LMG, RGRID_PC, AQ = NS["INV"], NS["LMG"], NS["RGRID_PC"], NS["AQ"]
H_NAT, Rn, R, FN = NS["H_NAT"], NS["Rn"], NS["R"], NS["FN"]
IDX_ALL, IDX_PRIM, sel_of = NS["IDX_ALL"], NS["IDX_PRIM"], NS["sel_of"]
BGX, SIGA0, eta_of, sigma_coll, Bfun, SAT, solve_r0 = NS["BG"], NS["SIGA0"], NS["eta_of"], NS["sigma_coll"], NS["B"], NS["SAT"], NS["solve_r0"]
T2n = NS["T2n"]
HBG = BGX["A_c2b_refit"]["h"]
IDX_OUT = NS["NF"]["IDX_OUT"] if "NF" in NS else None
if IDX_OUT is None:
    IDX_OUT = [i for i in range(15) if NS["R"][0][i] > 0.4]
if MUT:
    for b in range(4):
        INV[b]["logMs70"] = INV[b]["logMs70"] + 1.0                     # MUTATE: lens stellar masses +1 dex
P(f"X55_one_halo_mass_for_both{'  [MUTATE: lens M* +1 dex]' if MUT else ''}   criteria 32f994b55e")
P("kappa = 1/2 FITTED; footings never pooled; route E: Newtonian + a0-floor Burkert cold dark energy halos; relation log M200 = a + b (log Mb - 10.5)")
P(f"X53 machinery loaded read-only (F2 inventory, CFG805 2h); native factor f {FN:.4f}  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
Yn0, Cn0 = NS["Yn"], NS["Cn"]

# ============================================================ step 0 items 1 and 2 (X53 chi2; A1 shifts)
X53J = json.load(open(os.path.join(X53D, "x53_outer_lensing_results.json")))
A1J = json.load(open(os.path.join(X53D, "x53_diag_A1_results.json")))
HP = dict(NS["H_PRIMARY"])
stack_model, stack_H, fit, CENTRAL0 = NS["stack_model"], NS["stack_H"], NS["fit"], NS["CENTRAL0"]
S0 = {}; ok1 = True; LAWK = {}; MH0 = {}
for foot in FOOTS:
    mL = stack_model(foot, Rn, CENTRAL0); mH, _ = stack_H(foot, HP); SAT["n"] = 0; MH0[foot] = mH
    for lab, idx in (("primary", IDX_PRIM), ("all", IDX_ALL)):
        v = dict(L=fit(mL, idx, False)[0]["chi2"], H=fit(mH, idx, False)[0]["chi2"], L2H=fit(mL, idx, True)[0]["chi2"], H2H=fit(mH, idx, True)[0]["chi2"])
        for k in v:
            ref = X53J["footings"][foot][lab][k]["chi2"]; p = abs(v[k] - ref) < 0.05; ok1 &= p
            S0[f"{foot}|{lab}|{k}"] = dict(value=v[k], frozen=ref, pass_=p)
        LAWK[(foot, lab)] = v
        P(f"  step0.1 X53 [{foot} {lab}] L {v['L']:.3f} H {v['H']:.3f} L2H {v['L2H']:.3f} H2H {v['H2H']:.3f} (committed "
          + " ".join(f"{X53J['footings'][foot][lab][k]['chi2']:.3f}" for k in ("L", "H", "L2H", "H2H")) + ")")
check("K0_X53", ok1, "X53 L/H/L2H/H2H chi2 within 0.05, both ranges, both footings")
RES["step0_X53"] = S0
EMJ = json.load(open(os.path.join(HERE, "x55_step0_em1_results.json")))
P(f"  step0.3 EM1 rerun (x55_step0_em1.py): " + "; ".join(f"{t} a {v['a']:.2f} b {v['b']:.2f} rms {v['rms']:.5f}" for t, v in EMJ["rows"].items()))
check("K0_EM1", EMJ["pass_"], "x55_step0_em1_results.json")


# ============================================================ KiDS: halo tables on log M200, lens weight matrices
LMH = np.round(np.arange(8.0, 15.0001, 0.01), 2); NH = len(LMH)
def rhoc_pc():
    return 2.775e11 * HBG ** 2 / 1e18                                         # Msun/pc^3, 200 rho_crit,0, bg A h (X38/X53)


def halo_core(foot, lM, rule):
    """(Sigma [Msun/pc^2], R200 [pc], r0 [pc], saturated) for one log M200; rule 'floor' or 'x43' (c_f 4)."""
    M200 = 10 ** lM; R200 = (3 * M200 / (4 * math.pi * 200 * rhoc_pc())) ** (1 / 3)
    Sig = SIGA0[foot] if rule == "floor" else max(SIGA0[foot], eta_of(M200, "cf4") * sigma_coll(M200))
    n0 = SAT["n"]; r0 = solve_r0(M200, R200, Sig); sat = SAT["n"] > n0; SAT["n"] = 0
    return Sig, R200, r0, sat


def kids_halo_table(foot, trunc=True):
    tab = np.empty((4, NH, 15)); sat = np.zeros(NH, bool)
    for k, lM in enumerate(LMH):
        Sig, R200, r0, s = halo_core(foot, float(lM), "x43"); sat[k] = s
        rcut = R200 if trunc else 100 * R200
        Mh = math.pi * Sig * r0 ** 2 * Bfun(np.minimum(RGRID_PC, rcut) / r0)
        for b in range(4):
            tab[b, k] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, Mh, "const")
    return tab, sat


# baryons per LMG node (Newtonian, F2 inventory; identical to X53 mass_H(halo=False))
DSB = np.empty((4, len(LMG), 15)); LMBREL = np.empty(len(LMG))
for j, lm in enumerate(LMG):
    Mb, _ = NS["mass_H"]("canonical", float(lm), H_NAT, HP, halo=False)
    lm70 = lm - 2 * np.log10(0.70 / H_NAT); lmc = lm + (-0.69 * lm70 + 6.63)
    LMBREL[j] = math.log10(10 ** lm + 10 ** lmc)
    for b in range(4):
        DSB[b, j] = AQ.delta_sigma(Rn[b] * 1e6, RGRID_PC, Mb, "const")


def lens_W(delta):
    """per bin: (n_LMG,) weights so that stacked = W @ table, identical to np.interp at the lens masses (+ delta dex)."""
    W = np.zeros((4, len(LMG))); stats_ = []
    for b in range(4):
        x = INV[b]["logMs70"] + 2 * np.log10(0.70 / H_NAT) + 2 * np.log10(INV[b]["qDA"]) + delta
        w = INV[b]["w"] / INV[b]["w"].sum()
        xc = np.clip(x, LMG[0], LMG[-1]); j = np.clip(np.searchsorted(LMG, xc) - 1, 0, len(LMG) - 2)
        t = (xc - LMG[j]) / (LMG[j + 1] - LMG[j])
        np.add.at(W[b], j, (1 - t) * w); np.add.at(W[b], j + 1, t * w)
        lmb = np.interp(xc, LMG, LMBREL)
        o = np.argsort(lmb); cw = np.cumsum(w[o])
        pc = [float(lmb[o][np.searchsorted(cw, q)]) for q in (0.05, 0.16, 0.5, 0.84, 0.95)]
        stats_.append(dict(mean=float(np.sum(w * lmb)), p05=pc[0], p16=pc[1], p50=pc[2], p84=pc[3], p95=pc[4], lmb=lmb, w=INV[b]["w"]))
    return W, stats_


# ============================================================ (a, b) grid and vectorised chi2 with b_eff >= 0
AGR = np.round(np.arange(10.0, 14.0001, 0.02), 2); BGR = np.round(np.arange(-0.5, 2.5001, 0.02), 2)
NA, NB = len(AGR), len(BGR)


def kids_models(DSH, W, a_arr, b_val, sat=None):
    """stacked (n_a, 4, 15) for relation (a_arr, b_val); also lens-weight fraction saturated per bin (n_a, 4)."""
    nz = np.where(W.sum(0) > 0)[0]
    lM = a_arr[:, None] + b_val * (LMBREL[nz][None, :] - PIV)                  # (n_a, nz)
    x = np.clip((lM - LMH[0]) / 0.01, 0, NH - 1 - 1e-9); k = np.floor(x).astype(int); t = x - k
    out = np.empty((len(a_arr), 4, 15)); fs = np.zeros((len(a_arr), 4))
    for b in range(4):
        H = DSH[b][k] * (1 - t)[..., None] + DSH[b][k + 1] * t[..., None]   # (n_a, nz, 15)
        out[:, b] = np.einsum("j,ajr->ar", W[b, nz], H + DSB[b][nz][None])
        if sat is not None:
            fs[:, b] = (sat[np.rint(x).astype(int)] * W[b, nz][None]).sum(1)
    return out, fs


def make_chi2(Y, C, idx):
    s = sel_of(idx); Lc = np.linalg.cholesky(C[np.ix_(s, s)])
    A = np.zeros((60, 4))
    for b in range(4):
        A[15 * b:15 * b + 15, b] = T2n[b]
    Aw = np.linalg.solve(Lc, A[s]); Yv = Y.ravel()[s]
    subs = [list(S) for n in range(5) for S in itertools.combinations(range(4), n)]
    pre = []
    for S in subs:
        if S:
            AS = Aw[:, S]; pre.append((S, AS, np.linalg.inv(AS.T @ AS)))
        else:
            pre.append((S, None, None))

    def chi2(models):
        r = Yv[None, :] - models.reshape(len(models), 60)[:, s]
        rw = np.linalg.solve(Lc, r.T).T                                           # (n, ns)
        base = np.sum(rw * rw, 1); best = base.copy(); bb = np.zeros((len(models), 4))
        for S, AS, Gi in pre:
            if not S:
                continue
            u = rw @ AS; c = u @ Gi; x2 = base - np.sum(u * c, 1)
            okk = np.all(c >= -1e-12, 1) & (x2 < best)
            best = np.where(okk, x2, best)
            if okk.any():
                bb[okk] = 0.0
                for i_, sidx in enumerate(S):
                    bb[okk, sidx] = c[okk, i_]
        return best, bb
    return chi2, len(s)


def kids_grid(DSH, sat, W, chi2f):
    X2 = np.empty((NA, NB)); FS = np.empty((NA, NB, 4)); BE = np.empty((NA, NB, 4))
    for jb, bv in enumerate(BGR):
        m, fs = kids_models(DSH, W, AGR, float(bv), sat)
        X2[:, jb], BE[:, jb] = chi2f(m); FS[:, jb] = fs
    return X2, FS, BE


def nsig(d2):
    d2 = np.maximum(np.asarray(d2, float), 0.0)
    return stats.norm.isf(np.maximum(stats.chi2.sf(d2, 2), 1e-300) / 2)


# ============================================================ SPARC: EM1 machinery read-only (up to backgrounds), X38 floor
EM1SRC = os.path.join(REB, "EM1_emergent_dust_law", "em1_emergent.py"); TE = open(EM1SRC).read()
NE = {"__file__": EM1SRC, "__name__": "em1_ro"}; sys.argv = [EM1SRC]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(TE[:TE.index("# ---------------- backgrounds")], EM1SRC, "exec"), NE)
sys.argv = argv0
GALS, fit_one, LAWS, UPS, A0E = NE["GALS"], NE["fit_one"], NE["LAW"], NE["UPS"], NE["A0"]
GE, MSUNE, MPCE = NE["G"], NE["MSUN"], NE["MPC"]
NG = len(GALS); LMB = np.array([q["lMb"] for q in GALS])
PC = 3.0857e16
P(f"EM1 SPARC machinery loaded read-only: {NG} galaxies; law rms {LAWS['canonical']['rms']:.4f} / {LAWS['alt']['rms']:.4f}  [{time.time() - T0:.0f} s]")


def sparc_tables(foot, rule):
    """per galaxy, on LMH: best-Upsilon wr2, ws, Upsilon index; plus saturation flag per LMH node."""
    rc = 3 * (100 * HBG * 1e3 / MPCE) ** 2 / (8 * math.pi * GE)
    r0s = np.empty(NH); sigs = np.empty(NH); sat = np.zeros(NH, bool)
    for k, lM in enumerate(LMH):
        M200 = 10 ** lM * MSUNE; R200 = (3 * M200 / (4 * math.pi * 200 * rc)) ** (1 / 3)
        Sig = A0E[foot] / (2 * math.pi * GE)
        if rule == "x43":
            Sig = max(Sig, eta_of(10 ** lM, "cf4") * sigma_coll(10 ** lM) * MSUNE / PC ** 2)
        n0 = SAT["n"]; r0s[k] = solve_r0(M200, R200, Sig); sat[k] = SAT["n"] > n0; SAT["n"] = 0; sigs[k] = Sig
    WR2 = np.empty((NG, NH)); WS = np.empty((NG, NH)); IU = np.empty((NG, NH), int)
    for g, q in enumerate(GALS):
        for c0 in range(0, NH, 120):
            sl = slice(c0, min(NH, c0 + 120))
            gh = GE * math.pi * sigs[sl, None] * r0s[sl, None] ** 2 * Bfun(q["Rm"][None, :] / r0s[sl, None]) / q["Rm"][None, :] ** 2
            lgp = np.log10(np.maximum(q["GB"][None, :, :] + gh[:, :, None], 1e-300))
            WR2[g, sl], WS[g, sl], IU[g, sl] = fit_one(q, lgp)
    return WR2, WS, IU, sat


def sparc_node_tables(WR2, WS, IU, sat, gsel=None):
    """(n_gal, NA, NB) interpolated wr2 / ws, nearest Upsilon index and saturation."""
    gs = np.arange(NG) if gsel is None else gsel
    n = len(gs); tw = np.empty((n, NA, NB)); tsum = np.empty((n, NA, NB)); iu = np.empty((n, NA, NB), np.int16)
    sn = np.empty((n, NA, NB), bool); off = np.empty((n, NA, NB), bool)
    for c0 in range(0, n, 10):                                                  # galaxy chunks (memory)
        g = gs[c0:c0 + 10]
        lM = AGR[None, :, None] + BGR[None, None, :] * (LMB[g][:, None, None] - PIV)
        x = np.clip((lM - LMH[0]) / 0.01, 0, NH - 1 - 1e-9); k = np.floor(x).astype(np.int32); t = x - k; kn = np.rint(x).astype(np.int32)
        gi = g[:, None, None]
        tw[c0:c0 + 10] = WR2[gi, k] * (1 - t) + WR2[gi, k + 1] * t
        tsum[c0:c0 + 10] = WS[gi, k] * (1 - t) + WS[gi, k + 1] * t
        iu[c0:c0 + 10] = IU[gi, kn]; sn[c0:c0 + 10] = sat[kn]; off[c0:c0 + 10] = (lM < LMH[0]) | (lM > LMH[-1])
    return tw, tsum, iu, sn, off


def sparc_fit(tw, tsum, iu, satn, seed=55, nboot=1000):
    rms = np.sqrt(tw.sum(0) / tsum.sum(0))
    medU = np.median(UPS[iu], axis=0)
    i, j = np.unravel_index(np.argmin(rms), rms.shape)
    rng = np.random.default_rng(seed); ng = tw.shape[0]
    cnt = np.stack([np.bincount(rng.integers(0, ng, ng), minlength=ng) for _ in range(nboot)]).astype(float)
    TWf, TSf = tw.reshape(ng, -1), tsum.reshape(ng, -1)
    bi = np.empty(nboot, int)
    for c0 in range(0, nboot, 50):
        num = cnt[c0:c0 + 50] @ TWf; den = cnt[c0:c0 + 50] @ TSf
        bi[c0:c0 + 50] = np.argmin(num / den, 1)
    ab = np.stack([AGR[bi // NB], BGR[bi % NB]], 1)
    cov = np.cov(ab.T); ci = np.linalg.inv(cov)
    dA = AGR[:, None] - AGR[i]; dB = BGR[None, :] - BGR[j]
    d2 = ci[0, 0] * dA ** 2 + 2 * ci[0, 1] * dA * dB + ci[1, 1] * dB ** 2
    edge = float(np.mean((ab[:, 0] <= AGR[0]) | (ab[:, 0] >= AGR[-1]) | (ab[:, 1] <= BGR[0]) | (ab[:, 1] >= BGR[-1])))
    return dict(rms=rms, medU=medU, ibest=(int(i), int(j)), a=float(AGR[i]), b=float(BGR[j]), boot=ab, cov=cov, d2=d2,
                nsat=satn.sum(0), edge=edge, line=(rms <= 0.110) & (medU >= 0.50) & (medU <= 0.80))


def regions_text(d2, lab):
    out = {}
    for n_, thr in ((1, 2.2958), (2, 6.1801)):
        m = d2 <= thr
        if m.any():
            ia, ib = np.where(m)
            out[f"{n_}sigma"] = dict(a=[float(AGR[ia].min()), float(AGR[ia].max())], b=[float(BGR[ib].min()), float(BGR[ib].max())], n_nodes=int(m.sum()))
        else:
            out[f"{n_}sigma"] = None
    return out


def separation(d2S, d2K, mask=None):
    ns = np.maximum(nsig(d2S), nsig(d2K))
    if mask is not None:
        ns = np.where(mask, ns, np.inf)
    if not np.isfinite(ns).any():
        return None, None
    i, j = np.unravel_index(np.argmin(ns), ns.shape)
    return float(ns[i, j]), (int(i), int(j))


def cls_of(n, informative):
    if n is None:
        return "UNDECIDED (no line-passing node)"
    if n <= 2:
        return "ONE RELATION FITS BOTH" if informative else "NOT INFORMATIVE"
    return "TENSION" if n < 3 else "CONTRADICTION"


# ============================================================ main loop per footing
K0A1 = True; FT = {}
for foot in FOOTS:
    P(f"\n=== [{foot}]  a0 {A0E[foot]:.4e} m/s^2; Sigma_a0 {SIGA0[foot]:.1f} Msun/pc^2")
    fo = {}
    DSH, satK = kids_halo_table(foot, True)
    W0, LST = lens_W(0.0)
    P(f"  KiDS halo table: log M200 8-15, saturated above 10^{LMH[np.argmax(satK)]:.2f}" if satK.any() else "  KiDS halo table: no saturation on 8-15")
    for b in range(4):
        P(f"  lens bin {b + 1}: log Mb (M* + cold, native) mean {LST[b]['mean']:.3f}, 5-95 % {LST[b]['p05']:.2f}-{LST[b]['p95']:.2f}")
    fo["lens_Mb"] = [{k: v for k, v in s.items() if k not in ("lmb", "w")} for s in LST]
    chiA, nA = make_chi2(Yn0, Cn0, IDX_ALL); chiP, nP = make_chi2(Yn0, Cn0, IDX_PRIM)
    # K_NNLS and K_TAB / step0.2 (A1 shifts) with the table
    mT, _ = kids_models(DSH, W0, np.array([11.18 + 0.9 * 0.5]), 0.9)
    xa, _ = chiA(mT); xr = fit(MH0[foot], IDX_ALL, True)[0]["chi2"]
    xm = fit(mT[0], IDX_ALL, True)[0]["chi2"]
    if foot == "canonical":
        check("K_NNLS_matches_X53_fit", abs(xa[0] - xm) < 1e-6, f"{xa[0]:.6f} vs {xm:.6f}")
    check(f"K_TAB_{foot}", abs(xa[0] - xr) < 0.1, f"table H2H all {xa[0]:.3f} vs X53 stack_H {xr:.3f}")
    SH = np.round(np.arange(-0.3, 1.2001, 0.05), 2)
    mS, _ = kids_models(DSH, W0, 11.18 + 0.9 * 0.5 + SH, 0.9)
    for lab, cf in (("primary", chiP), ("all", chiA)):
        x2, _ = cf(mS); k = int(np.argmin(x2)); ref = A1J["footings"][foot]["truncated"][lab]
        p = abs(SH[k] - ref["common_shift"]) < 1e-9 and abs(x2[k] - ref["chi2_common"]) < 0.2; K0A1 &= p
        P(f"  step0.2 A1 [{lab}] best common shift {SH[k]:+.2f} chi2 {x2[k]:.2f} (A1 {ref['common_shift']:+.2f} / {ref['chi2_common']:.2f}): {'PASS' if p else 'FAIL'}")
    # ---------------- SPARC tables (floor, primary) and step0.4 (X38 row)
    t1 = time.time()
    WR2, WS, IU, satS = sparc_tables(foot, "floor")
    tw, ts, iu, sn, offg = sparc_node_tables(WR2, WS, IU, satS)
    # X38 point (11.18 + 0.45 = 11.63 at pivot 10.5) is off the 0.02 grid: evaluate directly
    lM38 = 11.18 + 0.9 * (LMB - 10.0); x = (lM38 - LMH[0]) / 0.01; k = np.floor(x).astype(int); t = x - k
    g_ = np.arange(NG)
    rms38 = math.sqrt(np.sum(WR2[g_, k] * (1 - t) + WR2[g_, k + 1] * t) / np.sum(WS[g_, k] * (1 - t) + WS[g_, k + 1] * t))
    u38 = float(np.median(UPS[IU[g_, np.rint(x).astype(int)]])); s38 = int(satS[np.rint(x).astype(int)].sum())
    ref38 = {"canonical": (0.0795, 0.77), "alt": (0.0729, 0.60)}[foot]
    p4 = abs(rms38 - ref38[0]) < 2e-4 and abs(u38 - ref38[1]) <= 0.0101 and s38 == 0
    P(f"  step0.4 X38 SPARC row at EM1's relation: rms {rms38:.4f} median U {u38:.2f} saturated {s38} (X38 {ref38[0]} / {ref38[1]} / 0): {'PASS' if p4 else 'FAIL'}  [{time.time() - t1:.0f} s]")
    CHK[f"K0_X38_{foot}"] = bool(p4)
    SP = sparc_fit(tw, ts, iu, sn)
    i, j = SP["ibest"]
    fo["sparc_floor_saturation"] = dict(first_saturated_lM200=(float(LMH[np.argmax(satS)]) if satS.any() else None), grid_nodes_with_any=int((SP["nsat"] > 0).sum()),
                                        grid_nodes=int(NA * NB))
    P(f"  SPARC floor halos saturate (R200 at 200 rho_c0) above log M200 {fo['sparc_floor_saturation']['first_saturated_lM200']}; "
      f"(a, b) grid nodes with any saturated galaxy {fo['sparc_floor_saturation']['grid_nodes_with_any']} of {NA * NB}")
    P(f"  SPARC best fit (floor): a {SP['a']:.2f} b {SP['b']:.2f}: rms {SP['rms'][i, j]:.4f}, median U {SP['medU'][i, j]:.2f}, line {bool(SP['line'][i, j])}, saturated {int(SP['nsat'][i, j])}; "
          f"bootstrap sd a {math.sqrt(SP['cov'][0, 0]):.3f} b {math.sqrt(SP['cov'][1, 1]):.3f} corr {SP['cov'][0, 1] / math.sqrt(SP['cov'][0, 0] * SP['cov'][1, 1]):+.2f}; boot at grid edge {SP['edge']:.3f}")
    # SPARC log M200 at the lens-bin masses (bootstrap)
    infw = []; spM = []
    for b in range(4):
        v = SP["boot"][:, 0] + SP["boot"][:, 1] * (LST[b]["mean"] - PIV)
        q = np.percentile(v, [2.5, 16, 50, 84, 97.5]); infw.append(float(q[3] - q[1])); spM.append(q.tolist())
    informative = all(wd <= 0.30 for wd in infw)
    P(f"  SPARC log M200 at lens-bin mean Mb (boot 16/50/84): " + "; ".join(f"bin{b + 1} {spM[b][1]:.2f}/{spM[b][2]:.2f}/{spM[b][3]:.2f} (w {infw[b]:.2f})" for b in range(4))
      + f" -> informative (all <= 0.30 dex): {informative}")
    # ---------------- KiDS graded grid
    t1 = time.time()
    X2, FS, BE = kids_grid(DSH, satK, W0, chiA)
    ki, kj = np.unravel_index(np.argmin(X2), X2.shape); dof = nA - 4 - 2; sK = max(1.0, X2[ki, kj] / dof)
    d2K = (X2 - X2[ki, kj]) / sK; d2Ku = X2 - X2[ki, kj]
    P(f"  KiDS best fit (all radii, 2h, c_f 4, truncated): a {AGR[ki]:.2f} b {BGR[kj]:.2f}: chi2 {X2[ki, kj]:.1f} / dof {dof} -> Birge s_K {sK:.2f}; "
      f"b_eff {np.round(BE[ki, kj], 2).tolist()}; saturated lens weight per bin {np.round(FS[ki, kj], 3).tolist()}  [{time.time() - t1:.0f} s]")
    kM = []
    for b in range(4):
        lmv = AGR[:, None] + BGR[None, :] * (LST[b]["mean"] - PIV); m1 = (X2 - X2[ki, kj]) / sK <= 1.0
        kM.append([float(lmv[m1].min()), float(lmv[ki, kj]), float(lmv[m1].max())])
    P(f"  KiDS log M200 at lens-bin mean Mb (best; profile 68 % Birge): " + "; ".join(f"bin{b + 1} {kM[b][1]:.2f} [{kM[b][0]:.2f}, {kM[b][2]:.2f}]" for b in range(4)))
    # ---------------- separation (graded: line-passing nodes)
    nsep, node = separation(SP["d2"], d2K, SP["line"])
    nsep_u, node_u = separation(SP["d2"], d2K, None)
    nsep_raw, node_raw = separation(SP["d2"], d2Ku, SP["line"])
    cl = cls_of(nsep, informative) if (ok1 and EMJ["pass_"] and K0A1 and p4) else "UNDECIDED (step 0 failed)"

    def node_info(nd):
        if nd is None:
            return None
        a_, b_ = nd
        return dict(a=float(AGR[a_]), b=float(BGR[b_]), sparc_rms=float(SP["rms"][a_, b_]), sparc_medU=float(SP["medU"][a_, b_]), sparc_line=bool(SP["line"][a_, b_]),
                    sparc_saturated=int(SP["nsat"][a_, b_]), nsig_S=float(nsig(SP["d2"][a_, b_])), kids_chi2_all=float(X2[a_, b_]), kids_b_eff=BE[a_, b_].tolist(),
                    nsig_K=float(nsig(d2K[a_, b_])), kids_sat_weight=FS[a_, b_].tolist(),
                    lM200_at_bins=[float(AGR[a_] + BGR[b_] * (LST[b]["mean"] - PIV)) for b in range(4)])
    J0 = node_info(node)
    P(f"  SEPARATION (line-passing nodes): n_sep {nsep:.2f} sigma at a {J0['a']:.2f} b {J0['b']:.2f}: SPARC rms {J0['sparc_rms']:.4f} U {J0['sparc_medU']:.2f} "
      f"(n_S {J0['nsig_S']:.2f}, sat {J0['sparc_saturated']}); KiDS chi2 {J0['kids_chi2_all']:.1f} (n_K {J0['nsig_K']:.2f}, b_eff {np.round(J0['kids_b_eff'], 2).tolist()}, sat weight {np.round(J0['kids_sat_weight'], 3).tolist()})")
    P(f"     law for comparison: SPARC rms {LAWS[foot]['rms']:.4f} (U {LAWS[foot]['U_median']:.2f}); KiDS L2H all {LAWK[(foot, 'all')]['L2H']:.1f}, L {LAWK[(foot, 'all')]['L']:.1f}")
    P(f"     unrestricted (no line): n_sep {nsep_u:.2f} at a {AGR[node_u[0]]:.2f} b {BGR[node_u[1]]:.2f}; unscaled KiDS (s_K 1): n_sep {nsep_raw:.2f}")
    P(f"  CLASS [{foot}]: {cl}")
    jd = np.unravel_index(np.argmin(SP["d2"] + d2K), d2K.shape)
    fo.update(sparc=dict(a=SP["a"], b=SP["b"], rms=float(SP["rms"][i, j]), medU=float(SP["medU"][i, j]), line=bool(SP["line"][i, j]), saturated=int(SP["nsat"][i, j]),
                         boot_cov=SP["cov"].tolist(), boot_sd=[math.sqrt(SP["cov"][0, 0]), math.sqrt(SP["cov"][1, 1])], boot_edge_frac=SP["edge"],
                         regions=regions_text(SP["d2"], "S"), lM200_at_lens_bins_boot_2p5_16_50_84_97p5=spM, width68_at_lens_bins=infw, informative=informative,
                         n_line_nodes=int(SP["line"].sum()), sat_nodes_in_2sigma=int(((SP["d2"] <= 6.1801) & (SP["nsat"] > 0)).sum())),
              kids=dict(a=float(AGR[ki]), b=float(BGR[kj]), chi2=float(X2[ki, kj]), dof=dof, s_K=sK, b_eff=BE[ki, kj].tolist(), sat_weight=FS[ki, kj].tolist(),
                        regions=regions_text(d2K, "K"), regions_unscaled=regions_text(d2Ku, "K"), lM200_at_lens_bins_best_and_68=kM,
                        sat_nodes_in_2sigma=int(((d2K <= 6.1801) & (FS.max(2) > 0)).sum()),
                        sparc_at_kids_best=dict(rms=float(SP["rms"][ki, kj]), medU=float(SP["medU"][ki, kj]), saturated=int(SP["nsat"][ki, kj]), nsig_S=float(nsig(SP["d2"][ki, kj])))),
              n_sep=nsep, joint=J0, n_sep_unrestricted=nsep_u, joint_unrestricted=node_info(node_u), n_sep_unscaled_kids=nsep_raw,
              joint_min_sum=node_info(jd), sparc_at_EM1=dict(rms=rms38, medU=u38, saturated=s38), cls=cl,
              law=dict(sparc_rms=LAWS[foot]["rms"], sparc_U=LAWS[foot]["U_median"], kids_L2H_all=LAWK[(foot, "all")]["L2H"], kids_L_all=LAWK[(foot, "all")]["L"],
                       kids_L2H_primary=LAWK[(foot, "primary")]["L2H"]))
    P(f"     SPARC at the KiDS best fit: rms {SP['rms'][ki, kj]:.4f} U {SP['medU'][ki, kj]:.2f} sat {int(SP['nsat'][ki, kj])} (n_S {float(nsig(SP['d2'][ki, kj])):.2f}); "
      f"KiDS at the SPARC best fit: chi2 {X2[i, j]:.1f} (n_K {float(nsig(d2K[i, j])):.2f}); saturated lens weight {np.round(FS[i, j], 3).tolist()}")
    P(f"     regions SPARC {json.dumps(fo['sparc']['regions'])}")
    P(f"     regions KiDS  {json.dumps(fo['kids']['regions'])}   (unscaled {json.dumps(fo['kids']['regions_unscaled'])})")
    P(f"     nodes inside 2 sigma with any saturation: SPARC {fo['sparc']['sat_nodes_in_2sigma']}, KiDS {fo['kids']['sat_nodes_in_2sigma']}")
    P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    # ---------------- reported variants
    var = {}

    def kids_variant(lab, DSH_, sat_, W_, cf_, nidx):
        X2v, FSv, BEv = kids_grid(DSH_, sat_, W_, cf_)
        a_, b_ = np.unravel_index(np.argmin(X2v), X2v.shape); dofv = nidx - 6; sv = max(1.0, X2v[a_, b_] / dofv); d2v = (X2v - X2v[a_, b_]) / sv
        n1, nd1 = separation(SP["d2"], d2v, SP["line"])
        o = dict(kids_a=float(AGR[a_]), kids_b=float(BGR[b_]), chi2=float(X2v[a_, b_]), s_K=sv, n_sep=n1, joint=None if nd1 is None else [float(AGR[nd1[0]]), float(BGR[nd1[1]])],
                 sat_weight_best=FSv[a_, b_].tolist(), cls=cls_of(n1, informative))
        var[lab] = o
        P(f"  (reported) {lab}: KiDS best a {o['kids_a']:.2f} b {o['kids_b']:.2f} chi2 {o['chi2']:.1f} s_K {sv:.2f}; n_sep {n1:.2f} -> {o['cls']}")
        return d2v
    for dl in (-0.15, +0.15):
        Wd, _ = lens_W(dl)
        kids_variant(f"lens M* {dl:+.2f} dex", DSH, satK, Wd, chiA, nA)
    d2P = kids_variant("primary range R <= 0.31 Mpc (leakage test i)", DSH, satK, W0, chiP, nP)
    DSHu, satU = kids_halo_table(foot, False)
    kids_variant("untruncated halos (100 R200)", DSHu, satU, W0, chiA, nA)
    Y2 = Yn0.copy(); C2 = Cn0.copy(); fac = np.ones(60)
    for b in range(4):
        for ii in IDX_OUT:
            fac[15 * b + ii] = 0.64
    Y2 = (Y2.ravel() * fac).reshape(4, 15); C2 = C2 * np.outer(fac, fac)
    chiL, _ = make_chi2(Y2, C2, IDX_ALL)
    kids_variant("outer data x 0.64 (F2 GAMA/KiDS; leakage test ii)", DSH, satK, W0, chiL, nA)
    # SPARC with the X43 rule
    WR2x, WSx, IUx, satSx = sparc_tables(foot, "x43")
    SPx = sparc_fit(*sparc_node_tables(WR2x, WSx, IUx, satSx)[:4])
    nx, ndx = separation(SPx["d2"], d2K, SPx["line"])
    var["SPARC with X43 rule (c_f 4)"] = dict(a=SPx["a"], b=SPx["b"], rms=float(SPx["rms"][SPx["ibest"]]), n_sep=nx, cls=cls_of(nx, informative))
    P(f"  (reported) SPARC with X43 rule: best a {SPx['a']:.2f} b {SPx['b']:.2f} rms {float(SPx['rms'][SPx['ibest']]):.4f}; n_sep {nx:.2f}")
    del WR2x, WSx, IUx, SPx
    # restricted overlap
    allm = np.concatenate([LST[b]["lmb"] for b in range(4)]); allw = np.concatenate([LST[b]["w"] for b in range(4)])
    o = np.argsort(allm); cw = np.cumsum(allw[o]); lo, hi = allm[o][np.searchsorted(cw, 0.05 * cw[-1])], allm[o][np.searchsorted(cw, 0.95 * cw[-1])]
    gsel = np.where((LMB >= lo) & (LMB <= hi))[0]
    twr, tsr, iur, snr, _ = sparc_node_tables(WR2, WS, IU, satS, gsel)
    SPr = sparc_fit(twr, tsr, iur, snr)
    nr, ndr = separation(SPr["d2"], d2K, SPr["line"]); nrp, _ = separation(SPr["d2"], d2P, SPr["line"])
    rM = []
    for b in range(4):
        v = SPr["boot"][:, 0] + SPr["boot"][:, 1] * (LST[b]["mean"] - PIV); rM.append(np.percentile(v, [16, 50, 84]).tolist())
    var["restricted overlap"] = dict(range_logMb=[float(lo), float(hi)], n_gal=int(len(gsel)), a=SPr["a"], b=SPr["b"], rms=float(SPr["rms"][SPr["ibest"]]),
                                     medU=float(SPr["medU"][SPr["ibest"]]), boot_sd=[math.sqrt(SPr["cov"][0, 0]), math.sqrt(SPr["cov"][1, 1])], boot_edge=SPr["edge"],
                                     n_sep_vs_kids_all=nr, n_sep_vs_kids_primary=nrp, lM200_at_bins_16_50_84=rM)
    P(f"  (reported) restricted overlap: lens log Mb 5-95 % {lo:.2f}-{hi:.2f}; {len(gsel)} SPARC galaxies; best a {SPr['a']:.2f} b {SPr['b']:.2f} rms {float(SPr['rms'][SPr['ibest']]):.4f} "
          f"U {float(SPr['medU'][SPr['ibest']]):.2f}; boot sd a {math.sqrt(SPr['cov'][0, 0]):.2f} b {math.sqrt(SPr['cov'][1, 1]):.2f} (edge {SPr['edge']:.2f}); n_sep vs KiDS all {nr if nr is None else round(nr, 2)}, "
          f"vs KiDS R<=0.31 {nrp if nrp is None else round(nrp, 2)}")
    P("     SPARC-subset log M200 at lens-bin masses (16/50/84): " + "; ".join(f"bin{b + 1} {rM[b][0]:.2f}/{rM[b][1]:.2f}/{rM[b][2]:.2f} vs KiDS {kM[b][1]:.2f}" for b in range(4)))
    fo["variants"] = var
    FT[foot] = fo
    del tw, ts, iu, sn, offg, twr, tsr, iur, snr, SP, SPr, WR2, WS, IU
    P(f"  [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")

check("K0_A1", K0A1, "A1 common shifts reproduced with the table (shift exact, chi2 within 0.2)")
for foot in FOOTS:
    P(f"  K0_X38_{foot}: {'PASS' if CHK[f'K0_X38_{foot}'] else 'FAIL'}")
rng1 = np.random.default_rng(55).integers(0, NG, NG); rng2 = np.random.default_rng(55).integers(0, NG, NG)
check("K_BOOT_seed_reproducible", np.array_equal(rng1, rng2), "default_rng(55) twice")
RES["footings"] = FT
STEP0 = all(CHK[k] for k in ("K0_X53", "K0_EM1", "K0_A1", "K0_X38_canonical", "K0_X38_alt"))
V = {f: FT[f]["cls"] for f in FOOTS}
if not STEP0:
    LANE = "UNDECIDED (step 0 failed)"
elif V["canonical"] == V["alt"]:
    LANE = V["canonical"]
else:
    LANE = f"UNDECIDED (footings disagree: {V})"
RES["verdict"] = LANE
P(f"\n=== VERDICT (both footings, frozen rule): {LANE}")
check("K_R_rss_below_1GB", rss() < 1.0, f"{rss():.2f} GB")
n = sum(CHK.values()); RES["checks"] = CHK
P(f"\nchecks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"x55_one_halo_results{SFX}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"x55_one_halo{SFX}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)
