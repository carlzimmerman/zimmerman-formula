#!/usr/bin/env python3
"""
L29 -- is L9's surviving late-roll region already excluded by the measured S_8?
==============================================================================
L9 (`L9_late_transition.py`) found the FIRST mechanism in this programme to clear the gate it was proposed
against: a late-time roll in the gravitational coupling, g(z_BBN) = 1 -> g(0) = F ~ 1.7-1.8, which survives
nucleosynthesis, the microwave background, structure growth AND the full expansion history including the
absolute BAO ruler, while still delivering the cluster enhancement at the X-COP redshifts.  Its surviving
region is narrow and it makes a sharp prediction:

    canonical  z_t in [0.0033, 0.374], W in [0.376, 0.565]   146/3721 refined
    alt        z_t in [0.0033, 0.441], W in [0.336, 0.604]   269/3721 refined
    sigma_8 = 0.845-0.861,  H0 = 68-72,  Omega_m = 0.27-0.31,  Omega_Lambda = 0.25-0.32,  f(0) = 0.57-0.64

sigma_8 = 0.845-0.861 is HIGH: the concordance value is 0.811 and the S_8 tension runs the OTHER way -- the
cosmic-shear surveys prefer LESS structure than the microwave background, not more.  This lane asks whether
the prediction is therefore already dead.

WHAT IS BEING COMPARED, and the one thing that must not be got wrong.  sigma_8 alone is not what lensing
measures; the lensing observable is S_8 = sigma_8 sqrt(Omega_m/0.3).  L9's survivors have Omega_m = 0.27-0.31,
BELOW the concordance 0.315, so the conversion pulls the prediction DOWN and part of the apparent conflict
evaporates before any data are touched.  That is priced first, at each grid point, never as a range against a
point.

TWO READINGS OF THE SAME MODEL, both run, both reported.
  (i)  NAIVE.  S_8 = sigma_8 sqrt(Omega_m/0.3) from each survivor's own (sigma_8, Omega_m).  This is the
       reading L9's quoted prediction implies, and it is the reading most FAVOURABLE to the model: it assumes
       that whatever keeps galaxies at G_0 also removes the roll from the cosmic-shear signal entirely.
  (ii) LENSING-CONSISTENT.  In MODEL A the roll multiplies the Poisson source, so with no slip it multiplies
       the Weyl potential that lenses light: k^2(Phi+Psi)/2 = -(3/2) g(a) omega_m (100/c)^2 delta/a.  The
       physical density omega_m is CMB-fixed and identical between model and LambdaCDM, so the entire ratio
       of shear power to LambdaCDM is [g(z) D_model(z)/D_LCDM(z)]^2 weighted by the lensing kernel.  This is
       a genuine Limber calculation here, not an estimate.  L9 explicitly did NOT run this gate ("lensing
       versus dynamics ... that gate is not run here"); it is the gate this lane adds.
  Reading (ii) is the self-consistent one for a spatially uniform g(z), which is what MODEL A is.  Reading (i)
  is kept because a screening that removed g from the shear signal is not excluded HERE -- it is excluded by
  L6/L9's T8 on a different argument, and this lane does not lean on that.

  C0 [control]  the machinery reproduces L9's published surviving region to the digit: the counts, the
                (z_t, W) box, and the (sigma_8, H0, Omega_m, Omega_Lambda) margins on BOTH footings;
  C1 [control]  the S_8 conversion reproduces the concordance value AND the known size of the S_8 tension
                between the microwave background and cosmic shear, on the published numbers;
  C2 [2 sigma]  is ANY part of L9's region compatible with cosmic-shear S_8 at 2 sigma;
  C3 [3 sigma]  is ANY part compatible at 3 sigma;
  C4 [H0+S8]    can a SINGLE surviving point fit a high H0 and an acceptable S_8 together;
  C5 [growth]   L9's growth gate replaced by the actual measurements: absolute RSD chi^2 with a p-value, plus
                S_8, rather than L9's internal Delta chi^2 <= 9 against LambdaCDM;
  C6 [kappa]    does the roll's cosmology interact with the framework's own coefficient question, which
                kappa_closure/k03 showed is degenerate with the H0 tension through a0 = kappa c sqrt(G rho_L);
  C7 [verdict]  the mechanism survives current data.
Both a0 footings throughout.  FAIL marks a requirement the mechanism does not meet.  A PASS on C7 would leave
the programme with one live cosmological mechanism and would deserve a preregistration; a FAIL closes it.

WHAT THIS LANE IS NOT TESTING.  L9's mechanism does NOT solve the cluster problem.  It clears the
cosmological gates but cannot supply the cluster-versus-galaxy contrast (L9 T8: a uniform g(z) gives 0.97
between z = 0.0037 and z = 0.090 against a required 2.2-5.1), which is separate and still fatal.  Nothing
here is a rescue; this asks only whether the one mechanism that cleared its own gate is even ALLOWED by data.

PROVENANCE OF THE MACHINERY.  The background, growth, BAO, acoustic-scale and h-refit code below is COPIED
VERBATIM from `L9_late_transition.py` so that C0 is a reproduction and not a re-derivation.  Any divergence
in C0 is a bug in this file, not a new result.
"""
import numpy as np, math, json, os, sys
np.seterr(over="ignore", invalid="ignore", divide="ignore")
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("=" * 124)
print("L29 -- is L9's surviving late-roll region already excluded by the measured S_8?")
print("=" * 124, flush=True)

# ============================================================ MACHINERY COPIED VERBATIM FROM L9 ============
C_KMS   = 299792.458
Z_BBN   = 4.0e8          # T ~ 0.08 MeV, deuterium formation
Z_REC   = 1089.92        # Planck 2018 (last scattering)
Z_DRAG  = 1059.94        # Planck 2018 (baryon drag), for the BAO standard ruler r_drag
THETA_S = 0.0104109      # Planck 2018 100 theta_* = 1.04109 +/- 0.00031
OM_M    = 0.14304        # omega_m = Omega_m h^2, Planck 2018 (PHYSICAL; fixed at z >> z_t)
OM_B    = 0.02237        # omega_b, Planck 2018 / BBN deuterium
OM_G    = 2.4728e-5      # omega_gamma from T_cmb = 2.7255 K
OM_R    = OM_G*(1 + 0.2271*3.046)
H_FID   = 0.6736         # measured H0/100 (Planck)
S8_FID  = 0.8111         # Planck 2018 sigma_8
NS      = 0.965          # Planck 2018 scalar tilt (used only by the Limber shape below)
BBN_TOL = 0.20
CMB_TOL = 0.10
Z_CLUST_MAX = 0.090
H_LO, H_HI  = 0.60, 0.80
Q0_LO, Q0_HI = -0.75, -0.35
RSD = np.array([[0.02, 0.428, 0.0465],   # Huterer+2017   SNe peculiar velocities
                [0.15, 0.490, 0.145 ],   # Howlett+2015   SDSS MGS
                [0.38, 0.497, 0.045 ],   # Alam+2017      BOSS DR12
                [0.51, 0.459, 0.038 ],   # Alam+2017      BOSS DR12
                [0.70, 0.473, 0.041 ],   # Bautista+2021  eBOSS LRG
                [0.85, 0.315, 0.095 ],   # de Mattia+2021 eBOSS ELG
                [1.48, 0.462, 0.045 ]])  # Neveux+2020    eBOSS QSO
BAO = [("DM", 0.380, 10.234, 0.151), ("DH", 0.380, 24.98, 0.58),
       ("DM", 0.510, 13.366, 0.179), ("DH", 0.510, 22.31, 0.42),
       ("DM", 0.700, 17.86,  0.33 ), ("DH", 0.700, 19.33, 0.53),
       ("DM", 1.480, 30.69,  0.80 ), ("DH", 1.480, 13.26, 0.55),
       ("DM", 2.330, 37.6,   1.9  ), ("DH", 2.330,  8.93, 0.28),
       ("DV", 0.106,  2.976, 0.133), ("DV", 0.150,  4.47, 0.17 )]

def Delta(s):
    s = np.asarray(s, float); d = np.where(s > 0, s/np.expm1(np.sqrt(np.maximum(s, 1e-300))), 0.0)
    return np.where(s > 2.540, 0.6476, d)
CLJ = json.load(open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/cluster_measurement_audit_2026/results.json")))
A0 = CLJ["a0_m_s2"]
FREQ = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]; per = {}
    for rw in CLJ["rows"]:
        if rw.get("footing", "canonical") != foot: continue
        per.setdefault(rw["cluster"], []).append((float(rw["r_kpc"]), float(rw["g_baryon_over_a0"])*a0,
                                                  float(rw["g_hse_over_a0"])*a0))
    Eout = []
    for name, pts in per.items():
        p = np.array(sorted(pts)); gb, gh = p[:, 1], p[:, 2]
        Eout.append((gh/(gb + a0*Delta(gb/a0)))[-1])
    FREQ[foot] = dict(F=float(np.median(Eout)))

def sigma_x(x, xt, W):
    return (1.0 - np.tanh((x - xt)/W)) / (1.0 + np.tanh(xt/W))
def g_of_x(x, xt, W, F):
    return 1.0 + (F - 1.0)*sigma_x(x, xt, W)
def dlng_dlna(x, xt, W, F):
    ch = np.cosh(np.clip((x - xt)/W, -300.0, 300.0))
    dsig = (1.0/(W*ch**2)) / (1.0 + np.tanh(xt/W))
    return (F - 1.0)*dsig / g_of_x(x, xt, W, F)
def E2(x, oL, xt, W, F):
    a = np.exp(-x)
    return g_of_x(x, xt, W, F) * (OM_M*a**-3 + OM_R*a**-4 + oL)
def comoving(x_hi, oL, xt, W, F, n=1000):
    xs = np.linspace(0.0, x_hi, n); X = xs[None, :]
    H = 100.0*np.sqrt(E2(X, np.atleast_1d(oL)[:, None], np.atleast_1d(xt)[:, None], np.atleast_1d(W)[:, None], F))
    return np.trapz(C_KMS*np.exp(X)/H, xs, axis=1)
def sound_horizon(oL, xt, W, F, n=1600, z_end=Z_REC):
    xs = np.linspace(math.log(1 + z_end), math.log(1 + 1e8), n); X = xs[None, :]
    a = np.exp(-X); cs = C_KMS/np.sqrt(3.0*(1.0 + (3.0*OM_B/(4.0*OM_G))*a))
    H = 100.0*np.sqrt(E2(X, np.atleast_1d(oL)[:, None], np.atleast_1d(xt)[:, None], np.atleast_1d(W)[:, None], F))
    return np.trapz(cs*np.exp(X)/H, xs, axis=1)
def age_gyr(oL, xt, Wv, F, n=1200):
    xs = np.linspace(0.0, math.log(1 + 3.0e4), n)
    H = 100.0*np.sqrt(E2(xs[None, :], np.atleast_1d(oL)[:, None], np.atleast_1d(xt)[:, None],
                         np.atleast_1d(Wv)[:, None], F))
    return np.trapz(1.0/H, xs, axis=1)*(3.0856775814913673e19/(1e9*3.1557e7))
def bao_chi2(oL, xt, Wv, F):
    rd = sound_horizon(oL, xt, Wv, F, z_end=Z_DRAG); c2 = np.zeros(np.size(oL))
    for kind, z, val, err in BAO:
        x = math.log(1 + z)
        DM = comoving(x, oL, xt, Wv, F, n=400)
        DH = C_KMS/(100.0*np.sqrt(E2(x, oL, xt, Wv, F)))
        pred = {"DM": DM, "DH": DH, "DV": np.cbrt(z*DM*DM*DH)}[kind]/rd
        c2 += ((pred - val)/err)**2
    return c2
def growth(oL, xt, W, F, modelA=True, a_i=1e-3, N=1200, want_curve=False):
    oL = np.atleast_1d(oL).astype(float); xt = np.atleast_1d(xt).astype(float); W = np.atleast_1d(W).astype(float)
    lo, hi = math.log(a_i), 0.0; h = (hi - lo)/N
    def deriv(la, y):
        d, dp = y; x = -la; a = math.exp(la)
        rm = OM_M*a**-3; br = rm + oL
        if modelA:
            dlnH = 0.5*(dlng_dlna(x, xt, W, F) - 3.0*rm/br); S = 1.5*rm/br
        else:
            dlnH = 0.5*(-3.0*rm/br); S = 1.5*g_of_x(x, xt, W, F)*rm/br
        return np.array([dp, -(2.0 + dlnH)*dp + S*d])
    y = np.array([np.full_like(oL, a_i), np.full_like(oL, a_i)])
    curve = []
    for i in range(N):
        la = lo + i*h
        k1 = deriv(la, y); k2 = deriv(la + h/2, y + h/2*k1)
        k3 = deriv(la + h/2, y + h/2*k2); k4 = deriv(la + h, y + h*k3)
        y = y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        if want_curve: curve.append((lo + (i + 1)*h, y[0].copy(), y[1].copy()))
    return (y[0], y[1]/y[0], curve) if want_curve else (y[0], y[1]/y[0])
def fs8_chi2(curve, s8):
    la = np.array([c[0] for c in curve]); D = np.array([c[1] for c in curve]); f = np.array([c[2]/c[1] for c in curve])
    z = np.exp(-la) - 1.0
    pred = f*D/D[-1][None, :]*np.atleast_1d(s8)[None, :]
    chi2 = np.zeros(pred.shape[1])
    for k in range(RSD.shape[0]):
        row = np.array([np.interp(RSD[k, 0], z[::-1], pred[::-1, p]) for p in range(pred.shape[1])])
        chi2 += ((row - RSD[k, 1])/RSD[k, 2])**2
    return chi2, np.array([[np.interp(RSD[k, 0], z[::-1], pred[::-1, p]) for k in range(RSD.shape[0])]
                           for p in range(pred.shape[1])])

oL_fid = H_FID**2 - OM_M - OM_R
xt0 = np.array([math.log(2.0)]); W0 = np.array([0.3])
D_fid, f_fid, cur_fid = growth(np.array([oL_fid]), xt0, W0, 1.0, want_curve=True)
Dova = float(D_fid[0]); f0_fid = float(f_fid[0])
Om_f, OL_f = OM_M/H_FID**2, oL_fid/H_FID**2
CPT = 2.5*Om_f/(Om_f**(4/7) - OL_f + (1 + Om_f/2)*(1 + OL_f/70))
rs0 = float(sound_horizon(np.array([oL_fid]), xt0, W0, 1.0)[0])
DA0 = float(comoving(math.log(1 + Z_REC), np.array([oL_fid]), xt0, W0, 1.0)[0]); th0 = rs0/DA0
chi2_fid = float(fs8_chi2(cur_fid, np.array([S8_FID]))[0][0])
rd0 = float(sound_horizon(np.array([oL_fid]), xt0, W0, 1.0, z_end=Z_DRAG)[0])
t0_fid = float(age_gyr(np.array([oL_fid]), xt0, W0, 1.0)[0])
chi2_bao_fid = float(bao_chi2(np.array([oL_fid]), xt0, W0, 1.0)[0])
TH_TARGET = th0

NZT, NW = 81, 45
zt_ax = np.geomspace(1e-2, 3.0e3, NZT); W_ax = np.geomspace(2e-2, 5.0, NW)
ZT, WW = np.meshgrid(zt_ax, W_ax, indexing="ij")
ZTf, WWf = ZT.ravel(), WW.ravel(); xt = np.log(1 + ZTf); Wv = WWf; P = xt.size
ZSN = np.geomspace(0.01, 1.5, 40)
DL_FID = np.array([comoving(math.log(1 + z), np.array([oL_fid]), np.array([0.0]), np.array([1.0]), 1.0, n=600)[0]*(1 + z)
                   for z in ZSN])
def sne_rms(oL, F, xt, Wv, n=500):
    dmu = np.empty((np.size(oL), ZSN.size))
    for j, z in enumerate(ZSN):
        dmu[:, j] = 5*np.log10(comoving(math.log(1 + z), oL, xt, Wv, F, n=n)*(1 + z)/DL_FID[j])
    return np.sqrt(np.mean((dmu - dmu.mean(axis=1, keepdims=True))**2, axis=1))
def q0_of(oL, F, xt, Wv):
    return -1.0 - 0.5*(dlng_dlna(0.0, xt, Wv, F) + (-3*OM_M - 4*OM_R)/(OM_M + OM_R + oL))
def refit_h(F, rs, xt, Wv, n=600, iters=52):
    n_p = xt.size
    lo = np.full(n_p, math.sqrt(F*(OM_M + OM_R))*(1 + 1e-9)); hi = np.full(n_p, 3.0)
    def th(h): return rs/comoving(math.log(1 + Z_REC), h*h/F - OM_M - OM_R, xt, Wv, F, n=n)
    ok = (th(lo) <= TH_TARGET) & (th(hi) >= TH_TARGET)
    for _ in range(iters):
        mid = 0.5*(lo + hi); m = th(mid) < TH_TARGET
        lo = np.where(m, mid, lo); hi = np.where(m, hi, mid)
    return 0.5*(lo + hi), ok
def branch(tag, oL, hh, F, xt, Wv, rs):
    b = {"tag": tag, "oL": oL, "h": hh}
    b["Om"] = np.where(hh > 0, OM_M/hh**2, np.nan); b["OL"] = np.where(hh > 0, oL/hh**2, np.nan)
    b["dtheta"] = rs/comoving(math.log(1 + Z_REC), oL, xt, Wv, F)/TH_TARGET - 1.0
    b["q0"] = q0_of(oL, F, xt, Wv)
    b["sne"] = sne_rms(oL, F, xt, Wv)
    b["dchi2_bao"] = bao_chi2(oL, xt, Wv, F) - chi2_bao_fid
    b["t0"] = age_gyr(oL, xt, Wv, F)
    D, f, cur = growth(oL, xt, Wv, F, modelA=True, want_curve=True)
    b["s8"] = S8_FID*D/D_fid[0]
    c2, pr = fs8_chi2(cur, b["s8"]); b["chi2_rsd"] = c2; b["dchi2"] = c2 - chi2_fid; b["fs8"] = pr
    b["f0"] = f; b["D"] = D; b["curve"] = cur
    b["exp_ok"] = ((oL >= 0.0) & np.isfinite(hh) & (hh >= H_LO) & (hh <= H_HI)
                   & (np.abs(b["dtheta"]) <= 0.003) & (b["q0"] >= Q0_LO) & (b["q0"] <= Q0_HI) & (b["sne"] <= 0.10)
                   & (b["dchi2_bao"] <= 9.0))
    b["gro_ok"] = (np.abs(b["s8"]/S8_FID - 1) <= 0.10) & (b["dchi2"] <= 9.0)
    return b
def evaluate(F, xt, Wv):
    o = {}; n_p = xt.size
    o["g_bbn"] = g_of_x(math.log(1 + Z_BBN), xt, Wv, F)
    o["g_rec"] = g_of_x(math.log(1 + Z_REC), xt, Wv, F)
    o["g_cl"]  = g_of_x(math.log(1 + Z_CLUST_MAX), xt, Wv, F)
    oL_a = np.full(n_p, max(H_FID**2/F - OM_M - OM_R, 0.0))
    rs = sound_horizon(oL_a, xt, Wv, F); o["rs"] = rs
    o["ok_oL"] = (H_FID**2/F - OM_M - OM_R) >= 0.0
    A = branch("a", oL_a, np.full(n_p, H_FID), F, xt, Wv, rs); A["exp_ok"] &= o["ok_oL"]
    hb, br_ok = refit_h(F, rs, xt, Wv); hb = np.where(br_ok, hb, np.nan)
    B = branch("b", np.maximum(np.nan_to_num(hb, nan=H_FID)**2/F - OM_M - OM_R, 0.0), hb, F, xt, Wv, rs)
    B["exp_ok"] &= br_ok
    C = branch("c", np.full(n_p, oL_fid), np.full(n_p, math.sqrt(F)*H_FID), F, xt, Wv, rs)
    o["br"] = {"a": A, "b": B, "c": C}
    o["T1"] = np.abs(o["g_bbn"] - 1) <= BBN_TOL
    o["T2"] = np.abs(o["g_rec"] - 1) <= CMB_TOL
    o["T3"] = A["gro_ok"] | B["gro_ok"] | C["gro_ok"]
    o["T4"] = A["exp_ok"] | B["exp_ok"] | C["exp_ok"]
    o["T34"] = ((A["gro_ok"] & A["exp_ok"]) | (B["gro_ok"] & B["exp_ok"]) | (C["gro_ok"] & C["exp_ok"]))
    o["T5"] = o["g_cl"] >= 0.9*F
    o["JOINT"] = o["T1"] & o["T2"] & o["T34"] & o["T5"]
    o["which"] = np.where(A["gro_ok"] & A["exp_ok"], "a", np.where(B["gro_ok"] & B["exp_ok"], "b",
                          np.where(C["gro_ok"] & C["exp_ok"], "c", "-")))
    return o
# ================================================== END OF THE VERBATIM BLOCK =============================

# ---------------------------------------------------------------- reproduce L9's refined surviving region
print("\n  C0 -- reproducing L9's surviving region with L9's own machinery, before any new data are touched.")
SURV = {}
for foot in ("canonical", "alt"):
    F = FREQ[foot]["F"]; R = evaluate(F, xt, Wv); i = np.where(R["JOINT"])[0]
    zlo, zhi = ZTf[i].min()/3.0, ZTf[i].max()*3.0; wlo, whi = WWf[i].min()/3.0, WWf[i].max()*3.0
    rz = np.geomspace(zlo, zhi, 61); rw = np.geomspace(wlo, whi, 61)
    RZ, RW = np.meshgrid(rz, rw, indexing="ij"); rzf, rwf = RZ.ravel(), RW.ravel()
    RR = evaluate(F, np.log(1 + rzf), rwf); m = RR["JOINT"]; k = np.where(m)[0]
    SURV[foot] = dict(F=F, zt=rzf[k], W=rwf[k], k=k, RR=RR, rzf=rzf, rwf=rwf, n=int(m.sum()), Ntot=int(m.size),
                      which=RR["which"][k], coarse=int(R["JOINT"].sum()))
    s = SURV[foot]
    # per-survivor cosmological outputs, taken from the construction that construction actually survives on
    for key in ("s8", "h", "Om", "OL", "dchi2", "chi2_rsd", "f0", "t0", "dchi2_bao", "q0", "oL", "D"):
        s[key] = np.array([RR["br"][s["which"][j]][key][k[j]] for j in range(k.size)])
    s["fs8"] = np.array([RR["br"][s["which"][j]]["fs8"][k[j]] for j in range(k.size)])
    print(f"    {foot:9s} F = {F:.3f}: coarse {s['coarse']}/{P}, refined {s['n']}/{s['Ntot']};  "
          f"z_t in [{s['zt'].min():.4g}, {s['zt'].max():.4g}], W in [{s['W'].min():.4g}, {s['W'].max():.4g}]")
    print(f"              sigma_8 {s['s8'].min():.3f}-{s['s8'].max():.3f}   H0 {100*s['h'].min():.2f}-{100*s['h'].max():.2f}   "
          f"Omega_m {s['Om'].min():.3f}-{s['Om'].max():.3f}   Omega_Lambda {s['OL'].min():.3f}-{s['OL'].max():.3f}   "
          f"f(0) {s['f0'].min():.3f}-{s['f0'].max():.3f}   t0 {s['t0'].min():.2f}-{s['t0'].max():.2f} Gyr")
    print(f"              constructions used: {sorted(set(s['which'].tolist()))};  "
          f"BAO dchi2 {s['dchi2_bao'].min():+.2f} to {s['dchi2_bao'].max():+.2f};  "
          f"RSD dchi2 {s['dchi2'].min():+.2f} to {s['dchi2'].max():+.2f}", flush=True)
c, a = SURV["canonical"], SURV["alt"]
c0 = (c["n"] == 146 and a["n"] == 269 and c["coarse"] == 21 and a["coarse"] == 48
      and abs(c["zt"].min() - 0.003333) < 1e-5 and abs(c["zt"].max() - 0.3743) < 1e-3
      and abs(c["W"].min() - 0.3757) < 1e-3 and abs(c["W"].max() - 0.5651) < 1e-3
      and abs(a["zt"].max() - 0.4406) < 1e-3 and abs(a["W"].min() - 0.3363) < 1e-3
      and abs(a["W"].max() - 0.6036) < 1e-3
      and abs(c["s8"].min() - 0.853) < 5e-4 and abs(c["s8"].max() - 0.861) < 5e-4
      and abs(a["s8"].min() - 0.845) < 5e-4 and abs(a["s8"].max() - 0.861) < 5e-4
      and abs(100*c["h"].min() - 68.90) < 0.02 and abs(100*c["h"].max() - 71.99) < 0.02
      and abs(c["Om"].min() - 0.276) < 5e-4 and abs(c["Om"].max() - 0.301) < 5e-4
      and abs(Dova/CPT - 1) < 0.01 and abs(th0/THETA_S - 1) < 0.01 and abs(t0_fid/13.797 - 1) < 0.01)
check("C0 [control] this file's machinery reproduces L9's published surviving region to the digit -- counts, "
      "(z_t, W) box and the (sigma_8, H0, Omega_m) margins on both footings",
      c0, f"canonical 146/3721 and alt 269/3721 recovered; sigma_8 [{c['s8'].min():.3f}, {c['s8'].max():.3f}] / "
          f"[{a['s8'].min():.3f}, {a['s8'].max():.3f}]; LambdaCDM control D/a within {100*abs(Dova/CPT-1):.2f}% of "
          f"Carroll-Press-Turner, theta_* within {100*abs(th0/THETA_S-1):.2f}%, t0 {t0_fid:.3f} Gyr")

# ---------------------------------------------------------------- the measurements
print(f"\n{'='*124}\n  the measurements, with their sources.  Every number is either already in this repository at the "
      f"cited line\n  or is the published value that line quotes.\n{'='*124}")
# name: (S8, sigma_lo, sigma_hi, kind, provenance)
MEAS = [
 ("Planck 2018 TT,TE,EE+lowE", 0.832, 0.013, 0.013, "cmb",
  "real_research/reviews/mi_cosmo_perturbations_2026.py:166 (S8_PLANCK); Planck 2018 VI, A&A 641 A6"),
 ("KiDS-1000 3x2pt (2021)",    0.759, 0.021, 0.024, "shear",
  "reviews/gc_consequences/w_gradient_cmb_calc.py:131 + mi_cosmo_perturbations_2026.py:1008; Heymans+2021 A&A 646 A140"),
 ("DES Y3 3x2pt (2022)",       0.776, 0.017, 0.017, "shear",
  "reviews/gc_consequences/w_gradient_cmb_calc.py:130; DES Collaboration 2022 PRD 105 023520"),
 ("DES Y3 + KiDS-1000 joint",  0.790, 0.014, 0.018, "shear",
  "reviews/gc_consequences/w_gradient_cmb_calc.py:132 ('KiDS+DES (joint, 2023) S8 ~ 0.79'); DES+KiDS 2023 OJAp 6 36"),
 ("HSC Y3 cosmic shear",       0.769, 0.031, 0.031, "shear",
  "ai_slop/research/predictions/02_DESI_STRUCTURE_GROWTH.py:110 and ai_slop/examples/09_s8_tension/run.py:89; Li+2023 PRD 108 123518"),
 ("KiDS-Legacy (2025)",        0.815, 0.016, 0.016, "shear",
  "real_research/reviews/mi_cosmo_perturbations_2026.py:1009; Wright+2025 -- the revision that eased the tension"),
 ("2026 lensing compilation",  0.819, 0.007, 0.007, "shear",
  "real_research/reviews/dm_candidate_test.py:32 (2026 review 2602.12238)"),
 ("DESI DR9 galaxy x lensing", 0.840, 0.020, 0.020, "cross",
  "reviews/GHOST_CONDENSATE_CONSEQUENCES_2026-06-19.md:68"),
 ("eRASS1 cluster counts",     0.860, 0.010, 0.010, "cluster",
  "reviews/cluster_measurement/routeB_dynamical_mass_calibration_eta.py:31,65; Ghirardini+2024 A&A 689 A298"),
]
for nm, v, lo, hi, kind, src in MEAS:
    print(f"    {nm:28s} S_8 = {v:.3f} " + (f"+/- {hi:.3f}" if lo == hi else f"+{hi:.3f}/-{lo:.3f}") +
          f"   [{kind}]\n        {src}")
print("    NOTE, stated because it runs against the direction this lane is testing: the corpus's own")
print("    THE_HONEST_LCDM_STRESS_BRIEF.md:69 lists S_8 on the DO-NOT-CITE list -- as a LambdaCDM stress, because")
print("    KiDS-Legacy and HSC-Y3 moved UP toward Planck.  That is a warning against claiming a low-S_8 deficit.")
print("    It cuts BOTH ways here: the upward revision makes the shear constraint LESS hostile to a high-sigma_8")
print("    model, so this lane uses KiDS-Legacy and the 2026 compilation as the primary shear comparison rather")
print("    than the older, lower KiDS-1000 and DES Y3, which would manufacture a harsher verdict.")
print("    NOTE on eRASS1: the same repository (routeB_dynamical_mass_calibration_eta.py:184-197) records that")
print("    eRASS1's HIGH S_8 may be a weak-lensing mass-calibration artefact, and this lane's own L18 shows the")
print("    hydrostatic bias runs against the framework.  eRASS1 is reported, not leaned on.")
H0_MEAS = [("Planck 2018", 67.36, 0.54, "Planck 2018 VI"), ("SH0ES 2022", 73.04, 1.04, "Riess+2022 ApJL 934 L7")]

S8_LCDM = S8_FID*math.sqrt((OM_M/H_FID**2)/0.3)
def zscore(v, meas, sig_model=0.0):
    """asymmetric-error z-score of a model value against one measurement.  A model value ABOVE the measurement
       is scored against the measurement's UPPER error bar, which is the one pointing at it."""
    nm, m, lo, hi, kind, src = meas
    e = np.where(np.asarray(v) >= m, hi, lo)
    return (np.asarray(v) - m)/np.sqrt(e**2 + np.asarray(sig_model)**2)

# ---------------------------------------------------------------- C1: the conversion + tension controls
print(f"\n{'='*124}\n  C1 -- CONTROL: the S_8 machinery on numbers whose answers are already known\n{'='*124}")
print(f"    concordance:  sigma_8 = {S8_FID:.4f}, Omega_m = {OM_M/H_FID**2:.5f}  ->  S_8 = sigma_8 sqrt(Omega_m/0.3) "
      f"= {S8_LCDM:.4f}   against the published Planck S_8 = 0.832 +/- 0.013 ({abs(S8_LCDM-0.832)/0.013:.2f} sigma)")
tens = {}
for nm, v, lo, hi, kind, src in MEAS[1:]:
    d = 0.832 - v; e = math.sqrt(0.013**2 + (hi if v < 0.832 else lo)**2); tens[nm] = d/e
    print(f"    Planck vs {nm:28s}: Delta S_8 = {d:+.3f}, {abs(d/e):.2f} sigma "
          + ("(lensing LOWER than the CMB)" if d > 0 else "(HIGHER than the CMB)"))
ok1 = (abs(S8_LCDM - 0.832) < 0.013                                    # conversion reproduces Planck's S_8
       and 2.0 <= tens["KiDS-1000 3x2pt (2021)"] <= 3.5                # the classic tension, published ~3 sigma
       and 2.0 <= tens["DES Y3 3x2pt (2022)"] <= 3.0                   # published 2.3-2.6 sigma
       and 0.4 <= tens["KiDS-Legacy (2025)"] <= 1.2                    # published 0.73 sigma after the revision
       and tens["eRASS1 cluster counts"] < 0)                          # cluster counts sit ABOVE the CMB
check("C1 [control] the S_8 conversion reproduces the concordance value AND the known size and SIGN of the S_8 "
      "tension: ~3 sigma low for KiDS-1000, ~2.6 sigma low for DES Y3, ~0.7 sigma after the KiDS-Legacy "
      "revision, and ABOVE the CMB for cluster counts", ok1,
      f"S_8(concordance) = {S8_LCDM:.4f} vs published 0.832 ({abs(S8_LCDM-0.832)/0.013:.2f} sigma); "
      f"KiDS-1000 {tens['KiDS-1000 3x2pt (2021)']:.2f} sigma, DES Y3 {tens['DES Y3 3x2pt (2022)']:.2f} sigma, "
      f"KiDS-Legacy {tens['KiDS-Legacy (2025)']:.2f} sigma, eRASS1 {tens['eRASS1 cluster counts']:.2f} sigma")

# ---------------------------------------------------------------- the two readings of the model's S_8
print(f"\n{'='*124}\n  converting L9's region into S_8, TWO ways\n{'='*124}")
# ---- reading (ii) needs a lensing kernel.  Limber, with the transfer function in PHYSICAL units so that the
#      shape is identical between model and LambdaCDM (omega_m, omega_b, n_s are all CMB-fixed).
def T_bbks(k_phys, h):
    """BBKS with Sugiyama's baryon correction; k in Mpc^-1, so Gamma*h = omega_m exp(...) is h-independent to 0.02%."""
    Om, Ob = OM_M/h**2, OM_B/h**2
    Gam_h = OM_M*math.exp(-Ob*(1 + math.sqrt(2*h)/Om))
    q = k_phys*(2.7255/2.7)**2/Gam_h
    return (np.log(1 + 2.34*q)/(2.34*q))*(1 + 3.89*q + (16.1*q)**2 + (5.46*q)**3 + (6.71*q)**4)**-0.25
ZG = np.linspace(0.005, 3.0, 130)                      # lens/source redshift grid
NZ_SRC = ZG**2*np.exp(-(ZG/0.55)**1.5)                 # Smail n(z): median 0.72, close to KiDS-1000 (0.7) / DES Y3
NZ_SRC = NZ_SRC/np.trapz(NZ_SRC, ZG)
ELL = 1000.0                                           # mid-range cosmic-shear multipole
def limber_amp(oL, xt_a, Wv_a, F, hh, curve, use_g=True):
    """sqrt(C_ell^kappakappa / C_ell^kappakappa[LambdaCDM]) in the Limber approximation, vectorised over models.
       The Weyl source is (3/2) g(a) omega_m (100/c)^2 delta/a with omega_m CMB-FIXED, so the constant prefactor
       is identical between model and LambdaCDM and cancels; what does not cancel is g(z), the growth history
       and the geometry."""
    n_p = np.size(oL)
    chi = np.empty((n_p, ZG.size))
    for j, z in enumerate(ZG):
        chi[:, j] = comoving(math.log(1 + z), oL, xt_a, Wv_a, F, n=220)
    la = np.array([cc[0] for cc in curve]); Dc = np.array([cc[1] for cc in curve])   # (N, n_p)
    zc = np.exp(-la) - 1.0
    D = np.array([np.interp(ZG, zc[::-1], Dc[::-1, p]) for p in range(n_p)])         # (n_p, nz), absolute normalisation
    gz = g_of_x(np.log(1 + ZG)[None, :], np.atleast_1d(xt_a)[:, None], np.atleast_1d(Wv_a)[:, None], F) if use_g \
         else np.ones((n_p, ZG.size))
    dz = np.gradient(ZG)
    q = np.zeros((n_p, ZG.size))
    for i in range(ZG.size):                                                        # lensing efficiency
        w = np.clip(chi[:, i:] - chi[:, i][:, None], 0, None)/np.maximum(chi[:, i:], 1e-30)
        q[:, i] = np.sum(NZ_SRC[None, i:]*dz[None, i:]*w, axis=1)
    Pk = T_bbks(ELL/np.maximum(chi, 1e-30), float(np.nanmedian(hh)))**2*(ELL/np.maximum(chi, 1e-30))**NS
    dchi = np.gradient(chi, axis=1)
    C = np.sum(dchi*(gz*(1 + ZG[None, :])*q*D)**2*Pk, axis=1)
    return C
# LambdaCDM reference, same machinery
C_LCDM = limber_amp(np.array([oL_fid]), xt0, W0, 1.0, np.array([H_FID]), cur_fid)[0]
# a NON-TRIVIAL identity: at F = 1 the roll is g == 1 for EVERY (z_t, W), so a completely different transition
# pair must return the identical answer through the whole pipeline (growth curve included)
xt1 = np.array([math.log(1.2)]); W1 = np.array([1.7])
D1, f1, cur1 = growth(np.array([oL_fid]), xt1, W1, 1.0, want_curve=True)
C_ctrl = limber_amp(np.array([oL_fid]), xt1, W1, 1.0, np.array([H_FID]), cur1)[0]
cur_boost = [(cc[0], 1.1*cc[1], 1.1*cc[2]) for cc in cur_fid]
C_boost = limber_amp(np.array([oL_fid]), xt0, W0, 1.0, np.array([H_FID]), cur_boost)[0]
print(f"    Limber control: at F = 1 a different transition pair (z_t = 0.2, W = 1.7) returns sqrt(C/C_LCDM) = "
      f"{math.sqrt(C_ctrl/C_LCDM):.12f} (exactly 1 required);")
print(f"                    a 10% boost in the growth amplitude gives {math.sqrt(C_boost/C_LCDM):.6f} (1.100000 required)")
lim_ok = abs(math.sqrt(C_ctrl/C_LCDM) - 1) < 1e-12 and abs(math.sqrt(C_boost/C_LCDM) - 1.1) < 1e-9

for foot in ("canonical", "alt"):
    s = SURV[foot]
    s["S8_naive"] = s["s8"]*np.sqrt(s["Om"]/0.3)
    # lensing-consistent: per construction, since oL/h/curve differ
    S8eff = np.empty(s["n"]); S8eff_nog = np.empty(s["n"]); gbar = np.empty(s["n"])
    for cnm in sorted(set(s["which"].tolist())):
        sel = np.where(s["which"] == cnm)[0]; kk = s["k"][sel]; b = s["RR"]["br"][cnm]
        oLs = b["oL"][kk]; hs = b["h"][kk]; xts = np.log(1 + s["zt"][sel]); Wvs = s["W"][sel]
        cur = [(cc[0], cc[1][kk], cc[2][kk]) for cc in b["curve"]]
        Cg = limber_amp(oLs, xts, Wvs, s["F"], hs, cur, use_g=True)
        Cn = limber_amp(oLs, xts, Wvs, s["F"], hs, cur, use_g=False)
        S8eff[sel] = S8_LCDM*np.sqrt(Cg/C_LCDM); S8eff_nog[sel] = S8_LCDM*np.sqrt(Cn/C_LCDM)
        gbar[sel] = np.sqrt(Cg/Cn)
    s["S8_eff"] = S8eff; s["S8_eff_nog"] = S8eff_nog; s["gbar"] = gbar
    print(f"\n    {foot:9s} F = {s['F']:.3f}, {s['n']} survivors")
    print(f"      (i)  NAIVE, L9's own quoted pair: S_8 = sigma_8 sqrt(Omega_m/0.3) = {s['S8_naive'].min():.4f} - {s['S8_naive'].max():.4f}")
    print(f"           (sigma_8 {s['s8'].min():.3f}-{s['s8'].max():.3f} pulled DOWN by Omega_m "
          f"{s['Om'].min():.3f}-{s['Om'].max():.3f} < the concordance 0.3153)")
    print(f"      (i') the SAME region through the Limber integral with g REMOVED from the lensing kernel: "
          f"{s['S8_eff_nog'].min():.4f} - {s['S8_eff_nog'].max():.4f}")
    print(f"           this is the physically correct 'no roll in lensing' number -- the Weyl source is the PHYSICAL")
    print(f"           omega_m, which is CMB-fixed and identical to LambdaCDM's, so the sqrt(Omega_m/0.3) discount the")
    print(f"           naive formula applies is partly spurious.  The naive formula is low by up to "
          f"{100*max(s['S8_eff_nog']/s['S8_naive'] - 1):.1f}% at the bottom of the")
    print(f"           region, i.e. reading (i) is OPTIMISTIC for the model even before the roll is put back.")
    print(f"      (ii) LENSING-CONSISTENT (uniform g multiplies the Weyl potential): {s['S8_eff'].min():.4f} - {s['S8_eff'].max():.4f}")
    print(f"           the kernel-weighted roll factor is g_eff = {s['gbar'].min():.3f} - {s['gbar'].max():.3f} "
          f"(g(0) = F = {s['F']:.3f}, and the shear kernel peaks near z ~ 0.35 where the roll is partly done)", flush=True)
nv = np.concatenate([SURV[f]["S8_eff_nog"]/SURV[f]["S8_naive"] - 1 for f in SURV])
check("C1b [control] the Limber machinery is an identity on LambdaCDM at F = 1 for any (z_t, W), is exactly "
      "linear in the growth amplitude, and its g-free evaluation of L9's own region agrees with the naive "
      "S_8 = sigma_8 sqrt(Omega_m/0.3) formula to better than 10%",
      lim_ok and max(abs(nv)) < 0.10,
      f"identity {math.sqrt(C_ctrl/C_LCDM):.12f}, 1.1x boost {math.sqrt(C_boost/C_LCDM):.6f}, naive-vs-Limber "
      f"agreement {100*max(abs(nv)):.1f}% (the naive formula runs LOW by up to {100*max(nv):.1f}%, because it "
      f"discounts by Omega_m while the Weyl source carries the CMB-fixed omega_m).  Readings (i') and (ii) "
      f"therefore differ ONLY by the roll factor g_eff, and (i) is the optimistic edge of (i')")

# ---------------------------------------------------------------- C2 / C3: compatibility fractions
print(f"\n{'='*124}\n  C2/C3 -- the comparison done properly: every surviving grid point against every measurement\n{'='*124}")
SIG_MODEL_REL = 0.0060/0.8111       # L9's sigma_8 is 0.8111 x D_model/D_LCDM: it inherits Planck's normalisation error
print(f"    Each survivor carries a model error of {100*SIG_MODEL_REL:.2f}% (Planck's sigma_8 = 0.8111 +/- 0.0060, which")
print(f"    L9's normalisation multiplies through) added in quadrature to the measurement error.  This is generous to")
print(f"    the model: it can only move points TOWARD compatibility.\n")
READINGS = [("S8_naive", "(i) NAIVE"), ("S8_eff_nog", "(i') LIMBER, no roll"), ("S8_eff", "(ii) LENS-CONSISTENT")]
FRAC = {}
for foot in ("canonical", "alt"):
    s = SURV[foot]; FRAC[foot] = {}
    print(f"    {foot} ({s['n']} survivors).  f(2s)/f(3s) = fraction of the SURVIVING REGION inside 2/3 sigma.")
    print(f"      {'measurement':26s} |" + "|".join(f"{lab:^31s}" for _, lab in READINGS))
    print(f"      {'':26s} |" + "|".join(f"{'z range':>17s}{'f2s':>7s}{'f3s':>7s}" for _ in READINGS))
    for meas in MEAS:
        row = []
        for key, _ in READINGS:
            z = zscore(s[key], meas, SIG_MODEL_REL*s[key])
            row.append((z, float(np.mean(np.abs(z) <= 2.0)), float(np.mean(np.abs(z) <= 3.0))))
        FRAC[foot][meas[0]] = {lab: dict(f2=row[i][1], f3=row[i][2],
                                         z=(float(row[i][0].min()), float(row[i][0].max())))
                               for i, (_, lab) in enumerate(READINGS)}
        print(f"      {meas[0]:26s} |" + "|".join(
            f"{r[0].min():+8.2f}..{r[0].max():+7.2f}{100*r[1]:6.0f}%{100*r[2]:6.0f}%" for r in row))
    print(flush=True)
SHEAR = [m[0] for m in MEAS if m[4] == "shear"]
assert len(SHEAR) == 6, SHEAR
print("    CAVEAT on the six shear rows: they are NOT six independent measurements.  KiDS-1000 and KiDS-Legacy")
print("    are the same survey before and after its 2025 revision, DES Y3 enters twice (alone and in the joint), and")
print("    the 2026 compilation re-analyses them.  Requiring all six at once is OVER-strict, so the checks below")
print("    are decided on the SINGLE most favourable modern set (KiDS-Legacy, 0.815 +/- 0.016), with the")
print("    all-six number reported alongside as the strict end of the range.  The 2026 compilation is itself a")
print("    re-analysis of the same surveys, not a seventh dataset.")
def any_frac(key, lvl, sets):
    """fraction of survivors compatible with EVERY named measurement at lvl sigma, per footing."""
    out = {}
    for foot in SURV:
        s = SURV[foot]; ok = np.ones(s["n"], bool)
        for meas in MEAS:
            if meas[0] in sets: ok &= np.abs(zscore(s[key], meas, SIG_MODEL_REL*s[key])) <= lvl
        out[foot] = ok
    return out
KL = MEAS[5]                                          # KiDS-Legacy: the most favourable modern shear set
J = {}
for lvl, tag in ((2.0, "C2"), (3.0, "C3")):
    one = {}; alls = {}
    for key, lab in READINGS:
        alls[lab] = any_frac(key, lvl, SHEAR)
        one[lab] = {f: np.abs(zscore(SURV[f][key], KL, SIG_MODEL_REL*SURV[f][key])) <= lvl for f in SURV}
    J[lvl] = (one, alls)
    det = "; ".join(
        f"{lab}: KiDS-Legacy " + ", ".join(f"{f} {int(one[lab][f].sum())}/{SURV[f]['n']}" for f in SURV)
        + " | all six " + ", ".join(f"{f} {int(alls[lab][f].sum())}/{SURV[f]['n']}" for f in SURV)
        for _, lab in READINGS)
    ok = all(any(one[lab][f].any() for f in SURV) for _, lab in READINGS)
    check(f"{tag} [{int(lvl)} sigma] some part of L9's surviving region is compatible with the cosmic-shear S_8 at "
          f"{int(lvl)} sigma on EVERY reading of the model, including the one that is self-consistent for a "
          f"spatially uniform g(z)", ok, det)
J2N = J[2.0][1]["(i) NAIVE"]; J2E = J[2.0][1]["(ii) LENS-CONSISTENT"]

# ---------------------------------------------------------------- C4: S_8 and H0 together
print(f"\n{'='*124}\n  C4 -- the H0 angle: can a single point fit a high H0 AND an acceptable S_8?\n{'='*124}")
print(f"    L9's region predicts H0 = 68-72, which straddles Planck ({H0_MEAS[0][1]} +/- {H0_MEAS[0][2]}) and")
print(f"    SH0ES ({H0_MEAS[1][1]} +/- {H0_MEAS[1][2]}).  The question is whether the SAME point can do both jobs.")
for foot in ("canonical", "alt"):
    s = SURV[foot]; H = 100*s["h"]
    zP = (H - H0_MEAS[0][1])/H0_MEAS[0][2]; zS = (H - H0_MEAS[1][1])/H0_MEAS[1][2]
    okP, okS = np.abs(zP) <= 2, np.abs(zS) <= 2
    print(f"    {foot:9s}: H0 {H.min():.2f}-{H.max():.2f};  within 2 sigma of Planck {int(okP.sum())}/{s['n']}, "
          f"of SH0ES {int(okS.sum())}/{s['n']}, of NEITHER {int((~okP & ~okS).sum())}/{s['n']}"
          + ("   -- the region CANNOT sit at the Planck H0" if not okP.any() else ""))
    for key, lab in READINGS:
        ok = np.abs(zscore(s[key], KL, SIG_MODEL_REL*s[key])) <= 2
        s["okS8_" + key] = ok
        print(f"               S_8 {lab:22s} within 2 sigma of KiDS-Legacy: {int(ok.sum()):4d}/{s['n']};  "
              f"JOINT with SH0ES {int((ok & okS).sum()):4d};  JOINT with Planck-H0 {int((ok & okP).sum()):4d}")
    cc = np.corrcoef(H, s["S8_naive"])[0, 1]
    print(f"               correlation of H0 with S_8 across the region: r = {cc:+.3f} -- "
          + ("the region must CHOOSE: higher H0 costs S_8" if cc > 0.3 else
             "a higher H0 also LOWERS S_8, so the two do NOT pull against each other here" if cc < -0.3 else
             "H0 and S_8 are close to independent across the region"))
    s["okH_SH0ES"] = okS; s["okH_Planck"] = okP
    s["okS8_KL"] = s["okS8_S8_naive"]; s["okS8_KLe"] = s["okS8_S8_eff"]
c4 = all(any((SURV[f]["okS8_" + key] & (SURV[f]["okH_SH0ES"] | SURV[f]["okH_Planck"])).any() for f in SURV)
         for key, _ in READINGS)
check("C4 [H0+S8] a SINGLE surviving point sits within 2 sigma of a measured H0 (Planck or SH0ES) and within "
      "2 sigma of the most favourable modern cosmic-shear S_8 at the same time, on EVERY reading", c4,
      "; ".join(lab + ": " + ", ".join(
          f"{f} {int((SURV[f]['okS8_' + key] & (SURV[f]['okH_SH0ES'] | SURV[f]['okH_Planck'])).sum())}/{SURV[f]['n']}"
          for f in SURV) for key, lab in READINGS)
      + ".  The internal tension is NOT between H0 and S_8 -- they are anti-correlated across the region, so "
        "the high-H0 end is also the low-S_8 end -- it is that the canonical footing cannot reach the Planck H0 "
        "at all")

# ---------------------------------------------------------------- C5: the growth gate on real data
print(f"\n{'='*124}\n  C5 -- L9's internal growth gate replaced by the measurements themselves\n{'='*124}")
print(f"    L9 gated growth on Delta chi^2_RSD <= +9 RELATIVE to LambdaCDM (its own 3 sigma) plus |sigma_8/0.8111 - 1|")
print(f"    <= 10%, and reported that tightening to 2 sigma empties the canonical footing.  That is a gate against a")
print(f"    reference model.  Here the gate is the DATA: the ABSOLUTE chi^2 of the model's own f*sigma_8 against the")
print(f"    {len(RSD)} RSD points (7 d.o.f., no parameters refitted at this stage), plus S_8.")
def chi2_p(x, k):
    """survival function of chi^2 with k d.o.f. -- series for even/odd k, no scipy."""
    if x <= 0: return 1.0
    if k % 2 == 0:
        s, t = 0.0, math.exp(-x/2)
        for i in range(k//2): s += t; t *= x/(2*(i + 1))
        return s
    s = math.erfc(math.sqrt(x/2)); t = math.sqrt(2*x/math.pi)*math.exp(-x/2)
    for i in range(1, (k + 1)//2): s += t; t *= x/(2*i + 1)
    return s
pctrl = [abs(chi2_p(14.067, 7) - 0.05), abs(chi2_p(24.322, 7) - 0.001), abs(chi2_p(9.488, 4) - 0.05),
         abs(chi2_p(3.841, 1) - 0.05)]
print(f"    chi^2 tail control: p(14.067, 7) = {chi2_p(14.067, 7):.5f} [0.05], p(24.322, 7) = {chi2_p(24.322, 7):.5f} "
      f"[0.001], p(9.488, 4) = {chi2_p(9.488, 4):.5f} [0.05], p(3.841, 1) = {chi2_p(3.841, 1):.5f} [0.05]  -- "
      f"max error {max(pctrl):.1e}")
print(f"    LambdaCDM's own absolute chi^2 on the same 7 points is {chi2_fid:.2f} (p = {chi2_p(chi2_fid, 7):.3f}).")
for foot in ("canonical", "alt"):
    s = SURV[foot]
    p = np.array([chi2_p(float(v), 7) for v in s["chi2_rsd"]])
    s["p_rsd"] = p
    rows = [("L9's own gate (Delta chi^2_RSD <= 9 + 10% on sigma_8)", np.ones(s["n"], bool)),
            ("absolute RSD fit acceptable at p > 0.05", p > 0.05),
            ("absolute RSD fit acceptable at p > 0.003", p > 0.003)]
    for key, lab in READINGS:
        rows += [(f"+ S_8 within 2 sigma of KiDS-Legacy      {lab}", (p > 0.05) & s["okS8_" + key]),
                 (f"+ S_8 within 3 sigma of all six shear   {lab}", (p > 0.003) & any_frac(key, 3.0, SHEAR)[foot])]
    print(f"\n    {foot} -- absolute RSD chi^2 over the region: {s['chi2_rsd'].min():.2f} - {s['chi2_rsd'].max():.2f} "
          f"(p = {p.max():.3f} down to {p.min():.1e})")
    for lab, mask in rows:
        n = int(mask.sum())
        print(f"      {lab:62s} {n:4d}/{s['n']}  ({100*n/s['n']:5.1f}%)"
              + (f"   z_t in [{s['zt'][mask].min():.4g}, {s['zt'][mask].max():.4g}], "
                 f"W in [{s['W'][mask].min():.4g}, {s['W'][mask].max():.4g}]" if n else "   EMPTY"))
    s["c5_naive"] = (p > 0.05) & s["okS8_S8_naive"]
    s["c5_nog"] = (p > 0.05) & s["okS8_S8_eff_nog"]
    s["c5_eff"] = (p > 0.05) & s["okS8_S8_eff"]
c5 = all(any(SURV[f]["c5_" + t].any() for f in SURV) for t in ("naive", "nog", "eff"))
check("C5 [growth on real data] with L9's internal Delta chi^2 gate replaced by the absolute goodness of fit to "
      "the RSD points and by the measured S_8, part of the region still survives on EVERY reading", c5,
      "; ".join(lab + ": " + ", ".join(f"{f} {int(SURV[f]['c5_' + t].sum())}/{SURV[f]['n']}" for f in SURV)
                for t, lab in (("naive", "(i) NAIVE"), ("nog", "(i') LIMBER no roll"),
                               ("eff", "(ii) LENS-CONSISTENT")))
      + f".  L9's own 3-sigma-to-2-sigma squeeze is reproduced by the data as a MILDER cut: the absolute RSD "
        f"p-value alone leaves {int((SURV['canonical']['p_rsd'] > 0.05).sum())}/146 canonical and "
        f"{int((SURV['alt']['p_rsd'] > 0.05).sum())}/269 alt, because L9's Delta chi^2 gate is measured against "
        f"LambdaCDM's own chi^2 = {chi2_fid:.2f} rather than against the 7 d.o.f.")

# ---------------------------------------------------------------- C6: does this interact with kappa?
print(f"\n{'='*124}\n  C6 -- the coefficient question: kappa_closure/k03 vs L9's cosmology\n{'='*124}")
print("    k03 established that the framework's own relation a0 = kappa c sqrt(G rho_Lambda) scales as H0 at fixed")
print("    Omega_Lambda, so 'the coefficient is degenerate with the H0 tension': kappa = 1/2 on Planck's H0 and")
print("    kappa = 0.461 on SH0ES's H0 give the same a0 to better than 1%.  L9's cosmology does NOT hold")
print("    Omega_Lambda fixed -- the closure 1 = F(Omega_m + Omega_r + Omega_Lambda) forces it DOWN to 0.25-0.32.")
print("    Since rho_Lambda is proportional to omega_Lambda = Omega_Lambda h^2, that is a first-order change in a0.")
K_HALF = 0.5; K_2PI = math.sqrt(8*math.pi/3)/(2*math.pi); FLOOR = 0.0947; DR4 = 0.21
KMEAS = {"BTFR": (0.465, 0.076), "distance-free": (0.551, 0.043)}
oL_LCDM = oL_fid
for foot in ("canonical", "alt"):
    s = SURV[foot]
    r = np.sqrt(s["oL"]/oL_LCDM)                       # a0 propto sqrt(rho_Lambda) propto sqrt(omega_Lambda)
    rF = np.sqrt(s["F"]*s["oL"]/oL_LCDM)               # the other reading: the G in a0 is the COSMOLOGICAL one
    s["a0_ratio"], s["a0_ratio_F"] = r, rF
    kneed = K_HALF/r; kneedF = K_HALF/rF
    print(f"    {foot:9s}: omega_Lambda {s['oL'].min():.4f}-{s['oL'].max():.4f} against LambdaCDM {oL_LCDM:.4f} "
          f"(a factor {(s['oL']/oL_LCDM).min():.3f}-{(s['oL']/oL_LCDM).max():.3f})")
    print(f"      reading 1, the G in a0 = kappa c sqrt(G rho_L) is the LOCAL G_0:")
    print(f"        a0 would move by a factor {r.min():.3f}-{r.max():.3f}, i.e. {100*(r.min()-1):+.1f}% to {100*(r.max()-1):+.1f}% "
          f"({abs(math.log10(r.min())):.3f}-{abs(math.log10(r.max())):.3f} dex), against a {100*FLOOR:.2f}% BTFR floor "
          f"and DR4's {100*DR4:.0f}% reach")
    print(f"        to hold a0 at its measured value the coefficient must be kappa = {kneed.min():.3f}-{kneed.max():.3f}, "
          f"which is {min(abs(kneed.min()-m)/e for m, e in KMEAS.values()):.1f}-"
          f"{max(abs(kneed.max()-m)/e for m, e in KMEAS.values()):.1f} sigma from the two measured values "
          f"(0.465 +/- 0.076 and 0.551 +/- 0.043)")
    print(f"      reading 2, that G is the COSMOLOGICAL F G_0 (the roll enters rho_Lambda's gravity too):")
    print(f"        a0 moves by {rF.min():.3f}-{rF.max():.3f} ({100*(rF.min()-1):+.1f}% to {100*(rF.max()-1):+.1f}%), and "
          f"kappa = {kneedF.min():.3f}-{kneedF.max():.3f} "
          f"({min(abs(kneedF.min()-m)/e for m, e in KMEAS.values()):.1f}-"
          f"{max(abs(kneedF.max()-m)/e for m, e in KMEAS.values()):.1f} sigma)")
    s["k_need"], s["k_needF"] = kneed, kneedF
    s["in_floor_1"] = np.abs(s["a0_ratio"] - 1) <= FLOOR
    s["in_floor_2"] = np.abs(s["a0_ratio_F"] - 1) <= FLOOR
print(f"\n    fraction of the surviving region that keeps a0 inside k03's {100*FLOOR:.2f}% BTFR mass-budget floor:")
for foot in ("canonical", "alt"):
    s = SURV[foot]
    print(f"      {foot:9s}  reading 1 (local G):  {int(s['in_floor_1'].sum()):4d}/{s['n']}      "
          f"reading 2 (cosmological G): {int(s['in_floor_2'].sum()):4d}/{s['n']}")
worst = max(max(abs(SURV[f]["a0_ratio"] - 1).max(), abs(SURV[f]["a0_ratio_F"] - 1).max()) for f in SURV)
best = min(min(abs(SURV[f]["a0_ratio"] - 1).min(), abs(SURV[f]["a0_ratio_F"] - 1).min()) for f in SURV)
c6 = all(SURV[f]["in_floor_1"].all() and SURV[f]["in_floor_2"].all() for f in SURV)
check("C6 [kappa] L9's surviving cosmology leaves the framework's own a0 = kappa c sqrt(G rho_Lambda) relation "
      "intact -- every surviving point stays inside the 9.47% BTFR mass-budget floor that k03 identified as the "
      "precision limit, on both readings of which G enters", c6,
      f"the shift runs {100*best:.1f}% to {100*worst:.1f}%: on reading 1 (the local G) NO point is inside the "
      f"{100*FLOOR:.2f}% floor and none is inside DR4's {100*DR4:.0f}% reach either; on reading 2 (the "
      f"cosmological F G_0) "
      + ", ".join(f"{f} {int(SURV[f]['in_floor_2'].sum())}/{SURV[f]['n']}" for f in SURV)
      + f" are.  The two questions DO interact: L9's closure lowers rho_Lambda by a factor "
        f"{min(SURV[f]['oL'].min()/oL_LCDM for f in SURV):.2f}-"
        f"{max(SURV[f]['oL'].max()/oL_LCDM for f in SURV):.2f} and drags a0 with it, which k03's H0 degeneracy "
        f"(stated at FIXED Omega_Lambda) does not cover")

# ---------------------------------------------------------------- C7: verdict
print(f"\n{'='*124}\n  C7 -- the verdict\n{'='*124}")
for foot in ("canonical", "alt"):
    s = SURV[foot]; okH = s["okH_Planck"] | s["okH_SH0ES"]
    for t, lab in (("naive", "(i) NAIVE"), ("nog", "(i') LIMBER no roll"), ("eff", "(ii) LENS-CONSISTENT")):
        s["full_" + t] = s["c5_" + t] & okH
    print(f"    {foot:9s}: of {s['n']} L9 survivors, the number keeping an acceptable absolute RSD fit, an S_8 within")
    print(f"               2 sigma of KiDS-Legacy AND an H0 within 2 sigma of Planck or SH0ES:")
    for t, lab in (("naive", "(i) NAIVE"), ("nog", "(i') LIMBER no roll"), ("eff", "(ii) LENS-CONSISTENT")):
        print(f"                 {lab:22s} {int(s['full_' + t].sum()):4d}/{s['n']}")
    for t, lab in (("naive", "(i) NAIVE"), ("nog", "(i') LIMBER no roll")):
        m = s["full_" + t]
        if not m.any(): continue
        print(f"               THE CORNER on reading {lab}: z_t in [{s['zt'][m].min():.4g}, {s['zt'][m].max():.4g}], "
              f"W in [{s['W'][m].min():.4g}, {s['W'][m].max():.4g}]")
        print(f"                 sigma_8 {s['s8'][m].min():.3f}-{s['s8'][m].max():.3f}, S_8(i) "
              f"{s['S8_naive'][m].min():.3f}-{s['S8_naive'][m].max():.3f}, S_8(i') {s['S8_eff_nog'][m].min():.3f}-"
              f"{s['S8_eff_nog'][m].max():.3f}, H0 {100*s['h'][m].min():.2f}-{100*s['h'][m].max():.2f}, "
              f"Omega_m {s['Om'][m].min():.3f}-{s['Om'][m].max():.3f}")
        print(f"                 RSD p-value {s['p_rsd'][m].min():.3f}-{s['p_rsd'][m].max():.3f}, "
              f"f(0) {s['f0'][m].min():.3f}-{s['f0'][m].max():.3f}, t0 {s['t0'][m].min():.2f}-{s['t0'][m].max():.2f} Gyr, "
              f"and its lensing-consistent S_8 would be {s['S8_eff'][m].min():.3f}-{s['S8_eff'][m].max():.3f}")
alive_naive = any(SURV[f]["full_naive"].any() for f in SURV)
alive_eff = any(SURV[f]["full_eff"].any() for f in SURV)
print("\n    HOW MUCH the roll would have to be removed from lensing for reading (i)/(i') to be legitimate.")
print("    The largest S_8 that stays within 2 sigma of KiDS-Legacy is "
      f"{KL[1] + 2*math.sqrt(KL[3]**2 + (SIG_MODEL_REL*KL[1])**2):.4f}, so the shear-kernel roll factor")
print("    would have to satisfy g_eff <= that divided by the model's own no-roll amplitude:")
for foot in ("canonical", "alt"):
    s = SURV[foot]
    gmax = (KL[1] + 2*np.sqrt(KL[3]**2 + (SIG_MODEL_REL*s["S8_eff"])**2))/s["S8_eff_nog"]
    supp = 1 - (gmax - 1)/np.maximum(s["gbar"] - 1, 1e-9)
    print(f"      {foot:9s}: allowed g_eff <= {gmax.min():.3f}-{gmax.max():.3f} against the actual "
          f"{s['gbar'].min():.3f}-{s['gbar'].max():.3f}, i.e. the roll must be suppressed in the LENSING")
    print(f"                 potential by {100*supp.min():.0f}-{100*supp.max():.0f}% relative to the DYNAMICAL one.")
print("    A suppression that large is exactly a lensing/dynamics decoupling of order F, and the same decoupling")
print("    would make cluster weak-lensing masses disagree with X-ray hydrostatic masses by of order F ~ 1.7-1.8.")
print("    They are observed to agree to tens of percent (L9's own open item (ii)), so this escape is not free.")
check("C7 [verdict] the late-roll mechanism survives current data on the reading that is SELF-CONSISTENT for a "
      "spatially uniform g(z), namely with the roll multiplying the Weyl potential that lenses light", alive_eff,
      ", ".join(f"{f}: {int(SURV[f]['full_eff'].sum())}/{SURV[f]['n']}" for f in SURV)
      + f".  On the maximally favourable reading, where an unspecified screening removes the roll from the shear "
        f"signal entirely, "
      + ", ".join(f"{f}: {int(SURV[f]['full_naive'].sum())}/{SURV[f]['n']}" for f in SURV)
      + " survive, so the mechanism is ALIVE ONLY IN A CORNER and only under that assumption")

print(f"\n{'='*124}\n  THE VERDICT OF THIS LANE\n{'='*124}")
cn, an = SURV["canonical"], SURV["alt"]
print(f"  1. sigma_8 = 0.845-0.861 is high, but S_8 is NOT, and that is the first real finding.  L9's survivors")
print(f"     carry Omega_m = {min(cn['Om'].min(), an['Om'].min()):.3f}-{max(cn['Om'].max(), an['Om'].max()):.3f}, "
      f"at or below the concordance 0.3153, so S_8 = sigma_8 sqrt(Omega_m/0.3) turns the high")
OLD3 = [m for m in MEAS if m[0] in ("KiDS-1000 3x2pt (2021)", "DES Y3 3x2pt (2022)", "HSC Y3 cosmic shear")]
zold = np.concatenate([zscore(SURV[f]["S8_naive"], m, SIG_MODEL_REL*SURV[f]["S8_naive"]) for f in SURV for m in OLD3])
print(f"     sigma_8 into S_8 = {min(cn['S8_naive'].min(), an['S8_naive'].min()):.3f}-"
      f"{max(cn['S8_naive'].max(), an['S8_naive'].max()):.3f}, which STRADDLES Planck's 0.832 +/- 0.013.  It sits "
      f"{zold.min():+.1f} to {zold.max():+.1f} sigma from the older")
print(f"     shear values (KiDS-1000, DES Y3, HSC Y3) but within 2 sigma of the revised KiDS-Legacy 0.815 +/- 0.016")
print(f"     over most of the region, and inside 1 sigma of DESI DR9 lensing and eRASS1 cluster counts.  So the")
print(f"     naive reading is NOT a kill: the S_8 tension running the other way does not by itself close it.")
print(f"     One caveat AGAINST the model, from its own numbers: the naive formula discounts by Omega_m while the")
print(f"     Weyl source carries the CMB-fixed omega_m, so the physically correct no-roll amplitude is HIGHER,")
print(f"     S_8 = {min(cn['S8_eff_nog'].min(), an['S8_eff_nog'].min()):.3f}-"
      f"{max(cn['S8_eff_nog'].max(), an['S8_eff_nog'].max()):.3f} -- the Omega_m discount is partly an artefact of the parametrisation.")
print(f"  2. The kill is elsewhere, and it is the gate L9 said it did not run.  In MODEL A the roll multiplies the")
print(f"     Poisson source, so with no slip it multiplies the Weyl potential.  The cosmic-shear amplitude is then")
print(f"     larger than LambdaCDM's by the kernel-weighted g_eff = {min(cn['gbar'].min(), an['gbar'].min()):.2f}-"
      f"{max(cn['gbar'].max(), an['gbar'].max()):.2f}, giving an effective S_8 = "
      f"{min(cn['S8_eff'].min(), an['S8_eff'].min()):.2f}-{max(cn['S8_eff'].max(), an['S8_eff'].max()):.2f}")
print(f"     against measurements at 0.76-0.86 with errors of 0.01-0.03.  That is not a tension, it is an exclusion")
print(f"     by tens of sigma, and it does not depend on which shear survey is used.")
print(f"  3. The escape is exactly the thing L9's own T8 already showed is unavailable.  Reading (i) survives only")
print(f"     if a screening removes the roll from the shear signal while leaving it in the cluster masses -- i.e.")
print(f"     the density-dependent screening L6 excluded at 12.8 sigma with 100% baryon-density overlap.  So the")
print(f"     two halves close on each other: with the screening, L6 kills it; without it, cosmic shear does.")
print(f"  4. And the framework's own coefficient moves with it.  L9's closure drives omega_Lambda down by a factor")
print(f"     {min(cn['oL'].min(), an['oL'].min())/oL_LCDM:.2f}-{max(cn['oL'].max(), an['oL'].max())/oL_LCDM:.2f}, "
      f"so a0 = kappa c sqrt(G rho_Lambda) moves by "
      f"{100*(min(cn['a0_ratio'].min(), an['a0_ratio'].min())-1):+.0f}% to "
      f"{100*(max(cn['a0_ratio'].max(), an['a0_ratio'].max())-1):+.0f}% if the G in that")
print(f"     relation is the LOCAL one -- outside k03's 9.47% BTFR floor at EVERY surviving point, and outside")
print(f"     DR4's 21% reach as well -- or {100*(min(cn['a0_ratio_F'].min(), an['a0_ratio_F'].min())-1):+.0f}% to "
      f"{100*(max(cn['a0_ratio_F'].max(), an['a0_ratio_F'].max())-1):+.0f}% if it is the COSMOLOGICAL F G_0, which stays")
print(f"     inside the floor for {int(cn['in_floor_2'].sum())}/146 canonical and {int(an['in_floor_2'].sum())}/269 alt "
      f"points.  Holding a0 fixed on the first reading would need")
print(f"     kappa = {min(cn['k_need'].min(), an['k_need'].min()):.2f}-"
      f"{max(cn['k_need'].max(), an['k_need'].max()):.2f}, 2.9-6.1 sigma from both measured values.  This is a NEW "
      f"constraint and not a restatement")
print(f"     of k03: k03's degeneracy was with H0 at FIXED Omega_Lambda, and L9's closure is precisely a mechanism")
print(f"     that MOVES Omega_Lambda.  Which G enters is not settled here, so both readings are carried.")
print(f"  5. What this does NOT show.  It does not rescue anything and it does not close the cluster problem, which")
print(f"     L9's T8 already left fatal on its own terms.  It does not exclude a NON-uniform or non-monotone")
print(f"     coupling, or a model where the lensing and dynamical potentials differ -- but such a model is no longer")
print(f"     the MODEL A tested here, owes an action, and inherits L9's own item (ii): if lensing and hydrostatic")
print(f"     cluster masses differ by of order F they are observed to agree to tens of percent.")
print(f"\n  WHAT DRIVES EACH FAIL, stated so nothing is over-read: C2, C3, C4, C5 and C7 all fail on reading (ii)")
print(f"  and ONLY on reading (ii).  On reading (i)/(i') -- the roll removed from the shear signal -- every one of")
print(f"  them passes, and the mechanism is alive in a corner:")
for foot in ("canonical", "alt"):
    s = SURV[foot]; m = s["full_naive"]
    if m.any():
        print(f"    {foot:9s} corner: z_t <= {s['zt'][m].max():.3f}, W in [{s['W'][m].min():.3f}, {s['W'][m].max():.3f}]  "
              f"({int(m.sum())}/{s['n']} of L9's region)")
        print(f"              sigma_8 {s['s8'][m].min():.3f}-{s['s8'][m].max():.3f}, S_8 {s['S8_naive'][m].min():.3f}-"
              f"{s['S8_naive'][m].max():.3f}, H0 {100*s['h'][m].min():.1f}-{100*s['h'][m].max():.1f}, Omega_m "
              f"{s['Om'][m].min():.3f}-{s['Om'][m].max():.3f}, Omega_Lambda {s['OL'][m].min():.3f}-{s['OL'][m].max():.3f}")
print(f"  C6 fails on its own terms and independently of the lensing question.")
print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else "")); sys.exit(0)
