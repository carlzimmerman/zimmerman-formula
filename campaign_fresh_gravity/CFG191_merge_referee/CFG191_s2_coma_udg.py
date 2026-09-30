#!/usr/bin/env python3
"""CFG191_s2_coma_udg -- item (b): the Coma UDG 'E7 merge fails 5.6 / 5.4 sigma'.  Own reconstruction from the committed Freundlich+2022
tsv; own E7 solver; L23's field table and error budget quoted (string-checked against L23's committed .out).  No CFG179 file is opened.
MUTATE=1: M3 (g_ext -> 0, ownership) and M4 (g_obs x 10^1.3) -- both must make the 'fails >= 5 sigma' check fail."""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, sympy as sp, pathlib, re
from scipy.optimize import brentq
from CFG191_common import Run, REPO, rel
np.seterr(all="ignore")
R = Run("CFG191_s2_coma_udg", "item (b): Coma UDGs under the E7 merge")
MUT = R.mutate
TSV = REPO/"real_research/data/freundlich2022_coma_udgs.tsv"
L23 = REPO/"fable_independent_2026/L23_udg_verify.out"
G, MSUN, KPC, LSUN = 6.674e-11, 1.989e30, 3.0857e19, 3.828e26
A0_CAN, A0_ALT, A0_L23 = 9.3603e-11, 1.1312e-10, 9.3619e-11
R.p(f"inputs: {rel(TSV)} (measured columns + Freundlich+2022 model columns), {rel(L23)} (field table, budget; quoted)")

# ---- data
rows = [l.rstrip("\n").split("\t") for l in TSV.read_text().splitlines() if l.strip() and not l.startswith("#")]
hdr, body = rows[0], rows[1:]
D = {h: np.array([r[i] for r in body], dtype=object) for i, h in enumerate(hdr)}
num = lambda k: np.array(D[k], dtype=float)
name, dmean, L1e8, Re, ML, sig = D["name"], num("dmean_kpc"), num("L_1e8"), num("Re_kpc"), num("ML"), num("sig")
lgbar_t, elgbar, lgobs_t, elgobs = num("lgbar"), num("elgbar"), num("lgobs"), num("elgobs")
N = len(name)
w = 1.0/(elgobs**2 + elgbar**2); w /= w.sum()
R.p(f"{N} galaxies; weights 1/(elgobs^2+elgbar^2) normalised (L23's estimator)")

R.sec("classification of inputs (frozen before any number)")
R.p("  MEASURED: sigma_obs (esig), R_e, L, projected distance.   MODEL-DEPENDENT: M/L (SSP fits), the sigma->g estimator (3 sigma^2/r_1/2, r_1/2 = 4 R_e/3, g_bar = G M_*/2 / r_1/2^2),")
R.p("  the 3-D position (van der Burg Einasto), the Coma mass profile and hence g_ext (beta model + closure inversion, L23), E7's theta_0 = sqrt 2 (postulated), the kernel (P2), the 0.235-dex budget.")

R.sec("B1  control: my g_bar, g_obs from (L, M/L, R_e, sigma)")
rh = 4*Re*KPC/3
g_obs_my = 3*(sig*1e3)**2/rh
Mstar = ML*L1e8*1e8*MSUN                       # solar luminosity * M/L -> solar masses; L in L_sun, M/L in solar units
g_bar_my = G*(Mstar/2)/rh**2
d_b, d_o = np.abs(np.log10(g_bar_my) - lgbar_t), np.abs(np.log10(g_obs_my) - lgobs_t)
R.p(f"  max |dlog g_bar| = {d_b.max():.4f} dex, max |dlog g_obs| = {d_o.max():.4f} dex")
R.check("B1 reconstruction matches the tsv columns to <= 0.02 dex", d_b.max() <= 0.02 and d_o.max() <= 0.02)

# ---- kernels
nu_rar = lambda y: 1/(1 - np.exp(-np.sqrt(y)))
nu_p2 = lambda y: np.sqrt(1 + 1/y)
def wmean(x, ww=None): return float(np.sum((w if ww is None else ww)*x))
def offset_iso(nu, a0, lgb=None, lgo=None):
    lgb = lgbar_t if lgb is None else lgb; lgo = lgobs_t if lgo is None else lgo
    y = 10**lgb/a0
    return lgo - np.log10(10**lgb*nu(y))

R.sec("B2  control: isolated stars-only nu_RAR offset, a0 = 9.3619e-11 (L23 C1: +0.3965)")
o_rar = offset_iso(nu_rar, A0_L23)
o_rar_my = offset_iso(nu_rar, A0_L23, np.log10(g_bar_my), np.log10(g_obs_my))
R.p(f"  tsv columns: {wmean(o_rar):+.4f}; my reconstruction: {wmean(o_rar_my):+.4f}")
R.check("B2 isolated nu_RAR offset +0.3965 +- 0.003 (tsv columns)", abs(wmean(o_rar) - 0.3965) <= 0.003)

R.sec("B3  E7 cubic: re-derived and solved")
x, b, e = sp.symbols("x b e", positive=True)
Mf = lambda t: (sp.sqrt(1 + 4*t**2) - 1)/2
# M(x+e) x/(x+e) = b  ->  (s-1) x = 2 b (x+e), s = sqrt(1+4(x+e)^2); squaring and dividing by 4(x+e):
sq = sp.expand((x + 2*b*(x+e))**2 - x**2 - 4*x**2*(x+e)**2)      # (x+2b(x+e))^2 = x^2 + 4x^2 (x+e)^2   [s x = x + 2b(x+e)]
cubic = sp.expand(-sq/(4*(x+e)))
cubic = sp.simplify(cubic)
target = x**3 + e*x**2 - b*(b+1)*x - b**2*e
R.p(f"  squared equation / (-4(x+e)) simplifies to: {sp.factor(cubic)}")
R.check("B3a sympy: clearing the radical gives x^3 + e x^2 - b(b+1) x - b^2 e = 0", sp.simplify(cubic - target) == 0)
def E7x(bb, ee):
    r = np.roots([1.0, ee, -bb*(bb+1), -bb*bb*ee]); pos = [q.real for q in r if abs(q.imag) < 1e-12*max(1, abs(q.real)) and q.real > 0]
    assert len(pos) == 1, (bb, ee, r)
    return pos[0]
# direct check against the defining equation
chk = []
for bb, ee in ((0.008, 1.195), (0.01, 0.16), (1.0, 3.0)):
    xx = E7x(bb, ee); chk.append(abs(float(Mf(sp.Float(xx+ee))*xx/(xx+ee)) - bb))
R.check("B3b unique positive root (Descartes) and it solves M(x+e) x/(x+e) = b to 1e-9", max(chk) < 1e-9, f"max residual {max(chk):.1e}")
R.check("B3c e=0 gives x = sqrt(b^2+b) (the isolated P2 law)", abs(E7x(0.05, 1e-12) - np.sqrt(0.05**2 + 0.05)) < 1e-6)

# ---- L23 quoted inputs, string-checked
txt = L23.read_text()
need = ["Freundlich+2022 X-ray beta-model                              1.059         0.845         0.427",
        "quadrature sum of systematics                                         0.227",
        "statistical (inverse-variance, as h9 quoted it)                       0.062",
        "corrected EFE, equilibrium at the Einasto mean 3-D radius, canonical    +1.159      4.9",
        "corrected EFE, first infall at 9 Mpc (Nagesh+2024 resolution)       +0.635      2.7",
        "9 Mpc"]
FIELD_R = np.array([0.87, 1.13, 2.34]); FIELD_G = np.array([1.059, 0.845, 0.427])
budget = dict(ML=0.148, aperture=0.120, mass_model_position=0.088, sigma_instr=0.052, estimator=0.047, a0_footing=0.047, distance=0.021)
R.check("L23 quoted strings present in its committed .out (field table 1.059/0.845/0.427; budget 0.227 / 0.062; 4.9 sigma; 2.7 sigma)", all(" ".join(s.split()) in " ".join(txt.split()) for s in need))
sys_q = float(np.sqrt(sum(v*v for v in budget.values()))); STAT = 0.062
TOT = float(np.hypot(sys_q, STAT))
R.p(f"  budget quadrature: systematic {sys_q:.4f}, with statistic {TOT:.4f} (L23: 0.227, 0.235)")
R.check("B7a 0.235 = sqrt(0.227^2 + 0.062^2) recomputed from L23's seven entries", abs(TOT - 0.235) < 0.002)
R.data["budget_total"] = TOT

# ---- headline
def gext_ratio(a0, gext_can=0.845):
    return gext_can*A0_L23/a0          # L23 canonical ratio converted to SI with L23's a0, re-expressed in this footing's a0
def e7_offsets(a0, gext_over_a0, lgb=None, lgo=None, mlmult=1.0):
    lgb = lgbar_t if lgb is None else lgb; lgo = lgobs_t if lgo is None else lgo
    gb = 10**lgb*mlmult
    bb = gb/a0
    ge = np.broadcast_to(np.asarray(gext_over_a0, dtype=float), bb.shape)
    xx = np.array([E7x(b_, np.sqrt(2)*g_) for b_, g_ in zip(bb, ge)])
    return lgo - np.log10(xx*a0)
def iso_p2(a0, **kw):
    lgb = kw.get("lgb", lgbar_t); lgo = kw.get("lgo", lgobs_t)
    y = 10**lgb/a0
    return lgo - np.log10(10**lgb*nu_p2(y))

lgo_use = lgobs_t + (1.3 if MUT and False else 0)
R.sec("B4  HEADLINE: E7 (P2) offset, weighted mean, single field 0.845 a0 (beta model at 1.13 Mpc)")
if MUT:
    R.p("  MUTATE: M3 = g_ext set to 0 (ownership) AND M4 = g_obs multiplied by 10^1.3, evaluated as two separate controls below")
head = {}
for foot, a0, tgt_off, tgt_sig in (("canonical", A0_CAN, 1.309, 5.6), ("alt", A0_ALT, 1.275, 5.4)):
    g_ratio = gext_ratio(a0)
    off = e7_offsets(a0, g_ratio)
    om, sg = wmean(off), wmean(off)/TOT
    head[foot] = dict(offset=om, sigma=sg, gext=g_ratio, iso=wmean(iso_p2(a0)))
    R.p(f"  {foot:9s} a0={a0:.4e}: g_ext/a0 = {g_ratio:.4f}; E7 offset {om:+.4f} dex = {sg:.2f} sigma  (README {tgt_off:+.3f} / {tgt_sig})   isolated P2 {head[foot]['iso']:+.4f} = {head[foot]['iso']/TOT:.2f} sigma")
R.data["headline"] = head
if not MUT:
    R.check("B4a E7 offset within 0.03 dex of README (+1.309 / +1.275) on both footings", abs(head["canonical"]["offset"]-1.309) <= 0.03 and abs(head["alt"]["offset"]-1.275) <= 0.03)
    R.check("B4b significance within 0.15 sigma of README (5.6 / 5.4) on both footings", abs(head["canonical"]["sigma"]-5.6) <= 0.15 and abs(head["alt"]["sigma"]-5.4) <= 0.15)
    R.check("B4c 'fails' as a statement: E7 significance >= 5 sigma on both footings (this is the load-bearing cell M3/M4 flip)", min(head["canonical"]["sigma"], head["alt"]["sigma"]) >= 5.0)
else:
    off0 = wmean(iso_p2(A0_CAN))
    R.p(f"  M3 (g_ext = 0): offset {off0:+.4f} = {off0/TOT:.2f} sigma")
    R.check("B4c [M3] E7 significance >= 5 sigma with g_ext = 0 -- must FAIL", off0/TOT >= 5.0)
    off4 = wmean(e7_offsets(A0_CAN, gext_ratio(A0_CAN), lgo=lgobs_t + 1.3))
    R.p(f"  M4 AS FROZEN (g_obs x 10^+1.3): offset {off4:+.4f} = {off4/TOT:.2f} sigma  -- the frozen text has the SIGN WRONG: offset = log g_obs - log g_pred, so raising g_obs widens it; kept, not repaired")
    R.check("B4c' [M4 as frozen, x10^+1.3] E7 significance >= 5 sigma -- frozen expectation was that this FAILS; it does not (frozen-text sign error, kept)", off4/TOT >= 5.0, lb=False)
    off4b = wmean(e7_offsets(A0_CAN, gext_ratio(A0_CAN), lgo=lgobs_t - 1.3))
    R.p(f"  M4' (labelled deviation, corrected sign, g_obs x 10^-1.3): offset {off4b:+.4f} = {off4b/TOT:.2f} sigma")
    R.check("B4c'' [M4' corrected sign] E7 significance >= 5 sigma with g_obs x 10^-1.3 -- must FAIL", off4b/TOT >= 5.0)

R.sec("B5  ownership: P2 isolated stars-only")
R.p(f"  canonical {head['canonical']['iso']:+.4f} dex ({head['canonical']['iso']/TOT:.2f} sigma of {TOT:.3f}); alt {head['alt']['iso']:+.4f} ({head['alt']['iso']/TOT:.2f})")
R.p(f"  E7 minus isolated (the EFE term) canonical: {head['canonical']['offset']-head['canonical']['iso']:+.4f} dex")
R.p(f"  nu_RAR isolated: canonical {wmean(offset_iso(nu_rar, A0_CAN)):+.4f}, alt {wmean(offset_iso(nu_rar, A0_ALT)):+.4f}")

R.sec("B6  field sweep (L23 first-infall rows and the beta-model bracket), both footings")
sweep = {}
for gc in (0.112, 0.168, 0.252, 0.427, 0.653, 0.845, 1.059):
    r_ = []
    for a0 in (A0_CAN, A0_ALT):
        o = wmean(e7_offsets(a0, gext_ratio(a0, gc))); r_.append((o, o/TOT))
    sweep[gc] = r_
    R.p(f"  g_ext = {gc:5.3f} a0(L23): canonical {r_[0][0]:+.3f} = {r_[0][1]:.2f} sigma | alt {r_[1][0]:+.3f} = {r_[1][1]:.2f} sigma")
R.data["sweep"] = {str(k): v for k, v in sweep.items()}
R.p("  README M6 bracket over 0.427-1.059: 4.7-5.7 sigma")
R.check("B6a equilibrium rows (0.427-1.059) all >= 4.5 sigma on both footings", all(sweep[g][i][1] >= 4.5 for g in (0.427, 0.653, 0.845, 1.059) for i in (0, 1)), lb=False)

R.sec("B7  error-budget attack: the same offset over different budgets")
oc = head["canonical"]["offset"]; ic = head["canonical"]["iso"]
R.p(f"  E7 offset {oc:+.3f}: over statistic only 0.062 -> {oc/0.062:.1f} sigma; over the full 0.235 -> {oc/TOT:.2f}; EFE term alone ({oc-ic:+.3f}) over sqrt(0.112^2+0.062^2)={np.hypot(0.112,0.062):.3f} -> {(oc-ic)/np.hypot(0.112,0.062):.2f} sigma")
R.p("  Reading: the '5.6 sigma' is offset / a DECLARED systematic budget (dominated by M/L 0.148 and aperture 0.120); it moves by a factor 3.8 between statistic-only and full budget. It is not a measured significance.")

R.sec("B8  per-galaxy fields (each galaxy at its dmean_kpc; log-log interpolation of L23's table)")
def field_at(dk):
    return np.exp(np.interp(np.log(dk/1000), np.log(FIELD_R), np.log(FIELD_G)))
gf = field_at(dmean)
R.p("  per-galaxy g_ext (a0 L23): " + ", ".join(f"{v:.3f}" for v in gf))
pg = {}
for foot, a0 in (("canonical", A0_CAN), ("alt", A0_ALT)):
    o = e7_offsets(a0, gf*A0_L23/a0); pg[foot] = (wmean(o), wmean(o)/TOT, o)
    R.p(f"  {foot:9s}: E7 offset {pg[foot][0]:+.4f} = {pg[foot][1]:.2f} sigma  (single-field row {head[foot]['offset']:+.4f})")
R.data["per_galaxy"] = {k: (v[0], v[1]) for k, v in pg.items()}

R.sec("B9  resampling (canonical, single field)")
o = e7_offsets(A0_CAN, gext_ratio(A0_CAN))
jk = [wmean(np.delete(o, i), np.delete(w, i)/np.delete(w, i).sum()) for i in range(N)]
R.p(f"  jackknife (drop one): offset range {min(jk):+.3f} to {max(jk):+.3f} -> {min(jk)/TOT:.2f} to {max(jk)/TOT:.2f} sigma")
idx_df44 = [i for i, n in enumerate(name) if n == "DF44"][0]
m = np.arange(N) != idx_df44
R.p(f"  drop DF44: {wmean(o[m], w[m]/w[m].sum()):+.3f}")
chil = np.array([n.startswith("J") for n in name])
R.p(f"  Chilingarian nine only: {wmean(o[chil], w[chil]/w[chil].sum()):+.3f};  DF44+DFX1 only: {wmean(o[~chil], w[~chil]/w[~chil].sum()):+.3f}")
rng = np.random.default_rng(191)
bw, bu = [], []
for _ in range(20000):
    ii = rng.integers(0, N, N); ww = w[ii]/w[ii].sum(); bw.append(float(np.sum(ww*o[ii]))); bu.append(float(o[ii].mean()))
R.p(f"  bootstrap weighted: {np.mean(bw):+.3f} +- {np.std(bw):.3f};  unweighted: {np.mean(bu):+.3f} +- {np.std(bu):.3f} (statistical only; the budget is coherent and does not average down)")
R.data["bootstrap"] = dict(weighted=(np.mean(bw), np.std(bw)), unweighted=(np.mean(bu), np.std(bu)), jack=(min(jk), max(jk)))

R.sec("B10  M/L closing factor for the E7 offset")
f = lambda lm: wmean(e7_offsets(A0_CAN, gext_ratio(A0_CAN), mlmult=10**lm))
lm = brentq(f, 0.0, 3.0)
R.p(f"  the offset closes at an M_* multiplier {10**lm:.1f} (L23: 14.4 for its recipe); SSP M/L range 0.37-1.48 would become {0.37*10**lm:.1f}-{1.48*10**lm:.1f}")
R.data["ml_closing"] = 10**lm

R.sec("B11  kernel dependence and control against L23's committed EFE rows (sphere-averaged nu(1+L/3) at y_extN, per-galaxy Einasto field)")
def coupling_offsets(nu, a0, ge_over_a0):
    lg = []
    for i in range(N):
        xe = ge_over_a0[i]
        ye = brentq(lambda y: y*nu(y) - xe, 1e-9, 1e4)
        h = 1e-5*ye; Lg = (np.log(nu(ye*(1+h))) - np.log(nu(ye*(1-h))))/(np.log(1+h) - np.log(1-h))
        lg.append(lgobs_t[i] - np.log10(10**lgbar_t[i]*nu(ye)*(1+Lg/3)))
    return np.array(lg)
kd = {}
for foot, a0, l23 in (("canonical", A0_L23, 1.159), ("alt", 1.13e-10, 1.112)):
    ge = gf*A0_L23/a0
    kd[foot] = (wmean(coupling_offsets(nu_rar, a0, ge)), wmean(coupling_offsets(nu_p2, a0, ge)))
    R.p(f"  {foot:9s}: nu_RAR sphere-coupling {kd[foot][0]:+.3f} (L23 committed {l23:+.3f}) | P2 sphere-coupling {kd[foot][1]:+.3f} | E7 P2 per-galaxy {wmean(e7_offsets(a0, ge)):+.3f}")
R.check("B11a control: my nu_RAR sphere-coupling row reproduces L23's committed +1.159 / +1.112 to 0.05 dex", abs(kd["canonical"][0]-1.159) <= 0.05 and abs(kd["alt"][0]-1.112) <= 0.05, "L23's alt a0 is 1.13e-10; a difference of the field re-expression convention would show here", lb=False)
R.data["kernel_dependence"] = kd

R.sec("VERDICT (frozen rule)")
if not MUT:
    hc = head["canonical"]; ha = head["alt"]
    inf = sweep[0.112]
    R.finding("(b) Coma UDG E7", "AGREES WITH QUALIFICATION" if (abs(hc['offset']-1.309) <= 0.03 and abs(ha['offset']-1.275) <= 0.03) else "DISAGREES",
              f"E7+P2 at 0.845 a0: {hc['offset']:+.3f}/{ha['offset']:+.3f} dex = {hc['sigma']:.2f}/{ha['sigma']:.2f} sigma over the declared 0.235 budget. Qualifications: (1) sigma = offset/declared systematic budget (statistic-only would be ~21); "
              f"(2) first-infall field (0.112 a0) gives {inf[0][1]:.2f}/{inf[1][1]:.2f} sigma; (3) ownership (isolated P2) is {head['canonical']['iso']/TOT:.2f} sigma without infall gas; (4) per-galaxy fields give {pg['canonical'][1]:.2f}/{pg['alt'][1]:.2f}; (5) E7's theta_0 is postulated.")
R.finish()
