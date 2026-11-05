#!/usr/bin/env python3
"""FN6_powerlaw_screening, reported and not graded (criteria 5f0f4a5d99): for each passing (window) point, the length at
1 Msun against wide-binary separations, and the DR4 gamma_v the frozen pipeline (prep_2026/gaia_dr4_prep, imported read
only) would return, by CW1's injection procedure (cw1.py lines 229-262) with FN6's form-R curve in place of CW1's forms.
The curve: the l = 0 gamma_r of a 1 Msun point mass at the window's L(1 Msun), form R (S applied to CZ3's SO phantom
monopole, the planet engine of fn6_small.py), host field CW1's primary 1.9e-10 m/s^2 inverted to Newtonian. One mass, so
L / r_M is held at its 1 Msun value for every pair (a stated approximation: it scales as M^(p - 1/2)). A prediction only.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 -I -B fn6_wb.py. kappa = 1/2 FITTED and held fixed; not theory closed."""
import contextlib, hashlib, io, json, math, os, resource, sys, time
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
import warnings
for _m in ("invalid value encountered in matmul", "divide by zero encountered in matmul", "overflow encountered in matmul"): warnings.filterwarnings("ignore", message=_m)
from scipy.optimize import brentq
from scipy.special import erf
T00 = time.time(); HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); OUT = []; RES = {}
def P(s=""): print(s, flush=True); OUT.append(s)
G, MS, AU = 6.6743e-11, 1.98892e30, 1.495978707e11; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; GPRI = 1.9e-10; M0 = 6.0e10
S_KAU = np.array([1, 2, 3, 5, 7, 10, 15, 20, 30], float)
nu = lambda y: 0.5 + np.sqrt(0.25 + 1 / np.maximum(y, 1e-300))
def eta_newton(gobs, a0): eo = gobs / a0; return brentq(lambda y: float(y * nu(y)) - eo, 1e-9, eo)   # CW1's inversion
# ---- copied from fn6_small.py (CZ3's monopole and gh_pt, verbatim there; FN6's outer smoothing)
def monopole(h, a0, ge, N):   # CZ3 verbatim
    mu, w = np.polynomial.legendre.leggauss(N); H = h[:, None]; m = mu[None, :]; y = np.sqrt(H * H + ge * ge + 2 * H * ge * m) / a0
    return .5 * np.sum(w[None, :] * (nu(y) - 1) * (H + ge * m), axis=1)
def gh_pt(r, xi):   # CZ3 verbatim
    xi = np.broadcast_to(xi, r.shape); x = r / xi; out = np.empty_like(r); s = x < 1e-3
    out[~s] = (erf(x[~s] / math.sqrt(2)) - math.sqrt(2 / math.pi) * x[~s] * np.exp(-x[~s] ** 2 / 2)) / r[~s] ** 2; out[s] = math.sqrt(2 / math.pi) / 3 * r[s] / xi[s] ** 3; return out
def dWds(r, s, sg):
    R = r[:, None]; S = s[None, :]; sh = np.broadcast(R, S).shape; t = np.broadcast_to(R * S / sg ** 2, sh); pre = np.broadcast_to(sg / (math.sqrt(2 * math.pi) * S * S), sh)
    out = np.empty(sh); sm = t < 0.1; e0 = np.exp(-(R * R + S * S) / (2 * sg * sg))
    out[sm] = (2 * pre * e0 * (-(t ** 3) / 3) * (1 + t ** 2 / 10 + t ** 4 / 280))[sm]
    A = np.exp(-(R - S) ** 2 / (2 * sg * sg)); B = np.exp(-(R + S) ** 2 / (2 * sg * sg)); out[~sm] = (pre * ((1 - t) * A - (1 + t) * B))[~sm]
    return out
def outer_field(F, r, sg, smax, n=20000, smin=1e-10):
    ls = np.linspace(math.log(smin), math.log(smax), n); s = np.exp(ls); M = s * s * F(s); out = np.empty_like(r)
    for i in range(0, len(r), 64):
        rr = r[i:i + 64]; out[i:i + 64] = -np.trapz(M[None, :] * dWds(rr, s, sg) * s[None, :], ls, axis=1) / rr ** 2
    return out
def curve(sig, eta, tx):
    """l = 0 gamma_r(x) = 1 + x^2 F_R(x), x = r / r_M, form R at width sig (r_M units)."""
    F = outer_field(lambda s: monopole(gh_pt(s, sig), 1.0, eta, 160), tx, sig, tx[-1] + 12 * sig); return 1 + tx * tx * F
lab = json.load(open(os.path.join(HERE, "fn6_label.json"))); WIN = {f: [tuple(x) for x in lab["labels"][f]["passing"]] for f in A0}
P("FN6 wide binaries, reported and not graded (criteria 5f0f4a5d99); form R; kappa = 1/2 FITTED; not theory closed")
P(f"window points: canonical {WIN['canonical']}; alt {WIN['alt']}")
tx = np.geomspace(1e-3, 1e3, 241); CUR = {}
for foot, a0 in A0.items():
    rM = math.sqrt(G * MS / a0); eta = eta_newton(GPRI, a0); CUR[foot] = {}
    for p, LMW in WIN[foot]:
        L1 = LMW * (1.0 / M0) ** p * 3.0857e19; sig = L1 / rM; g = curve(sig, eta, tx); xs = S_KAU * 1e3 * AU / rM; gs = np.interp(np.log(xs), np.log(tx), g)
        CUR[foot][f"{p}|{LMW}"] = dict(L_1Msun_AU=L1 / AU, L_1Msun_pc=L1 / 3.0857e16, r_M_AU=rM / AU, sigma_rM=sig, gamma_r_at_s_kAU=dict(zip(map(str, S_KAU.tolist()), gs.tolist())), tx=tx.tolist(), g=g.tolist())
        P(f"  [{foot}] (p {p}, L_MW {LMW}): L(1 Msun) {L1 / AU:,.0f} AU = {L1 / 3.0857e16:.4f} pc = {sig:.3f} r_M (r_M {rM / AU:,.0f} AU); gamma_r at s = " + " ".join(f"{s:.0f}:{v:.3f}" for s, v in zip(S_KAU, gs)) + " kAU")
# ---- CW1's DR4 injection (cw1.py lines 229-262), the pipeline imported read only
PIPE = os.path.join(REPO, "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py"); sha = hashlib.sha256(open(PIPE, "rb").read()).hexdigest(); P(f"pipeline SHA-256 {sha} (CW1 used 7c884e0e0a4cb9cb...)")
sys.path.insert(0, os.path.dirname(PIPE)); import wide_binary_pipeline as wbp; sys.path.pop(0)
assert sys.dont_write_bytecode
rng = np.random.default_rng(20261216); NM = 1_000_000; pop_m = wbp.make_population(NM, rng, dr4=True)
with contextlib.redirect_stdout(io.StringIO()):
    MOD = {"canonical": wbp.model_medians(pop_m, wbp.A0_CAN, wbp.GRID, rng), "alt": wbp.model_medians(pop_m, wbp.A0_ALT, wbp.GRID, rng)}
PA0 = {"canonical": wbp.A0_CAN, "alt": wbp.A0_ALT}; ND = 30000; NREAL = 4
def vt_custom(pop, gv):
    vX = (gv * pop['pmx'] + pop['npmx']) * 4.74e3 * (pop['d_obs'] / 1000.); vY = (gv * pop['pmy'] + pop['npmy']) * 4.74e3 * (pop['d_obs'] / 1000.); return np.hypot(vX, vY) / pop['vc_obs']
def draw():
    pop = wbp.make_population(int(ND * 2.7), rng, dr4=True); keep = rng.permutation(len(pop['s_obs']))[:ND]; return {k: v[keep] for k, v in pop.items()}
def fit(foot, vt_d, pop):
    with contextlib.redirect_stdout(io.StringIO()): g, sg, med, sgm, cnt = wbp.run_fit(np.log10(pop['g_proj'] / PA0[foot]), vt_d, MOD[foot], rng, "fn6")
    return g, sg, med
PIPEOUT = {}
for foot, a0 in A0.items():
    PIPEOUT[foot] = {}
    for key in ["N"] + list(CUR[foot]):
        gs_ = []
        for _ in range(NREAL):
            pop = draw(); xt = (pop['g_true'] / a0) ** -0.5
            gv = np.ones_like(xt) if key == "N" else np.sqrt(np.maximum(np.interp(np.log(np.clip(xt, tx[0], tx[-1])), np.log(tx), np.array(CUR[foot][key]["g"])), 0))
            g, sg, med = fit(foot, vt_custom(pop, gv), pop); gs_.append(g)
        PIPEOUT[foot][key] = dict(gamma_inf=float(np.mean(gs_)), spread=float(np.std(gs_)), each=gs_)
        P(f"  [{foot}] {key:>9s}: DR4 pipeline gamma_inf {PIPEOUT[foot][key]['gamma_inf']:.4f} (spread {PIPEOUT[foot][key]['spread']:.4f}, {NREAL} realisations)")
RES = dict(curves=CUR, pipeline=PIPEOUT, pipeline_sha256=sha, peak_rss_GB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30, runtime_s=round(time.time() - T00, 1))
P(f"\npeak RSS {RES['peak_rss_GB']:.2f} GB; runtime {RES['runtime_s']:.0f} s")
open(os.path.join(HERE, "fn6_wb.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, "fn6_wb.json"), "w"), indent=1, default=float)
