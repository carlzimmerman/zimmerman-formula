"""CFG880 -- is the cold clump's velocity dispersion sigma_x UNIVERSAL across dwarfs, or does it vary intrinsically?
Criteria: FROZEN_CRITERIA.md (8c1d0b870, committed alone before this script).
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg880.py   (CFG880_MUTATE=scatter|null -> separate outputs named by mode).
kappa = 1/2 FITTED; nu_e; the two a0 footings are never pooled; not theory closed."""
import os, csv, json, math, numpy as np
from scipy.special import logsumexp
from scipy.stats import chi2
from scipy import fft as sfft

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG880_MUTATE", ""); assert MUT in ("", "scatter", "null"); SUF = f"_MUTATE_{MUT}" if MUT else ""; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, PC = 6.674e-11, 1.989e30, 3.0857e16; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; RC = 104.0
THR = 0.15; HBR = (7.36, 8.22)                      # class threshold on s_int; CFG878 hydrogen-cooling bracket (post-hoc label)
nu = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-15))))
def fnum(x):
    try:
        v = float(x); return None if math.isnan(v) else v
    except (TypeError, ValueError): return None
LVD = {}
for f in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", f))): LVD[r["name"]] = r
EXCL = {"LMC", "SMC", "WLM", "NGC 6822", "IC 1613", "Leo A", "Sagittarius dIrr", "Pegasus dIrr", "M 32"}
J = lambda *p: json.load(open(os.path.join(LANES, *p)))
R870 = J("CFG870_cored_component_joint", "cfg870_results.json"); R876 = J("CFG876_cold_floor_universality", "cfg876_results.json")
R877 = J("CFG877_finite_cold_clump", "cfg877_results.json"); R28 = J("CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")
R59 = J("CFG859_extra_speed_vs_ufds", "cfg859_results.json"); R24 = J("CFG824_dwarf_age_fossil", "cfg824_results.json")["rows"]
R27 = J("CFG827_dwarf_age_sfh_ml", "cfg827_results.json")["rows"]
SREF = {f: R870[f]["Vx"] / math.sqrt(2) for f in A0}     # CFG877's sigma_x = V_x/sqrt(2)

# ---------------- physics (CFG874 gas, CFG877 clump) ----------------
def gas_in(lHI, r12_pc):                                   # CFG874 primary (extended root), copied unchanged
    if lHI is None: return 0.0
    Mg = 1.33 * 10 ** lHI; MHI = 10 ** lHI; RHI = 0.5 * 10 ** (0.506 * lHI - 3.293) * 1e3
    f = lambda Rs: MHI / (2 * math.pi * Rs * Rs) * math.exp(-RHI / Rs) - 1.0
    grid = np.geomspace(1e-3 * RHI, 10 * RHI, 4000); v = [f(x) for x in grid]
    roots = [grid[i] for i in range(len(grid) - 1) if v[i] * v[i + 1] < 0]
    Rs = max(roots) if roots else RHI / 2; x = r12_pc / Rs
    return Mg * (1 - (1 + x) * math.exp(-x))
def law2(nm, a0, ups, gas=True):                           # sigma_law^2 (km/s)^2 and r12 (pc); Wolf, r12 = (4/3) r_h
    L = LVD[nm]; rh_pc = fnum(L.get("rhalf_sph_physical")) or fnum(L.get("rhalf_physical")); r12_pc = (4 / 3) * rh_pc; r12 = r12_pc * PC
    Ms = ups * 10 ** (0.4 * (4.83 - fnum(L["M_V"]))); Mg = gas_in(fnum(L.get("mass_HI")), r12_pc) if gas else 0.0
    gN = G * (Ms / 2 + Mg) * Msun / r12 ** 2
    return float(gN * nu(gN / a0)) * r12 / 3 / 1e6, r12_pc
def clump2(r12_pc, sx, a0, rc=RC):                         # G M_x(<r12)/(3 r12) in (km/s)^2; finite clump of CFG877
    r = r12_pc * PC; s = sx * 1e3
    Mx = np.minimum(2 * s ** 2 * r ** 3 / (G * (r ** 2 + (rc * PC) ** 2)), 81 * s ** 4 / (4 * G * a0))
    return G * Mx / (3 * r) / 1e6
def sig_pred(sl2, r12_pc, sx, a0, rc=RC): return np.sqrt(sl2 + clump2(r12_pc, sx, a0, rc))

# ---------------- sample ----------------
SAMP = []
for nm, r in LVD.items():
    if nm in EXCL: continue
    s = fnum(r.get("vlos_sigma"))
    if s is None or fnum(r.get("vlos_sigma_ul")) is not None: continue
    rh = fnum(r.get("rhalf_sph_physical")) or fnum(r.get("rhalf_physical"))
    if rh is None or fnum(r.get("M_V")) is None: continue
    em, ep = fnum(r.get("vlos_sigma_em")), fnum(r.get("vlos_sigma_ep")); assert em and ep, nm
    SAMP.append(dict(name=nm, host=r.get("host") or "field", MV=fnum(r["M_V"]), s=s, em=em, ep=ep))
def arrays(S, a0, ups=lambda nm: 2.0, gas=True):
    q = [law2(d["name"], a0, ups(d["name"]), gas) for d in S]
    return dict(names=[d["name"] for d in S], host=[d["host"] for d in S], MV=np.array([d["MV"] for d in S]),
                sl2=np.array([x[0] for x in q]), r12=np.array([x[1] for x in q]),
                s=np.array([d["s"] for d in S]), em=np.array([d["em"] for d in S]), ep=np.array([d["ep"] for d in S]))
def sub(A, keep):
    keep = np.asarray(keep, bool); return {k: ([x for x, kk in zip(v, keep) if kk] if isinstance(v, list) else v[keep]) for k, v in A.items()}

# ---------------- hierarchical likelihood ----------------
DU = 0.0025; U = np.arange(math.log(1e-3), math.log(3e3) + 1e-12, DU); NU = len(U)
M_IDX = np.where((U >= -1e-12) & (U <= math.log(50.0) + 1e-12))[0]; MG = U[M_IDX]
S_GRID = np.round(np.concatenate([[0.0], np.arange(0.005, 0.30001, 0.005), np.arange(0.32, 1.00001, 0.02), np.arange(1.05, 2.00001, 0.05)]), 6)
PAD = int(math.ceil(8 * S_GRID.max() / DU)) + 2; NFFT = sfft.next_fast_len(NU + 2 * PAD); FLOOR = 1e-10
LNFLOOR = math.log(FLOOR)
def loglike(A, a0, u, rc_link=None):                       # (N, len(u)); split normal, constant normalisation
    sx = np.exp(u)[None, :]; rc = RC if rc_link is None else RC * (sx / rc_link) ** 2
    sp = sig_pred(A["sl2"][:, None], A["r12"][:, None], sx, a0, rc)
    so = A["s"][:, None]; e = np.where(so < sp, A["ep"][:, None], A["em"][:, None])
    return -0.5 * ((so - sp) / e) ** 2 + np.log(math.sqrt(2 / math.pi) / (A["em"] + A["ep"]))[:, None]
def kernel(s):
    h = int(math.ceil(8 * s / DU)); kk = np.arange(-h, h + 1); lnK = -0.5 * (kk * DU / s) ** 2; return h, kk, lnK - logsumexp(lnK)
class Marg:
    """Per-dwarf likelihood on the u grid, edge-padded (below: law-only plateau; above: ~0), convolved with the normalised discrete
    Gaussian kernel by FFT; entries below FLOOR (FFT dynamic range) are flagged and evaluated directly in log space when needed."""
    def __init__(self, ll):
        self.mx = ll.max(1); self.g = ll - self.mx[:, None]
        self.gp = np.pad(self.g, ((0, 0), (PAD, PAD)), mode="edge"); self.Lf = sfft.rfft(np.exp(self.gp), NFFT, axis=1)
    def conv(self, s):
        if s == 0: return self.g[:, M_IDX].copy(), np.zeros((len(self.mx), len(M_IDX)), bool), None
        h, kk, lnK = kernel(s); K = np.zeros(NFFT); K[kk % NFFT] = np.exp(lnK)
        C = sfft.irfft(self.Lf * sfft.rfft(K), NFFT, axis=1)[:, PAD + M_IDX]; bad = C < FLOOR
        return np.log(np.where(bad, FLOOR, C)), bad, (h, lnK)
    def exact(self, i, m, hk):
        h, lnK = hk; c = PAD + M_IDX[m]; return float(logsumexp(self.gp[i, c - h:c + h + 1] + lnK[::-1]))
def interval(x, d, thr):                                   # contiguous region around the minimum of d = -2 Delta lnL
    i0 = int(np.argmin(d)); j = i0
    while j + 1 < len(x) and d[j + 1] <= thr: j += 1
    hi = math.inf if j + 1 == len(x) else x[j] + (thr - d[j]) * (x[j + 1] - x[j]) / (d[j + 1] - d[j])
    j = i0
    while j - 1 >= 0 and d[j - 1] <= thr: j -= 1
    lo = x[0] if j == 0 else x[j] - (thr - d[j]) * (x[j] - x[j - 1]) / (d[j - 1] - d[j])
    return [float(lo), float(hi)], (j == 0)
def classify(ul95, ll95): return "UNIVERSAL" if ul95 <= THR else ("NOT UNIVERSAL" if ll95 > THR else "UNDECIDED")
def fit(A, a0, rc_link=None, per_dwarf=False):
    ll = loglike(A, a0, U, rc_link); Mg = Marg(ll); NS, NM = len(S_GRID), len(M_IDX)
    Traw = np.empty((NS, NM)); store = []
    for k, s in enumerate(S_GRID):
        lnC, bad, hk = Mg.conv(s); Traw[k] = lnC.sum(0) + Mg.mx.sum(); store.append((bad, hk))
    def exact_T(k, m):
        bad, hk = store[k]; idx = np.where(bad[:, m])[0]
        return Traw[k, m] if len(idx) == 0 else Traw[k, m] - len(idx) * LNFLOOR + sum(Mg.exact(i, m, hk) for i in idx)
    T = Traw.copy(); k0, m0 = np.unravel_index(np.argmax(Traw), Traw.shape); E0 = exact_T(k0, m0); nref = 0
    for k, m in np.argwhere(Traw >= E0 - 10.0):            # exact values wherever the upper bound could reach within 10 of the max
        if store[k][0][:, m].any(): T[k, m] = exact_T(k, m); nref += 1
    ps, pm = T.max(1), T.max(0); kh, mh = np.unravel_index(np.argmax(T), T.shape); Lmax = float(T[kh, mh])
    ds, dm, d0 = 2 * (Lmax - ps), 2 * (Lmax - pm), 2 * (T[0].max() - T[0])
    s68, _ = interval(S_GRID, ds, 1.0); s95, _ = interval(S_GRID, ds, 3.84)
    m68, e1 = interval(MG, dm, 1.0); m95, e2 = interval(MG, dm, 3.84); u68, e3 = interval(MG, d0, 1.0); u95, e4 = interval(MG, d0, 3.84)
    Lam = float(ds[0]); p = 1.0 if Lam < 1e-9 else float(0.5 * chi2.sf(Lam, 1))
    sbar_u = float(math.exp(MG[int(np.argmax(T[0]))]))
    R = dict(N=len(A["s"]), s_hat=float(S_GRID[kh]), s68=s68, s95=s95, sbar_hat=float(math.exp(MG[mh])),
             sbar68=[math.exp(x) for x in m68], sbar95=[math.exp(x) for x in m95], sbar_univ=sbar_u,
             sbar_univ68=[math.exp(x) for x in u68], sbar_univ95=[math.exp(x) for x in u95], Lambda=Lam, p_scatter=p,
             lnLmax=Lmax, n_refined=nref, m_edge=bool(e2 or e4), cls=classify(s95[1], s95[0]))
    R["hbr_hier"] = overlap(R["sbar95"]); R["hbr_univ"] = overlap(R["sbar_univ95"]); R["ul95_le_0055"] = bool(s95[1] <= 0.055)
    if per_dwarf:
        rows = []; spu = sig_pred(A["sl2"], A["r12"], sbar_u, a0)
        for i in range(len(A["s"])):
            li = ll[i]; j = int(np.argmax(li)); (lo, hi), at_edge = interval(U, 2 * (li[j] - li), 3.84)
            z = (A["s"][i] - spu[i]) / (A["ep"][i] if A["s"][i] < spu[i] else A["em"][i])
            rows.append(dict(name=A["names"][i], host=A["host"][i], MV=float(A["MV"][i]), r12=float(A["r12"][i]), sigma=float(A["s"][i]),
                             em=float(A["em"][i]), ep=float(A["ep"][i]), law=float(math.sqrt(A["sl2"][i])), pred_univ=float(spu[i]), z_univ=float(z),
                             sx_mle=float(math.exp(U[j])) if j > 0 else 0.0, sx95=[0.0 if at_edge else math.exp(lo), math.exp(hi)], sx_ul=bool(at_edge)))
        R["rows"] = rows
        R["n_excl_low"] = sum(r["sx95"][1] < sbar_u for r in rows); R["n_excl_high"] = sum(r["sx95"][0] > sbar_u for r in rows)
    return R
def overlap(iv): return "OVERLAPS" if iv[1] >= HBR[0] and iv[0] <= HBR[1] else ("BELOW" if iv[1] < HBR[0] else "ABOVE")
def synth(A, a0, sref, rng, s_true):                       # sigma_obs = sigma_pred(sigma_x,i) + split-normal noise (neg side e_p, pos side e_m)
    n = len(A["s"]); z = rng.standard_normal(n); sx = sref * np.exp(s_true * z); sp = sig_pred(A["sl2"], A["r12"], sx, a0)
    neg = rng.random(n) < A["ep"] / (A["em"] + A["ep"]); a = np.abs(rng.standard_normal(n))
    B = dict(A); B["s"] = np.maximum(np.where(neg, sp - a * A["ep"], sp + a * A["em"]), 0.1); return B
def fmt(R):
    ul = "> 2.0" if math.isinf(R["s95"][1]) else f"{R['s95'][1]:.3f}"
    return (f"N {R['N']:2d}  s_int^ {R['s_hat']:.3f} [68% {R['s68'][0]:.3f}-{R['s68'][1]:.3f}; 95% {R['s95'][0]:.3f}-{ul}]  "
            f"sigma_bar^ {R['sbar_hat']:.2f} [95% {R['sbar95'][0]:.2f}-{R['sbar95'][1]:.2f}]  univ {R['sbar_univ']:.2f} "
            f"[95% {R['sbar_univ95'][0]:.2f}-{R['sbar_univ95'][1]:.2f}]  Lambda {R['Lambda']:.2f} (p {R['p_scatter']:.2g})  -> {R['cls']}")

# ---------------- run ----------------
P("CFG880  is the cold clump's sigma_x universal?  hierarchical ln sigma_x,i = ln sigma_bar + delta_i, delta ~ N(0, s_int^2)"
  + (f"  [MUTATE {MUT}: synthetic data, s_int = {0.4 if MUT == 'scatter' else 0.0}]" if MUT else ""))
P(f"  sample N = {len(SAMP)} (LVD MW + M31 + local field; measured sigma; rotating set excluded); r_c = {RC} pc; Ups_V 2 + gas (primary)")
RES = dict(lane="CFG880", mutate=MUT or None, N=len(SAMP), thr=THR, hbracket=HBR, s_grid_max=float(S_GRID.max()))

# ---- POST-HOC diagnostic (added AFTER the pre-registered run; not graded): how large an unmodelled per-dwarf systematic in sigma
# (added in quadrature to both error sides, as in V5) would make the data compatible with a universal sigma_x (LL95 <= 0.15)?
POST = os.environ.get("CFG880_POSTHOC", ""); assert POST in ("", "floor") and not (POST and MUT)
if POST:
    P("  POST-HOC systematic-floor scan (added after the pre-registered run; not graded)"); PR = dict(lane="CFG880", posthoc="floor")
    for foot in A0:
        a0 = A0[foot]; A = arrays(SAMP, a0); PR[foot] = {}
        for fl in (0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40):
            AF = dict(A); AF["em"] = np.sqrt(A["em"] ** 2 + (fl * A["s"]) ** 2); AF["ep"] = np.sqrt(A["ep"] ** 2 + (fl * A["s"]) ** 2)
            RF = fit(AF, a0); PR[foot][f"{fl:.2f}"] = RF; P(f"  [{foot}] floor {fl:.2f}: {fmt(RF)}")
    json.dump(PR, open(os.path.join(HERE, "cfg880_results_POSTHOC_floor.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "cfg880_POSTHOC_floor.out"), "w").write("\n".join(OUT) + "\n"); raise SystemExit(0)

if not MUT:
    K1 = {}
    for foot in A0:                                         # K1: CFG877's five group means at s_int = 0, sigma_bar = V_x/sqrt(2)
        a0 = A0[foot]; sx = SREF[foot]; rows = R28[f"{foot}|nu_e"]["rows"]; host = lambda nm: LVD[nm].get("host") or "field"
        grp = {"MW classical (calib)": [(r["name"], R24[r["name"]]["so"], R27[r["name"]]["ups"], False) for r in rows if host(r["name"]) == "mw" and r["delta"] > 0.05],
               "M31 + field (T2)": [(r["name"], R24[r["name"]]["so"], R27[r["name"]]["ups"], False) for r in rows if host(r["name"]) in ("m_031", "field")],
               "UFDs (T3)": [(nm, fnum(LVD[nm]["vlos_sigma"]), 2.20, False) for nm in R59[f"{foot}|secondary (literature sigma)"]["names"]],
               "large out-of-sample": [(x["name"], fnum(LVD[x["name"]]["vlos_sigma"]), 2.0, True) for x in R876[foot]["primary B"]["rows"]],
               "small out-of-sample": [(x["name"], fnum(LVD[x["name"]]["vlos_sigma"]), 2.0, True) for x in R876[foot]["small (r12<312)"]["rows"]]}
        for k, its in grp.items():
            E = float(np.mean([math.log(so / float(sig_pred(*law2(nm, a0, ups, gas), sx, a0))) for nm, so, ups, gas in its]))
            K1[f"{foot}|{k}"] = abs(E - R877[foot]["groups"][k]["E"])
    k1 = max(K1.values()); RES["K1"] = dict(diffs=K1, max=k1, ok=k1 < 1e-9)
    P(f"  K1 (CFG877 five group means, both footings, s_int 0, sigma_bar = V_x/sqrt2): max |diff| {k1:.1e} -> {'PASS' if k1 < 1e-9 else 'FAIL'}")
    A = arrays(SAMP, A0["canonical"]); ll = loglike(A, A0["canonical"], U); Mg = Marg(ll); s = 0.3
    m = int(np.argmin(abs(MG - math.log(SREF["canonical"])))); lnC, bad, hk = Mg.conv(s); col = lnC[:, m].copy()
    for i in np.where(bad[:, m])[0]: col[i] = Mg.exact(i, m, hk)
    mine = col + Mg.mx; t = np.linspace(-10, 10, 40001); w = np.full(t.size, t[1] - t[0]); w[[0, -1]] *= 0.5
    brute = logsumexp(loglike(A, A0["canonical"], MG[m] + s * t) - 0.5 * t ** 2 - 0.5 * math.log(2 * math.pi) + np.log(w)[None, :], axis=1)
    k2 = float(np.max(np.abs(mine - brute))); RES["K2"] = dict(max_abs_dlnL=k2, ok=k2 < 1e-3, n_fft_floor=int(bad[:, m].sum()))
    P(f"  K2 (s_int 0.3, sigma_bar {math.exp(MG[m]):.3f}: FFT/direct marginal vs fine quadrature, {len(mine)} dwarfs): max |d lnL| {k2:.1e} -> {'PASS' if k2 < 1e-3 else 'FAIL'}")

CL = {}
for foot in A0:
    a0 = A0[foot]; sref = SREF[foot]; A = arrays(SAMP, a0); F = RES.setdefault(foot, dict(sref=sref))
    if MUT:
        A = synth(A, a0, sref, np.random.default_rng(880), 0.4 if MUT == "scatter" else 0.0)
    R = fit(A, a0, per_dwarf=not MUT); F["primary"] = R; CL[foot] = R["cls"]
    P(f"\n  [{foot}] sigma_ref = V_x/sqrt2 = {sref:.4f} km/s;  PRIMARY  {fmt(R)}")
    P(f"     H-cooling bracket {HBR} (post-hoc): hierarchical {R['hbr_hier']}, universal fit {R['hbr_univ']};  UL95 <= 0.055: {R['ul95_le_0055']};"
      f"  refined cells {R['n_refined']}" + ("  [sigma_bar interval hits the grid edge]" if R["m_edge"] else ""))
    if MUT: continue
    P(f"     dwarfs whose own 95% sigma_x range excludes the universal {R['sbar_univ']:.2f}: {R['n_excl_low']} below, {R['n_excl_high']} above")
    for r in sorted(R["rows"], key=lambda q: q["z_univ"]):
        P(f"       {r['name']:18s} {r['host']:6s} M_V {r['MV']:6.1f} r12 {r['r12']:6.0f}  sigma {r['sigma']:5.2f} +{r['ep']:.2f}/-{r['em']:.2f}  law {r['law']:5.2f}"
          f"  pred {r['pred_univ']:5.2f}  z {r['z_univ']:+5.1f}  own sigma_x " + (f"< {r['sx95'][1]:6.2f}" if r["sx_ul"] else f"{r['sx_mle']:6.2f} [{r['sx95'][0]:5.2f}-{r['sx95'][1]:6.2f}]"))
    # ---- variants (reported; V3 and V5 feed the qualifiers)
    zlaw = np.array([(d - math.sqrt(l2)) / ep if d < math.sqrt(l2) else 0.0 for d, l2, ep in zip(A["s"], A["sl2"], A["ep"])])
    V3names = [n for n, z in zip(A["names"], zlaw) if z <= -2]
    AP = {}
    for l in open(os.path.join(REPO, "real_research", "data", "arroyopolonio2026_ufd_binary_corrected.tsv")):
        if l.startswith("#") or l.startswith("name"): continue
        v = l.rstrip("\n").split("\t"); AP[v[0]] = (float(v[11]), float(v[12]), float(v[14]))      # sig_f, +1sigma, -1sigma
    APMAP = {"Boo I": "Bootes I", "Car II": "Carina II", "Cra II": "Crater II", "Hyd I": "Hydrus I", "Leo IV": "Leo IV", "Leo V": "Leo V",
             "Ret II": "Reticulum II", "Sag II": "Sagittarius II", "Seg 1": "Segue 1", "Uni 1": "Unions 1", "Wil 1": "Willman 1"}
    A4 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in A.items()}; V4names = []
    for k, nm in APMAP.items():
        if nm in A4["names"]:
            i = A4["names"].index(nm); A4["s"][i], A4["ep"][i], A4["em"][i] = AP[k]; V4names.append(nm)
    A5 = dict(A); A5["em"] = np.sqrt(A["em"] ** 2 + (0.1 * A["s"]) ** 2); A5["ep"] = np.sqrt(A["ep"] ** 2 + (0.1 * A["s"]) ** 2)
    VAR = [("V1 Ups_SFH (CFG827 where available)", arrays(SAMP, a0, ups=lambda nm: R27[nm]["ups"] if nm in R27 else 2.0), None),
           ("V2 M_V <= -6", sub(A, A["MV"] <= -6), None),
           ("V3 law-over-predicted removed (z_law <= -2)", sub(A, zlaw > -2), None),
           ("V4 binary-corrected sigma (Arroyo-Polonio flat f)", A4, None),
           ("V5 10% systematic floor", A5, None),
           ("V6 law-linked core r_c ~ sigma_x^2", A, sref)]
    F["V3_removed"] = V3names; F["V4_replaced"] = V4names; F["V1_n_sfh"] = sum(d["name"] in R27 for d in SAMP); F["variants"] = {}
    P(f"\n     variants  (V3 removes: {', '.join(V3names) or 'none'};  V4 replaces: {', '.join(V4names)};  V1 Ups_SFH for {F['V1_n_sfh']} dwarfs)")
    for lab, AV, rl in VAR:
        RV = fit(AV, a0, rc_link=rl); F["variants"][lab] = RV; P(f"     {lab:50s} {fmt(RV)}")
    # ---- power pre-flight
    ULs = []
    for sd in range(8800, 8816):
        ULs.append(fit(synth(A, a0, sref, np.random.default_rng(sd), 0.0), a0)["s95"][1])
    ULa = np.array(ULs); F["power"] = dict(UL95=[float(x) for x in ULa], median=float(np.median(ULa)), p84=float(np.percentile(ULa, 84)),
                                          frac_le_thr=float(np.mean(ULa <= THR)))
    P(f"     power pre-flight (16 nulls, s_int = 0): UL95 median {F['power']['median']:.3f}, 84th pct {F['power']['p84']:.3f}, "
      f"fraction <= {THR}: {F['power']['frac_le_thr']:.2f}" + ("  -> UNIVERSAL out of reach with present errors" if F["power"]["median"] > THR else ""))

cc, ca = CL["canonical"], CL["alt"]; overall = cc if cc == ca else f"UNDECIDED (footings disagree: canonical {cc}, alt {ca})"
if not MUT:
    q = []
    v3 = RES["canonical"]["variants"]["V3 law-over-predicted removed (z_law <= -2)"]["cls"]
    if v3 != cc: q.append(f"rests on the law-over-predicted dwarfs: {', '.join(RES['canonical']['V3_removed'])}")
    if overall == "NOT UNIVERSAL" and RES["canonical"]["variants"]["V5 10% systematic floor"]["cls"] != "NOT UNIVERSAL": q.append("not robust to a 10% systematic")
    overall += "".join(f" ({x})" for x in q)
P(f"\n  CLASS: {overall}")
if MUT:
    ok = (cc == "NOT UNIVERSAL" and ca == "NOT UNIVERSAL") if MUT == "scatter" else (cc != "NOT UNIVERSAL" and ca != "NOT UNIVERSAL")
    RES["mutate_ok"] = ok; P(f"  MUTATE-{MUT}: {'control behaves as required' if ok else 'CONTROL FAILED'}")
RES["cls"] = overall
json.dump(RES, open(os.path.join(HERE, f"cfg880_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg880{SUF}.out"), "w").write("\n".join(OUT) + "\n")
