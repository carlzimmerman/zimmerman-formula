#!/usr/bin/env python3
"""
agentBB -- THE LEGAL-MIXTURE ESCAPE TEST (agentV section 5.2 pre-registered NNLS follow-up).
Question: can a LEGAL (dS Kallen-Lehmann-POSITIVE) spectral mixture with the one allowed tuning
(conformal balance: int (x-2) drho = 0, x = M^2/H^2 -- kills the leading (a0/a)-level lightcone term)
produce an effective mu(a) on the Deser-Levin family that fits the REAL 175-galaxy SPARC RAR at the
survival line (within ~0.01 dex of the McGaugh baseline 0.1950 fw / 0.1977 canon, locked conventions
of mi_f4_sparc_shape_test.py), while clearing the banked solar budgets (agentE reflex line
delta_a_sun <= 2.47e-15 strict / 3.38e-15 loose; Folkner Cassini Saturn radial <= 1e-14)?

Machinery (all banked):
  atom kernel (agentN1 closed form, T-hat normalization of agentV section 1.1):
      K_x(u) = (x-2) * 2F1(3/2+nu, 3/2-nu; 2; -u/2),  nu = sqrt(9/4 - x)   [units H=1, 1/(16pi) absorbed]
  response (agentV [V-A4], probability-measure form):
      E_t[K] = int_0^inf K(u) dnu_t(u),  dnu_t = (t/2) u^(-1/2) (u+t)^(-3/2) du,  t = 2H^2/kappa^2
  effective MI law on stationary worldlines:
      mu_mix(x_acc) = 1 - (1/sqrt(1+alpha^2)) * sum_j c_j E_t(alpha)[K_xj],  alpha = eta*x_acc,
      t(alpha) = 2/(1+alpha^2), eta = a0/(c H_Lambda); c_j >= 0 (KL positivity), amplitude absorbed in c.
  legal tuning: sum_j c_j (x_j - 2) = 0  (the J=0 conformal balance; J=1 too would collapse the measure
      to the zero-tail conformal point -- agentV [X2] theorem -- so it is NOT imposed; its forced nonzero
      value is the residual solar tail we then measure).
  rotation curves (modified inertia, exact): mu(g_obs/a0) g_obs = g_bar  =>  nu_mix(y) by numeric inversion.
Scoring: the LOCKED SPARC conventions (mi_f4_sparc_shape_test.py): 175 galaxies, residual
  log10(g_obs) - log10(nu(g_bar/a0) g_bar), per-function best-Upsilon on the 0.3-1.2 (46) grid,
  UNWEIGHTED dex scatter primary + error-weighted secondary, both a0 footings.
Pre-registered verdict lines (task): ESCAPE-LIVES if best legal mixture <= baseline+0.0100 dex (own footing)
  AND passes both solar budgets; ESCAPE-CLOSED if no legal mixture within 0.0200 dex at either footing OR all
  SPARC-fitting mixtures violate solar budgets; else PARTIAL. Both-ways per the working rule: the mixture
  gets per-variant best-Upsilon, both footings, a signed (illegal) control to separate positivity-cost from
  basis-cost, and an SLSQP polish DIRECTLY on the locked objective so the NNLS surrogate cannot manufacture
  a kill. 2026-06-11. No git.
"""
import numpy as np, glob, os, time
import mpmath as mp
from scipy.optimize import nnls, minimize

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "agentBB_legal_mixture.out")
_f = open(OUT, "w")
T0 = time.time()
def P(s=""):
    _f.write(str(s) + "\n"); _f.flush(); print(s, flush=True)

LINE = "=" * 100
P(LINE)
P("agentBB LEGAL-MIXTURE ESCAPE TEST -- run date 2026-06-11")
P("the one escape agentV section 5.2 left open: conformal-balanced positive KL mixture vs the real SPARC RAR")
P(LINE)

# ---------------------------------------------------------------- [0] constants & conventions
cc  = 2.99792458e8
HL  = 1.81e-18                      # H_Lambda [s^-1] (agentV [F] convention; cH_L = 5.426e-10)
A0  = {"fw": 9.36e-11, "canon": 1.2e-10}
ETA = {k: v/(cc*HL) for k, v in A0.items()}
BASE = {"fw": 0.1950, "canon": 0.1977}          # locked McGaugh baselines (mi_f4_sparc_shape_test.out)
F4   = {"fw": 0.1984, "canon": 0.1980}
# banked solar budgets
A_SUN = 2.09e-7                      # agentE integrated mean |a_sun| (Jupiter line 2.0908e-7)
BUD_SUN_STRICT, BUD_SUN_LOOSE = 2.47e-15, 3.38e-15
G_SAT = 1.32712440018e20/(9.53707*1.495978707e11)**2
BUD_SAT = 1.0e-14                    # Folkner Cassini radiometric, anomalous radial accel at Saturn
P(f"[0] eta = a0/cH_L: fw {ETA['fw']:.5f} ; canon {ETA['canon']:.5f}   (agentV [F]: 0.17250 / 0.22115)")
P(f"[0] solar lines: x_sun = 2.09e-7/a0 -> fw {A_SUN/A0['fw']:.0f}, canon {A_SUN/A0['canon']:.0f} ;"
  f" g_Sat = {G_SAT:.3e} -> x_Sat fw {G_SAT/A0['fw']:.3e}, canon {G_SAT/A0['canon']:.3e}")
P(f"[0] budgets: delta_a_sun <= {BUD_SUN_STRICT:.2e} strict / {BUD_SUN_LOOSE:.2e} loose ;"
  f" delta_a_Saturn <= {BUD_SAT:.0e}")

# ---------------------------------------------------------------- [1] kernel machinery
P("\n" + LINE); P("[1] ATOM KERNELS K_x(u) = (x-2) 2F1(3/2+nu,3/2-nu;2;-u/2) on the master u-grid"); P(LINE)
mp.mp.dps = 20

# master log-u grid: Gauss-Legendre per decade, u in [1e-16, 1e8]
NPD = 24
glx, glw = np.polynomial.legendre.leggauss(NPD)
_nodes, _wts = [], []
for d in range(-16, 8):
    l0, l1 = d*np.log(10.0), (d+1)*np.log(10.0)
    lam = 0.5*(l1-l0)*glx + 0.5*(l1+l0)
    _nodes.append(np.exp(lam)); _wts.append(0.5*(l1-l0)*glw*np.exp(lam))   # du-weights
UN = np.concatenate(_nodes); UW = np.concatenate(_wts)
UWS = UW/np.sqrt(UN)                                                       # premultiplied u^-1/2 du
P(f"    grid: {len(UN)} nodes, {NPD}/decade, u in [1e-16, 1e8]")

def wvec(t):
    """probability-measure weights: E_t[K] = wvec(t) . K(UN);  sum = 1 - truncation."""
    return 0.5*t*UWS*(UN + t)**-1.5

for t in [2.0, 0.5, 6.7e-2, 1e-5, 1.4e-10]:
    P(f"    [norm] t={t:9.2e}: sum w = {wvec(t).sum():.10f}  (exact 1; deficit = grid truncation)")

# atom x-grid (agentV LP band [0.05, 40] + boundary pair at 2 +- 0.01 + heavy tail to 200;
# heavy cap set by u-grid resolution: principal-series phase rate mu-hat = sqrt(x-9/4) per ln u,
# 24 GL nodes/decade = 10.4/ln-unit -> x = 200 (mu-hat 14.1) has ~4.6 nodes/period: validated below)
XATOMS = np.array([0.05, 0.08, 0.12, 0.17, 0.24, 0.33, 0.45, 0.60, 0.78, 1.00, 1.25, 1.50, 1.72,
                   1.90, 1.95, 1.99, 2.01, 2.05, 2.10, 2.25, 2.45, 2.70, 3.00, 3.40, 3.90, 4.50,
                   5.20, 6.00, 7.00, 8.20, 9.60, 11.3, 13.2, 15.5, 18.2, 21.3, 25.0, 29.3, 34.4,
                   40.3, 47.3, 55.4, 70.0, 85.0, 105.0, 130.0, 160.0, 200.0])
NA = len(XATOMS)
P(f"    atoms: {NA} masses x = M^2/H^2 in [{XATOMS[0]}, {XATOMS[-1]}] "
  f"(principal series above 2.25; boundary pairs near 2)")

CACHE = os.path.join(HERE, "agentBB_kernel_cache.npz")
def kernel_row(x):
    nu = mp.sqrt(mp.mpc(2.25 - x))
    hp, hm = mp.mpf(1.5) + nu, mp.mpf(1.5) - nu
    row = np.empty(len(UN)); im_max = 0.0
    for i, u in enumerate(UN):
        v = mp.hyp2f1(hp, hm, 2, -u/2.0)
        row[i] = float(mp.re(v))
        im_max = max(im_max, abs(float(mp.im(v))))
    return (x - 2.0)*row, im_max

if os.path.exists(CACHE):
    z = np.load(CACHE)
    if z["xatoms"].shape == XATOMS.shape and np.allclose(z["xatoms"], XATOMS) and z["un"].shape == UN.shape:
        TK = z["TK"]; P("    kernel cache HIT (delete agentBB_kernel_cache.npz to rebuild)")
    else:
        TK = None
else:
    TK = None
if TK is None:
    t_b = time.time(); _ = kernel_row(XATOMS[-1])
    P(f"    benchmark: heaviest atom row ({len(UN)} hyp2f1) in {time.time()-t_b:.1f}s -> "
      f"~{(time.time()-t_b)*NA/60:.1f} min total")
    TK = np.empty((NA, len(UN)))
    for j, x in enumerate(XATOMS):
        TK[j], imx = kernel_row(x)
        P(f"    atom {j+1:2d}/{NA} x={x:6.2f} built ({time.time()-T0:.0f}s, max|Im|={imx:.1e})")
    np.savez(CACHE, TK=TK, xatoms=XATOMS, un=UN)
assert np.isfinite(TK).all()

# sanity battery
P("\n    [sanity] endpoints and anchors:")
P(f"      K_x(u->0) vs (x-2): " + ", ".join(f"x={x:.2f}: {TK[j,0]:+.4f}/{x-2:+.4f}"
  for j, x in [(0, 0.05), (14, 1.99), (20, 3.00), (40, 60.0)]))
# MMC anchor: x -> 0 constant tail (N1: 2F1(3,0;2;y) == 1); use a direct tiny-x row at 3 u points
nu0 = mp.sqrt(mp.mpc(2.25 - 1e-8))
for u_ in [1e-6, 1.0, 1e6]:
    v = float(mp.re(mp.hyp2f1(mp.mpf(1.5)+nu0, mp.mpf(1.5)-nu0, 2, -u_/2)))
    P(f"      MMC anchor x=1e-8: 2F1 at u={u_:.0e}: {v:.6f} (must be ~1: constant tail)")
# resolution check: grid dot vs direct adaptive quadrature (v-substitution u = t v)
def E_direct(x, t):
    nu = mp.sqrt(mp.mpc(2.25 - x)); hp, hm = mp.mpf(1.5)+nu, mp.mpf(1.5)-nu
    f = lambda v: mp.re(mp.hyp2f1(hp, hm, 2, -(t*v)/2.0))*(x-2.0)*v**mp.mpf('-0.5')*(1.0+v)**mp.mpf('-1.5')/2.0
    pans = [0, 1, 10, 100, 1e4, 1e6, 1e8]
    return float(mp.quad(f, pans))
P("    [resolution] grid-dot vs direct mp.quad (rel diff):")
for x_, t_ in [(60.0, 2.0), (200.0, 2.0), (200.0, 6.7e-2), (0.05, 2.0), (0.05, 1e-5), (8.2, 0.5)]:
    j = int(np.argmin(np.abs(XATOMS - x_)))
    Eg = float(wvec(t_) @ TK[j]); Ed = E_direct(XATOMS[j], t_)
    P(f"      x={XATOMS[j]:5.2f} t={t_:8.2e}: grid {Eg:+.8e}  direct {Ed:+.8e}  rel {abs((Eg-Ed)/Ed):.2e}")
# deep-MOND analyticity echo (agentV [D]) on a mid atom
j8 = int(np.argmin(np.abs(XATOMS - 8.2)))
E2 = float(wvec(2.0) @ TK[j8]); Ds = []
for e in [1e-1, 1e-2, 1e-3, 1e-4]:
    Ds.append(float(wvec(2.0 - e) @ TK[j8]) - E2)
sl = [np.log(abs(Ds[i+1]/Ds[i]))/np.log(0.1) for i in range(3)]
P(f"    [analyticity echo] x=8.2 atom: slopes of E(2-eps)-E(2): {', '.join(f'{s:.4f}' for s in sl)} "
  f"(agentV [D]: -> 1.0000; target law would need 0.25)")

# ---------------------------------------------------------------- [2] response surfaces
P("\n" + LINE); P("[2] RESPONSE SURFACES Psi_j(x_acc) = E_t[K_j]/sqrt(1+alpha^2), alpha = eta x_acc"); P(LINE)
XGRID = np.logspace(-8, 6, 2800)     # acceleration grid in units of a0 (per footing via eta)

def build_PSI(xacc, eta):
    al = eta*np.asarray(xacc, dtype=float)
    t = 2.0/(1.0 + al*al)
    W = 0.5*t[:, None]*UWS[None, :]*(UN[None, :] + t[:, None])**-1.5     # [nx, nu]
    return (TK @ W.T)/np.sqrt(1.0 + al*al)[None, :]                       # [NA, nx]

PSIX = {k: build_PSI(XGRID, ETA[k]) for k in ("fw", "canon")}
P(f"    PSI built on {len(XGRID)} x_acc nodes (1e-8..1e6, both footings) ({time.time()-T0:.0f}s)")

def mu_rar(x):  return -np.expm1(-np.sqrt(x))
# THE FIT TARGET: the mu(x) whose exact MI inversion reproduces the McGaugh nu function
# nu_rar(y) = 1/(1-exp(-sqrt(y))) -- the survival-line FUNCTION (0.1950 dex fw). NOTE the duality gap:
# the exact MI inversion of mu_rar(x) = 1-e^{-sqrt(x)} is a DIFFERENT nu that scores 0.2189 fw ([REG]);
# matching THAT would already be past the closed line, so we target nu_rar's implied mu instead:
#   x(y) = y * nu_rar(y)  (g_obs pairing with g_bar on the McGaugh relation),  mu_target(x) = y/x.
_yt = np.logspace(-9, 9, 6000)
_nut = 1.0/(-np.expm1(-np.sqrt(_yt)))
_xt = _yt*_nut
_lyt, _lxt = np.log10(_yt), np.log10(_xt)
_dlx_dly = np.gradient(_lxt, _lyt)
def mu_target(x):
    lx = np.log10(x)
    return 10**(np.interp(lx, _lxt, _lyt) - lx)
def L_target(x):   # d ln(mu x)/d ln x = d ln y/d ln x along the target relation
    return 1.0/np.interp(np.log10(x), _lxt, _dlx_dly)

# ---------------------------------------------------------------- [3] SPARC: locked pipeline + regression
P("\n" + LINE); P("[3] SPARC -- locked conventions (mi_f4_sparc_shape_test.py); regression gate first"); P(LINE)
kpc = 3.0857e19
DATA = os.path.join(HERE, "..", "..", "data", "sparc_data")
gA_l, gD_l, gB_l, go_l, fr_l = [], [], [], [], []
ngal = 0
for fn in sorted(glob.glob(os.path.join(DATA, "*_rotmod.dat"))):
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6: continue
    R, Vobs, eV, Vgas, Vdisk, Vbul = (d[:, i] for i in range(6))
    Rm = R*kpc; ngal += 1
    gA_l.append(np.sign(Vgas)*Vgas**2*1e6/Rm); gD_l.append(Vdisk**2*1e6/Rm); gB_l.append(1.4*Vbul**2*1e6/Rm)
    go_l.append((Vobs*1e3)**2/Rm); fr_l.append(np.clip(eV, 1, None)/np.clip(Vobs, 1, None))
GA, GD, GB = map(np.concatenate, (gA_l, gD_l, gB_l))
GO, FR = np.concatenate(go_l), np.concatenate(fr_l)
WTS = 1.0/FR**2
OKB = np.isfinite(GO) & (GO > 0) & np.isfinite(GA) & np.isfinite(GD) & np.isfinite(GB)
P(f"    SPARC galaxies loaded: {ngal} ; points: {len(GO)}")
UDS = np.linspace(0.3, 1.2, 46)

def scatter_nu(nufn, Ud, a0):
    gb = GA + Ud*GD + Ud*GB                      # GB already carries the 1.4 bulge factor
    ok = OKB & (gb > 0) & np.isfinite(gb)
    r = np.log10(GO[ok]) - np.log10(nufn(gb[ok]/a0)*gb[ok])
    w = WTS[ok]
    return float(np.sqrt(np.mean(r**2))), float(np.sqrt(np.sum(w*r**2)/np.sum(w)))

def best_ud(nufn, a0, grid=None):
    g = UDS if grid is None else grid
    s = [scatter_nu(nufn, U, a0) for U in g]
    i = int(np.argmin([v[0] for v in s]))
    return g[i], s[i][0], s[i][1]

def nu_fw(y):     return np.sqrt(1 + 1/y)
def nu_rar(y):    return 1.0/(1.0 - np.exp(-np.sqrt(y)))
def nu_simple(y): return 0.5 + np.sqrt(0.25 + 1/y)
def nu_std(y):    return np.sqrt((y + np.sqrt(y*y + 4))/(2*y))
# exact MI inversion of mu_rar (the duality-gap reference: mu_rar(x) x = y)
_xg = np.logspace(-8, 8, 4000); _Yg = mu_rar(_xg)*_xg
def nu_rar_mi(y):
    lx = np.interp(np.log10(y), np.log10(_Yg), np.log10(_xg))
    return 10**(lx - np.log10(y))

P("    [REG] regression vs locked .out (must reproduce 0.1969/0.1950/0.1951/0.1984 fw etc.):")
for foot in ("fw", "canon"):
    a0 = A0[foot]
    P(f"      a0 = {foot} {a0:.2e}:")
    for lab, fn in [("fw sqrt(1+1/y)", nu_fw), ("McGaugh RAR", nu_rar), ("simple", nu_simple),
                    ("F4 standard", nu_std), ("McGaugh-MI (exact inv)", nu_rar_mi)]:
        U, su, sw = best_ud(fn, a0)
        P(f"        {lab:24s} Ud={U:5.2f}  unw {su:.4f}  wt {sw:.4f}")

# ---------------------------------------------------------------- [4] mixture machinery (sign-aware)
# THE SIGN FLAG (agentV section 5.2 registry item iv / N2 [C4]): the absolute deficit-channel sign is OPEN
# in the repo (Quinn-anchored: heavy side M^2>2H^2 = deficit; the Link-5 chain line says the opposite).
# The legal family therefore gets BOTH overall response signs -- mu = 1 - sign * sum_j c_j Psi_j -- and the
# verdict uses whichever sign serves the escape best (working-rule fairness; the sign flip is exactly the
# unresolved convention).
SIGNS = {+1: "Quinn-anchored (heavy=deficit)", -1: "chain-line (light=deficit)"}

def mixture(c, foot, sign):
    """nu(y) + diagnostics for coefficient vector c >= 0 on XATOMS under the given response sign."""
    mu = 1.0 - sign*(c @ PSIX[foot])
    band = (XGRID >= 1e-3) & (XGRID <= 1e3)
    mu_min_band = float(mu[band].min()); mu_min_all = float(mu.min())
    mu_f = np.clip(mu, 1e-9, None)
    Y = mu_f*XGRID
    Ym = np.maximum.accumulate(Y)
    mono_viol = float(np.max((Ym - Y)/np.maximum(Ym, 1e-300)))
    lY, lx = np.log10(Ym), np.log10(XGRID)
    def nufn(y):
        ly = np.log10(y)
        return 10**(np.interp(ly, lY, lx) - ly)
    return nufn, dict(mu=mu, mu_min_band=mu_min_band, mu_min_all=mu_min_all, mono_viol=mono_viol)

def moments(c):
    m0 = float(np.dot(c, XATOMS - 2.0))                 # conformal balance (must be 0 for the legal family)
    var = float(np.dot(c, (XATOMS - 2.0)**2))           # when m0=0 this equals m1 = sum c(x-2)x: FORCED > 0
    return m0, var, float(c.sum()), float(c[(XATOMS > 1.9) & (XATOMS < 2.1)].sum())

def rebalance(c):
    """exact conformal balance: scale the light side so sum c (x-2) = 0 to machine precision."""
    c = c.copy(); hp = (XATOMS > 2.0); lp = ~hp
    Sp = np.dot(c[hp], XATOMS[hp] - 2.0); Sm = np.dot(c[lp], 2.0 - XATOMS[lp])
    if Sm > 0: c[lp] *= Sp/Sm
    return c

def solar_lines(c, foot, sign):
    """mu, response c(x)=1/mu-1 and delta_a at the Sun-reflex and Saturn-radial lines + measured tail power."""
    out = {}
    for lab, xacc, amb in (("sun", A_SUN/A0[foot], A_SUN), ("sat", G_SAT/A0[foot], G_SAT)):
        al = ETA[foot]*xacc; t = 2.0/(1.0 + al*al)
        E = float(np.dot(c, TK @ wvec(t)))
        one_minus_mu = sign*E/np.sqrt(1.0 + al*al)
        mu = 1.0 - one_minus_mu
        cresp = one_minus_mu/mu                       # 1/mu - 1; sign carries: deficit > 0, anti-MOND < 0
        out[lab] = (mu, cresp, amb*cresp)
    xs = np.logspace(3, 6, 16); vals = []
    for xacc in xs:
        al = ETA[foot]*xacc; t = 2.0/(1.0 + al*al)
        vals.append(abs(float(np.dot(c, TK @ wvec(t))))/np.sqrt(1.0 + al*al))
    vals = np.array(vals); pos = vals > 0
    out["tail_power"] = float(np.polyfit(np.log10(xs[pos]), np.log10(vals[pos]), 1)[0]) if pos.sum() > 4 else np.nan
    return out

# the balanced positive cone, EXACTLY: every balanced positive measure on the atom grid is a positive
# combination of two-point balanced pairs v_ij = e_i/(2-x_i) + e_j/(x_j-2), x_i < 2 < x_j
LIG = np.where(XATOMS < 2.0)[0]; HVY = np.where(XATOMS > 2.0)[0]
PAIRS = [(i, j) for i in LIG for j in HVY]
VMAT = np.zeros((NA, len(PAIRS)))
for p_, (i_, j_) in enumerate(PAIRS):
    VMAT[i_, p_] = 1.0/(2.0 - XATOMS[i_]); VMAT[j_, p_] = 1.0/(XATOMS[j_] - 2.0)
P(f"\n    balanced cone: {len(LIG)} light x {len(HVY)} heavy = {len(PAIRS)} generating pairs (exact parameterization)")

# ---------------------------------------------------------------- [5] fits per (footing, sign)
P("\n" + LINE); P("[5] NNLS per (footing, sign): positive unbalanced / balanced cone / signed control"); P(LINE)

def make_design(foot, sign):
    a0 = A0[foot]
    Ud0 = 0.52 if foot == "fw" else 0.46                     # McGaugh-best Upsilon (locked .out)
    gb = GA + Ud0*GD + Ud0*GB
    ok = OKB & (gb > 0)
    xacc = GO[ok]/a0
    lo, hi = np.percentile(np.log10(xacc), [0.5, 99.5])
    edges = np.linspace(lo, hi, 37)
    cent = 0.5*(edges[1:] + edges[:-1]); xb = 10**cent
    nb, _ = np.histogram(np.log10(xacc), bins=edges)
    keep = nb > 0
    xb, nb = xb[keep], nb[keep]
    wb = np.sqrt(nb)/(np.log(10)*mu_target(xb)*L_target(xb))   # bin weight ~ data density / dex conversion
    PSIb = build_PSI(xb, ETA[foot])
    Adat = sign*(PSIb*wb[None, :]).T
    ydat = (1.0 - mu_target(xb))*wb
    return Adat, ydat, xb, nb, wb

def report_fit(tag, c, foot, sign, Adat, ydat, nb):
    resid = Adat @ c - ydat
    rms_b = float(np.sqrt(np.sum(resid**2)/np.sum(nb)))
    m0, var, mt, m2 = moments(c)
    nufn, dg = mixture(c, foot, sign)
    U, su, sw = best_ud(nufn, A0[foot])
    P(f"    {tag:42s} | shape-rms {rms_b:.4f} | SPARC unw {su:.4f} (Ud {U:.2f}; wt {sw:.4f}) | "
      f"mu_min band {dg['mu_min_band']:+.3f} all {dg['mu_min_all']:+.3f} mono {dg['mono_viol']:.1e}")
    P(f"    {'':42s} | m0 {m0:+.2e}  var=sum c(x-2)^2 {var:.3e}  mass {mt:.3e}  mass@2 {m2:.2e}")
    return su, sw, U

UDS_COARSE2 = UDS[::3]
def real_obj_factory(foot, sign, Mmap, solar=False, bscale=1.0):
    a0 = A0[foot]
    def f(w):
        w = np.maximum(w, 0.0)
        c = Mmap @ w
        nufn, dg = mixture(c, foot, sign)
        _, su, _ = best_ud(nufn, a0, grid=UDS_COARSE2)
        pen = 1e2*max(0.0, -dg["mu_min_all"]) + 1e2*dg["mono_viol"]
        if solar:
            sol = solar_lines(c, foot, sign)
            pen += 10.0*max(0.0, np.log10(max(abs(sol["sun"][2]), 1e-30)/(bscale*BUD_SUN_STRICT)))
            pen += 10.0*max(0.0, np.log10(max(abs(sol["sat"][2]), 1e-30)/(bscale*BUD_SAT)))
        return su + pen
    return f

def polish(Mmap, w0, foot, sign, solar, maxfev=4000, xtol=1e-3, bscale=1.0):
    """Powell polish on the LOCKED objective (coarse inner Ud scan) over a nonneg weight vector."""
    f = real_obj_factory(foot, sign, Mmap, solar=solar, bscale=bscale)
    best_s, best_f = 1.0, f(w0)
    for s in np.logspace(-1.5, 1.5, 31):                      # amplitude prescan
        v = f(s*w0)
        if v < best_f: best_f, best_s = v, s
    w0 = best_s*w0
    from scipy.optimize import Bounds
    res = minimize(f, w0, method="Powell", bounds=Bounds(0.0, np.inf),
                   options=dict(maxfev=maxfev, xtol=xtol, ftol=1e-6))
    w = np.maximum(res.x, 0.0)
    return Mmap @ w, res

RES = {}
for foot in ("fw", "canon"):
    for sign in (+1, -1):
        key = (foot, sign)
        P(f"\n  === footing {foot} (a0={A0[foot]:.2e}), sign {sign:+d} = {SIGNS[sign]} ===")
        Adat, ydat, xb, nb, wb = make_design(foot, sign)
        # (U) unconstrained positive
        cU, rU = nnls(Adat, ydat)
        # (B) balanced cone: NNLS over the exact pair parameterization
        Apair = Adat @ VMAT
        wB, rB = nnls(Apair, ydat)
        cB = rebalance(VMAT @ wB)
        # single-pair surrogate ranking (seeds + diagnostic): 1-D optimal amplitude per pair
        num = Apair.T @ ydat; den = np.einsum('ij,ij->i', Apair.T, Apair.T)
        amp1 = np.where((num > 0) & (den > 0), num/np.maximum(den, 1e-300), 0.0)
        res1 = np.sum(ydat**2) - 2*amp1*num + amp1**2*den
        rank = list(np.argsort(res1)[:8])
        P("    top single pairs (surrogate): " + "; ".join(
            f"({XATOMS[PAIRS[p][0]]:.2f},{XATOMS[PAIRS[p][1]]:.1f}) r={np.sqrt(max(res1[p],0)/np.sum(nb)):.3f}"
            for p in rank[:5]))
        uU = report_fit("NNLS positive UNBALANCED (illegal 1/a tail)", cU, foot, sign, Adat, ydat, nb)
        uB = report_fit("NNLS BALANCED cone (the legal family)", cB, foot, sign, Adat, ydat, nb)
        RES[key] = dict(cU=cU, cB=cB, uU=uU, uB=uB, design=(Adat, ydat, xb, nb), wB=wB, rank=rank)

# signed control once per footing (coefficient signs free = ILLEGAL; basis ceiling diagnostic)
for foot in ("fw", "canon"):
    Adat, ydat, xb, nb, wb = make_design(foot, +1)
    PENS = 1e3*np.abs(Adat).max()/np.abs(XATOMS - 2.0).max()
    cS = np.linalg.lstsq(np.vstack([Adat, PENS*(XATOMS - 2.0)]), np.append(ydat, 0.0), rcond=None)[0]
    P(f"\n  [signed control, {foot}]")
    uS = report_fit("SIGNED lstsq control (illegal; basis ceiling)", cS, foot, +1, Adat, ydat, nb)
    RES[(foot, "signed")] = uS

# ---------------------------------------------------------------- [6] Powell polish on the locked objective
P("\n" + LINE); P("[6] POLISH (Powell, locked objective, coarse inner Ud scan; full scan at report)"); P(LINE)
for foot in ("fw", "canon"):
    for sign in (+1, -1):
        key = (foot, sign); R = RES[key]
        P(f"\n  === footing {foot}, sign {sign:+d} ===")
        Adat, ydat, xb, nb = R["design"]
        # balanced: active pairs = NNLS support + surrogate top-8
        topw = [p for p in np.argsort(R["wB"])[::-1][:24] if R["wB"][p] > 0]
        act = sorted(set(topw + R["rank"]))
        Mp = VMAT[:, act]
        w0 = R["wB"][act].copy()
        if w0.max() <= 0:
            w0 = np.where(np.isin(act, R["rank"][:1]), 1.0, 1e-6)   # seed from best surrogate pair
        t_p = time.time()
        cPb, resP = polish(Mp, w0, foot, sign, solar=False)
        cPb = rebalance(cPb)
        P(f"    balanced polish: nfev={resP.nfev} ({time.time()-t_p:.0f}s)")
        uP = report_fit("POLISHED balanced (SPARC-only)", cPb, foot, sign, Adat, ydat, nb)
        # balanced + solar budget (start from the SPARC-only polished point, re-expressed in pair weights)
        w0q = np.linalg.lstsq(Mp, cPb, rcond=None)[0].clip(min=0) + 1e-12
        t_p = time.time()
        cQb, resQ = polish(Mp, w0q, foot, sign, solar=True, maxfev=3000)
        cQb = rebalance(cQb)
        P(f"    balanced+solar polish: nfev={resQ.nfev} ({time.time()-t_p:.0f}s)")
        uQ = report_fit("POLISHED balanced + SOLAR-CONSTRAINED", cQb, foot, sign, Adat, ydat, nb)
        # unbalanced control polish (atom space, active set)
        actA = sorted(set(list(np.where(R["cU"] > 0)[0]) + [0, 5, 10, 16, 22, 28, 34, NA - 1]))
        Ma = np.eye(NA)[:, actA]
        t_p = time.time()
        cPu, resU = polish(Ma, np.maximum(R["cU"][actA], 1e-9), foot, sign, solar=False, maxfev=2500)
        P(f"    unbalanced polish: nfev={resU.nfev} ({time.time()-t_p:.0f}s)")
        uPu = report_fit("POLISHED unbalanced (illegal control)", cPu, foot, sign, Adat, ydat, nb)
        R.update(cP=cPb, uP=uP, cQ=cQb, uQ=uQ, cPu=cPu, uPu=uPu, act=act)

# ---------------------------------------------------------------- [6b] aggressive restarts (fairness)
P("\n" + LINE); P("[6b] AGGRESSIVE RESTARTS: balanced family, the MOND-capable sign (-1), both footings"); P(LINE)
for foot in ("fw", "canon"):
    sign = -1; R = RES[(foot, sign)]
    Adat, ydat, xb, nb = R["design"]
    a0 = A0[foot]
    # alternative target: the DATA's own binned-median shape (not the McGaugh functional form)
    Ud0 = 0.40
    gb = GA + Ud0*GD + Ud0*GB; ok = OKB & (gb > 0) & (GO > 0)
    xacc = GO[ok]/a0; mu_dat = gb[ok]/GO[ok]
    lo, hi = np.percentile(np.log10(xacc), [0.5, 99.5]); edges = np.linspace(lo, hi, 37)
    idx = np.digitize(np.log10(xacc), edges)
    xb2, tb2 = [], []
    for b in range(1, len(edges)):
        m = idx == b
        if m.sum() > 3:
            xb2.append(10**(0.5*(edges[b-1] + edges[b]))); tb2.append(np.median(mu_dat[m]))
    xb2 = np.array(xb2); tb2 = np.clip(np.array(tb2), 1e-3, None)
    wb2 = 1.0/(np.log(10)*tb2*np.maximum(L_target(xb2), 0.5))
    PSIb2 = build_PSI(xb2, ETA[foot])
    A2 = sign*(PSIb2*wb2[None, :]).T; y2 = (1.0 - tb2)*wb2
    w2, _ = nnls(A2 @ VMAT, y2)
    act = sorted(set([p for p in np.argsort(R["wB"])[::-1][:24] if R["wB"][p] > 0]
                     + [p for p in np.argsort(w2)[::-1][:24] if w2[p] > 0] + list(R["rank"])))
    Mp = VMAT[:, act]
    best_c, best_su = R["cP"], R["uP"][0]
    for lab0, w0 in (("from-NNLS", np.linalg.lstsq(Mp, R["cB"], rcond=None)[0].clip(min=0) + 1e-12),
                     ("from-data-median", w2[act] + 1e-12)):
        cX, rX = polish(Mp, w0, foot, sign, solar=False, maxfev=12000, xtol=1e-5)
        cX = rebalance(cX)
        nufnX, dgX = mixture(cX, foot, sign)
        _, suX, _ = best_ud(nufnX, a0)
        P(f"    {foot} restart {lab0:18s}: nfev={rX.nfev} -> SPARC unw {suX:.4f} "
          f"(mu_min {dgX['mu_min_all']:+.3f})")
        if suX < best_su and dgX["mu_min_all"] > -1e-9:
            best_su, best_c = suX, cX
    R["act"] = act
    if best_su < R["uP"][0]:
        P(f"    {foot}: improved balanced optimum {R['uP'][0]:.4f} -> {best_su:.4f}; UPDATING")
        R["cP"] = best_c
        R["uP"] = report_fit("POLISHED balanced (best restart)", best_c, foot, sign, Adat, ydat, nb)
    else:
        P(f"    {foot}: no improvement over {R['uP'][0]:.4f} (restarts confirm the optimum)")

# ---------------------------------------------------------------- [7] solar budgets
P("\n" + LINE); P("[7] SOLAR BUDGETS (agentE reflex strict 2.47e-15 / loose 3.38e-15 ; Saturn radial 1e-14)"); P(LINE)
P(f"    {'mixture':38s} {'foot':5s} {'sgn':>3s} {'1-mu(sun)':>11s} {'da_sun':>10s} {'x_strict':>9s} "
  f"{'da_Sat':>10s} {'x_Sat':>9s} {'tailpow':>8s}  verdict")
SOLAR = {}
def solar_row(lab, c, foot, sign):
    sol = solar_lines(c, foot, sign)
    mu_s, cr_s, da_s = sol["sun"]; mu_t, cr_t, da_t = sol["sat"]
    ok_s = abs(da_s) <= BUD_SUN_STRICT; ok_sl = abs(da_s) <= BUD_SUN_LOOSE; ok_t = abs(da_t) <= BUD_SAT
    v = ("PASS" if ok_s else ("PASS(loose)" if ok_sl else "FAIL-sun")) + ("" if ok_t else "+FAIL-Sat")
    P(f"    {lab:38s} {foot:5s} {sign:+3d} {1-mu_s:11.3e} {da_s:10.3e} {abs(da_s)/BUD_SUN_STRICT:9.2e} "
      f"{da_t:10.3e} {abs(da_t)/BUD_SAT:9.2e} {sol['tail_power']:8.2f}  {v}")
    SOLAR[(foot, sign, lab)] = (da_s, da_t, v)
    return v
for foot in ("fw", "canon"):
    for sign in (+1, -1):
        R = RES[(foot, sign)]
        solar_row("NNLS UNBALANCED", R["cU"], foot, sign)
        solar_row("POLISHED unbalanced", R["cPu"], foot, sign)
        solar_row("NNLS BALANCED", R["cB"], foot, sign)
        solar_row("POLISHED balanced", R["cP"], foot, sign)
        solar_row("POLISHED balanced+solar", R["cQ"], foot, sign)

# [7b] the pincer curve: how much solar overage must the balanced family buy to reach a given scatter?
P("\n    [7b] PINCER CURVE (fw, sign -1): best balanced scatter vs allowed solar budget k x strict")
P(f"         (the band fit needs var = sum c(x-2)^2 ~ 5; the strict sun line caps var; no sweet spot = pincer)")
foot, sign = "fw", -1; R = RES[(foot, sign)]
Mp = VMAT[:, R["act"]]
w_start = np.linalg.lstsq(Mp, R["cP"], rcond=None)[0].clip(min=0) + 1e-12
P(f"         {'k':>8s} {'scatter':>8s} {'+over base':>10s} {'da_sun/strict':>13s} {'var':>9s}")
for k in (1.0, 3.16, 10.0, 31.6, 100.0):
    cK, rK = polish(Mp, w_start, foot, sign, solar=True, bscale=k, maxfev=6000, xtol=1e-4)
    cK = rebalance(cK)
    nufnK, dgK = mixture(cK, foot, sign)
    _, suK, _ = best_ud(nufnK, A0[foot])
    solK = solar_lines(cK, foot, sign)
    m0K, varK, mtK, _ = moments(cK)
    P(f"         {k:8.2f} {suK:8.4f} {suK-BASE[foot]:+10.4f} {abs(solK['sun'][2])/BUD_SUN_STRICT:13.2f} {varK:9.3f}")

# ---------------------------------------------------------------- [8] shape autopsy (best legal, fw)
P("\n" + LINE); P("[8] SHAPE AUTOPSY (framework footing; the sign that serves the escape best)"); P(LINE)
sbest = min((+1, -1), key=lambda s: RES[("fw", s)]["uP"][0])
R = RES[("fw", sbest)]
P(f"    best-escape sign: {sbest:+d} = {SIGNS[sbest]}")
nuP, dgP = mixture(R["cP"], "fw", sbest)
nuQ, dgQ = mixture(R["cQ"], "fw", sbest)
nuU, dgU = mixture(R["cPu"], "fw", sbest)
xs_show = np.array([0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 30.0, 100.0])
P(f"    {'x=a/a0':>8s} {'mu_tgt':>8s} {'mu_unbal':>9s} {'mu_bal(P)':>9s} {'mu_bal(Q)':>9s} "
  f"{'dex(nu_P vs McGaugh)':>21s}")
for x in xs_show:
    i = int(np.argmin(np.abs(np.log10(XGRID) - np.log10(x))))
    mt = float(mu_target(x)); y = mt*x
    ddex = float(np.log10(nuP(np.array([y]))[0]) - np.log10(nu_rar(y)))
    P(f"    {x:8.2f} {mt:8.4f} {dgU['mu'][i]:9.4f} {dgP['mu'][i]:9.4f} {dgQ['mu'][i]:9.4f} {ddex:21.4f}")
ys = np.logspace(-4, 2, 400)
dd = np.abs(np.log10(nuP(ys)) - np.log10(nu_rar(ys)))
below = ys[dd > 0.05]
if len(below):
    P(f"    flattening: |dex(nu_P, McGaugh)| > 0.05 for y < {below.max():.3f} "
      f"(the agentV a_* flattening pulled INTO the band)")
else:
    P("    no 0.05-dex deviation from the McGaugh nu anywhere in y = 1e-4..1e2")
P("    polished balanced spectral content (c_j > 1e-4 of max):")
cm = R["cP"].max() if R["cP"].max() > 0 else 1.0
for j in range(NA):
    if R["cP"][j] > 1e-4*cm:
        P(f"      x={XATOMS[j]:6.2f}: c={R['cP'][j]:.4e}")

# ---------------------------------------------------------------- [9] VERDICT
P("\n" + LINE); P("[9] VERDICT (pre-registered thresholds)"); P(LINE)
verdict_rows = []
for foot in ("fw", "canon"):
    base = BASE[foot]
    P(f"  footing {foot}: McGaugh baseline {base:.4f} | survival {base+0.01:.4f} | closed line {base+0.02:.4f}")
    for sign in (+1, -1):
        R = RES[(foot, sign)]
        P(f"    sign {sign:+d}: NNLS bal {R['uB'][0]:.4f} (+{R['uB'][0]-base:.4f}) ; "
          f"POL bal {R['uP'][0]:.4f} (+{R['uP'][0]-base:.4f}) ; "
          f"POL bal+solar {R['uQ'][0]:.4f} (+{R['uQ'][0]-base:.4f}) ; "
          f"[controls] unbal-pol {R['uPu'][0]:.4f} ; NNLS unbal {R['uU'][0]:.4f}")
    P(f"    [signed lstsq ceiling] {RES[(foot,'signed')][0]:.4f} (+{RES[(foot,'signed')][0]-base:.4f})")
    cand = []
    for sign in (+1, -1):
        R = RES[(foot, sign)]
        for lab, ckey, ukey in (("NNLS BALANCED", "cB", "uB"), ("POLISHED balanced", "cP", "uP"),
                                ("POLISHED balanced+solar", "cQ", "uQ")):
            cand.append((R[ukey][0], lab, sign, R[ckey]))
    cand.sort(key=lambda r: r[0])
    su, lab, sign, c = cand[0]
    da_s, da_t, v = SOLAR[(foot, sign, lab)]
    d = su - base
    P(f"    BEST LEGAL [{foot}]: {lab} (sign {sign:+d}) -> {su:.4f} = baseline + {d:.4f} ; solar {v}")
    verdict_rows.append((foot, d, v.startswith("PASS")))
P("")
lives = [f for f, d, ok in verdict_rows if d <= 0.0100 and ok]
within2_ok = [f for f, d, ok in verdict_rows if d <= 0.0200 and ok]
if lives:
    P("  => ESCAPE-LIVES at " + ", ".join(lives))
elif within2_ok:
    P("  => PARTIAL: a legal mixture sits within 0.02 dex with solar intact at " + ", ".join(within2_ok))
else:
    P("  => ESCAPE-CLOSED: no legal (conformal-balanced, KL-positive) mixture reaches baseline+0.02 dex")
    P("     with the solar budgets intact, at EITHER footing, under EITHER sign convention.")
P(f"\nDONE in {time.time()-T0:.0f}s.")
_f.close()
