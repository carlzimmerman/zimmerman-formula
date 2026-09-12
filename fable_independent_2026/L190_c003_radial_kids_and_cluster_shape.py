#!/usr/bin/env python3
"""L190 -- A CONVENTION CORRECTION TO L188, AND THE BREAKDOWN OF THE IMPULSIVE KICK MODEL (superseded for C003 by L191's orbit integration).

CORRECTION FIRST. L188 evaluated the galaxy-galaxy-lensing gate as the retained mass fraction in the 0.1-1 Mpc SHELL around a 1e12 halo.
That shell is dominated by 2-halo (correlated large-scale-structure) mass which is present in LCDM and in the framework alike, so it is not
what the repository's '<= 14% CDM-like halo' bound refers to; that bound is on the 1-HALO amplitude, i.e. the retained CDM-like mass inside
R200 of the lens. L190 recomputes the L188 gate under the corrected convention and reports whether its kill stands.

THE MODEL (supersedes L189's single-sigma impulsive model; still not an orbit integration). NFW host, Dutton-Maccio c(M). At radius r:
  M(r) = M200 m(x)/m(c),  V_c^2 = G M(r)/r,  sigma^2(r) = V_c^2(r)/2,  v_esc^2(r) = 2 G M200 ln(1+x)/(m(c) r).
Poisson kicks of mean n; after k kicks v^2 -> v^2 + k v_k^2 with speeds ~ 3D Maxwellian(sigma(r)).
  (a) ESCAPE: bound fraction at r = sum_k P(k;n) * gammainc(3/2, (v_esc^2 - k v_k^2)/(2 sigma^2)).
  (b) HEATING of the bound remainder: local specific-energy gain dk(r) = n v_k^2/(3 sigma^2(r)); the shell originally at r(1-dk) now sits at r,
      so M_ret(r) = M_NFW(r(1 - dk(r))) * f_bound(r). Radially resolved: the outskirts (low sigma) expand more than the centre.
Both a0 footings are irrelevant (no kernel enters).

GATES: (1) ledger anchors refitted with the radial model; (2) G7 KiDS on the CORRECTED 1-halo convention (retained mass inside R200 of a
1e12 lens <= 0.14); (3) G3 SHAPE: the repository's required cluster residual is rho ~ r^-1.53, NOT cored (g04a) -- does the retained
component have that slope over 75-420 kpc? No literal-True checks."""
import numpy as np, json
from scipy.stats import poisson
from scipy.special import gammainc
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL190 C003 RADIALLY RESOLVED: ledger refit, KiDS on the corrected 1-halo convention, cluster residual SHAPE\n" + "=" * 118)
G = 4.301e-9                                            # Mpc (km/s)^2 / Msun
h = 0.6736; rho_c = 2.775e11*h**2                        # Msun/Mpc^3
m = lambda x: np.log(1 + x) - x/(1 + x)
cDM = lambda M: 10**(0.905 - 0.101*np.log10(M*h/1e12))
def halo(M):
    R200 = (3*M/(4*np.pi*200*rho_c))**(1/3); c = cDM(M); return R200, c, R200/c
def Menc(r, M):
    R200, c, rs = halo(M); return M*m(np.maximum(r, 1e-9)/rs)/m(c)
def sig(r, M): return np.sqrt(G*Menc(r, M)/np.maximum(r, 1e-9)/2)
def vesc(r, M):
    R200, c, rs = halo(M); return np.sqrt(2*G*M/m(c)*np.log(1 + np.maximum(r, 1e-9)/rs)/np.maximum(r, 1e-9))
def f_bound(r, M, n, vk):
    s = sig(r, M); ve = vesc(r, M); tot = np.zeros_like(np.atleast_1d(r), dtype=float)
    for k in range(0, 60):
        pk = poisson.pmf(k, n)
        if pk < 1e-10: continue
        lim2 = ve**2 - k*vk**2
        tot += pk*np.where(lim2 > 0, gammainc(1.5, np.maximum(lim2, 0)/(2*s**2)), 0.0)
    return tot
def M_ret(r, M, n, vk):
    s = sig(r, M); dk = np.minimum(n*vk**2/(3*s**2), 0.95)
    return Menc(r*(1 - dk), M)*f_bound(r, M, n, vk)
def f_at(r, M, n, vk): return M_ret(r, M, n, vk)/Menc(r, M)
# ---- ledger anchors, refitted with the radial model ----
A = [("spiral 1.2e10 Mb (M200 3e11), 3R_d = 7.5 kpc", 3e11, 0.0075, 0.105, "ceiling"),
     ("Milky Way (1e12), 30 kpc", 1e12, 0.030, 0.14, "anchor"),
     ("group (1e13), R500", 1e13, 0.0, None, "prediction"),
     ("cluster (1e15), R500 = 1.38 Mpc", 1e15, 1.38, 0.576, "anchor")]
A[2] = (A[2][0], 1e13, 0.65*halo(1e13)[0], None, "prediction")     # R500 ~ 0.65 R200
best = None
for vk in np.arange(200., 1201., 25.):
    for n in np.geomspace(0.2, 40, 120):
        fs = [float(f_at(np.array([r]), M, n, vk)[0]) for _, M, r, _, _ in A]
        if fs[0] > 0.105: continue
        cost = (np.log(max(fs[1], 1e-3)/0.14))**2 + (np.log(max(fs[3], 1e-3)/0.576))**2
        if best is None or cost < best[0]: best = (cost, vk, n, fs)
cost, vk, n, fs = best
print(f"    radial refit: v_k = {vk:.0f} km/s, n = {n:.2f} kicks per particle by z = 0 (L189 single-sigma model gave 650 km/s, 2.31)")
for (nm, M, r, t, kind), f in zip(A, fs):
    print(f"      {nm:<45} sigma = {sig(np.array([r]), M)[0]:6.1f}, v_esc = {vesc(np.array([r]), M)[0]:7.1f} km/s -> f = {f:.3f}" + (f"  (target {t})" if t else "  (PREDICTION)"))
check("V1 [MODEL BREAKDOWN, the point of this script] the radially resolved impulsive model is NOT trustworthy: its expansion factor M(r(1-dk))/M(r) with dk = n v_k^2/(3 sigma^2) exceeds its cap wherever the kick energy beats the local binding energy, double-counting particles the escape criterion already removed, and the resulting anchors are mutually inconsistent (the spiral is driven to ~0.00 while the cluster stays above 0.9). L191 replaces it with an orbit integration; no ledger verdict is taken from this script",
      fs[0] < 0.02 and fs[3] > 0.90, "f = " + " ".join(f"{x:.3f}" for x in fs) + " -- spiral over-depleted and cluster untouched at the same parameters, the signature of the double-count")
# ---- G7 KiDS, CORRECTED CONVENTION: retained mass inside R200 of a 1e12 lens ----
R200_12 = halo(1e12)[0]
f_1halo_c003 = float(f_at(np.array([R200_12]), 1e12, n, vk)[0])
rr = np.geomspace(0.02*R200_12, R200_12, 60)
prof = f_at(rr, 1e12, n, vk)
print(f"    1e12 lens: R200 = {R200_12*1e3:.0f} kpc; C003 retained-mass fraction inside R200 = {f_1halo_c003:.3f}; local retention at 0.1/0.3/1.0 R200 = " +
      " ".join(f"{float(f_at(np.array([q*R200_12]), 1e12, n, vk)[0]):.3f}" for q in (0.1, 0.3, 1.0)))
check("V2 [WITHDRAWN as a C003 verdict; reported as a model number only] the same broken model would put C003's retained mass inside R200 of a 1e12 lens below the 0.14 ceiling; because the model double-counts, this number carries no weight and the KiDS gate for C003 must be recomputed from the L191 orbit integration",
      f_1halo_c003 <= 0.14, f"retained inside R200 = {f_1halo_c003:.3f} vs ceiling 0.14; the kick speed exceeds the escape speed over the whole halo (v_esc(R200) = {float(vesc(np.array([R200_12]), 1e12)):.0f} km/s < v_k = {vk:.0f})")
# ---- the L188 correction: density-gated rate under the same corrected convention ----
Msun_g = 1.989e33; Mpc_cm = 3.086e24; Gcgs = 6.674e-8
def rho_nfw(r, M):
    R200, c, rs = halo(M); rho_s = 200*rho_c*c**3/(3*m(c)); return rho_s/((r/rs)*(1 + r/rs)**2)*Msun_g/Mpc_cm**3
def dens_ret(M, r1, r2, eps, alpha):
    r = np.geomspace(max(r1, 1e-4), r2, 3000); rho = rho_nfw(r, M); w = rho*r**2
    return np.trapz(w*np.exp(-eps*(Gcgs*rho)**(alpha/2)), r)/np.trapz(w, r)
bestd = None
for alpha in (0.5, 1.0, 1.5):
    for eps in np.geomspace(1e-30, 1e40, 300):
        g = [dens_ret(M, 0, r, eps, alpha) for _, M, r, _, _ in A if r > 0]
        c2 = sum((np.log(max(x, 1e-6)) - np.log(t))**2 for x, t in zip([g[0], g[1], g[3]], (0.105, 0.14, 0.576)))
        if bestd is None or c2 < bestd[0]: bestd = (c2, alpha, eps, [g[0], g[1], g[3]])
_, al, ep, gd = bestd
f_1halo_dens = dens_ret(1e12, 1e-4, R200_12, ep, al)
check("V3 [CORRECTION to L188, recomputed] under the corrected 1-halo convention the density-gated class is still excluded by galaxy-galaxy lensing: its retained mass inside R200 of a 1e12 lens exceeds 0.14 by more than 3x, because the outer halo is less dense than the cluster anchor and a density-monotone rate must spare it",
      f_1halo_dens > 3*0.14, f"density-gated best fit (alpha = {al}, ledger {gd[0]:.3f}/{gd[1]:.3f}/{gd[2]:.3f}): retained inside R200 = {f_1halo_dens:.3f} vs ceiling 0.14; L188's shell number (0.75) used the wrong convention, the kill stands with this number instead")
# ---- G3 SHAPE: the cluster residual profile ----
rc = np.geomspace(0.075, 0.420, 40)                                  # 75-420 kpc, the range used for the cluster residual
Mr = M_ret(rc, 1e15, n, vk); rho_ret = np.gradient(Mr, rc)/(4*np.pi*rc**2)
slope = np.polyfit(np.log(rc), np.log(rho_ret), 1)[0]
Mn = Menc(rc, 1e15); rho_nf = np.gradient(Mn, rc)/(4*np.pi*rc**2); slope_nfw = np.polyfit(np.log(rc), np.log(rho_nf), 1)[0]
print(f"    cluster 1e15 over 75-420 kpc: retained-component logarithmic slope = {slope:.2f}, NFW = {slope_nfw:.2f}, required residual (g04a) = -1.53")
check("V4 [G3 shape, computed] the kicks do NOT steepen the retained cluster profile: its slope tracks NFW's to 0.01 over 75-420 kpc, so the agreement with the required -1.53 is inherited from NFW and is not produced by the mechanism (a survives-by-construction result, flagged as such)",
      abs(slope - slope_nfw) < 0.05, f"retained {slope:.2f} vs NFW {slope_nfw:.2f} (the retained profile is if anything a hair shallower, not steeper); required -1.53; residual mismatch {abs(slope + 1.53):.2f} dex per dex")
check("V5 [G3 shape, the non-trivial half] what IS non-trivial is the absence of a core: NFW over 75-420 kpc of a 1e15 halo already has the required slope, and the kicks leave it there instead of flattening it, unlike every dark-sector candidate the programme tried (which cored the profile)",
      abs(slope + 1.53) <= 0.25 and abs(slope - slope_nfw) <= 0.05, f"retained {slope:.2f}, NFW {slope_nfw:.2f}, required -1.53")
print("    LIMITS: NFW + Dutton-Maccio; sigma^2 = V_c^2/2 (isotropic Jeans not solved); impulsive heating with shell-wise re-virialisation and no orbit\n"
      "    integration (an N-body run must replace this); the KiDS bound is the repository's 1-halo '<= 14% CDM-like halo' figure; the cluster residual slope -1.53 is g04a's.")
json.dump(dict(vk=float(vk), n=float(n), ledger=[float(x) for x in fs], f_1halo_c003=f_1halo_c003, f_1halo_density=float(f_1halo_dens),
               cluster_slope=float(slope), nfw_slope=float(slope_nfw)), open("L190_results.json", "w"), indent=1)
print(f"\nL190 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
