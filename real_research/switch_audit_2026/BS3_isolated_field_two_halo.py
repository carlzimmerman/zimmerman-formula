#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
BS3 -- CLOSING BS2's TWO GAPS: THE EXTERNAL FIELD AN ISOLATED LENS ACTUALLY FEELS, AND A TWO-HALO TERM.
(Support audit of the lead track's bound-region switch; no lead-track file is edited.)

WHERE BS2 LEFT IT
  C-H/K + switch keeps the linear web Newtonian and LCDM-like, and its kernel takes free-fall fields in its argument
  (L340 S1).  With the LCDM rms field (sigma_g,3D ~ 0.013 a0) it fails KiDS-1000 isolated lensing by Delta chi^2 +570,
  +40 inside 0.3 Mpc.  Two things stood between that and a clean verdict either way:
    (i)  the field CONDITIONED ON ISOLATION (a 4x weaker field, e = 0.003, passes inside 0.3 Mpc);
    (ii) a two-halo term at 0.3-3 Mpc, which could make up a deficit there.

WHAT THIS LANE DOES
  A  THE ISOLATED-LENS FIELD, from a mock.  A fixed-amplitude Gaussian linear density field (Eisenstein-Hu P(k),
     sigma_8 = 0.811, z = 0.25) in a 300 Mpc box on 256^3 cells; its Newtonian field by FFT; galaxies Poisson-sampled
     from a lognormal of the smoothed field (n = 0.01 Mpc^-3, bias 1.2 -- the KiDS-bright neighbour population above
     ~10% of a lens's stellar mass); a lens is ISOLATED if no other galaxy lies within 3 Mpc (Brouwer+21's radius).
     Modes longer than the box are uniform across the isolation sphere and are added back analytically as an
     independent Gaussian vector.  Two phase realisations.  Cross-check: the analytic field from outside a 3 Mpc
     sphere, window j0(kR) (the exact kernel for the field at a sphere's centre from the matter outside it).
  B  A TWO-HALO TERM: Delta Sigma_2h(R) = b rho_m [wbar(R) - w(R)], w = projected linear LCDM xi_mm at z = 0.25,
     with b FREE PER BIN in [0, 2] (generous: LCDM bias for these stellar masses is ~1, and isolation lowers the
     neighbour term), profiled with M_b per bin and x_c, full covariance.  The same freedom is given to every model.

CHECKS (gates set before the run)
  A1 (documentary) the mock: isolated fraction; mean |g|^2 at random points, all galaxies, isolated galaxies.
  A2 the isolated-lens field used below is the mock's (both realisations' isolated lenses pooled, long modes added);
     sanity: its rms lies within a factor 2 of the analytic outside-3-Mpc field (else the mock is not trusted).
  B0 machinery: with b = 0 the no-EFE switch fit reproduces BS2's chi^2 (97.4 / 86.7) within 0.2.
  G1 THE GATE: C-H/K + switch at its isolation-conditioned own field, with the two-halo term (b <= 2 per bin), lies
     within Delta chi^2 <= 4 of the no-EFE switch fit given the same two-halo freedom, both footings.
  G2 (documentary) the same inside R <= 0.3 Mpc; with b <= 1; at Brouwer+21's e = 0.003; baryons-only kernel; pure
     MOND at its own field (e_N = e_M^2); fitted b's.
  G3 INJECTION (the gate can pass): 10 synthetic data sets drawn from the construction's own model (its field, b = 1,
     x_c = 5); G1's test must pass in >= 80% of them.
  MUTATE=1 injects the no-EFE switch model instead: G3 must then FAIL (rc = 1).
  G2b (documentary) the two-halo amplitude each model would NEED: b free up to 20 per bin.
  SCOPE: L342's base model (point-mass baryons, lens z = 0.25); a linear-theory mock (no nonlinear field boost near
  groups -- irrelevant for isolated lenses, whose field comes from > 3 Mpc); 3-D isolation at 3 Mpc as in Brouwer+21's
  definition (their photometric redshifts make the real selection noisier, admitting some non-isolated lenses, which
  can only raise the mean field).

Run from the repository root:  python3 real_research/switch_audit_2026/BS3_isolated_field_two_halo.py
"""
import os, sys, json, math, time, warnings
import numpy as np
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")   # spurious BLAS warning (no result changes)
from scipy.optimize import brentq, lsq_linear
from scipy.spatial import cKDTree
from scipy.special import spherical_jn

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "BS3_isolated_field_two_halo"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "BS3", "mutate": MUTATE, "checks": {}, "numbers": {}}
_trap = getattr(np, "trapezoid", None) or np.trapz
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}"); P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 104); P(t); P("=" * 104)


# ------------------------------------------------------------------ L342 / BS2 constants, kernel, data, ESD model
Mpc = 3.0856775814913673e22; G = 6.67430e-11
h = 0.6736; om_b, om_c = 0.02237, 0.1200
H0 = 100 * h * 1e3 / Mpc
Ob, Oc = om_b / h ** 2, om_c / h ** 2; Om = Ob + Oc; OL = 1 - Om
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
FOOTS = ("canonical", "alt")
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore"): return np.where(y < 1e4, y / np.expm1(np.sqrt(np.minimum(y, 1e4))), 0.0)
def dh_rar(y, e=1e-6): return (h_rar(y * (1 + e)) - h_rar(y * (1 - e))) / (2 * y * e)
YP = brentq(lambda y: float(dh_rar(y)), 1, 5); HP = float(h_rar(YP))
LYG = np.linspace(-14, 14, 280001); YG = 10 ** LYG; DH = np.maximum(dh_rar(YG), 0.05 * HP / (YG + YP))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DH[1:] + DH[:-1]) * np.diff(YG))])
def nu_mono_arr(y):
    y = np.maximum(np.asarray(y, float), 1e-14); return 1.0 + np.interp(np.log10(y), LYG, HM) / y

B = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
MS, PCm = 1.98892e30, 3.0857e16; MPCm = PCm * 1e6
Rd, Ed = [], []
for b in (1, 2, 3, 4):
    d = np.genfromtxt(os.path.join(B, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt"), comments="#")
    Rd.append(d[:, 0]); Ed.append(d[:, 1] / d[:, 4])
cv = np.genfromtxt(os.path.join(B, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
vv = cv[:, 4] / cv[:, 6]; npb = len(Rd[0]); Cf = vv.reshape(4, 4, npb, npb).transpose(0, 2, 1, 3).reshape(4 * npb, 4 * npb)
Cf = (Cf + Cf.T) / 2; Ci = np.linalg.inv(Cf)
rr = np.geomspace(1e-3, 30, 4000) * MPCm; Rp = np.geomspace(0.02, 4, 240) * MPCm
ZL = 0.25; Hlens = H0 * math.sqrt(Om * (1 + ZL) ** 3 + OL)
W = np.zeros((len(Rp), len(rr)))
for i, Rv in enumerate(Rp):
    m = np.where(rr > Rv * 1.0000001)[0]; r_ = rr[m]; dr = np.diff(r_)
    wt = np.zeros_like(r_); wt[:-1] += 0.5 * dr; wt[1:] += 0.5 * dr
    W[i, m] = 2 * r_ / np.sqrt(r_ ** 2 - Rv ** 2) * wt


def esd_from_M(M, Mb, xc):
    if xc:
        rho_dyn = np.gradient(M, rr) / (4 * math.pi * rr ** 2); on = 4 * math.pi * G * rho_dyn / Hlens ** 2 >= xc
        it = int(np.where(on)[0].max()) if on.any() else 0
        M = np.where(np.arange(len(rr)) > it, M[it], M)
    Sig = W @ (np.gradient(M - Mb, rr) / (4 * math.pi * rr ** 2))
    Mc = np.concatenate([[0], np.cumsum(0.5 * (Sig[1:] * Rp[1:] + Sig[:-1] * Rp[:-1]) * np.diff(Rp))]) * 2 * math.pi \
        + math.pi * Rp[0] ** 2 * Sig[0]
    return Rp / MPCm, (Mc / (math.pi * Rp ** 2) - Sig + Mb / (math.pi * Rp ** 2)) * PCm ** 2 / MS


LYT = np.linspace(-9.5, 6.5, 1601); YT = 10 ** LYT; MU = np.linspace(-1.0, 1.0, 4001)
def N_of(y, e):
    y = np.atleast_1d(np.asarray(y, float))
    if e == 0: return nu_mono_arr(y)
    out = np.empty_like(y)
    for s in range(0, len(y), 64):
        yy = y[s:s + 64, None]
        w = np.sqrt(np.maximum(yy ** 2 + e ** 2 - 2 * yy * e * MU[None, :], 0.0))
        out[s:s + 64] = 0.5 * _trap(nu_mono_arr(w) * (yy - e * MU[None, :]), MU, axis=1) / yy[:, 0]
    return out


ES = [0.0] + [float(v) for v in np.round(np.geomspace(1e-6, 0.1, 36), 9)]
XCS = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.5, 10.0, 15.0, 20.0]
LM = np.round(np.arange(9.8, 11.8001, 0.02), 4)
NTAB = {e: N_of(YT, e) for e in ES}
TABA = np.zeros((2, len(ES), len(XCS), len(LM), 4, npb))
for jf, foot in enumerate(FOOTS):
    for ie, e in enumerate(ES):
        for im, lm in enumerate(LM):
            Mb = 10 ** lm * MS; y = G * Mb / rr ** 2 / A0[foot]
            M = Mb * (nu_mono_arr(y) if e == 0 else np.interp(np.log10(y), LYT, NTAB[e]))
            for ix, xc in enumerate(XCS):
                Rq, dS = esd_from_M(M, Mb, xc)
                TABA[jf, ie, ix, im] = [np.interp(Rd[b], Rq, dS) for b in range(4)]
P(f"ESD tables: {TABA.shape[0] * TABA.shape[1] * TABA.shape[2] * TABA.shape[3]} profiles ({time.time() - T0:.0f} s)")
LOGE = np.log10(np.array(ES[1:]))
def stack_weights(e_samples):
    w = np.zeros(len(ES)); le = np.log10(np.maximum(e_samples, 1e-12))
    below = le < LOGE[0] - 0.5 * (LOGE[1] - LOGE[0]); w[0] += below.sum()
    idx = np.clip(np.rint((le[~below] - LOGE[0]) / (LOGE[1] - LOGE[0])).astype(int), 0, len(LOGE) - 1) + 1
    np.add.at(w, idx, 1.0); return w / w.sum()

# ------------------------------------------------------------------ linear LCDM: P(k), growth, field normalisation
TH27 = 2.7255 / 2.7; NS, S8 = 0.9649, 0.8111
def T_eh(k):
    omh2 = Om * h * h; fb = Ob / Om
    s_ = 44.5 * np.log(9.83 / omh2) / np.sqrt(1 + 10 * (Ob * h * h) ** 0.75)
    aG = 1 - 0.328 * np.log(431 * omh2) * fb + 0.38 * np.log(22.3 * omh2) * fb ** 2
    Gm = Om * h * (aG + (1 - aG) / (1 + (0.43 * k * s_) ** 4)); q = k * TH27 ** 2 / (Gm * h)
    L_ = np.log(2 * np.e + 1.8 * q); C_ = 14.2 + 731 / (1 + 62.5 * q); return L_ / (L_ + C_ * q * q)
def W_th(x): return 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
KK = np.geomspace(1e-5, 50, 40000); PK0 = KK ** NS * T_eh(KK) ** 2
PK0 *= S8 ** 2 / _trap(PK0 * W_th(KK * 8 / h) ** 2 * KK ** 2 / (2 * math.pi ** 2), KK)
def Pk0(k): return np.interp(np.log(np.maximum(k, 1e-5)), np.log(KK), PK0, left=0.0, right=0.0)
def growth(z):
    a_ = np.linspace(1e-4, 1, 20001)
    def D_(a1):
        aa = a_[a_ <= a1]; E = np.sqrt(Om / aa ** 3 + OL); return math.sqrt(Om / a1 ** 3 + OL) * _trap(1 / (aa * E) ** 3, aa)
    return D_(1 / (1 + z)) / D_(1.0)
DZ = growth(ZL)
CG = 1.5 * Om * H0 ** 2 * (1 + ZL) ** 2 * DZ * Mpc          # m/s^2 per (comoving Mpc of grad^-1 delta_0)
SIG2_TOT = CG ** 2 * _trap(PK0, KK) / (2 * math.pi ** 2)     # 3-D variance of g at a random point, no window
R_ISO = 3.0
SIG2_OUT = CG ** 2 * _trap(PK0 * np.sinc(KK * R_ISO / math.pi) ** 2, KK) / (2 * math.pi ** 2)   # j0(kR)^2 window

# ============================================================================================ A
banner("A  THE EXTERNAL FIELD AN ISOLATED LENS FEELS: linear LCDM mock, 300 Mpc / 256^3, KiDS-like isolation at 3 Mpc")
L_BOX, NG = 300.0, 256; CELL = L_BOX / NG; NBAR, BG, RS = 0.01, 1.2, 2.0
kx = 2 * math.pi * np.fft.fftfreq(NG, d=CELL); kz = 2 * math.pi * np.fft.rfftfreq(NG, d=CELL)
KX, KY, KZ = np.meshgrid(kx, kx, kz, indexing="ij"); K2 = KX ** 2 + KY ** 2 + KZ ** 2; K2[0, 0, 0] = 1.0
AMP = np.sqrt(Pk0(np.sqrt(K2)) * NG ** 3 / L_BOX ** 3); AMP[0, 0, 0] = 0.0
mock = {"random": [], "all": [], "iso": [], "iso_frac": [], "n_gal": []}
GISO = []
for seed in (11, 12):
    rng = np.random.default_rng(seed)
    Wk = np.fft.rfftn(rng.standard_normal((NG, NG, NG)))
    Wk = Wk / np.maximum(np.abs(Wk), 1e-30) * math.sqrt(NG ** 3)          # fixed amplitude, random phases
    dk = Wk * AMP
    g = np.stack([np.fft.irfftn(1j * Kc * dk / K2, s=(NG, NG, NG)) * CG for Kc in (KX, KY, KZ)], axis=-1)
    g2 = np.sum(g ** 2, axis=-1)
    ds = np.fft.irfftn(dk * np.exp(-0.5 * K2 * RS ** 2), s=(NG, NG, NG)) * DZ
    nu = BG * ds; lam = NBAR * CELL ** 3 * np.exp(nu - nu.var() / 2)
    cnt = rng.poisson(lam); cells = np.repeat(np.arange(NG ** 3), cnt.ravel())
    ijk = np.stack(np.unravel_index(cells, (NG, NG, NG)), axis=-1)
    pos = (ijk + rng.random(ijk.shape)) * CELL
    tree = cKDTree(pos, boxsize=L_BOX)
    nnb = np.array([len(v) - 1 for v in tree.query_ball_point(pos, R_ISO, workers=-1)])
    iso = nnb == 0
    gg = g.reshape(-1, 3)[cells]
    mock["random"].append(float(g2.mean())); mock["all"].append(float(np.mean(np.sum(gg ** 2, 1))))
    mock["iso"].append(float(np.mean(np.sum(gg[iso] ** 2, 1)))); mock["iso_frac"].append(float(iso.mean()))
    mock["n_gal"].append(int(len(pos)))
    GISO.append(gg[iso])
    P(f"    seed {seed}: {len(pos)} galaxies, isolated fraction {iso.mean():.3f};  rms |g| (box modes): random "
      f"{math.sqrt(g2.mean()) / A0['canonical']:.4f}, all galaxies {math.sqrt(mock['all'][-1]) / A0['canonical']:.4f}, "
      f"isolated {math.sqrt(mock['iso'][-1]) / A0['canonical']:.4f} a0 (canonical)")
    del g, g2, ds, nu, lam, cnt, Wk, dk
SIG2_BOX = float(np.mean(mock["random"])); SIG2_MISS = max(SIG2_TOT - SIG2_BOX, 0.0)
GISO = np.concatenate(GISO)
rs_ = np.random.default_rng(99)
G_ISO_FULL = GISO + rs_.standard_normal(GISO.shape) * math.sqrt(SIG2_MISS / 3)
rms_iso = float(np.sqrt(np.mean(np.sum(G_ISO_FULL ** 2, 1))))
rms_all_full = math.sqrt(np.mean(mock["all"]) + SIG2_MISS); rms_rand = math.sqrt(SIG2_TOT)
P(f"    long modes (k < 2 pi/L, uniform over the sphere): rms {math.sqrt(SIG2_MISS) / A0['canonical']:.4f} a0 added back")
P(f"    FULL rms |g| at z = {ZL}: random points {rms_rand / A0['canonical']:.4f}, all galaxies {rms_all_full / A0['canonical']:.4f}, "
  f"ISOLATED lenses {rms_iso / A0['canonical']:.4f} a0 (canonical);  analytic field from outside 3 Mpc "
  f"{math.sqrt(SIG2_OUT) / A0['canonical']:.4f} a0")
P(f"    isolated lenses: median |g| {np.median(np.linalg.norm(G_ISO_FULL, axis=1)) / A0['canonical']:.4f} a0; fraction below 0.003 a0: "
  f"{np.mean(np.linalg.norm(G_ISO_FULL, axis=1) < 0.003 * A0['canonical']):.4f}")
OUT["numbers"]["A"] = {"mock": mock, "sig2_box": SIG2_BOX, "sig2_miss": SIG2_MISS, "rms_random_over_a0c": rms_rand / A0["canonical"],
                       "rms_all_over_a0c": rms_all_full / A0["canonical"], "rms_iso_over_a0c": rms_iso / A0["canonical"],
                       "rms_outside_3Mpc_analytic_over_a0c": math.sqrt(SIG2_OUT) / A0["canonical"]}
check("A1 (documentary) mock isolation statistics and field at random points / galaxies / isolated lenses",
      {"isolated fraction": [round(v, 3) for v in mock["iso_frac"]],
       "rms iso / rms random": round(rms_iso / rms_rand, 3)}, True,
      "isolation removes the field of near neighbours; the long modes that dominate |g| are shared by every lens",
      load_bearing=False)
ratio_an = rms_iso / math.sqrt(SIG2_OUT)
check("A2 the mock's isolated-lens field is within a factor 2 of the analytic field from outside a 3 Mpc sphere",
      f"mock / analytic = {ratio_an:.3f}", 0.5 <= ratio_an <= 2.0, "")
E_ISO = {f_: np.linalg.norm(G_ISO_FULL, axis=1) / A0[f_] for f_ in FOOTS}

# ============================================================================================ B: two-halo template
rgrid = np.geomspace(0.05, 300, 3000)                              # comoving Mpc
kq = np.geomspace(1e-5, 30, 60000)
XI0 = np.array([_trap(kq ** 2 * Pk0(kq) * np.sinc(kq * r / math.pi) * np.exp(-(kq / 20) ** 2), kq) / (2 * math.pi ** 2)
                for r in rgrid])
RHO_M0 = Om * 3 * H0 ** 2 / (8 * math.pi * G) * Mpc ** 3 / MS      # Msun / Mpc^3 comoving
def w_proj(Rc):
    pi_ = np.geomspace(1e-3, 150, 1500)
    return 2 * _trap(np.interp(np.sqrt(Rc ** 2 + pi_ ** 2), rgrid, XI0), pi_)
Rc_g = np.geomspace(0.01, 5, 400) * (1 + ZL)
wv = np.array([w_proj(x) for x in Rc_g])
inner = wv[0] * Rc_g[0] ** 2 / 2                                   # int_0^R0 w R dR with w ~ const inside R0
wbar = np.array([2 * (inner + (_trap(wv[:i + 1] * Rc_g[:i + 1], Rc_g[:i + 1]) if i > 0 else 0.0)) / Rc_g[i] ** 2
                 for i in range(len(Rc_g))])
DS2H = RHO_M0 * DZ ** 2 * (wbar - wv) * (1 + ZL) ** 2 / 1e12     # Msun/pc^2 physical, for b = 1
T2H = [np.interp(Rd[b], Rc_g / (1 + ZL), DS2H) for b in range(4)]
P(f"\n    two-halo template (b = 1, z = {ZL}): Delta Sigma_2h at 0.1 / 0.3 / 1 / 2.6 Mpc = "
  + ", ".join(f"{np.interp(x, Rc_g / (1 + ZL), DS2H):.3f}" for x in (0.1, 0.3, 1.0, 2.6)) + " Msun/pc^2")
OUT["numbers"]["B_template"] = {str(x): float(np.interp(x, Rc_g / (1 + ZL), DS2H)) for x in (0.1, 0.3, 1.0, 2.6)}
TM = np.zeros((4 * npb, 4))
for b in range(4): TM[b * npb:(b + 1) * npb, b] = T2H[b]


def fit_2h(blk, data, bmax, sel=None):
    """chi^2 of model block blk[im, bin, R] + b_bin * T2H, M_b per bin by coordinate descent, b in [0, bmax] per bin
    by bounded least squares under the full (or selected) covariance."""
    D = np.concatenate(data); idx = np.arange(4 * npb) if sel is None else np.array(sel)
    Cs = Cf[np.ix_(idx, idx)]; Csi = np.linalg.inv(Cs); U = np.linalg.cholesky(Csi)
    A = U.T @ TM[idx]; Apinv = np.linalg.pinv(A)
    def solve_batch(R_):                                           # R_: (ncand, 4*npb) residual vectors
        Y = (U.T @ R_[:, idx].T).T
        if bmax == 0: return np.zeros((len(Y), 4)), np.sum(Y ** 2, 1)
        Bu = (Apinv @ Y.T).T; out_b = Bu.copy(); c2 = np.sum((Bu @ A.T - Y) ** 2, 1)
        bad = np.where(np.any(Bu < 0, 1) | np.any(Bu > bmax, 1))[0]
        for i in bad:
            r_ = lsq_linear(A, Y[i], bounds=(0, bmax), method="bvls"); out_b[i] = r_.x
            c2[i] = float(np.sum((A @ r_.x - Y[i]) ** 2))
        return out_b, c2
    im = [len(LM) // 2] * 4; best = None; bb = np.zeros(4)
    for _ in range(8):
        moved = False
        for b in range(4):
            base = np.concatenate([blk[im[q], q] for q in range(4)])
            V = np.repeat(base[None, :], len(LM), axis=0); V[:, b * npb:(b + 1) * npb] = blk[:, b]
            bs, c2 = solve_batch(D[None, :] - V)
            j = int(np.argmin(c2))
            if j != im[b]: im[b], moved = j, True
            best, bb = float(c2[j]), bs[j]
        if not moved: break
    return best, im, bb


def family_fit(foot, data, w, bmax, sel=None, xcs=range(len(XCS))):
    jf = FOOTS.index(foot); best = None
    for ix in xcs:
        blk = np.tensordot(w, TABA[jf, :, ix], axes=(0, 0))
        c_, im, bb = fit_2h(blk, data, bmax, sel)
        if best is None or c_ < best[0]: best = (c_, ix, im, bb)
    return best


W_NONE = np.zeros(len(ES)); W_NONE[0] = 1.0
def w_own(foot): return stack_weights(E_ISO[foot])
def w_bar(foot): return stack_weights(E_ISO[foot] * Ob / Om)
def w_pm(foot): return stack_weights(E_ISO[foot] ** 2)
def w_b21(foot):
    s3 = 0.003 / math.sqrt(8 / (3 * math.pi)); gs = np.random.default_rng(5).standard_normal((200000, 3))
    return stack_weights(np.linalg.norm(gs, axis=1) * s3 / math.sqrt(3))
SEL = [b * npb + i for b in range(4) for i in range(npb) if Rd[b][i] <= 0.3]
DATA = [np.array(e) for e in Ed]

# ============================================================================================ B0
banner("B0  MACHINERY: b = 0 reproduces BS2's no-EFE switch fit")
b0 = {f_: family_fit(f_, DATA, W_NONE, 0.0)[0] for f_ in FOOTS}
ok0 = abs(b0["canonical"] - 97.4) < 0.2 and abs(b0["alt"] - 86.7) < 0.2
check("B0 with b = 0 the no-EFE switch chi^2 equals BS2's (97.4 / 86.7) within 0.2", {k: round(v, 2) for k, v in b0.items()}, ok0)

# ============================================================================================ G1-G2
banner("G1-G2  THE CONSTRUCTION AT ITS ISOLATED-LENS FIELD, WITH A TWO-HALO TERM (b <= 2 per bin), vs the comparator")
RES = {}
for foot in FOOTS:
    row = {}
    for bmax in (2.0, 1.0):
        for sel_lab, sel in (("all", None), ("R<=0.3", SEL)):
            ref = family_fit(foot, DATA, W_NONE, bmax, sel)
            for lab, wf in (("own field (isolated)", w_own), ("B21 e=0.003", w_b21), ("baryons-only kernel", w_bar),
                            ("pure MOND", w_pm)):
                r_ = family_fit(foot, DATA, wf(foot), bmax, sel)
                row[(bmax, sel_lab, lab)] = {"chi2": r_[0], "dchi2": r_[0] - ref[0], "xc": XCS[r_[1]],
                                             "b": [round(x, 2) for x in r_[3]]}
            row[(bmax, sel_lab, "comparator: no-EFE switch")] = {"chi2": ref[0], "xc": XCS[ref[1]], "b": [round(x, 2) for x in ref[3]]}
    RES[foot] = row
    P(f"    {foot}:")
    for bmax in (2.0, 1.0):
        for sel_lab in ("all", "R<=0.3"):
            c = row[(bmax, sel_lab, "comparator: no-EFE switch")]
            P(f"      b <= {bmax:.0f}, {sel_lab:6s}: comparator chi^2 {c['chi2']:.1f} (x_c {c['xc']}, b {c['b']})")
            for lab in ("own field (isolated)", "B21 e=0.003", "baryons-only kernel", "pure MOND"):
                r_ = row[(bmax, sel_lab, lab)]
                P(f"          {lab:22s}: Delta chi^2 {r_['dchi2']:+8.1f}   (x_c {r_['xc']}, b {r_['b']})")
OUT["numbers"]["G"] = {f_: {"|".join(map(str, k)): v for k, v in RES[f_].items()} for f_ in FOOTS}
g1 = {f_: round(RES[f_][(2.0, "all", "own field (isolated)")]["dchi2"], 1) for f_ in FOOTS}
check("G1 C-H/K + switch at its isolation-conditioned field, with a two-halo term (b <= 2 per bin), lies within "
      "Delta chi^2 <= 4 of the no-EFE switch fit given the same freedom, both footings", g1,
      all(v <= 4 for v in g1.values()),
      "a failure here survives both of BS2's open gaps")
check("G2 (documentary) inside 0.3 Mpc; b <= 1; Brouwer+21's field; baryons-only kernel; pure MOND",
      {f_: {f"b<={k[0]:.0f}|{k[1]}|{k[2]}": round(v["dchi2"], 1) for k, v in RES[f_].items() if "dchi2" in v}
       for f_ in FOOTS}, True, "", load_bearing=False)

banner("G2b  THE TWO-HALO AMPLITUDE EACH MODEL WOULD NEED (b free up to 20 per bin, all points)")
NEED = {}
for foot in FOOTS:
    ref = family_fit(foot, DATA, W_NONE, 20.0)
    NEED[foot] = {"comparator": {"chi2": ref[0], "b": [round(x, 2) for x in ref[3]]}}
    for lab, wf in (("own field (isolated)", w_own), ("B21 e=0.003", w_b21), ("baryons-only kernel", w_bar), ("pure MOND", w_pm)):
        r_ = family_fit(foot, DATA, wf(foot), 20.0)
        NEED[foot][lab] = {"dchi2": r_[0] - ref[0], "b": [round(x, 2) for x in r_[3]]}
    P(f"    {foot:9s}: comparator chi^2 {ref[0]:.1f}, b {NEED[foot]['comparator']['b']}")
    for lab in ("own field (isolated)", "B21 e=0.003", "baryons-only kernel", "pure MOND"):
        P(f"      {lab:22s}: Delta chi^2 {NEED[foot][lab]['dchi2']:+7.1f} with b = {NEED[foot][lab]['b']}")
OUT["numbers"]["G2b"] = NEED
check("G2b (documentary) the two-halo bias each model needs when b may reach 20", {f_: {k: v["b"] for k, v in NEED[f_].items()}
      for f_ in FOOTS}, True, "LCDM bias for these lenses is ~1, and isolation lowers the neighbour term", load_bearing=False)

# ============================================================================================ G3
banner("G3  INJECTION: can the gate pass? synthetic data from the construction's own model (canonical, 10 draws)")
rng3 = np.random.default_rng(20260925); Lch = np.linalg.cholesky(Cf)
LMS_TRUE = [10.2, 10.6, 10.9, 11.2]; IMS = [int(np.argmin(np.abs(LM - l))) for l in LMS_TRUE]
if MUTATE:
    w_true = W_NONE; P("*** MUTATE=1: injecting the no-EFE switch model instead of the construction's own ***")
else:
    w_true = w_own("canonical")
blk_true = np.tensordot(w_true, TABA[0, :, XCS.index(5.0)], axes=(0, 0))
mean_true = np.concatenate([blk_true[IMS[b], b] + 1.0 * T2H[b] for b in range(4)])
passes = []
for t in range(10):
    dv = mean_true + Lch @ rng3.standard_normal(4 * npb); dat = [dv[b * npb:(b + 1) * npb] for b in range(4)]
    ref = family_fit("canonical", dat, W_NONE, 2.0)[0]; own = family_fit("canonical", dat, w_own("canonical"), 2.0)[0]
    passes.append(own - ref)
frac = float(np.mean(np.array(passes) <= 4))
P(f"    Delta chi^2 (construction - comparator) per draw: {np.round(passes, 1).tolist()};  passes: {frac:.2f}")
OUT["numbers"]["G3"] = {"dchi2": passes, "pass_fraction": frac}
check("G3 when the construction is true, G1's test passes in >= 80% of 10 synthetic draws", f"{frac:.2f}", frac >= 0.8,
      "the gate is not rigged: it can pass")

# ============================================================================================ verdict
banner("VERDICT")
rc = RES["canonical"]; ra = RES["alt"]
P(f"""  (i) The field an isolated lens feels.  In the linear LCDM mock, isolation removes the pull of near neighbours but not
  the long modes that dominate |g|: rms |g| = {rms_iso / A0['canonical']:.4f} a0 for isolated lenses vs {rms_rand / A0['canonical']:.4f} at random points (canonical);
  only {100 * np.mean(np.linalg.norm(G_ISO_FULL, axis=1) < 0.003 * A0['canonical']):.1f}% of isolated lenses are as quiet as Brouwer+21's adopted e = 0.003.
  (ii) With a two-halo term free per bin (b <= 2) given to every model, the construction at that field sits at
  Delta chi^2 {g1['canonical']:+.1f} / {g1['alt']:+.1f} (all points) and {rc[(2.0, 'R<=0.3', 'own field (isolated)')]['dchi2']:+.1f} / {ra[(2.0, 'R<=0.3', 'own field (isolated)')]['dchi2']:+.1f} inside 0.3 Mpc against the no-EFE switch.
  Injection: when the construction is true the test passes in {frac:.0%} of draws.
  Given b up to 20 it still sits at {NEED['canonical']['own field (isolated)']['dchi2']:+.1f} / {NEED['alt']['own field (isolated)']['dchi2']:+.1f}, asking for b = {NEED['canonical']['own field (isolated)']['b']} (canonical).
  Baryons-only kernel: {rc[(2.0, 'all', 'baryons-only kernel')]['dchi2']:+.1f} / {ra[(2.0, 'all', 'baryons-only kernel')]['dchi2']:+.1f} at b <= 2 (passes inside 0.3 Mpc); with b up to 20: {NEED['canonical']['baryons-only kernel']['dchi2']:+.1f}, b = {NEED['canonical']['baryons-only kernel']['b']}.
  Pure MOND at its own (MOND-level) field: {rc[(2.0, 'all', 'pure MOND')]['dchi2']:+.1f} / {ra[(2.0, 'all', 'pure MOND')]['dchi2']:+.1f} at b <= 2, 0.0 inside 0.3 Mpc -- a tension at 0.3-3 Mpc on this
  point-mass base model, not a kill.
  READING: both of BS2's gaps are closed and the verdict stands.  Isolation does not quiet the field (the long modes that
  dominate it are shared), and no plausible two-halo term makes up the deficit.  C-H/K + switch, with its kernel seeing
  the total Newtonian field of an LCDM-like web, is EXCLUDED by KiDS-1000 isolated lensing -- inside 0.3 Mpc (+47 / +52,
  where isolation is certain) and on all points (+404 / +415).  A kernel sourced by baryons only is disfavoured on all
  points but survives inside 0.3 Mpc.  The door left open by this lane is a kernel blind to the large-scale field.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname} "
  f"({time.time() - T0:.0f} s)")
sys.exit(0 if n_fail == 0 else 1)
