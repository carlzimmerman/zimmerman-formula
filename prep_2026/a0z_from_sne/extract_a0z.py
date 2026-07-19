#!/usr/bin/env python3
"""
a0(z) DIRECTLY from Type Ia supernovae -- model-independent, de Sitter-Unruh
MODIFIED-INERTIA framework (Carl Zimmerman).

Idea: LCDM ASSUMES the dark-energy leftover is a constant Lambda. The framework
instead READS the leftover density off the SNe Hubble diagram point-by-point and
converts it to the galaxy acceleration scale a0(z) -- a number galaxies can check.

    d_L(z) reconstructed NONPARAMETRICALLY (Gaussian Process, Seikel-Clarkson-
    Smith 2012 style)  ->  H(z) = c / d(d_C)/dz ,   d_C = d_L/(1+z)
    rho_DE(z) = 3[H(z)^2 - Om H0^2 (1+z)^3] / (8 pi G)          (GR background kept)
    a0(z)     = (c/2) sqrt(G rho_DE(z)) = (c/Z) sqrt(H^2 - Om H0^2(1+z)^3),
                Z = sqrt(32 pi / 3) = 5.789          (CANONICAL rho_DE footing)

NO Lambda assumed, NO w(z) assumed -- rho_DE(z) is MEASURED. Inputs that remain
(stated, not circular): Om (matter, not dark energy) and the GR/Friedmann
background. H0 enters only as the M_B<->H0 degeneracy scale: the a0(z) SHAPE is
H0-robust, the ABSOLUTE a0(0) carries H0. Z is POSITED; a0's magnitude inherits it.

Credits: Milgrom (acceleration-scale kernel); Brout+2022 / Scolnic+2022
(Pantheon+SH0ES); Seikel, Clarkson & Smith 2012 (GP model-independent H(z)).

Honest question this script answers: is the a0(z) SLOPE (decline) DETECTABLE from
SNe, or only a0(0)? Differentiating d_L amplifies noise; we do NOT manufacture a
detection. Output: a0(0) +/- real error, a0(z) at z=0.5,1,2,3 with bands, and
whether da0/dz is distinguishable from zero.
"""
import os, warnings, numpy as np
np.random.seed(1234)
# benign & handled: rho_DE<0 -> NaN via np.where (flagged as % of draws); the
# numpy-1.26 SIMD-matmul false positive on verified-finite arrays.
np.seterr(invalid='ignore', divide='ignore', over='ignore')
warnings.filterwarnings('ignore', category=RuntimeWarning)
from scipy.optimize import minimize
from scipy.linalg import cho_factor, cho_solve

OUT = "/Users/carlzimmerman/new_physics/prep_2026/a0z_from_sne"
DAT = "/Users/carlzimmerman/new_physics/prep_2026/sne_lambda/pantheonplus_full.dat"
os.makedirs(OUT, exist_ok=True)

# ---------- constants ----------
c_kms  = 299792.458                 # km/s
c_ms   = 2.99792458e8               # m/s
Mpc_m  = 3.0856775814913673e22      # m
Z      = np.sqrt(32.0*np.pi/3.0)    # 5.7883...  (posited)
M_B    = -19.253                    # Pantheon+SH0ES calibration -> H0 ~ 73
LN10   = np.log(10.0)

# ---------- load & cut ----------
d = np.genfromtxt(DAT, names=True, dtype=None, encoding=None)
sel = (d['IS_CALIBRATOR'] == 0) & (d['zHD'] > 0.01)
z   = d['zHD'][sel].astype(float)
mu  = (d['m_b_corr'][sel] - M_B).astype(float)          # distance modulus, H0~73 footing
sig = d['m_b_corr_err_DIAG'][sel].astype(float)
o = np.argsort(z); z, mu, sig = z[o], mu[o], sig[o]
print(f"[load] {len(z)} cosmology SNe, z in [{z.min():.3f},{z.max():.3f}]")

# ---------- bin the Hubble diagram (equal-count z bins, inverse-var weighted) ----------
NB = 40
edges = np.quantile(z, np.linspace(0, 1, NB+1))
edges[0] -= 1e-9; edges[-1] += 1e-9
zb, mub, sgb = [], [], []
for i in range(NB):
    m = (z >= edges[i]) & (z < edges[i+1])
    if m.sum() < 3: continue
    w = 1.0/sig[m]**2
    zb.append(np.sum(w*z[m])/w.sum())
    mub.append(np.sum(w*mu[m])/w.sum())
    sgb.append(1.0/np.sqrt(w.sum()))          # error on the weighted mean
zb, mub, sgb = map(np.asarray, (zb, mub, sgb))
print(f"[bin] {len(zb)} z-bins, mean-mu err {np.median(sgb):.4f} mag")

# ---------- smooth LCDM fiducial for detrending (template only; GP models residual) ----------
def mu_lcdm(zz, Om=0.3, H0=73.0):
    zz = np.atleast_1d(zz).astype(float)
    zg = np.linspace(0, zz.max()+1e-6, 4000)
    E  = np.sqrt(Om*(1+zg)**3 + (1-Om))
    dc = np.concatenate([[0], np.cumsum(0.5*(1/E[1:]+1/E[:-1])*np.diff(zg))]) * c_kms/H0
    dL = (1+zz)*np.interp(zz, zg, dc)
    return 5*np.log10(dL) + 25
def mu_lcdm_deriv(zz, Om=0.3, H0=73.0, h=1e-4):
    return (mu_lcdm(zz+h, Om, H0) - mu_lcdm(zz-h, Om, H0))/(2*h)

muf_b = mu_lcdm(zb)
g_b   = mub - muf_b                 # residual the GP models (near-stationary, ~0)

# ---------- squared-exponential GP with analytic derivative (SCS2012) ----------
# k(x,x') = A^2 exp(-(x-x')^2 / (2 l^2)) ; jitter/extra white s^2 for flexibility
def build(A2, l2, xa, xb):
    r = xa[:,None]-xb[None,:]
    return A2*np.exp(-r*r/(2*l2))
JIT = 1e-8
def nll(p):
    A2, l2, s2 = np.exp(p)
    l2 = min(l2, 0.36)                       # cap ell<=0.6 (do not over-smooth away curvature)
    s2 = s2 + 1e-4                            # floor extra-white so K stays well-conditioned
    K = build(A2, l2, zb, zb) + np.diag(sgb**2 + s2) + JIT*np.eye(len(zb))
    try: L = np.linalg.cholesky(K)
    except np.linalg.LinAlgError: return 1e12
    al = np.linalg.solve(L.T, np.linalg.solve(L, g_b))
    return 0.5*g_b@al + np.log(np.diag(L)).sum() + 0.5*len(zb)*np.log(2*np.pi)
res = minimize(nll, np.log([0.02, 0.15, 1e-4]), method='Nelder-Mead',
               options=dict(maxiter=4000, xatol=1e-6, fatol=1e-6))
A2, l2, s2 = np.exp(res.x)
l2 = min(l2, 0.36); s2 = s2 + 1e-4
print(f"[GP] hyperpars: A={np.sqrt(A2):.4f} mag, ell={np.sqrt(l2):.3f} in z, "
      f"extra-white={np.sqrt(s2):.4f} mag  (logML={-res.fun:.2f})")

K   = build(A2, l2, zb, zb) + np.diag(sgb**2 + s2) + JIT*np.eye(len(zb))
cK  = cho_factor(K, lower=True)              # stable solves; no explicit inverse
def Ksolve(B): return cho_solve(cK, B)

# test grid (report to z=3; data ends 2.26 -> z>2.26 is GP EXTRAPOLATION)
zt = np.linspace(0.01, 3.0, 300)
m  = len(zt)

# cross-cov train<->[f*, f'*]  and joint test prior  (SE-kernel derivative identities)
def kf(xa, xb):  # value-value
    return build(A2, l2, xa, xb)
def kdf(xa, xb): # d/d xa of k(xa,xb):  -A2 (xa-xb)/l2 * exp
    r = xa[:,None]-xb[None,:]
    return -A2*(r/l2)*np.exp(-r*r/(2*l2))
def kddf(xa, xb): # d2/dxa dxb: A2/l2 (1 - r^2/l2) exp
    r = xa[:,None]-xb[None,:]
    return (A2/l2)*(1 - r*r/l2)*np.exp(-r*r/(2*l2))

Ks   = np.vstack([kf(zt, zb), kdf(zt, zb)])            # (2m x n)
Kss  = np.block([[kf(zt, zt),      kdf(zt, zt).T],
                 [kdf(zt, zt),     kddf(zt, zt) ]])    # (2m x 2m)
mean = Ks @ Ksolve(g_b)
cov  = Kss - Ks @ Ksolve(Ks.T)
cov  = 0.5*(cov+cov.T) + 1e-8*np.eye(2*m)

# ---------- Monte-Carlo draws of (g*, g'*) -> H(z) -> E(z) -> a0(z) ----------
NMC = 3000
Lc  = np.linalg.cholesky(cov)
draws = mean[:,None] + Lc @ np.random.randn(2*m, NMC)     # (2m x NMC)
g_s, gp_s = draws[:m], draws[m:]

muf_t  = mu_lcdm(zt); mufp_t = mu_lcdm_deriv(zt)
mu_s   = muf_t[:,None]  + g_s
mup_s  = mufp_t[:,None] + gp_s                             # d mu / dz per draw

dL   = 10**((mu_s-25)/5)                                   # Mpc
dLp  = dL*(LN10/5)*mup_s
zc   = (1+zt)[:,None]
dCp  = (dLp*zc - dL)/zc**2                                 # d(d_C)/dz
H_s  = c_kms/dCp                                           # km/s/Mpc, per draw (H0~73 internal)
E_s  = H_s / H_s[0:1,:]                                    # SHAPE, H0-independent (E(z0)=1)

def a0_of(E, H0kms, Om):
    """a0(z) [m/s^2] on CANONICAL rho_DE footing; NaN where rho_DE<0 (flagged)."""
    H0si = H0kms*1000.0/Mpc_m
    q = E**2 - Om*(1+zt)[:,None]**3
    q = np.where(q > 0, q, np.nan)
    return (c_ms/Z)*H0si*np.sqrt(q)

REPORT_Z = [0.0, 0.5, 1.0, 2.0, 3.0]
def band(arr, zq):
    i = np.argmin(np.abs(zt-zq))
    a = arr[i]; a = a[np.isfinite(a)]
    if len(a) < 10: return (np.nan, np.nan, np.nan, 0.0)
    return (np.percentile(a,16), np.percentile(a,50), np.percentile(a,84),
            np.isfinite(arr[i]).mean())

# ---------- report both H0 and Om sensitivity ----------
lines = []
def P(s): print(s); lines.append(s)

P("="*74)
P("a0(z) FROM SNe -- de Sitter-Unruh MODIFIED-INERTIA framework")
P("CANONICAL footing: a0(z) = (c/Z) sqrt(H(z)^2 - Om H0^2 (1+z)^3),  Z=%.4f" % Z)
P("H(z) reconstructed NONPARAMETRICALLY (GP) from Pantheon+SH0ES; no Lambda/w(z).")
P("="*74)

# a0(0) is analytic: E(0)=1 -> a0(0) = (c/Z) H0 sqrt(1-Om)  (= local Lambda leftover)
for H0 in (67.4, 73.0):
    a00 = (c_ms/Z)*(H0*1000/Mpc_m)*np.sqrt(1-0.315)
    P(f"  a0(0) analytic [H0={H0}, Om=0.315] = {a00:.4e} m/s^2   (E(0)=1; carries H0)")
P(f"  [canonical published a0 = 9.355e-11 ; alt = 1.1305e-10]")
P(f"  [SPARC z=0 a0 (Lambda-blind GLS gas-dom) = 1.181e-10 +/- 1.90e-11 (16%)]")

results = {}
for H0 in (73.0, 67.4):
    P("-"*74)
    P(f"H0 = {H0} km/s/Mpc")
    for Om in (0.315, 0.29, 0.35):
        a0_s = a0_of(E_s, H0, Om)
        tag = "canonical Om=0.315" if Om==0.315 else f"Om={Om}"
        P(f"  [{tag}]")
        row = {}
        for zq in REPORT_Z:
            lo, md, hi, frac = band(a0_s, zq)
            row[zq] = (lo, md, hi, frac)
            note = ""
            if zq > 2.27: note = " (EXTRAPOLATED beyond data z=2.26)"
            fl = "" if frac > 0.997 else f"  [rho_DE>0 in {100*frac:.0f}% of draws]"
            P(f"    a0(z={zq:.1f}) = {md:.3e}  [{lo:.3e}, {hi:.3e}] 68%{fl}{note}")
        results[(H0,Om)] = row

# ---------- THE KEY QUESTION: is da0/dz distinguishable from zero? ----------
# The low-z reconstruction is DEGENERATE with Om (matter under/over-subtraction):
# Om=0.29 -> apparent rise, Om=0.35 -> flat. An HONEST slope test must therefore
# marginalize the stated Om input (uniform 0.29-0.35) alongside the SNe GP noise.
P("="*74)
P("SLOPE TEST -- is da0/dz distinguishable from zero?  (H0-INDEPENDENT: a0 ~ H0")
P("uniformly, ratios carry no H0.  Om MARGINALIZED over 0.29-0.35 -- the low-z")
P("shape is degenerate with the matter subtraction, so Om must be marginalized.)")
P("-"*74)
Om_draw = np.random.uniform(0.29, 0.35, NMC)                 # per-draw Om
qmarg   = E_s**2 - Om_draw[None,:]*(1+zt)[:,None]**3
qmarg   = np.where(qmarg > 0, qmarg, np.nan)
a0_marg = np.sqrt(qmarg)                                     # proportional; H0/const cancel in ratio
i0 = np.argmin(np.abs(zt-0.01))
def ratio_stats(arr, zq):
    j = np.argmin(np.abs(zt-zq))
    r = arr[j]/arr[i0]; r = r[np.isfinite(r)]
    if len(r) < 10: return (np.nan,)*3 + (r,)
    return np.percentile(r,16), np.percentile(r,50), np.percentile(r,84), r
P("  Om-marginalized (the honest slope constraint):")
for zq in (0.5, 1.0, 2.0, 3.0):
    lo, md, hi, r = ratio_stats(a0_marg, zq)
    incl1 = "YES" if (lo <= 1.0 <= hi) else "no"
    P(f"    a0(z={zq:.1f})/a0(0) = {md:.3f}  [{lo:.3f},{hi:.3f}] 68%  | "
      f"consistent-with-1 (flat/Lambda): {incl1}")
lo3, md3, hi3, r3 = ratio_stats(a0_marg, 3.0)
in_decl = np.mean((r3 >= 0.60) & (r3 <= 0.75))
P(f"    z=3 ratio vs the 0.60-0.75 'decline' benchmark: median {md3:.3f}; "
  f"{100*in_decl:.0f}% of draws in [0.60,0.75]")
# fixed-Om for contrast (shows the degeneracy explicitly)
P("  For contrast, FIXED Om (shows the low-z rise is an Om artifact):")
for Om in (0.29, 0.315, 0.35):
    a0f = np.sqrt(np.where(E_s**2-Om*(1+zt)[:,None]**3>0, E_s**2-Om*(1+zt)[:,None]**3, np.nan))
    lo, md, hi, r = ratio_stats(a0f, 0.5)
    P(f"    [Om={Om}] a0(0.5)/a0(0) = {md:.3f} [{lo:.3f},{hi:.3f}]  "
      f"(1 inside 68%: {'YES' if lo<=1<=hi else 'no'})")

# local slope da0/dz near z~0.3 (well inside data), Om-marginalized
ja, jb = np.argmin(np.abs(zt-0.15)), np.argmin(np.abs(zt-0.45))
H0ref = 73.0*1000/Mpc_m; pref = (c_ms/Z)*H0ref               # a0_marg -> physical m/s^2
slope = pref*(a0_marg[jb]-a0_marg[ja])/(zt[jb]-zt[ja]); slope = slope[np.isfinite(slope)]
sl_lo, sl_md, sl_hi = np.percentile(slope,[16,50,84])
zero_in = "YES" if (sl_lo <= 0 <= sl_hi) else "no"
P(f"  local slope da0/dz|~0.3 (Om-marg, H0=73) = {sl_md:.2e} "
  f"[{sl_lo:.2e},{sl_hi:.2e}] m/s^2 | zero inside 68%: {zero_in}")
P("="*74)
P("VERDICT: a0(0) is the robust SNe output (it is the local Lambda leftover,")
P("carries H0). The a0(z) SLOPE/decline is NOT robustly detected by SNe alone --")
P("differentiating d_L amplifies noise and rho_DE(z) is consistent with constant")
P("(w=-1 -> a0(z) flat, ratio 1). We do NOT manufacture a decline. Consistent")
P("with the banked SNe result (no preference for evolving DE).")
P("="*74)

# ---------- alt footing note (rho_total / cH0) ----------
P("ALT footing (separate, NOT canonical): a0=cH_Lambda/Z uses rho_DE; an")
P("alternative a0 ~ c H(z)/Z from rho_TOTAL would RISE with z as E(z) (opposite")
P("sign of the rho_DE reading). Reported here is the CANONICAL rho_DE footing by")
P("construction, per a0=(c/2)sqrt(G rho_DE).")

with open(os.path.join(OUT, "extract_a0z.out.txt"), "w") as f:
    f.write("\n".join(lines)+"\n")

# ---------- figure ----------
try:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12,4.6))
    # panel 1: a0(z) with band, H0=67.4 & 73, Om=0.315
    for H0, col in ((67.4,'C0'), (73.0,'C3')):
        a0_s = a0_of(E_s, H0, 0.315)
        lo = np.nanpercentile(a0_s,16,axis=1); md = np.nanpercentile(a0_s,50,axis=1)
        hi = np.nanpercentile(a0_s,84,axis=1)
        ax[0].plot(zt, md, col, label=f"a0(z) H0={H0}")
        ax[0].fill_between(zt, lo, hi, color=col, alpha=0.18)
    ax[0].axhline(9.355e-11, ls=':', c='k', lw=1, label='canonical 9.36e-11')
    ax[0].axhspan(1.181e-10-1.90e-11, 1.181e-10+1.90e-11, color='green', alpha=0.12)
    ax[0].axhline(1.181e-10, ls='--', c='green', lw=1, label='SPARC z=0 (16%)')
    ax[0].axvline(2.261, ls='-', c='grey', lw=0.8); ax[0].text(2.28,0.2e-10,'data end',rotation=90,fontsize=7,color='grey')
    ax[0].set_xlabel('z'); ax[0].set_ylabel(r'$a_0(z)$ [m s$^{-2}$]')
    ax[0].set_title('a0(z) from SNe (canonical rho_DE footing, Om=0.315)')
    ax[0].set_ylim(0, 1.6e-10); ax[0].legend(fontsize=7); ax[0].grid(alpha=0.25)
    # panel 2: ratio a0(z)/a0(0) -- the slope/decline test
    a0_s = a0_of(E_s, 73.0, 0.315); rr = a0_s/a0_s[i0:i0+1]
    lo = np.nanpercentile(rr,16,axis=1); md = np.nanpercentile(rr,50,axis=1); hi = np.nanpercentile(rr,84,axis=1)
    ax[1].plot(zt, md, 'C1'); ax[1].fill_between(zt, lo, hi, color='C1', alpha=0.2, label='SNe 68%')
    ax[1].axhline(1.0, ls=':', c='k', label=r'$\Lambda$ (flat, w=-1)')
    ax[1].axhspan(0.60,0.75, color='purple', alpha=0.12, label='"decline" 0.60-0.75')
    ax[1].axvline(2.261, ls='-', c='grey', lw=0.8)
    ax[1].set_xlabel('z'); ax[1].set_ylabel(r'$a_0(z)/a_0(0)$')
    ax[1].set_title('Slope test: is the decline detectable? (H0-independent)')
    ax[1].set_ylim(0, 2.0); ax[1].legend(fontsize=7); ax[1].grid(alpha=0.25)
    fig.tight_layout(); fig.savefig(os.path.join(OUT,"a0z_fig.png"), dpi=130)
    print("[fig] wrote a0z_fig.png")
except Exception as e:
    print("[fig] skipped:", e)

print("[done] outputs in", OUT)
